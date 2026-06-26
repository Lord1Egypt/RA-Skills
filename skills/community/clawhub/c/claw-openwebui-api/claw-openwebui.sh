#!/bin/bash
# Claw OpenWebUI - Open WebUI API 技能

# 設定
WEBUI_URL="${OPENWEBUI_URL:-http://192.168.0.176:3000}"
API_KEY="${OPENWEBUI_API_KEY:-}"

# 顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 檢查 API Key
check_api_key() {
    if [ -z "$API_KEY" ]; then
        echo -e "${RED}錯誤：請設定 OPENWEBUI_API_KEY 環境變數${NC}"
        echo "export OPENWEBUI_API_KEY=\"your-jwt-token\""
        exit 1
    fi
}

# 測試連線
ping_webui() {
    check_api_key
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$WEBUI_URL" 2>/dev/null)
    if [ "$status" = "200" ]; then
        echo -e "${GREEN}✅ Open WebUI 連線正常${NC}"
    else
        echo -e "${RED}❌ Open WebUI 無法連線 (HTTP $status)${NC}"
    fi
}

# 列出模型
list_models() {
    check_api_key
    echo -e "${CYAN}📦 可用模型：${NC}"
    curl -s "$WEBUI_URL/api/v1/models" \
        -H "Authorization: Bearer $API_KEY" | \
        jq -r '.data[] | "  • \(.id) (\(.name))"' 2>/dev/null || echo "  無法取得模型列表"
}

# 聊天
chat() {
    check_api_key
    local model="$1"
    local message="$2"
    
    if [ -z "$model" ] || [ -z "$message" ]; then
        echo "用法: claw-openwebui chat <model> <message>"
        return 1
    fi
    
    curl -s -X POST "$WEBUI_URL/api/chat/completions" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"$message\"}], \"stream\": false}" | \
        jq -r '.choices[0].message.content' 2>/dev/null
}

# ===== 知識庫功能 =====

# 列出知識庫
list_knowledge() {
    check_api_key
    echo -e "${CYAN}📚 知識庫列表：${NC}"
    curl -s "$WEBUI_URL/api/v1/knowledge/" \
        -H "Authorization: Bearer $API_KEY" | \
        jq -r '.items[] | "  • \(.name) (ID: \(.id))"' 2>/dev/null || echo "  無知識庫"
}

# 建立知識庫
create_knowledge() {
    check_api_key
    local name="$1"
    local description="${2:-}"
    
    if [ -z "$name" ]; then
        echo "用法: claw-openwebui create-knowledge <名稱> [描述]"
        return 1
    fi
    
    local response=$(curl -s -X POST "$WEBUI_URL/api/v1/knowledge/" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\", \"description\": \"$description\"}")
    
    local kn_id=$(echo "$response" | jq -r '.id' 2>/dev/null)
    
    if [ "$kn_id" != "null" ] && [ -n "$kn_id" ]; then
        echo -e "${GREEN}✅ 知識庫建立成功！ID: $kn_id${NC}"
    else
        echo -e "${RED}❌ 建立失敗${NC}"
    fi
}

# 上傳並添加到知識庫（自動流程）
upload_to_knowledge() {
    check_api_key
    local file_path="$1"
    local knowledge_name="$2"
    
    if [ -z "$file_path" ]; then
        echo "用法: claw-openwebui upload-rag <檔案路徑> [知識庫名稱]"
        echo "範例: claw-openwebui upload-rag /path/to/file.txt test3"
        return 1
    fi
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}錯誤：檔案不存在: $file_path${NC}"
        return 1
    fi
    
    local knowledge_id=""
    
    # 如果指定了知識庫名稱，用名稱查詢 ID
    if [ -n "$knowledge_name" ]; then
        knowledge_id=$(curl -s "$WEBUI_URL/api/v1/knowledge/" \
            -H "Authorization: Bearer $API_KEY" | \
            jq -r ".items[] | select(.name == \"$knowledge_name\") | .id" 2>/dev/null)
        
        if [ -z "$knowledge_id" ] || [ "$knowledge_id" = "null" ]; then
            echo -e "${RED}錯誤：知識庫 '$knowledge_name' 不存在！${NC}"
            echo "請先建立知識庫或確認名稱正確"
            return 1
        fi
        echo -e "${CYAN}使用知識庫: $knowledge_name (ID: $knowledge_id)${NC}"
    else
        # 沒指定知識庫，要求使用者輸入
        echo -e "${RED}錯誤：請指定知識庫名稱${NC}"
        echo "用法: claw-openwebui upload-rag <檔案路徑> <知識庫名稱>"
        echo ""
        echo "現有知識庫："
        curl -s "$WEBUI_URL/api/v1/knowledge/" \
            -H "Authorization: Bearer $API_KEY" | \
            jq -r '.items[] | "  • \(.name) (ID: \(.id))"' 2>/dev/null
        return 1
    fi
    
    echo -e "${YELLOW}📤 上傳檔案並添加到知識庫...${NC}"
    
    # 上傳檔案
    local upload_response=$(curl -s -X POST "$WEBUI_URL/api/v1/files/" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Accept: application/json" \
        -F "file=@$file_path")
    
    local file_id=$(echo "$upload_response" | jq -r '.id' 2>/dev/null)
    
    if [ "$file_id" = "null" ] || [ -z "$file_id" ]; then
        echo -e "${RED}❌ 上傳失敗${NC}"
        echo "$upload_response"
        return 1
    fi
    
    echo -e "${GREEN}✅ 檔案上傳成功！ID: $file_id${NC}"
    
    # 添加到知識庫
    echo -e "${YELLOW}📚 添加到知識庫...${NC}"
    
    local add_response=$(curl -s -X POST "$WEBUI_URL/api/v1/knowledge/$knowledge_id/file/add" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"file_id\": \"$file_id\"}")
    
    if echo "$add_response" | jq -r '.id' >/dev/null 2>&1; then
        echo -e "${GREEN}✅ 已添加到知識庫！${NC}"
        echo "知識庫 ID: $knowledge_id"
        echo "檔案 ID: $file_id"
    else
        echo -e "${YELLOW}⚠️ 添加到知識庫可能失敗: $add_response${NC}"
    fi
}

