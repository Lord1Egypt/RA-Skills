---
name: gamma
description: Create presentations, documents, social posts, and web pages via the Gamma.app API. Use when asked to create a presentation, pitch deck, slide deck, document, social media carousel, or webpage using Gamma. Also use when asked to generate slides, export to PDF/PPTX, or create content from a Gamma template. Triggers on "create a presentation", "make a deck", "gamma", "slides", "pitch deck", "create a document in gamma".
metadata:
  openclaw:
    homepage: https://gamma.app
    publisher: autosolutionsai-didac
    requires:
      env:
        - GAMMA_API_KEY
      bins:
        - curl
        - python3
---

# Gamma.app — Presentations & Documents API

Create presentations, documents, social posts, and web pages programmatically via the Gamma API.

**Homepage:** https://gamma.app
**API Docs:** https://developers.gamma.app/docs/getting-started
**Runtime dependencies:** `curl`, `python3` (for JSON building/parsing)

## Setup

Set the environment variable before using:
```bash
export GAMMA_API_KEY="sk-gamma-xxxxx"  # Get from https://gamma.app/settings
```

The script only makes network calls to `https://public-api.gamma.app/v1.0`. Your API key and inputText content are sent to Gamma's servers.

## Quick Start

### Generate a presentation
```bash
bash scripts/gamma.sh generate "AI trends in 2026 for business leaders" \
  --format presentation --num-cards 10 --export pdf --wait
```

### Generate a document
```bash
bash scripts/gamma.sh generate "Quarterly marketing report Q1 2026" \
  --format document --text-mode generate --amount detailed \
  --tone "professional" --audience "executive team" --export pdf --wait
```

### Create from template
```bash
bash scripts/gamma.sh template "g_abcdef123" "Update this pitch deck for Twist Broadband client" \
  --export pdf --wait
```

### Check status manually
```bash
bash scripts/gamma.sh status "generationId123"
```

### List themes and folders
```bash
bash scripts/gamma.sh themes
bash scripts/gamma.sh themes "dark"
bash scripts/gamma.sh folders
```

## Script Reference

`scripts/gamma.sh <command> [args] [options]`

### Commands

| Command | Args | Description |
|---------|------|-------------|
| `generate` | `"inputText"` | Create from scratch |
| `template` | `"gammaId" "prompt"` | Create from existing template |
| `status` | `"generationId"` | Check generation status |
| `themes` | `[query]` | List available themes |
| `folders` | `[query]` | List workspace folders |

### Generate Options

| Option | Values | Default |
|--------|--------|---------|
| `--format` | presentation, document, social, webpage | presentation |
| `--text-mode` | generate, condense, preserve | generate |
| `--num-cards` | 1-60 (Pro) / 1-75 (Ultra) | 10 |
| `--card-split` | auto, inputTextBreaks | auto |
| `--theme` | theme ID from `themes` command | (Gamma picks) |
| `--export` | pdf, pptx | (none) |
| `--tone` | free text | (none) |
| `--audience` | free text | (none) |
| `--language` | ISO code (en, es, fr...) | (auto) |
| `--amount` | brief, medium, detailed, extensive | (auto) |
| `--image-source` | aiGenerated, pexels, noImages, etc. | (auto) |
| `--image-model` | flux-1-pro, imagen-4-pro, etc. | (auto) |
| `--image-style` | free text ("photorealistic") | (none) |
| `--instructions` | additional guidance (max 2000 chars) | (none) |
| `--dimensions` | fluid, 16x9, 4x3, 1x1, 4x5, 9x16, a4, letter | fluid |
| `--workspace-access` | noAccess, view, comment, edit, fullAccess | (default) |
| `--external-access` | noAccess, view, comment, edit | (default) |
| `--folder` | folder ID (comma-separated for multiple) | (none) |
| `--wait` | (flag) Poll until generation completes | false |
| `--poll-interval` | seconds between polls | 5 |

## Workflow

1. **Generate** — POST creates the gamma, returns a `generationId`
2. **Poll** — Use `--wait` or manually check `status` until `completed`
3. **Result** — Completed response includes `gammaUrl` (live link) and export download URL if requested
4. **Credits** — Response shows `credits.deducted` and `credits.remaining`

## Input Tips

- Short prompts work ("AI trends 2026") but detailed structured text produces better results
- Insert image URLs directly in inputText where you want them placed
- Use `\n---\n` in inputText to force card breaks (set `--card-split inputTextBreaks`)
- To use only your images (no AI-generated ones), set `--image-source noImages`
- JSON-escape special characters in inputText

## Credit Costs

- Cards: 1-5 credits each
- AI images: 2 credits (basic) to 125 credits (ultra) per image
- Example: 10-card deck with basic AI images ≈ 20-60 credits

## Full API Reference

For complete parameter details, header/footer configuration, and sharing options, read `references/api-reference.md`.
