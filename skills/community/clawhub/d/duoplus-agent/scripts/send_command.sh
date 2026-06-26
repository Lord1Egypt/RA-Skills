#!/bin/bash
# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called: none (local ADB only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

# 发送命令到安卓设备
# 用法: send_command.sh <DEVICE_ID> <ACTION_JSON>
# 示例: send_command.sh 192.168.1.100:5555 '{"action_name":"GO_TO_HOME","params":{}}'

DEVICE_ID="${1:?Usage: send_command.sh <DEVICE_ID> <ACTION_JSON>}"
ACTION_JSON="${2:?Usage: send_command.sh <DEVICE_ID> <ACTION_JSON>}"

# 验证 DEVICE_ID 格式：仅允许 IP:PORT（如 192.168.1.100:5555）或设备序列号（字母数字和常见分隔符）
if ! echo "$DEVICE_ID" | grep -qE '^[a-zA-Z0-9._:/-]+$'; then
  echo "❌ Invalid DEVICE_ID format: contains disallowed characters" >&2
  exit 1
fi

BROADCAST_ACTION="com.duoplus.service.PROCESS_DATA"
TASK_ID="openclaw-$(date +%s)-$$"
MD5="openclaw-md5"

# 从 ACTION_JSON 中提取 action_name 和 params，构建完整 payload
# 如果传入的是完整 JSON（包含 task_type），直接使用
if echo "$ACTION_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'task_type' in d" 2>/dev/null; then
  FULL_JSON="$ACTION_JSON"
else
  # 通过环境变量传递数据给 Python，避免命令注入
  FULL_JSON=$(ACTION_JSON="$ACTION_JSON" TASK_ID="$TASK_ID" MD5="$MD5" python3 -c "
import json, os, sys

try:
    action_data = json.loads(os.environ['ACTION_JSON'])
except (json.JSONDecodeError, KeyError) as e:
    print(f'Error: invalid ACTION_JSON: {e}', file=sys.stderr)
    sys.exit(1)

action_name = action_data.get('action_name', '')
params = action_data.get('params', {})

payload = {
    'task_type': 'ai',
    'action': 'execute',
    'task_id': os.environ['TASK_ID'],
    'md5': os.environ['MD5'],
    'action_name': action_name,
    'params': params
}
print(json.dumps(payload))
")
fi

# Base64 编码
BASE64=$(echo -n "$FULL_JSON" | base64 -w 0 2>/dev/null || echo -n "$FULL_JSON" | base64)

# 发送广播
echo "Sending to device $DEVICE_ID:"
echo "  Action: $FULL_JSON"
adb -s "$DEVICE_ID" shell am broadcast -a "$BROADCAST_ACTION" --es message "$BASE64"
