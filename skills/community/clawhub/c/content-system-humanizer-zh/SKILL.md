---
name: humanizer-zh
description: Remove obvious AI-writing traces from Chinese text in a constrained way. Use when Codex needs to reduce AI smell without changing facts, data, or the article's core argument.
---

# Humanizer ZH

This repo-local skill is inspired by `op7418/Humanizer-zh` and `blader/humanizer`, but implemented for the content-system runtime.

## Quick Start

```bash
.venv/bin/python -m skill_runtime.cli run-skill humanizer-zh \
  --input content-production/drafts/harness-engineering-一人公司-article.md
```

## What It Does

- Detects obvious AI-writing traces in Chinese prose
- Applies a surgical rewrite pass on body paragraphs
- Preserves facts, numbers, headings, structure, and article intent
- Writes a humanized copy plus a JSON report

## Output

- `content-production/drafts/<slug>-humanized.md`
- `content-production/drafts/<slug>-humanizer-report.json`

## Constraints

- Do not invent new facts or sources
- Do not flatten strong viewpoints into neutral filler
- Do not rewrite headings or titles by default
- Do not pretend the text comes from personal experience if it does not
