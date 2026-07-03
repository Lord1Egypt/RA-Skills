# Deckly Deck Redesign

> AI-powered PowerPoint/PDF slide beautification — turn rough lecture decks into polished presentations.

An agent skill for **Claude Code, Codex CLI, Cursor, OpenClaw, and other AI coding assistants**. Uses the [Deckly](https://deckly.art) API to analyze, restyle, and fine-tune presentation decks automatically.

## What It Does

- **Analyze** any `.pptx` or `.pdf` deck — extracts slide structure and recommends improvements
- **Pick an aesthetic** — 5 built-in text styles (minimalist corporate, flat illustration, futuristic tech, premium presentation, academic lecture) + template themes
- **Free preview** — new accounts get a free 3-slide preview (0 credits)
- **Fine-tune** individual slides with natural language instructions
- **Download** the polished deck as `.pptx`

## Quick Install

```bash
npx skills add jimmymelbj/deckly-redesign
```

Or install via ClawHub:

```bash
clawhub install deckly-redesign
```

## Requirements

- Python 3 (standard library only — no `pip install` needed)
- A Deckly account (free to sign up; in-conversation onboarding supported)

## Usage

Once installed, just tell your AI agent:

> "Redesign this presentation to look more professional"

The skill handles authentication, style selection, preview, fine-tuning, and download — all interactively.

## File Structure

```
deckly-redesign/
├── SKILL.md           # Agent skill definition
├── README.md          # This file
├── reference.md       # Full API reference & HTTP flow
└── scripts/
    └── deckly.py      # Python CLI for Deckly API
```

## Pricing (Deckly Credits)

| Slides | Credits |
|--------|---------|
| 1–10 | 10 |
| 11–20 | 20 |
| 21–60 | 40 |

First-time accounts get one free 3-slide preview. Fine-tuning costs 1 credit per slide.

## License

MIT
