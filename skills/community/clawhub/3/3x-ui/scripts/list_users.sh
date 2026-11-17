#!/bin/bash
# 列出3x-ui面板所有用户
# 用法: ./list_users.sh <panel_url> <token>
# 示例: ./list_users.sh https://panel.example.com:2053 "Bearer eyJ..."

PANEL_URL="$1"
TOKEN="$2"

if [ -z "$PANEL_URL" ] || [ -z "$TOKEN" ]; then
  echo "用法: $0 <panel_url> <token>"
  echo "示例: $0 https://panel.example.com:2053 'Bearer eyJ...'"
  exit 1
fi

curl -s -X GET "${PANEL_URL}/panel/api/clients/list" \
  -H "Authorization: ${TOKEN}" \
  -H "Accept: application/json" | python3 -m json.tool
