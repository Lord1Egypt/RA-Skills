---
name: build-opportunity-scout
description: Analyze harvested trend data and generate prioritized build opportunities for new skills/apps (P0/P1/P2) with implementation hints. Use when user wants actionable project direction from continuous trend scraping.
---

# Build Opportunity Scout

Turn trend feed noise into actionable build queue.

## Inputs

- `/root/.openclaw/workspace/data/harvest/feature_patterns.json`

## Outputs

- `/root/.openclaw/workspace/data/harvest/opportunities.json`
- `/root/.openclaw/workspace/data/harvest/opportunities.md`

## Run

```bash
python3 /root/.openclaw/workspace/skills/build-opportunity-scout/scripts/scout.py
```

## What it generates

For each opportunity:
- title
- type (skill/app)
- priority (P0/P1/P2)
- impact (1-5)
- effort (1-5)
- score
- why_now
- mvp_steps

## Operator rules

- Prefer practical opportunities with clear MVP steps
- Keep output concise and execution-first
- Deduplicate similar ideas
