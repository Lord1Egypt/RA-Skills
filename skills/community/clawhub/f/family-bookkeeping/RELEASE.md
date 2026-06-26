# family-bookkeeping v1.0.0

## Release Notes

Initial public release of the `family-bookkeeping` OpenClaw skill.

### Included
- Natural-language family bookkeeping workflow guidance in `SKILL.md`
- Bill normalization for WeChat and Alipay exports
- Import precheck and deduplication flow
- Feishu-importable CSV export
- Optional direct write helpers for Feishu Bitable
- Query, reporting, recent-record, and lightweight update scripts
- Public-facing bilingual `README.md`
- Usage details moved into `references/usage.md`

### Public release preparation
- Removed hardcoded live ledger identifiers from docs and scripts
- Switched default ledger configuration to environment variables
- Replaced personal example names with generic placeholders
- Added `.gitignore` for caches, env files, and generated artifacts
- Restructured docs for cleaner public repository presentation

### Required local configuration
This repository does not include credentials or live production ledger settings.
To use it locally, configure:
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FAMILY_BOOKKEEPING_APP_TOKEN`
- `FAMILY_BOOKKEEPING_TABLE_ID`
- `FAMILY_BOOKKEEPING_BITABLE_URL`
