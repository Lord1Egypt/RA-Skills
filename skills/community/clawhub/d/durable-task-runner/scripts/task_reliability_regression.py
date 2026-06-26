#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
STATE = ROOT / 'state' / 'tasks'


def run(*args: str, input_text: str | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(list(args), text=True, input=input_text, capture_output=True, check=True, env=merged)


def load(task_id: str) -> dict:
    return json.loads((STATE / f'{task_id}.json').read_text())


def rm(task_id: str) -> None:
    for suffix in ['.json', '.events.jsonl', '.progress.log']:
        p = STATE / f'{task_id}{suffix}'
        if p.exists():
            p.unlink()


def main() -> int:
    results: dict[str, object] = {}

    # 0) resumable running tasks should ask before resuming after reset by default
    task0 = 'reliability-ask-before-resume'
    rm(task0)
    run(
        'python3', str(SCRIPTS / 'task_ctl.py'), 'create', task0,
        '--title', 'Ask before resume',
        '--goal', 'Regression test',
        '--desired-state', 'running',
        '--phase', 'test',
        '--next-step', 'resume main execution'
    )
    boot0 = json.loads(run('python3', str(SCRIPTS / 'task_resume_bootstrap.py'), '--task-id', task0, '--plan').stdout)
    item0 = boot0['tasks'][0]
    assert item0['classification'] == 'resumable', item0
    assert item0['recommendation']['action'] == 'ask_to_resume', item0
    assert 'Do you want me to continue' in item0['recommendation']['prompt'], item0
    results['ask_before_resume'] = item0['recommendation']

    # 1) paused classification must outrank attention-lines
    task1 = 'reliability-paused-vs-attention'
    rm(task1)
    run(
        'python3', str(SCRIPTS / 'task_ctl.py'), 'create', task1,
        '--title', 'Paused outranks attention',
        '--goal', 'Regression test',
        '--desired-state', 'paused',
        '--phase', 'test',
        '--artifacts', json.dumps([{
            'kind': 'subagent_lines',
            'lines': {
                'waiter': {
                    'status': 'autopilot',
                    'controller_decision': 'pending',
                    'next_role': 'worker'
                }
            }
        }]),
    )
    boot1 = json.loads(run('python3', str(SCRIPTS / 'task_resume_bootstrap.py'), '--task-id', task1, '--plan').stdout)
    item1 = boot1['tasks'][0]
    assert item1['classification'] == 'paused', item1
    assert item1['recommendation']['action'] == 'stay_paused', item1
    results['paused_outranks_attention'] = item1['classification']

    # 2) applying pending pause control should remove it from pending_actions and clear reconcile
    task2 = 'reliability-user-control-cleanup'
    rm(task2)
    run(
        'python3', str(SCRIPTS / 'task_ctl.py'), 'create', task2,
        '--title', 'User control cleanup',
        '--goal', 'Regression test',
        '--desired-state', 'running',
        '--phase', 'test',
        '--pending-actions', json.dumps([
            {
                'id': 'pause-1',
                'kind': 'user_control',
                'intent': 'pause',
                'message': 'pause now',
                'status': 'pending',
                'boundary': 'immediate'
            }
        ]),
        '--reconcile', json.dumps({'needed': True, 'reason': 'seeded', 'last_run_at': None, 'status': 'idle'})
    )
    boot2 = json.loads(run('python3', str(SCRIPTS / 'task_resume_bootstrap.py'), '--task-id', task2, '--plan').stdout)
    applied2 = json.loads(run('python3', str(SCRIPTS / 'task_resume_apply.py'), input_text=json.dumps(boot2)).stdout)
    snap2 = load(task2)
    assert applied2['applied'][0]['applied'] is True, applied2
    assert snap2['desired_state'] == 'paused', snap2
    assert snap2['pending_actions'] == [], snap2
    assert snap2['reconcile']['needed'] is False, snap2
    results['user_control_cleanup'] = {
        'desired_state': snap2['desired_state'],
        'pending_actions': len(snap2['pending_actions']),
        'reconcile': snap2['reconcile']['status'],
    }

    # 3) explicit continue-this recovery should promote paused tasks back to running
    task3 = 'reliability-continue-this'
    rm(task3)
    run(
        'python3', str(SCRIPTS / 'task_ctl.py'), 'create', task3,
        '--title', 'Continue this recovery',
        '--goal', 'Regression test',
        '--desired-state', 'paused',
        '--phase', 'test',
        '--next-step', 'resume main execution'
    )
    continued3 = json.loads(run('python3', str(SCRIPTS / 'task_continue.py'), '--task-id', task3).stdout)
    snap3 = load(task3)
    assert continued3['promoted_from_state'] == 'paused', continued3
    assert continued3['classification'] == 'resumable', continued3
    assert snap3['desired_state'] == 'running', snap3
    results['continue_this'] = {
        'promoted_from_state': continued3['promoted_from_state'],
        'classification': continued3['classification'],
        'desired_state': snap3['desired_state'],
    }

    # 4) task creation should auto-bind delivery when OpenClaw chat context env is present
    task4 = 'reliability-auto-bind'
    rm(task4)
    env = {
        'OPENCLAW_CHANNEL': 'telegram',
        'OPENCLAW_ACCOUNT_ID': 'default',
        'OPENCLAW_CHAT_ID': 'telegram:1501302070',
        'OPENCLAW_SURFACE': 'direct-chat',
    }
    run(
        'python3', str(SCRIPTS / 'task_ctl.py'), 'create', task4,
        '--title', 'Auto bind delivery',
        '--goal', 'Regression test',
        '--desired-state', 'running',
        '--phase', 'test',
        env=env,
    )
    snap4 = load(task4)
    bindings = [a for a in snap4.get('artifacts', []) if isinstance(a, dict) and a.get('kind') == 'delivery_binding']
    assert len(bindings) == 1, snap4
    assert bindings[0]['target'] == 'telegram:1501302070', bindings[0]
    results['auto_bind'] = bindings[0]

    print(json.dumps({'ok': True, 'results': results}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
