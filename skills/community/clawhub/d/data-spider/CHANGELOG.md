# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /v1/extract` (20 sats): title and clean main text of one public page.
- Removed schema-guided, JSON, table and list extraction. Production does not offer it.
- Documents redirects, PDFs and JavaScript-only pages, all refunded.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
