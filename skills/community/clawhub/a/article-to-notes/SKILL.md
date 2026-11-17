---
name: article-to-notes
description: Turn a web article (URL) into a clean, personal-knowledge-base style markdown note. Use when the user shares a link and wants a distilled note with title, source, key points, and quotes instead of a raw dump. NOT for full-text mirroring, paywalled content, or image-heavy galleries.
---

# Article → Notes

Convert one web article into a distilled markdown note ready for a personal knowledge base (e.g. Obsidian, Logseq, plain `notes/` folder).

## When to use

- User pastes an article URL and says "take notes", "summarize into a note", "save this as a note"
- You already have article text fetched and just need the note shape

## When NOT to use

- Paywalled or login-gated content (do not scrape auth walls)
- Image-heavy galleries where images are the content
- Real-time news that needs just a headline brief (use a 3-line summary instead)

## Steps

1. Fetch the article with `web_fetch` (markdown mode). If extraction fails, ask the user to paste the text.
2. Extract: title, author/site, publish date, canonical URL.
3. Write the note in this exact shape:

```markdown
# <Title>

- **Source:** <site> · <URL>
- **Date:** <publish date or "unknown">
- **Saved:** <YYYY-MM-DD>

## Key points
- 3–6 bullets, one idea each, no filler.

## Worth quoting
> 1–2 short verbatim quotes (keep under ~15 words each).

## My take
- 1–2 lines: why this matters / what to follow up on.
```

4. Save to `notes/<YYYY-MM-DD>-<slug>.md` unless the user specifies another path.
5. Reply with the saved path and the 3-bullet key points inline.

## Notes

- Never invent quotes — if no good quote exists, drop that section.
- Keep "My take" honest; if the article added nothing new, say so in one line.
- If the article is > 5000 words, cap key points at 6 and note "(long read, distilled)".
