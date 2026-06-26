---
name: annas-archive
description: Find and download ebooks or papers from Anna's Archive with EPUB-first selection and /tmp storage. Use when a user asks to fetch a book/article, especially when arXiv has no result.
---

# annas-archive

## Workflow
1. Search and rank (EPUB-first):
   - `scripts/anna_epub_first.py --query "<query>"`
2. Download when requested:
   - `scripts/anna_epub_first.py --query "<query>" --download`
3. If no matching book exists, report that in chat and stop.

Optional raw MCP search:
- `mcporter call anna.book_search query="<query>"`

## Runtime
- Runner: `scripts/run-annas-mcp.sh`
- Downloads: `/tmp/annas-archive-downloads`
- Cleanup: `scripts/cleanup_annas_tmp.sh`
- Optional env: `ANNAS_MCP_COMMAND` or `ANNAS_MCP_SOURCE_DIR`
