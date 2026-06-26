#!/bin/bash
# Preferences Expiry Checker - v1.0
# 检查并清理过期的短期/中期偏好
# 运行方式：每天一次 via crontab

set -e

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/preferences-expiry.log}"
EXPIRY_TRACKER="$WORKSPACE/memory/preferences-expiry.json"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$WORKSPACE/memory"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 初始化过期追踪文件
init_expiry_tracker() {
    if [ ! -f "$EXPIRY_TRACKER" ]; then
        echo '{}' > "$EXPIRY_TRACKER"
    fi
}

# 获取今天日期（天数，用于计算）
get_day_number() {
    date +%j  # 一年中的第几天
}

# 计算天数差（v1.1: 使用 Unix timestamp 避免跨年 bug）
days_diff() {
    local date1=$1
    local date2=$2
    local d1=$(date -d "$date1" +%s 2>/dev/null || echo "0")
    local d2=$(date -d "$date2" +%s 2>/dev/null || echo "0")
    if [ "$d1" -eq 0 ] || [ "$d2" -eq 0 ]; then
        echo "0"
        return
    fi
    echo $(( (d2 - d1) / 86400 ))
}

# 检查偏好表格中的条目
check_preference_entries() {
    log "📋 Checking preference entries..."
    
    # 读取偏好表格
    local in_table=false
    local expired_count=0
    local today=$(date '+%Y-%m-%d')
    local today_day=$(date +%s)
    
    # 创建临时文件
    local temp_file=$(mktemp)
    local tracker_temp=$(mktemp)
    
    # 读取现有追踪数据
    if [ -f "$EXPIRY_TRACKER" ]; then
        cat "$EXPIRY_TRACKER" > "$tracker_temp"
    else
        echo '{}' > "$tracker_temp"
    fi
    
    # 扫描 MEMORY.md 的偏好表格
    while IFS= read -r line; do
        # 检测表格开始
        if echo "$line" | grep -q "^| 日期 | 类型 | 偏好"; then
            in_table=true
            continue
        fi
        
        # 检测表格结束（空行或新章节）
        if $in_table && [ -z "$line" ]; then
            in_table=false
            continue
        fi
        
        # 处理表格行
        if $in_table && echo "$line" | grep -q "^|"; then
            # 解析行：| 日期 | 类型 | 偏好 | 来源 |
            local date=$(echo "$line" | awk -F'|' '{print $2}' | tr -d ' ')
            local type=$(echo "$line" | awk -F'|' '{print $3}' | tr -d ' ')
            local pref=$(echo "$line" | awk -F'|' '{print $4}' | tr -d ' ')
            
            # 跳过空行或分隔符
            [ -z "$date" ] && continue
            [ "$date" = "日期" ] && continue
            
            # 计算天数差
            local pref_day=$(date -d "$date" +%s 2>/dev/null || echo "$today_day")
            local diff_days=$(( (today_day - pref_day) / 86400 ))
            
            # 根据类型检查是否过期
            local max_days=0
            case "$type" in
                "短期") max_days=7 ;;
                "中期") max_days=30 ;;
                "长期") max_days=999999 ;;  # 永不过期
                *) max_days=7 ;;  # 默认短期
            esac
            
            if [ $diff_days -gt $max_days ]; then
                log "⏰ Expired preference found: [$type] $pref (${diff_days} days old)"
                ((expired_count++))
                
                # 标记为需要移除（输出到临时文件，供外部处理）
                echo "EXPIRED|$type|$pref|$date" >> "$temp_file"
            fi
        fi
    done < "$MEMORY_FILE"
    
    # 汇总
    if [ $expired_count -gt 0 ]; then
        log "📊 Found $expired_count expired preferences"
        # 返回过期条目
        cat "$temp_file"
    else
        log "✅ No expired preferences"
    fi
    
    rm -f "$temp_file" "$tracker_temp"
    return 0
}

# 自动清理短期偏好区的过期内容
clean_short_term_preferences() {
    log "🧹 Cleaning short-term preferences section..."
    
    # 检查短期偏好区是否有内容
    if grep -A 3 "#### ⏰ 短期偏好" "$MEMORY_FILE" | grep -q "\[暂无\]"; then
        log "ℹ️ No short-term preferences to clean"
        return 0
    fi
    
    # 如果短期偏好区有条目，逐个检查过期
    local temp_file=$(mktemp)
    local in_section=false
    local today=$(date +%s)
    local changed=false
    
    while IFS= read -r line; do
        # 检测进入短期偏好区
        if echo "$line" | grep -q "#### ⏰ 短期偏好"; then
            in_section=true
            echo "$line" >> "$temp_file"
            continue
        fi
        
        # 检测离开短期偏好区（下一个章节）
        if $in_section && echo "$line" | grep -q "^#### "; then
            in_section=false
        fi
        
        # 处理短期偏好区的列表项
        if $in_section && echo "$line" | grep -q "^- "; then
            # 尝试提取日期标记（格式：- 偏好内容 @YYYY-MM-DD）
            local pref_line="$line"
            local pref_date=$(echo "$line" | grep -oP '@\K[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
            
            if [ -n "$pref_date" ]; then
                local pref_day=$(date -d "$pref_date" +%s 2>/dev/null || echo "$today")
                local diff_days=$(( (today - pref_day) / 86400 ))
                
                if [ $diff_days -gt 7 ]; then
                    log "🗑️ Removing expired: $line"
                    changed=true
                    continue  # 跳过这行（不写入 temp_file）
                fi
            fi
        fi
        
        # 默认：保留行
        echo "$line" >> "$temp_file"
    done < "$MEMORY_FILE"
    
    # 如果有改动，安全替换原文件（先写临时文件再 mv，防止中断损坏）
    if $changed; then
        cp "$MEMORY_FILE" "${MEMORY_FILE}.orig"
        mv "$temp_file" "${MEMORY_FILE}.tmp"
        mv "${MEMORY_FILE}.tmp" "$MEMORY_FILE"
        rm -f "${MEMORY_FILE}.orig"
        log "✅ Short-term preferences cleaned"
    else
        rm -f "$temp_file"
        log "ℹ️ No changes needed"
    fi
}

# 主函数
main() {
    log "=== Preferences Expiry Check ==="
    
    init_expiry_tracker
    
    # 检查偏好表格
    check_preference_entries
    
    # 清理短期偏好区
    clean_short_term_preferences
    
    log "=== Check Complete ==="
}

main
