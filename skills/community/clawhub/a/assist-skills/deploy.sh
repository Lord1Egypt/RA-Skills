#!/usr/bin/env bash
#
# assist-skills 参考资料包一键部署入口（macOS / Linux / WSL / Git Bash）。
#
# 本文件只负责定位技能包并转发给 scripts/deploy.sh，参数与之一致：
#
#   bash deploy.sh --target ~/my-project
#   bash deploy.sh -t . --dry-run
#
# 想更短，把下面一行加到 ~/.bashrc 或 ~/.zshrc，之后直接用 ai-deploy：
#
#   alias ai-deploy="bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/scripts/deploy.sh" "$@"
