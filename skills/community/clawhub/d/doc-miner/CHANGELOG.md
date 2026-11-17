# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /v1/summarize` (40 sats) with `text` or `url` (web page or PDF).
- Narrower trigger: only when the user asks to summarize a given document.
- Removed the auto-detected Q&A and extraction modes, which production does not offer.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
