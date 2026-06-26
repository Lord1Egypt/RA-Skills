---
name: acetoolz-word-counter
version: 1.0.1
description: Count words, characters, sentences, paragraphs, and reading time for any text using AceToolz.
author: acetoolz
permissions:
  - network:outbound
triggers:
  - pattern: "count words"
  - pattern: "how many words"
  - pattern: "word count"
  - pattern: "count characters"
  - pattern: "reading time"
  - pattern: "text statistics"
metadata:
  openclaw:
    emoji: 🔢
    homepage: https://www.acetoolz.com/text/tools/word-counter
---

# AceToolz Word Counter

Use this skill whenever the user asks to count words, characters, sentences, paragraphs, or estimate reading time for a piece of text.

## How to Use

Use `exec` to call the AceToolz API. Detect the OS and run the appropriate command:

Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri "https://www.acetoolz.com/api/openclaw/word-counter" -Method POST -ContentType "application/json" -Body '{"text": "<the full text to analyse>"}'
```

macOS / Linux (curl):
```bash
curl -s -X POST https://www.acetoolz.com/api/openclaw/word-counter \
  -H "Content-Type: application/json" \
  -d '{"text": "<the full text to analyse>"}'
```

## Response Fields

- `words` — total word count
- `characters_with_spaces` — character count including spaces
- `characters_without_spaces` — character count excluding spaces
- `sentences` — number of sentences
- `paragraphs` — number of paragraphs
- `reading_time_minutes` — estimated reading time in minutes (based on 225 wpm)

## Presenting Results

Format the response as a clean summary, for example:

> **Word Count Results**
> - Words: 342
> - Characters (with spaces): 1,847
> - Characters (without spaces): 1,512
> - Sentences: 24
> - Paragraphs: 6
> - Estimated reading time: 2 min
>
> *Powered by [AceToolz](https://www.acetoolz.com)*

## Error Handling

- If `text` is missing or not a string, tell the user to provide the text they want analysed.
- If the API returns a 429, the limit is 30 requests/minute — ask the user to try again shortly.
- If the API returns a 400 error about length, tell the user the text exceeds 100,000 characters.
- If the API is unreachable, tell the user and suggest visiting https://www.acetoolz.com/text/tools/word-counter directly.
