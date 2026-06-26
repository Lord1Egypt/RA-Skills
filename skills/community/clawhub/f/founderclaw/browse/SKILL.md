---
name: browse
description: >
  Fast headless browser for QA testing and site dogfooding. Navigate pages,
  interact with elements, verify state, diff before/after, take screenshots,
  test responsive layouts, forms, uploads, dialogs, and assert element states.
  ~100ms per command after initial startup.
  Use when: "open in browser", "test the site", "take a screenshot",
  "dogfood this", "check this page", "QA test", "verify deployment".
---

# Browse — Headless Browser for QA

Persistent headless Chromium. First call auto-starts (~3s), then ~100-200ms per command.
State persists between calls (cookies, tabs, sessions).

## Requirements

- **Bun** v1.0+ (required to build binary)
- **Playwright Chromium** (installed automatically on first setup)
- Container environments: set `CONTAINER=1` env var (auto-sandbox workaround)

## First-Time Setup

```bash
cd founderclaw/browse
bun install                        # install dependencies
bun build src/cli.ts --compile --outfile dist/browse  # build binary
CONTAINER=1 dist/browse goto "https://example.com"    # test it works
```

On first run, Playwright downloads Chromium (~150MB). Subsequent runs are instant.

## Usage

All commands via Bash: `CONTAINER=1 /path/to/browse <command>`

### Navigation
```bash
CONTAINER=1 $BROWSE goto https://yourapp.com
CONTAINER=1 $BROWSE back
CONTAINER=1 $BROWSE reload
CONTAINER=1 $BROWSE url              # print current URL
```

### Content
```bash
CONTAINER=1 $BROWSE text             # readable text on page
CONTAINER=1 $BROWSE html             # full HTML
CONTAINER=1 $BROWSE links            # all links
CONTAINER=1 $BROWSE forms            # all forms
```

### Interaction
```bash
CONTAINER=1 $BROWSE click @e3        # click element by ref
CONTAINER=1 $BROWSE fill @e4 "text"  # fill input
CONTAINER=1 $BROWSE select @e5 "option"
CONTAINER=1 $BROWSE hover @e6
CONTAINER=1 $BROWSE type "hello"
CONTAINER=1 $BROWSE press Enter
CONTAINER=1 $BROWSE scroll "#section"
CONTAINER=1 $BROWSE upload @input file1.txt
```

### Inspection
```bash
CONTAINER=1 $BROWSE js "document.title"
CONTAINER=1 $BROWSE console          # JS console errors
CONTAINER=1 $BROWSE network          # failed requests
CONTAINER=1 $BROWSE is visible ".modal"
CONTAINER=1 $BROWSE is enabled "#submit"
CONTAINER=1 $BROWSE cookies
```

### Visual
```bash
CONTAINER=1 $BROWSE screenshot /tmp/page.png
CONTAINER=1 $BROWSE screenshot "#hero" /tmp/hero.png
CONTAINER=1 $BROWSE responsive /tmp/layout    # mobile/tablet/desktop
CONTAINER=1 $BROWSE pdf /tmp/page.pdf
```

### Snapshot (structured page analysis)
```bash
CONTAINER=1 $BROWSE snapshot -i              # interactive elements only
CONTAINER=1 $BROWSE snapshot -i -a -o /tmp/annotated.png  # annotated screenshot
CONTAINER=1 $BROWSE snapshot -D              # diff vs previous snapshot
CONTAINER=1 $BROWSE snapshot -C              # all clickable elements
```

### Session
```bash
CONTAINER=1 $BROWSE wait ".loaded"           # wait for selector
CONTAINER=1 $BROWSE wait --networkidle       # wait for network idle
CONTAINER=1 $BROWSE viewport 375x812         # set viewport size
```

## QA Workflows

### Test a user flow
```bash
CONTAINER=1 $BROWSE goto https://app.example.com/login
CONTAINER=1 $BROWSE snapshot -i
CONTAINER=1 $BROWSE fill @e3 "$TEST_EMAIL"
CONTAINER=1 $BROWSE fill @e4 "$TEST_PASSWORD"
CONTAINER=1 $BROWSE click @e5
CONTAINER=1 $BROWSE snapshot -D              # diff shows what changed
CONTAINER=1 $BROWSE is visible ".dashboard"
CONTAINER=1 $BROWSE screenshot /tmp/after-login.png
```

### Verify a deployment
```bash
CONTAINER=1 $BROWSE goto https://yourapp.com
CONTAINER=1 $BROWSE text
CONTAINER=1 $BROWSE console
CONTAINER=1 $BROWSE network
CONTAINER=1 $BROWSE is visible ".hero-section"
CONTAINER=1 $BROWSE screenshot /tmp/prod-check.png
```

### Responsive layout check
```bash
CONTAINER=1 $BROWSE goto https://yourapp.com
CONTAINER=1 $BROWSE responsive /tmp/layout
# Creates: layout-mobile.png, layout-tablet.png, layout-desktop.png
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CONTAINER=1` | Required in Docker/container — disables Chromium sandbox |
| `BROWSE_EXTENSIONS_DIR` | Path to Chrome extensions (optional) |

## Troubleshooting

**"Chromium sandboxing failed"** — Set `CONTAINER=1` environment variable.

**"browse binary not found"** — Run the build step:
```bash
cd founderclaw/browse && bun install && bun build src/cli.ts --compile --outfile dist/browse
```

**Slow first launch** — Playwright downloads Chromium on first use (~150MB). Subsequent runs are instant.
