#!/bin/bash
# 随机选择一个设计风格

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESIGN_MD_DIR="$SCRIPT_DIR/../design-md"

# 获取所有风格目录
styles=($(ls -d "$DESIGN_MD_DIR"/*/ 2>/dev/null | xargs -n1 basename))

if [ ${#styles[@]} -eq 0 ]; then
    echo "错误：未找到任何设计风格"
    exit 1
fi

# 随机选择一个
random_index=$((RANDOM % ${#styles[@]}))
selected_style="${styles[$random_index]}"

# 输出结果
echo "$selected_style"
