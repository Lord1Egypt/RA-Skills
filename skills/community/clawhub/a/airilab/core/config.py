#!/usr/bin/env python3
"""
Unified config and runtime health management for AiriLab.
"""

import base64
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .paths import get_airilab_home, get_config_dir, get_scheduler_dir, ensure_runtime_dirs
except ImportError:  # pragma: no cover
    from paths import get_airilab_home, get_config_dir, get_scheduler_dir, ensure_runtime_dirs

CONFIG_DIR = get_config_dir()
TOKEN_FILE = CONFIG_DIR / '.env'
PROJECT_FILE = CONFIG_DIR / 'project_config.json'

SCHEDULER_DIR = get_scheduler_dir()
DB_FILE = SCHEDULER_DIR / 'jobs.db'
PID_FILE = SCHEDULER_DIR / 'worker.pid'
LOG_FILE = SCHEDULER_DIR / 'worker.log'


class AiriLabConfig:
    """AiriLab unified config manager."""

    def __init__(self):
        ensure_runtime_dirs()

    # ==================== Token ====================

    def get_token(self) -> Optional[str]:
        if not TOKEN_FILE.exists():
            return None

        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('AIRILAB_API_KEY='):
                        return line.split('=', 1)[1].strip()
            return None
        except Exception:
            return None

    def save_token(self, token: str, phone: str = "") -> bool:
        try:
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                f.write('# AiriLab API Token\n')
                f.write(f'AIRILAB_API_KEY={token}\n')
                if phone:
                    f.write(f'AIRILAB_PHONE={phone}\n')
                f.write(f'AIRILAB_UPDATED={datetime.now().isoformat()}\n')
            return True
        except Exception as e:
            print(f'Failed to save token: {e}')
            return False

    def clear_token(self) -> bool:
        try:
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
            return True
        except Exception as e:
            print(f'Failed to clear token: {e}')
            return False

    def is_token_valid(self, token: str) -> bool:
        if not token:
            return False

        try:
            parts = token.split('.')
            if len(parts) != 3:
                return False

            payload = parts[1] + '=' * (-len(parts[1]) % 4)
            decoded = json.loads(base64.urlsafe_b64decode(payload))
            exp = decoded.get('exp')
            if exp and datetime.now() >= datetime.fromtimestamp(exp):
                return False

            return len(token) >= 50
        except Exception:
            return False

    # ==================== Project ====================

    def get_project(self) -> Optional[Dict[str, Any]]:
        if not PROJECT_FILE.exists():
            return None

        try:
            with open(PROJECT_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

            required_fields = ['teamId', 'projectId', 'projectName']
            if all(field in config for field in required_fields):
                return config
            return None
        except Exception:
            return None

    def save_project(self, team_id: int, project_id: int, project_name: str) -> bool:
        config = {
            'teamId': team_id,
            'projectId': project_id,
            'projectName': project_name,
            'selected_at': datetime.now().isoformat(),
        }

        try:
            with open(PROJECT_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f'Failed to save project config: {e}')
            return False

    def clear_project(self) -> bool:
        try:
            if PROJECT_FILE.exists():
                PROJECT_FILE.unlink()
            return True
        except Exception as e:
            print(f'Failed to clear project config: {e}')
            return False

    # ==================== Combined ====================

    def is_fully_configured(self) -> bool:
        return self.get_token() is not None and self.get_project() is not None

    def get_config_status(self) -> Dict[str, Any]:
        token = self.get_token()
        project = self.get_project()

        return {
            'has_token': token is not None,
            'has_project': project is not None,
            'is_ready': self.is_fully_configured(),
            'token_preview': f"{token[:20]}..." if token else None,
            'project': project,
        }

    def get_health_status(self) -> Dict[str, Any]:
        status = self.get_config_status()

        worker_pid = None
        worker_running = False
        if PID_FILE.exists():
            try:
                worker_pid = int(PID_FILE.read_text(encoding='utf-8').strip())
                if os.name == 'nt':
                    import ctypes

                    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                    handle = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_QUERY_LIMITED_INFORMATION, False, worker_pid
                    )
                    worker_running = bool(handle)
                    if handle:
                        ctypes.windll.kernel32.CloseHandle(handle)
                else:
                    os.kill(worker_pid, 0)
                    worker_running = True
            except Exception:
                worker_running = False

        job_counts = {
            'pending': 0,
            'processing': 0,
            'completed': 0,
            'failed': 0,
            'total': 0,
        }

        if DB_FILE.exists():
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('SELECT status, COUNT(1) FROM jobs GROUP BY status')
                for row in cursor.fetchall():
                    key = str(row[0])
                    count = int(row[1])
                    if key in job_counts:
                        job_counts[key] = count
                    job_counts['total'] += count
                conn.close()
            except Exception:
                pass

        return {
            'airilab_home': str(get_airilab_home()),
            'config_dir': str(CONFIG_DIR),
            'scheduler_dir': str(SCHEDULER_DIR),
            'token_file': str(TOKEN_FILE),
            'project_file': str(PROJECT_FILE),
            'db_file': str(DB_FILE),
            'log_file': str(LOG_FILE),
            'worker_pid_file': str(PID_FILE),
            'worker_pid': worker_pid,
            'worker_running': worker_running,
            'jobs': job_counts,
            **status,
        }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='AiriLab config management')
    parser.add_argument(
        'action', choices=['status', 'health', 'clear-token', 'clear-project', 'clear-all'], help='action'
    )

    args = parser.parse_args()

    config = AiriLabConfig()

    if args.action == 'status':
        status = config.get_config_status()
        print('AiriLab config status:')
        print(f"  Token: {'yes' if status['has_token'] else 'no'}")
        print(f"  Project: {'yes' if status['has_project'] else 'no'}")
        print(f"  Ready: {'yes' if status['is_ready'] else 'no'}")
        if status['project']:
            print(f"  Project Name: {status['project']['projectName']} (ID: {status['project']['projectId']})")

    elif args.action == 'health':
        health = config.get_health_status()
        print('AiriLab health')
        print(f"home: {health['airilab_home']}")
        print(f"ready: {health['is_ready']}")
        print(f"has_token: {health['has_token']}")
        print(f"has_project: {health['has_project']}")
        print(f"worker_running: {health['worker_running']}")
        print(f"worker_pid: {health['worker_pid']}")
        print(f"db: {health['db_file']}")
        print('jobs:')
        print(f"  pending: {health['jobs']['pending']}")
        print(f"  processing: {health['jobs']['processing']}")
        print(f"  completed: {health['jobs']['completed']}")
        print(f"  failed: {health['jobs']['failed']}")
        print(f"  total: {health['jobs']['total']}")

    elif args.action == 'clear-token':
        config.clear_token()
        print('Token cleared')

    elif args.action == 'clear-project':
        config.clear_project()
        print('Project config cleared')

    elif args.action == 'clear-all':
        config.clear_token()
        config.clear_project()
        print('All config cleared')
