import requests
from bs4 import BeautifulSoup
import json

def fetchPage(page_number):
    url = f'https://books.toscrape.com/catalogue/page-{page_number}.html'
    response = requests.get(url)
    # https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup
    # soup = BeautifulSoup(response.text) # if "html.parser" is not passed you will receive an warning.
    soup = BeautifulSoup(response.text, "html.parser")

    # print(soup.prettify())

    books = []
    book_elements = soup.find_all('article', class_='product_pod')

    for el in book_elements:
        title = el.find('h3').find('a')['title']
        # https://beautiful-soup-4.readthedocs.io/en/latest/#the-string-argument
        price = el.find('p', class_='price_color').text
        stock = 'In Stock' if el.find('p', class_='instock availability').text else 'Out of Stock'
        rating = el.find('p', class_='star-rating')['class'][1]
        link = el.find('h3').find('a')['href']

        books.append({
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating,
            'link': f'https://books.toscrape.com/catalogue/{link}'
        })
    return books


def main():
    all_books = []
    max_pages = 10

    for current_page in range(1, max_pages + 1):
        books = fetchPage(1)
        all_books.append(books)

        print(f'Books on {current_page}: {books}')
    
    # save data to json file
    with open('books.json', 'w') as file:
        json.dump(all_books, file, indent=2)

    print("Books saved to JSON file")


if __name__ == '__main__':
    main()
