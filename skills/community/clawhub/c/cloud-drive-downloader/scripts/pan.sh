#!/usr/bin/env bash
# pan 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/pan.cmd 或 python scripts/pan.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pan.py" "$@"
