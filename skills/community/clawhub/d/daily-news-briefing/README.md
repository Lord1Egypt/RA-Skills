# Daily News Briefing

Production-grade skill for creating polished daily briefings, executive digests, morning newsletters, and market snapshots with verified sourcing and premium formatting.

## Why This Skill Exists

Most AI-generated news summaries feel generic, repetitive, and weakly sourced. This skill is designed to produce outputs that feel closer to a paid editorial product: concise, current, clearly structured, and tailored to a specific audience.

## What It Does

- turns current developments into a clean daily briefing
- prioritizes stories by decision value instead of pure volume
- adds "why it matters" context for each major item
- supports Markdown and HTML output styles
- includes reusable templates and a package generator script

## Best For

- founder and CEO digests
- investor and operator briefings
- polished morning newsletters
- trend and industry roundups
- recurring daily report workflows

## Included Files

- `SKILL.md` for the core editorial workflow
- `references/editorial-standards.md` for quality and sourcing rules
- `references/output-blueprints.md` for output format presets
- `assets/briefing-template.md` for Markdown rendering
- `assets/briefing-template.html` for premium HTML rendering
- `scripts/render_briefing_package.py` for generating reusable briefing skeletons

## Quick Example

```bash
python3 scripts/render_briefing_package.py \
  --title "AI Daily Brief" \
  --date "2026-03-18" \
  --audience "Founders and investors" \
  --scope "AI and startup ecosystem" \
  --tone "authoritative" \
  --format html \
  --output /tmp/ai-daily-brief
```

## Security Posture

- no remote installer commands
- no bundled network fetchers
- no opaque binaries
- local template rendering only

## Suggested Listing Blurb

Create elegant, source-linked daily briefings and executive digests for founders, investors, and operators.
