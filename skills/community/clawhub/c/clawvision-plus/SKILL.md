---
name: "clawvision-plus"
description: "Companion plugin for ClawVision: add PDF, OG images, and Telegram sharing."
metadata:
  version: 1.0.0
  author: Maximius
  tags: [clawvision, plugin, companion, pdf, og-image, telegram, export, social, openclaw]
  homepage: https://github.com/monaxamo/clawvision
  license: MIT
  icon: clawvision_demo_en.png
allowed-tools:
  - write
  - read
  - exec
  - message
user-invocable: true
---

# ClawVision Plus — companion plugin for ClawVision

This is **not a standalone skill**. It extends [ClawVision](https://github.com/monaxamo/clawvision) with three extra outputs for summaries it already generated.

## Adds

1. **PDF export** — multi-page PDF, one page per ClawVision tab (Main / Format / Built / Next).
2. **OG image** — 1200×630 social-preview PNG.
3. **Telegram sharing** — send the OG image + summary caption to a Telegram chat or channel.

## When to use

Only after the main `clawvision` skill has generated the HTML card. Good triggers:

- "Export this ClawVision summary as PDF."
- "Generate an OG image for this ClawVision card."
- "Send this ClawVision summary to Telegram."
- "Run ClawVision Plus on the summary we just made."

## Workflow

1. Use `clawvision` to generate the summary card (HTML + JSON).
2. Run `clawvision-plus/scripts/extend_visual.py` on the same JSON and output directory.
3. Get the PDF, OG image, and/or Telegram delivery.

## Usage

```bash
# 1. Generate summary with the main ClawVision skill
python clawvision/scripts/generate_visual.py \
  --summary summary.json \
  --output ./out \
  --png --md --pptx \
  --lang en

# 2. Run the companion plugin
python clawvision-plus/scripts/extend_visual.py \
  --summary summary.json \
  --output ./out \
  --pdf --og \
  --telegram \
  --telegram-chat-id "@your_channel" \
  --telegram-bot-token "YOUR_BOT_TOKEN"
```

## Parameters

- `--summary` — path to ClawVision summary JSON.
- `--output` — directory containing the rendered HTML card.
- `--slug` — optional slug override.
- `--pdf` — export HTML to a multi-page PDF, one page per tab.
- `--og` — generate 1200×630 OG image.
- `--telegram` — send OG image + caption to Telegram.
- `--telegram-chat-id` — Telegram chat/channel ID.
- `--telegram-bot-token` — Telegram bot token.
- `--telegram-caption` — override the generated caption.

## Requirements

- Python 3.10+
- `playwright` (already required by ClawVision)
- `Pillow`
- `reportlab` (for multi-page PDF)
- `python-telegram-bot` (only for Telegram sharing)

## Safety

- Do not send summaries to Telegram without explicit user confirmation.
- Never share Telegram bot tokens in chat or logs.
- The plugin does not upload raw session transcripts.
