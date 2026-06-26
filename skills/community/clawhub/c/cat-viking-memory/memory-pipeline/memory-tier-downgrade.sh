#!/bin/bash
#
# memory-tier-downgrade.sh
# 每天自动将记忆从 L0→L1→L2→L3→L4 降级
#
# 用法: memory-tier-downgrade.sh [agent_name]
# 示例: memory-tier-downgrade.sh maojingli
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

AGENT_NAME="${1:-maojingli}"
SV_WORKSPACE="$HOME/.openclaw/viking-$AGENT_NAME"

# 层级映射：当前层级 -> 降级后层级
# L0(0-1天) -> L1(2-7天)
# L1(2-7天) -> L2(8-30天)
# L2(8-30天) -> L3(30-90天)
# L3(30-90天) -> L4(90天+)

echo "=== 记忆自动降级 ==="
echo "Agent: $AGENT_NAME"
echo "时间: $(date)"
echo ""

# 检查 workspace 是否存在
if [ ! -d "$SV_WORKSPACE/agent/memories" ]; then
    echo -e "${RED}错误: Viking workspace 不存在: $SV_WORKSPACE${NC}"
    exit 1
fi

# 检查是否为高重要性记忆
is_important_memory() {
    local file="$1"
    local content=$(cat "$file" 2>/dev/null)
    
    # 跳过自动保存的记忆（让它们正常降级）
    if echo "$content" | grep -qE "auto_saved: *true"; then
        return 1
    fi
    
    # 检查 frontmatter 中的 importance: high
    if echo "$content" | grep -qE "^importance: *high"; then
        return 0
    fi
    
    # 检查标签中的"重要"、"高优先级"（排除自动保存）
    if echo "$content" | grep -qE "tags:.*\[.*重要|高优先级"; then
        return 0
    fi
    
    # 检查内容中的高权重关键词（排除自动保存）
    if echo "$content" | grep -qiE "紧急|严重|致命|关键决策|重要里程碑"; then
        return 0
    fi
    
    return 1
}

# 保护高重要性记忆（跳过降级）
protect_important_memory() {
    local file="$1"
    local workspace="$2"
    local filename=$(basename "$file")
    
    # 创建重要记忆保护区
    local important_dir="$workspace/agent/memories/important"
    mkdir -p "$important_dir"
    
    # 复制到保护区并标记
    local content=$(cat "$file")
    local protected_content=$(echo "$content" | sed "s/tier: L[0-9]/tier: IMPORTANT/" | sed "/^---$/a protected: true\nprotected_at: $(date +%Y-%m-%d)")
    
    echo "$protected_content" > "$important_dir/$filename"
    
    # 从原位置删除
    rm -f "$file"
    
    echo -e "${YELLOW}  🔒 高重要性记忆已保护: $filename → important/${NC}"
}

# 降级函数
downgrade_tier() {
    local source_dir="$1"
    local target_dir="$2"
    local source_tier="$3"
    local target_tier="$4"
    local workspace="$SV_WORKSPACE"
    
    if [ ! -d "$source_dir" ] || [ -z "$(ls -A "$source_dir" 2>/dev/null)" ]; then
        return
    fi
    
    echo -e "${YELLOW}降级: $source_tier -> $target_tier${NC}"
    
    # 确保目标目录存在
    mkdir -p "$target_dir"
    
    # 遍历源目录下的 .md 文件
    for file in "$source_dir"/*.md; do
        [ -e "$file" ] || continue
        
        filename=$(basename "$file")
        
        # 跳过非记忆文件
        [[ "$filename" == .* ]] && continue
        
        # 检查是否为高重要性记忆（L0->L1 时保护）
        if [ "$source_tier" = "L0" ] && is_important_memory "$file"; then
            protect_important_memory "$file" "$SV_WORKSPACE"
            continue
        fi
        
        # 读取内容，更新层级标识
        content=$(cat "$file")
        
        # 替换层级标识（支持多种格式）
        new_content="${content//\[$source_tier\]/[$target_tier]}"
        new_content="${new_content//层级: $source_tier/层级: $target_tier}"
        new_content="${new_content//tier: $source_tier/tier: $target_tier}"
        
        # 压缩内容（根据目标层级）
        case "$target_tier" in
            L1)
                # L1: 保留核心轮廓 ~70%
                # 保留标题、标签、背景、结果，去掉部分细节
                new_content=$(echo "$new_content" | awk '
                    /^## 背景/,/^## / { if (/^## 背景/ || /^## 结果/ || /^## 待办/ || /^- \[ \]/) print; else if (/^## /) { print; next } }
                    /^## 结果/,/^## / { if (/^## 结果/ || /^## 待办/ || /^- \[ \]/) print; else if (/^## /) { print; next } }
                    !/^## / { print }
                ' | head -30)
                ;;
            L2)
                # L2: 仅保留关键词 ~30%
                new_content=$(echo "$new_content" | awk '
                    /^# / { print }
                    /^## 结果/ { found=1 }
                    found { print }
                ' | head -10)
                ;;
            L3)
                # L3: 仅标签 ~10%
                new_content=$(echo "$new_content" | awk '
                    /^# / { print }
                    /^\*\*/ { print }
                ')
                ;;
            L4)
                # L4: 仅标题
                new_content=$(echo "$new_content" | head -1)
                ;;
        esac
        
        # 写入目标目录
        target_file="$target_dir/$filename"
        echo "$new_content" > "$target_file"
        
        # 删除源文件（仅当 source_dir != target_dir 时）
        if [ "$source_dir" != "$target_dir" ]; then
            rm -f "$file"
        fi
        
        echo "  ✅ $filename -> $target_tier"
    done
}

