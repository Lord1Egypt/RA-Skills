---
name: ebook-search
description: >
  Search and download ebooks from jbiaojerry.github.io/ebook-treasure-chest.
  Use when the user wants to find ebooks, search for books by title/author/category,
  get download links, or browse the 24,000+ book collection.
  Supports epub, mobi, azw3 formats. Chinese and English books available.
  USE FOR: search ebooks, find books, download ebooks, book recommendations,
  ebook collection, 电子书搜索, 电子书下载.
---

# Ebook Search 📚

Search and download ebooks from jbiaojerry.github.io/ebook-treasure-chest (24,000+ books).

## Quick Start

```bash
# Search for books
python3 scripts/ebook-db.py search "武侠"

# Search with category filter
python3 scripts/ebook-db.py search "科幻" --category "科幻"

# Limit results
python3 scripts/ebook-db.py search "python" -l 10

# Update the database cache
python3 scripts/ebook-db.py update

# Show database stats
python3 scripts/ebook-db.py stats

# List all categories
python3 scripts/ebook-db.py categories
```

## How It Works

1. Downloads `all-books.json` from the website (~5MB)
2. Caches locally at `~/.cache/ebook-search/all-books.json`
3. Cache refreshes every 24 hours automatically
4. Searches by title, author, and category (case-insensitive, multi-word)

## Book Data Structure

Each book has:
- `title` - Book title
- `author` - Author name
- `category` - Genre/category (武侠, 科幻, 文学, etc.)
- `link` - Download URL (ctfile.com/城通网盘)
- `formats` - Available formats (epub, mobi, azw3)
- `language` - Language code (ZH, EN)

## Workflow

1. Run `search` with user's query
2. Present results in a readable format
3. When user picks a book, show the download link
4. If user wants more results, increase `-l` limit or refine keywords

## Tips

- Use multiple keywords for better results (e.g., "金庸 武侠")
- Check `categories` first to find the right genre
- Run `update` if searches return stale results
- The download links are on ctfile.com (城通网盘) - users need to visit them in browser
