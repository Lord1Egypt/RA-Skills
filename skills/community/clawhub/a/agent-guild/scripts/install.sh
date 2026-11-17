#!/usr/bin/env bash
# Agent Guild 安装器（macOS / Linux / WSL / Git Bash）。
# 下载并检查同一固定提交的 install.sh 和 ag.py 后执行：bash install.sh
# 不接受流式执行；不会下载或执行可变 main 分支代码。
# Python 标准库统一校验固定 release ZIP 后安装，保留用户数据。

set -eu

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -f "$SCRIPT_DIR/ag.py" ]; then
  printf '%s\n' '缺少同目录 ag.py；请先下载并检查同一固定提交的安装脚本与 ag.py。' >&2
  exit 1
fi
PYTHON="${AGENT_GUILD_PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  printf '%s\n' '需要 Python 3.9+；可通过 AGENT_GUILD_PYTHON 指定可执行文件。' >&2
  exit 1
fi
VERSION="${AGENT_GUILD_VERSION:-4.0.0}"
export PYTHONDONTWRITEBYTECODE=1
"$PYTHON" -c 'import sys; sys.version_info >= (3, 9) or sys.exit("需要 Python 3.9+"); sys.path.insert(0, sys.argv[1]); import ag; sys.exit(ag._install_release(sys.argv[2]))' "$SCRIPT_DIR" "$VERSION" > /dev/null

printf '\n%s\n\n%s\n\n' '  请复制以下内容发给你的 AI 助手：' '  Read ~/.agent-guild/ONBOARDING.md'
