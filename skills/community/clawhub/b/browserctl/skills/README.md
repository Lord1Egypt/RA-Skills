---
name: browsectl
version: 0.1.1
description: "WebDriver automation CLI for AI-driven browser control. Provides session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL."
metadata:
  requires:
    bins: ["browsectl"]
  cliHelp: "browsectl --help"
---

# browsectl (0.1.1)

> **CRITICAL:** Before doing anything, run `browsectl setup` to detect installed browsers and auto-download the matching WebDriver binary. Sessions persist to `.browsectl/sessions.json` across CLI invocations — you do not need to create a new session every time.

A WebDriver automation CLI for AI-driven browser control. `browsectl` provides subcommands for browser session management, tab control, element interaction, screenshots, batch execution, and an interactive REPL.

## Installation

```sh
npm install -g @yorelog/browsectl
browsectl setup
```

`browsectl setup` detects your platform, finds installed browsers (Chrome / Edge), and automatically downloads the matching WebDriver binary (chromedriver / msedgedriver).

## Skills Index

| Skill file | Category | Commands |
|---|---|---|
| [session.md](session.md) | Session & driver lifecycle | `setup`, `status`, `driver-start`, `session-create`, `session-list`, `session-use`, `session-delete` |
| [browser.md](browser.md) | Browser commands | `run --type open`, `click`, `fill`, `paste`, `screenshot`, `scroll`, `title`, `last-message-content`, `wait` |
| [tabs.md](tabs.md) | Tab management | `tab-list`, `tab-create`, `tab-switch`, `tab-close` |
| [batch.md](batch.md) | Batch execution | `run`, `batch` — single commands, batch files, parallel groups |
| [selectors.md](selectors.md) | Selector syntax reference | CSS selectors + `::text(/regex/flags)` extension |
| [repl.md](repl.md) | Interactive REPL | Live command entry, history, tab-completion |

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
| `--session` | *(default session)* | Session ID to operate on (omit for default) |

## Platform Support

| OS | x64 | arm64 |
|---|---|---|
| macOS | ✅ | ✅ |
| Linux | ✅ | ✅ |
| Windows | ✅ | ✅ |