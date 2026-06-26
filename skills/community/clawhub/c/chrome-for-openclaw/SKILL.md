---
name: chrome-for-openclaw
description: Browser automation CLI for AI agents using Google Chrome via CDP. Connects to a running Chrome instance started by chrome_for_openclaw.sh inside an XRDP session. Use when the user needs to interact with websites using their existing login sessions, navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, or automating browser tasks.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
metadata: {"clawdbot":{"emoji":"🌐","requires":{"commands":["agent-browser"]},"homepage":"https://github.com/joustonhuang/chrome_for_openclaw"}}
---

# Chrome Browser Skill (CDP Mode)

> **Read first**: Complete setup guide, Chrome launcher script, and all reference docs at
> **https://github.com/joustonhuang/chrome_for_openclaw**

Browser automation via `agent-browser` connected to a real, running **Google Chrome** instance
over CDP. All commands connect to Chrome at `localhost:9222` — no separate Chromium download needed.
Your existing Chrome login sessions (Gmail, GitHub, etc.) are immediately available.

> **Also install this skill in OpenClaw:**
> [openclaw-agent-browser-clawdbot](https://clawhub.ai/hsyhph/openclaw-agent-browser-clawdbot)
> — the original `agent-browser` skill that this one is based on and compatible with.

## Prerequisites

Everything is handled by a single script: `chrome_for_openclaw.sh`.

### Step 1 — One-time system setup (run once, requires sudo)

Installs Google Chrome if missing, then configures XRDP + XFCE.
OpenClaw can run this step itself:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh) --install
```

Other options:

```bash
# Reinstall everything from scratch
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh) --reinstall

# Undo all changes made by --install
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh) --uninstall
```

After `--install` completes, **log out and reconnect via RDP** to get a fresh XFCE session.

### Step 2 — Start Chrome (run when Chrome is not already running)

Launch Chrome in CDP debug mode. Only needed if Chrome is not already open.
OpenClaw can run this step itself:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh)
```

Optional environment variable overrides:

```bash
DEBUG_PORT=9222 START_URL=https://gmail.com \
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh)
```

This kills any existing Chrome processes, starts Google Chrome with
`--remote-debugging-port=9222`, and waits for the CDP endpoint to respond.

### Step 3 — Install agent-browser

