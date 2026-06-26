---
name: ai-pa-browser
description: Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection
metadata: {"clawdbot":{"emoji":"🌐","requires":{"commands":["agent-browser"]},"homepage":"https://github.com/vercel-labs/agent-browser"}}
---

# Agent Browser Skill

Fast browser automation via accessibility tree snapshots and ref-based element selection.

## When to Use

**Use agent-browser (this skill) when:**
- Automating multi-step web workflows
- Need deterministic element selection
- Working with complex SPAs or login flows
- Need parallel sessions or video recording

**Use built-in browser tool when:**
- Need screenshots/PDFs for visual analysis
- Browser extension integration needed

## Core Workflow

```bash
agent-browser open <url>
agent-browser snapshot -i --json   # Get interactive elements with refs
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser wait --load networkidle
agent-browser snapshot -i --json   # Re-snapshot after navigation
```

## Most Common Commands

```bash
# Navigate
agent-browser open <url> | back | forward | reload | close

# Snapshot
agent-browser snapshot -i --json          # Always use these flags
agent-browser snapshot -s "#main" -i      # Scope to selector

# Interact (use @refs from snapshot)
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser press Enter
agent-browser select @e3 "value"
agent-browser scroll down 500

# Wait
agent-browser wait --load networkidle
agent-browser wait --text "Success"
agent-browser wait @e1

# State
agent-browser state save auth.json
agent-browser state load auth.json
```

## Installation

```bash
npm install -g agent-browser
agent-browser install           # Download Chromium
agent-browser install --with-deps  # Linux: + system deps
```

## Full Reference

For complete command list: read `skills/ai-pa-browser-clawdbot/references/commands.md`
For examples: read `skills/ai-pa-browser-clawdbot/references/examples.md`
