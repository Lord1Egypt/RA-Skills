#!/usr/bin/env bash
# Dify Workflow Script - CLI for querying knowledge base and executing workflows
# Usage: ./dify-workflow.sh <query> [options]
# Options: --wf WORKFLOW_ID, --chat, --conv CONVERSATION_ID

set -e

# Configuration from environment or defaults
DIFY_BASE_URL="${DIFY_BASE_URL:-http://10.10.10.159/v1}"
DIFY_API_KEY="${DIFY_API_KEY:-app-jUhDcPj3lcnEG04JW4gRsfyy}"
DEFAULT_TIMEOUT=120

# Parse arguments
QUERY=""
WORKFLOW_ID=""
CONVERSATION_ID=""
USE_CHAT_MODE=false
REQUEST_MODE="blocking"

while [[ $# -gt 0 ]]; do
    case $1 in
        --wf)
            WORKFLOW_ID="$2"
            shift 2
            ;;
        --chat|--chatapp)
            USE_CHAT_MODE=true
            shift
            ;;
        --conv|--conversation-id)
            CONVERSATION_ID="$2"
            shift 2
            ;;
        --stream)
            REQUEST_MODE="streaming"
            shift
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            if [ -z "$QUERY" ]; then
                QUERY="$1"
            elif [ -n "$WORKFLOW_ID" ] && [[ ! "$1" =~ ^-- ]]; then
                CONVERSATION_ID="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <query> [options]" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  $0 '你好' --chat                              # ChatApp mode (default)" >&2
    echo "  $0 '如何部署？' --wf wf_123456                # Workflow mode" >&2
    echo "  $0 '继续聊天' --conv conv_xyz789               # Multi-turn chat" >&2
    exit 1
fi

# Build API endpoints (base URL already includes /v1)
WORKFLOW_ENDPOINT="${DIFY_BASE_URL}/workflows/run"
CHAT_ENDPOINT="${DIFY_BASE_URL}/chat-messages"

# Log start message
echo "🔄 Connecting to Dify at: ${DIFY_BASE_URL}"
if [ "$USE_CHAT_MODE" = true ]; then
    echo "📡 API Endpoint: ${CHAT_ENDPOINT}"
    echo "🤖 Mode: ChatApp (chat-messages)"
elif [ -n "$WORKFLOW_ID" ]; then
    echo "📡 API Endpoint: ${WORKFLOW_ENDPOINT}"
    echo "⚙️  Mode: Workflow"
    echo "📋 Workflow ID: ${WORKFLOW_ID}"
else
    echo "📡 API Endpoint: ${WORKFLOW_ENDPOINT} (generic)"
    echo "⚙️  Mode: Workflow (default)"
fi

if [ -n "$CONVERSATION_ID" ]; then
    echo "💬 Conversation ID: ${CONVERSATION_ID} (multi-turn)"
fi
echo "⏱️  Timeout: ${DEFAULT_TIMEOUT}s, Response mode: ${REQUEST_MODE}"

# Prepare request body based on mode
if [ "$USE_CHAT_MODE" = true ]; then
    # ChatApp mode with conversation_id
    if [ -n "$CONVERSATION_ID" ]; then
        WORKFLOW_PAYLOAD="{\"inputs\": {}, \"query\": \"${QUERY}\", \"conversation_id\": \"${CONVERSATION_ID}\", \"response_mode\": \"${REQUEST_MODE}\", \"user\": \"openclaw-user\", \"files\": []}"
    else
        # ChatApp mode without conversation_id (auto-generate)
        WORKFLOW_PAYLOAD="{\"inputs\": {}, \"query\": \"${QUERY}\", \"response_mode\": \"${REQUEST_MODE}\", \"user\": \"openclaw-user\", \"files\": []}"
    fi
elif [ -n "$WORKFLOW_ID" ]; then
    # Workflow mode with workflow ID
    WORKFLOW_PAYLOAD="{\"workflow_id\": \"${WORKFLOW_ID}\", \"inputs\": {\"query\": \"${QUERY}\"}, \"response_mode\": \"${REQUEST_MODE}\", \"user\": \"openclaw-user\"}"
else
    # Generic workflow execution (may not work without workflow_id)
    WORKFLOW_PAYLOAD="{\"inputs\": {\"query\": \"${QUERY}\"}, \"response_mode\": \"${REQUEST_MODE}\", \"user\": \"openclaw-user\"}"
fi

# Determine which endpoint to use
if [ "$USE_CHAT_MODE" = true ]; then
    ENDPOINT="$CHAT_ENDPOINT"
