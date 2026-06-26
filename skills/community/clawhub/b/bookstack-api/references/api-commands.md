# BookStack API Commands Reference

Full command reference for `scripts/bookstack.py`.

## Table of Contents

- [Books](#books)
- [Chapters](#chapters)
- [Pages](#pages)
- [Shelves](#shelves)
- [Search](#search)

## Books

```bash
list_books [--count N]                          # List all books
get_book <id>                                    # Book details with contents
create_book "Name" ["Description"]               # Create a book
update_book <id> [--name "Name"] [--description "Desc"]
delete_book <id>                                 # Delete a book
```

## Chapters

```bash
list_chapters [--count N]                        # List all chapters
get_chapter <id>                                 # Chapter details with pages
create_chapter --book-id <id> --name "Name" [--description "Desc"]
update_chapter <id> [--name] [--description] [--book-id <id>]
delete_chapter <id>
```

## Pages

```bash
list_pages [--count N]                           # List all pages
get_page <id>                                    # Page preview (text snippet)
get_page <id> --content                          # Full HTML content
get_page <id> --markdown                         # Markdown content

# Create in a book or chapter
create_page --book-id <id> --name "Name" --html "<p>HTML</p>"
create_page --chapter-id <id> --name "Name" --markdown "# Markdown"
create_page --book-id <id> --name "Name" --content "Auto-detect HTML/MD"

# Update
update_page <id> --html "<p>New HTML</p>"
update_page <id> --markdown "# New Markdown"
update_page <id> --name "New Title"
update_page <id> --book-id <new-book-id>         # Move to another book
update_page <id> --chapter-id <new-chapter-id>   # Move to another chapter

delete_page <id>
```

### Content detection

The `--content` flag auto-detects format:
- Starts with `#` or contains no `<` → treated as Markdown
- Otherwise → treated as HTML

## Shelves

```bash
list_shelves [--count N]                         # List all shelves
get_shelf <id>                                   # Shelf details with books
create_shelf "Name" ["Description"]
```

## Search

```bash
search "query"                                   # Search all content
search "query" --type page                       # Pages only
search "query" --type book                       # Books only
search "query" --type chapter                    # Chapters only
search "query" --type shelf                      # Shelves only
search "query" --count 50                        # Max results (default: 20)
```

## Programmatic Usage

For complex operations (e.g., reading a page, modifying HTML, updating), use the script's `api_call()` function directly from Python:

```python
import subprocess, json

# Read page HTML
result = subprocess.run(
    ["python3", "scripts/bookstack.py", "get_page", "24", "--content"],
    capture_output=True, text=True, env={...}
)

# Or use curl for Cloudflare-protected instances
# curl -s -H "Authorization: Token ID:SECRET" \
#   "https://bookstack.example.com/api/pages/24" | python3 -c "..."
```

## API Endpoints

| Resource | List | Read | Create | Update | Delete |
|----------|------|------|--------|--------|--------|
| Books | GET /api/books | GET /api/books/{id} | POST /api/books | PUT /api/books/{id} | DELETE /api/books/{id} |
| Chapters | GET /api/chapters | GET /api/chapters/{id} | POST /api/chapters | PUT /api/chapters/{id} | DELETE /api/chapters/{id} |
| Pages | GET /api/pages | GET /api/pages/{id} | POST /api/pages | PUT /api/pages/{id} | DELETE /api/pages/{id} |
| Shelves | GET /api/shelves | GET /api/shelves/{id} | POST /api/shelves | PUT /api/shelves/{id} | DELETE /api/shelves/{id} |
| Search | GET /api/search?query= | — | — | — | — |

Auth header: `Authorization: Token {TOKEN_ID}:{TOKEN_SECRET}`
