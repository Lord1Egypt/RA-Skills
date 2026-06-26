#!/bin/bash
# 脑筋急转弯 Skill 入口脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误：需要 Python 3"
    exit 1
fi

# 运行 Python 脚本
python3 invoke.py "$@"
