---
name: agent-paddleocr-vision
description: Multi-language document understanding with PaddleOCR
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_DOC_PARSING_API_URL
        - PADDLEOCR_ACCESS_TOKEN
      bins:
        - python
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "👁️"
    homepage: https://github.com/NHZallen/agent-paddleocr-vision
---

# Agent PaddleOCR Vision

**OCR with Agent Actions — powered by PaddleOCR only.** Automatically classifies documents and provides actionable prompts.

## What It Does

- OCR extraction via **PaddleOCR cloud API** (requires credentials)
- 11 document types: invoice, business card, receipt, table, contract, ID card, passport, bank statement, driver's license, tax form, general
- Action suggestion with structured parameters
- Batch processing
- Searchable PDF generation (with bbox alignment)

## Quick Start

```bash
# Install dependencies
pip3 install -r scripts/requirements.txt

# Configure PaddleOCR API
export PADDLEOCR_DOC_PARSING_API_URL=https://your-api.paddleocr.com/layout-parsing
export PADDLEOCR_ACCESS_TOKEN=your_token

# Process a file
python3 scripts/doc_vision.py --file-path ./invoice.jpg --pretty --make-searchable-pdf
```

## Batch

```bash
python3 scripts/doc_vision.py --batch-dir ./inbox --output-dir ./out
```

## Output

See `docs/README.zh.md` for full JSON schema and integration guide.

## Supported Types

| Type | Actions |
|------|---------|
| Invoice | create_expense, archive, tax_report |
| Business Card | add_contact, save_vcard |
| Receipt | create_expense, split_bill |
| Table | export_csv, analyze_data |
| Contract | summarize, extract_dates, flag_obligations |
| ID Card | extract_id_info, verify_age |
| Passport | store_passport_info, check_validity |
| Bank Statement | categorize_transactions, generate_report |
| Driver License | store_license_info, check_expiry |
| Tax Form | summarize_tax, suggest_deductions |
| General | summarize, translate, search_keywords |

## Configuration

Required environment variables:
- `PADDLEOCR_DOC_PARSING_API_URL` — API endpoint ending in `/layout-parsing`
- `PADDLEOCR_ACCESS_TOKEN` — Access token

Optional:
- `PADDLEOCR_DOC_PARSING_TIMEOUT` — Default 600 seconds

## Searchable PDF

With `--make-searchable-pdf`, embeds OCR text layer aligned to original layout using bounding boxes. Requires `pdf2image` + `poppler` (system) and `reportlab`, `pypdf`, `pillow` (Python).

## Full Documentation

Detailed usage, troubleshooting, and development guide available in multiple languages under `docs/`:
- 中文: `docs/README.zh.md`
- English: `docs/README.en.md`
- Español: `docs/README.es.md`
- العربية: `docs/README.ar.md`

## License

MIT-0

---

**Made for OpenClaw.** Let your agent see and act.