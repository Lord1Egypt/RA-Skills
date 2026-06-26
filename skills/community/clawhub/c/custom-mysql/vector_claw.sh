#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# vectorclaw — Agent-facing MySQL command wrapper for MySQLClaw
#
# Usage:
#   vectorclaw query "SQL"                Execute a read-only SELECT query
#   vectorclaw exec --file X              Execute a reviewed SQL script
#   vectorclaw insert_interaction ...     Log a user interaction
#   vectorclaw insert_note ...            Add a user note
#   vectorclaw insert_context ...         Set user context
#   vectorclaw insert_skill_usage ...     Log skill usage
#   vectorclaw insert_relationship ...    Add a user relationship
#   vectorclaw insert_mood ...            Track user mood
#   vectorclaw insert_reminder ...        Set a proactive reminder
#   vectorclaw insert_thought ...         Log agent thought
#   vectorclaw insert_learning ...        Log agent learning
#   vectorclaw insert_event ...           Log community event
#   vectorclaw help                       Show this help
#
# All commands route through sql_safe_exec.sh which enforces:
#   - Single-statement only (semicolons rejected)
#   - DDL blocked (DROP, TRUNCATE, CREATE, ALTER)
#   - DML requires interactive confirmation (no --yes bypass)
#   - query command is SELECT-only
#   - Table allowlist enforced for all write operations (28 tables)
#   - Path traversal blocked
#   - Comment injection blocked
#   - Hex-encoded string detection blocked
#   - Credentials via temporary --defaults-extra-file
#   - .env file support
# ------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAFE_EXEC="$SCRIPT_DIR/sql_safe_exec.sh"

