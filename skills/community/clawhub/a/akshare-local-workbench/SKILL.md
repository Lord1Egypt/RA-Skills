---
name: akshare-local-workbench
description: Install, run, maintain, and troubleshoot a bundled local single-user AKShare financial data workbench. Use this skill when OpenClaw needs to create the workbench project from included assets without cloning GitHub, start/stop the FastAPI and React app, run setup/tests, manage local result cache, edit the AKShare YAML indicator catalog, or reduce Eastmoney/东方财富 request-limit errors.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npm
    anyBins:
      - python3
      - python
    envVars:
      - name: AKSHARE_WORKBENCH_ROOT
        required: false
        description: Optional path to an existing akshare-workbench project.
      - name: AKSHARE_PROXY_MODE
        required: false
        description: "Optional proxy mode for AKShare requests: auto, direct, or system."
      - name: AKSHARE_EASTMONEY_INTERVAL_SECONDS
        required: false
        description: Optional Eastmoney request interval in seconds; increase when rate-limited.
      - name: AKSHARE_BACKEND_PORT
        required: false
        description: Optional backend port, defaults to 8000.
      - name: AKSHARE_FRONTEND_PORT
        required: false
        description: Optional frontend port, defaults to 5173.
    emoji: "📈"
    homepage: https://github.com/TianYeDavid/akshare-local-workbench
---

# AKShare Local Workbench

Use this skill to create and operate a local AKShare data workbench from bundled source files. This standalone ClawHub package includes the app source under `assets/akshare-workbench`, so `init-project` does not clone GitHub.

Treat the app as a local single-user tool. Prefer caching, slow request pacing, and targeted indicators over high-frequency or bulk data-source access.

## Quick Start

Create the workbench project from bundled assets:

```bash
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py init-project --target akshare-workbench
```

Then install dependencies and start:

```bash
cd akshare-workbench
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py setup
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py start
```

When installed through OpenClaw/ClawHub, use the skill's installed script path. If the app already exists, run commands from inside the app project or pass:

```bash
--root /path/to/akshare-workbench
```

## Main Commands

```bash
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py init-project --target akshare-workbench
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py doctor
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py setup
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py start
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py status
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py restart
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py test
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py clear-cache
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py stop
```

The frontend defaults to `http://127.0.0.1:5173`; backend health is `http://127.0.0.1:8000/api/health`.

## Request-Limit Guidance

The controller starts the backend with conservative defaults:

```bash
AKSHARE_MAX_CONCURRENT=1
AKSHARE_EASTMONEY_INTERVAL_SECONDS=12
AKSHARE_EASTMONEY_HTTP_RETRIES=2
AKSHARE_EASTMONEY_CALL_ATTEMPTS=1
AKSHARE_EASTMONEY_CACHE_TTL_SECONDS=1800
AKSHARE_RESULT_CACHE_TTL_SECONDS=900
AKSHARE_ENRICH_NAMES=0
```

Ordinary "提取" uses local cache. "强制刷新" bypasses cache and should be used sparingly.

For Eastmoney/东方财富 `RemoteDisconnected` or `Connection aborted` errors:

1. Wait several minutes.
2. Avoid repeated forced refreshes.
3. Prefer single-symbol indicators over full-market real-time endpoints.
4. Try `AKSHARE_PROXY_MODE=direct` or `AKSHARE_PROXY_MODE=system`.
5. Raise `AKSHARE_EASTMONEY_INTERVAL_SECONDS` to `20` or `30`.

Do not use IP rotation, high-concurrency scraping, or attempts to bypass upstream restrictions. For production, commercial, high-frequency, or bulk use, use an official or licensed data feed.

## Maintenance

Read `references/maintenance.md` for bundled asset details, common commands, catalog maintenance, troubleshooting, and open-source/disclaimer notes.
