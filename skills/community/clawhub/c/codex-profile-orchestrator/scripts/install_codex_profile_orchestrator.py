#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

START_PS1 = r'''param(
  [string]$Workspace
)
$Config = Join-Path $Workspace "config\codex-profile-orchestrator.json"
$Log = Join-Path $Workspace "state\codex-profile-orchestrator.log"
python scripts\codex_profile_orchestrator.py --config $Config --apply --daemon | Tee-Object -FilePath $Log -Append
'''


def main() -> int:
    parser = argparse.ArgumentParser(description='install codex profile orchestrator config into a workspace')
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--state-dir', required=True)
    parser.add_argument('--telegram-target', default='')
    parser.add_argument('--telegram-account', default='')
    parser.add_argument('--session-target', action='append', default=[])
    parser.add_argument('--loop-seconds', type=int, default=60)
    parser.add_argument('--threshold', type=float, default=25.0)
    parser.add_argument('--invalid-streak', type=int, default=3)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    config_dir = workspace / 'config'
    state_dir = workspace / 'state'
    config_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    cfg = {
        'agent': 'main',
        'stateDir': args.state_dir,
        'loopSeconds': args.loop_seconds,
        'thresholdPercent': args.threshold,
        'usageTimeoutSeconds': 15,
        'probeTimeoutSeconds': 8,
        'invalidStreakBeforeDelete': args.invalid_streak,
        'sessionTargets': ['agent:main:main', *args.session_target],
        'notify': {
            'enabled': bool(args.telegram_target),
            'channel': 'telegram',
            'target': args.telegram_target or None,
            'account': args.telegram_account or None,
            'dedupeSeconds': 300,
        },
        'registryPath': str((workspace / 'state' / 'codex-profile-orchestrator-state.json').resolve()),
        'probeUrl': 'https://chatgpt.com/',
    }
    config_path = config_dir / 'codex-profile-orchestrator.json'
    config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ps1_path = state_dir / 'start_codex_profile_orchestrator.ps1'
    ps1_path.write_text(START_PS1, encoding='utf-8')

    print(json.dumps({
        'config': str(config_path),
        'starter': str(ps1_path),
        'dryRun': f'python scripts\\codex_profile_orchestrator.py --config "{config_path}" --dry-run --json',
        'apply': f'python scripts\\codex_profile_orchestrator.py --config "{config_path}" --apply --json',
        'daemon': f'python scripts\\codex_profile_orchestrator.py --config "{config_path}" --apply --daemon',
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
