#!/usr/bin/env bash
# monitor_dialogs 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/monitor_dialogs.cmd 或 python scripts/monitor_dialogs.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/monitor_dialogs.py" "$@"
