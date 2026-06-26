---
name: chrome-devtools-remote
description: Drive a remote chrome-devtools-mcp server (typically on a tailnet) over HTTPS using the chrome-devtools CLI. Use this when the user wants to navigate, screenshot, inspect, or evaluate JavaScript on a browser running on another host (e.g. a Tailscale-connected Mac mini or a CI runner) — and you don't have a local Chrome to control. Examples of triggers ("open <url> on the lab mac", "take a screenshot of the browser on host X", "evaluate this on the remote browser").
---

# chrome-devtools-remote

You are operating the `chrome-devtools` CLI in **remote** mode against a `chrome-devtools-mcp` server that the user has running on another host. The remote server owns the browser; your job is to drive it.

## When to use this skill

Trigger on any request that:

- Names a remote machine ("on the lab mac", "on host X", "on my tailnet box") and asks you to do something a browser would do
- Provides a `chrome-devtools-mcp` HTTPS URL (typically ending in `/mcp`) and asks for an interactive browser action
- Mentions environment variables `CHROME_DEVTOOLS_MCP_REMOTE_URL` or `CHROME_DEVTOOLS_MCP_REMOTE_INSECURE`

If the user wants to drive a **local** browser, use the regular `chrome-devtools` CLI (without `--remote`) or the `mcp__chrome-devtools__*` MCP tools instead.

## Install (on the local box, once)

The `chrome-devtools` client CLI ships in the same npm package as the server. Install globally on the machine where the agent runs — **not** on the remote host:

```bash
npm install -g @vibebrowser/chrome-devtools-mcp
chrome-devtools --version   # should print 0.26.6 or newer
```

You do not install anything on the remote host — that host is whoever already serves `https://.../mcp` and is set up out-of-band.

Troubleshooting:

