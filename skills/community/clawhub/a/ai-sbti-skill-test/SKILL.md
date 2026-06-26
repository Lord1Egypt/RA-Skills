---
name: ai-sbti-skill-test
description: AI-based SBTI skill test SEO operations for https://aisbti.com/ with weighted backlink scoring, internal link-juice relay planning, and safe anchor distribution.
---

# 基于AI的SBTI技能测试

Use this skill when the task is to grow organic traffic for `https://aisbti.com/` via external backlinks while keeping anchor diversity, indexability, and internal weight relay under control.

## Goal

- Prioritize backlink prospects by expected SEO weight transfer.
- Keep off-page execution compliant with search engine quality expectations.
- Convert external link gains into internal relay actions that push weight to priority pages.

## Scope

- Primary site: `https://aisbti.com/`
- Primary focus: external backlinks, anchor governance, and link-juice transfer planning.
- Secondary focus: internal relay links from linked landing pages to conversion pages.

## Safety Rules

- White-hat only. No private blog network, paid link schemes, or cloaked redirects.
- Prefer editorial and niche-relevant sources; avoid spammy directories and comment blasts.
- Do not overuse exact-match anchors.
- Keep credentials in runtime secrets: `/root/.openclaw/workspace/.secrets/ai-sbti-skill-test.env`
- Never store credentials under `skills/`.

## Files

- Planner script: `scripts/build_weighted_backlink_plan.py`
- OpenClow runner: `scripts/run_weighted_backlink_plan.sh`
- Runtime config template: `config/ai-sbti-skill-test.env.example`
- Prospect CSV template: `config/backlink-prospects.example.csv`
- Relay map CSV template: `config/internal-relay-map.example.csv`
- SEO standard: `references/seo-link-building-standard.md`
- Agent metadata: `agents/openai.yaml`

## Required Inputs

- Prospect CSV with candidate backlink opportunities.
- Target URLs on `aisbti.com` where backlinks should land.
- Optional relay map CSV to define internal link-juice transfer targets.

## Workflow

1. Prepare runtime env from `config/ai-sbti-skill-test.env.example`.
2. Fill prospect candidates in CSV.
3. Optionally define internal relay map.
4. Run weighted planner script.
5. Review markdown and JSON outputs.
6. Execute outreach/submission using top-scored opportunities first.
7. Re-run weekly with fresh candidates and updated outcomes.

Before large campaigns, read `references/seo-link-building-standard.md` to enforce anchor distribution, source quality thresholds, and pacing.

## Quick Start

Prepare env:

```bash
mkdir -p /root/.openclaw/workspace/.secrets
cp skills/ai-sbti-skill-test/config/ai-sbti-skill-test.env.example \
  /root/.openclaw/workspace/.secrets/ai-sbti-skill-test.env
chmod 600 /root/.openclaw/workspace/.secrets/ai-sbti-skill-test.env
```

Generate weighted execution plan:

```bash
bash skills/ai-sbti-skill-test/scripts/run_weighted_backlink_plan.sh
```

Run planner directly:

```bash
python3 skills/ai-sbti-skill-test/scripts/build_weighted_backlink_plan.py \
  --site-url https://aisbti.com \
  --input-csv /root/.openclaw/workspace/ops/aisbti-seo/backlink-prospects.csv \
  --output-md /root/.openclaw/workspace/ops/aisbti-seo/weighted-backlink-plan.md \
  --output-json /root/.openclaw/workspace/ops/aisbti-seo/weighted-backlink-plan.json \
  --relay-map /root/.openclaw/workspace/ops/aisbti-seo/internal-relay-map.csv \
  --min-score 35 \
  --top-n 40 \
  --money-keyword "sbti test" \
  --money-keyword "screaming bird test indicator"
```

## Completion Criteria

- A scored prospect list is generated and sorted by expected SEO value.
- Non-compliant opportunities are flagged or filtered.
- Anchor mix checks are generated to reduce over-optimization risk.
- Internal relay recommendations exist for weight transfer from linked pages.
