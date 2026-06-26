---
name: dataify-duckduckgo-search
description: Use when the user asks to search DuckDuckGo, fetch DuckDuckGo results
---

# Dataify DuckDuckGo Search

## Workflow

Use `python3` to run the bundled script for the entire flow. Do not build the HTTP request manually unless the script needs maintenance.

Always preview parameters before every API call:

```bash
python3 scripts/duckduckgo_search.py --request "<user request>" --preview
```

On Windows workspaces where the `python3` alias is unavailable, use the installed Python 3 launcher for the same script, for example `python scripts/duckduckgo_search.py ...`.

Show the preview table to the user. The table must include the complete field list except `Authorization`, and only these columns: parameter name, current value, default value, and description. Ask whether the user wants to modify any parameter. Do not call the API until the user confirms.

After the user confirms, call the API with the same request and explicit overrides, adding `--confirmed`. If the user provides a token in the conversation, pass it explicitly:

```bash
python3 scripts/duckduckgo_search.py --request "<user request>" --token "<DATAIFY_API_TOKEN>" --confirmed
```

The script reads `DATAIFY_API_TOKEN` from the environment when `--token` is not provided. If no token is available, stop and ask the user to provide a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).

## Field Mapping

Pass the user's full request to `--request`; the script automatically maps natural-language hints and explicit assignments to Dataify fields:

| Field | Behavior |
| --- | --- |
| `engine` | Always `duckduckgo`. |
| `q` | Search query parsed from the user request or `--q`. Required. |
| `json` | Output format: `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. Defaults to `1`. |
| `kl` | DuckDuckGo region code such as `us-en`, `uk-en`, or `fr-fr`; no default. |
| `search_assist` | `true` or `false`; defaults to `false`; cannot be sent with `m`. If enabled, the script omits `m`. |
| `safe` | `1` strict, `-1` moderate (default), `-2` off. |
| `df` | `d`, `w`, `m`, `y`, or a date range like `2021-06-15..2024-06-16`. |
| `start` | Result offset; defaults to `0` or empty according to the API description. |
| `m` | Maximum result count, defaults to `50`, clamped to `1..50`; omitted when `search_assist=true`. |
| `no_cache` | `true` skips cache; `false` uses cache by default. |

Use default values from parameter descriptions when the user does not specify a field: `engine=duckduckgo`, `json=1`, `search_assist=false`, `safe=-1`, `start=0`, `m=50`, and `no_cache=false`. `q`, `kl`, and `df` have no default. Do not treat API documentation examples as defaults: never use `q=pizza`, `kl=us-en`, `search_assist=true`, `safe=1`, `df=d`, `start=0` because it appeared in an example, `m=10`, or `no_cache=true` unless the user request or the documented default says so.

For exact control, pass explicit flags such as `--q`, `--json`, `--kl`, `--safe`, `--df`, `--start`, `--m`, `--no-cache`, and `--search-assist`; explicit flags override the natural-language parser.

## Response Handling

The script submits the request as `application/x-www-form-urlencoded` form data, not JSON.

Return the script stdout directly to the user. Do not summarize, translate, pretty-print, filter, or otherwise process the API response.
