---
name: browser-fetch
description: Use browser-backed fetch when a page needs real Chromium rendering, JavaScript execution, browser user agent behavior, proxy-aware navigation, or blocked-page diagnostics instead of plain HTTP fetch.
---

# Browser Fetch

Use the skill-relative wrapper through `bash`. Do not assume `browser-fetch` is
on `PATH` or installed with executable file permissions.

```bash
bash {baseDir}/bin/browser-fetch https://example.com/ --json
```

Default output is extracted page text from `body`. Browser Fetch enables Chromium stealth evasions by default. Use `--html` for full HTML, `--json` for metadata plus content, or `--output PATH --metadata PATH` when another command should read files.

Supported options:

- `--timeout MS`: navigation timeout, default `15000`.
- `--user-agent VALUE`: override browser context user agent.
- `--proxy-server URL`: proxy for this call.
- `--chromium-path PATH`: Chromium executable path.
- `--no-stealth`: disable default stealth evasions for A/B checks.
- `--wait-until VALUE`: `domcontentloaded`, `load`, or `networkidle`.
- `--selector CSS`: selector for text extraction, default `body`.
- `--html`: output full page HTML.
- `--text`: output extracted page text.
- `--json`: output metadata plus content.
- `--output PATH`: write content to a file.
- `--metadata PATH`: write metadata JSON to a file.
- `--include-metadata`: write compact metadata JSON to stderr.
- `--fail`: exit non-zero for HTTP status `>= 400`.

Proxy behavior follows curl-style ambient proxy defaults. The CLI uses `--proxy-server` first, then `FETCH_PROXY_SERVER`, then ambient `HTTP_PROXY` or `HTTPS_PROXY`. Ambient `HTTP_PROXY` or `HTTPS_PROXY` is used by default. Set `FETCH_USE_ENV_PROXY=0` to ignore ambient proxy variables.

Exit codes:

- `0`: acceptable fetch.
- `1`: completed fetch with blocked signal, or `--fail` with HTTP status `>= 400`.
- `2`: command-line usage error.
- `3`: runtime fetch error such as timeout, DNS, proxy, browser launch, or connection failure.
