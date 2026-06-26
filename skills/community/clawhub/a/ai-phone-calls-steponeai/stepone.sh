#!/bin/bash
# stepone.sh - Low-level Stepone AI API wrapper
# Usage: ./stepone.sh <command> [options]
#
# Commands:
#   call       - Make a call (raw JSON body; guarded)
#   callinfo   - Get call info/transcript
#   stream     - Stream real-time conversation (SSE)
#   balance    - Check account balance
#   version    - Check skill version

set -e

SKILL_VERSION="1.0.0"
API_BASE="https://open-skill-api.steponeai.com"
MAX_RECIPIENTS=1

require_python3() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Error: python3 is required to encode JSON safely"
        exit 1
    fi
}

# JSON转义函数
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

normalize_json_body() {
    local raw_json="$1"
    RAW_JSON="$raw_json" python3 - <<'PY'
import json
import os
import sys

raw = os.environ.get("RAW_JSON", "")
try:
    payload = json.loads(raw)
except Exception as exc:
    print(f"Error: invalid JSON body: {exc}", file=sys.stderr)
    sys.exit(1)

# Keep the HTTP body ASCII-only so prompt text survives non-UTF-8 shells,
# terminals, logs, and middleware. The provider receives normal Unicode after
# JSON decoding.
print(json.dumps(payload, ensure_ascii=True, separators=(",", ":")))
PY
}

json_string_field() {
    local raw_json="$1"
    local field="$2"
    RAW_JSON="$raw_json" JSON_FIELD="$field" python3 - <<'PY'
import json
import os
import sys

try:
    payload = json.loads(os.environ.get("RAW_JSON", ""))
except Exception:
    sys.exit(1)

value = payload.get(os.environ.get("JSON_FIELD", ""))
if isinstance(value, str):
    print(value)
PY
}

# Remove service-side instruction payloads before printing API responses to an
# agent. These fields are not call data and should not become prompt context.
sanitize_json_response() {
    local response="$1"
    if command -v python3 >/dev/null 2>&1; then
        RESPONSE_TO_SANITIZE="$response" python3 - <<'PY'
import json
import os

raw = os.environ.get("RESPONSE_TO_SANITIZE", "")
try:
    data = json.loads(raw)
except Exception:
    print(raw)
else:
    def strip_instruction_fields(value):
        if isinstance(value, dict):
            value.pop("LLM_SYSTEM_INSTRUCTION", None)
            for child in value.values():
                strip_instruction_fields(child)
        elif isinstance(value, list):
            for child in value:
                strip_instruction_fields(child)

    strip_instruction_fields(data)
    print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
PY
        return
    fi
    echo "$response" | sed 's/,"LLM_SYSTEM_INSTRUCTION":{[^}]*}//g'
}

# 验证手机号
validate_phone() {
    local phone="$1"
    if [[ ! "$phone" =~ ^1[3-9][0-9]{9}$ ]]; then
        echo "Error: Invalid phone number format (must be 11 digits starting with 1)"
        return 1
    fi
    return 0
}

# 验证call_id
validate_call_id() {
    local call_id="$1"
    if [[ ! "$call_id" =~ ^[a-zA-Z0-9^_-]+$ ]]; then
        echo "Error: Invalid call_id format"
        return 1
    fi
    return 0
}

