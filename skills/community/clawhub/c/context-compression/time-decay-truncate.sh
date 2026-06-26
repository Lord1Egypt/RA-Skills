#!/bin/bash
# Time-Decay Truncation with Char Limit - v1.0
# 时间衰减 + Char 上限的双重约束策略
# 
# 衰减规则：
# - 最近 6h  → 优先级 × 1.5（高权重保留）
# - 6-24h   → 优先级 × 1.0（正常）
# - 24-72h  → 优先级 × 0.5（只有高优先级保留）
# - > 72h   → 仅保留"记住/重要"标记的内容

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_FILE="$WORKSPACE/.context-compression-config.json"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/truncation.log}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
BUDGET_UNITS=40000
UNITS_PER_CHAR=2
DECAY_6H=1.5
DECAY_24H=1.0
DECAY_72H=0.5
DECAY_OLD=0.0

# Load configuration
if [ -f "$CONFIG_FILE" ]; then
    config_budget_units=$(grep -o '"maxTokens": [0-9]*' "$CONFIG_FILE" 2>/dev/null | grep -o '[0-9]*')
    [ -n "$config_budget_units" ] && BUDGET_UNITS="$config_budget_units"
fi

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Get current timestamp in seconds
now_ts() {
    date +%s
}

# Parse timestamp from JSONL line
# Format: {"timestamp":"2026-03-08T22:00:00+08:00",...} or {"ts":1234567890,...}
parse_timestamp() {
    local line=$1
    local ts=""
    
    # Try ISO format first
    ts=$(echo "$line" | grep -oP '(?<="timestamp":")[^"]+' | head -1)
    if [ -n "$ts" ]; then
        # Convert ISO to epoch
        date -d "$ts" +%s 2>/dev/null && return
    fi
    
    # Try Unix timestamp
    ts=$(echo "$line" | grep -oP '(?<="ts":)[0-9]+' | head -1)
    if [ -n "$ts" ]; then
        # Might be milliseconds
        if [ ${#ts} -gt 10 ]; then
            echo $((ts / 1000))
        else
            echo "$ts"
        fi
        return
    fi
    
    # Fallback: use file modification time
    echo "0"
}

# Calculate time decay multiplier
time_decay_multiplier() {
    local msg_ts=$1
    local now=$(now_ts)
    local age_hours=$(( (now - msg_ts) / 3600 ))
    
    if [ $age_hours -le 6 ]; then
        echo "$DECAY_6H"
    elif [ $age_hours -le 24 ]; then
        echo "$DECAY_24H"
    elif [ $age_hours -le 72 ]; then
        echo "$DECAY_72H"
    else
        echo "$DECAY_OLD"
    fi
}

# Score content priority (0-100)
score_content_priority() {
    local line=$1
    local score=50
    
    # High priority keywords (user preferences, decisions, tasks)
    [[ "$line" =~ (用户偏好|喜欢|讨厌|偏好|习惯|风格) ]] && score=$((score + 40))
    [[ "$line" =~ (重要|关键|记住|别忘|必须|一定要) ]] && score=$((score + 45))
    [[ "$line" =~ (决定|确定|选择|方案|定下|决策) ]] && score=$((score + 35))
    [[ "$line" =~ (任务|TODO|待办|进度|完成|进行中) ]] && score=$((score + 25))
    [[ "$line" =~ (明天|下周|周[一二三四五六日]|[0-9]+月[0-9]+日|截止) ]] && score=$((score + 20))
    
    # Low priority
    [[ "$line" =~ (哈哈|呵呵|嗯嗯|好的|收到|OK) ]] && score=$((score - 10))
    [[ "$line" =~ (HEARTBEAT|heartbeat|system) ]] && score=$((score - 20))
    
    [ $score -lt 0 ] && score=0
    [ $score -gt 100 ] && score=100
    
    echo $score
}

# Calculate final priority = content_priority × time_decay
calculate_final_priority() {
    local line=$1
    local msg_ts=$2
    
    local content_score=$(score_content_priority "$line")
    local decay=$(time_decay_multiplier "$msg_ts")
    
    # Use bc for floating point
    local final=$(echo "$content_score * $decay" | bc 2>/dev/null || echo "$content_score")
    
    # Round to integer
    printf "%.0f" "$final"
}

# Check if line is critical (must preserve regardless of time)
is_critical_content() {
    local line=$1
    [[ "$line" =~ (记住|重要|关键|必须|用户偏好|决定) ]]
}

# Estimate chars in a line
estimate_line_units() {
    local line=$1
    local chars=${#line}
    echo $((chars / UNITS_PER_CHAR))
}

# Main truncation function with time-decay
truncate_with_time_decay() {
    local file=$1
    local budget_units=$2
    local temp_scores="/tmp/scores-$$.tmp"
    local temp_result="/tmp/result-$$.tmp"
    
    > "$temp_scores"
    > "$temp_result"
    
    local total_units=0
    local line_num=0
    local now=$(now_ts)
    
    log "  🕐 Applying time-decay priority..."
    
    # Phase 1: Score all lines
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        ((line_num++))
        
        local msg_ts=$(parse_timestamp "$line")
        local final_priority=$(calculate_final_priority "$line" "$msg_ts")
        local chars=$(estimate_line_units "$line")
        
        # Format: priority|line_num|chars|line
        echo "${final_priority}|${line_num}|${chars}|${line}" >> "$temp_scores"
    done < "$file"
    
    # Phase 2: Sort by priority (descending) then by line_num (ascending, for recency)
    sort -t'|' -k1,1nr -k2,2n "$temp_scores" > "${temp_scores}.sorted"
    
    # Phase 3: Select lines within char budget
    local kept_lines=""
    local kept_units=0
    local critical_preserved=0
    
    while IFS='|' read -r priority line_num chars line; do
        # Always preserve critical content (unless extremely old and low priority)
        if is_critical_content "$line"; then
            if [ $((kept_units + chars)) -le $budget_units ] || [ $priority -ge 70 ]; then
                kept_lines="${kept_lines}${line_num}|"
                kept_units=$((kept_units + chars))
                ((critical_preserved++))
                continue
            fi
        fi
        
        # Check budget
        if [ $((kept_units + chars)) -le $budget_units ]; then
            kept_lines="${kept_lines}${line_num}|"
            kept_units=$((kept_units + chars))
        fi
    done < "${temp_scores}.sorted"
    
    # Phase 4: Reconstruct file preserving original order
    local total_lines=$(wc -l < "$file")
    local preserved_count=0
    
    for i in $(seq 1 $total_lines); do
        if [[ "$kept_lines" == *"|${i}|"* ]]; then
            sed -n "${i}p" "$file" >> "$temp_result"
            ((preserved_count++))
        fi
    done
    
    # Phase 5: Replace original file
    if [ $preserved_count -gt 0 ]; then
        mv "$temp_result" "$file"
        log "  ✅ Preserved $preserved_count lines (~${kept_units}t), critical: $critical_preserved"
    else
        log "  ⚠️ No lines preserved, keeping last 100 lines as fallback"
        tail -n 100 "$file" > "$temp_result"
        mv "$temp_result" "$file"
    fi
    
    # Cleanup
    rm -f "$temp_scores" "${temp_scores}.sorted" "$temp_result"
    
    echo $preserved_count
}

# Process a single session file
process_session() {
    local file=$1
    local filename=$(basename "$file")
    
    # Check if file is large enough to need truncation
    local total_chars=$(wc -c < "$file" 2>/dev/null || echo 0)
    local total_units=$((total_chars / UNITS_PER_CHAR))
    
    if [ $total_units -le $BUDGET_UNITS ]; then
        return 0
    fi
    
    log "Processing: $filename (~${total_units}t)"
    
    # Apply time-decay truncation
    truncate_with_time_decay "$file" "$BUDGET_UNITS"
}

# Main entry point
main() {
    local sessions_dir="${SESSIONS_DIR:-$HOME/.openclaw/agents/main/sessions}"
    
    log "=== Time-Decay Truncation (v1.0) ==="
    log "Max chars: $BUDGET_UNITS"
    log "Decay factors: 6h=${DECAY_6H}, 24h=${DECAY_24H}, 72h=${DECAY_72H}, old=${DECAY_OLD}"
    
    local processed=0
    local truncated=0
    
    for f in "$sessions_dir"/*.jsonl; do
        [ ! -f "$f" ] && continue
        ((processed++))
        
        if process_session "$f"; then
            ((truncated++))
        fi
    done
    
    log "Processed: $processed, Truncated: $truncated"
    log ""
}

# CLI
if [ $# -eq 0 ]; then
    main
elif [ "$1" = "--file" ] && [ -n "$2" ]; then
    process_session "$2"
elif [ "$1" = "--test" ]; then
    echo "Testing time-decay calculation..."
    now=$(now_ts)
    
    echo "Now: $now"
    echo "6h ago: $((now - 6*3600)) -> decay: $(time_decay_multiplier $((now - 6*3600)))"
    echo "12h ago: $((now - 12*3600)) -> decay: $(time_decay_multiplier $((now - 12*3600)))"
    echo "48h ago: $((now - 48*3600)) -> decay: $(time_decay_multiplier $((now - 48*3600)))"
    echo "100h ago: $((now - 100*3600)) -> decay: $(time_decay_multiplier $((now - 100*3600)))"
else
    echo "Usage: $0 [--file <session.jsonl> | --test]"
    exit 1
fi
