#!/usr/bin/env bash
# 一站式安装（跨平台薄转发到 scripts/setup.py，支持 --dry-run/--force/--quiet）。
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SkillHub 分发包（zip）会丢失可执行位：首次运行时幂等自愈，避免 permission denied
find "$SKILL_DIR/scripts" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x -exec chmod +x {} + 2>/dev/null || true

PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then PYTHON_BIN="${candidate}"; break; fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ 未找到 python3，需要 Python 3.10+" >&2
  exit 1
fi

exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/setup.py" "$@"
