# Workflow

1. Load the latest delivered workbook if available; otherwise load the latest automation-created workbook; otherwise load the template
2. Determine run mode: regular daily or ad hoc range
3. Determine target order range
4. Access BUYMA in Chrome default profile
5. Check and input receipt memo numbers for target orders
6. Download shipping CSV or accept a manual CSV fallback from the operator
7. Parse CSV with `scripts/parse_buyma_csv.py`
8. Build draft workbook with `scripts/build_order_sheet.py`
9. Fill F using Chrome auto-translated Korean product names
10. Enrich I/J/M from prior workbook history with `scripts/enrich_from_history.py`
11. Validate workbook with `scripts/validate_output.py`
12. Compose output name with `scripts/compose_output_filename.py`
13. Send by Naver Mail in Chrome with subject `buyma 주문서 초안 -YYMMDD (start-end)`
14. Update `last_state.json` with `scripts/update_state.py`
15. On BUYMA/CSV/mail failure, stop immediately and notify via Telegram with file attachment if available
