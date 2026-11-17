---
name: dataify-google-scholar
description: "Search Google Scholar for academic papers and scholarly results. Do not use for patents or general web search."
---

# Dataify Google Scholar

Use this skill to turn a user's Google Scholar request into a Dataify Scraper API call.
## Workflow

1. Parse the user's request into Dataify Google Scholar fields. Always set `engine` to `google_scholar`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters from the user's request plus documented defaults. Defaults must come only from parameter descriptions in `references/google_scholar_api.md`; never use example values as defaults.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_scholar.py`.

Preview the complete parameter table:

```bash
python3 scripts/google_scholar.py --request "搜索 large language model，2020 到 2024，返回 20 条" --preview
```

Call the API after the user confirms:

```bash
python3 scripts/google_scholar.py --q "large language model" --as_ylo 2020 --as_yhi 2024 --num 20
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_scholar.py --params-json '{"q":"large language model","as_ylo":"2020","as_yhi":"2024","num":"20"}'
```


## Field Mapping

Use `references/google_scholar_api.md` when you need the exact field list, defaults, or accepted values.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_scholar`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Include documented defaults when the user did not specify a field.
- Omit optional fields that have no documented default and no user value.
- Ask a follow-up only when no usable search condition can be inferred. A usable search condition is `q`, `cites`, or `cluster`.
- Do not combine `cluster` with `q` or `cites`; `cluster` must be used by itself.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- language-restricted results -> `lr`, formatted like `lang_fr` or `lang_fr|lang_de`
- page number N -> `start: String((N - 1) * 10)`
- result count -> `num`, range `1` to `20`
- cited-by search -> `cites`
- all versions search -> `cluster`
- year range lower bound -> `as_ylo`
- year range upper bound -> `as_yhi`
- past-year/date sort -> `scisbd: "1"` for abstracts only or `scisbd: "2"` for all content
- include patents -> `as_sdt: "7"`
- exclude patents -> `as_sdt: "0"`
- US case law -> `as_sdt: "4"`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- disable similar/omitted result filter -> `filter: "0"`
- exclude citations -> `as_vis: "1"`
- include citations -> `as_vis: "0"`
- review articles only -> `as_rr: "1"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_scholar.py --help
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
