# Agent Browser — Full Command Reference

## Navigation
```bash
agent-browser open <url>
agent-browser back | forward | reload | close
```

## Snapshot
```bash
agent-browser snapshot -i --json          # Interactive elements, JSON output
agent-browser snapshot -i -c -d 5 --json  # Compact, depth limit
agent-browser snapshot -s "#main" -i      # Scope to CSS selector
```

## Interactions (Ref-based)
```bash
agent-browser click @e1
agent-browser dblclick @e1
agent-browser fill @e2 "text"       # Clear + type
agent-browser type @e2 "text"       # Type without clearing
agent-browser hover @e3
agent-browser check @e4 | uncheck @e4
agent-browser select @e5 "value"
agent-browser press Enter | "Control+a"
agent-browser scroll down 500
agent-browser drag @e6 @e7
agent-browser upload @e8 file.pdf
agent-browser scrollintoview @e1
```

## Get Information
```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
agent-browser get box @e1 --json
```

## Check State
```bash
agent-browser is visible @e1 --json
agent-browser is enabled @e2 --json
agent-browser is checked @e3 --json
```

## Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait ms
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "**/dashboard"    # Wait for URL pattern
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --fn "window.ready"     # Wait for JS condition
```

## Sessions (Parallel Browsers)
```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
# Or via env: AGENT_BROWSER_SESSION=admin agent-browser ...
```

## State Persistence
```bash
agent-browser state save auth.json
agent-browser state load auth.json
```

## Screenshots & PDFs
```bash
agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf
```

## Video Recording
```bash
agent-browser record start ./demo.webm
agent-browser record stop
agent-browser record restart ./take2.webm
# Tip: Explore first, then record for smooth demos
```

## Mouse Control
```bash
agent-browser mouse move 100 200
agent-browser mouse down left | up left
agent-browser mouse wheel 100
```

## Semantic Locators (alternative to refs)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

## Browser Settings
```bash
agent-browser set viewport 1920 1080
agent-browser set device "iPhone 14"
agent-browser set geo 37.7749 -122.4194
agent-browser set offline on
agent-browser set headers '{"X-Key":"v"}'
agent-browser set credentials user pass
agent-browser set media dark
```

## Dialogs
```bash
agent-browser dialog accept [text]
agent-browser dialog dismiss
```

## JavaScript
```bash
agent-browser eval "document.title"
```

## Network Control
```bash
agent-browser network route "**/ads/*" --abort
agent-browser network route "**/api/*" --body '{"x":1}'
agent-browser network requests --filter api
agent-browser network unroute [url]
```

## Cookies & Storage
```bash
agent-browser cookies
agent-browser cookies set name value
agent-browser cookies clear
agent-browser storage local key
agent-browser storage local set key val
agent-browser storage local clear
```

## Tabs & Frames
```bash
agent-browser tab | tab new [url] | tab 2 | tab close
agent-browser window new
agent-browser frame "#iframe" | frame main
```

## Debugging
```bash
agent-browser open example.com --headed   # Show browser window
agent-browser console | console --clear
agent-browser errors | errors --clear
agent-browser highlight @e1
agent-browser trace start | trace stop trace.zip
agent-browser --cdp 9222 snapshot
```

## JSON Output
Add `--json` to any command for machine-readable output.

## Options
- `--session <name>` — isolated session
- `--json` — JSON output
- `--full` — full page screenshot
- `--headed` — show browser window
- `--timeout <ms>` — command timeout
- `--cdp <port>` — connect via CDP
