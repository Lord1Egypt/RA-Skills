---
name: Apple News (MacOS)
slug: apple-news
version: 1.0.0
homepage: https://clawic.com/skills/apple-news
description: Open Apple News, read Apple News links, and run local News workflows on macOS using deterministic CLI commands and shortcut-based search fallback.
changelog: Initial release with validated macOS command paths for Apple News reading flows, link opening, and safe multi-link handling.
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":[],"anyBins":["open","osascript","shortcuts"],"config":["~/apple-news/"]},"os":["darwin"],"configPaths":["~/apple-news/"]}}
---

## Setup

On first use, follow `setup.md` to define command-path preferences, link-opening behavior, and search fallback strategy before bulk actions.

## When to Use

User wants to open Apple News, read specific Apple News articles, or run repeatable News reading workflows from macOS.
Agent handles app launch, article and feed link opening, reading queue workflows, and optional shortcut-based topic search.

## Requirements

- macOS with News.app installed at `/System/Applications/News.app`.
- At least one working command path: `open`, `osascript`, or `shortcuts`.
- Apple News links when opening specific articles (`https://apple.news/...`).
- Explicit confirmation before opening multiple links or running broad shortcut workflows.

## Architecture

Memory lives in `~/apple-news/`. See `memory-template.md` for structure.

```text
~/apple-news/
├── memory.md             # Status, defaults, and preferred workflows
├── command-paths.md      # Command probes and validated launch paths
├── safety-log.md         # Multi-link confirmations and sensitive link notes
└── operation-log.md      # Open operations, shortcut calls, and outcomes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and first-run behavior | `setup.md` |
| Memory structure | `memory-template.md` |
| Command hierarchy and probes | `command-paths.md` |
| Deterministic operation flows | `operation-patterns.md` |
| Safety checklist before action | `safety-checklist.md` |
| Failure handling and recovery | `troubleshooting.md` |

## Data Storage

All skill files are stored in `~/apple-news/`.
Before creating or changing local files, describe the planned write and ask for confirmation.

## Core Rules

### 1. Launch News.app with Deterministic Paths
- Prefer opening News by absolute app path: `open /System/Applications/News.app`.
- Do not assume `open -a News` works on every macOS locale.

### 2. Treat Apple News Links as the Primary Read Interface
- For direct article reads, prefer `https://apple.news/...` links and open them in News.app.
- Validate URL shape before launch and reject malformed links.

### 3. Use Search Fallbacks Explicitly
- If user asks for topic search and no direct Apple News link is available, use a user-owned Shortcut workflow when configured.
- If no search shortcut is configured, ask for one target source or one reference link before proceeding.

### 4. Preview Actions Before Opening
- Show which URL or shortcut will run before execution.
- For query text that may contain sensitive terms, require explicit confirmation before launch.

### 5. Confirm High-Impact Opens
- Always require confirmation before opening multiple links in one step.
- For more than one link, show count and require a second explicit confirmation.

### 6. Verify Launch Result State
- After launch, confirm expected state: app opened, target link opened, or shortcut completed.
- If expected state is not reached, stop and switch to a safer fallback path.

### 7. Keep Data Exposure Minimal
- Use only links and fields needed for the requested read task.
- Do not send undeclared data to third-party APIs from this skill.

## Common Traps

- Assuming `open -a News` works everywhere -> launch failures on some systems.
- Trying unsupported URL schemes (`applenews://`) -> no app resolver errors.
- Running topic search without a validated shortcut path -> inconsistent behavior.
- Opening many article links at once -> user loses reading context.
- Treating generic web pages as Apple News links -> wrong app or wrong result.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://apple.news | Apple News article/feed URL parameters | Open Apple News content in News.app |

No other external endpoint is required by default.

## Security & Privacy

**Data that stays local:**
- Operational defaults, safety choices, and command reliability notes in `~/apple-news/`.

**Data that may leave your machine:**
- Apple News links opened through `https://apple.news`.
- Any network requests triggered by user-owned Shortcuts if user enables them.

**This skill does NOT:**
- Execute undeclared API calls by default.
- Persist sensitive reading context without user approval.
- Run bulk opens without explicit confirmation.

## Trust

By using this skill, links are opened against Apple News.
If you enable shortcut-based search, those shortcuts may call additional services defined by the user.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `macos` - macOS command workflows and automation patterns.
- `news` - general news workflows and monitoring patterns.
- `travel` - location and context workflows for news around destinations.
- `reading` - reading queue and prioritization workflows.
- `productivity` - execution frameworks for daily information intake.

## Feedback

- If useful: `clawhub star apple-news`
- Stay updated: `clawhub sync`
