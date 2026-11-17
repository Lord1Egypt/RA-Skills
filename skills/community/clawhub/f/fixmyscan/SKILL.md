---
name: fixmyscan
description: Turn a scanned book (PDF or DjVu, up to 1,000 pages) into a clean, searchable PDF for Kindle and e-readers with FixMyScan. Use when the user wants to fix, clean up, OCR, crop, straighten, split two-page spreads in, or convert a scanned book for an e-reader.
---

# FixMyScan

FixMyScan crops scanned pages to the text, straightens them, turns them into sharp black and white (or gentle greyscale), splits two-page spreads and adds a searchable text layer. It keeps every page and illustration. Files are deleted 24 hours after a book is ready.

## In an AI app (MCP)

1. Connect the remote MCP server `https://mcp.fixmyscan.com/mcp` (OAuth sign-in; the tool list is readable without signing in).
2. Call `fix_scan` with exactly one source: `file` (an attachment the app passes), `source_url` (a public https link to the PDF or DjVu) or `upload_id` (from `create_upload_link`).
3. If the file is attached but the app cannot pass attachments to tools, call `create_upload_link` at once and show the user the link or upload box; then call `fix_scan` with the `upload_id`.
4. Poll `get_scan_status` with the `scan_id` every 10 to 20 seconds until the state is `ready`, then give the user `download_url`.
5. `preview_scan` shows before-and-after images of 3 pages first; `cancel_scan` and `delete_scan` stop or remove a book.

## From code (REST API)

- Base URL `https://api.fixmyscan.com/v1`, header `Authorization: Bearer fms_live_...` (keys at https://app.fixmyscan.com/account).
- `POST /v1/books` with `{"source_url": "...", "webhook_url": "..."}` starts a book; `GET /v1/books/{id}` reports progress and the download link; the webhook posts `book.ready` or `book.failed`, signed in `FixMyScan-Signature`.
- Full reference: https://api.fixmyscan.com/openapi.json and https://fixmyscan.com/llms-full.txt

## Options

`trim_margins` (default true), `split_spreads` (default true), `output` `bw` or `grey`, `language` (default `auto`).
