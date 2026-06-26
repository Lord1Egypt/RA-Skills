#!/bin/bash
# AMK音视频处理工具集启动脚本
# 兼容各种执行路径
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/scripts" || exit 1
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
python main.py "$@"