#!/usr/bin/env bash
# cad-file-reader -> lis-skill-bus 可选接线（薄壳，逻辑在 cad_statesync.py）。
# 用法见 SKILL.md「lis-skill-bus 可选联动」；未安装 bus 自动降级本机状态文件。
set -uo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for c in "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 "$(command -v python3 || true)"; do
  if [[ -n "$c" && -x "$c" ]]; then PY3="$c"; break; fi
done
if [[ -z "${PY3:-}" ]]; then echo "❌ 未找到 python3，无法执行 cad_statesync" >&2; exit 127; fi
exec "$PY3" "$HERE/cad_statesync.py" "$@"
