# Baidu Baike API Notes

Use this reference before changing lightweight entity lookup behavior.

## Purpose

Baike lookup is a low-budget path for simple entity questions such as:

```text
这是什么？
量子计算是什么？
某个产品/机构/地点有没有百科词条？
```

It is not a substitute for web research, recent news, reviews, complaints, or forum discussion.

## Candidate List

```text
GET https://appbuilder.baidu.com/v2/baike/lemma/get_list_by_title
```

Query parameters:

```text
lemma_title=<term>
top_k=1..100
```

Expected useful fields:

```text
lemma_id
lemma_title
lemma_desc
is_default
url
```

Use this first when the term may be ambiguous.

## Content Lookup

```text
GET https://appbuilder.baidu.com/v2/baike/lemma/get_content
```

Query parameters:

```text
search_type=lemmaTitle|lemmaId
search_key=<title-or-id>
```

Prefer `lemmaId` when the candidate list returned an ID.

Expected useful fields:

```text
lemma_id
lemma_title
lemma_desc
url
summary
abstract_plain
abstract_html
abstract_structured
pic_url
square_pic_url
relations
```

## Authentication

Use the same key environment as web search:

```text
BAIDU_AI_SEARCH_API_KEYS=key1,key2,key3
```

Never write or print the full key. `lookup.py` defaults to the official Baike header:

```text
Authorization: Bearer <key>
```

It can also send these when compatibility testing requires it:

```text
X-Appbuilder-Authorization: Bearer <key>
```

Use `--auth-header both` or `--auth-header x-appbuilder` only if live testing shows the default `Authorization` header is not accepted in a specific environment.

## Response Compatibility

The official docs describe a `result` array for candidate lists, while the success example shows a top-level array. `lookup.py` normalizes both shapes into:

```json
{"result": [...]}
```

## Cache

Baike lookup uses `cache/baike` by default. The cache stores URL, response, and timestamp only. It must not store Authorization headers or keys.

Bypass cache with:

```bash
python scripts/search.py "<topic>" --mode lookup --no-cache
```

## Output

Lookup runs write:

```text
baike_candidates.json
baike_content.json
fallback_web_results.json
errors.jsonl
run_summary.json
lookup_pack.md
```

Use `lookup_pack.md` for agent-readable output. Use JSON files for exact raw response inspection.

## Excluded APIs

Do not add these to the default path:

- SecondKnow video
- image or video search
- Aladdin beta cards
- intelligent search generation / generated-answer endpoints

These either do not serve the text-first search-tool goal or add a generated summary layer that conflicts with preserving source evidence.
