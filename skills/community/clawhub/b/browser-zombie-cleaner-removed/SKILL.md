---
name: browser-zombie-cleaner
slug: browser-zombie-cleaner
version: 1.0.0
description: >
  Detect and clean up zombie browser processes left by OpenClaw's browser tool.
  When the OpenClaw Gateway restarts, Playwright-launched browser processes get
  orphaned and accumulate memory. This skill identifies them safely and optionally
  terminates them. Use when: memory is high, browser processes are piling up,
  or as part of periodic health checks.
triggers:
  - zombie browser
  - chrome memory
  - browser cleanup
  - orphan process
  - 僵尸浏览器
  - 浏览器清理
  - 内存占用高
---

# Browser Zombie Cleaner

Detect and clean up orphaned browser processes left behind when OpenClaw Gateway restarts.

## The Problem

OpenClaw's `browser` tool uses Playwright to launch Chrome/Chromium/Firefox. When the Gateway
restarts (update, crash, manual restart), these browser child processes become orphans — their
parent PID changes to 1 (init/systemd). They keep running, consuming memory, and accumulate
over days.

## Safety Design

This tool is **safe by default**:

1. **Detect-only mode** is the default — no processes are killed without `--kill`
2. **Triple verification** before killing: OpenClaw user-data-dir pattern + orphaned PPID + minimum age
3. **Only current user's processes** — never touches other users
4. **Only OpenClaw browsers** — identified by `~/.openclaw/browser/` in the command line
5. **Graceful shutdown** — SIGTERM first, SIGKILL only after grace period
6. **Audit log** — every action is logged to `/tmp/openclaw/zombie-browser-cleanup.log`
7. **No root required** — runs as regular user

## Usage

### Detect only (safe, default)

```bash
bash <skill_dir>/scripts/cleanup-zombie-browsers.sh
```

Output example:
```
Found 8 OpenClaw browser processes, 5 are zombies (1200MB total)
  ZOMBIE: PID=66301 PPID=1 age=3d 2h mem=388MB
  ZOMBIE: PID=152356 PPID=1 age=2d 4h mem=168MB
  ...
Run with --kill to terminate these zombie processes
```

### Detect and clean

```bash
bash <skill_dir>/scripts/cleanup-zombie-browsers.sh --kill
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--kill` | off | Actually terminate zombie processes |
| `--min-age N` | 3600 (1h) | Only target processes older than N seconds |
| `--grace N` | 10 | Seconds between SIGTERM and SIGKILL |
| `--json` | off | Output as JSON (for programmatic use) |
| `--log PATH` | `/tmp/openclaw/zombie-browser-cleanup.log` | Log file location |
| `--pattern STR` | `.openclaw/browser/` | Pattern to identify OpenClaw browsers |

## Integration with Health Checks

Add to your health check script or heartbeat:

```bash
# Detect and report (no kill)
bash /path/to/cleanup-zombie-browsers.sh

# Auto-clean with safety margin (processes must be >2 hours old)
bash /path/to/cleanup-zombie-browsers.sh --kill --min-age 7200
```

## How It Identifies Zombies

A process is classified as a zombie browser if ALL of these are true:

1. **Browser process** — executable name matches chrome/chromium/brave/msedge/firefox
2. **OpenClaw origin** — command line contains `.openclaw/browser/` (the user-data-dir used by OpenClaw)
3. **Orphaned** — PPID is 1 (init) or systemd, meaning the parent Gateway process is gone
4. **Old enough** — process age exceeds `--min-age` threshold (prevents killing browsers that are actively initializing)

If ANY condition is not met, the process is skipped.

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Linux | Full | Uses /proc filesystem for precise detection |
| macOS | Full | Uses ps with etime parsing |
| Windows | Not yet | Planned (PowerShell-based) |

## Supported Browsers

All Playwright-supported browsers with OpenClaw user-data-dir:
- Google Chrome / Chromium
- Brave Browser
- Microsoft Edge
- Firefox

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No zombies found, or zombies cleaned (--kill mode) |
| 1 | Zombies detected but not killed (detect mode) |
