---
name: application-use
description: macOS desktop automation CLI for AI agents. Use for opening apps, clicking elements, filling forms, scrolling, or any macOS desktop task. Triggers: "open an app", "click a button", "fill a form", or programmatic macOS interaction.
allowed-tools: Bash(./application-use:*), Bash(application-use:*)
---

# macOS Desktop Automation (`application-use`)

A CLI to automate macOS applications.

## install

```bash
npm i -g application-use
```

## 🚀 Core Workflow

1. **Open**: `application-use open --appName "<Name>"` -- _Auto-shows initial snapshot._
2. **Interact**: Use hints (e.g., `[A]`) to click, type, or scroll.
3. **Auto-Update**: Commands (`open`, `click`, `type`, `sendkey`, `scroll`) automatically display an updated snapshot.

> [!TIP]
> Use `application-use snapshot` only when you need a fresh view without any action (e.g., after waiting for dynamic content).

## 🛠 Command Reference

| Command      | Usage                            | Description                              |
| :----------- | :------------------------------- | :--------------------------------------- |
| `open`       | `open --appName "Safari"`        | Opens app and shows snapshot.            |
| `click`      | `click A [--right] [--double]`   | Clicks element by hint letter.           |
| `fill`       | `fill A "text"` or `fill "text"` | Fills text into hint or focused element. |
| `sendkey`    | `sendkey enter`, `sendkey cmd+v` | Sends single or shortcut keys.           |
| `scroll`     | `scroll "Main" down [500]`       | Scrolls area by name/hint.               |
| `screenshot` | `screenshot [path] [--frame]`    | Captures window or specific coordinates. |
| `search`     | `search "Safari"`                | Finds installed application names.       |
| `close`      | `close --appName "Safari"`       | Quits the specified application.         |
| `type`       | `type "text"`                    | Types text into the focused element.     |

## 🏷 Hint System

- **Elements**: `[A]`, `[B]`, `[AA]`... (Interactive elements).
- **Areas**: `[a]`, `[b]`... (Targets for scrolling).
- **Special Marks**: `(*)` = OCR-detected; `(+)` = Newly added since last snapshot.

## ⚡️ Common Automation Patterns

### Form Filling & Submission & scroll

```bash
application-use open --appName "Safari"
application-use fill A "user@example.com"    # Fill email
application-use sendkey tab                   # Next field
application-use fill "password"               # Focus-fill password
application-use sendkey enter                 # Submit
application-use scroll d down 1000            # Scroll down area d
```

### Browser Navigation

```bash
application-use open --appName "Safari"
application-use fill A "https://google.com" && application-use sendkey enter
# Wait for load, then interact with hints from auto-snapshot
```

### File Operations (Finder)

```bash
application-use open --appName "Finder"
application-use sendkey cmd+shift+g           # Go to Folder
application-use fill "/Users/name/Downloads" && application-use sendkey enter

# Open in New Tab via right-click
application-use click A --right               # Right-click folder/file (hint A)
application-use click B                       # Click "Open in New Tab" from menu (hint B)
```
