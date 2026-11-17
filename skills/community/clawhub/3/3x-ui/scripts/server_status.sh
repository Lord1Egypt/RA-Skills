#!/bin/bash
# 查看3x-ui面板服务器状态
# 用法: ./server_status.sh <panel_url> <token>
# 示例: ./server_status.sh https://panel.example.com:2053 "Bearer eyJ..."

PANEL_URL="$1"
TOKEN="$2"

if [ -z "$PANEL_URL" ] || [ -z "$TOKEN" ]; then
  echo "用法: $0 <panel_url> <token>"
  echo "示例: $0 https://panel.example.com:2053 'Bearer eyJ...'"
  exit 1
fi

echo "=== 服务器状态 ==="
curl -s -X GET "${PANEL_URL}/panel/api/server/status" \
  -H "Authorization: ${TOKEN}" \
  -H "Accept: application/json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    s = data['obj']
    print(f\"CPU: {s['cpu']}%\")
    print(f\"内存: {s['mem']['current']/1024**3:.1f}GB / {s['mem']['total']/1024**3:.1f}GB\")
    print(f\"硬盘: {s['disk']['current']/1024**3:.1f}GB / {s['disk']['total']/1024**3:.1f}GB\")
    print(f\"Xray: {s['xray']['state']} (v{s['xray']['version']})\")
    print(f\"在线连接: {s['tcpCount']}\")
    print(f\"负载: 1min={s['load']['load1']} 5min={s['load']['load5']} 15min={s['load']['load15']}\")
else:
    print(f\"错误: {data.get('msg', '未知')}\")
"
