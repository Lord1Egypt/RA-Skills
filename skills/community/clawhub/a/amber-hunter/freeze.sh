#!/bin/bash
# Amber-Hunter Freeze Trigger
# 用法：bash freeze.sh
# 说明：从 amber-hunter 读取当前 session freeze 数据并输出到终端

# 获取本地 API token（从 config.json）
CONFIG_PATH="$HOME/.amber-hunter/config.json"
TOKEN=$(python3 -c "
import json, os
path = os.path.expanduser('$CONFIG_PATH')
try:
    cfg = json.load(open(path))
    print(cfg.get('api_key') or cfg.get('api_token', ''))
except:
    print('')
" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ 未找到 API token，请先在 huper.org/dashboard 生成 API Key"
    echo "   并确保 ~/.amber-hunter/config.json 中有 api_key 字段"
    exit 1
fi

# GET /freeze（浏览器兼容，query param 认证）
RESULT=$(curl -s "http://localhost:18998/freeze?token=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$TOKEN'))")" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$RESULT" ]; then
    echo "❌ 无法连接 amber-hunter（localhost:18998），请确认服务已启动"
    echo "   启动命令：python3 ~/.openclaw/skills/amber-hunter/amber_hunter.py"
    exit 1
fi

echo "🌙 Amber-Hunter Freeze"
echo "=========================================="

python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Session: {d.get(\"session_key\", \"N/A\")}')
print()
print('【预填内容】')
content = (d.get('prefill') or d.get('summary') or '').strip()
if content:
    print(content[:300])
    if len(content) > 300:
        print('...')
else:
    print('（无内容）')
print()
print('【最近文件】')
files = d.get('files', [])
if files:
    for f in files[:5]:
        print(f'  📄 {f[\"path\"]} ({f.get(\"size_kb\", 0)}KB)')
else:
    print('  （无文件）')
print()
print('✅ 前往 https://huper.org 点击「冻结当下」查看详情')
"
