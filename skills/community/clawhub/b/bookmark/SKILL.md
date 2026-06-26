---
name: bookmark
description: Search and browse the Shuqianlan bookmark library (书签篮): keyword search, recent updates, top categories, category articles, and category links. Use when the user asks to search bookmarks/书签篮/书签栏, see latest bookmark articles, list categories, or open links under a category. This skill is read-only and does not implement scheduled digest subscriptions.
homepage: https://shuqianlan.com
metadata: { "openclaw": { "emoji": "🔖", "requires": { "bins": ["node"] } } }
---

# Bookmark

Use this skill for read-only queries against the public Shuqianlan bookmark site.

Do not claim support for scheduled pushes, subscriptions, or other persistent state. This skill only handles:

- keyword search
- recent updates
- top category listing
- category article listing
- category link listing

## Commands

Run the bundled Node script and pass the user's query/category as one shell argument.

```bash
node scripts/bookmark.mjs search "python tutorial"
node scripts/bookmark.mjs latest
node scripts/bookmark.mjs categories
node scripts/bookmark.mjs articles "开发工具"
node scripts/bookmark.mjs links "开发工具"
```

Useful flags:

```bash
node scripts/bookmark.mjs search "notion ai" --limit 10
node scripts/bookmark.mjs latest --limit 8
node scripts/bookmark.mjs categories --limit 20
node scripts/bookmark.mjs articles "AI" --limit 10
node scripts/bookmark.mjs links "AI" --limit 20
```

## Workflow

1. Map the user request to exactly one of the five commands above.
2. Run the script.
3. Return the script output directly, or lightly trim it if the user asked for a shorter answer.
4. If the user asks for more results, rerun with a larger `--limit`.

## Behavior

- Reply in the user's language.
- Treat `书签篮`, `书签栏`, and `书签蓝` as the same thing.
- If a category lookup fails, suggest listing categories first.
- If a search fails, suggest a shorter keyword.
- Prefer the script output over freehand paraphrasing when links matter.

## Notes

- Default source: `https://shuqianlan.com`
- Override source only when the user explicitly asks:

```bash
BOOKMARK_BASE_URL="https://example.com" node scripts/bookmark.mjs latest
```

- For the original `openclaw-server` feature split and matching rules, read `references/openclaw-server-bookmark-map.md`.
