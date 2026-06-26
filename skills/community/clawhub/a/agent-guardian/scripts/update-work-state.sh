#!/bin/bash
# 更新工作状态（AI 干活时调用）
# 用法: ./update-work-state.sh <status> [task] [is_error]
# status: idle / working / done / error

STATE_FILE="/tmp/agent-work-state.json"
NOW=$(date +%s)

STATUS="${1:-idle}"
TASK="${2:-none}"
IS_ERROR="${3:-}"

python3 -c "
import json, os

state_file = '$STATE_FILE'
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        d = json.load(f)
else:
    d = {
        'current_task': None, 'status': 'idle',
        'started_at': 0, 'last_update': 0,
        'update_count': 0, 'last_status_values': [],
        'error_count': 0, 'last_report_at': 0
    }

d['status'] = '$STATUS'
d['current_task'] = '$TASK' if '$TASK' != 'none' else d.get('current_task')
d['last_update'] = $NOW
d['update_count'] = d.get('update_count', 0) + 1

vals = d.get('last_status_values', [])
vals.append('$STATUS')
d['last_status_values'] = vals[-10:]

if '$IS_ERROR':
    d['error_count'] = d.get('error_count', 0) + 1
elif '$STATUS' in ('done', 'idle'):
    d['error_count'] = 0

if '$STATUS' == 'working' and d.get('started_at', 0) == 0:
    d['started_at'] = $NOW

if '$STATUS' in ('done', 'idle'):
    d['started_at'] = 0

with open(state_file, 'w') as f:
    json.dump(d, f, indent=2)

print('OK: status=$STATUS task=$TASK')
"
