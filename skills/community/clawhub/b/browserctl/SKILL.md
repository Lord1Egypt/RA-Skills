---
name: browsectl
version: 0.1.1
description: "WebDriver automation CLI for AI-driven browser control. Provides session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL."
requires:
  bins: ["browsectl"]
cliHelp: "browsectl --help"
repository: "https://github.com/yorelog/browsectl"
license: MIT
platforms:
  - darwin-amd64
  - darwin-arm64
  - linux-amd64
  - linux-arm64
  - windows-amd64
  - windows-arm64
install: "npm install -g @yorelog/browsectl"
---

# browsectl

> **CRITICAL:** Before doing anything, run `browsectl setup` to detect installed browsers and auto-download the matching WebDriver binary. Sessions persist to `.browsectl/sessions.json` across CLI invocations — you do not need to create a new session every time.

WebDriver automation CLI for AI-driven browser control. `browsectl` provides subcommands for browser session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL.

## Installation

```sh
npm install -g @yorelog/browsectl
browsectl setup
```

## Skills

### Session & Driver Lifecycle

> [skills/session.md](skills/session.md)

Session & driver lifecycle management.

| Command | Description |
|---|---|
| `setup` | Detect browsers and download WebDriver binary |
| `status` | Show driver and session status |
| `driver-start` | Start the WebDriver server |
| `session-create` | Create a new browser session |
| `session-list` | List all active sessions |
| `session-use` | Switch the default session |
| `session-delete` | Delete a session |

### Browser Commands

> [skills/browser.md](skills/browser.md)

Browser interaction commands — navigate, click, type, screenshot, scroll, read state, wait.

| Command | Description |
|---|---|
| `run --type open` | Navigate to a URL |
| `run --type click` | Click a DOM element by CSS selector |
| `run --type fill` | Type text into an input field character by character |
| `run --type paste` | Paste text via clipboard simulation |
| `run --type screenshot` | Capture a DOM element to PNG |
| `run --type scroll` | Scroll the page or a specific element |
| `run --type title` | Get the current page title |
| `run --type last-message-content` | Extract the last message block (chat UIs) |
| `run --type wait` | Wait for a condition (visible, hidden, URL, title, JS) |

### Tab Management

> [skills/tabs.md](skills/tabs.md)

Tab management — list, create, switch, and close browser tabs.

| Command | Description |
|---|---|
| `tab-list` | List all open tabs |
| `tab-create` | Open a new tab |
| `tab-switch` | Switch to a tab by index, alias, or handle |
| `tab-close` | Close a tab |

### Batch Execution

> [skills/batch.md](skills/batch.md)

Batch execution — run single commands, sequential batches from JSON files, and parallel groups.

| Command | Description |
|---|---|
| `run` | Execute a single WebDriver command |
| `batch` | Run a sequence of commands from a JSON file |

### Selector Syntax

> [skills/selectors.md](skills/selectors.md)

CSS selectors with `::text(/regex/flags)` extension for filtering elements by text content.

### Interactive REPL

> [skills/repl.md](skills/repl.md)

Interactive REPL — live command entry, tab-completion, persistent history.

| Command | Description |
|---|---|
| `repl` | Start the interactive REPL |

## Global CLI Flags

| Flag | Default | Description |
|---|---|---|
| `--browser` | `chrome` | Browser to automate: `chrome` or `edge` |
| `--server` | `http://127.0.0.1:9515` | WebDriver server URL |
| `--chromedriver` | *(auto-detected)* | Path to WebDriver binary (chromedriver / msedgedriver) |
| `--chrome-binary` | *(auto-detected)* | Path to browser binary |
| `--user-data-dir` | `~/.browsectl/<browser>-profile` | Browser user-data directory |
| `--profile-directory` | `Default` | Browser profile directory name |
| `--headless` | `false` | Run browser in headless mode |
| `--viewport` | `1024,768` | Viewport size as `width,height` |
| `--session` | *(default session)* | Session ID to operate on |

## Platform Support

| OS | x64 | arm64 |
|---|---|---|
| macOS | ✅ | ✅ |
| Linux | ✅ | ✅ |
| Windows | ✅ | ✅ |