#!/usr/bin/env bash
# Zombie Session Cleaner - 清理长期不活跃的 session
# 用法: bash clean-zombies.sh [天数] [--dry-run]
# 默认清理 7 天前的 session

set -euo pipefail

DAYS="${1:-7}"
DRY_RUN="${2:-}"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

RED=$'\033[0;31m' GREEN=$'\033[0;32m' YELLOW=$'\033[1;33m' CYAN=$'\033[0;36m' BOLD=$'\033[1m' NC=$'\033[0m'

echo -e "${BOLD}🧟 僵尸 Session 清理${NC}"
echo "   阈值: ${DAYS} 天未活动"
echo ""

# 计算截止时间戳（毫秒）
CUTOFF=$(python3 -c "import time; print(int((time.time() - $DAYS * 86400) * 1000))")

sessions_json=$(openclaw sessions --json 2>/dev/null)
if [[ -z "$sessions_json" ]] || [[ "$sessions_json" == "null" ]]; then
    echo -e "${RED}无法获取 session 数据${NC}"
    exit 1
fi

total=$(echo "$sessions_json" | jq '.count')
zombies=$(echo "$sessions_json" | jq --argjson cutoff "$CUTOFF" \
    '[.sessions[] | select(.updatedAt < $cutoff)]')
zombie_count=$(echo "$zombies" | jq 'length')

echo -e "   总 session: ${total}"
echo -e "   僵尸 session: ${YELLOW}${zombie_count}${NC}"
echo ""

if [[ "$zombie_count" -eq 0 ]]; then
    echo -e "${GREEN}✓ 没有僵尸 session，一切正常${NC}"
    exit 0
fi

# 列出僵尸
echo -e "${CYAN}僵尸列表:${NC}"
echo "$zombies" | jq -r '.[] | "  \(.key) | \(.kind) | \(.totalTokens) tokens | 最后活动: \(.updatedAt)"'
echo ""

# 计算可节省的 token
total_tokens=$(echo "$zombies" | jq '[.[].totalTokens] | add')
echo -e "   可回收 token: ${YELLOW}${total_tokens}${NC}"
echo ""

if [[ "$DRY_RUN" == "--dry-run" ]]; then
    echo -e "${YELLOW}[预览模式] 未执行任何删除${NC}"
    echo "要实际执行: bash clean-zombies.sh $DAYS"
    exit 0
fi

echo -e "${BOLD}确认删除 ${zombie_count} 个僵尸 session? (y/N)${NC}"
read -r confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "已取消"
    exit 0
fi

# 备份 + 删除
deleted=0
echo "$zombies" | jq -r '.[] | "\(.sessionId)|\(.key)"' | while IFS='|' read -r sid key; do
    agent_id=$(echo "$key" | cut -d':' -f2)
    jsonl="$STATE_DIR/agents/$agent_id/sessions/$sid.jsonl"

    if [[ -f "$jsonl" ]]; then
        # 备份
        mkdir -p "$STATE_DIR/agents/$agent_id/sessions/.zombie-backup"
        mv "$jsonl" "$STATE_DIR/agents/$agent_id/sessions/.zombie-backup/${sid}.jsonl"
        echo -e "  ${GREEN}删除:${NC} $key"
        ((deleted++))
    fi
done

echo ""
echo -e "${GREEN}✅ 清理完成${NC}"
echo "   备份位置: $STATE_DIR/agents/*/sessions/.zombie-backup/"
echo "   恢复: 把备份文件移回 sessions/ 目录即可"
