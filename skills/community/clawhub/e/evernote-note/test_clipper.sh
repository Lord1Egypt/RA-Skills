#!/usr/bin/env bash
# 测试 yinxiang-skill RESTful API 集成
# 用法: bash test_clipper.sh
#
# 前置: 环境变量 YX_AUTH_TOKEN 已设置
# 来源: https://app.yinxiang.com/third/skills-oauth/

set -e

if [ -z "$YX_AUTH_TOKEN" ]; then
  echo "❌ 缺少 YX_AUTH_TOKEN 环境变量"
  echo "   请访问 https://app.yinxiang.com/third/skills-oauth/ 生成 Token"
  echo "   然后 export YX_AUTH_TOKEN=\"S=s...\""
  exit 1
fi

BASE="https://app.yinxiang.com"

echo "=== 1. listNoteBooks (验证 token 有效) ==="
RESP=$(curl -s -X POST \
  "$BASE/third/ai-chat-note/grpc-api/search/listNoteBooks" \
  -H "Content-Type: application/json" \
  -H "auth: $YX_AUTH_TOKEN" \
  -d '{}')
echo "$RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('status', {}).get('code') == 8200:
    n = len(d.get('data', {}).get('noteBookList', []))
    print(f'✅ 笔记本数: {n}')
else:
    print(f'❌ {d}')
    sys.exit(1)
"

echo
echo "=== 2. clipAndSaveNote (剪藏 example.com) ==="
RESP=$(curl -s -X POST \
  "$BASE/third/clipper-gateway/restful/v1/clipAndSaveNote" \
  -H "Content-Type: text/plain" \
  -H "auth: $YX_AUTH_TOKEN" \
  -H "clipper-c-auth: $YX_AUTH_TOKEN" \
  -d '{"url":"https://example.com"}')
echo "$RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('status', {}).get('code') == 8200:
    guid = d.get('data', {}).get('noteGuid', '')
    print(f'✅ 剪藏成功，noteGuid: {guid}')
else:
    print(f'❌ {d}')
    sys.exit(1)
"

echo
echo "✅ 所有测试通过。请到印象笔记客户端查看新建的笔记。"
