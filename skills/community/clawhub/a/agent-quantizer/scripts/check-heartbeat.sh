#!/usr/bin/env bash
# Heartbeat Checker - 检查 heartbeat 是否在空转
# 用法: bash check-heartbeat.sh

set -euo pipefail

G=$'\033[0;32m' Y=$'\033[1;33m' R=$'\033[0;31m' B=$'\033[1m' C=$'\033[0;36m' N=$'\033[0m'

echo -e "${B}💓 Heartbeat 健康检查${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查所有 workspace 下的 HEARTBEAT.md
checked=0
problems=0

for ws in "$HOME/.openclaw/workspace"*; do
    ws_name=$(basename "$ws")
    hb="$ws/HEARTBEAT.md"

    echo -e "\n${C}${ws_name}:${NC}"

    if [[ ! -f "$hb" ]]; then
        echo -e "  ${Y}⚠️  没有 HEARTBEAT.md${NC}"
        echo "  → 如果不需要定期任务，这是正常的"
        continue
    fi

    # 检查内容
    content=$(grep -v '^#' "$hb" | grep -v '^$' | wc -l | tr -d ' ')

    if [[ "$content" -eq 0 ]]; then
        echo -e "  ${R}🚨 空转！HEARTBEAT.md 只有注释或空行${NC}"
        echo "  → 每次心跳都会白烧一轮 API"
        echo "  → 建议: 删除文件或写入实际任务"
        ((problems++))
    else
        echo -e "  ${G}✓ 有 ${content} 个任务${NC}"
        grep -v '^#' "$hb" | grep -v '^$' | head -5 | while read -r line; do
            echo "    - $line"
        done
    fi
    ((checked++))
done

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "检查了 ${checked} 个 workspace"

if [[ $problems -gt 0 ]]; then
    echo -e "${R}发现 ${problems} 个空转的 HEARTBEAT${NC}"
    echo ""
    echo "修复方法:"
    echo "  1. 不需要定期任务: 删除 HEARTBEAT.md"
    echo "  2. 需要定期任务: 在 HEARTBEAT.md 里写具体内容"
    echo ""
    echo "常见定期任务:"
    echo "  - 检查新邮件"
    echo "  - 查看日历"
    echo "  - 检查服务器状态"
    echo "  - 同步文件"
else
    echo -e "${G}✓ 所有 Heartbeat 都正常${NC}"
fi

# 检查 config 中的 heartbeat 间隔
echo -e "\n${B}配置检查:${NC}"
if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
    interval=$(grep -o '"heartbeatInterval"[^,}]*' "$HOME/.openclaw/openclaw.json" 2>/dev/null || echo "未设置(使用默认)")
    echo "  心跳间隔: $interval"
fi
