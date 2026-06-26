# browsectl

> WebDriver automation CLI for AI-driven browser control.

[![npm](https://img.shields.io/npm/v/@yorelog/browsectl)](https://www.npmjs.com/package/@yorelog/browsectl)
[![license](https://img.shields.io/github/license/yorelog/browsectl)](LICENSE)

**browsectl** is a cross-platform CLI that wraps the WebDriver protocol for browser automation. It provides session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL — designed to be driven by AI agents or used directly from the terminal.

## Installation

```sh
npm install -g @yorelog/browsectl
```

The `postinstall` script automatically downloads the correct pre-built binary for your platform.

Then run the one-time setup:

```sh
browsectl setup
```

This detects installed browsers (Chrome / Edge), downloads the matching WebDriver binary (chromedriver / msedgedriver), and saves the configuration to `.browsectl/setup.json`.

## Quick Start

```sh
# 1. Setup (first time only)
browsectl setup

# 2. Create a browser session
browsectl session-create

# 3. Navigate to a page
browsectl run --type open --url "https://example.com"

# 4. Click an element
browsectl run --type click --selector "a"

# 5. Take a screenshot
browsectl run --type screenshot --selector "body" --path screenshot.png

# 6. Interactive mode
browsectl repl
```

## Commands

### Session & Driver Lifecycle

| Command | Description |
|---|---|
| `setup` | Detect browsers and download WebDriver binary |
| `status` | Show driver and session status |
| `driver-start` | Start the WebDriver server |
| `session-create` | Create a new browser session |
| `session-list` | List all active sessions |
| `session-use` | Switch the default session |
| `session-delete` | Delete a session |

### Browser Interaction

All browser commands use `browsectl run --type <command>`:

| Command | Description |
|---|---|
| `open` | Navigate to a URL |
| `click` | Click a DOM element by CSS selector |
| `fill` | Type text into an input field character by character |
| `paste` | Paste text via clipboard simulation (faster for large text) |
| `screenshot` | Capture a DOM element to PNG |
| `scroll` | Scroll the page or a specific element |
| `title` | Get the current page title |
| `last-message-content` | Extract the last message block (for chat UIs) |
| `wait` | Wait for a condition (visible, hidden, URL, title, JS) |

### Tab Management

| Command | Description |
|---|---|
| `tab-list` | List all open tabs |
| `tab-create` | Open a new tab |
| `tab-switch` | Switch to a tab by index, alias, or handle |
| `tab-close` | Close a tab |

### Batch Execution

| Command | Description |
|---|---|
| `run` | Execute a single WebDriver command |
| `batch` | Run a sequence of commands from a JSON file |

Batch files support sequential execution and parallel groups.

### Interactive REPL

```sh
browsectl repl
```

Live command entry with tab-completion and persistent history.

## Selector Syntax

browsectl supports standard CSS selectors with an extension for text-based filtering:

```
CSS::text(/pattern/flags)
```

Examples:

```sh
# Click a button containing "Submit"
browsectl run --type click --selector "button::text(/submit/i)"

# Click a link matching exact text
browsectl run --type click --selector "a::text(/^Sign In$/)"
```

## Global Flags

| Flag | Default | Description |
|---|---|---|
| `--browser` | `chrome` | Browser to automate: `chrome` or `edge` |
| `--server` | `http://127.0.0.1:9515` | WebDriver server URL |
| `--chromedriver` | *(auto)* | Path to WebDriver binary |
| `--chrome-binary` | *(auto)* | Path to browser binary |
| `--user-data-dir` | `~/.browsectl/<browser>-profile` | Browser user-data directory |
| `--profile-directory` | `Default` | Browser profile directory name |
| `--headless` | `false` | Run in headless mode |
| `--viewport` | `1024,768` | Viewport size as `width,height` |
| `--session` | *(default)* | Session ID to operate on |

## Platform Support

| OS | x64 | arm64 |
|---|---|---|
| macOS | ✅ | ✅ |
| Linux | ✅ | ✅ |
| Windows | ✅ | ✅ |

Requires Node.js ≥ 16 for the npm wrapper. The CLI binary itself has no runtime dependencies.

## How It Works

The npm package is a lightweight wrapper (~32 kB). On install, it downloads the pre-built Rust binary from [GitHub Releases](https://github.com/yorelog/browsectl/releases) for your platform. The `browsectl` command proxies to that binary.

```
npm install → postinstall downloads binary → bin/browsectl
                                                  ↑
                            scripts/run.js (npm bin entry point)
```

## Documentation

Detailed skill documentation is bundled with the package:

- [Skills Index](skills/README.md) — Overview and quick reference
- [Session & Driver Lifecycle](skills/session.md) — Setup, driver, and session management
- [Browser Commands](skills/browser.md) — Navigation, clicks, typing, screenshots, scrolling
- [Tab Management](skills/tabs.md) — Create, list, switch, close tabs
- [Batch Execution](skills/batch.md) — Single commands, batch files, parallel groups
- [Selector Syntax](skills/selectors.md) — CSS selectors with `::text()` extension
- [Interactive REPL](skills/repl.md) — Live command entry and history

## License

[MIT](LICENSE)