> **WARNING:** Do NOT install `agent-browser` by cloning or building from the GitHub repo
> ([https://github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)).
> Doing so is known to **break XRDP on Debian/Ubuntu**.
> Install via npm only:

```bash
npm install -g agent-browser
# Do NOT run `agent-browser install` — we connect to Chrome via CDP, no Chromium needed.
```

---

## CDP Connection

Every command uses `--cdp 9222` to connect to the running Chrome:

```bash
agent-browser --cdp 9222 <command>
```

To avoid repeating it, export once for the session:

```bash
export AGENT_BROWSER_CDP_URL=http://127.0.0.1:9222
agent-browser <command>   # automatically connects to Chrome
```

Auto-discovery also works if you are unsure of the port:

```bash
agent-browser --auto-connect <command>
```

---

## Core Workflow

Every browser automation follows this pattern:

1. **Navigate**: `agent-browser --cdp 9222 open <url>`
2. **Snapshot**: `agent-browser --cdp 9222 snapshot -i` (get element refs like `@e1`, `@e2`)
3. **Interact**: Use refs to click, fill, select
4. **Re-snapshot**: After navigation or DOM changes, get fresh refs

```bash
export AGENT_BROWSER_CDP_URL=http://127.0.0.1:9222

agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait 2000
agent-browser snapshot -i  # Check result
```

## Command Chaining

Commands can be chained with `&&`. The browser persists between commands via a background daemon.

```bash
agent-browser --cdp 9222 open https://example.com && agent-browser --cdp 9222 snapshot -i
agent-browser --cdp 9222 fill @e1 "user@example.com" && agent-browser --cdp 9222 fill @e2 "password123" && agent-browser --cdp 9222 click @e3
```

**When to chain:** Use `&&` when you don't need to read intermediate output before proceeding.
Run commands separately when you need to parse snapshot output to discover refs first.

## Handling Authentication

Because Chrome is already running with your login sessions, **you are already authenticated**
on sites you have previously logged into. No login flow needed in most cases.

**Option 1: Use the existing Chrome session (default — zero setup)**

```bash
# Chrome already has your Gmail/GitHub/etc. cookies — just open and automate
agent-browser --cdp 9222 open https://mail.google.com/mail/u/0/#inbox
agent-browser --cdp 9222 snapshot -i
```

**Option 2: Save session state for use outside CDP**

```bash
# Export auth from the running Chrome
agent-browser --cdp 9222 state save ./auth.json
# Use it later in a standalone agent-browser session
agent-browser --state ./auth.json open https://app.example.com/dashboard
```

**Option 3: Chrome profile reuse**

```bash
agent-browser --cdp 9222 profiles  # List profiles in the running Chrome
```

**Option 4: Auth vault (for recurring credentials)**

```bash
echo "$PASSWORD" | agent-browser auth save myapp --url https://app.example.com/login --username user --password-stdin
agent-browser --cdp 9222 auth login myapp
```

See [references/authentication.md](references/authentication.md) for OAuth, 2FA, and cookie patterns.

## Essential Commands

```bash
# Batch: ALWAYS use batch for 2+ sequential commands
agent-browser --cdp 9222 batch "open https://example.com" "snapshot -i"
agent-browser --cdp 9222 batch "open https://example.com" "screenshot"
agent-browser --cdp 9222 batch "click @e1" "wait 1000" "screenshot"

# Navigation
agent-browser --cdp 9222 open <url>              # Navigate (aliases: goto, navigate)
agent-browser --cdp 9222 close                   # Close browser
agent-browser --cdp 9222 close --all             # Close all active sessions

# Snapshot
agent-browser --cdp 9222 snapshot -i             # Interactive elements with refs (recommended)
agent-browser --cdp 9222 snapshot -i --urls      # Include href URLs for links
agent-browser --cdp 9222 snapshot -s "#selector" # Scope to CSS selector

# Interaction (use @refs from snapshot)
agent-browser --cdp 9222 click @e1               # Click element
agent-browser --cdp 9222 click @e1 --new-tab     # Click and open in new tab
agent-browser --cdp 9222 fill @e2 "text"         # Clear and type text
agent-browser --cdp 9222 type @e2 "text"         # Type without clearing
agent-browser --cdp 9222 select @e1 "option"     # Select dropdown option
agent-browser --cdp 9222 check @e1               # Check checkbox
agent-browser --cdp 9222 press Enter             # Press key
agent-browser --cdp 9222 keyboard type "text"    # Type at current focus (no selector)
agent-browser --cdp 9222 scroll down 500         # Scroll page

# Get information
agent-browser --cdp 9222 get text @e1            # Get element text
agent-browser --cdp 9222 get url                 # Get current URL
agent-browser --cdp 9222 get title               # Get page title
agent-browser --cdp 9222 get cdp-url             # Get CDP WebSocket URL

# Wait
agent-browser --cdp 9222 wait @e1                # Wait for element
agent-browser --cdp 9222 wait 2000               # Wait milliseconds
agent-browser --cdp 9222 wait --url "**/page"    # Wait for URL pattern
agent-browser --cdp 9222 wait --text "Welcome"   # Wait for text to appear
agent-browser --cdp 9222 wait --fn "!document.body.innerText.includes('Loading...')"

# Downloads
agent-browser --cdp 9222 download @e1 ./file.pdf
agent-browser --cdp 9222 wait --download ./output.zip

# Tab management
agent-browser --cdp 9222 tab list
agent-browser --cdp 9222 tab new https://example.com
agent-browser --cdp 9222 tab 2
agent-browser --cdp 9222 tab close

# Network
agent-browser --cdp 9222 network requests
agent-browser --cdp 9222 network requests --type xhr,fetch
agent-browser --cdp 9222 network route "**/ads/*" --abort

# Capture
agent-browser --cdp 9222 screenshot
agent-browser --cdp 9222 screenshot --full
agent-browser --cdp 9222 screenshot --annotate
agent-browser --cdp 9222 pdf output.pdf
```

## Batch Execution

ALWAYS use `batch` when running 2+ commands in sequence:

```bash
# Navigate and snapshot
agent-browser --cdp 9222 batch "open https://example.com" "snapshot -i"

# Navigate, snapshot, and screenshot
agent-browser --cdp 9222 batch "open https://example.com" "snapshot -i" "screenshot"

# Click, wait, screenshot
agent-browser --cdp 9222 batch "click @e1" "wait 1000" "screenshot"

# With --bail to stop on first error
agent-browser --cdp 9222 batch --bail "open https://example.com" "click @e1" "screenshot"
```

Only use a single command (not batch) when you need to read the output before deciding the next
step — e.g., after `snapshot -i` to discover refs. After reading, batch the remaining steps.

## Efficiency Strategies

**Use `--urls` to avoid re-navigation.** Get all href URLs from one snapshot, then `open` each
directly instead of clicking refs and navigating back.

**Snapshot once, act many times.** Extract all refs from a single snapshot, then batch actions.

**Multi-page workflow:**

```bash
# 1. Get all URLs in one call
agent-browser --cdp 9222 batch "open https://news.ycombinator.com" "snapshot -i --urls"
# Read output to extract URLs, then visit each directly:
agent-browser --cdp 9222 batch "open https://github.com/example/repo" "screenshot"
agent-browser --cdp 9222 batch "open https://example.com/article" "screenshot"
```

## Common Patterns

### Form Submission

```bash
agent-browser --cdp 9222 batch "open https://example.com/signup" "snapshot -i"
# Read snapshot to identify form refs, then fill and submit
agent-browser --cdp 9222 batch "fill @e1 \"Jane Doe\"" "fill @e2 \"jane@example.com\"" "click @e3" "wait 2000"
```

### Gmail Workflow (already logged in via Chrome)

```bash
export AGENT_BROWSER_CDP_URL=http://127.0.0.1:9222

agent-browser batch "open https://mail.google.com/mail/u/0/#inbox" "wait 2000" "snapshot -i"
# Agent identifies Compose button ref @e4
agent-browser batch "click @e4" "wait 1000" "snapshot -i"
# Agent fills To/Subject/Body
agent-browser batch \
  "fill @e5 \"recipient@example.com\"" \
  "fill @e6 \"Subject\"" \
  "fill @e7 \"Body text\"" \
  "click @e8"
```

### Save Auth State from Running Chrome

```bash
# Export your current Chrome login cookies for later reuse
agent-browser --cdp 9222 state save ./auth.json
# Reuse without CDP (standalone session)
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard
```

### Working with Iframes

Iframe content is automatically inlined in snapshots. Refs inside iframes work directly.

```bash
agent-browser --cdp 9222 batch "open https://example.com/checkout" "snapshot -i"
# @e2 [Iframe] "payment-frame"
#   @e3 [input] "Card number"
#   @e4 [button] "Pay"
agent-browser --cdp 9222 batch "fill @e3 \"4111111111111111\"" "click @e4"
```

### Parallel Sessions

```bash
agent-browser --cdp 9222 --session site1 open https://site-a.com
agent-browser --cdp 9222 --session site2 open https://site-b.com

agent-browser --cdp 9222 --session site1 snapshot -i
agent-browser --cdp 9222 --session site2 snapshot -i

agent-browser --cdp 9222 session list
```

## Annotated Screenshots (Vision Mode)

```bash
agent-browser --cdp 9222 screenshot --annotate
# Output: image path + legend:
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
agent-browser --cdp 9222 click @e2
```

## Semantic Locators (Alternative to Refs)

```bash
agent-browser --cdp 9222 find text "Sign In" click
agent-browser --cdp 9222 find label "Email" fill "user@test.com"
agent-browser --cdp 9222 find role button click --name "Submit"
agent-browser --cdp 9222 find placeholder "Search" type "query"
agent-browser --cdp 9222 find testid "submit-btn" click
```

## JavaScript Evaluation

```bash
agent-browser --cdp 9222 eval 'document.title'

# Complex JS — use --stdin to avoid shell escaping issues
agent-browser --cdp 9222 eval --stdin <<'EVALEOF'
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => a.href))
EVALEOF
```

## Streaming

```bash
agent-browser --cdp 9222 stream enable           # Start WebSocket stream
agent-browser --cdp 9222 stream enable --port 9223
agent-browser --cdp 9222 stream status
agent-browser --cdp 9222 stream disable
```

## Timeouts and Slow Pages

Default timeout: 25 seconds. Override with `AGENT_BROWSER_DEFAULT_TIMEOUT` (milliseconds).

`open` already waits for the page `load` event. Only add explicit waits for async content.

```bash
agent-browser --cdp 9222 wait "#content"        # Wait for element (preferred)
agent-browser --cdp 9222 wait 2000              # Fixed duration for slow SPAs
agent-browser --cdp 9222 wait --url "**/dashboard"
agent-browser --cdp 9222 wait --text "Results loaded"
```

**Avoid `wait --load networkidle`** — ad-heavy or websocket sites will hang. Use `wait 2000`
or `wait <selector>` instead.

## Session Cleanup

```bash
agent-browser --cdp 9222 close --all            # Close all sessions
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser --cdp 9222 open example.com
```

## Security

```bash
# Wrap page content to protect against prompt injection
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser --cdp 9222 snapshot

# Restrict navigation to trusted domains
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"

# Gate destructive actions via policy file
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

## Observability Dashboard

```bash
agent-browser --cdp 9222 dashboard start   # Start live dashboard on port 4848
agent-browser --cdp 9222 dashboard stop
```

## Ref Lifecycle (Important)

Refs (`@e1`, `@e2`, …) are invalidated when the page changes. Always re-snapshot after:
- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals)

```bash
agent-browser --cdp 9222 click @e5       # Navigates
agent-browser --cdp 9222 snapshot -i     # MUST re-snapshot
agent-browser --cdp 9222 click @e1       # Use new refs
```

## Installation Summary

```bash
# Step 1: One-time system setup (Chrome + XRDP + XFCE, requires sudo)
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh) --install
# → Log out and reconnect via RDP after this completes

# Step 2: Launch Chrome in CDP debug mode (only if not already running)
bash <(curl -fsSL https://raw.githubusercontent.com/joustonhuang/chrome_for_openclaw/main/chrome_for_openclaw.sh)

# Step 3: Install agent-browser via npm ONLY
# WARNING: Do NOT clone/build from https://github.com/vercel-labs/agent-browser
#          — it breaks XRDP on Debian/Ubuntu. Use npm only:
npm install -g agent-browser

# Step 4: Connect and automate
export AGENT_BROWSER_CDP_URL=http://127.0.0.1:9222
agent-browser batch "open https://example.com" "snapshot -i"
```

## Deep-Dive Reference Docs

| Reference | When to Use |
|---|---|
| [references/commands.md](references/commands.md) | Full command reference with all options |
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref lifecycle, invalidation, troubleshooting |
| [references/session-management.md](references/session-management.md) | Parallel sessions, state persistence |
| [references/authentication.md](references/authentication.md) | Login flows, OAuth, 2FA, state reuse |
| [references/video-recording.md](references/video-recording.md) | Recording workflows for debugging |
| [references/profiling.md](references/profiling.md) | Chrome DevTools performance profiling |
| [references/proxy-support.md](references/proxy-support.md) | Proxy configuration, geo-testing |

---

## Credits

Chrome launcher script: [joustonhuang/chrome_for_openclaw](https://github.com/joustonhuang/chrome_for_openclaw)

agent-browser CLI: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) (Apache 2.0)
