#!/usr/bin/env bash
# demo.sh —— 一键验证团队是否正常运行
set -euo pipefail

OFFICE_DIR="${HERMES_OFFICE_DIR:-$HOME/.hermes/office}"
STATE_FILE="$OFFICE_DIR/state/office_state.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Agent Office 团队健康检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "❌ 团队未初始化，请先安装 skill 并重启 OpenClaw"
  exit 1
fi

python3 -c "
import json, sys, urllib.error, urllib.request

with open('$STATE_FILE') as f:
    state = json.load(f)

workers = state.get('workers', {})
if not workers:
    print('⚠️  当前没有员工，请说「添加员工」开始')
    sys.exit(0)

print(f'\n员工总数: {len(workers)}\n')

all_ok = True
for wid, w in workers.items():
    port = w.get('port', 0)
    name = w.get('name', wid)
    engine = w.get('engine', 'unknown')
    role = w.get('role', '')
    status = w.get('status', 'unknown')
    last = w.get('last_active', '从未')

    # 严格检查 /health 是否返回 200 且 status=ok
    if port:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=3) as resp:
                payload = json.loads(resp.read().decode('utf-8'))
                if resp.status == 200 and payload.get('status') == 'ok':
                    health = '🟢 在线'
                else:
                    health = f'🟡 异常({resp.status})'
        except urllib.error.URLError:
            health = '🔴 未启动'
        except Exception:
            health = '🟡 响应异常'
    else:
        health = '⚪ 端口未分配'

    print(f'{health}  {name}({wid}) | 引擎:{engine} | 端口:{port} | 职责:{role} | 状态:{status}')
    if last and last != '从未':
        print(f'         最后活跃: {last}')

    if status == 'not_ready':
        all_ok = False

print()
if all_ok:
    print('✅ 团队运行正常')
else:
    print('⚠️  部分员工未就绪，请检查安装')
"
