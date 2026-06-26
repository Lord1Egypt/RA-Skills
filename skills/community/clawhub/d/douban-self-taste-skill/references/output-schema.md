# Output schema

Use JSON as the primary local storage and exchange format.

## Cache file schema

```json
{
  "platform": "douban",
  "owner": "self",
  "subject_type": "book",
  "fetched_at": "2026-03-13T13:20:00Z",
  "source": {
    "kind": "logged-in-crawl",
    "cookie_file": ".local/douban-self-taste/cookies/douban_cookies.json"
  },
  "items": [
    {
      "title": "故事新编",
      "url": "https://book.douban.com/subject/1234567/",
      "douban_id": "1234567",
      "subject_type": "book",
      "status": "done",
      "rating": 5,
      "date": "2024-08-03",
      "tags": ["鲁迅", "小说"],
      "comment": "短，但很狠。",
      "creators": ["鲁迅"],
      "year": "1936",
      "raw_meta": {
        "source_page": "https://book.douban.com/people/example/collect"
      }
    }
  ],
  "count": 1
}
```

## Analysis summary schema

```json
{
  "platform": "douban",
  "owner": "self",
  "focus_type": "book",
  "source_files": [
    ".local/douban-self-taste/cache/collections/book.json"
  ],
  "stats": {
    "total_items": 86,
    "by_type": {
      "book": 86
    },
    "by_status": {
      "done": 52,
      "wish": 28,
      "doing": 6
    },
    "ratings": {
      "1": 1,
      "2": 4,
      "3": 21,
      "4": 35,
      "5": 25
    },
    "date_range": {
      "from": "2019-01-05",
      "to": "2026-03-10"
    }
  },
  "high_rated_items": [],
  "low_rated_items": [],
  "commented_items": [],
  "recent_items": []
}
```

## Notes

- Use JSON, not SQLite, as the default local persistence format for this skill.
- Keep `fetched_at` at the top level of every cache file.
- Keep category explicit with `subject_type`.
