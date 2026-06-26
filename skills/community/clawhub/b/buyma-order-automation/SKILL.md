---
name: buyma-order-automation
description: automate buyma order processing for regular daily runs and ad hoc order-range runs. use when chatgpt needs to access buyma in chrome, check or fill receipt memo numbers, download or use a provided buyma csv, write the tmazon order workbook, enrich rows from prior workbook history, and send the result by naver mail before a deadline or after an ad hoc request. stop immediately and notify by telegram with file attachment on buyma, csv, or mail failure.
---

# Overview

This skill supports two modes:

1. Regular daily draft creation
- Start time can vary
- Must ensure mail is sent by 08:30 local time
- Orders up to 07:00 must be included
- Orders from 07:00 to 08:00 should be included as much as feasible while still guaranteeing mail send by 08:30
- If any critical failure occurs, stop immediately and notify via Telegram

2. Ad hoc range creation
- Triggered when the operator requests a specific order-number range
- Example: 123450~123470
- Complete the draft for that range
- Notify via Telegram immediately after completion
- Send mail immediately after completion

## Core rules

- Always use Chrome default profile for BUYMA and Naver Mail
- Use the latest delivered workbook first; otherwise use the latest automation-created workbook
- Start from the last order number in the most recently delivered file from the operator. If no new delivered file exists, continue from the last workbook previously created by the automation
- If BUYMA CSV download fails, allow operator-provided CSV as fallback input
- If mail sending fails, notify and attach the result file in Telegram fallback
- Follow MEMORY.md and recent memory logs before acting

## Base file selection

Select the base order workbook in this order:
1. latest file in `~/.openclaw/workspace/buyma_order/orders/incoming/`
2. latest file in `~/.openclaw/workspace/buyma_order/orders/current/`
3. `~/.openclaw/workspace/buyma_order/templates/tmazonORDERLIST_template.xlsx`

## Output file naming

Always save output as:
`tmazonORDERLISTYYMMDD_start-end.xlsx`

Example:
`tmazonORDERLIST260307_123450-123470.xlsx`

## Receipt memo numbering

Always check memo state for target orders.

- If memo already contains a valid 6-digit order number, do not rewrite it
- If memo contains text or a number shorter than 6 digits, prepend the 6-digit order number before the existing memo content
- In ad hoc range mode, always perform the memo check/input step

See `references/memo-rules.md`.

## Workflow

1. Determine run mode: regular daily or ad hoc range
2. Select base workbook
3. Access BUYMA in Chrome default profile
4. Check and input receipt memo numbers for target orders
5. Download shipping CSV (or use provided CSV fallback)
6. Parse CSV using `scripts/parse_buyma_csv.py`
7. Build draft workbook using `scripts/build_order_sheet.py`
8. Fill F using Chrome auto-translated Korean product names (browser placeholder step)
9. Enrich I/J/M from prior workbook history using `scripts/enrich_from_history.py`
10. Validate output using `scripts/validate_output.py`
11. Save output using `scripts/compose_output_filename.py`
12. Send by Naver Mail in Chrome (browser placeholder step)
13. Update state using `scripts/update_state.py`
14. On BUYMA/CSV/mail failure, stop immediately and notify via Telegram with file attachment if available

## Browser placeholder steps

This package intentionally leaves browser-only steps as placeholders:
- BUYMA login and page navigation
- Receipt memo editing in BUYMA UI
- BUYMA CSV download click-flow
- Product page Korean name capture from Chrome auto-translation
- Naver Mail compose/send
- Telegram file attachment send from browser/channel tool path

Use these references:
- `references/workflow.md`
- `references/failure-rules.md`
- `references/run-modes.md`

## Script entrypoints

- `scripts/select_base_file.py`
- `scripts/parse_buyma_csv.py`
- `scripts/build_order_sheet.py`
- `scripts/enrich_from_history.py`
- `scripts/validate_output.py`
- `scripts/compose_output_filename.py`
- `scripts/update_state.py`
