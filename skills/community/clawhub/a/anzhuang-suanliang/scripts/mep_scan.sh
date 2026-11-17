#!/usr/bin/env bash
# mep_scan 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/mep_scan.cmd 或 python scripts/mep_scan.py）。
# 统一运行时解析（Python / 识图底座 / vendor）见 scripts/runtime_env.sh
set -euo pipefail
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_HERE/runtime_env.sh"
exec "$PYTHON_BIN" "$_HERE/mep_scan.py" "$@"
