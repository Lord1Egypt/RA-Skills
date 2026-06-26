# TOOLS.md

## Feishu Review Delivery

- Review channel: Feishu DM
- Target open_id comes from env: `XHS_REVIEW_OPEN_ID`

## Local Search

Use your local search helper first.

Example:

`python3 scripts/local_search.py "<query>"`

## Publish Assist

Preview-only by default:

`python3 scripts/publish_approved_note.py --input <draft.json>`

Live publish only after explicit approval:

`python3 scripts/publish_approved_note.py --input <draft.json> --allow-live --confirm-title "<exact title>"`

## Memory

Write daily memory after finalizing the review package:

`python3 scripts/write_memory_entry.py --input <memory.json>`
