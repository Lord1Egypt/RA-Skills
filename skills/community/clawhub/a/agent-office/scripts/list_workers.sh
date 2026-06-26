#!/usr/bin/env bash
# list_workers.sh —— 查看团队成员
# 用法: bash list_workers.sh
set -euo pipefail

OFFICE_DIR="${HERMES_OFFICE_DIR:-$HOME/.hermes/office}"
STATE_FILE="$OFFICE_DIR/state/office_state.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Agent Office 团队成员"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "⚠️  团队未初始化，请说「添加员工」开始"
  exit 0
fi

python3 -c "
import json

with open('$STATE_FILE') as f:
    s = json.load(f)

workers = s.get('workers', {})
port_pool = s.get('port_pool', {})

if not workers:
    print('⚠️  当前没有员工，请说「添加员工」')
    print()
    print('端口池状态：')
    print(f'  已用: {port_pool.get(\"used\", [])}')
    print(f'  可用: {port_pool.get(\"available\", [])}')
    exit(0)

print(f'\n员工总数: {len(workers)}')
print(f'端口池: 已用 {len(port_pool.get(\"used\", []))} 个，可用 {len(port_pool.get(\"available\", []))} 个')
print()

# 表头
STATUS_HDR='状态'; NAME_HDR='名字'; ID_HDR='工号'; ENGINE_HDR='引擎'; PORT_HDR='端口'; ROLE_HDR='职责'
print(f"{STATUS_HDR:<8} {NAME_HDR:<10} {ID_HDR:<18} {ENGINE_HDR:<10} {PORT_HDR:<6} {ROLE_HDR:<15}")
print('-' * 75)

status_icon = {'idle':'🟢','running':'🔵','busy':'🟡','not_ready':'🔴','onboarding':'🟠','offline':'⚪'}

for wid, w in workers.items():
    icon = status_icon.get(w.get('status','unknown'), '⚪')
    name = w.get('name', wid)
    engine = w.get('engine', '-')
    port = w.get('port', '-')
    role = w.get('role', '-')
    last = w.get('last_active', '')
    print(f'{icon}  {name:<8} {wid:<18} {engine:<10} {port:<6} {role:<15}')

print()
print('状态说明：')
print('  🟢 idle       空闲，可接收任务')
print('  🔵 running    正在执行任务')
print('  🟡 busy       忙碌中')
print('  🟠 onboarding 入职中')
print('  🔴 not_ready  未就绪（依赖未安装）')
print('  ⚪ offline    已离线')
"
