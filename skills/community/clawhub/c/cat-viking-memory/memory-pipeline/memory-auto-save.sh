#!/bin/bash
#
# memory-auto-save.sh
# 自动记忆保存机制 - 三层触发过滤
#

set -e

AGENT_NAME="${AGENT_NAME:-maojingli}"
SV_WORKSPACE="$HOME/.openclaw/viking-$AGENT_NAME"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ===== 触发机制 =====

# 显式标记（触发保存 + 标记重要）
# 使用更灵活的模式，支持"保存记忆"、"记一下"等变体
EXPLICIT_MARKERS="保存.*记忆|记一下|存一下|记住.*这个|记录这个"

# 时间窗口：30分钟内相同话题不重复存储
TIME_WINDOW=1800  # 30分钟 = 1800秒

# ===== 辅助函数 =====

# 检查显式标记
check_explicit() {
    local content="$1"
    echo "$content" | grep -qE "$EXPLICIT_MARKERS"
}

# 检查时间窗口（去重）
check_time_window() {
    local content="$1"
    local workspace="${2:-$SV_WORKSPACE}"
    local key_content=$(echo "$content" | head -c 50 | tr -s ' ')
    
    # 检查 hot 目录中最近30分钟的记忆
    if [ -d "$workspace/agent/memories/hot" ]; then
        local now=$(date +%s)
        for file in "$workspace/agent/memories/hot"/*.md; do
            [ -f "$file" ] || continue
            [[ "$(basename "$file")" == .* ]] && continue
            
            # 检查文件修改时间
            local file_time=$(stat -c %Y "$file" 2>/dev/null || echo "$now")
            local time_diff=$((now - file_time))
            
            # 在时间窗口内且内容相似
            if [ "$time_diff" -lt "$TIME_WINDOW" ]; then
                local file_content=$(head -c 50 "$file" | tr -s ' ')
                if [ "$key_content" = "$file_content" ]; then
                    echo "时间窗口内重复: $(basename "$file")"
                    return 0  # 是重复
                fi
            fi
        done
    fi
    return 1
}

# 判断重要程度（决定是否保护）
# 简化逻辑：只有显式标记才保护，其他默认保存到 hot(L0) 正常降级
get_importance_level() {
    local content="$1"
    
    # 只有显式标记才是 high
    if check_explicit "$content"; then
        echo "high"
        return
    fi
    
    # 默认 - low（保存到 hot，会正常降级）
    echo "low"
}

# ===== 存储函数 =====

# 去重：检查标题是否已存在
is_duplicate() {
    local title="$1"
    local workspace="${2:-$SV_WORKSPACE}"
    
    norm_title=$(echo "$title" | tr -d '\n' | tr -s ' ')
    
    if [ -d "$workspace/agent/memories/hot" ]; then
        for file in "$workspace/agent/memories/hot"/*.md; do
            [ -f "$file" ] || continue
            [[ "$(basename "$file")" == .* ]] && continue
            
            filename=$(basename "$file" .md | sed 's/^[0-9-]*_*[0-9]*_//')
            
            if echo "$filename" | grep -qF "$norm_title"; then
                echo "重复: $(basename "$file")"
                return 0
            fi
        done
    fi
    return 1
}

# 自动保存（带去重）
auto_save_session() {
    local summary="$1"
    local title="${2:-会话摘要}"
    
    [ -z "$summary" ] && return 1
    
    # 时间窗口检查
    if check_time_window "$summary" "$SV_WORKSPACE"; then
        echo -e "${YELLOW}跳过（30分钟内已存储相同内容）${NC}"
        return 1
    fi
    
    # 标题去重
    if is_duplicate "$title" "$SV_WORKSPACE"; then
        echo -e "${YELLOW}跳过（已有相同标题记忆）${NC}"
        return 1
    fi
    
    # 获取重要程度
    local importance=$(get_importance_level "$summary")
    echo -e "${YELLOW}保存记忆: $title (重要性: $importance)${NC}"
    
    # 默认保存到 hot (L0)，重要则保护
    if [ "$importance" = "high" ]; then
        ~/.openclaw/skills/memory-pipeline/scripts/memory-pipeline mp_store \
            --content "$summary" --title "$title" --tags "自动保存,重要" --tier L0 --important
    else
        ~/.openclaw/skills/memory-pipeline/scripts/memory-pipeline mp_store \
            --content "$summary" --title "$title" --tags "自动保存" --tier L0
    fi
}

# ===== 主入口 =====
case "$1" in
    save)
        auto_save_session "$2" "$3"
        ;;
    check)
        if should_auto_save "$2"; then
            echo "需要保存"
            should_auto_save "$2"
        else
            echo "不需要保存"
        fi
        ;;
    test)
        echo "=== 触发测试（简化版）==="
        echo "显式标记: $EXPLICIT_MARKERS"
        echo "默认保存到 hot (L0)，只有显式标记才加 --important"
        echo ""
        
        # 测试显式标记触发
        echo "测试1（显式-保存记忆）:"
        check_explicit "请保存这个记忆" && echo "✅ 触发" || echo "❌ 不触发"
        
        echo "测试2（显式-记一下）:"
        check_explicit "帮我记一下这个" && echo "✅ 触发" || echo "❌ 不触发"
        
        echo "测试3（显式-存一下）:"
        check_explicit "存一下这个地址" && echo "✅ 触发" || echo "❌ 不触发"
        
        echo "测试4（显式-记住这个）:"
        check_explicit "记住这个密码" && echo "✅ 触发" || echo "❌ 不触发"
        
        echo ""
        echo "测试5（普通内容-默认保存到hot）:"
        check_explicit "今天天气不错" && echo "✅ 触发（重要）" || echo "❌ 不触发（但会默认保存到hot）"
        
        echo "测试6（普通内容-项目交付）:"
        check_explicit "完成了项目交付" && echo "✅ 触发（重要）" || echo "❌ 不触发（但会默认保存到hot）"
        ;;
    *)
        echo "用法: $0 save <内容> [标题] | check <内容> | test"
        ;;
esac
