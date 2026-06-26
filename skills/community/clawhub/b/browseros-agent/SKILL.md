---
name: browseros
description: "Use when a task requires interacting with a website beyond just reading it — clicking elements, filling forms, submitting data, navigating through multi-step flows, taking screenshots, or any workflow where the user needs a real browser with actions like click, type, scroll, or select. Also use for managing browser bookmarks, history, or tabs. Trigger whenever the user mentions browseros, browseros-cli, or BrowserOS. Do NOT use when simply fetching or reading page content would suffice — use curl, fetch, or WebFetch for that instead."
allowed-tools: Bash(browseros-cli *)
---

# Browser Automation with BrowserOS

Control a real Chromium browser via `browseros-cli`. Run commands via Bash. Use `--json` for structured output, `-p <pageId>` to target specific tabs.

## When NOT to Use

- Headless scraping in CI/CD with no display — use Playwright or Puppeteer instead.
- Static page fetching where `curl`/`wget` suffices.

## Safety Defaults

- Default to read-only first: `snap`, `text`, `links`, `pages`, `ss`.
- Avoid `eval` unless no simpler command works.
- Save screenshots/PDFs only to user-specified or workspace paths.
- Close tabs when done: `browseros-cli close <pageId>`.

## Setup

```bash
# Check if CLI is available
browseros-cli --version

# If not installed:
npm install -g browseros-cli

# If BrowserOS app is not installed:
browseros-cli install

# If BrowserOS is not running:
browseros-cli launch

# Configure connection:
browseros-cli init --auto

# Verify:
browseros-cli health
```

## Core Workflow: snap → act → re-snap

Every interaction follows this loop:

1. **Open** a page → get a page ID.
2. **Snap** → get element IDs like `[10] textbox "Email"`, `[15] button "Submit"`.
3. **Act** on elements by ID (`fill 10 "text"`, `click 15`).
4. **Re-snap** after ANY click, navigation, or form submit — IDs change after DOM updates.

**Critical rules:**
- `open <url>` = new tab. `nav <url>` = navigate current tab.
- NEVER reuse element IDs after navigation — always `snap` again.
- Use `text` for content extraction, `snap` for interaction, `ss` for visual verification.

```bash
browseros-cli open https://example.com/login    # → Page ID: 5
browseros-cli snap -p 5                          # → [10] textbox "Email", [11] textbox "Password", [15] button "Sign In"
browseros-cli fill 10 "user@example.com"
browseros-cli fill 11 "password123"
browseros-cli click 15
browseros-cli snap -p 5                          # Re-snap! IDs have changed after submit
browseros-cli text -p 5                          # Read result page
browseros-cli close 5                            # Clean up
```

## Commands Quick Reference

| Category | Key Commands |
|----------|-------------|
| **Navigate** | `open <url>`, `open --hidden`, `nav <url>`, `back`, `forward`, `reload`, `pages`, `active`, `close [id]` |
| **Observe** | `snap`, `snap -e`, `text`, `text --selector <css>`, `text --links`, `text --viewport`, `links`, `ss -o <path>`, `ss --full`, `eval "<js>"`, `dom`, `dom-search "<q>"`, `wait --text "<txt>"` |
| **Input** | `click <id>`, `click --double`, `fill <id> "text"`, `clear <id>`, `key Enter`, `hover <id>`, `focus <id>`, `check <id>`, `uncheck <id>`, `select <id> "val"`, `scroll down [amt]`, `drag <id> --to <id>`, `upload <id> <file>`, `dialog accept/dismiss` |
| **Export** | `pdf <path>`, `download <id> <dir>` |
| **Resources** | `window list/create/close/activate`, `bookmark list/search/create/remove/update/move`, `history recent/search/delete`, `group list/create/update/ungroup/close` |

Full flags and options: see [references/cli-commands.md](references/cli-commands.md) or run `browseros-cli <command> --help`.

## Common Patterns

### Data extraction
```bash
browseros-cli open https://example.com/data
browseros-cli text                         # full page as markdown
browseros-cli text --selector "table"      # scoped to element
browseros-cli text --links                 # include hyperlinks
```

### Multi-tab research
```bash
browseros-cli open https://site-a.com      # → Page ID: 1
browseros-cli open https://site-b.com      # → Page ID: 2
browseros-cli text -p 1                    # extract from first
browseros-cli text -p 2                    # extract from second
browseros-cli close 1 && browseros-cli close 2
```

### Web app testing
```bash
browseros-cli open http://localhost:3000
browseros-cli snap                         # get interactive elements
browseros-cli ss -o test-state.png         # visual snapshot
browseros-cli eval "document.querySelectorAll('.error').length"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using CSS selectors (`fill --selector "input[type=email]"`) | Always `snap` first, then use element IDs (`fill 10 "text"`) |
| Reusing element IDs after a click or navigation | IDs are invalidated by DOM changes — `snap` again |
| Using `eval` to extract text | Use `text` or `text --selector` instead — lower tokens, structured output |
| Forgetting to close tabs | Always `close <pageId>` when done to avoid resource leaks |
| Using `nav` when you want a new tab | `nav` replaces the current tab. Use `open` for a new tab |
| Using `open` when you want to stay in the same tab | `open` creates a new tab. Use `nav` to navigate in place |
| Taking screenshots for content extraction | Use `text` for content — screenshots burn tokens and need vision |
| Using `dialog --accept` (flag syntax) | Correct syntax is `dialog accept` or `dialog dismiss` (positional arg) |

## Deep-Dive Documentation

| Reference | Description |
|-----------|-------------|
| [references/cli-commands.md](references/cli-commands.md) | Full command reference with all flags |

## Links

- [BrowserOS](https://browseros.com)
- [CLI Source](https://github.com/browseros-ai/BrowserOS/tree/main/packages/browseros-agent/apps/cli)
- [MCP Setup Guide](https://docs.browseros.com/features/use-with-claude-code)
- [Skills Repository](https://github.com/browseros-ai/skills)
