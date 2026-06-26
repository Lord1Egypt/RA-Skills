---
name: buku
description: |
  Manage bookmarks using buku CLI. Use when: adding/saving URLs, searching bookmarks,
  listing/browsing saved links, tagging bookmarks, importing/exporting bookmarks,
  deleting bookmarks, or when user says "bookmark", "save this link", "find that link",
  "my bookmarks", "saved links".
---

# buku — Bookmark Manager

CLI bookmark manager with SQLite backend. Always use `--nostdin` and `--np` flags to prevent interactive prompts.

## Common Operations

### Add bookmark
```bash
buku --nostdin -a "URL" --tag tag1,tag2 --title "Title" -c "Description"
```
Omit `--title` to auto-fetch from web. Use `--offline` to skip fetching.

### Search
```bash
# Any keyword
buku --nostdin --np -s keyword1 keyword2

# All keywords
buku --nostdin --np -S keyword1 keyword2

# By tag (ANY match with comma, ALL match with +)
buku --nostdin --np -t tag1,tag2
buku --nostdin --np -t tag1+tag2

# Regex
buku --nostdin --np -r "pattern"

# Deep search (substring matching)
buku --nostdin --np -s keyword --deep
```

### List/Print
```bash
# Last N bookmarks
buku --nostdin --np -p -5

# All bookmarks
buku --nostdin --np -p

# Specific index
buku --nostdin --np -p 42

# JSON output (preferred for parsing)
buku --nostdin --np -p -j

# Limit fields: 1=URL, 2=URL+tag, 3=title, 4=URL+title+tag, 5=title+tag
buku --nostdin --np -p -f 4
```

### List all tags
```bash
buku --nostdin --np -t
```

### Update bookmark
```bash
# Update fields at index
buku --nostdin -u INDEX --url "NEW_URL" --title "New Title" --tag tag1,tag2

# Append tags
buku --nostdin -u INDEX --tag + newtag1,newtag2

# Remove tags
buku --nostdin -u INDEX --tag - oldtag

# Refresh title/description from web
buku --nostdin -u INDEX
```

### Delete
```bash
# By index (use --tacit to skip confirmation)
buku --nostdin --tacit -d INDEX

# Range
buku --nostdin --tacit -d 10-20
```

### Import/Export
```bash
# Import from browser
buku --nostdin --ai

# Import from file (.html, .md, .json, .org, .db)
buku --nostdin -i bookmarks.html

# Export to markdown
buku --nostdin -e bookmarks.md

# Export search results
buku --nostdin -s keyword -e results.md
```

### Tag management
```bash
# Replace tag everywhere
buku --nostdin --replace oldtag newtag

# Delete tag everywhere
buku --nostdin --replace oldtag
```

## Important Notes

- **Always use `--nostdin`** as first arg to prevent waiting for input
- **Always use `--np`** for search/print to skip interactive prompt
- **Use `--tacit`** for delete operations to skip confirmation
- **Use `-j`** for JSON output when parsing results programmatically
- DB location: `~/.local/share/buku/bookmarks.db`
