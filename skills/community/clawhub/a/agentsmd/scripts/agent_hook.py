#!/usr/bin/env python3
"""Project-scoped lifecycle journal; never treats a turn ending as task completion."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
EVENTS = {'SessionStart', 'UserPromptSubmit', 'Stop', 'Interrupt', 'SessionEnd'}


def atomic_json(path, value):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', required=True, choices=['Codex', 'ZCode', 'QwenWork'])
    args = parser.parse_args()
    settings = json.loads((ROOT / ".agent-handoff.json").read_text())
    if settings.get("version") != 1 or settings.get("enabled") is not True:
        return
    event = json.load(sys.stdin)
    if not isinstance(event, dict) or not isinstance(event.get('cwd'), str):
        return
    cwd = Path(event['cwd']).resolve()
    if not cwd.is_relative_to(ROOT):
        return
    name = event.get('hook_event_name')
    session = event.get('session_id')
    if name not in EVENTS or not isinstance(session, str) or not session:
        return
    now = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
    key = hashlib.sha256(session.encode()).hexdigest()[:20]
    folder = ROOT / 'docs/execution/agent-runs' / f'{args.agent}-{key}'
    folder.mkdir(parents=True, exist_ok=True)
    # Per-session lock protects concurrent events; human notes are created once only.
    with (folder / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        runtime = folder / 'runtime.json'
        state = json.loads(runtime.read_text()) if runtime.exists() else {}
        state.update(agent=args.agent, session_id=session, updated_at=now,
                     last_event=name, business_status='待 Agent 核对，钩子不判断业务完成')
        state.setdefault('started_at', now)
        state.setdefault('run_id', f'{args.agent}-{key}')
        statuses = {'SessionStart': '会话已启动／恢复', 'UserPromptSubmit': '进行中',
                    'Stop': '回合结束，业务完成情况待核对',
                    'Interrupt': '已中断，待接手', 'SessionEnd': '会话已关闭，业务完成情况待核对'}
        state['runtime_status'] = statuses[name]
        turn_id = event.get('turn_id')
        if isinstance(turn_id, str):
            state['turn_id'] = turn_id
        atomic_json(runtime, state)
        # Whitelist metadata: never save prompt, response, commands or transcript contents.
        record = {k: state[k] for k in ['run_id', 'agent', 'updated_at', 'last_event', 'runtime_status']}
        with (folder / 'events.jsonl').open('a') as output:
            output.write(json.dumps(record, ensure_ascii=False) + '\n')
        handover = folder / 'handover.md'
        if not handover.exists():
            with handover.open('x') as note:
                note.write(f'''# Agent 交接记录

- 运行编号：{args.agent}-{key}（自动生成；业务任务沿用原编号）
- 负责 Agent：{args.agent}
- 创建时间：{now}（北京时间）
- 业务任务编号：待填写
- 目标与范围：待填写
- 对应任务文档／台账：待填写
- 业务状态：待核对
- 已完成与核验：待填写
- 产物与证据：待填写
- 未完成与阻塞：待填写
- 下一步：待填写
- 授权范围：按最新用户明确指令，不因钩子扩大授权

自动运行状态见 runtime.json；本文件由 Agent 补齐，钩子不会覆盖已有内容。
已有任务台账时填写入口和简短交接，不重复复制完整过程。
''')
    if name in {'SessionStart', 'UserPromptSubmit'}:
        context = (f'本项目自动运行记录已建立：{folder.relative_to(ROOT)}。'
                   '先读 AGENTS.md、HANDOVER.md 及对应任务台账；沿用业务任务编号。'
                   f'结束前更新对应任务记录和 {handover.relative_to(ROOT)} 的简短摘要／入口，'
                   '并同步 HANDOVER.md，最终回复附记录路径；自动运行状态不等于任务完成。')
        print(json.dumps({'hookSpecificOutput': {'hookEventName': name, 'additionalContext': context}}, ensure_ascii=False))
    elif name == 'Stop' and '待填写' in handover.read_text():
        print(json.dumps({'systemMessage': f'运行状态已保存；交接记录尚有待填写项：{handover.relative_to(ROOT)}。请补齐任务摘要或已有台账入口；本提示不代表业务验收。'}, ensure_ascii=False))
    else:
        print('{}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # A journal failure must never block unrelated work or reveal input data.
        print(f'Coremon hook: recording failed ({type(exc).__name__}); task may continue.', file=sys.stderr)
        print('{}')
