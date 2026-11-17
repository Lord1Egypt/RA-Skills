---
name: dataify-google-lens
description: "Run Google Lens or reverse-image search from an image. Do not use for text-only Google Images queries."
---

# Dataify Google Lens

Use this skill to turn a user's Google Lens or reverse-image-search request into a Dataify Scraper API form submission.
## Workflow

1. Parse the user's request into Google Lens fields. Use `url` for the image URL, set `engine` to `google_lens`, and infer optional fields only when the user asks for them.
2. Build request parameters from the user's request. If the user did not specify a field, use only the documented default from the parameter description:
   - `engine`: `google_lens`
   - `json`: `1`
   - `type`: `all`
   - `no_cache`: `false`
   Fields with no documented default stay unset. Do not treat examples such as `us`, `en`, `active`, or `true` as defaults.

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us --preview
```

Ask the user: `请确认是否需要修改这些参数；确认无误后我再调用接口。`

5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_lens.py`. The script submits form data to the hardcoded API endpoint; it does not send a JSON body.

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us
```

Natural-language fallback is available when useful:

```bash
python3 scripts/google_lens.py --request "Search Google Lens for https://example.com/image.jpg, products, country US, safe on, no cache"
```


## Field Mapping

Use `references/google_lens_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always encode request data as UTF-8.
- Always force `engine` to `google_lens`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Use documented defaults when the user does not specify a value. Omit fields that have no documented default and were not requested.
- Ask a follow-up only when the required image `url` cannot be inferred from the user's request.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Never include `Authorization` in the preview table, and never print the token value in the final explanation.

Common mappings:

- Image URL, picture URL, reverse image search target -> `url`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- country or region for Lens behavior -> `country`
- all results -> `type: "all"`
- product results -> `type: "products"`
- about this image -> `type: "about_this_image"`
- exact matches -> `type: "exact_matches"`
- visual matches or similar images -> `type: "visual_matches"`
- extra query/keyword/refinement used with `all`, `visual_matches`, or `products` -> `q`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_lens.py --help
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