# Load .env if present — parse as KEY=ONLY safe KEY=VALUE lines (no shell evaluation)
if [ -f "$SCRIPT_DIR/.env" ]; then
    while IFS='=' read -r key val; do
        # Skip comments, blank lines, and keys with special chars
        [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        export "$key=$val"
    done < <(grep -v '^[[:space:]]*#' "$SCRIPT_DIR/.env" | grep '=')
fi

# ------------------------------------------------------------------
# mysql_escape: Properly escape a string value for MySQL
# Uses Python for reliable escaping (handles all edge cases)
# ------------------------------------------------------------------
mysql_escape() {
    python3 -c "
import sys
val = sys.argv[1]
# MySQL escaping: backslash, single quote, newline, carriage return, NUL
val = val.replace('\\\\', '\\\\\\\\')
val = val.replace(\"'\", \"''\")
val = val.replace('\\n', '\\\\n')
val = val.replace('\\r', '\\\\r')
val = val.replace('\\x00', '\\\\0')
print(val, end='')
" "$1"
}

# ------------------------------------------------------------------
# validate_enum: Validate a value against allowed options
# ------------------------------------------------------------------
validate_enum() {
    local val="$1"
    shift
    local allowed=("$@")
    for a in "${allowed[@]}"; do
        if [ "$val" = "$a" ]; then
            return 0
        fi
    done
    echo "ERROR: Invalid value '$val'. Allowed: ${allowed[*]}" >&2
    return 1
}

CMD="${1:-help}"
shift || true

case "$CMD" in
    query)
        SQL="${1:-}"
        if [ -z "$SQL" ]; then
            echo "ERROR: No SQL provided. Usage: vectorclaw query \"SQL\"" >&2
            exit 1
        fi
        "$SAFE_EXEC" --readonly "$SQL"
        ;;

    exec)
        FILE=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --file) FILE="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
            echo "ERROR: --file <path> required." >&2
            exit 1
        fi
        ERRORS=0
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ -z "${line// /}" ]] && continue
            [[ "$line" =~ ^-- ]] && continue
            [[ "$line" =~ ^# ]] && continue
            echo "Executing: $line"
            if ! "$SAFE_EXEC" "$line"; then
                echo "ERROR: Statement failed: $line" >&2
                ERRORS=$((ERRORS + 1))
            fi
        done < "$FILE"
        if [ "$ERRORS" -gt 0 ]; then
            echo "WARNING: $ERRORS statement(s) failed." >&2
            exit 1
        fi
        echo "Script execution complete." ;;

    insert_interaction)
        # Usage: vectorclaw insert_interaction <user_id> <direction> <topic> <summary> [sentiment] [is_important]
        USER_ID="${1:-}"; DIRECTION="${2:-}"; TOPIC="${3:-}"; SUMMARY="${4:-}"; SENTIMENT="${5:-neutral}"; IS_IMPORTANT="${6:-false}"
        if [ -z "$USER_ID" ] || [ -z "$DIRECTION" ] || [ -z "$TOPIC" ]; then
            echo "ERROR: Usage: vectorclaw insert_interaction <user_id> <direction> <topic> <summary> [sentiment] [is_important]" >&2
            exit 1
        fi
        validate_enum "$SENTIMENT" "positive" "neutral" "negative" "mixed" || exit 1
        validate_enum "$DIRECTION" "inbound" "outbound" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_direction=$(mysql_escape "$DIRECTION")
        esc_topic=$(mysql_escape "$TOPIC")
        esc_summary=$(mysql_escape "$SUMMARY")
        esc_sentiment=$(mysql_escape "$SENTIMENT")
        esc_important=$(mysql_escape "$IS_IMPORTANT")
        "$SAFE_EXEC" "INSERT INTO user_interactions (user_id, channel, direction, topic, summary, sentiment, is_important) VALUES ('${esc_user_id}', 'discord', '${esc_direction}', '${esc_topic}', '${esc_summary}', '${esc_sentiment}', ${esc_important})"
        ;;

    insert_note)
        # Usage: vectorclaw insert_note <user_id> <note> [category] [is_pinned]
        USER_ID="${1:-}"; NOTE="${2:-}"; CATEGORY="${3:-general}"; IS_PINNED="${4:-false}"
        if [ -z "$USER_ID" ] || [ -z "$NOTE" ]; then
            echo "ERROR: Usage: vectorclaw insert_note <user_id> <note> [category] [is_pinned]" >&2
            exit 1
        fi
        validate_enum "$CATEGORY" "general" "preference" "behavior" "event" "reminder" "other" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_note=$(mysql_escape "$NOTE")
        esc_category=$(mysql_escape "$CATEGORY")
        esc_pinned=$(mysql_escape "$IS_PINNED")
        "$SAFE_EXEC" "INSERT INTO user_notes (user_id, note, category, is_pinned) VALUES ('${esc_user_id}', '${esc_note}', '${esc_category}', ${esc_pinned})"
        ;;

    insert_context)
        # Usage: vectorclaw insert_context <user_id> <key> <value> [type] [importance] [expires_at]
        USER_ID="${1:-}"; KEY="${2:-}"; VALUE="${3:-}"; CTYPE="${4:-episodic}"; IMPORTANCE="${5:-0.5}"; EXPIRES="${6:-}"
        if [ -z "$USER_ID" ] || [ -z "$KEY" ]; then
            echo "ERROR: Usage: vectorclaw insert_context <user_id> <key> <value> [type] [importance] [expires_at]" >&2
            exit 1
        fi
        validate_enum "$CTYPE" "episodic" "semantic" "procedural" "emotional" "preference" "fact" "custom" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_key=$(mysql_escape "$KEY")
        esc_value=$(mysql_escape "$VALUE")
        esc_type=$(mysql_escape "$CTYPE")
        esc_expires=$(mysql_escape "$EXPIRES")
        # Validate importance is numeric
        if [[ ! "$IMPORTANCE" =~ ^[0-9]*\.?[0-9]+$ ]]; then
            echo "ERROR: importance must be numeric" >&2
            exit 1
        fi
        if [ -n "$EXPIRES" ]; then
            "$SAFE_EXEC" "INSERT INTO user_context (user_id, context_key, context_value, context_type, importance, expires_at) VALUES ('${esc_user_id}', '${esc_key}', '${esc_value}', '${esc_type}', ${IMPORTANCE}, '${esc_expires}') ON DUPLICATE KEY UPDATE context_value='${esc_value}', context_type='${esc_type}', importance=${IMPORTANCE}, expires_at='${esc_expires}', is_active=TRUE, updated_at=NOW()"
        else
            "$SAFE_EXEC" "INSERT INTO user_context (user_id, context_key, context_value, context_type, importance) VALUES ('${esc_user_id}', '${esc_key}', '${esc_value}', '${esc_type}', ${IMPORTANCE}) ON DUPLICATE KEY UPDATE context_value='${esc_value}', context_type='${esc_type}', importance=${IMPORTANCE}, is_active=TRUE, updated_at=NOW()"
        fi
        ;;

    insert_skill_usage)
        # Usage: vectorclaw insert_skill_usage <user_id> <skill_name> [action] [status] [duration_ms] [error_type]
        USER_ID="${1:-}"; SKILL="${2:-}"; ACTION="${3:-}"; STATUS="${4:-success}"; DURATION="${5:-}"; ERROR_TYPE="${6:-}"
        if [ -z "$USER_ID" ] || [ -z "$SKILL" ]; then
            echo "ERROR: Usage: vectorclaw insert_skill_usage <user_id> <skill_name> [action] [status] [duration_ms] [error_type]" >&2
            exit 1
        fi
        validate_enum "$STATUS" "success" "failure" "timeout" "cancelled" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_skill=$(mysql_escape "$SKILL")
        esc_action=$(mysql_escape "$ACTION")
        esc_status=$(mysql_escape "$STATUS")
        esc_error_type=$(mysql_escape "$ERROR_TYPE")
        if [ -n "$ERROR_TYPE" ]; then
            if [[ -n "$DURATION" && "$DURATION" =~ ^[0-9]+$ ]]; then
                "$SAFE_EXEC" "INSERT INTO skill_usage (user_id, skill_name, action, status, duration_ms, error_type) VALUES ('${esc_user_id}', '${esc_skill}', '${esc_action}', '${esc_status}', $DURATION, '${esc_error_type}')"
            else
                "$SAFE_EXEC" "INSERT INTO skill_usage (user_id, skill_name, action, status, error_type) VALUES ('${esc_user_id}', '${esc_skill}', '${esc_action}', '${esc_status}', '${esc_error_type}')"
            fi
        else
            if [[ -n "$DURATION" && "$DURATION" =~ ^[0-9]+$ ]]; then
                "$SAFE_EXEC" "INSERT INTO skill_usage (user_id, skill_name, action, status, duration_ms) VALUES ('${esc_user_id}', '${esc_skill}', '${esc_action}', '${esc_status}', $DURATION)"
            else
                "$SAFE_EXEC" "INSERT INTO skill_usage (user_id, skill_name, action, status) VALUES ('${esc_user_id}', '${esc_skill}', '${esc_action}', '${esc_status}')"
            fi
        fi
        ;;

    insert_relationship)
        # Usage: vectorclaw insert_relationship <user_id> <related_user_id> <type> [strength] [trust] [notes]
        USER_ID="${1:-}"; RELATED="${2:-}"; TYPE="${3:-acquaintance}"; STRENGTH="${4:-5}"; TRUST="${5:-5}"; NOTES="${6:-}"
        if [ -z "$USER_ID" ] || [ -z "$RELATED" ]; then
            echo "ERROR: Usage: vectorclaw insert_relationship <user_id> <related_user_id> <type> [strength] [trust] [notes]" >&2
            exit 1
        fi
        validate_enum "$TYPE" "friend" "close_friend" "family" "colleague" "acquaintance" "blocked" "mentor" "mentee" "rival" "other" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_related=$(mysql_escape "$RELATED")
        esc_type=$(mysql_escape "$TYPE")
        esc_notes=$(mysql_escape "$NOTES")
        if [[ "$STRENGTH" =~ ^[0-9]+$ ]] && [[ "$TRUST" =~ ^[0-9]+$ ]]; then
            "$SAFE_EXEC" "INSERT INTO user_relationships (user_id, related_user_id, relationship_type, strength, trust_level, notes) VALUES ('${esc_user_id}', '${esc_related}', '${esc_type}', $STRENGTH, $TRUST, '${esc_notes}') ON DUPLICATE KEY UPDATE relationship_type='${esc_type}', strength=$STRENGTH, trust_level=$TRUST, notes='${esc_notes}'"
        else
            echo "ERROR: strength and trust must be numeric" >&2
            exit 1
        fi
        ;;

    insert_mood)
        # Usage: vectorclaw insert_mood <user_id> <mood> [intensity] [trigger_topic] [confidence]
        USER_ID="${1:-}"; MOOD="${2:-}"; INTENSITY="${3:-0.5}"; TRIGGER="${4:-}"; CONFIDENCE="${5:-0.7}"
        if [ -z "$USER_ID" ] || [ -z "$MOOD" ]; then
            echo "ERROR: Usage: vectorclaw insert_mood <user_id> <mood> [intensity] [trigger_topic] [confidence]" >&2
            exit 1
        fi
        validate_enum "$MOOD" "happy" "excited" "calm" "neutral" "tired" "stressed" "frustrated" "sad" "angry" "anxious" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_mood=$(mysql_escape "$MOOD")
        esc_trigger=$(mysql_escape "$TRIGGER")
        if [[ ! "$INTENSITY" =~ ^[0-9]*\.?[0-9]+$ ]]; then
            echo "ERROR: intensity must be numeric" >&2
            exit 1
        fi
        if [[ ! "$CONFIDENCE" =~ ^[0-9]*\.?[0-9]+$ ]]; then
            echo "ERROR: confidence must be numeric" >&2
            exit 1
        fi
        "$SAFE_EXEC" "INSERT INTO user_mood (user_id, mood_state, intensity, trigger_topic, confidence) VALUES ('${esc_user_id}', '${esc_mood}', ${INTENSITY}, '${esc_trigger}', ${CONFIDENCE})"
        ;;

    insert_reminder)
        # Usage: vectorclaw insert_reminder <user_id> <trigger_type> <condition> <text> [priority]
        USER_ID="${1:-}"; TRIGGER_TYPE="${2:-}"; CONDITION="${3:-}"; TEXT="${4:-}"; PRIORITY="${5:-medium}"
        if [ -z "$USER_ID" ] || [ -z "$TRIGGER_TYPE" ] || [ -z "$CONDITION" ] || [ -z "$TEXT" ]; then
            echo "ERROR: Usage: vectorclaw insert_reminder <user_id> <trigger_type> <condition> <text> [priority]" >&2
            exit 1
        fi
        validate_enum "$TRIGGER_TYPE" "time_based" "event_based" "pattern_based" "followup" || exit 1
        validate_enum "$PRIORITY" "low" "medium" "high" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_type=$(mysql_escape "$TRIGGER_TYPE")
        esc_condition=$(mysql_escape "$CONDITION")
        esc_text=$(mysql_escape "$TEXT")
        esc_priority=$(mysql_escape "$PRIORITY")
        "$SAFE_EXEC" "INSERT INTO proactive_reminders (user_id, trigger_type, trigger_condition, reminder_text, priority) VALUES ('${esc_user_id}', '${esc_type}', '${esc_condition}', '${esc_text}', '${esc_priority}')"
        ;;

    insert_thought)
        # Usage: vectorclaw insert_thought <user_id> <thought> [type] [channel_id]
        USER_ID="${1:-}"; THOUGHT="${2:-}"; TTYPE="${3:-reasoning}"; CHANNEL="${4:-}"
        if [ -z "$USER_ID" ] || [ -z "$THOUGHT" ]; then
            echo "ERROR: Usage: vectorclaw insert_thought <user_id> <thought> [type] [channel_id]" >&2
            exit 1
        fi
        validate_enum "$TTYPE" "reasoning" "observation" "decision" "reflection" "planning" || exit 1
        esc_user_id=$(mysql_escape "$USER_ID")
        esc_thought=$(mysql_escape "$THOUGHT")
        esc_type=$(mysql_escape "$TTYPE")
        esc_channel=$(mysql_escape "$CHANNEL")
        "$SAFE_EXEC" "INSERT INTO thought_stream (user_id, thought, thought_type, channel_id) VALUES ('${esc_user_id}', '${esc_thought}', '${esc_type}', '${esc_channel}')"
        ;;

    insert_learning)
        # Usage: vectorclaw insert_learning <type> <title> <description> [priority] [related_user] [related_skill]
        LTYPE="${1:-}"; TITLE="${2:-}"; DESC="${3:-}"; PRIORITY="${4:-medium}"; REL_USER="${5:-}"; REL_SKILL="${6:-}"
        if [ -z "$LTYPE" ] || [ -z "$TITLE" ] || [ -z "$DESC" ]; then
            echo "ERROR: Usage: vectorclaw insert_learning <type> <title> <description> [priority] [user] [skill]" >&2
            exit 1
        fi
        validate_enum "$LTYPE" "correction" "preference" "pattern" "error" "success" "insight" "rule" || exit 1
        validate_enum "$PRIORITY" "low" "medium" "high" "critical" || exit 1
        esc_type=$(mysql_escape "$LTYPE")
        esc_title=$(mysql_escape "$TITLE")
        esc_desc=$(mysql_escape "$DESC")
        esc_priority=$(mysql_escape "$PRIORITY")
        esc_user=$(mysql_escape "$REL_USER")
        esc_skill=$(mysql_escape "$REL_SKILL")
        "$SAFE_EXEC" "INSERT INTO agent_learnings (learning_type, title, description, priority, related_user_id, related_skill) VALUES ('${esc_type}', '${esc_title}', '${esc_desc}', '${esc_priority}', '${esc_user}', '${esc_skill}')"
        ;;

    insert_event)
        # Usage: vectorclaw insert_event <type> <title> <description> [channel_id]
        ETYPE="${1:-}"; TITLE="${2:-}"; DESC="${3:-}"; CHANNEL="${4:-}"
        if [ -z "$ETYPE" ] || [ -z "$TITLE" ]; then
            echo "ERROR: Usage: vectorclaw insert_event <type> <title> [description] [channel_id]" >&2
            exit 1
        fi
        validate_enum "$ETYPE" "milestone" "achievement" "incident" "trend" "custom" || exit 1
        esc_type=$(mysql_escape "$ETYPE")
        esc_title=$(mysql_escape "$TITLE")
        esc_desc=$(mysql_escape "$DESC")
        esc_channel=$(mysql_escape "$CHANNEL")
        "$SAFE_EXEC" "INSERT INTO community_events (event_type, title, description, channel_id) VALUES ('${esc_type}', '${esc_title}', '${esc_desc}', '${esc_channel}')"
        ;;

    help|*)
        echo "MySQLClaw — vectorclaw command wrapper (v2.0.0)"
        echo ""
        echo "Usage:"
        echo "  vectorclaw query \"SQL\"                Execute a read-only SELECT query"
        echo "  vectorclaw exec --file path.sql         Execute a SQL script"
        echo "  vectorclaw insert_interaction <uid> <dir> <topic> <sum> [sentiment] [is_important]"
        echo "  vectorclaw insert_note <uid> <note> [category] [is_pinned]"
        echo "  vectorclaw insert_context <uid> <key> <val> [type] [importance] [expires]"
        echo "  vectorclaw insert_skill_usage <uid> <skill> [action] [status] [duration] [error_type]"
        echo "  vectorclaw insert_relationship <uid> <ruid> <type> [strength] [trust] [notes]"
        echo "  vectorclaw insert_mood <uid> <mood> [intensity] [trigger] [confidence]"
        echo "  vectorclaw insert_reminder <uid> <type> <condition> <text> [priority]"
        echo "  vectorclaw insert_thought <uid> <thought> [type] [channel_id]"
        echo "  vectorclaw insert_learning <type> <title> <desc> [priority] [user] [skill]"
        echo "  vectorclaw insert_event <type> <title> [description] [channel_id]"
        echo "  vectorclaw help                         Show this help"
        echo ""
        echo "Credentials: set MYSQL_USER/MYSQL_PASSWORD env vars or .env file."
        ;;
esac
