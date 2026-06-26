---
name: chat-distill
description: >
  Distill a person's chat style from exported conversation records and generate replies that mimic their voice. Use when (1) analyzing chat history to extract vocabulary, tone, emoji habits, sentence patterns, and personality traits, (2) generating replies in someone's specific chat style, (3) creating a style profile from WeChat, TG, Discord, or text chat exports, (4) asking to analyze chat records or mimic a speaker's tone. Supports .txt, .json, and WeChat chat export formats.
---

# Chat Distill — Style Analysis & Mimicry

## Workflow

1. **Parse** → extract messages per speaker from raw export (see `references/format-parsers.md`)
2. **Analyze** → build style profile (see `references/style-dimensions.md`)
3. **Report** → output analysis report using template in `references/output-template.md`
4. **Mimic** → generate replies on demand using the profile

## Quick Start

Given a chat export file:

1. Read the file and identify the format (WeChat export, plain text, JSON array, TG export).
2. Normalize into `{ speaker, text, time? }` messages using parsing rules in `references/format-parsers.md`.
3. Pick the **target speaker** — the one whose style to learn. If multiple speakers exist, ask which one.
4. Run analysis following `references/style-dimensions.md`.
5. Output the report per `references/output-template.md` § Analysis Report.
6. When the user asks for a mimicked reply, use the profile + `references/output-template.md` § Mimic Reply.

## Key Principles

- **Show, don't tell**: Include concrete examples from the actual chat when reporting style traits.
- **Preserve quirks**: Capture tics the speaker doesn't notice — repeated filler words, capitalization habits, punctuation style.
- **Respect privacy**: Never echo sensitive content (passwords, addresses, financials) from chats into reports. Anonymize if needed.
- **Minimum sample**: Require at least 20 messages from the target speaker. If fewer, warn that analysis may be unreliable.
