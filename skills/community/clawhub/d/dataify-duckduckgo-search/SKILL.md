---
name: dataify-duckduckgo-search
description: "Run a DuckDuckGo web search. Do not use when the user explicitly requests Google, Bing, or Yandex."
---

# Dataify DuckDuckGo Search

## Workflow

Use `python3` to run the bundled script for the entire flow. Do not build the HTTP request manually unless the script needs maintenance.


```bash
python3 scripts/duckduckgo_search.py --request "<user request>" --preview
```

On Windows workspaces where the `python3` alias is unavailable, use the installed Python 3 launcher for the same script, for example `python scripts/duckduckgo_search.py ...`.



```bash
```


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

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/duckduckgo_search.py --help
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
