# Eir Content Specification

> Single source of truth for all content field constraints and quality criteria.
> Used by: writer prompts, API validation, front-end rendering.

## Contents

- [Field Reference](#field-reference) — dot, l1, l2, sources fields
- [via vs sources](#via-vs-sources) — Attribution handling
- [lang field](#lang-field) — Language requirements
- [Null handling](#null-handling)
- [Validation summary](#validation-summary)
- [Content ID format](#content-id-format)
- [Interest Signals](#interest-signals)

---

## Field Reference

### dot (L0 — the dot on canvas)

| Field | Type | Recommended | Hard Limit | Notes |
|-------|------|-------------|------------|-------|
| `hook` | string | ≤10 CJK chars / ≤6 EN words | **100 chars** (API rejects) | Creates curiosity gap. No hype words ("Breaking", "Exciting"). Rendered as single-line label on the dot. |
| `category` | enum | — | `focus` \| `attention` \| `seed` | Determines dot visual style. |

### l1 (card — what the user sees first)

| Field | Type | Recommended | Hard Limit | Notes |
|-------|------|-------------|------------|-------|
| `title` | string | 15-40 CJK chars / 8-15 EN words | **200 chars** (API rejects) | Opinionated, not a headline. Must be in `lang`. |
| `summary` | string | 50-80 words | — | 2-3 sentences. Advances beyond the title — don't repeat. |
| `key_quote` | string | 1 sentence | — | Best direct quote from sources. Use `""` if none. |
| `via` | **string[]** | — | — | **Must be an array.** Auto-derived from `sources[].name`. Pipeline populates it; API also falls back to `sources[].name` if empty. Writer should NOT set this. |
| `bullets` | string[] | 3-4 items | 10 items (API rejects) | Each: ≤20 CJK chars / ≤50 EN chars. Don't repeat summary. |

### l2 (depth — expanded view)

| Field | Type | Recommended | Hard Limit | Notes |
|-------|------|-------------|------------|-------|
| `content` | string | 200-600 CJK chars / 150-400 EN words | — | 2-4 paragraphs separated by `\n\n`. Starts where summary left off. |
| `bullets` | array | 3-5 items | — | Each: `{text: string, confidence: "high"\|"medium"\|"low"}`. Concrete facts with numbers/names. Every bullet must have supporting detail in `content`. |
| `context` | string | 1-2 sentences | — | Optional. "SO WHAT for the reader." Omit or leave empty if not needed. |
| `eir_take` | string | 1 sentence | — | Optional. Eir's sharp opinion. **PUBLIC** (visible on share pages) if included. |
| `related_topics` | string[] | 3-5 items | — | Human-readable phrases in `lang`. NOT slugs. e.g. `"Vector Search and ANN Algorithms"` ✅, `"vector-search-ann"` ❌ |

### sources (provenance — machine-readable)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `url` | string | **Yes** | Must be valid URL. Used for server-side dedup — duplicate URLs are rejected. |
| `title` | string | No | Original article title. |
| `name` | string | No | Publisher/source name (e.g. "MIT Technology Review"). This is what `l1.via` selects from. |
| `publishTime` | string | **Recommended** | ISO 8601 date or date string from source. Used for freshness display and sorting. `eir_post.py` auto-extracts from `sources[0].publishTime` if omitted. |

### Top-level item fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `lang` | `"zh"` \| `"en"` | **Yes** | **Required.** Language of this document's content. Determines which `{contentGroup}_{lang}` document is created. Not locale, not source language — the language the content is written in. API rejects if missing. API rejects `lang="en"` if hook contains CJK characters (Chinese hooks with English words are fine). |
| `slug` | string | No | Human-readable identifier. Falls back to `contentGroup` if omitted. |
| `interests` | object | **Recommended** | See Interest Signals section below. |
| `dot` | object | **Yes** | See dot section above. |
| `l1` | object | **Yes** | See l1 section above. `l1.title` is required. |
| `l2` | object | No | See l2 section above. Strongly recommended. |
| `sources` | array | No | See sources section above. At least 1 recommended. |
| `publishTime` | string | **Recommended** | ISO 8601 date of the primary source. Used for freshness display and sorting. If omitted, `eir_post.py` auto-extracts from `sources[0].publishTime`. Prefer providing explicitly. |
| `visibility` | `"private"` \| `"public"` | **Yes** | `private` for user content, `public` for pool/shared content. Set by API, not writer. |
| `channelId` | string | **Yes** | Content channel: `user-private`, `eir-express`, `shared-pick`, etc. Set by API, not writer. |

---

## via vs sources

`via` = `sources[].name` — the full set, not a subset.

| | `sources[]` | `l1.via` |
|---|---|---|
| **Purpose** | Machine: dedup, provenance, linking | Human: display attribution on card |
| **Contains** | Full metadata (url, title, name) | Just the names |
| **Type** | `Array<{url, title, name}>` | `string[]` |
| **Set by** | Writer (required) | Pipeline (auto-derived); API also falls back to `sources[].name` if empty |
| **Example** | `[{url: "...", name: "MIT Tech Review"}, {url: "...", name: "ArXiv"}]` | `["MIT Tech Review", "ArXiv"]` |

**Writers only need to set `sources[]`.** The pipeline auto-populates `via` from `sources[].name`; the API also falls back to `sources[].name` if `via` is empty. If the writer includes `via` it will be overwritten.

---

## lang field

`lang` means: **"what language is this content written in?"**

- Set by pipeline's `output_lang` parameter
- Each language version is a **separate document** with ID `{contentGroup}_{lang}`
- For bilingual users: pipeline generates two items with same `slug` but different `lang`
- `lang` is NOT locale (UI language) and NOT source_lang (language of source articles)

| Field | Meaning | Set by |
|-------|---------|--------|
| `lang` | Content language | Pipeline `output_lang` |
| `locale` (user pref) | UI language (dates, buttons) | User settings |

---

## Null handling

**Never set any field to `null`.** The front-end renders null as literal "placeholder" text.

| Instead of | Use |
|-----------|-----|
| `null` | `""` (empty string) |
| `null` | `[]` (empty array) |
| `{field: null}` | Omit the field entirely |

---

## Validation summary

### API rejects (400 error)

- `dot` missing or not an object
- `dot.hook` empty or >100 chars
- `dot.category` not in allowed enum
- `l1` missing or not an object
- `l1.title` empty or >200 chars
- `l1.via` present but not an array
- `l1.bullets` present but not an array, or >10 items
- `sources[].url` missing or not a valid URL
- `sources` >10 items per content item
- `lang` missing, or not `"zh"` or `"en"`
- `lang` is `"en"` but hook contains CJK characters (language mismatch)
- `items` empty, not an array, or >20 items
- No source `publishTime` within the global freshness window (currently 3 days) → `stale content`

### API skips (returned as `status: "skipped"`)

- Any `sources[].url` already exists for this user → `duplicate source_url`

### Pipeline should reject (pre-POST)

- `l1.title` missing → don't POST, file is broken
- `l2.content` <300 chars → quality too low
- `dot.hook` >50 chars → consider shortening (API allows up to 100 but shorter hooks render better)

---

## Content ID format

Both use the same ID scheme:

```
{8-char contentGroup}_{lang}    e.g. a3k9m2x7_zh
```

- `contentGroup`: 8-char base64url, globally unique, server-assigned on first POST
- All language versions of the same content **must** share the same `contentGroup` — POST the primary language first (without `contentGroup`), then use the returned `contentGroup` when posting other languages

---

## Interest Signals

Every content item should include interest signals:

```json
"interests": {
  "anchor": ["ai-agents"],
  "related": [
    { "slug": "a2a-protocol", "label": "A2A Protocol" }
  ]
}
```

### Anchor

- 1-3 slugs from the curation directives
- Must match user's interests (API validates, rejects 400 if mismatch)
- Use `topicSlug` (camelCase) in the content item

### Related

- 2-5 adjacent topics
- Slugs: lowercase-hyphenated
- Labels: human-readable in content's `lang`
- Unknown topics auto-created as candidates

See `eir-interest-rules.md` for curation guidelines.