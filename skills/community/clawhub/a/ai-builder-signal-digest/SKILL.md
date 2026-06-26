---
name: ai-builder-signal-digest
description: Create a transparent, sourced “Top 3–5” AI builder signal digest (weekly or date-range) from a list of links or from a local signals log; includes a short “why care” line per item and explicit maturity/adoption notes (e.g., GitHub stars/forks, paper-only). Use when preparing ClawHub Skill content or posts for the AI agent/tooling community.
---

Generate short, post-ready digests that answer: **what is it, why should builders care, and how mature is it**.

## Rules (non-negotiable)

- **Source-first:** every item must include a primary link.
- **No speculation:** don’t claim adoption, performance, or production readiness unless the source states it.
- **Transparent maturity:**
  - GitHub repos → include **stars/forks** (or “unknown” if you can’t fetch).
  - Papers → label as **paper** and prefer quoting the headline quantitative claim from the abstract.
  - Very early repos (low stars/forks) → explicitly call it out (“early / reference implementation”).

## Preferred output shape

Title + 3–5 numbered bullets.

Each bullet:
- **Name** — one-liner (what it is)
- **Why care:** one sentence (builder-relevant benefit)
- **Maturity:** one short clause (e.g., “early repo (~X★, Y forks)” or “paper + open-source link”)
- Link

Keep it tight. If a digest needs nuance, add a single “Notes” line at the end.

## Use the bundled script (recommended)

If you have a local JSONL signals log (e.g., `memory/edge-signal-miner.normalized.jsonl`), use:

```bash
python3 skills/ai-builder-signal-digest/scripts/make_digest.py \
  --input memory/edge-signal-miner.normalized.jsonl \
  --since 2026-03-05 \
  --until 2026-03-19 \
  --top 5 \
  --category "Secure Cognitive / CDS" \
  --out /tmp/digest.md
```

If you already have curated links, you can pass them directly:

```bash
python3 skills/ai-builder-signal-digest/scripts/make_digest.py \
  --links https://github.com/Kailash-Sankar/PocketMCP https://arxiv.org/abs/2603.04428 \
  --out /tmp/digest.md
```

## What to do if GitHub stats fetch fails

- Keep the item.
- Replace maturity with: `Maturity: GitHub stats unavailable (rate-limit/blocked).`
- Do **not** guess.
