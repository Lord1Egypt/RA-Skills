#!/bin/bash
# 解析纯文本消息示例

set -e

# 获取 token
TOKEN=$(bash "$(dirname "$0")/../scripts/feishu-auth.sh" get)

# 示例消息
MESSAGE_JSON='{
  "msg_type": "text",
  "body": {
    "content": "{\"text\":\"Hello World\"}"
  }
}'

# 解析
python3 "$(dirname "$0")/../scripts/feishu-message-parser.py" \
  "$TOKEN" \
  "$MESSAGE_JSON"
