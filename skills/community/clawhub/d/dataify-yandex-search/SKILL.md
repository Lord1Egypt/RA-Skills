---
name: dataify-yandex-search
description: "Run a Yandex web search. Do not use when the user explicitly requests Google, Bing, or DuckDuckGo."
---

# Dataify Yandex Search

## Workflow

1. Read the user's request and map it to the API fields below.
2. Apply defaults from the parameter descriptions only. Do not use the example YAML body as the source of defaults.

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

5. If the user requests changes, adjust the arguments, show the complete preview table again, and ask for confirmation again.
7. Call the API with the confirmed parameters:

```bash
```

8. Return the script stdout directly to the user. Do not parse, summarize, translate, filter, reformat, or otherwise process the API response.


## Preview Table


- `参数名`
- `当前值`
- `默认值`
- `说明`

The bundled script generates this table with:

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

## Defaults

Use these documented defaults when the user does not specify a field:

- `engine`: `yandex`
- `json`: `1`
- `yandex_domain`: `yandex.com`
- `lang`: `en` when `yandex_domain` is `yandex.com`
- `family_mode`: `1`
- `fix_typo`: `true`
- `groups_on_page`: `20`
- `no_cache`: `false`

No documented default:

- `text`: required from the user request.
- `lr`: leave unset unless the user specifies it.
- `p`: leave unset unless the user specifies it; page numbering starts from `0` when specified.

Important corrections from the API example body:

- Do not treat example `family_mode: "0"` as the default. The description default is medium, so use `1`.
- Do not treat example `no_cache: "true"` as the default. The description says `false` is the default.

## Field Mapping

- `--json`: output format. Use `1` JSON, `2` JSON+HTML, `3` HTML, or `4` Light JSON.
- `--yandex-domain`: Yandex domain such as `yandex.com`, `yandex.ru`, `ya.ru`, `yandex.kz`, `yandex.com.tr`, or another supported domain.
- `--lang`: search language, for example `en`, `ru`, `tr`.
- `--lr`: country or region ID.
- `--p`: page number, starting from `0`.
- `--family-mode`: safe search mode. Use `0` off, `1` moderate, `2` strict.
- `--fix-typo`: `true` or `false`.
- `--groups-on-page`: maximum result groups per page.
- `--no-cache`: `true` to bypass cache, `false` to use cache.
- `--params-json`: JSON object of raw field overrides for unusual requests. Use `null` to omit a defaulted field.

For the full field list, read `references/api_fields.md` only when needed.

## Examples

Preview parameters for a normal search:

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --preview
```

After user confirmation, call the API:

```bash
```

Preview Russian Yandex, page 2, HTML output:

```bash
python3 scripts/yandex_search.py --text "artificial intelligence news" --yandex-domain yandex.ru --lang ru --p 1 --json 3 --preview
```

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/yandex_search.py --help
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
