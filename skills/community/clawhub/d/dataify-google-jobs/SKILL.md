---
name: dataify-google-jobs
description: "Search Google Jobs for job and recruitment listings. Do not use to scrape a known Indeed job URL."
---

# Dataify Google Jobs

Use this skill to turn a user's Google Jobs request into a Dataify Scraper API form POST.
## Workflow

1. Parse the user's request into Dataify Google Jobs fields. Use `q` as the job search query and set `engine` to the fixed value `google_jobs`.
2. Build request parameters from the user-provided values plus documented defaults only. Defaults must come from the parameter descriptions in `references/google_jobs_api.md`; never treat examples as defaults.
   - `engine`: fixed `google_jobs`
   - `json`: default `1`
   - `google_domain`: default `google.com`
   - `no_cache`: default `false`
   - All other parameters have no documented default and must stay unset unless the user provides them.
4. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_jobs.py`. 

```bash
python3 scripts/google_jobs.py --q "software engineer jobs" --location "San Francisco" --gl us --hl en
```


```bash
python3 scripts/google_jobs.py --request "搜索 java 相关工作" --preview-table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_jobs.py --params-json '{"q":"software engineer jobs","location":"San Francisco","gl":"us","hl":"en"}'
```

For a natural-language fallback, pass the whole request:

```bash
python3 scripts/google_jobs.py --request "搜索美国旧金山的软件工程师工作，语言英文，不使用缓存"
```


## Field Mapping

Use `references/google_jobs_api.md` for the complete parameter descriptions and defaults.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_jobs`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when the required job search query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not include `Authorization` in the preview table.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- geographic search origin -> `location`
- encoded Google location -> `uule`
- next page -> `next_page_token`
- chips/filter token from Google Jobs -> `chips`
- search radius in kilometers -> `lrad`
- work from home / remote-only filter -> `ltype: "1"` when requested
- Google-provided filter string -> `uds`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_jobs.py --q "software engineer jobs" --location "San Francisco" --gl us --hl en
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
