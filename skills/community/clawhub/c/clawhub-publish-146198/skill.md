# Agent Browser

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

## When to use
- Automating web interactions (login, form fill, scraping)
- Extracting structured data from pages
- Testing web UIs or workflows
- Filling forms programmatically

## Prerequisites
- Node.js ≥ 18
- `npm install -g agent-browser` (run once to install CLI)

## How it works
1. `agent-browser open <url>` → launch browser & navigate
2. `agent-browser snapshot -i` → get interactive elements with stable refs (e.g., `@e1`)
3. Use refs to interact: `click @e1`, `fill @e2 "text"`, `wait @e3`
4. `agent-browser close` → clean up

## Key capabilities
- Snapshot with accessibility tree or interactive-only mode
- Precise element interaction (click/fill/hover/drag/upload)
- Wait conditions (element visible, URL change, network idle)
- Screenshot, PDF export, video recording
- Cookie/storage/network control
- Tab/window/frame management
- JSON output for programmatic parsing

## Example
```bash
agent-browser open https://example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --url "/dashboard"
```