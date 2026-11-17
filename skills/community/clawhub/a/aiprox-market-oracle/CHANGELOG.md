# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /api/orchestrate` with `capability: market-data` (one step on market-oracle, 50 sats). The task is a market slug, or anything else for trending markets.
- Added the not-financial-advice note from the AIProx terms and a no-trading rule.
- Removed the `market`, `markets` (batch) and `timeframe` fields, which AIProx does not forward.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
