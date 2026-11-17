---
name: dataify-google-play
description: "Search Google Play for apps, rankings, or store results. Do not use to collect reviews from a known app URL."
---

# Dataify Google Play

Use this skill to turn a user's Google Play request into a Dataify Scraper API call.
## Workflow

1. Parse the user's request into Dataify Google Play fields. Use `q` as the app-store search query and set `engine` to `google_play`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required defaults. Use `json: "1"` unless the user asks for another output format. Do not treat example values in the API docs as defaults.
5. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_play.py`.

```bash
python3 scripts/google_play.py --q "meditation app" --gl us --hl en --json 1
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_play.py --params-json '{"q":"meditation app","gl":"us","hl":"en","json":"1"}'
```


```bash
python3 scripts/google_play.py --request "搜索美国 Google Play 上的冥想 app，英文，JSON" --dry-run
```


## Field Mapping

Use `references/google_play_api.md` when you need the exact field list, defaults, and parameter values.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_play`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request.
- Ask a follow-up only when required `q` cannot be inferred and the request is not a category/chart/device-only request supported by the user's provided fields.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not use more than one of `next_page_token`, `section_page_token`, `see_more_token`, and `chart` together.
- Do not use `store_device` together with `apps_category` or `q`.
- Use `age` only when `apps_category` is `FAMILY`.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- app search phrase -> `q`
- country or region for Google Play behavior -> `gl`
- interface/search language -> `hl`
- Google Play category -> `apps_category`
- next page token -> `next_page_token`
- section page token -> `section_page_token`
- top chart / popular ranking -> `chart`
- see more token -> `see_more_token`
- phone/tablet/tv/chromebook/watch/car device browsing -> `store_device`
- kids/family category -> `apps_category: "FAMILY"`
- age 5 and under -> `age: "AGE_RANGE1"`
- age 6 to 8 -> `age: "AGE_RANGE2"`
- age 9 to 12 -> `age: "AGE_RANGE3"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_play.py --q "meditation app" --gl us --hl en --json 1
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
