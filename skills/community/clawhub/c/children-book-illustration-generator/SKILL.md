---
name: children-book-illustration-generator
description: AI children's book illustration generator — create whimsical storybook art, picture book pages, fairy tale scenes, and kids' story illustrations. Perfect for self-publishing authors, KDP creators, teachers, and parents making bedtime story books, educational materials, and nursery wall art via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Children's Book Illustration Generator

AI children's book illustration generator — create whimsical storybook art, picture book pages, fairy tale scenes, and kids' story illustrations. Perfect for self-publishing authors, KDP creators, teachers, and parents making bedtime story books, educational materials, and nursery wall art.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create children book illustration ai generator images.

## Quick start
```bash
node childrenbookillustrationgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/children-book-illustration-generator
```
