---
name: browser-context
description: Background knowledge about browser automation tools and capabilities. Provides reference for how to control the browser, available primitives, interaction patterns, and error handling. 浏览器控制参考、浏览器工具文档、浏览器自动化能力、browser_subagent使用方法。
user-invocable: false
---

# Browser Automation Reference

You have access to browser automation that controls the local Google Chrome browser.

## Backend Detection

Detect which backend is available and use it:

### Backend A: Antigravity (`browser_subagent`)
If you have the `browser_subagent` tool available, use it directly.
See [api-reference.md](../docs/api-reference.md) for full details.

### Backend B: Playwright CLI (`scripts/browser.py`)
If you have terminal/command execution access but no `browser_subagent`, use the CLI adapter:

```bash
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py navigate <url>
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py screenshot [url] [--output path.png] [--full]
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py dom
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py text
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py click <x> <y>
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py type <text>
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py key <key_name>
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py scroll <direction> [amount]
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py resize <width> <height>
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py network
python ${CLAUDE_SKILL_DIR}/../scripts/browser.py console
```

## Tool Mapping

| Action | Antigravity (`browser_subagent`) | Playwright CLI (`browser.py`) |
|--------|----------------------------------|-------------------------------|
| Navigate | `open_browser_url` | `browser.py navigate <url>` |
| Screenshot | `capture_browser_screenshot` | `browser.py screenshot` |
| Read DOM | `browser_get_dom` | `browser.py dom` |
| Read text | `read_browser_page` | `browser.py text` |
| Click | `click_browser_pixel x y` | `browser.py click <x> <y>` |
| Type | (via browser_press_key) | `browser.py type <text>` |
| Key press | `browser_press_key` | `browser.py key <key>` |
| Scroll | `browser_scroll` | `browser.py scroll <dir> [amt]` |
| Resize | `browser_resize_window` | `browser.py resize <w> <h>` |
| Network | `browser_list_network_requests` | `browser.py network` |
| Console | `capture_browser_console_logs` | `browser.py console` |
| Lock input | (automatic in Antigravity) | `browser.py lock` |
| Unlock input | (automatic in Antigravity) | `browser.py unlock` |

## Core Pattern: Observe → Act → Verify

1. Get DOM / screenshot to understand current state
2. Perform action (click, type, scroll)
3. Screenshot to verify the result

## Key Rules

- Use **pixel coordinates** for clicking (from DOM data), not CSS selectors
- Always **verify via screenshot** after actions
- For Antigravity: pass `ReusedSubagentId` to continue multi-step flows
- For CLI: the browser session persists automatically between calls
- For CLI: use `browser.py lock` before interactive sequences to **prevent user interference**, and `browser.py unlock` after
