#!/bin/bash
# Session Window Truncation (Char-based) - v10
# Supports multiple strategies: compact-only, time-decay, priority-first
# Enhanced with fact identification and priority-based preservation
# v7: Added preserveUserMessages option to always keep user messages
# v8: Fixed priority-first strategy to call fact identification before truncating
# v9: Identify facts from active sessions too (even when skipActive=true)
# v10: Added recursion guard + flock idempotency + fixed priority-first ordering
# This script runs OUTSIDE of OpenClaw agent context

# Recursion guard: prevent nested calls (e.g. agent→truncation→agent)
if [ "${CONTEXT_COMPRESSION_RUNNING:-false}" = "true" ]; then
    exit 0
fi
export CONTEXT_COMPRESSION_RUNNING=true

# Idempotency: flock prevents concurrent runs from corrupting session files
LOCK_FILE="/tmp/context-compression.lock"
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "[$(date)] ⏭️ Another truncation instance is running, exiting" >&2; exit 0; }

# Cleanup temp files on exit (even if SIGTERM/SIGINT)
_CLEANUP_PIDS=()
cleanup_on_exit() {
    for pid in "${_CLEANUP_PIDS[@]}"; do
        rm -f "$SESSIONS_DIR"/*.${pid} 2>/dev/null || true
    done
    flock -u 9 2>/dev/null || true
}
trap cleanup_on_exit EXIT
# Track this PID's temp files
_CLEANUP_PIDS+=("$$")

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_FILE="$WORKSPACE/.context-compression-config.json"
SESSIONS_DIR="${SESSIONS_DIR:-$HOME/.openclaw/agents/main/sessions}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/truncation.log}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
BUDGET_UNITS=60000
MAX_LINE_CHARS=4000
MAX_HISTORY_LINES=200
SKIP_ACTIVE=true
UNITS_PER_CHAR=2  # Conservative estimate: 1 char ≈ 2 chars (Chinese-heavy content)
STRATEGY="priority-first"  # "compact-only", "time-decay", or "priority-first"
ENABLE_FACT_IDENTIFICATION=true  # P0 optimization: identify facts before truncation
USE_AI_IDENTIFICATION=false    # AI-assisted: requires explicit opt-in (may send content to remote LLMs)
ENABLE_PRIORITY_PRESERVATION=true  # P0 optimization: preserve high-priority content
PRESERVE_USER_MESSAGES=true  # v7: Always preserve user messages

# Default priority keywords (can be overridden by config)
# v8: Bilingual support for global users (case-insensitive via extended patterns)
# Note: bash regex is case-sensitive, so include common case variants
PRIORITY_KEYWORDS="重要|决定|记住|别忘了|TODO|待办|偏好|我喜欢|我讨厌|千万|务必|关键|明天|下周|约会|会议|截止|同事|老板|客户|朋友|important|Important|IMPORTANT|remember|Remember|REMEMBER|must|MUST|deadline|Deadline|DEADLINE|decision|Decision|DECISION|prefer|Prefer|critical|Critical|CRITICAL|urgent|Urgent|URGENT|note|Note|NOTE"

# Load configuration from JSON file if exists
if [ -f "$CONFIG_FILE" ]; then
    # Use Python or jq if available, otherwise fall back to grep
    if command -v jq &> /dev/null; then
        BUDGET_UNITS=$(jq -r '.maxChars // .maxTokens // empty' "$CONFIG_FILE" 2>/dev/null || echo "$BUDGET_UNITS")
        SKIP_ACTIVE=$(jq -r '.skipActive // empty' "$CONFIG_FILE" 2>/dev/null || echo "$SKIP_ACTIVE")
        STRATEGY=$(jq -r '.strategy // empty' "$CONFIG_FILE" 2>/dev/null || echo "$STRATEGY")
        PRESERVE_USER_MESSAGES=$(jq -r '.preserveUserMessages // empty' "$CONFIG_FILE" 2>/dev/null || echo "$PRESERVE_USER_MESSAGES")
        MAX_HISTORY_LINES=$(jq -r '.maxHistoryLines // empty' "$CONFIG_FILE" 2>/dev/null || echo "$MAX_HISTORY_LINES")
        USE_AI_IDENTIFICATION=$(jq -r '.useAiIdentification // empty' "$CONFIG_FILE" 2>/dev/null || echo "$USE_AI_IDENTIFICATION")
        # v8: Load priority keywords from config
        CONFIG_KEYWORDS=$(jq -r '.priorityKeywords | join("|") // empty' "$CONFIG_FILE" 2>/dev/null)
        [ -n "$CONFIG_KEYWORDS" ] && PRIORITY_KEYWORDS="$CONFIG_KEYWORDS"
    else
        # Fallback: use sed for simple JSON parsing
        config_budget_units=$(sed -n 's/.*"maxTokens"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p' "$CONFIG_FILE" 2>/dev/null)
        config_skip_active=$(sed -n 's/.*"skipActive"[[:space:]]*:[[:space:]]*\([a-z]*\).*/\1/p' "$CONFIG_FILE" 2>/dev/null)
        config_strategy=$(sed -n 's/.*"strategy"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$CONFIG_FILE" 2>/dev/null)
        config_preserve=$(sed -n 's/.*"preserveUserMessages"[[:space:]]*:[[:space:]]*\([a-z]*\).*/\1/p' "$CONFIG_FILE" 2>/dev/null)
        config_max_lines=$(sed -n 's/.*"maxHistoryLines"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p' "$CONFIG_FILE" 2>/dev/null)
        
        [ -n "$config_budget_units" ] && BUDGET_UNITS="$config_budget_units"
        [ -n "$config_skip_active" ] && SKIP_ACTIVE="$config_skip_active"
        [ -n "$config_strategy" ] && STRATEGY="$config_strategy"
        [ -n "$config_preserve" ] && PRESERVE_USER_MESSAGES="$config_preserve"
        [ -n "$config_max_lines" ] && MAX_HISTORY_LINES="$config_max_lines"
    fi
fi

# Override with environment variables
[ -n "${BUDGET_UNITS:-}" ] && BUDGET_UNITS="$BUDGET_UNITS"
[ -n "${SKIP_ACTIVE:-}" ] && SKIP_ACTIVE="$SKIP_ACTIVE"
[ -n "${STRATEGY:-}" ] && STRATEGY="$STRATEGY"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# ===== P0 Optimization: Fact Identification =====
# Identify high-value facts from content before it gets truncated
identify_facts_from_content() {
    local file=$1
    local start_line=$2
    local end_line=$3
    
    [ "$ENABLE_FACT_IDENTIFICATION" != "true" ] && return 0
    
    # Default to keyword-based (local-only, no external calls).
    # AI-assisted identification only when useAiIdentification=true in config.
    local identify_script="$SCRIPT_DIR/identify-facts.sh"
    [ "$USE_AI_IDENTIFICATION" = "true" ] && identify_script="$SCRIPT_DIR/identify-facts-enhanced.sh"
    [ ! -x "$identify_script" ] && return 0
    
    # Identify the portion that will be truncated (lines from start_line to end_line)
    local content_to_truncate
    if [ "$start_line" -eq 1 ]; then
        content_to_truncate=$(head -n "$end_line" "$file" 2>/dev/null)
    else
        content_to_truncate=$(sed -n "${start_line},${end_line}p" "$file" 2>/dev/null)
    fi
    
    if [ -n "$content_to_truncate" ]; then
        log "  🤖 Calling fact identification agent..."
        # Call identify-facts script via stdin
        echo "$content_to_truncate" | "$identify_script" "$file" 2>&1 | while read -r line; do
            log "    $line"
        done
        return 0
    fi
}

# ===== P0 Optimization: Priority-Based Preservation =====
# Delegate scoring to content-priority.sh (single source of truth)
# Falls back to inline scoring if the script is unavailable
score_line_priority() {
    local line=$1
    local priority_script="$SCRIPT_DIR/content-priority.sh"
    
    if [ -x "$priority_script" ]; then
        bash "$priority_script" /dev/stdin 2>/dev/null <<< "$line" || true
        # Identify score from the tab-separated output: "1\t<score>\t..."
        local scored
        scored=$(echo "$line" | bash "$priority_script" /dev/stdin 2>/dev/null | head -1)
        if [ -n "$scored" ]; then
            echo "$scored" | awk -F'\t' '{print $2}'
            return
        fi
    fi
    
    # Inline fallback (matches content-priority.sh score_content logic)
    local score=50
    if [ -n "$PRIORITY_KEYWORDS" ]; then
        [[ "$line" =~ ($PRIORITY_KEYWORDS) ]] && score=$((score + 40))
    fi
    [[ "$line" =~ (用户偏好|喜欢|讨厌|偏好|习惯|风格) ]] && score=$((score + 40))
    [[ "$line" =~ (关键|必须|一定要) ]] && score=$((score + 45))
    [[ "$line" =~ (确定|选择|方案|定下|决策) ]] && score=$((score + 35))
    [[ "$line" =~ (任务|进度|完成|进行中) ]] && score=$((score + 25))
    [[ "$line" =~ (周[一二三四五六日]|[0-9]+月[0-9]+日) ]] && score=$((score + 20))
    [[ "$line" =~ (哈哈|呵呵|嗯嗯|好的|收到|OK) ]] && score=$((score - 10))
    [[ "$line" =~ (HEARTBEAT|heartbeat|system) ]] && score=$((score - 20))
    [ $score -lt 0 ] && score=0
    [ $score -gt 100 ] && score=100
    echo $score
}

# Check if a line is high priority (should be preserved or identified)
is_high_priority() {
    local line=$1
    local threshold=${2:-70}
    local score=$(score_line_priority "$line")
    [ "$score" -ge "$threshold" ]
}

# Estimate char count from character count
# Conservative: 1 char ≈ 3 chars (handles mixed Chinese/English)
estimate_units() {
    local char_count=$1
    echo $((char_count / UNITS_PER_CHAR))
}

# Count total characters in a file
count_chars() {
    local file=$1
    wc -c < "$file" 2>/dev/null || echo 0
}

# Find how many lines from the end fit within char budget
find_truncate_point() {
    local file=$1
    local budget_units=$2
    local max_chars=$((budget_units * UNITS_PER_CHAR))
    
    local total_chars=$(count_chars "$file")
    if [ "$total_chars" -le "$max_chars" ]; then
        echo 0  # No truncation needed
        return
    fi
    
    # Binary search for the right number of lines
    local total_lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    local low=1
    local high=$total_lines
    local result=$total_lines
    
    while [ $low -le $high ]; do
        local mid=$(( (low + high) / 2 ))
        local char_count=$(tail -n $mid "$file" | wc -c 2>/dev/null || echo 0)
        
        if [ "$char_count" -le "$max_chars" ]; then
            result=$mid
            high=$((mid - 1))
        else
            low=$((mid + 1))
        fi
    done
    
    echo $result
}

log "=== Session Window Truncation (v10 - Strategy: $STRATEGY) ==="
log "Config: $CONFIG_FILE"
log "Max chars: $BUDGET_UNITS (~$((BUDGET_UNITS * UNITS_PER_CHAR)) chars)"
log "Skip active: $SKIP_ACTIVE"
log "Strategy: $STRATEGY"
log "Preserve user messages: $PRESERVE_USER_MESSAGES"
log "Max history lines: $MAX_HISTORY_LINES"
log "Fact identification: $ENABLE_FACT_IDENTIFYION"
log "Priority preservation: $ENABLE_PRIORITY_PRESERVATION"

truncated_count=0
trimmed_count=0
skipped_count=0
error_count=0
facts_identified=0

for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -e "$f" ] || continue
    filename=$(basename "$f")
    
    [[ "$f" == *.deleted.* ]] && continue
    
    # Calculate current char count
    total_chars=$(count_chars "$f")
    total_units=$(estimate_units "$total_chars")
    
    # v9: Even active sessions need fact identification if over threshold
    if [ -f "${f}.lock" ] && [ "$SKIP_ACTIVE" = "true" ]; then
        if [ "$total_units" -gt "$BUDGET_UNITS" ] && [ "$ENABLE_FACT_IDENTIFYION" = "true" ]; then
            log "📋 Active session over threshold (~${total_units}t), identifying facts..."
            
            # Scan for high-priority content in the session
            lines=$(wc -l < "$f" 2>/dev/null || echo 0)
            high_priority_count=0
            
            while IFS= read -r line; do
                if is_high_priority "$line" 70; then
                    ((high_priority_count++))
                fi
            done < "$f"
            
            if [ "$high_priority_count" -gt 0 ]; then
                log "  💎 Found $high_priority_count high-priority lines, selecting..."
                identify_facts_from_content "$f" 1 "$lines"
                ((facts_identified++))
            else
                log "  ✅ No high-priority content found"
            fi
        fi
        
        log "⏭️  Skip active: $filename"
        ((skipped_count++))
        continue
    fi
    
    [ "$total_units" -le "$BUDGET_UNITS" ] && continue
    
    lines=$(wc -l < "$f" 2>/dev/null)
    log "Processing: $filename (~${total_units} chars, ${lines}L)"
    
    # Step 1: Trim oversized lines first
    temp_file="${f}.trim.$$"
    oversized=0
    
    while IFS= read -r line; do
        len=${#line}
        if [ "$len" -gt "$MAX_LINE_CHARS" ]; then
            # Truncate line content
            prefix="${line:0:3000}"
            suffix="${line: -500}"
            echo "${prefix}...[TRUNCATED ${len}b]...${suffix}" >> "$temp_file"
            ((oversized++))
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$f"
    
    if [ "$oversized" -gt 0 ]; then
        mv "$temp_file" "$f"
        log "  Trimmed $oversized oversized lines"
        ((trimmed_count+=oversized))
    else
        rm -f "$temp_file"
    fi
    
    # Step 2: Apply truncation strategy
    total_chars=$(count_chars "$f")
    total_units=$(estimate_units "$total_chars")
    
    if [ "$total_units" -gt "$BUDGET_UNITS" ]; then
        if [ "$STRATEGY" = "priority-first" ]; then
            # v10: Priority-first truncation — preserve message ORDER
            # Strategy: keep first line (metadata) + identify facts from discarded head + tail to budget
            log "  🎯 Applying priority-first strategy..."
            
            temp_file="${f}.priority.$$"
            
            # Find how many lines from the end fit within budget (same as compact-only)
            keep_lines=$(find_truncate_point "$f" "$BUDGET_UNITS")
            
            if [ "$keep_lines" -gt 0 ] && [ "$keep_lines" -lt "$lines" ]; then
                # Identify facts from the discarded portion BEFORE truncating
                if [ "$ENABLE_FACT_IDENTIFYION" = "true" ]; then
                    truncate_end=$((lines - keep_lines))
                    high_priority_count=0
                    
                    log "  📋 Scanning lines 1-$truncate_end for high-priority content..."
                    
                    while IFS= read -r line; do
                        if is_high_priority "$line" 70; then
                            ((high_priority_count++))
                        fi
                    done < <(head -n "$truncate_end" "$f")
                    
                    if [ "$high_priority_count" -gt 0 ]; then
                        log "  💎 Found $high_priority_count high-priority lines, identifying facts..."
                        identify_facts_from_content "$f" 1 "$truncate_end"
                        facts_identified=$((facts_identified + 1))
                    else
                        log "  ✅ No high-priority content in discarded portion"
                    fi
                fi
                
                # Preserve message order: keep first line + recent lines (no reordering)
                # First line = session metadata, must always be kept
                head -1 "$f" > "$temp_file"
                tail -n $((keep_lines - 1)) "$f" >> "$temp_file"
                
                new_chars=$(wc -c < "$temp_file")
                new_units=$(estimate_units "$new_chars")
                new_lines=$(wc -l < "$temp_file")
                
                if [ "$new_units" -lt "$total_units" ]; then
                    if mv "$temp_file" "$f" 2>/dev/null; then
                        log "  ✂️ Truncated (order preserved): ~${total_units}t ${lines}L → ~${new_units}t ${new_lines}L"
                        ((truncated_count++))
                    else
                        rm -f "$temp_file"
                        log "  ❌ Failed to apply priority-first truncation"
                        ((error_count++))
                    fi
                else
                    rm -f "$temp_file"
                    log "  ⚠️ Priority-first didn't reduce size"
                fi
            else
                log "  ⚠️ Cannot truncate further (already at minimum)"
            fi
        elif [ "$STRATEGY" = "time-decay" ]; then
            # Use time-decay truncation
            log "  🕐 Applying time-decay strategy..."
            "$SCRIPT_DIR/time-decay-truncate.sh" --file "$f" 2>/dev/null
            ((truncated_count++))
        else
            # Default: compact-only truncation with fact identification
            keep_lines=$(find_truncate_point "$f" "$BUDGET_UNITS")
            
            if [ "$keep_lines" -gt 0 ] && [ "$keep_lines" -lt "$lines" ]; then
                # Identify facts BEFORE truncating
                if [ "$ENABLE_FACT_IDENTIFYION" = "true" ]; then
                    truncate_end=$((lines - keep_lines))
                    high_priority_count=0
                    
                    log "  📋 Scanning lines 1-$truncate_end for high-priority content..."
                    
                    while IFS= read -r line; do
                        if is_high_priority "$line" 70; then
                            ((high_priority_count++))
                        fi
                    done < <(head -n "$truncate_end" "$f")
                    
                    if [ "$high_priority_count" -gt 0 ]; then
                        log "  💎 Found $high_priority_count high-priority lines to identify"
                        identify_facts_from_content "$f" 1 "$truncate_end"
                    else
                        log "  ✅ No high-priority content in truncated portion"
                    fi
                fi
                
                # Perform truncation
                temp_file="${f}.trunc.$$"
                tail -n "$keep_lines" "$f" > "$temp_file" 2>/dev/null
                
                if mv "$temp_file" "$f" 2>/dev/null; then
                    final_chars=$(count_chars "$f")
                    final_units=$(estimate_units "$final_chars")
                    final_lines=$(wc -l < "$f")
                    log "  ✂️ Truncated: ~${total_units}t ${lines}L → ~${final_units}t ${final_lines}L"
                    ((truncated_count++))
                else
                    rm -f "$temp_file"
                    log "  ❌ Failed to truncate"
                    ((error_count++))
                fi
            else
                log "  ⚠️ Cannot truncate further (already at minimum)"
            fi
        fi
    else
        log "  ✅ Size OK after trim: ~${total_units}t"
    fi
done

log ""
log "=== Summary ==="
log "Truncated: $truncated_count"
log "Lines trimmed: $trimmed_count"
log "Skipped: $skipped_count"
log "Errors: $error_count"
log "Facts identified: ${facts_identified:-0}"
log ""

[ "$error_count" -eq 0 ]