else
    ENDPOINT="$WORKFLOW_ENDPOINT"
fi

# Execute request with timeout
echo "" >&2
echo "🚀 Sending request..." >&2
RESPONSE=$(curl -s -X POST "$ENDPOINT" \
    -H "Authorization: Bearer ${DIFY_API_KEY}" \
    -H "Content-Type: application/json" \
    --max-time "$DEFAULT_TIMEOUT" \
    --data-binary "${WORKFLOW_PAYLOAD}")

# Check if it's an error response
if echo "$RESPONSE" | grep -q '"error_code"'; then
    ERROR_CODE=$(echo "$RESPONSE" | grep -oE '"error_code":"[^"]+"' | sed 's/"error_code":"//;s/"$//')
    ERROR_MSG=$(echo "$RESPONSE" | grep -oE '"message":"[^"]+"' | sed 's/"message":"//;s/"$//')
    
    echo "" >&2
    echo "❌ Dify API Error (Code: ${ERROR_CODE})" >&2
    echo "${ERROR_MSG:-Unknown error}" >&2
    
    # Provide helpful suggestions based on error code
    case "$ERROR_CODE" in
        "not_workflow_app")
            echo "" >&2
            echo "💡 This app is not configured as a Workflow:" >&2
            echo "   - Use --chat flag for ChatApp mode: $0 'query' --chat" >&2
            echo "   - Or specify a valid workflow ID: $0 'query' --wf wf_xxx" >&2
            ;;
        "conversation_id_invalid")
            echo "" >&2
            echo "💡 Invalid conversation ID:" >&2
            echo "   - Start fresh without --conv option" >&2
            echo "   - Get a new conversation ID from Dify dashboard" >&2
            ;;
        "workflow_not_found")
            echo "" >&2
            echo "💡 Workflow not found:" >&2
            echo "   - Verify workflow ID: ${WORKFLOW_ID}" >&2
            echo "   - Check it exists in your Dify app" >&2
            ;;
        *)
            echo "💡 For other errors, check your Dify configuration and API credentials." >&2
            ;;
    esac
    exit 1
fi

# Create a temporary Python script for extracting answer and decoding Unicode
PYTHON_SCRIPT=$(cat << 'PYEOF'
import sys
import json

response = sys.stdin.read()

try:
    data = json.loads(response)
    
    # Extract answer from various possible locations
    answer = None
    
    if "answer" in data:
        answer = data["answer"]
    elif "data" in data and isinstance(data["data"], dict):
        if "answer" in data["data"]:
            answer = data["data"]["answer"]
        elif "outputs" in data["data"] and isinstance(data["data"]["outputs"], dict):
            if "answer" in data["data"]["outputs"]:
                answer = data["data"]["outputs"]["answer"]
    
    if answer is None:
        print("ERROR_NO_ANSWER")
        sys.exit(1)
    
    # Extract conversation_id for multi-turn support
    conv_id = data.get("conversation_id", "")
    
    # Output using a delimiter that won't appear in normal text
    separator = "\x01CONV_SEP\x01"
    print(f"{answer}{separator}{conv_id}")
    
except Exception as e:
    print(f"ERROR_PARSE:{e}", file=sys.stderr)
    sys.exit(1)
PYEOF
)

# Execute Python script
RESULT=$(echo "$RESPONSE" | python3 -c "$PYTHON_SCRIPT")

# Extract answer and conversation_id
ANSWER="${RESULT%%$'\x01CONV_SEP\x01'*}"
CONVERSATION_ID_FROM_RESPONSE="${RESULT##*$'\x01CONV_SEP\x01'}"

# Output result
if [[ "$ANSWER" == ERROR* ]]; then
    echo ""
    echo "⚠️  Unexpected response format:"
    echo ""
    echo "$RESPONSE"
    echo ""
    
    echo "💡 Tips for troubleshooting:" >&2
    echo "   - Use --chat mode if your app is a ChatApp: $0 'query' --chat" >&2
    echo "   - Specify workflow ID for Workflow apps: $0 'query' --wf wf_xxx" >&2
    echo "   - Check Dify dashboard for correct API configuration" >&2
    
    exit 1
fi

echo ""
echo "✅ Dify Response:"
echo ""
echo "$ANSWER"

if [ -n "$CONVERSATION_ID_FROM_RESPONSE" ]; then
    echo ""
    echo "💬 New conversation ID: ${CONVERSATION_ID_FROM_RESPONSE}"
fi

exit 0
