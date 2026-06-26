---
name: brave-browser-agent
description: |
  Control Brave Browser via CDP for web browsing, content extraction, screenshots, and JavaScript execution. Use when needing browser automation, web scraping, dynamic content interaction, or page screenshots. Requires: Brave with --remote-debugging-port=9222.
---

# Brave Browser Agent

Attach to the user's daily Brave Browser via CDP on port 9222. The browser has all login sessions and bookmarks. **Agents only attach — never start, restart, or kill the browser.**

## Critical Rules

> **⚠️ 绝对禁止启动/重启/关闭浏览器！** 浏览器由用户手动管理，agent 只 attach。
> **⚠️ 绝对不要使用 `--restart` 参数！** 除非用户明确要求。

Multiple agents share the same browser instance (port 9222), which has all user login states.

- **Port: 9222** — Brave's remote debugging port (non-configurable)
- **Do NOT start/restart/kill browser** — Browser is manually managed by user, agents only attach
- **Do NOT use `openclaw browser start`** — Will crash Gateway
- **Do NOT use `openclaw gateway restart`** — Will crash Gateway
- **Do NOT use `--restart` parameter** — Strictly prohibited unless explicitly requested
- **Read-first preference** — Use `eval` to extract content, avoid modifying page state
- If 9222 doesn't respond, tell user: "Brave Browser 未启动远程调试，请手动开启" — do NOT auto-start

## Quick Start

### Diagnostic Health Check (Recommended)

```bash
# Full check: CDP connection, tabs, script syntax, SKILL.md health
python3 {{SKILL_DIR}}/scripts/check_cdp.py

# Quick check (connection only)
python3 {{SKILL_DIR}}/scripts/check_cdp.py --quick

# JSON output for debugging
python3 {{SKILL_DIR}}/scripts/check_cdp.py --json
```

### Check Browser Status (Legacy)

```bash
python3 {{SKILL_DIR}}/scripts/check_brave.py
```

### List Tabs

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py list
```

### Open a Page

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py open "https://example.com"
```

### Execute JavaScript

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.title"
```

### Take Screenshot

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot <tab_id> output.png
```

## Smart Interaction (Anti-Detection)

For anti-bot sites (Xiaohongshu, etc.), use CDP native mouse events instead of JS `.click()`:

```bash
# Click element — real mouse events, isTrusted=true
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "button.submit"

# Type text into focused element
python3 {{SKILL_DIR}}/scripts/cdp_exec.py type <tab_id> "search query" --human

# Press a key
python3 {{SKILL_DIR}}/scripts/cdp_exec.py key <tab_id> Enter
```

## Framework-Aware Click (React/Vue/Angular SPAs)

For SPA sites where standard CDP clicks fail (React/Vue/Angular), use multi-strategy auto-fallback:

```bash
# Multi-strategy click (auto: CDP native → React Fiber → Vue emit → dispatchEvent → Enter)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector "button.submit"

# Or find by text content
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --text "发布"

# Detect which JS framework the page uses
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>

# Deep-analyze a button (debugging)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py analyze-button <tab_id> --selector "button.submit"
```

### What `click-smart` Does (Strategy Order)

1. **Editor sync** — Auto-syncs rich text editors before clicking (CKEditor 4/5, Lexical, ProseMirror, Quill, 语雀, iframe editors). Critical for Vue/React editors where content is not synced to framework state
1. **Hit-test check** — ScrollIntoView + elementFromPoint (ensures element is visible and uncovered)
2. **CDP native click** — Input.dispatchMouseEvent with complete event sequence
3. **React Fiber invocation** — Calls React's `onClick` handler via `__reactProps$`. **Fallback: React 18 root container event delegation** for ByteUI/headless UI
4. **Vue emit invocation** — Enhanced Vue 2/3 detection: component tree traversal, `$emit`, `$listeners`, setupState handlers, vnode event walk
5. **dispatchEvent** — Creates a native `MouseEvent(isTrusted=true)` and dispatches it
6. **Enter key** — Focus + Enter key + form submit (for form buttons)

**Publish Validation (auto)**: After all strategies, detects success via toast messages, URL changes, modal state, and button state. Reports errors if found.

Returns JSON showing which strategy succeeded and debugging info.

### New Standalone Commands

```bash
# Validate if publish was successful (after clicking)
python3 {{SKILL_DIR}}/scripts/framework_click.py publish-validate <tab_id>

# Sync editor data without clicking
python3 {{SKILL_DIR}}/scripts/framework_click.py editor-sync <tab_id>
```

### Platform-Specific Notes