- `command not found: chrome-devtools` — npm's global bin isn't on `PATH`. Add `$(npm config get prefix)/bin` to `PATH`, or on macOS Homebrew add `eval "$(brew shellenv)"` to your shell rc.
- `Cannot find package 'pkce-challenge'` on first run — known bundling gap (issue dzianisv/chrome-devtools-mcp#17). Workaround: `cd "$(npm root -g)/@vibebrowser/chrome-devtools-mcp" && npm install pkce-challenge --no-save`.

## Connect

Configure the endpoint **once per shell session** and verify connectivity before doing anything else.

```bash
export CHROME_DEVTOOLS_MCP_REMOTE_URL="https://lab.tailnet.ts.net/mcp"
chrome-devtools status --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"
```

A healthy response prints `status=ok http=200` plus a JSON body. Anything else is a hard stop — surface the error to the user instead of retrying.

If the URL is unset, ask the user once for the endpoint. Conventional shape: `https://<host>/mcp` (the `/mcp` path is required — the bare host returns a 404).

Connection-time flags:

| Situation                                                               | What to pass                                                                                        |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Self-signed cert (common on tailnets without Tailscale-issued certs)    | `--insecure` on every call, or `export CHROME_DEVTOOLS_MCP_REMOTE_INSECURE=1`                       |
| Bearer-token gateway                                                    | `--header "Authorization: Bearer $TOKEN"` — repeatable, **not** cached, must be on every invocation |
| Custom static header (e.g. `X-Tenant: foo`)                             | `--header "X-Tenant: foo"`                                                                          |
| Endpoint behind Tailscale and `status` returns `Failed to reach remote` | `tailscale status` locally; the box is offline or the URL has the wrong hostname                    |

Once `status` is green, every subsequent `chrome-devtools <tool> ... --remote "$URL"` call reuses the same server-side tab via a sticky session id cached at `~/.cache/chrome-devtools-mcp/remote/<hash>.session`.

## Session model — read this before chaining commands

Each CLI invocation reuses a sticky session id stored under `~/.cache/chrome-devtools-mcp/remote/<hash>.session`. This means:

- `navigate_page` → `take_snapshot` → `click` → `take_screenshot` all hit the **same** server-side tab. You can chain them as separate CLI calls and assume continuity.
- If the server restarts between calls, the next call transparently re-initializes against a fresh session. **Tab state on the server is lost** — re-navigate before assuming anything.
- To explicitly end the server-side session and free its browser context, run `chrome-devtools stop --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"`.

## Common operations

All commands accept `--output-format json` to return structured output you can pipe into `jq`.

```bash
# Open a page
chrome-devtools navigate_page "https://example.com" --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# Get a structured a11y snapshot (use for finding clickable uids)
chrome-devtools take_snapshot --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL" --output-format json

# Click an element by uid from the snapshot
chrome-devtools click "$UID" --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# Fill an input
chrome-devtools fill "$UID" "value" --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# Take a screenshot (saved to /tmp/<uuid>.png locally)
chrome-devtools take_screenshot --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# Evaluate JS in the page — return value must be JSON-serializable
chrome-devtools evaluate_script '() => document.title' --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# Read console messages from the page
chrome-devtools list_console_messages --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"

# List network requests since page load
chrome-devtools list_network_requests --remote "$CHROME_DEVTOOLS_MCP_REMOTE_URL"
```

## Recipes

### Smoke-check a deployed web app

```bash
URL="$CHROME_DEVTOOLS_MCP_REMOTE_URL"
chrome-devtools navigate_page "https://app.example.com" --remote "$URL"
chrome-devtools evaluate_script '() => ({title: document.title, ready: document.readyState})' --remote "$URL"
chrome-devtools list_console_messages --remote "$URL" --output-format json
chrome-devtools take_screenshot --remote "$URL"
```

If `console_messages` contains any `level: "error"` entries, surface them — they are usually the root cause of "the page looks broken" reports.

### Drive a login form

```bash
chrome-devtools navigate_page "https://app.example.com/login" --remote "$URL"
chrome-devtools take_snapshot --remote "$URL" --output-format json > /tmp/snap.json
# Find the uid of the email input + password input + submit button from /tmp/snap.json
chrome-devtools fill "<email-uid>" "$LOGIN_EMAIL" --remote "$URL"
chrome-devtools fill "<password-uid>" "$LOGIN_PASSWORD" --remote "$URL"
chrome-devtools click "<submit-uid>" --remote "$URL"
```

### Capture a CrUX-style trace

```bash
chrome-devtools performance_start_trace --remote "$URL"
chrome-devtools navigate_page "https://app.example.com" --remote "$URL"
chrome-devtools performance_stop_trace --remote "$URL" --output-format json
```

## Output discipline

- Always print the URL of the page you navigated to so the user knows which tab they're looking at.
- For screenshots, print the path of the saved file (`Saved to /tmp/<uuid>.png.`) — the CLI already writes that line on stdout.
- For `evaluate_script`, prefer `--output-format json` and forward only the relevant field instead of dumping the whole structuredContent envelope.
- If the user asks "what's on the page", prefer `take_snapshot` over `take_screenshot` — the snapshot is text and cheaper to reason over.

## Failure modes

| Symptom                                                                           | Cause                                                                                                          | Fix                                                                                     |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `Failed to reach remote`                                                          | DNS, Tailscale offline, or wrong URL                                                                           | `tailscale status` on the local box; verify `--remote` URL                              |
| `Streamable HTTP error: ... 404 Session not found`                                | Server restarted; sticky id was stale. Retried once internally — if you see this it means the retry also 404'd | `chrome-devtools stop --remote $URL` to wipe the sticky pointer, then retry the command |
| TLS verify error (`UNABLE_TO_VERIFY_LEAF_SIGNATURE`, `SELF_SIGNED_CERT_IN_CHAIN`) | Server uses a self-signed cert (no Tailscale-issued cert)                                                      | Add `--insecure` or `export CHROME_DEVTOOLS_MCP_REMOTE_INSECURE=1`                      |
| `Bad Request: Mcp-Session-Id header is required`                                  | Local cache directory was wiped mid-session                                                                    | First call after the wipe will mint a fresh session; just retry                         |
| Hangs on first call after a long idle                                             | Server idle reaper closed the session                                                                          | Same fix as the 404 row — `stop` then retry                                             |

## Don'ts

- Don't loop `navigate_page` to "wait for the page to load" — use `wait_for` with a text selector instead.
- Don't `take_screenshot` for every step in a chain — the user almost always wants one final screenshot, not five intermediate ones.
- Don't pass `--insecure` for a hosted endpoint with a real cert. It silently disables TLS for the whole CLI process.
- Don't try to `start` a server with `--remote` — that subcommand only manages local daemons.
