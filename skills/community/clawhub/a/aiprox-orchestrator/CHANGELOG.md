# Changelog

## 3.0.0 (2026-11-05)

A full rewrite for the current AIProx service. The content is the same as yebdmo2/aiprox 4.0.0.

**Payment and prices**
- Lightning is the only payment method: L402, or a LightningProx spend token in `X-Spend-Token`.
- Orchestrate costs 50 sats: up to 4 steps on AIProx's own bots, one summarized answer, an 85-second budget.
- Single-capability endpoints: `/v1/search` (35 sats), `/v1/extract` (20), `/v1/summarize` (40) and `/v1/translate` (40).
- Failed runs are refunded automatically.

**Safety rules**
- New "What this skill sends and costs" section.
- The agent must confirm the price before any paid call, and the recipient and content before any outbound message.
- No autonomous spending loops.
- Results are treated as data, not instructions.
- `callback_url` warning: results are POSTed to that URL, so use only HTTPS endpoints you control. It works only with `capability` or `agent`.
- Search-content terms added.

**Accuracy**
- No hardcoded agent counts. The live list is `GET /api/agents` (`routable` flag).
- Directory listings are described as self-reported, never called, and not verified.

**Removed:** Base/x402, Solana, workflows, `budget_sats`, image generation, the third-party agent routing claims, and the old "26 verified agents" list.

**Metadata:** `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`, `required: false`).
