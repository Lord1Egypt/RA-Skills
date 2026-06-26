# Reference — Endpoints & Tools

The FRED MCP server exposes **6 tools**. Five wrap a specific FRED endpoint; the sixth (`fred_request`) reaches **any** endpoint. The server always injects `api_key` and `file_type=json` — never pass those.

---

## The 6 tools

| Tool | FRED endpoint | Required input | Purpose |
|------|---------------|----------------|---------|
| `fred_series_search` | `/series/search` | `search_text` | Find a `series_id` by keyword. |
| `fred_series` | `/series` | `series_id` | Metadata for one series. |
| `fred_series_observations` | `/series/observations` | `series_id` | The actual data points (+ transforms). |
| `fred_category_series` | `/category/series` | `category_id` | Series within a category. |
| `fred_release_series` | `/release/series` | `release_id` | Series within a release. |
| `fred_request` | **any** | `endpoint` | Generic passthrough to the whole API. |

Optional parameters per tool are in `../../mcp/docs/03-tools-reference.md`.

---

## Quick parameter notes

- `fred_series_search`: `search_text`, `limit?`, `order_by?` (`search_rank`, `popularity`, …), `sort_order?`, `search_type?` (`full_text`|`series_id`).
- `fred_series_observations`: `series_id`, `observation_start?`, `observation_end?`, `units?`, `frequency?`, `aggregation_method?`, `sort_order?`, `limit?`, `offset?`.
- `fred_category_series` / `fred_release_series`: id + `limit?` + `offset?`.

---

## Generic endpoint pattern (`fred_request`)

```json
{ "endpoint": "<path without leading /fred>", "params": { /* endpoint-specific */ } }
```

Common endpoints reachable this way:

| Goal | `endpoint` | `params` |
|------|-----------|----------|
| Browse category tree | `category/children` | `{ "category_id": 0 }` |
| One category's metadata | `category` | `{ "category_id": 125 }` |
| All releases | `releases` | — |
| Series in a release | `release/series` | `{ "release_id": 53 }` |
| Data sources | `sources` | — |
| Series for a tag | `tags/series` | `{ "tag_names": "gdp" }` |
| Recently updated series | `series/updates` | `{ "limit": 10 }` |
| As-of (vintage) dates | `series/vintagedates` | `{ "series_id": "GDP" }` |
| A series' categories | `series/categories` | `{ "series_id": "UNRATE" }` |

---

## Complete catalog

For the full list of FRED endpoints and every parameter, see the API docs:

- Tools reference (this server): `../../mcp/docs/03-tools-reference.md`
- Official FRED API catalog: <https://fred.stlouisfed.org/docs/api/fred/>

> Verification needed: confirm endpoint paths and required params at the official catalog.
