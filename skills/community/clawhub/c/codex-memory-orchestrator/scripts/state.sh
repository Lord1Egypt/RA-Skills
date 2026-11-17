#!/usr/bin/env bash
# state 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/state.cmd 或 python scripts/state.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/state.py" "$@"
