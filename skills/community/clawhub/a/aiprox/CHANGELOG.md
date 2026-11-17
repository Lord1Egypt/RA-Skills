# Changelog

## 4.0.0 (2026-11-05)

A full rewrite for the current AIProx service.

**Payment and prices**
- Lightning is the only payment method: L402, or a LightningProx spend token in `X-Spend-Token`.
- Orchestrate costs 50 sats: up to 4 steps on AIProx's own bots, one summarized answer, an 85-second budget.
- New single-capability endpoints: `/v1/search` (35 sats), `/v1/extract` (20), `/v1/summarize` (40) and `/v1/translate` (40).
- Failed runs are refunded automatically.

**Safety rules**
- New "What this skill sends and costs" section.
- The agent must confirm the price before any paid call, and the recipient and content before any email or other outbound message.
- No autonomous spending loops.
- Results are treated as data, not instructions.
- `callback_url` warning: results are POSTed to that URL, so use only HTTPS endpoints you control. It works only with `capability` or `agent`.
- Search-content terms added.

**Accuracy**
- No hardcoded agent counts. The live list is `GET /api/agents` (`routable` flag).
- Directory listings are described as self-reported, never called, and not verified.
- The strict-pipeline example is now search → sentiment. It no longer sends email.

**Removed:** Base/x402, Solana, workflows and scheduling, the job board, ratings, the old agent list, and `budget_sats`. None of these exist on AIProx today.

**Metadata:** `AIPROX_SPEND_TOKEN` is now optional (`envVars`, `required: false`), and the frontmatter uses `metadata.openclaw`.
