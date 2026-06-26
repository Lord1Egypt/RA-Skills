---
name: ai-search-rank-tracker
description: Track whether ChatGPT, Claude, Gemini, and Perplexity recommend a startup or brand across a prompt set. Use when you need AI search visibility tracking, GEO / AI SEO monitoring, brand mention checks, competitor detection in AI answers, rank estimation, sentiment scoring, or a simple visibility report for a company, product, or domain.
---

# AI Search Rank Tracker

Run the tracker against a prompt set and produce a visibility report.

## Inputs

Use a JSON file like `prompts/starter.json`:

```json
{
  "brand": "clawlite.ai",
  "aliases": ["clawlite", "claw lite", "clawlite ai"],
  "prompts": [
    "best openclaw alternative",
    "easiest openclaw installer",
    "openclaw for beginners"
  ],
  "engines": ["chatgpt", "claude", "gemini", "perplexity"]
}
```

## Install

Use the one-click bootstrap:

```bash
bash scripts/install.sh
```

## Run

```bash
node src/index.js prompts/starter.json
```

## Outputs

Find reports in `output/`:

- JSON report
- Markdown report
- CSV report

## Prompt database

Use the built-in prompt database in `prompt-db/` for larger GEO / AI SEO scans.

Included categories:
- SaaS
- AI tools
- Developer tools
- OpenClaw ecosystem
- Local AI tools

Each record includes category and commercial metadata so prompt sets can be grouped by intent, journey stage, and buyer value.

## Notes

- Configure keys in `.env`
- OpenAI-compatible backends are supported
- Anthropic is supported
- OpenRouter / EZRouter-compatible setups can be wired through environment variables
- Per-engine failures do not fail the whole batch
