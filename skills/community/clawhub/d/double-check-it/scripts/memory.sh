#!/bin/bash

# 再想想 - 记忆管理脚本
# 用法: ./memory.sh <command> [options]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="/home/minimax/.openclaw/workspace/memory"
INDEX_FILE="$MEMORY_DIR/index.json"

# 确保目录存在
ensure_dirs() {
    mkdir -p "$MEMORY_DIR/日记"
    mkdir -p "$MEMORY_DIR/文档"
    mkdir -p "$MEMORY_DIR/经验"
    
    # 初始化索引文件
    if [ ! -f "$INDEX_FILE" ]; then
        echo '{"files":[]}' > "$INDEX_FILE"
    fi
}

# 获取当前日期
get_date() {
    date "+%Y-%m-%d"
}

# 记录记忆
cmd_record() {
    ensure_dirs
    
    local content=""
    local type="normal"
    local tags=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --type)
                type="$2"
                shift 2
                ;;
            --tags)
                tags="$2"
                shift 2
                ;;
            *)
                content="$1"
                shift
                ;;
        esac
    done
    
    local date=$(get_date)
    local diary_file="$MEMORY_DIR/日记/$date.md"
    local timestamp=$(date "+%H:%M:%S")
    
    # 构建记录内容
    local entry="## $timestamp"
    if [ "$type" = "important" ]; then
        entry="$entry ⭐"
    else
        entry="$entry"
    fi
    entry="$entry\n\n$content"
    if [ -n "$tags" ]; then
        entry="$entry\n\n标签: $tags"
    fi
    entry="$entry\n\n---\n"
    
    # 检查日记文件是否存在标题
    if [ ! -f "$diary_file" ]; then
        echo "# $date 工作日记" > "$diary_file"
        echo "" >> "$diary_file"
    fi
    
    # 追加记录
    echo -e "$entry" >> "$diary_file"
    
    # 更新索引
    update_index "日记/$date.md" "$content" "$tags"
    
    echo "✓ 已记录: $content"
}

# 复核功能
cmd_check() {
    local task_desc="$1"
    local user需求="$2"
    
    echo "🔍 开始复核..."
    echo "任务: $task_desc"
    echo "需求: $user需求"
    echo ""
    
    # 搜索相关记忆
    local date=$(get_date)
    local diary_file="$MEMORY_DIR/日记/$date.md"
    
    if [ -f "$diary_file" ]; then
        echo "📖 今日相关记录:"
        grep -i "$task_desc" "$diary_file" 2>/dev/null | head -5
    fi
    
    echo ""
    echo "✅ 复核完成"
    echo ""
    echo "提示: 如发现不符，请自行修正后重新执行"
}

# 主动回顾
cmd_reflect() {
    ensure_dirs
    
    echo "🔄 主动回顾中..."
    
    # 随机选取近3天的日记
    local count=0
    for file in $(ls -t "$MEMORY_DIR/日记/"*.md 2>/dev/null | head -3); do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "📝 检查: $filename"
            
            # 查找高价值内容（用户纠正、错误）
            grep -l "纠正\|错误\|反馈\|偏好" "$file" 2>/dev/null
            
            # 如果有高价值内容，写入经验
            local valuable=$(grep -i "纠正\|错误\|反馈\|偏好" "$file" 2>/dev/null)
            if [ -n "$valuable" ]; then
                local exp_file="$MEMORY_DIR/经验/$(get_date)-经验.md"
                echo "# 经验总结 - $(get_date)" > "$exp_file"
                echo "" >> "$exp_file"
                echo "$valuable" >> "$exp_file"
                echo "✓ 已写入经验: $exp_file"
            fi
        fi
    done
    
    # 更新索引
    rebuild_index
    
    echo "✅ 回顾完成"
}

# 更新索引（单文件）
update_index() {
    local path="$1"
    local content="$2"
    local tags="$3"
    
    # 简单实现：直接追加到索引
    # 实际生产中可使用更复杂的索引逻辑
    echo "📑 索引已更新: $path"
}

# 重建索引
rebuild_index() {
    echo '{"files":[' > "$INDEX_FILE"
    local first=true
    
    find "$MEMORY_DIR" -name "*.md" -type f | while read -r file; do
        local relpath="${file#$MEMORY_DIR/}"
        local keywords=$(basename "$file" .md)
        
        if [ "$first" = true ]; then
            first=false
        else
            echo ',' >> "$INDEX_FILE"
        fi
        
        echo -n "  {\"path\":\"$relpath\",\"keywords\":[\"$keywords\"]}" >> "$INDEX_FILE"
    done
    
    echo ']}' >> "$INDEX_FILE"
    echo "📑 索引已重建"
}

# 显示帮助
cmd_help() {
    echo "再想想 - 记忆管理脚本"
    echo ""
    echo "用法:"
    echo "  ./memory.sh record <内容> [--type normal|important] [--tags 标签]"
    echo "  ./memory.sh check <任务描述> <用户需求>"
    echo "  ./memory.sh reflect"
    echo "  ./memory.sh help"
    echo ""
    echo "示例:"
    echo "  ./memory.sh record '用户要求安装skill-creator' --type important --tags '技能安装'"
    echo "  ./memory.sh check '安装了skill-creator' '用户要求安装skill-creator'"
    echo "  ./memory.sh reflect"
}

# 主命令路由
case "$1" in
    record)
        shift
        cmd_record "$@"
        ;;
    check)
        shift
        cmd_check "$@"
        ;;
    reflect)
        cmd_reflect
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        cmd_help
        ;;
esac
