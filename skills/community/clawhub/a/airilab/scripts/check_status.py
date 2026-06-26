#!/usr/bin/env python3
"""
AiriLab task status checker.
Always prints a machine-readable line: status:<value>
"""

import sys
from pathlib import Path

import requests

AIRILAB_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AIRILAB_PATH))

from core.paths import get_config_dir  # noqa: E402

CONFIG_DIR = get_config_dir()
TOKEN_FILE = CONFIG_DIR / '.env'
STATUS_URL_TEMPLATE = 'https://cn.airilab.com/api/Universal/Job/{job_id}'


def get_token():
    if not TOKEN_FILE.exists():
        return None

    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('AIRILAB_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None


def normalize_status(raw_status: str) -> str:
    value = (raw_status or '').strip().lower()
    if value in {'completed', 'success', 'succeeded', 'done'}:
        return 'completed'
    if value in {'failed', 'failure', 'error'}:
        return 'failed'
    if value in {'processing', 'running', 'sending_now', 'in_progress'}:
        return 'processing'
    if value in {'queued', 'pending', ''}:
        return 'pending'
    return 'pending'


def check_status(job_id: str) -> str:
    token = get_token()
    if not token:
        print('error:missing_token')
        print('status:error')
        return 'error'

    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',
    }
    url = STATUS_URL_TEMPLATE.format(job_id=job_id)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        result = response.json()

        if result.get('status') != 200:
            print(f"error:api_{result.get('message', 'unknown')}")
            print('status:error')
            return 'error'

        data = result.get('data', {})
        raw_status = data.get('status') or ''
        status = normalize_status(str(raw_status))
        print(f'status:{status}')
        return status

    except requests.exceptions.RequestException as e:
        print(f'error:network_{e}')
        print('status:error')
        return 'error'
    except Exception as e:
        print(f'error:unexpected_{e}')
        print('status:error')
        return 'error'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Check task status')
    parser.add_argument('--job-id', required=True, help='Task job ID')
    args = parser.parse_args()

    status = check_status(args.job_id)
    sys.exit(0 if status != 'error' else 1)
