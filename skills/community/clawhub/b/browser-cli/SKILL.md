# browser-use CLI Skill

## What This Skill Covers
Use this skill any time you need to automate a browser from the command line using `browser-use`. This includes navigating pages, clicking/typing/filling forms, taking screenshots, running JavaScript, managing tabs, handling cookies, driving cloud browsers, and exposing local servers via tunnels.

---

## Installation

### Prerequisites
| Platform | Requirements |
|----------|-------------|
| macOS    | Python 3.11+ |
| Linux    | Python 3.11+ |
| Windows  | Git for Windows + Python 3.11+ |

### One-line Install (Recommended)
```bash
# macOS / Linux
curl -fsSL https://browser-use.com/cli/install.sh | bash

# Windows (PowerShell)
& "C:\Program Files\Git\bin\bash.exe" -c 'curl -fsSL https://browser-use.com/cli/install.sh | bash'
```

### Manual Install
```bash
uv pip install browser-use
browser-use install   # downloads Chromium
browser-use doctor    # validates setup
```

### Post-Install Health Check
```bash
browser-use doctor   # prints diagnostics + config
browser-use setup    # optional interactive wizard
```

---

## Core Mental Model

The workflow is always:
1. **Open** a page → `browser-use open <url>`
2. **Inspect** the page → `browser-use state` (returns numbered element indices)
3. **Interact** using those indices → `browser-use click 3`, `browser-use input 1 "text"`
4. **Repeat** — the daemon keeps the browser alive between commands (~50ms latency)

A background daemon process starts automatically on first command and stays alive until you `browser-use close`.

---

## Browser Modes

```bash
# Default: headless Chromium (invisible)
browser-use open https://example.com

# Visible window
browser-use --headed open https://example.com

# Use your real Chrome (preserves logins, cookies, extensions)
browser-use connect

# Use a specific Chrome profile
browser-use --profile "Default" open https://gmail.com

# Zero-config cloud browser (requires API key)
browser-use cloud connect

# Connect to existing browser via CDP
browser-use --cdp-url http://localhost:9222 open https://example.com
browser-use --cdp-url ws://localhost:9222/devtools/browser/... state
```

After `connect` or `cloud connect`, all subsequent commands automatically target that browser — no extra flags needed.

---

## All Commands

### Navigation
```bash
browser-use open <url>               # Navigate to URL
browser-use back                     # Go back in history
browser-use scroll down              # Scroll down
browser-use scroll up                # Scroll up
browser-use scroll down --amount 1000  # Scroll by pixel amount
```

### Inspection
```bash
browser-use state                    # Get URL, title, and numbered clickable elements
browser-use screenshot output.png    # Take screenshot to file
browser-use screenshot               # Screenshot as base64 (stdout)
browser-use screenshot --full page.png  # Full-page screenshot
```

### Interaction
```bash
browser-use click <index>            # Click element by index (from state)
browser-use click <x> <y>           # Click at pixel coordinates
browser-use type "text"              # Type into currently focused element
browser-use input <index> "text"     # Click element then type (most common for forms)
browser-use keys "Enter"             # Send keyboard key
browser-use keys "Control+a"         # Send key combination
browser-use select <index> "value"   # Select dropdown option
browser-use upload <index> /path/to/file  # Upload file to file input
browser-use hover <index>            # Hover over element
browser-use dblclick <index>         # Double-click element
browser-use rightclick <index>       # Right-click element
```

### Tabs
```bash
browser-use tab list                 # List all open tabs
browser-use tab new                  # Open blank tab
browser-use tab new https://url.com  # Open tab with URL
browser-use tab switch <index>       # Switch to tab by index
browser-use tab close                # Close current tab
browser-use tab close <index>        # Close specific tab
```

### Cookies
```bash
browser-use cookies get                        # Get all cookies
browser-use cookies get --url https://site.com # Get cookies for URL
browser-use cookies set name value             # Set a cookie
browser-use cookies set name val --domain .example.com --secure
browser-use cookies set name val --same-site Strict   # Strict | Lax | None
browser-use cookies set name val --expires 1735689600 # Unix timestamp
browser-use cookies clear                      # Clear all cookies
browser-use cookies clear --url https://site.com
browser-use cookies export cookies.json        # Export to JSON
browser-use cookies import cookies.json        # Import from JSON
```

