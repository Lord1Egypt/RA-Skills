#!/bin/bash
# 解析富文本消息示例

set -e

# 获取 token
TOKEN=$(bash "$(dirname "$0")/../scripts/feishu-auth.sh" get)

# 示例富文本消息
MESSAGE_JSON='{
  "msg_type": "post",
  "body": {
    "content": "{\"title\":\"测试标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"第一行文本\"},{\"tag\":\"at\",\"user_name\":\"张三\"}],[{\"tag\":\"lark_md\",\"content\":\"**粗体内容**\"}]]}"
  }
}'

# 解析
python3 "$(dirname "$0")/../scripts/feishu-message-parser.py" \
  "$TOKEN" \
  "$MESSAGE_JSON"