# 执行降级
# L0 -> L1 (hot -> hot)
downgrade_tier "$SV_WORKSPACE/agent/memories/hot" "$SV_WORKSPACE/agent/memories/hot" "L0" "L1"

# L1 -> L2 (hot -> warm)
downgrade_tier "$SV_WORKSPACE/agent/memories/hot" "$SV_WORKSPACE/agent/memories/warm" "L1" "L2"

# L2 -> L3 (warm -> cold)
downgrade_tier "$SV_WORKSPACE/agent/memories/warm" "$SV_WORKSPACE/agent/memories/cold" "L2" "L3"

# L3 -> L4 (cold -> archive)
downgrade_tier "$SV_WORKSPACE/agent/memories/cold" "$SV_WORKSPACE/agent/memories/archive" "L3" "L4"

echo ""
echo -e "${GREEN}✅ 降级完成${NC}"

# ===== 重要记忆压缩 =====
compress_important_memories() {
    local workspace="$1"
    local important_dir="$workspace/agent/memories/important"
    
    if [ ! -d "$important_dir" ] || [ -z "$(ls -A "$important_dir" 2>/dev/null)" ]; then
        return
    fi
    
    echo ""
    echo -e "${YELLOW}压缩重要记忆...${NC}"
    
    for file in "$important_dir"/*.md; do
        [ -e "$file" ] || continue
        
        filename=$(basename "$file")
        [[ "$filename" == .* ]] && continue
        
        # 读取内容
        content=$(cat "$file")
        
        # 提取关键信息
        local theme=$(echo "$content" | grep "^# " | head -1 | sed 's/^# //')
        local decisions=$(echo "$content" | grep "^## 关键决策" -A 10 | grep "^- " | head -5)
        local todos=$(echo "$content" | grep "^## 待办任务" -A 10 | grep "^- \[ \]" | head -5)
        local tags=$(echo "$content" | grep "^tags:" | sed 's/^tags: \[\(.*\)\].*/\1/')
        local importance=$(echo "$content" | grep "^importance:" | sed 's/^importance: //')
        local date=$(echo "$content" | grep "^date:" | sed 's/^date: //')
        
        # 创建压缩版本
        local compressed_content="# ${theme:-压缩摘要}\n\n"
        compressed_content+="**日期:** ${date:-未知}\n"
        compressed_content+="**重要性:** ${importance:-high}\n\n"
        
        if [ -n "$decisions" ]; then
            compressed_content+="## 关键决策\n$decisions\n\n"
        fi
        
        if [ -n "$todos" ]; then
            compressed_content+="## 待办任务\n$todos\n\n"
        fi
        
        compressed_content+="---\n"
        compressed_content+="*压缩时间: $(date +%Y-%m-%d)*\n"
        compressed_content+="*原始标签: [${tags}]*\n"
        
        # 创建压缩版本（作为历史记录）
        local compressed_file="$important_dir/.compressed/${filename%.md}_$(date +%Y%m).md"
        mkdir -p "$important_dir/.compressed"
        echo "$compressed_content" > "$compressed_file"
        
        # 更新原文件，标记已压缩
        local updated_content=$(echo "$content" | sed "/^---$/a compressed: true\ncompressed_at: $(date +%Y-%m-%d)\ncompressed_version: $compressed_file")
        echo "$updated_content" > "$file"
        
        echo -e "${GREEN}  ✅ 已压缩: $filename${NC}"
    done
}

# 执行重要记忆压缩
compress_important_memories "$SV_WORKSPACE"
