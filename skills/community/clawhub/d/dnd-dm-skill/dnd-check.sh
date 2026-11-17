#!/usr/bin/env bash
# 一条命令完成一次检定：./dnd-check.sh --actor 老白 --skill 潜行 --dc 15
# 实际逻辑在 dnd-check.py（它自己把包内引擎加进 sys.path，不依赖 PYTHONPATH）。
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$HERE/dnd-engine/.venv/bin/python3"
[ -x "$PY" ] || PY="$HERE/dnd-engine/.venv/Scripts/python.exe"
[ -x "$PY" ] || PY="$HERE/../dnd-engine/.venv/Scripts/python.exe"
[ -x "$PY" ] || PY="$(command -v python3 || command -v python)"
exec "$PY" "$HERE/dnd-check.py" "$@"