extract_json_string_field() {
    local json="$1"
    local field="$2"
    echo "$json" | grep -o "\"$field\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | head -1 | sed 's/.*"\([^"]*\)"$/\1/'
}

validate_phone_list() {
    local phones="$1"
    local count=0
    local phone

    if [[ -z "$phones" ]]; then
        echo "Error: raw call JSON must include a phones string"
        return 1
    fi

    IFS=',' read -ra PHONE_ITEMS <<< "$phones"
    for phone in "${PHONE_ITEMS[@]}"; do
        phone="$(echo "$phone" | xargs)"
        [[ -z "$phone" ]] && continue
        count=$((count + 1))
        if ! validate_phone "$phone"; then
            return 1
        fi
    done

    if [[ "$count" -eq 0 ]]; then
        echo "Error: raw call JSON must include at least one phone number"
        return 1
    fi

    if [[ "$count" -gt "$MAX_RECIPIENTS" ]]; then
        echo "Error: Too many recipients. Raw call allows at most $MAX_RECIPIENTS recipient per invocation."
        return 1
    fi

    return 0
}

confirm_raw_call() {
    local phones="$1"
    local requirement="$2"

    if [[ "${STEPONEAI_ENABLE_RAW_CALL:-}" != "1" ]]; then
        echo "Error: raw call is disabled by default."
        echo "Use ./callout.sh for normal calls, or set STEPONEAI_ENABLE_RAW_CALL=1 for advanced/manual use."
        exit 1
    fi

    echo "⚠️  Raw JSON call confirmation required"
    echo "Recipient(s): $phones"
    echo "Task: $requirement"
    echo "Billing: this may consume Stepone AI call credit."
    echo "Consent: continue only if you are authorized to call this recipient for this purpose."
    echo ""
    read -r -p "Type RAWCALL to place this raw call, or anything else to cancel: " CONFIRMATION
    if [[ "$CONFIRMATION" != "RAWCALL" ]]; then
        echo "Cancelled: raw call was not initiated."
        exit 1
    fi
}

# 加载API key
load_api_key() {
    if [[ -z "$STEPONEAI_API_KEY" ]]; then
        echo "Error: STEPONEAI_API_KEY not set"
        echo "Set it in your environment before running this script."
        exit 1
    fi
}

COMMAND="${1:-help}"

case "$COMMAND" in
    help|--help|-h)
        echo "Stepone AI API Wrapper (v${SKILL_VERSION})"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  call '<json>'       Make a guarded raw call with JSON body"
        echo "  callinfo <id>     Get call info by call_id"
        echo "  stream <id>       Stream real-time conversation (SSE)"
        echo "  balance           Check account balance"
        echo "  version           Check skill version"
        echo "  help              Show this help"
        echo ""
        echo "Examples:"
        echo "  STEPONEAI_ENABLE_RAW_CALL=1 $0 call '{\"phones\": \"13800138000\", \"user_requirement\": \"Hello\"}'"
        echo "  $0 callinfo abc123def456"
        echo "  $0 stream abc123def456"
        ;;
        
    call)
        load_api_key
        if [[ -z "$2" ]]; then
            echo "Usage: $0 call '<json_body>'"
            exit 1
        fi
        require_python3
        RAW_BODY="$2"
        NORMALIZED_BODY=$(normalize_json_body "$RAW_BODY")
        if [[ -n "${3:-}" ]]; then
            echo "Error: unknown option ${3:-}"
            exit 1
        fi

        RAW_PHONES=$(json_string_field "$RAW_BODY" "phones")
        RAW_REQUIREMENT=$(json_string_field "$RAW_BODY" "user_requirement")
        if ! validate_phone_list "$RAW_PHONES"; then
            exit 1
        fi
        if [[ -z "$RAW_REQUIREMENT" ]]; then
            echo "Error: raw call JSON must include user_requirement"
            exit 1
        fi
        confirm_raw_call "$RAW_PHONES" "$RAW_REQUIREMENT"
        
        RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/callinfo/initiate_call" \
            -H "Content-Type: application/json; charset=utf-8" \
            -H "X-API-Key: $STEPONEAI_API_KEY" \
            -H "X-Skill-Version: $SKILL_VERSION" \
            --data-binary "$NORMALIZED_BODY")
        echo "$RESPONSE"
        ;;
        
    callinfo)
        load_api_key
        if [[ -z "$2" ]]; then
            echo "Usage: $0 callinfo <call_id>"
            exit 1
        fi
        
        if ! validate_call_id "$2"; then
            exit 1
        fi
        
        RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/callinfo/search_callinfo" \
            -H "Content-Type: application/json; charset=utf-8" \
            -H "X-API-Key: $STEPONEAI_API_KEY" \
            -H "X-Skill-Version: $SKILL_VERSION" \
            -d "{\"call_id\": \"$2\"}")
        RESPONSE=$(sanitize_json_response "$RESPONSE")
        echo "$RESPONSE"
        ;;

    stream)
        load_api_key
        if [[ -z "$2" ]]; then
            echo "Usage: $0 stream <call_id>"
            exit 1
        fi

        if ! validate_call_id "$2"; then
            exit 1
        fi

        SAFE_ID=$(json_escape "$2")
        curl -sN -X POST "${API_BASE}/api/v1/callinfo/stream_chat_history" \
            -H "Content-Type: application/json; charset=utf-8" \
            -H "X-API-Key: $STEPONEAI_API_KEY" \
            -H "X-Skill-Version: $SKILL_VERSION" \
            -d "{\"call_id\": \"$SAFE_ID\"}"
        ;;
        
    balance)
        echo "Check your balance at: https://open-skill.steponeai.com"
        ;;

    version)
        echo "Local skill version: $SKILL_VERSION"
        REMOTE=$(curl -s "${API_BASE}/api/v1/callinfo/skill_version" 2>/dev/null)
        REMOTE_VER=$(echo "$REMOTE" | grep -o '"skill_version":"[^"]*"' | cut -d'"' -f4)
        if [[ -n "$REMOTE_VER" ]]; then
            echo "Remote skill version: $REMOTE_VER"
            if [[ "$SKILL_VERSION" != "$REMOTE_VER" ]]; then
                echo "⚠️  Version mismatch! Please update skills."
            else
                echo "✅ Up to date."
            fi
        fi
        ;;
        
    *)
        echo "Unknown command: $COMMAND"
        echo "Run '$0 help' for usage"
        exit 1
        ;;
esac