# 上傳檔案
upload_file() {
    check_api_key
    local file_path="$1"
    
    if [ -z "$file_path" ]; then
        echo "用法: claw-openwebui upload <檔案路徑>"
        return 1
    fi
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}錯誤：檔案不存在: $file_path${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📤 上傳檔案: $file_path${NC}"
    
    local response=$(curl -s -X POST "$WEBUI_URL/api/v1/files/" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Accept: application/json" \
        -F "file=@$file_path")
    
    local file_id=$(echo "$response" | jq -r '.id' 2>/dev/null)
    
    if [ "$file_id" != "null" ] && [ -n "$file_id" ]; then
        echo -e "${GREEN}✅ 上傳成功！${NC}"
        echo "File ID: $file_id"
    else
        echo -e "${RED}❌ 上傳失敗${NC}"
    fi
}

# 查詢檔案
get_file() {
    check_api_key
    local file_id="$1"
    
    if [ -z "$file_id" ]; then
        echo "用法: claw-openwebui file <file_id>"
        return 1
    fi
    
    curl -s "$WEBUI_URL/api/v1/files/$file_id" \
        -H "Authorization: Bearer $API_KEY" | \
        jq -r '.data.content' 2>/dev/null
}

# 列出檔案
list_files() {
    check_api_key
    echo -e "${CYAN}📄 已上傳的檔案：${NC}"
    curl -s "$WEBUI_URL/api/v1/files/" \
        -H "Authorization: Bearer $API_KEY" | \
        jq -r '.data[] | "  • \(.id) - \(.filename)"' 2>/dev/null || echo "  無檔案"
}

# 顯示說明
show_help() {
    echo "Claw OpenWebUI - Open WebUI API 技能"
    echo ""
    echo "用法:"
    echo "  claw-openwebui ping                    - 測試連線"
    echo "  claw-openwebui models                 - 列出可用模型"
    echo "  claw-openwebui chat <model> <msg>    - 發送聊天"
    echo ""
    echo "  知識庫功能："
    echo "  claw-openwebui list-knowledge         - 列出知識庫"
    echo "  claw-openwebui create-knowledge <name> [desc] - 建立知識庫"
    echo "  claw-openwebui upload-rag <file> [knowledge] - 上傳並添加到知識庫"
    echo ""
    echo "  檔案功能："
    echo "  claw-openwebui upload <file>          - 上傳檔案"
    echo "  claw-openwebui file <file_id>         - 查詢檔案內容"
    echo "  claw-openwebui files                  - 列出已上傳檔案"
    echo ""
    echo "環境變數:"
    echo "  OPENWEBUI_URL      - Open WebUI URL (預設: http://192.168.0.176:3000)"
    echo "  OPENWEBUI_API_KEY  - JWT Token (必需)"
}

case "${1:-}" in
    ping) ping_webui ;;
    models) list_models ;;
    chat) chat "$2" "$3" ;;
    list-knowledge) list_knowledge ;;
    create-knowledge) create_knowledge "$2" "$3" ;;
    upload-rag) upload_to_knowledge "$2" "$3" ;;
    upload) upload_file "$2" ;;
    file) get_file "$2" ;;
    files) list_files ;;
    help|--help|-h) show_help ;;
    *) show_help ;;
esac
