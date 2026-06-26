---
name: browser-network-inspector
description: Browser-side request inspection and reporting for user-authorized web debugging. Use when you want one skill to observe page fetch/XHR/WebSocket activity, inspect login/register/API flows, and generate clean reports from browser interactions. This is for browser debugging, not raw system-wide packet sniffing, credential extraction, or auth bypass.
---

# Browser Network Inspector

A **single-skill browser debugging capture tool** for inspecting page requests and turning them into readable reports.

Use this when you want to:

- see which APIs a page or button triggers
- inspect login, registration, or form-submit flows
- capture page-level `fetch` / `XMLHttpRequest` / basic WebSocket activity
- export a clean JSON + Markdown report after browser actions

This skill is packaged as **one workflow**. Internally it uses a local browser runtime, but the user-facing experience should be treated as one skill from start to finish.

## Use this skill for

- Debugging requests from a web page you are authorized to inspect
- Understanding login / registration / submit flows at the page level
- Seeing which APIs a button click or form submit triggers
- Capturing and summarizing `fetch` / `XMLHttpRequest` activity from the current page
- Producing a redacted request summary for later analysis

## Do not use this skill for

- Extracting or replaying third-party login sessions
- Capturing full system traffic
- Pulling access tokens, cookies, session secrets, or passwords for reuse
- Bypassing captchas, auth, or platform protections

## About the capture model

This skill provides **browser-side request capture**, not raw packet sniffing.

It is designed to help with:

- page request inspection
- form submission debugging
- login / registration flow analysis
- browser API tracing around user actions

It can observe:

- page-level `fetch`
- page-level `XMLHttpRequest`
- basic WebSocket lifecycle + message events

It does **not** try to replace system/network tools such as:

- Wireshark
- mitmproxy
- Fiddler

It also does not inspect arbitrary native processes or full machine traffic.

In short: this skill is best described as a **browser debugging capture and reporting tool**.

## Runtime expectation

- This skill expects a local `agent-browser` CLI runtime to be installed on the machine.
- The helper script `scripts/capture-session.js` auto-detects the local binary and drives the browser runtime for you.
- If `agent-browser` is missing, install it first before using this skill.

## Workflow

1. Open the target page with the browser runtime managed by this skill.
2. Inject the network collector into the page:

```powershell
$collector = Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\browser-network-inspector\scripts\collect-network.js" -Raw
agent-browser eval $collector
```

3. Optional: configure include/exclude host filters before the flow:

```powershell
agent-browser eval "window.__bniSetConfig({ includeHosts: ['example.com'], excludeHosts: ['ads.example.com'], captureWebSocket: true })"
```

4. Perform the desired browser actions (open, click, fill, submit, wait).
5. Read back the captured records:

```powershell
agent-browser eval "JSON.stringify(window.__bniExport ? window.__bniExport() : [])"
```

6. Save the JSON output to a local file.
7. Run the summarizer:

```powershell
node "$env:USERPROFILE\.openclaw\workspace\skills\browser-network-inspector\scripts\summarize-network.js" <input.json> [output.md]
```

8. Or use the bundled one-shot helper after you finish the browser actions:

```bash
node "$env:USERPROFILE/.openclaw/workspace/skills/browser-network-inspector/scripts/capture-session.js" --json-out ".capture/session.json" --md-out ".capture/session.md" --include-hosts "example.com,api.example.com"
```

## v2 additions

- Host include/exclude filtering
- Basic WebSocket event logging
- One-shot export helper: `scripts/capture-session.js`
- Improved summary report with source breakdown

## Polished workflow helpers

Additional JS-only helpers included:

- `scripts/clear-session.js` — clear the in-page capture buffer
- `scripts/capture-and-report.js` — create a timestamped report directory and save both JSON + Markdown
- Export helpers sanitize non-JSON wrapper output before writing capture files

Example:

```bash
node "$env:USERPROFILE/.openclaw/workspace/skills/browser-network-inspector/scripts/clear-session.js"
node "$env:USERPROFILE/.openclaw/workspace/skills/browser-network-inspector/scripts/capture-and-report.js" --include-hosts "example.com,api.example.com" --label login-flow --open-report
```

## Notes

- This captures **page-level JS network activity**. It is not a full packet sniffer.
- `fetch` and `XMLHttpRequest` are supported in v1.
- v2 adds basic WebSocket event logging and a Node.js export helper.
- Request and response bodies are truncated and redacted before export.
- If a site uses service workers, native browser internals, or non-page network paths, results may be incomplete.
- Keep helper scripts in JavaScript or Python only for this environment.
- The bundled export helper is Node.js-based, auto-detects the local browser runtime executable, and injects the collector in chunks to avoid Windows command-length limits.

## Redaction defaults

The collector and summarizer should redact or suppress obvious sensitive values such as:

- `authorization`
- `cookie`
- `set-cookie`
- `password`
- `token`
- `accessToken`
- `refreshToken`
- `session`
- `csrf`

## Output expectation

The summary should tell you:

- how many requests were captured
- which endpoints were hit
- which requests failed
- rough timing and status distribution
- likely key requests in the user flow

If the user wants raw logs, save them locally first and avoid echoing full sensitive payloads into chat.
