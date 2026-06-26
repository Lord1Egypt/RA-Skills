---
name: browser-automation
description: Browser automation for AI agents using PinchTab. Control Chrome programmatically for testing, scraping, and interaction. Features token-efficient text extraction, multi-instance orchestration, headless/headed modes, and MCP integration. Use when automating browser tasks, extracting web data, testing web apps, or validating sites in real browsers.
metadata:
  version: "1.0"
  origin: "PinchTab"
---

# Browser Automation

Browser automation for AI agents using [PinchTab](https://pinchtab.com) — a high-performance Chrome bridge with HTTP API.

## What is PinchTab?

- **Standalone HTTP server** — Control Chrome via HTTP API
- **Token-efficient** — 800 tokens/page with text extraction (vs 10,000+ for screenshots)
- **Multi-instance** — Run multiple parallel Chrome processes with isolated profiles
- **Headless or Headed** — Run without window or with visible Chrome
- **Self-contained** — 12MB binary, no external dependencies
- **MCP integration** — Native SMCP plugin for Claude Code

## Quick Start

### Installation

```bash
# macOS / Linux
curl -fsSL https://pinchtab.com/install.sh | bash

# npm
npm install -g pinchtab

# Docker
docker run -d -p 9867:9867 pinchtab/pinchtab
```

### Start Server

```bash
# Terminal 1: Start PinchTab server
pinchtab
# Server runs on http://localhost:9867
```

### Basic Commands

```bash
# Navigate
pinchtab nav https://pinchtab.com

# Wait 3 seconds for accessibility tree
sleep 3

# Get interactive elements
pinchtab snap -i -c

# Extract text (token-efficient)
pinchtab text

# Click element by ref
pinchtab click e5

# Fill input
pinchtab fill e3 "user@example.com"
```

---

## Core Concepts

### Instance

A running Chrome process. Each instance has isolated state.

```bash
# Create headless instance
pinchtab instances create --mode=headless

# Create headed instance (visible window)
pinchtab instances create --mode=headed

# List instances
pinchtab instances list

# Stop instance
pinchtab instances stop <instance-id>
```

### Profile

Browser state (cookies, history, localStorage). Log in once, stay logged in.

```bash
# Create instance with profile
pinchtab instances create --profile=work

# Profile persists across restarts
```

### Tab

A single webpage. Each instance can have multiple tabs.

```bash
# Open new tab
pinchtab tabs open https://example.com

# List tabs
pinchtab tabs list

# Close tab
pinchtab tabs close <tab-id>
```

---

## Token-Efficient Patterns

### The 3-Second Wait Rule

**Critical:** Chrome's accessibility tree takes ~3 seconds to populate after navigation.

```bash
# ❌ Too fast - empty tree
pinchtab nav https://example.com
pinchtab snap
# Returns: {"count": 1, "nodes": [{"ref": "e0"}]}

# ✅ Wait 3 seconds
pinchtab nav https://example.com
sleep 3
pinchtab snap
# Returns: {"count": 2645, "nodes": [...]}
```

### Optimal Extraction Pattern

```bash
# Navigate + wait + filter (14x token savings)
curl -X POST http://localhost:9867/navigate \
  -d '{"url": "https://example.com"}' && \
sleep 3 && \
curl http://localhost:9867/snapshot | \
jq '.nodes[] | select(.name | length > 15) | .name' | \
head -30
```

**Why this works:**
1. Navigate + wait ensures full accessibility tree
2. jq filter extracts text nodes only
3. `length > 15` filters buttons/labels
4. `head -30` limits output

**Token comparison:**
- Exploratory approach: ~3,800 tokens
- Pattern-driven: ~270 tokens
- **Savings: 14x**

---

## HTTP API Reference

### Base URL

```
http://localhost:9867
```

### Instances

```bash
# Create instance
TAB=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"profile":"work","mode":"headless"}' | jq -r '.id')

# List instances
curl http://localhost:9867/instances

# Stop instance
curl -X POST "http://localhost:9867/instances/$TAB/stop"
```

### Navigation

```bash
# Navigate to URL
curl -X POST "http://localhost:9867/instances/$TAB/tabs/open" \
  -d '{"url":"https://example.com"}'

# Wait for load
sleep 3
```

### Snapshot

```bash
# Full snapshot
curl "http://localhost:9867/instances/$TAB/snapshot"

# Interactive elements only
curl "http://localhost:9867/instances/$TAB/snapshot?filter=interactive"

# With coordinates
curl "http://localhost:9867/instances/$TAB/snapshot?includeCoords=true"
```

### Actions

```bash
# Click element
curl -X POST "http://localhost:9867/instances/$TAB/action" \
  -d '{"kind":"click","ref":"e5"}'

# Type text
curl -X POST "http://localhost:9867/instances/$TAB/action" \
  -d '{"kind":"type","ref":"e12","text":"hello"}'

# Press key
curl -X POST "http://localhost:9867/instances/$TAB/action" \
  -d '{"kind":"key","ref":"e12","key":"Enter"}'

# Scroll
curl -X POST "http://localhost:9867/instances/$TAB/action" \
  -d '{"kind":"scroll","direction":"down"}'
```

### Extraction

```bash
# Extract text (token-efficient)
curl "http://localhost:9867/instances/$TAB/text"

# Take screenshot
curl "http://localhost:9867/instances/$TAB/screenshot" \
  --output screenshot.png

# Generate PDF
curl "http://localhost:9867/instances/$TAB/pdf" \
  --output page.pdf

# Evaluate JavaScript
curl -X POST "http://localhost:9867/instances/$TAB/evaluate" \
  -d '{"script": "document.title"}'
```

---

## Common Patterns

### Pattern 1: Web Scraping

```bash
#!/bin/bash
# scrape-headlines.sh

URL=$1
INST=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"mode":"headless"}' | jq -r '.id')

# Navigate and wait
curl -s -X POST "http://localhost:9867/instances/$INST/tabs/open" \
  -d "{\"url\":\"$URL\"}"
sleep 3

# Extract headlines (filter by length)
curl -s "http://localhost:9867/instances/$INST/snapshot" | \
  jq '.nodes[] | select(.name | length > 20) | .name' | \
  head -20

# Cleanup
curl -s -X POST "http://localhost:9867/instances/$INST/stop"
```

### Pattern 2: Form Interaction

```bash
#!/bin/bash
# fill-form.sh

INST=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"mode":"headless"}' | jq -r '.id')

# Navigate to form
curl -s -X POST "http://localhost:9867/instances/$INST/tabs/open" \
  -d '{"url":"https://example.com/login"}'
sleep 3

# Get snapshot to find element refs
SNAPSHOT=$(curl -s "http://localhost:9867/instances/$INST/snapshot?filter=interactive")

# Extract refs (example: e5=email, e7=password, e9=submit)
EMAIL_REF=$(echo $SNAPSHOT | jq -r '.nodes[] | select(.name | contains("email")) | .ref')
PASS_REF=$(echo $SNAPSHOT | jq -r '.nodes[] | select(.name | contains("password")) | .ref')
SUBMIT_REF=$(echo $SNAPSHOT | jq -r '.nodes[] | select(.role == "button") | .ref')

# Fill form
curl -s -X POST "http://localhost:9867/instances/$INST/action" \
  -d "{\"kind\":\"type\",\"ref\":\"$EMAIL_REF\",\"text\":\"user@example.com\"}"
curl -s -X POST "http://localhost:9867/instances/$INST/action" \
  -d "{\"kind\":\"type\",\"ref\":\"$PASS_REF\",\"text\":\"password123\"}"

# Submit
curl -s -X POST "http://localhost:9867/instances/$INST/action" \
  -d "{\"kind\":\"click\",\"ref\":\"$SUBMIT_REF\"}"

# Wait for navigation
sleep 3

# Verify login
curl -s "http://localhost:9867/instances/$INST/text" | jq -r '.title'

# Cleanup
curl -s -X POST "http://localhost:9867/instances/$INST/stop"
```

### Pattern 3: Multi-Instance Parallel Processing

```bash
#!/bin/bash
# parallel-scrape.sh

URLS=("https://site1.com" "https://site2.com" "https://site3.com")
INSTANCES=()

# Create instances
for i in {0..2}; do
  INST=$(curl -s -X POST http://localhost:9867/instances \
    -d '{"mode":"headless"}' | jq -r '.id')
  INSTANCES[$i]=$INST
done

# Launch parallel jobs
for i in {0..2}; do
  (
    curl -s -X POST "http://localhost:9867/instances/${INSTANCES[$i]}/tabs/open" \
      -d "{\"url\":\"${URLS[$i]}\"}"
    sleep 3
    TITLE=$(curl -s "http://localhost:9867/instances/${INSTANCES[$i]}/text" | jq -r '.title')
    echo "Result $i: $TITLE"
    curl -s -X POST "http://localhost:9867/instances/${INSTANCES[$i]}/stop"
  ) &
done

wait
echo "All complete"
```

### Pattern 4: Visual Regression Testing

```bash
#!/bin/bash
# visual-regression.sh

URLS=("https://staging.example.com" "https://production.example.com")
INST=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"mode":"headless"}' | jq -r '.id')

for URL in "${URLS[@]}"; do
  curl -s -X POST "http://localhost:9867/instances/$INST/tabs/open" \
    -d "{\"url\":\"$URL\"}"
  sleep 3

  # Take screenshot
  FILENAME=$(echo $URL | sed 's/[^a-zA-Z0-9]/_/g').png
  curl -s "http://localhost:9867/instances/$INST/screenshot" \
    --output "$FILENAME"
  echo "Saved: $FILENAME"
done

curl -s -X POST "http://localhost:9867/instances/$INST/stop"
```

### Pattern 5: Session Persistence

```bash
#!/bin/bash
# persistent-session.sh

# Create instance with named profile
INST=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"profile":"myaccount","mode":"headless"}' | jq -r '.id')

# Login once
curl -s -X POST "http://localhost:9867/instances/$INST/tabs/open" \
  -d '{"url":"https://example.com/login"}'
sleep 3
# ... perform login ...

# Stop (cookies saved to profile)
curl -s -X POST "http://localhost:9867/instances/$INST/stop"

# Later: Resume with same profile
INST2=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"profile":"myaccount","mode":"headless"}' | jq -r '.id')

# Already logged in!
curl -s -X POST "http://localhost:9867/instances/$INST2/tabs/open" \
  -d '{"url":"https://example.com/dashboard"}'
```

---

## MCP Integration

PinchTab provides an SMCP plugin for native Claude Code integration.

### Setup

```bash
# Set plugin directory
export MCP_PLUGINS_DIR=/path/to/pinchtab/plugins

# Restart Claude Code to load plugin
```

### Available Tools

| Tool | Description |
|------|-------------|
| `pinchtab__navigate` | Navigate to URL |
| `pinchtab__snapshot` | Get page structure |
| `pinchtab__action` | Click, type, press keys |
| `pinchtab__text` | Extract text content |
| `pinchtab__screenshot` | Capture screenshot |
| `pinchtab__pdf` | Generate PDF |
| `pinchtab__evaluate` | Run JavaScript |
| `pinchtab__cookies_get` | Get cookies |
| `pinchtab__stealth_status` | Check stealth mode |

### Usage in Claude Code

```
Use pinchtab to navigate to example.com and extract the main headlines.
```

Claude will:
1. Call `pinchtab__navigate` with URL
2. Wait 3 seconds
3. Call `pinchtab__snapshot` with filter
4. Extract headlines from result

---

## Headless vs Headed

| Aspect | Headless | Headed |
|--------|----------|--------|
| **Window** | No visible UI | Chrome window visible |
| **Speed** | ~20% faster | Slower (rendering overhead) |
| **Memory** | ~50-80 MB | ~100-150 MB |
| **Use Case** | CI/CD, scraping, batch | Debugging, visual QA |
| **Interaction** | API only | API + manual |

```bash
# Headless for production
pinchtab instances create --mode=headless

# Headed for debugging
pinchtab instances create --mode=headed
```

---

## Best Practices

### DO

- ✅ Wait 3+ seconds after navigation
- ✅ Use text extraction over screenshots (token-efficient)
- ✅ Filter snapshots to reduce tokens
- ✅ Use profiles for persistent sessions
- ✅ Run headless in production
- ✅ Clean up instances after use
- ✅ Handle errors gracefully

### DON'T

- ❌ Skip the 3-second wait
- ❌ Take screenshots for text extraction
- ❌ Parse full snapshots without filtering
- ❌ Use headed mode in CI/CD
- ❌ Leave instances running indefinitely
- ❌ Hardcode element refs (they change)

---

## Troubleshooting

### Only getting 1 node in snapshot

**Cause:** Accessibility tree not ready
**Fix:** Increase wait time to 3+ seconds

```bash
pinchtab nav https://example.com
sleep 3  # Increase if needed
pinchtab snap
```

### Timeouts

**Cause:** Page too slow or Chrome overloaded
**Fix:** Increase sleep or use headless mode

```bash
# Increase wait
sleep 5

# Or use headless for faster rendering
pinchtab instances create --mode=headless
```

### Element not found

**Cause:** Refs change between snapshots
**Fix:** Re-snapshot before each action

```bash
# Get fresh refs before each action
REF=$(pinchtab snap -i | jq -r '.nodes[] | select(.name == "Submit") | .ref')
pinchtab click "$REF"
```

### Connection refused

**Cause:** PinchTab server not running
**Fix:** Start server first

```bash
pinchtab  # In separate terminal
```

---

## References

- [PinchTab Documentation](https://pinchtab.com/docs)
- [PinchTab GitHub](https://github.com/pinchtab/pinchtab)
- [Agent Optimization Guide](https://pinchtab.com/docs/guides/agent-optimization)
- [Common Patterns](https://pinchtab.com/docs/guides/common-patterns)
- [SMCP Plugin](https://github.com/pinchtab/pinchtab/tree/main/plugins)

---

*Token-efficient browser automation for AI agents.*
