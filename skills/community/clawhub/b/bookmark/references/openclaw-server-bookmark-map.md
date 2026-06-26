# openclaw-server Bookmark Map

This skill mirrors the read-only bookmark features from `openclaw-server` without changing that project.

## Scope copied into this skill

| `openclaw-server` module | User-facing capability | Skill command |
| --- | --- | --- |
| `bookmark-search` | keyword search | `node scripts/bookmark.mjs search "<query>"` |
| `bookmark-search` | recent updates | `node scripts/bookmark.mjs latest` |
| `bookmark-search` | top categories | `node scripts/bookmark.mjs categories` |
| `bookmark-search` | category articles | `node scripts/bookmark.mjs articles "<category>"` |
| `bookmark-search` | category links | `node scripts/bookmark.mjs links "<category>"` |

## Public data sources used by both

| Capability | Endpoint or page |
| --- | --- |
| keyword search | `/static-article/searchKeywords/<encoded>.json` |
| recent updates | `/static-article/page/page_<n>.json` |
| top categories | `/static-article/index.html` |
| category article page | `/static-article/cate-page/{first|second}/<id>.html` |
| category article data | `/static-article/cate-page/{first|second}/<id>/page_<n>.json` |

Default site root: `https://shuqianlan.com`

## Matching rules preserved

- Search first tries the full normalized keyword and keeps article results only.
- If the exact keyword has no article matches, the query is tokenized and retried term by term.
- Token search results are merged by URL.
- Ranking keeps the same priority order as `openclaw-server`: more matched terms first, then article over second-level category over top-level category, then original discovery order.
- Category lookup merges top categories with category-shaped search results.
- Category resolution tries exact normalized name match first, then the shortest partial match.

## Rendering rules preserved

- Search results show title, optional description, and category/update metadata.
- Recent updates show article cards and a "view all" link when available.
- Category article replies end with the category browse link.
- Category link replies list direct links and also include the category browse link.
- Empty results keep the same guidance style as `openclaw-server`: shorter keywords for search, category listing for category misses.

## Intentionally not implemented here

- conversation-state clarification flow
- OpenClaw user metadata extraction such as `sender_id`
- daily digest subscriptions
- notification storage
- webhook delivery
- admin endpoints for pending or delivered digests

Those belong to `openclaw-server`'s `bookmark-digest` pipeline rather than a standalone read-only skill.
