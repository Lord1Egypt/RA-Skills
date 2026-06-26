---
name: book-cover-generator
description: AI book cover generator for indie authors and self-publishers — create stunning KDP book covers, novel cover art, ebook covers, and Kindle cover designs using AI. Generate genre-specific covers for fantasy, romance, thriller, sci-fi, and non-fiction books in portrait format via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Book Cover Generator

AI book cover generator for indie authors and self-publishers — create stunning KDP book covers, novel cover art, ebook covers, and Kindle cover designs using AI. Generate genre-specific covers for fantasy, romance, thriller, sci-fi, and non-fiction books in portrait format.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai book cover generator images.

## Quick start
```bash
node bookcovergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/book-cover-generator
```
