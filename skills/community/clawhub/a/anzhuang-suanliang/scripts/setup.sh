#!/usr/bin/env bash
# anzhuang-suanliang 安装/自检：显式依赖底座 cad-file-reader（未装自动安装，已装复用）。
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SkillHub 分发包（zip）会丢失可执行位：首次运行时幂等自愈，避免 permission denied
find "$SKILL_DIR/scripts" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x -exec chmod +x {} + 2>/dev/null || true
echo "[anzhuang-suanliang] 检测显式依赖底座 cad-file-reader……"
bash "$SKILL_DIR/scripts/ensure_base.sh"
echo "[anzhuang-suanliang] 安装自检完成。"
