---
name: doc-mcp
description: >-
  Search, browse, and read Doctor of Credit bank bonus and credit card posts.
  Use when the user wants to find bank account bonuses, credit card offers,
  brokerage deals, or any personal finance content from doctorofcredit.com.
  Tools: doc_search, doc_read_post, doc_hot_posts, doc_list_categories,
  doc_category_posts.
homepage: https://github.com/Guava-Tech-LLC/DoC-mcp
metadata:
  openclaw:
    emoji: "💳"
    mcpServers:
      doc-mcp:
        command: npx
        args: ["-y", "@guava-tech/doc-mcp"]
---

# Doctor of Credit MCP

Search, browse, and read posts from [Doctor of Credit](https://www.doctorofcredit.com/) — the leading source for bank account bonuses, credit card offers, and personal finance deals.

## Tools

| Tool | Purpose |
|------|---------|
| `doc_search` | Search posts by keyword, optionally filter by category |
| `doc_read_post` | Read a post by ID or slug, with comments |
| `doc_hot_posts` | Get trending posts within recent days |
| `doc_list_categories` | List all DoC categories with post counts |
| `doc_category_posts` | Browse posts in a specific category |

## Usage Patterns

### When the user asks about bank bonuses
1. Use `doc_search` with the bank name + "bonus" as query
2. Or use `doc_category_posts --category "bank-accounts"` to browse recent bank deals
3. Use `doc_read_post` on interesting results to get full details
4. Use `doc_hot_posts` to find trending/active deals

### When the user asks about credit cards
1. Use `doc_category_posts --category "credit-cards"` for recent offers
2. Use `doc_search --query "chase sapphire"` for specific cards
3. Use `doc_read_post` to get full terms and community comments

### Quick discovery
- `doc_list_categories` — see all available categories
- `doc_hot_posts --days 7` — what's trending this week

## Example Queries

```
doc_search --query "chase checking $300" --category bank-accounts
doc_read_post --id 12345
doc_hot_posts --days 14 --limit 10
doc_category_posts --category credit-cards --per_page 5
doc_list_categories
```

## Notes

- DoC is a WordPress site; all data comes from the WordPress REST API — no scraping
- Posts are listed newest-first by default
- Categories include: bank-accounts, credit-cards, brokerage, insurance, loans, and more
- The `doc_read_post` tool accepts either numeric post ID or URL slug

## Requirements

- Node.js >= 18 (for the MCP server)
- Internet access to doctorofcredit.com

## Source

- GitHub: https://github.com/Guava-Tech-LLC/DoC-mcp
- npm: https://www.npmjs.com/package/@guava-tech/doc-mcp
