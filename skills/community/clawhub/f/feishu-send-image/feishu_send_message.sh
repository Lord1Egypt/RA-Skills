#!/bin/bash

# feishu_send_message - 发送飞书图片/文件消息
# 用法: feishu_send_message --msg-type <type> --file-path <path> --receive-id <id> --receive-id-type <type>

set -e

# 默认值
MSG_TYPE=""
FILE_PATH=""
RECEIVE_ID=""
RECEIVE_ID_TYPE="open_id"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --msg-type)
            MSG_TYPE="$2"
            shift 2
            ;;
        --file-path)
            FILE_PATH="$2"
            shift 2
            ;;
        --receive-id)
            RECEIVE_ID="$2"
            shift 2
            ;;
        --receive-id-type)
            RECEIVE_ID_TYPE="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证必填参数
if [[ -z "$RECEIVE_ID" ]]; then
    echo "错误: 请指定 --receive-id"
    exit 1
fi

if [[ -z "$MSG_TYPE" ]]; then
    echo "错误: 请指定 --msg-type (image 或 file)"
    exit 1
fi

if [[ -z "$FILE_PATH" ]]; then
    echo "错误: 请指定 --file-path"
    exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
    echo "错误: 文件不存在: $FILE_PATH"
    exit 1
fi

# 获取飞书配置
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
APP_ID=$(grep -o '"appId": *"[^"]*"' "$CONFIG_FILE" | head -1 | sed 's/.*"appId": *"\([^"]*\)"/\1/')
APP_SECRET=$(grep -o '"appSecret": *"[^"]*"' "$CONFIG_FILE" | head -1 | sed 's/.*"appSecret": *"\([^"]*\)"/\1/')

if [[ -z "$APP_ID" ]] || [[ -z "$APP_SECRET" ]]; then
    echo "错误: 无法从配置中获取 appId 或 appSecret"
    exit 1
fi

echo "📤 获取 access token..."

# 获取 tenant_access_token
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"tenant_access_token":"[^"]*"' | sed 's/"tenant_access_token":"\([^"]*\)"/\1/')

if [[ -z "$TOKEN" ]]; then
    echo "错误: 获取 token 失败: $TOKEN_RESPONSE"
    exit 1
fi

echo "✅ Token 获取成功"

# 根据文件扩展名获取 file_type
get_file_type() {
    local filename="$1"
    local ext="${filename##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    
    case "$ext" in
        mp4|mov|avi|mkv)
            echo "mp4"
            ;;
        mp3|wav|aac|flac|m4a)
            echo "opus"
            ;;
        pdf)
            echo "pdf"
            ;;
        doc|docx)
            echo "doc"
            ;;
        xls|xlsx)
            echo "xls"
            ;;
        ppt|pptx)
            echo "ppt"
            ;;
        *)
            echo "stream"
            ;;
    esac
}

# 根据消息类型处理
case "$MSG_TYPE" in
    image)
        # 检查图片大小，如果超过 10MB 则压缩
        FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null)
        MAX_SIZE=10485760  # 10MB
        
        if [[ $FILE_SIZE -gt $MAX_SIZE ]]; then
            echo "📦 图片过大 ($((FILE_SIZE/1024/1024))MB)，压缩中..."
            TEMP_DIR=$(mktemp -d)
            TEMP_FILE="$TEMP_DIR/$(basename "$FILE_PATH")"
            sips -s format jpeg -s formatOptions 80 -z 3000 4000 "$FILE_PATH" --out "$TEMP_FILE" 2>/dev/null || {
                TEMP_FILE="$FILE_PATH"
            }
            FILE_PATH="$TEMP_FILE"
            echo "✅ 压缩完成"
        fi
        
        echo "📤 上传图片..."
        
        # 上传图片
        UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
            -H "Authorization: Bearer $TOKEN" \
            -F "image_type=message" \
            -F "image=@$FILE_PATH")
        
        IMAGE_KEY=$(echo "$UPLOAD_RESPONSE" | grep -o '"image_key":"[^"]*"' | sed 's/"image_key":"\([^"]*\)"/\1/')
        
        if [[ -z "$IMAGE_KEY" ]]; then
            echo "错误: 上传图片失败: $UPLOAD_RESPONSE"
            exit 1
        fi
        
        echo "✅ 图片上传成功, image_key: $IMAGE_KEY"
        
        # 发送图片消息
        echo "📤 发送图片消息..."
        MESSAGE_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json; charset=utf-8" \
            -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}")
        
        MESSAGE_ID=$(echo "$MESSAGE_RESPONSE" | grep -o '"message_id":"[^"]*"' | sed 's/"message_id":"\([^"]*\)"/\1/')
        
        if [[ -z "$MESSAGE_ID" ]]; then
            echo "错误: 发送消息失败: $MESSAGE_RESPONSE"
            exit 1
        fi
        
        echo "✅ 发送成功! message_id: $MESSAGE_ID"
        echo ""
        echo "🎉 图片消息已发送完成"
        exit 0
        ;;
        
    file)
        # 根据文件扩展名获取 file_type
        FILE_TYPE=$(get_file_type "$FILE_PATH")
        FILE_NAME=$(basename "$FILE_PATH")
        
        echo "📤 上传文件 (file_type: $FILE_TYPE)..."
        
        # 上传文件
        UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: multipart/form-data" \
            -F "file_type=$FILE_TYPE" \
            -F "file_name=$FILE_NAME" \
            -F "file=@$FILE_PATH")
        
        FILE_KEY=$(echo "$UPLOAD_RESPONSE" | grep -o '"file_key":"[^"]*"' | sed 's/"file_key":"\([^"]*\)"/\1/')
        
        if [[ -z "$FILE_KEY" ]]; then
            echo "错误: 上传文件失败: $UPLOAD_RESPONSE"
            exit 1
        fi
        
        echo "✅ 文件上传成功, file_key: $FILE_KEY"
        
        # 发送文件消息
        echo "📤 发送文件消息..."
        MESSAGE_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json; charset=utf-8" \
            -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")
        
        MESSAGE_ID=$(echo "$MESSAGE_RESPONSE" | grep -o '"message_id":"[^"]*"' | sed 's/"message_id":"\([^"]*\)"/\1/')
        
        if [[ -z "$MESSAGE_ID" ]]; then
            echo "错误: 发送消息失败: $MESSAGE_RESPONSE"
            exit 1
        fi
        
        echo "✅ 发送成功! message_id: $MESSAGE_ID"
        echo ""
        echo "🎉 文件消息已发送完成"
        exit 0
        ;;
        
    *)
        echo "错误: 不支持的 msg_type: $MSG_TYPE"
        echo "支持的类型: image, file"
        exit 1
        ;;
esac