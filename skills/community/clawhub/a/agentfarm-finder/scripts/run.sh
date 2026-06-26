#!/bin/bash
# Agentfarm-Finder 执行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Agentfarm-Finder ==="
echo "时间: $(date)"
echo ""

# 运行搜索
echo "1/2 执行搜索..."
cd "$SKILL_DIR"
bash agentfarm.sh

# 运行筛选
echo ""
echo "2/2 执行筛选..."
python3 filter_projects.py

# 汇报结果
echo ""
echo "=== 执行完成 ==="

# 显示结果摘要
if [ -f "$SKILL_DIR/output/results_$(date +%Y-%m-%d)_projects.csv" ]; then
    count=$(wc -l < "$SKILL_DIR/output/results_$(date +%Y-%m-%d)_projects.csv")
    echo "项目发现: $((count - 1)) 条"
    echo ""
    echo "前5条:"
    tail -n +2 "$SKILL_DIR/output/results_$(date +%Y-%m-%d)_projects.csv" | head -5 | while read line; do
        IFS=',' read -r热度 作者 用户名 内容 链接 <<< "$line"
        echo "- @$用户名: ${内容:0:50}..."
    done
fi
