---
name: dataify-bing-videos
description: "Search Bing Videos for video results. Do not use for general Bing web search or media-file downloads."
---

# Bing Videos

## Overview


The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Defaults

Use defaults only when they come from parameter descriptions, not from request examples.

- `engine`: default `bing_videos`.
- `json`: default `1`.
- `first`: default `1`.
- `no_cache`: default `false`.
- `q`: default `pizza` from the field description. Prefer the user's requested query whenever provided.
- `mkt`, `cc`, `setlang`, `length`, `date`, `resolution`, `source_site`, `price`: no default.

Treat source-document sample values such as `en-US`, `us`, `short`, `lt1440`, `360p`, `dailymotion.com`, `free`, or `no_cache=true` as examples only. `pizza` is used only because the `q` field description states it as the default.

## Workflow

1. Identify the user's video search query and map optional requirements to API fields:
   - `q`: search keywords. Default `pizza` when the user provides no query.
   - `json`: output format. Default `1`; use `2` for JSON plus HTML, `3` for HTML.
   - `mkt`: display language and market, such as `en-US` or `zh-CN`.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, `uk`.
   - `setlang`: two-letter search language, such as `en`, `zh`, or `ja`.
   - `first`: organic result offset. Default `1`.
   - `length`: video duration filter: `short`, `medium`, or `long`.
   - `date`: freshness filter: `lt1440`, `lt10080`, `lt43200`, or `lt525600`.
   - `resolution`: resolution filter: `lowerthan_360p`, `360p`, `480p`, `720p`, or `1080p`.
   - `source_site`: source filter, such as `vimeo.com`, `dailymotion.com`, or `cnn.com`.
   - `price`: `free` or `paid`.
   - `no_cache`: cache behavior. Default `false`; use `true` only when requested.
2. Prefer explicit user-provided field values over inferred values. Never fill fields from API example YAML values.

```bash
python3 scripts/bing_videos.py --prompt "pizza" --dry-run --table
```

4. If the user asks to modify parameters, apply their changes and show only consequential changed values when a recap is useful.
5. Call the live API only after the user confirms the displayed parameters.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - The script adds a `Bearer ` prefix when the token does not already include one.
7. Return the live script output directly to the user. Do not summarize video results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

Preview full parameters before confirmation:

```bash
python3 scripts/bing_videos.py \
  --prompt "用必应视频搜索 OpenAI 发布会，过去一周，免费，1080p，返回 JSON 和 HTML" \
  --dry-run \
  --table
```


```bash
python3 scripts/bing_videos.py \
  --prompt "用必应视频搜索 OpenAI 发布会，过去一周，免费，1080p，返回 JSON 和 HTML"
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--setlang`, `--first`, `--length`, `--date`, `--resolution`, `--source-site`, `--price`, `--no-cache`
- `--field key=value` for any supported API field
- `--body-format form|json`, default `form`
- `--dry-run` to print parsed payload JSON and skip network/auth checks

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/bing_videos.py --prompt "pizza" --dry-run --table
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
