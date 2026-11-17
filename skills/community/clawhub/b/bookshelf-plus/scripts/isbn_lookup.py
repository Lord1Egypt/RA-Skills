#!/usr/bin/env python3
"""
ISBN 多源查詢腳本
優先順序：Open Library → Google Books
返回：書名、作者、出版社、出版年、封面 URL、總頁數
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error


def lookup_open_library(isbn: str) -> dict | None:
    """查詢 Open Library API"""
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        key = f"ISBN:{isbn}"
        if key not in data or not data[key]:
            return None
        book = data[key]
        return {
            "title": book.get("title", ""),
            "authors": [a.get("name", "") for a in book.get("authors", [])],
            "publisher": book.get("publishers", [{}])[0].get("name", "") if book.get("publishers") else "",
            "publish_date": book.get("publish_date", ""),
            "cover_url": book.get("cover", {}).get("large", "") or book.get("cover", {}).get("medium", "") or "",
            "pages": book.get("number_of_pages", 0),
            "source": "Open Library",
        }
    except Exception as e:
        print(f"[OL] 查詢失敗: {e}", file=sys.stderr)
        return None


def lookup_google_books(isbn: str) -> dict | None:
    """查詢 Google Books API"""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        items = data.get("items", [])
        if not items:
            return None
        info = items[0].get("volumeInfo", {})
        authors = info.get("authors", [])
        return {
            "title": info.get("title", ""),
            "authors": authors,
            "publisher": info.get("publisher", ""),
            "publish_date": info.get("publishedDate", ""),
            "cover_url": info.get("imageLinks", {}).get("thumbnail", "").replace("http://", "https://"),
            "pages": info.get("pageCount", 0),
            "source": "Google Books",
        }
    except Exception as e:
        print(f"[GB] 查詢失敗: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="多源 ISBN 查詢")
    parser.add_argument("--isbn", required=True, help="ISBN-10 或 ISBN-13")
    args = parser.parse_args()

    isbn = args.isbn.strip().replace("-", "").replace(" ", "")

    # 1. Open Library
    result = lookup_open_library(isbn)
    if result and result.get("title"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 2. Google Books fallback
    result = lookup_google_books(isbn)
    if result and result.get("title"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 3. 皆失敗
    print(json.dumps({"error": "未找到書籍資訊，請嘗試手動輸入"}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
