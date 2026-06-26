#!/bin/bash
# AnythingLLM RAG API Client
# Usage: anythingllm.sh <command> [args]
#
# Commands:
#   query <question>              - Query the workspace with RAG
#   upload <file> [workspace]     - Upload a document
#   upload-text <text> <title>    - Upload raw text as document
#   list-docs                     - List documents in workspace
#   workspaces                    - List all workspaces
#   health                        - Check API health

# Config - update these if needed
ANYTHINGLLM_URL="${ANYTHINGLLM_URL:-http://localhost:3001}"
ANYTHINGLLM_API_KEY="${ANYTHINGLLM_API_KEY:-JYF2P4K-SQ6MKA3-NGW734W-6CVY672}"
DEFAULT_WORKSPACE="${ANYTHINGLLM_WORKSPACE:-e2c3afc4-d5fc-44c9-964a-7a571e7ee49f}"

api_call() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    local curl_cmd="curl -s -w '\n%{http_code}' -X ${method} \
        -H 'Authorization: Bearer ${ANYTHINGLLM_API_KEY}' \
        -H 'Content-Type: application/json' \
        '${ANYTHINGLLM_URL}/api${endpoint}'"
    
    if [ -n "$data" ]; then
        curl_cmd="${curl_cmd} -d '${data}'"
    fi
    
    local response=$(eval "$curl_cmd")
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 400 ] 2>/dev/null; then
        echo "Error (HTTP $http_code): $body" >&2
        return 1
    fi
    
    echo "$body"
}

query_rag() {
    local question="$1"
    local workspace="${2:-$DEFAULT_WORKSPACE}"
    
    local payload=$(cat <<EOF
{
    "message": "${question}",
    "mode": "query"
}
EOF
)
    
    curl -s -X POST \
        -H "Authorization: Bearer ${ANYTHINGLLM_API_KEY}" \
        -H "Content-Type: application/json" \
        "${ANYTHINGLLM_URL}/api/v1/workspace/${workspace}/chat" \
        -d "$payload"
}

upload_file() {
    local file="$1"
    local workspace="${2:-$DEFAULT_WORKSPACE}"
    
    if [ ! -f "$file" ]; then
        echo "Error: File not found: $file" >&2
        return 1
    fi
    
    curl -s -X POST \
        -H "Authorization: Bearer ${ANYTHINGLLM_API_KEY}" \
        -F "file=@${file}" \
        -F "addToWorkspaces=${workspace}" \
        "${ANYTHINGLLM_URL}/api/v1/document/upload"
}

upload_text() {
    local text="$1"
    local title="$2"
    local workspace="${3:-$DEFAULT_WORKSPACE}"
    
    local payload=$(cat <<EOF
{
    "textContent": "$(echo "$text" | sed 's/"/\\"/g' | tr '\n' ' ')",
    "metadata": {
        "title": "${title}"
    },
    "addToWorkspaces": "${workspace}"
}
EOF
)
    
    api_call "POST" "/v1/document/raw-text" "$payload"
}

list_docs() {
    local workspace="${1:-$DEFAULT_WORKSPACE}"
    # Use workspace documents endpoint
    curl -s -X GET \
        -H "Authorization: Bearer ${ANYTHINGLLM_API_KEY}" \
        -H "Accept: application/json" \
        "${ANYTHINGLLM_URL}/api/v1/workspace/${workspace}/documents"
}

list_workspaces() {
    api_call "GET" "/v1/workspaces"
}

health_check() {
    api_call "GET" "/v1/auth"
}

# Main command handler
case "$1" in
    query)
        query_rag "$2" "$3"
        ;;
    upload)
        upload_file "$2" "$3"
        ;;
    upload-text)
        upload_text "$2" "$3" "$4"
        ;;
    list-docs)
        list_docs "$2"
        ;;
    workspaces)
        list_workspaces
        ;;
    health)
        health_check
        ;;
    *)
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  query <question> [workspace]     - Query the workspace with RAG"
        echo "  upload <file> [workspace]        - Upload a document"
        echo "  upload-text <text> <title>       - Upload raw text as document"
        echo "  list-docs [workspace]            - List documents in workspace"
        echo "  workspaces                       - List all workspaces"
        echo "  health                           - Check API health"
        exit 1
        ;;
esac
