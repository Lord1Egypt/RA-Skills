# Digest Procedure

Compile a daily digest of architecture news relevant to the user's active projects.

## Steps

1. **Load projects** — Read `workspace/projects/README.md` for the active project list. If no active projects, ask the user what they're working on and stop.
2. **Load sources** — Read `workspace/config/sources.md` for the curated source list.
3. **Per project** — For each active project:
   - Read its project file to get Research Topics.
   - Search each relevant source category for recent news matching the research topics. Search in both English and the user's preferred language (from `USER.md`) to maximize coverage.
   - Prioritize: project-relevant findings > techniques/materials > notable buildings.
4. **Compile digest** — Write findings to `workspace/digests/YYYY-MM-DD.md` (today's date) in this format:

```markdown
# Architecture Digest — YYYY-MM-DD

## {Project Name}
- [{Article title}]({url}) — {one-line summary and relevance}

## General
- [{Article title}]({url}) — {one-line summary}
```

5. **Deliver** — Send each entry as a separate message so IM platforms auto-generate rich link previews.

   - First, send a short header:
     ```
     🏛️ Architecture Digest — YYYY-MM-DD
     ```
   - For each section, send a separator:
     ```
     — {Project Name} —
     ```
   - Each entry as its own message:
     ```
     **Article Title** — one-line summary and relevance
     https://example.com/article-url
     ```
     URL must be on its own line (not markdown link syntax) for rich preview.
   - After project sections, send `— General —` separator, then general entries.

## Guidelines

- The digest file is always written in **English**. Preserve proper nouns in their original language in parentheses where relevant.
- If a digest for today already exists, update rather than overwrite.
- Skip sources that return nothing relevant — don't pad.
- Note competition deadlines prominently (bold, with date).
- Prefer recent articles (last 48 hours) but include older ones if highly relevant.
