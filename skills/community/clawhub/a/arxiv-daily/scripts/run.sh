#!/bin/bash
# run.sh - arxiv文章获取启动脚本
#
# 用法: ./run.sh <领域> <保存路径> [日期]
# 示例: ./run.sh cs.CV ./output 2026-03-19
#       ./run.sh cs.CV ./output        # 使用当天日期

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <领域> <保存路径> [日期]"
    echo "  领域:     arxiv领域代码，如 cs.CV, cs.AI, cs.CL 等"
    echo "  保存路径: 输出文件保存的目录"
    echo "  日期:     可选，格式 YYYY-MM-DD，默认为当天"
    echo ""
    echo "示例:"
    echo "  $0 cs.CV ./output              # 获取当天cs.CV文章"
    echo "  $0 cs.AI ./data 2026-03-19     # 获取2026-03-19的cs.AI文章"
    exit 1
fi

CATEGORY=$1
SAVE_PATH=$2
DATE_ARG=${3:-}  # 如果$3未定义则为空字符串

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FETCH_SCRIPT="$SCRIPT_DIR/fetch.py"

# 检查fetch.py是否存在
if [ ! -f "$FETCH_SCRIPT" ]; then
    echo "错误: 找不到 fetch.py 脚本: $FETCH_SCRIPT"
    exit 1
fi

# 检查Python3是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请确保已安装Python 3"
    exit 1
fi

# 检查依赖库
python3 -c "import requests, bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装必要的依赖库..."
    pip3 install requests beautifulsoup4 -q
fi

# 创建保存目录（如果不存在）
mkdir -p "$SAVE_PATH"

# 执行fetch.py
echo "=========================================="
echo "启动arxiv文章获取"
echo "领域: $CATEGORY"
echo "保存路径: $SAVE_PATH"
if [ -n "$DATE_ARG" ]; then
    echo "日期: $DATE_ARG"
else
    echo "日期: 当天 ($(date +%Y-%m-%d))"
fi
echo "=========================================="

if [ -n "$DATE_ARG" ]; then
    python3 "$FETCH_SCRIPT" "$CATEGORY" "$SAVE_PATH" "$DATE_ARG"
else
    python3 "$FETCH_SCRIPT" "$CATEGORY" "$SAVE_PATH"
fi

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "=========================================="
    echo "执行成功！"
    echo "=========================================="
else
    echo "=========================================="
    echo "执行失败，请检查错误信息"
    echo "=========================================="
    exit 1
fi
