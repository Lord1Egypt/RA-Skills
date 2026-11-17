---
name: "dataify-web-unlocker"
description: "Fetch HTML or a screenshot from a known blocked or JavaScript-rendered webpage with Dataify Web Unlocker. Use for CAPTCHA-protected, dynamic, or SPA pages. Do not use for search-engine discovery or platform-specific structured records."
---

# Dataify Web Unlocker

Use the bundled wrappers to call Dataify's Web Unlocker API with a stable parameter set across platforms.

Treat every request field as optional user input except for `url`. Confirm the target `url` with the user before making the request if it is not already explicit in the prompt. For every other field, keep the default value unless the user explicitly asks to override it.


## Quick Start

**Input:** one public webpage URL.

```bash
python3 scripts/invoke-dataify-web-unlocker.py --url "https://example.com"
```

This is a synchronous request: the command prints the unlocked page result directly.

If `DATAIFY_API_TOKEN` is missing, log in or register at https://dashboard.dataify.com/login?utm_source=skill. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.

## Workflow

1. Use `scripts/invoke-dataify-web-unlocker.py` on macOS/Linux or when cross-platform portability matters.
2. Use `scripts/invoke-dataify-web-unlocker.ps1` on Windows when PowerShell is the best fit.
3. Use a raw `curl` command only when the user explicitly asks for it.
4. Confirm the target `url` with the user if it was not clearly provided. Do not guess the URL.
5. Treat every other request field as optional. Override a field only when the user explicitly asked for a non-default value.
6. Let the script read `DATAIFY_API_TOKEN` from the environment.
7. If the token is missing, stop and tell the user: `Dataify requires an API token. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Once registration is complete, tell me and I'll continue the current task.`.
8. Return the API response body directly unless the user asks for extra post-processing.

## Set DATAIFY_API_TOKEN

Prefer a permanent environment-variable setup instead of setting the token only for the current terminal session.

Windows PowerShell, permanent for the current user:

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "your_token_here", "User")
```

Then reopen PowerShell. If the current session also needs the token immediately, run:

```powershell
$env:DATAIFY_API_TOKEN = "your_token_here"
```

macOS or Linux, permanent for bash:

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

macOS or Linux, permanent for zsh:

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

## Default request body

Use these defaults unless the user asks for different values. Only `url` must be collected before the real request is sent:

```json
{
  "url": "https://www.google.com",
  "type": "html",
  "js_render": "True",
  "block_resources": "",
  "clean_content": "",
  "country": "us",
  "headers": "",
  "cookies": "",
  "wait": "",
  "wait_for": "",
  "follow_redirect": "True",
  "isjson": "1"
}
```

## Preferred commands

Ask for the URL first if the user did not provide one. After that, the minimal call should pass only `url` and rely on defaults for everything else.

Cross-platform Python:

```bash
python scripts/invoke-dataify-web-unlocker.py --url "https://www.google.com"
```

Windows PowerShell:

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" -Url "https://www.google.com"
```

Common overrides in Python:

```bash
python scripts/invoke-dataify-web-unlocker.py \
  --url "https://example.com" \
  --js-render "True" \
  --country "us" \
  --wait "3000" \
  --wait-for ".main-content"
```

Common overrides in PowerShell:

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" `
  -Url "https://example.com" `
  -JsRender "True" `
  -Country "us" `
  -Wait "3000" `
  -WaitFor ".main-content"
```

Use `--dry-run` or `-DryRun` to preview the endpoint, authorization state, and JSON payload without making the network request:

```bash
python scripts/invoke-dataify-web-unlocker.py --url "https://example.com" --dry-run
```

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" -Url "https://example.com" -DryRun
```

## Raw curl fallback

If the user explicitly wants the raw request, use `curl.exe` in PowerShell, not `curl`, to avoid the PowerShell alias ambiguity.

Before calling the API, check the token:

```powershell
if (-not $env:DATAIFY_API_TOKEN) {
  Write-Error "DATAIFY_API_TOKEN is not set. Sign in at https://dashboard.dataify.com?utm_source=skill to obtain it."
  exit 1
}
```

Then send the request:

```powershell
curl.exe -X POST "https://webunlocker.dataify.com/request" `
  -H "Authorization: Bearer $env:DATAIFY_API_TOKEN" `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://www.google.com\",\"type\":\"html\",\"js_render\":\"True\",\"block_resources\":\"\",\"clean_content\":\"\",\"country\":\"us\",\"headers\":\"\",\"cookies\":\"\",\"wait\":\"\",\"wait_for\":\"\",\"follow_redirect\":\"True\",\"isjson\":\"1\"}"
```

## Parameter notes

- `url` is the only field that should be treated as required input from the user.
- Ask the user to confirm `url` if it is missing or ambiguous.
- `headers` and `cookies` are passed through as strings exactly as provided by the caller.
- Keep boolean-like fields as strings such as `"True"` because that matches the supplied API format.
- Keep `isjson` as `"1"` unless the user explicitly requests a different response mode.
- Prefer minimal overrides. Do not invent custom headers, cookies, waits, render settings, or country overrides unless the user requested them.
- The Python wrapper uses only the standard library so it stays portable and does not require third-party packages.

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
