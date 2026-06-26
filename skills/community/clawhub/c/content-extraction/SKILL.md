---
name: content-extraction
description: OpenClaw-native executable content extraction skill for URLs, Feishu, YouTube, and web pages.
version: 1.1.0
author: halfmoon82
tags: [browser, feishu, extraction, markdown, executable]
---

# Content Extraction — Executable Skill

This skill is the **local executable version**. It keeps the source-aware routing design and restores a concrete extraction workflow.

## What it does
- Detects the input source
- Selects the best extraction channel
- Produces clean Markdown
- Saves long content locally when needed
- Explains fallback failures instead of hiding them

## Main entrypoints
- `scripts/extract_router.py` — classify input and build a route plan
- `scripts/extract.py` — generate an executable extraction spec

## Route priorities
1. **WeChat** → browser chain
2. **Feishu doc/wiki** → Feishu tools
3. **YouTube** → transcript chain
4. **Generic URL** → `r.jina.ai` → `defuddle.md` → `web_fetch` → browser fallback

## Output contract
Always return:
- title
- author when available
- source
- url
- summary
- Markdown body
- save path when content is long

## Fallback rule
Never claim success when extraction is partial. If a layer fails, report:
- where it failed
- why it failed
- what fallback was tried next

## Notes
- The ClawHub abstracted package stays abstract.
- This local version restores the executable workflow for OpenClaw use and ClawDex publishing.
