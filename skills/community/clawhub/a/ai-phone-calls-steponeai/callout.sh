#!/bin/bash
# callout.sh - Make an AI phone call via Stepone AI
# Usage: ./callout.sh <phone_number> <task> [options]
#
# Examples:
#   ./callout.sh "13800138000" "通知您明天上午9点开会"
#   ./callout.sh "13800138000" "提醒他明天上班" --wait

set -e

SKILL_VERSION="1.0.0"
API_BASE="https://open-skill-api.steponeai.com"
MAX_RECIPIENTS=1

require_python3() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Error: python3 is required to encode the prompt safely as JSON"
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

build_call_request_body() {
    local phone="$1"
    local task="$2"
    REQUEST_PHONE="$phone" REQUEST_TASK="$task" python3 - <<'PY'
import json
import os

payload = {
    "phones": os.environ["REQUEST_PHONE"],
    "user_requirement": os.environ["REQUEST_TASK"],
}

# Keep the HTTP body ASCII-only so prompts cannot be corrupted by an
# intermediate process that guesses the wrong text encoding.
print(json.dumps(payload, ensure_ascii=True, separators=(",", ":")))
PY
}

# 验证手机号
validate_phone() {
    local phone="$1"
    if [[ ! "$phone" =~ ^1[3-9][0-9]{9}$ ]]; then
        echo "Error: Invalid phone number (must be 11 digits starting with 1)"
        return 1
    fi
    return 0
}

confirm_real_call() {
    local phone="$1"
    local task="$2"

    echo "⚠️  Real outbound phone call confirmation required"
    echo "Recipient: $phone"
    echo "Task: $task"
    echo "Billing: this may consume Stepone AI call credit and may be subject to telecom/compliance rules."
    echo "Consent: only continue if you are authorized to call this recipient for this purpose."
    echo ""
    read -r -p "Type CALL to place this call, or anything else to cancel: " CONFIRMATION
    if [[ "$CONFIRMATION" != "CALL" ]]; then
        echo "Cancelled: call was not initiated."
        exit 1
    fi
}

# 检查帮助
for arg in "$@"; do
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        echo "Usage: $0 <phone_number> <task> [options]"
        echo ""
        echo "Arguments:"
        echo "  phone_number    Phone number (11 digits, e.g., 13800138000)"
        echo "  task            Instructions for the AI agent"
        echo ""
        echo "Options:"
        echo "  --wait                Wait for call to complete and show result"
        echo "  --help                Show this help"
        exit 0
    fi
done

if [[ -z "$STEPONEAI_API_KEY" ]]; then
    echo "Error: STEPONEAI_API_KEY not set"
    echo "Set it in your environment before running this script."
    exit 1
fi

# 解析参数
PHONE_NUMBER=""
TASK=""
WAIT_FOR_COMPLETION="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --wait)
            WAIT_FOR_COMPLETION="true"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <phone_number> <task> [options]"
            echo ""
            echo "Arguments:"
            echo "  phone_number    Phone number (11 digits, e.g., 13800138000)"
            echo "  task            Instructions for the AI agent"
            echo ""
            echo "Options:"
            echo "  --wait                Wait for call to complete and show result"
            echo "  --help                Show this help"
            exit 0
            ;;
        *)
            if [[ "$1" == --* ]]; then
                echo "Error: unknown option $1"
                exit 1
            elif [[ -z "$PHONE_NUMBER" ]]; then
                PHONE_NUMBER="$1"
            elif [[ -z "$TASK" ]]; then
                TASK="$1"
            else
                echo "Error: too many arguments"
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ -z "$PHONE_NUMBER" ]] || [[ -z "$TASK" ]]; then
    echo "Error: Phone number and task are required"
    echo "Usage: $0 <phone_number> <task> [options]"
    exit 1
fi

# 验证手机号
if [[ "$PHONE_NUMBER" == *","* ]]; then
    RECIPIENT_COUNT=$(echo "$PHONE_NUMBER" | tr ',' '\n' | sed '/^[[:space:]]*$/d' | wc -l | tr -d ' ')
else
    RECIPIENT_COUNT=1
fi

if [[ "$RECIPIENT_COUNT" -gt "$MAX_RECIPIENTS" ]]; then
    echo "Error: Too many recipients. This skill allows at most $MAX_RECIPIENTS recipient per invocation."
    echo "Run one confirmed call at a time to avoid unintended batch dialing."
    exit 1
fi

if ! validate_phone "$PHONE_NUMBER"; then
    exit 1
fi

confirm_real_call "$PHONE_NUMBER" "$TASK"

# 构建请求
require_python3
REQUEST_BODY=$(build_call_request_body "$PHONE_NUMBER" "$TASK")

# 发起呼叫
echo "📞 Initiating call to $PHONE_NUMBER..."
echo "📝 Task: $TASK"
echo ""

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/callinfo/initiate_call" \
    -H "Content-Type: application/json; charset=utf-8" \
    -H "X-API-Key: $STEPONEAI_API_KEY" \
    -H "X-Skill-Version: $SKILL_VERSION" \
    --data-binary "$REQUEST_BODY")

# 检查错误
SUCCESS=$(echo "$RESPONSE" | grep -o '"success":[^,}]*' | cut -d':' -f2)
if [[ "$SUCCESS" != "true" ]]; then
    ERROR_MSG=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "❌ Error: $ERROR_MSG"
    exit 1
fi

# 提取call_id
CALL_ID=$(echo "$RESPONSE" | grep -o '"call_ids":\["[^"]*"\]' | grep -o '\[".*"\]' | sed 's/\["//;s/"\]//')
if [[ -z "$CALL_ID" ]]; then
    CALL_ID=$(echo "$RESPONSE" | grep -o '"provider_call_id":"[^"]*"' | cut -d'"' -f4)
fi

if [[ -z "$CALL_ID" ]]; then
    echo "❌ Error: No call ID returned"
    echo "$RESPONSE"
    exit 1
fi

echo "✅ Call initiated!"
echo "📱 Call ID: $CALL_ID"
echo ""

# 如果有--wait标志，等待完成
if [[ "$WAIT_FOR_COMPLETION" == "true" ]]; then
    echo "⏳ Waiting for call to complete..."
    
    while true; do
        sleep 10
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        CALL_STATUS=$("$SCRIPT_DIR/callinfo.sh" "$CALL_ID" --json 2>/dev/null || echo '{}')
        DURATION=$(echo "$CALL_STATUS" | grep -o '"duration_seconds":[0-9]*' | cut -d':' -f2)
        
        if [[ -n "$DURATION" && "$DURATION" != "null" ]]; then
            echo ""
            echo "📋 Call completed!"
            "$SCRIPT_DIR/callinfo.sh" "$CALL_ID"
            break
        fi
        
        echo -n "."
    done
else
    echo "💡 Check status with: ./callinfo.sh $CALL_ID"
fi
