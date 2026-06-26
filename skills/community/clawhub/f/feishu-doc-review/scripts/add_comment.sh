#!/bin/bash
# add_comment.sh — 向飞书文档添加批注
# 用法: ./add_comment.sh <doc_token> "<批注内容>"

DOC_TOKEN="$1"
COMMENT_TEXT="$2"

if [ -z "$DOC_TOKEN" ] || [ -z "$COMMENT_TEXT" ]; then
  echo "用法: $0 <doc_token> <批注内容>"
  exit 1
fi

APP_ID="cli_a92d5b4257391bcb"
APP_SECRET="${FEISHU_APP_SECRET:-lo4II96JWo5W0DMjgYfZ1diOodp8xlnj}"

# 获取 tenant_access_token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

if [ -z "$TOKEN" ]; then
  echo "ERROR: 获取 token 失败"
  exit 1
fi

# 添加批注
RESULT=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/drive/v1/files/${DOC_TOKEN}/comments?file_type=docx" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"reply_list\": {
      \"replies\": [{
        \"content\": {
          \"elements\": [{
            \"type\": \"text_run\",
            \"text_run\": {
              \"text\": \"$COMMENT_TEXT\"
            }
          }]
        }
      }]
    }
  }")

CODE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code','?'))")
if [ "$CODE" = "0" ]; then
  COMMENT_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['comment_id'])")
  echo "✅ 批注添加成功，comment_id: $COMMENT_ID"
else
  echo "❌ 批注添加失败: $RESULT"
  exit 1
fi
