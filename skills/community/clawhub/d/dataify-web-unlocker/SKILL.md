---
name: "dataify-web-unlocker"
description: "Fetch blocked and dynamic web content via Dataify Web Unlocker API. Automatically identify and bypass CAPTCHA challenges, execute full-page JavaScript rendering, and return complete raw HTML source code or PNG webpage screenshots. Applicable for complex crawling scenarios including dynamic loading pages and SPA single-page applications."
---

# Dataify Web Unlocker

Use the bundled wrappers to call Dataify's Web Unlocker API with a stable parameter set across platforms.

Treat every request field as optional user input except for `url`. Confirm the target `url` with the user before making the request if it is not already explicit in the prompt. For every other field, keep the default value unless the user explicitly asks to override it.

## Workflow

1. Use `scripts/invoke-dataify-web-unlocker.py` on macOS/Linux or when cross-platform portability matters.
2. Use `scripts/invoke-dataify-web-unlocker.ps1` on Windows when PowerShell is the best fit.
3. Use a raw `curl` command only when the user explicitly asks for it.
4. Confirm the target `url` with the user if it was not clearly provided. Do not guess the URL.
5. Treat every other request field as optional. Override a field only when the user explicitly asked for a non-default value.
6. Let the script read `DATAIFY_API_TOKEN` from the environment.
7. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
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
