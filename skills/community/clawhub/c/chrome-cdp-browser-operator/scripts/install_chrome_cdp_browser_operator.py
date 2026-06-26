#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

START_CHROME_PS1 = r'''param(
  [string]$ChromePath = "chrome.exe",
  [string]$UserDataDir,
  [int]$Port = 9222
)
Start-Process -FilePath $ChromePath -ArgumentList @("--remote-debugging-port=$Port", "--user-data-dir=$UserDataDir")
'''


def main() -> int:
    parser = argparse.ArgumentParser(description='install chrome cdp browser operator workspace files')
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--cdp-url', default='http://127.0.0.1:9222')
    parser.add_argument('--chrome-path', default='chrome.exe')
    parser.add_argument('--user-data-dir', default='')
    parser.add_argument('--profile-directory', default='')
    parser.add_argument('--website-url', default='https://example.com')
    parser.add_argument('--telegram-target', default='')
    parser.add_argument('--telegram-account', default='')
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    config_dir = workspace / 'config'
    state_dir = workspace / 'state'
    output_dir = workspace / 'outputs' / 'chrome-cdp-browser-operator'
    config_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = {
        'baseUrl': 'https://x.com/home',
        'cdpUrl': args.cdp_url,
        'statePath': str((state_dir / 'chrome-cdp-browser-operator-state.json').resolve()),
        'outputDir': str(output_dir.resolve()),
        'websiteUrl': args.website_url,
        'keywords': ['customer support', 'pricing question', 'product feedback'],
        'maxTweetsPerKeyword': 8,
        'maxRepliesPerCycle': 3,
        'replyCooldownHours': 72,
        'allowPublicReply': False,
        'telegram': {
            'enabled': bool(args.telegram_target),
            'channel': 'telegram',
            'target': args.telegram_target or None,
            'account': args.telegram_account or None,
        },
        'launchFallback': {
            'enabled': bool(args.user_data_dir),
            'executablePath': args.chrome_path,
            'userDataDir': args.user_data_dir or None,
            'profileDirectory': args.profile_directory or None,
        },
    }
    config_path = config_dir / 'chrome-cdp-browser-operator.json'
    config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ps1_path = state_dir / 'start_chrome_cdp.ps1'
    ps1_path.write_text(START_CHROME_PS1, encoding='utf-8')

    print(json.dumps({
        'config': str(config_path),
        'chromeStarter': str(ps1_path),
        'check': f'python scripts\\browser_operator.py check --config "{config_path}"',
        'draftCycle': f'python scripts\\browser_operator.py run-cycle --config "{config_path}"',
        'applyCycle': f'python scripts\\browser_operator.py run-cycle --config "{config_path}" --apply',
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
