#!/bin/bash
# Context Guardian - Main check script
# Called by heartbeat or manually

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config/default.json"
USER_CONFIG_FILE="$SKILL_DIR/config/user.json"

# Workspace detection
if [ -n "${OPENCLAW_WORKSPACE:-}" ]; then
    WORKSPACE="$OPENCLAW_WORKSPACE"
else
    WORKSPACE="${HOME}/.openclaw/workspace"
fi

STATE_FILE="$WORKSPACE/memory/context-guardian-state.json"

# Ensure memory directory exists
mkdir -p "$WORKSPACE/memory"

# Load config
load_config() {
    local key="$1"
    local default="$2"
    
    # Try user config first, then default config
    if [ -f "$USER_CONFIG_FILE" ]; then
        local value=$(jq -r ".$key // empty" "$USER_CONFIG_FILE" 2>/dev/null || echo "")
        if [ -n "$value" ] && [ "$value" != "null" ]; then
            echo "$value"
            return
        fi
    fi
    
    if [ -f "$CONFIG_FILE" ]; then
        local value=$(jq -r ".$key // empty" "$CONFIG_FILE" 2>/dev/null || echo "")
        if [ -n "$value" ] && [ "$value" != "null" ]; then
            echo "$value"
            return
        fi
    fi
    
    echo "$default"
}

# Load thresholds
WARNING_THRESHOLD=$(load_config "thresholds.warning" "60")
DANGER_THRESHOLD=$(load_config "thresholds.danger" "70")
CRITICAL_THRESHOLD=$(load_config "thresholds.critical" "85")
PREVENT_DUPLICATES=$(load_config "preventDuplicates" "true")

# Get current context usage from session_status
get_context_usage() {
    # Try to get session status
    # This assumes we can call openclaw or have access to session_status
    # For now, we'll parse from a hypothetical session_status output
    
    # Attempt 1: Use openclaw CLI if available
    if command -v openclaw &> /dev/null; then
        local status_output=$(openclaw session status 2>/dev/null || echo "")
        if [ -n "$status_output" ]; then
            # Parse "Context: 54k/200k (27%)" format
            local usage=$(echo "$status_output" | grep -oP 'Context:.*?\(\K\d+(?=%)' || echo "")
            if [ -n "$usage" ]; then
                echo "$usage"
                return
            fi
        fi
    fi
    
    # Attempt 2: Check if we're in an agent context with session_status tool
    # This would require the agent to call this script with context info
    # For now, return empty to indicate we couldn't get usage
    echo ""
}

# Load state
load_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo '{"lastCheck":null,"lastUsage":null,"lastAlertLevel":null,"lastAlertTime":null,"history":[]}'
    fi
}

# Save state
save_state() {
    local usage="$1"
    local alert_level="$2"
    local timestamp=$(date +%s)
    
    local state=$(load_state)
    
    # Update state
    local new_state=$(echo "$state" | jq \
        --arg usage "$usage" \
        --arg level "$alert_level" \
        --arg time "$timestamp" \
        '.lastCheck = ($time | tonumber) |
         .lastUsage = ($usage | tonumber) |
         .lastAlertLevel = (if $level == "" then null else $level end) |
         .lastAlertTime = (if $level == "" then .lastAlertTime else ($time | tonumber) end) |
         .history += [{"timestamp": ($time | tonumber), "usage": ($usage | tonumber)}] |
         .history = (.history | if length > 100 then .[-100:] else . end)')
    
    echo "$new_state" > "$STATE_FILE"
}

# Check if should alert
should_alert() {
    local current_usage="$1"
    local current_level="$2"
    
    if [ "$PREVENT_DUPLICATES" != "true" ]; then
        echo "yes"
        return
    fi
    
    local state=$(load_state)
    local last_level=$(echo "$state" | jq -r '.lastAlertLevel // ""')
    local last_usage=$(echo "$state" | jq -r '.lastUsage // 0')
    
    # First time reaching threshold
    if [ -z "$last_level" ] && [ -n "$current_level" ]; then
        echo "yes"
        return
    fi
    
    # Level upgrade
    local level_map='{"warning":1,"danger":2,"critical":3}'
    local current_level_num=$(echo "$level_map" | jq -r ".[\"$current_level\"] // 0")
    local last_level_num=$(echo "$level_map" | jq -r ".[\"$last_level\"] // 0")
    
    if [ "$current_level_num" -gt "$last_level_num" ]; then
        echo "yes"
        return
    fi
    
    # Usage dropped and rose again
    local threshold=0
    case "$last_level" in
        warning) threshold=$WARNING_THRESHOLD ;;
        danger) threshold=$DANGER_THRESHOLD ;;
        critical) threshold=$CRITICAL_THRESHOLD ;;
    esac
    
    if [ "$last_usage" -lt $((threshold - 5)) ] && [ "$current_usage" -ge "$threshold" ]; then
        echo "yes"
        return
    fi
    
    echo "no"
}

# Format alert message
format_alert() {
    local usage="$1"
    local level="$2"
    
    case "$level" in
        warning)
            cat <<EOF
⚠️ Context: ${usage}%
Getting full. Consider wrapping up or starting fresh soon.
EOF
            ;;
        danger)
            cat <<EOF
🟠 Context: ${usage}%
Pollution risk rising. Recommend:
• Finish current task
• Start new session for next task
• Or compress with context-optimizer
EOF
            ;;
        critical)
            cat <<EOF
🔴 Context: ${usage}% - CRITICAL
High error risk. STRONGLY recommend:
• Save work
• Start new session NOW
• Quality degradation likely
EOF
            ;;
    esac
}

# Main logic
main() {
    # Get current usage
    local usage=$(get_context_usage)
    
    if [ -z "$usage" ]; then
        # Can't get usage, skip silently
        # This is expected when called outside of agent context
        exit 0
    fi
    
    # Determine alert level
    local alert_level=""
    if [ "$usage" -ge "$CRITICAL_THRESHOLD" ]; then
        alert_level="critical"
    elif [ "$usage" -ge "$DANGER_THRESHOLD" ]; then
        alert_level="danger"
    elif [ "$usage" -ge "$WARNING_THRESHOLD" ]; then
        alert_level="warning"
    fi
    
    # Check if should alert
    if [ -n "$alert_level" ]; then
        local should=$(should_alert "$usage" "$alert_level")
        if [ "$should" = "yes" ]; then
            format_alert "$usage" "$alert_level"
            save_state "$usage" "$alert_level"
        else
            # Update state without alerting
            save_state "$usage" ""
        fi
    else
        # Below all thresholds, update state
        save_state "$usage" ""
    fi
}

main "$@"
