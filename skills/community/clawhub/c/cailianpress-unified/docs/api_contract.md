# API Contract

## Query types

### `telegraph`
Returns raw telegraph items from the canonical CLS telegraph source.

Parameters:
- `--hours <int>` optional
- `--limit <int>` optional
- `--format json|text|markdown`

### `red`
Returns telegraph items filtered by `level in {A, B}`.

Parameters:
- `--hours <int>` optional
- `--limit <int>` optional
- `--format json|text|markdown`

### `hot`
Returns telegraph items filtered by reading count.

Parameters:
- `--hours <int>` optional
- `--limit <int>` optional
- `--min-reading <int>` optional, default `10000`
- `--format json|text|markdown`

### `article`
Returns or resolves article detail metadata from a known CLS article id.

Parameters:
- `--id <int>` required
- `--format json|text|markdown`

## Canonical field meanings

- `id`: CLS article/telegraph identifier
- `title`: headline
- `brief`: summary
- `content`: full or extended text when available
- `level`: raw CLS level field
- `is_red`: derived boolean, true when `level in {A, B}`
- `reading_num`: CLS reading count
- `ctime`: raw publish timestamp
- `published_at`: normalized Asia/Shanghai datetime string
- `shareurl`: article share URL
- `raw_source`: adapter name used to produce the item

## Endpoint quick reference

| Endpoint | Status | Purpose | Notes |
|---|---|---|---|
| `https://www.cls.cn/nodeapi/telegraphList` | usable | primary telegraph list ingestion | current recommended main source |
| `https://www.cls.cn/nodeapi/updateTelegraphList` | usable | update / incremental-like list retrieval | useful as helper, not primary source |
| `https://api3.cls.cn/share/article/{id}` | usable | article/share detail resolution | suitable for detail completion |
| `https://www.cls.cn/telegraph` | usable | page fallback | use only as HTML fallback |
| `/v1/roll/get_roll_list` | not recommended | front-end main roll API | direct calls currently fail with `签名错误` |
| `nodeapi/refreshTelegraphList` | limited | lightweight refresh payload | not suitable as the canonical ingest source |

## Recommended call path

1. Ingest telegraphs from `nodeapi/telegraphList`
2. Optionally compare / assist with `nodeapi/updateTelegraphList`
3. Resolve detail with `api3.cls.cn/share/article/{id}`
4. Use `www.cls.cn/telegraph` only as fallback
5. Do not route production ingestion through `/v1/roll/get_roll_list`
