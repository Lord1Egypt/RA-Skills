# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /api/orchestrate` with `capability: code-execution` (one step on code-auditor, 50 sats).
- Documents how the code is given: a GitHub repo URL, a code URL or a fenced block in `task`.
- Removed the `repo_url` and `focus` fields (AIProx does not forward them) and the gas-optimization claim.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