### Waiting
```bash
browser-use wait selector ".btn"               # Wait for element to be visible
browser-use wait selector ".loading" --state hidden  # Wait for element to disappear
browser-use wait text "Success"                # Wait for text to appear on page
browser-use wait selector "h1" --timeout 5000 # Custom timeout in ms
```

### Get (Information Retrieval)
```bash
browser-use get title                  # Get page title
browser-use get html                   # Get full page HTML
browser-use get html --selector "main" # Get HTML of specific element
browser-use get text <index>           # Get text content of element
browser-use get value <index>          # Get value of input/textarea
browser-use get attributes <index>     # Get all element attributes
browser-use get bbox <index>           # Get bounding box (x, y, width, height)
```

### JavaScript
```bash
browser-use eval "document.title"
browser-use eval "Array.from(document.querySelectorAll('a')).map(a => a.href)"
browser-use eval "window.scrollTo(0, document.body.scrollHeight)"
```

### Python (Persistent Session)
```bash
browser-use python "x = 42"              # Set a variable
browser-use python "print(x)"            # Access variable (prints: 42)
browser-use python "print(browser.url)"  # Access browser object
browser-use python --vars                # Show all defined variables
browser-use python --reset               # Clear namespace
browser-use python --file script.py      # Run a Python file
```

---

## Session Management

Each `--session` gets its own daemon, socket, and browser instance.

```bash
# Default session (implicit)
browser-use open https://example.com
browser-use state

# Named sessions
browser-use --session work open https://example.com
browser-use --session personal open https://gmail.com
browser-use --session work state    # targets work browser

# List all active sessions
browser-use sessions

# Close a specific session
browser-use --session work close

# Close all sessions
browser-use close --all

# Via environment variable
BROWSER_USE_SESSION=work browser-use state
```

---

## Cloud API

### Auth
```bash
browser-use cloud login sk-abc123...    # Save API key
browser-use cloud logout                # Remove API key
# Or: export BROWSER_USE_API_KEY=sk-abc123...
```

### Cloud Browser
```bash
browser-use cloud connect              # Provision cloud browser and connect
browser-use state                      # Works normally after connect
browser-use close                      # Disconnect AND stop cloud browser
browser-use cloud close                # Also stops cloud browser
```

### REST Passthrough
```bash
browser-use cloud v2 GET /browsers
browser-use cloud v2 POST /tasks '{"task":"Search for AI news","url":"https://google.com"}'
browser-use cloud v2 poll <task-id>    # Poll until task completes
browser-use cloud v3 POST /path '{"key":"value"}'
browser-use cloud v2 --help            # Show all v2 API endpoints
browser-use cloud v3 --help            # Show all v3 API endpoints
```

---

## Tunnels (Expose Local Server to Cloud Browser)

```bash
browser-use tunnel 3000                # Expose localhost:3000 → public HTTPS URL
browser-use tunnel list                # List active tunnels
browser-use tunnel stop 3000           # Stop tunnel for port
browser-use tunnel stop --all          # Stop all tunnels

# Typical flow for testing local app with a cloud browser:
npm run dev &
browser-use tunnel 3000                # → https://abc.trycloudflare.com
browser-use cloud connect
browser-use open https://abc.trycloudflare.com
```

---

## Profile Management (Sync Chrome Cookies to Cloud)

```bash
browser-use profile                    # Interactive sync wizard
browser-use profile list               # List detected browsers + profiles
browser-use profile sync --all         # Sync all profiles to cloud
browser-use profile sync --browser "Google Chrome" --profile "Default"
browser-use profile auth --apikey <key>
browser-use profile inspect --browser "Google Chrome" --profile "Default"
browser-use profile update             # Update the profile-use binary
```

---

## Global Options

| Flag | Description |
|------|-------------|
| `--headed` | Show browser window |
| `--profile [NAME]` | Use real Chrome profile (bare flag = "Default") |
| `--connect` | Auto-discover running Chrome via CDP |
| `--cdp-url <url>` | Connect to existing browser via CDP URL |
| `--session NAME` | Target named session (default: "default") |
| `--json` | Output as JSON |
| `--mcp` | Run as MCP server via stdin/stdout |

