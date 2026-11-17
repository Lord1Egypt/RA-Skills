---
name: dataify-bing-images
description: "Search Bing Images for image results. Do not use for Bing web, news, shopping, map, or video results."
---

# Bing Images

Use `scripts/bing_images.py` to turn a natural-language image request into a Bing Images API call. The API schema and uncommon field details are in [references/api.md](references/api.md); read it only when a requested filter is unclear.

## Interaction policy

Optimize for the user's outcome, not the API request shape.

- For ordinary read-only image searches, infer reasonable parameters and execute immediately. Do not pause to show a full parameter table or ask for confirmation.
- Before execution, give at most one short natural-language update when useful, such as `按“木偶实物摄影”搜索约 6 张照片，尺寸不限。`
- If a term has a plausible alternate meaning, state the assumption and continue when the search is easy to refine. Ask only when the ambiguity would materially change the result and no safe assumption is reasonable.
- Ask before execution only when the request introduces a meaningful cost, a consequential license/commercial-use constraint, or another choice that cannot be inferred safely.
- Show the full parameter table only when the user explicitly asks to inspect or modify advanced search settings. Technical fields such as `engine`, `json`, `first`, and `no_cache` should not appear in the ordinary flow.

## Request construction

Preserve explicit user choices. Infer only filters supported by the prompt. Do not copy example values into live requests.

Defaults provided by the API wrapper:

- `engine=bing_images`
- `json=1`
- `first=1`
- `no_cache=false`


```bash
# Ordinary search: execute directly after applying the interaction policy.

# Advanced-settings review requested by the user.
python3 scripts/bing_images.py --prompt "木偶实物摄影，6张" --preview
```

Useful explicit overrides:

- `--q`, `--json`, `--mkt`, `--cc`, `--first`, `--count`
- `--imagesize`, `--color2`, `--photo`, `--aspect`, `--face`, `--age`, `--license`, `--no-cache`
- `--field key=value` for any supported API field

## Results

Return the useful image results rather than raw API plumbing.

- For a normal image-finding request, present a compact gallery or concise list using the returned image URL, title, dimensions, and source link when available.
- Prefer the original image URL for display and keep attribution/source links accessible.
- Mention that licensing is unverified unless the user requested a license filter.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- If the API returns more items than requested, show only the requested number unless the user asks for all results.

## Authentication and account handling

Read `DATAIFY_API_TOKEN` from the environment. Never display its value or ask the user to paste it into chat.

Detect the current operating system and shell before showing setup instructions. Never ask the user to paste the token into chat. After configuration succeeds, continue the original task without requiring the user to repeat it.

- If missing, offer https://dashboard.dataify.com/login?utm_source=skill and state that new accounts receive 50 free credits. Show only the session-scoped setup command appropriate to the current OS and shell.
- After the user says it is configured, verify only whether the variable is present, then continue the original request without making them repeat it.
- Explain when a terminal or app restart may be required for environment changes to take effect. Do not recommend a project `.env` unless the execution path loads it and the file is ignored by version control.
- For an invalid token, direct the user to API-key management. For insufficient credits, direct them to balance or recharge management.
- Do not promote registration or the dashboard during normal successful use.

If a live call fails because of sandboxed network access, retry through the standard approval mechanism. Do not repeat a successful live call merely because the UI truncated the response; instead, preserve or retrieve the existing output locally when possible.

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
# Ordinary search: execute directly after applying the interaction policy.
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