| Platform | Framework | Known Issue | Solution |
|----------|-----------|-------------|----------|
| 掘金 | Vue 2 | 发布弹出层按钮 CDP 点击无效 | `click-smart` auto-syncs editor → tries Vue enhanced click |
| CSDN | Vue 3 + CKEditor iframe | 字数统计更新但按钮无反应 | `editor-sync` fires CKEditor `change:data` + iframe input event |
| 头条号 | React ByteUI | onClick 调用成功但无变化 | `click-smart` tries React 18 root delegation + deep fiber traversal |
| 阿里云开发者 | 语雀编辑器 | 非 contenteditable，注入困难 | `editor-sync` triggers lake-editor input events |
| 百家号 | Lexical | contenteditable 注入 | `editor-sync` calls lexical update + dispatchCommand |

### Framework Detection Commands

```bash
# Quick framework detection
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>

# Deep button analysis (for debugging)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py analyze-button <tab_id> --selector "button.submit"
python3 {{SKILL_DIR}}/scripts/cdp_exec.py analyze-button <tab_id> --selector "button.submit" --index 0
```

### Click Strategy Quick Reference

| Task | Command | Why |
|------|---------|-----|
| Simple click (known site) | `interact` | Lightweight, uses CDP native events |
| Click on React/Vue SPA | `click-smart` | Auto-tries 6 strategies + diagnostics |
| Click keeps failing | `detect-framework` + `analyze-button` | Debug overlay/modals/disabled state |
| Form button that won't click | `click-smart` | Auto-tries Enter key + form submit |

### Wait for Page State

```bash
# Wait for page load
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 10

# Wait for element to appear
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector ".result" --timeout 10

# Wait for network idle
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --network-idle --timeout 15
```

### Page State Analysis

```bash
# List interactive elements (useful for exploring unknown pages)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id>

# Check page load status
python3 {{SKILL_DIR}}/scripts/cdp_exec.py page-status <tab_id>

# Detect pagination buttons
python3 {{SKILL_DIR}}/scripts/cdp_exec.py pagination <tab_id>

# Count elements matching selector
python3 {{SKILL_DIR}}/scripts/cdp_exec.py count <tab_id> --selector ".item"

# Smooth scroll (triggers lazy loading)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py scroll <tab_id> --direction down --steps 3

# Highlight element for screenshot debugging
python3 {{SKILL_DIR}}/scripts/cdp_exec.py highlight <tab_id> --selector "#target"
```

### When to Use What

| Task | Command | Why |
|------|---------|-----|
| Read content | `eval` | No interaction needed |
| Simple click | `eval "el.click()"` | Trusted sites |
| Anti-detection click | `interact` | isTrusted=true |
| Fill form (anti-bot) | `type --human` | Char-by-char |
| Fill form (fast) | `type` | Bulk insert |
| Wait for content | `wait` | Dynamic pages |
| Infinite scroll | `scroll` | Lazy loading |
| Explore page | `elements` | Unknown structure |

## Command Reference

All commands go through `cdp_exec.py`:

| Command | Description |
|---------|-------------|
| `list` | List open tabs |
| `status` | Check browser status |
| `open <url>` | Open URL in new tab |
| `close <tab_id>` | Close tab |
| `eval <tab_id> <js>` | Execute JavaScript |
| `screenshot <tab_id> [file]` | Take screenshot |
| `interact <tab_id>` | CDP native mouse click |
| `type <tab_id> <text>` | Type text |
| `key <tab_id> <key>` | Press keyboard key |
| `wait <tab_id>` | Wait for page state |
| `scroll <tab_id>` | Smooth scroll |
| `elements <tab_id>` | List interactive elements |
| `page-status <tab_id>` | Page load status |
| `pagination <tab_id>` | Detect pagination buttons |
| `count <tab_id>` | Count elements by selector |
| `locate <tab_id>` | Get element coordinates |
| `highlight <tab_id>` | Highlight element outline |
| `snapshot <tab_id>` | Lightweight DOM snapshot |
| `click-smart <tab_id>` | **Multi-strategy click** (React/Vue auto-fallback) |
| `detect-framework <tab_id>` | **Detect JS framework** on page |
| `analyze-button <tab_id>` | **Deep-analyze** a button element |

## Common Patterns

For detailed usage patterns and workflows, see [references/PATTERNS.md](references/PATTERNS.md).

For site-specific anti-detection strategies (Xiaohongshu, SPA pages, etc.), see [references/site-patterns.md](references/site-patterns.md).

For React/Vue/Angular framework-aware clicking and platform-specific strategies (头条号, 掘金, CSDN, etc.), see [references/framework-publish.md](references/framework-publish.md).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `CDP HTTP error` | Check Brave is running with `curl -s http://localhost:9222/json/version`. If not, ask user to restart Brave with `--remote-debugging-port=9222` |
| `Tab not found` | Run `cdp_exec.py list` to get current tab IDs |
| `JS Error` | Check if page loaded; add `--await-promise` for async ops |
| `websockets not installed` | `pip3 install websockets` |
| Brave won't respond | Ask user to restart Brave. **DO NOT kill the process yourself.** |
| Click not working | Use `interact` instead of `eval ".click()"` for anti-bot sites |
| Element not found | Use `elements` to check page structure; `wait` before interacting |
