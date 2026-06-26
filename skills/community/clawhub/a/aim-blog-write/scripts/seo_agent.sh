#!/bin/bash
# ============================================================
# Skill: SEO Agent —— 生成 SEO 博客（同步 SSE）
#
# 使用方式:
#   bash scripts/seo_agent.sh '<JSON>'
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# 先在顶层做 aim-secret-key 校验；缺失则引导到申请页并写入降级文件
# 放在命令替换之外，exit 才能真正终止脚本
ensure_aep_env || exit 1

if [ -n "$1" ]; then
    INPUT_JSON="$1"
else
    if [ ! -t 0 ]; then
        INPUT_JSON=$(cat)
    else
        INPUT_JSON=""
    fi
fi

if [ -z "${INPUT_JSON}" ]; then
    echo '{"success": false, "msg": "缺少入参，请传入 JSON，如: {\"theme\": \"...\", \"industry\": \"...\", \"language\": \"en\"}"}'
    exit 1
fi

BODY=$(python3 -c "
import sys, json

try:
    input_data = json.loads(sys.argv[1])
except Exception:
    print(json.dumps({'success': False, 'msg': '入参解析失败，请传入合法 JSON'}))
    sys.exit(1)

missing = [f for f in ('theme', 'industry', 'language') if not input_data.get(f)]
if missing:
    print(json.dumps({'success': False, 'msg': '缺少必填字段: ' + ', '.join(missing)}, ensure_ascii=False))
    sys.exit(1)

from datetime import datetime, timedelta
now = datetime.now()

body = {
    'uuid': input_data.get('uuid', 'skill-client'),
    'sessionId': input_data.get('sessionId', 'skill-client'),
    'userId': input_data.get('userId', 'skill-client'),
    'data': {
        'theme': input_data['theme'],
        'industry': input_data['industry'],
        'language': input_data['language'],
        'startTime': input_data.get('startTime', (now - timedelta(days=31)).strftime('%Y-%m-%d')),
        'endTime': input_data.get('endTime', now.strftime('%Y-%m-%d')),
        'hotNums': input_data.get('hotNums', 10),
        'style': input_data.get('style', ''),
        'country': input_data.get('country', ''),
    }
}
print(json.dumps(body, ensure_ascii=False))
" "${INPUT_JSON}")

if [ $? -ne 0 ]; then
    echo "${BODY}"
    exit 1
fi

# 同步请求，接收 SSE 流后解析为完整 JSON
SSE_RAW=$(run_skill_sync "/seo_agent" "${BODY}")

echo "${SSE_RAW}" | python3 -c "
import sys, json

blog_content = ''
keywords = {}
images = []
success = True
error_msg = ''

for line in sys.stdin:
    line = line.strip()
    if not line.startswith('data: '):
        continue
    try:
        event = json.loads(line[6:])
    except Exception:
        continue

    code = event.get('code')
    content = event.get('content')

    if code == 1 and content:
        blog_content += content
    elif code == 4 and content:
        keywords = content
    elif code == 5 and content:
        images = content
    elif code == 3 and content == '[error]':
        success = False
        error_msg = event.get('msg', '')

result = {
    'success': success,
    'data': {
        'blog_content': blog_content,
        'keywords': keywords,
        'images': images
    }
}
if not success:
    result['msg'] = error_msg

print(json.dumps(result, ensure_ascii=False))
"
