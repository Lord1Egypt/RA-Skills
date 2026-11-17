#!/usr/bin/env bash
# step_orchestrator 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/step_orchestrator.cmd 或 python scripts/step_orchestrator.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/step_orchestrator.py" "$@"
