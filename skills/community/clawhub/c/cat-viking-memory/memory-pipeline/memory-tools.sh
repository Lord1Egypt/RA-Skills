#!/bin/bash
#
# memory-tools.sh
# 工具/技能记忆管理
# 功能：自动记录技能、查询可用工具
#

AGENT_NAME="${AGENT_NAME:-maojingli}"
SV_WORKSPACE="$HOME/.openclaw/viking-$AGENT_NAME"

# 工具注册
register_tool() {
    local tool_name="$1"
    local tool_desc="$2"
    local tool_path="$3"
    
    local date_str=$(date +%Y-%m-%d)
    local timestamp=$(date +%Y%m%d%H%M%S)
    
    # 工具存储路径
    local tools_dir="$SV_WORKSPACE/agent/resources/tools"
    mkdir -p "$tools_dir"
    
    local tool_file="$tools_dir/${tool_name}.md"
    
    cat > "$tool_file" << EOF
---
id: tool_${timestamp}
name: $tool_name
description: $tool_desc
path: $tool_path
loaded_at: $(date -Iseconds)
use_count: 1
status: active
---

# 工具: $tool_name

- 描述: $tool_desc
- 路径: $tool_path
- 加载时间: $(date)
- 使用次数: 1
- 状态: 活跃
EOF
    
    echo "✅ 已注册工具: $tool_name"
}

# 更新工具使用次数
update_tool_usage() {
    local tool_name="$1"
    local tools_dir="$SV_WORKSPACE/agent/resources/tools"
    local tool_file="$tools_dir/${tool_name}.md"
    
    if [ -f "$tool_file" ]; then
        # 更新使用次数
        use_count=$(grep "use_count:" "$tool_file" | awk '{print $2}')
        use_count=$((use_count + 1))
        sed -i "s/use_count: $((use_count - 1))/use_count: $use_count/" "$tool_file"
        
        # 更新最后使用时间
        sed -i "s/last_used:.*/last_used: $(date -Iseconds)/" "$tool_file"
        
        echo "✅ 更新 $tool_name 使用次数: $use_count"
    fi
}

# 列出所有工具
list_tools() {
    local tools_dir="$SV_WORKSPACE/agent/resources/tools"
    
    echo "=== 可用工具 ==="
    
    if [ ! -d "$tools_dir" ]; then
        echo "暂无工具记录"
        return
    fi
    
    for file in "$tools_dir"/*.md; do
        [ -f "$file" ] || continue
        [[ "$(basename "$file")" == .* ]] && continue
        
        name=$(basename "$file" .md)
        desc=$(grep "description:" "$file" | head -1 | sed 's/description: //')
        status=$(grep "status:" "$file" | head -1 | sed 's/status: //')
        
        echo "- $name: $desc [$status]"
    done
}

# 自动记录当前会话的技能
auto_record_skills() {
    echo "=== 自动记录技能 ==="
    
    # 尝试获取技能列表
    if command -v openclaw &>/dev/null; then
        skills=$(openclaw skills list 2>/dev/null || echo "")
        
        if [ -n "$skills" ]; then
            echo "$skills" | while read line; do
                tool_name=$(echo "$line" | awk '{print $1}')
                if [ -n "$tool_name" ]; then
                    register_tool "$tool_name" "自动记录" ""
                fi
            done
        fi
    else
        echo "⚠️ openclaw 命令不可用"
    fi
}

case "$1" in
    register)
        register_tool "$2" "$3" "$4"
        ;;
    update)
        update_tool_usage "$2"
        ;;
    list)
        list_tools
        ;;
    auto)
        auto_record_skills
        ;;
    *)
        echo "用法:"
        echo "  $0 register <名称> <描述> <路径>"
        echo "  $0 update <名称>"
        echo "  $0 list"
        echo "  $0 auto"
        ;;
esac
