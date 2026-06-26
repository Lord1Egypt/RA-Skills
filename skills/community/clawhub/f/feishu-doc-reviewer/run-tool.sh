#!/bin/bash
# Feishu Doc Reviewer - 工具调用脚本
# 用法：./run-tool.sh <tool_name> <args...>

cd "$(dirname "$0")"

TOOL_NAME=$1
shift

case "$TOOL_NAME" in
  "list_comments")
    DOCUMENT_TOKEN=$1
    KEYWORD=$2
    python3 -c "
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json

api = FeishuClient()
result = api.get_comments('$DOCUMENT_TOKEN')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
    ;;
  
  "get_block")
    DOCUMENT_TOKEN=$1
    BLOCK_ID=$2
    python3 -c "
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json

api = FeishuClient()
result = api.get_block('$DOCUMENT_TOKEN', '$BLOCK_ID')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
    ;;
  
  "update_block")
    DOCUMENT_TOKEN=$1
    BLOCK_ID=$2
    NEW_TEXT=$3
    python3 -c "
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json

api = FeishuClient()
result = api.update_block('$DOCUMENT_TOKEN', '$BLOCK_ID', '''$NEW_TEXT''')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
    ;;
  
  "reply_comment")
    DOCUMENT_TOKEN=$1
    COMMENT_ID=$2
    CONTENT=$3
    python3 -c "
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json

api = FeishuClient()
result = api.reply_comment('$DOCUMENT_TOKEN', '$COMMENT_ID', '''$CONTENT''')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
    ;;
  
  *)
    echo "用法：$0 <tool_name> <args...>"
    echo "可用工具:"
    echo "  list_comments <document_token> [keyword]"
    echo "  get_block <document_token> <block_id>"
    echo "  update_block <document_token> <block_id> <new_text>"
    echo "  reply_comment <document_token> <comment_id> <content>"
    exit 1
    ;;
esac