---

## Configuration

```bash
browser-use config list                              # Show all config
browser-use config set cloud_connect_proxy jp        # Set a value
browser-use config get cloud_connect_proxy           # Get a value
browser-use config unset cloud_connect_timeout       # Remove a value
```

Config file: `~/.browser-use/config.json`

---

## Template Generation

```bash
browser-use init                          # Interactive template picker
browser-use init --list                   # List all templates
browser-use init --template basic         # Generate specific template
browser-use init --output my_script.py    # Specify output filename
browser-use init --force                  # Overwrite existing files
```

---

## File Layout

```
~/.browser-use/
├── config.json          # API key + settings
├── bin/
│   └── profile-use      # Managed Go binary (auto-downloaded)
├── tunnels/
│   ├── {port}.json      # Tunnel metadata
│   └── {port}.log       # Tunnel logs
├── default.state.json   # Daemon lifecycle state
├── default.sock         # Daemon socket (ephemeral)
├── default.pid          # Daemon PID (ephemeral)
└── cli.log              # Daemon log
```

Override the base dir with `BROWSER_USE_HOME`.

---

## Common Recipes

### Fill and Submit a Form
```bash
browser-use open https://example.com/contact
browser-use state
# Output: [0] input "Name", [1] input "Email", [2] button "Submit"
browser-use input 0 "John Doe"
browser-use input 1 "john@example.com"
browser-use click 2
browser-use wait text "Thank you"
```

### Scrape Data with JavaScript
```bash
browser-use open https://news.ycombinator.com
browser-use eval "Array.from(document.querySelectorAll('.titleline a')).slice(0,5).map(a => a.textContent)"
```

### Multi-step Python Automation
```bash
browser-use open https://example.com
browser-use python "
for i in range(5):
    browser.scroll('down')
    browser.wait(0.5)
browser.screenshot('scrolled.png')
"
```

### Login with Saved Chrome Profile
```bash
browser-use --profile "Default" open https://gmail.com
browser-use state
# Gmail inbox loads already logged in
```

### Run Two Browsers in Parallel
```bash
browser-use --session a open https://site-a.com
browser-use --session b open https://site-b.com
browser-use --session a state
browser-use --session b state
browser-use close --all
```

### Test Local App via Cloud Browser
```bash
npm run dev &
browser-use tunnel 3000
# Copy the printed public URL, e.g. https://xyz.trycloudflare.com
browser-use cloud connect
browser-use open https://xyz.trycloudflare.com
browser-use screenshot check.png
```

---

## Windows Troubleshooting

**ARM64 Windows** — install x64 Python for emulation:
```powershell
winget install Python.Python.3.11 --architecture x64
```

**Multiple Python versions** — pin the version:
```powershell
$env:PY_PYTHON=3.11
```

**PATH not updated** — restart terminal, or run via Git Bash:
```powershell
& "C:\Program Files\Git\bin\bash.exe" -c 'browser-use --help'
```

**Daemon won't start** — kill stale processes:
```powershell
wmic process where "name='python.exe' and commandline like '%browser%use%'" get processid
taskkill /PID <pid> /F
```

**Stale venv** — nuke and reinstall:
```powershell
wmic process where "name='python.exe' and commandline like '%browser%use%'" call terminate
Remove-Item -Recurse -Force "$env:USERPROFILE\.browser-use-env"
# Re-run the installer
```

---

## Quick Reference Card

| Goal | Command |
|------|---------|
| Start + navigate | `browser-use open <url>` |
| See elements | `browser-use state` |
| Click element | `browser-use click <index>` |
| Fill input | `browser-use input <index> "text"` |
| Press key | `browser-use keys "Enter"` |
| Screenshot | `browser-use screenshot out.png` |
| Run JS | `browser-use eval "js here"` |
| Wait for element | `browser-use wait selector ".cls"` |
| Get page HTML | `browser-use get html` |
| Close browser | `browser-use close` |
| Use real Chrome | `browser-use connect` |
| Cloud browser | `browser-use cloud connect` |
| Named session | `browser-use --session NAME <cmd>` |
| Show config | `browser-use doctor` |
