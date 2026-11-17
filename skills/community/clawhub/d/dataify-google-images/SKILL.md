---
name: dataify-google-images
description: "Search Google Images for image results. Do not use for Google Lens reverse-image search or general web results."
---

# Dataify Google Images

Use this skill to turn a user's Google Images request into a Dataify Scraper API form submission.
## Workflow

1. Parse the user's request into Google Images fields. Use `q` as the image search query and set `engine` to `google_images`.
2. Apply documented defaults when the user does not specify a value. Use only defaults stated in the parameter descriptions: `json=1`, `google_domain=google.com`, `start=0`, `nfpr=0`, `filter=1`, `device=desktop`, and `no_cache=false`. Do not treat examples such as `pizza`, `us`, `en`, `radius=10`, `tbm=isch`, `render_js=true`, or `ai_overview=true` as defaults.
3. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
4. Build request parameters with the fields the user requested plus documented defaults. The script submits these parameters as form data, not a JSON request body.
5. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_images.py`.

```bash
python3 scripts/google_images.py --q "red sneakers" --json 1
```

For many fields, pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_images.py --params-json '{"q":"red sneakers","json":"1","google_domain":"google.com","gl":"us","hl":"en","device":"mobile"}'
```


## Field Mapping

Use `references/google_images_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_images`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Include documented default values when the user did not request a value. Omit optional fields only when they have no documented default and the user did not request them.
- Ask a follow-up only when the required image query `q` cannot be inferred.
- If `uule` is present, omit `location`, `lat`, `lon`, and `radius`.
- If `location` is present, omit `uule`, `lat`, and `lon`.
- Use `lat` and `lon` together. If only one is available, ask for the missing coordinate.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- country-restricted results -> `cr`, formatted like `countryFR`
- language-restricted results -> `lr`, formatted like `lang_fr`
- named search origin -> `location`
- Google encoded location -> `uule`
- GPS coordinates -> `lat` and `lon`
- location bias radius in meters -> `radius`
- page number N -> `start: String((N - 1) * 10)`
- advanced image filters, size, color, type, rights, or date -> `tbs`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- desktop/tablet/mobile -> `device`
- render JavaScript -> `render_js: "true"`
- bypass cache -> `no_cache: "true"`
- include AI Overview -> `ai_overview: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_images.py --q "red sneakers" --json 1
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
