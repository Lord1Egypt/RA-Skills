#!/bin/bash
#
# memory-tier-cron.sh
# 每天自动执行所有 Agent 和全局记忆的降级
# 由 cron 每天凌晨 3 点调用
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/memory-tier-downgrade-$(date +%Y%m%d).log"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== 记忆层级自动处理 Cron ==="
echo "时间: $(date)"
echo "今日: $TODAY"
echo "昨日: $YESTERDAY"
echo ""

# Agent 列表
AGENTS="maojingli maoxiami maogongtou maozhuli global"

# ===== 智能提取昨日会话摘要 =====
auto_save_yesterday() {
    local agent="$1"
    local workspace="$2"
    
    echo -e "${YELLOW}>>> 智能提取昨日记忆: $agent${NC}"
    
    # 查找昨日会话记录
    local session_dir="$HOME/.openclaw/agents/$agent/sessions"
    local yesterday_session=""
    
    if [ -d "$session_dir" ]; then
        yesterday_session=$(find "$session_dir" -name "*.jsonl" -mtime -1 -type f 2>/dev/null | head -1)
    fi
    
    local hot_dir="$workspace/agent/memories/hot"
    mkdir -p "$hot_dir"
    local filename="${YESTERDAY}_$(date +%H%M%S)_auto_save.md"
    
    if [ -n "$yesterday_session" ] && [ -f "$yesterday_session" ]; then
        echo "  找到会话: $yesterday_session"
        echo "  调用 LLM 智能提取..."
        
        # 调用智能提取脚本
        local extracted
        if extracted=$("$SCRIPT_DIR/memory-extract-summary.sh" "$agent" "$yesterday_session" "$YESTERDAY" 2>/dev/null); then
            # 解析提取结果
            local theme=$(echo "$extracted" | grep "^主题:" | sed 's/^主题: //')
            local decisions=$(echo "$extracted" | grep "^决策:" -A 10 | grep "^- " | head -5)
            local todos=$(echo "$extracted" | grep "^待办:" -A 10 | grep "^- \[ \]" | head -10)
            local importance=$(echo "$extracted" | grep "^重要性:" | sed 's/^重要性: //')
            
            [ -z "$importance" ] && importance="medium"
            
            local tags="自动保存,${YESTERDAY},智能提取"
            [ "$importance" = "high" ] && tags="自动保存,${YESTERDAY},智能提取,重要"
            
            # 构建摘要文档
            cat > "$hot_dir/$filename" << EOF
---
title: "${theme:-$YESTERDAY 每日摘要}"
date: ${YESTERDAY}
tags: [${tags}]
importance: ${importance}
tier: L0
auto_saved: true
extraction_method: llm
---

# ${theme:-$YESTERDAY 会话摘要}

## 关键决策
${decisions:-"- 无明确决策"}

## 待办任务
${todos:-"- [ ] 检查昨日任务完成情况"}

## 原始提取信息
\`\`\`
${extracted}
\`\`\`
EOF
            
            echo -e "${GREEN}  ✅ 智能提取完成: $hot_dir/$filename${NC}"
            echo "     主题: ${theme:-未提取}"
            echo "     重要性: $importance"
        else
            echo -e "${YELLOW}  ⚠️ 智能提取失败，使用基础模式${NC}"
            # 回退到基础保存
            basic_auto_save "$agent" "$workspace"
        fi
    else
        echo "  未找到昨日会话"
        basic_auto_save "$agent" "$workspace"
    fi
}

# 基础自动保存（回退模式）
basic_auto_save() {
    local agent="$1"
    local workspace="$2"
    
    local hot_dir="$workspace/agent/memories/hot"
    mkdir -p "$hot_dir"
    local filename="${YESTERDAY}_$(date +%H%M%S)_basic_save.md"
    
    cat > "$hot_dir/$filename" << EOF
---
title: "${YESTERDAY} 基础摘要"
date: ${YESTERDAY}
tags: [自动保存,${YESTERDAY},基础模式]
importance: low
tier: L0
auto_saved: true
extraction_method: basic
---

# ${YESTERDAY} 会话摘要

- 未找到活跃会话记录或未启用智能提取

## 待办任务
- [ ] 检查昨日任务完成情况
- [ ] 继续推进进行中的项目
EOF
    
    echo -e "${GREEN}  ✅ 基础保存完成: $hot_dir/$filename${NC}"
}

# ===== 主处理流程 =====

for agent in $AGENTS; do
    echo ">>> 处理: $agent"
    
    if [ "$agent" = "global" ]; then
        export SV_WORKSPACE="$HOME/.openclaw/viking-global"
        # global 是全局共享空间，不自动生成会话记忆，只执行降级
        echo "  (跳过自动保存，global 只保留手动写入的记忆)"
    else
        export SV_WORKSPACE="$HOME/.openclaw/viking-$agent"
        # 步骤1: 自动保存昨日会话摘要（仅对 Agent）
        auto_save_yesterday "$agent" "$SV_WORKSPACE"
        # 注意：创建后跳过降级，让新记忆在 hot 保留 1 天
        echo "  (新记忆保留在 hot，稍后自动降级)"
    fi
    
    # 步骤2: 执行降级（仅对 global）
    if [ "$agent" = "global" ]; then
        "$SCRIPT_DIR/memory-tier-downgrade.sh" "$agent" || echo "  ⚠️ $agent 降级完成"
    fi
    
    echo ""
done

echo "=== 全部完成 ==="

# ===== 构建向量索引 =====
echo ">>> 构建向量索引..."
export PATH="$HOME/.openclaw/skills/simple-viking/scripts:$PATH"
if command -v sv &> /dev/null; then
    sv build-index "$HOME/.openclaw/viking-global" 100
    echo "  ✅ 全局向量索引构建完成"
    
    # 为每个 Agent 构建索引
    for agent in maojingli maoxiami maogongtou maozhuli; do
        export SV_WORKSPACE="$HOME/.openclaw/viking-$agent"
        sv build-index "$SV_WORKSPACE" 100
        echo "  ✅ $agent 向量索引构建完成"
    done
else
    echo "  ⚠️ sv 命令未找到，跳过向量索引构建"
fi

echo "=== 所有任务完成 ==="
