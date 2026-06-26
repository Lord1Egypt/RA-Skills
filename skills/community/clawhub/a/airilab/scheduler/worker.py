#!/usr/bin/env python3
"""
AiriLab background polling worker.
"""

import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

AIRILAB_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AIRILAB_PATH))

from core.paths import ensure_runtime_dirs, get_scheduler_dir  # noqa: E402

ensure_runtime_dirs()

DATA_DIR = get_scheduler_dir()
SCRIPTS_DIR = AIRILAB_PATH / 'scripts'
DB_PATH = DATA_DIR / 'jobs.db'
PID_FILE = DATA_DIR / 'worker.pid'
LOG_FILE = DATA_DIR / 'worker.log'

POLL_INTERVAL = 15
MAX_ATTEMPTS = 60
TIMEOUT_MINUTES = 15

STATUS_PENDING = 'pending'
STATUS_PROCESSING = 'processing'
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger('airilab-worker')


class WorkerLockError(RuntimeError):
    pass


def _is_pid_running(pid: int) -> bool:
    if pid <= 0:
        return False

    try:
        if os.name == 'nt':
            import ctypes

            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return False

        os.kill(pid, 0)
        return True
    except Exception:
        return False


def acquire_worker_lock() -> None:
    if PID_FILE.exists():
        try:
            existing_pid = int(PID_FILE.read_text(encoding='utf-8').strip())
        except Exception:
            existing_pid = 0

        if _is_pid_running(existing_pid):
            raise WorkerLockError(f'worker already running (pid={existing_pid})')

        try:
            PID_FILE.unlink()
        except Exception:
            pass

    PID_FILE.write_text(str(os.getpid()), encoding='utf-8')


def release_worker_lock() -> None:
    try:
        if PID_FILE.exists():
            content = PID_FILE.read_text(encoding='utf-8').strip()
            if content == str(os.getpid()):
                PID_FILE.unlink()
    except Exception:
        pass


def startup_self_check() -> None:
    if not SCRIPTS_DIR.exists():
        raise RuntimeError(f'scripts dir missing: {SCRIPTS_DIR}')

    required_scripts = [SCRIPTS_DIR / 'check_status.py', SCRIPTS_DIR / 'fetch.py']
    for script in required_scripts:
        if not script.exists():
            raise RuntimeError(f'missing required script: {script}')

    ensure_runtime_dirs()
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            tool TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            submitted_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            input_params TEXT,
            output_url TEXT,
            thumbnail_url TEXT,
            error_message TEXT,
            attempts INTEGER DEFAULT 0
        )
        '''
    )
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user ON jobs(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_submitted ON jobs(submitted_at)')
    conn.commit()
    conn.close()
    logger.info('database initialized')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_job(job_id: str, user_id: str, chat_id: str, tool: str, input_params: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT OR REPLACE INTO jobs
        (job_id, user_id, chat_id, tool, status, submitted_at, input_params)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (job_id, user_id, chat_id, tool, STATUS_PENDING, datetime.now().isoformat(), json.dumps(input_params)),
    )
    conn.commit()
    conn.close()
    logger.info(f'job saved: {job_id}')


def get_pending_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM jobs
        WHERE status IN (?, ?)
        ORDER BY submitted_at ASC
        LIMIT 50
        ''',
        (STATUS_PENDING, STATUS_PROCESSING),
    )
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def update_job_status(job_id: str, status: str, output_url: str = None, thumbnail_url: str = None, error_message: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if status == STATUS_COMPLETED:
        cursor.execute(
            '''
            UPDATE jobs
            SET status = ?, completed_at = ?, output_url = ?, thumbnail_url = ?
            WHERE job_id = ?
            ''',
            (status, datetime.now().isoformat(), output_url, thumbnail_url, job_id),
        )
    elif status == STATUS_FAILED:
        cursor.execute(
            '''
            UPDATE jobs
            SET status = ?, completed_at = ?, error_message = ?
            WHERE job_id = ?
            ''',
            (status, datetime.now().isoformat(), error_message, job_id),
        )
    else:
        cursor.execute(
            '''
            UPDATE jobs
            SET status = ?, attempts = attempts + 1
            WHERE job_id = ?
            ''',
            (status, job_id),
        )

    conn.commit()
    conn.close()


def check_job_status(job_id: str) -> str:
    script_path = SCRIPTS_DIR / 'check_status.py'
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), '--job-id', job_id],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        logger.warning(f'check status timeout: {job_id}')
        return 'error'
    except Exception as e:
        logger.warning(f'check status failed {job_id}: {e}')
        return 'error'

    output = ((result.stdout or '') + '\n' + (result.stderr or '')).strip()
    lowered = output.lower()

    if 'error:missing_token' in lowered:
        return 'auth_error'
    if 'error:missing_project' in lowered:
        return 'error'

    for line in output.splitlines():
        match = re.search(r'^\s*(?:status|状态)\s*[:：]\s*([A-Za-z_]+)\s*$', line, re.IGNORECASE)
        if match:
            return match.group(1).strip().lower()

    if result.returncode != 0:
        return 'error'
    return 'unknown'


def fetch_result(job_id: str) -> dict:
    script_path = SCRIPTS_DIR / 'fetch.py'
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), '--job-id', job_id, '--format', 'json'],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return {'error': 'timeout'}
    except Exception as e:
        return {'error': str(e)}

    output = ((result.stdout or '') + '\n' + (result.stderr or '')).strip()
    if 'error:missing_token' in output.lower():
        return {'error': 'auth_required'}

    try:
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(output)
    except json.JSONDecodeError:
        return {'error': 'parse_failed', 'raw': output}


def notify_user(user_id: str, chat_id: str, job_id: str, status: str, output_urls: list = None, error_message: str = None, tool: str = None):
    completions_dir = Path.home() / '.openclaw' / 'completions'
    completions_dir.mkdir(parents=True, exist_ok=True)
    completion_file = completions_dir / f"airilab_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    if status == STATUS_COMPLETED:
        lines = [
            '✅ **任务完成**',
            '',
            f'🔎 **Job ID**: `{job_id}`',
            f'🎨 **工具**: {tool or "AiriLab"}',
            '',
            '🖼️ **生成结果**:',
            '',
        ]
        for i, url in enumerate(output_urls or [], 1):
            lines.append(f'![图片{i}]({url})')
            lines.append('')
        lines.append(f'_共 {len(output_urls or [])} 张图片_')
        message = '\n'.join(lines)
    else:
        message = (
            '❌ **任务失败**\n\n'
            f'🔎 **Job ID**: `{job_id}`\n'
            f'⚠️ **错误**: {error_message or "未知错误"}\n\n'
            '请重试或联系管理员。'
        )

    try:
        with open(completion_file, 'w', encoding='utf-8') as f:
            f.write(message)
    except Exception as e:
        logger.error(f'write completion failed: {e}')

    with open(DATA_DIR / 'notifications.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {user_id} | {chat_id} | {job_id} | {status}\n")


def process_job(job):
    job_id = job['job_id']
    user_id = job['user_id']
    chat_id = job['chat_id']
    attempts = int(job['attempts'] or 0)
    tool = job['tool']
    submitted_at = job['submitted_at']

    if attempts >= MAX_ATTEMPTS:
        detail = f'轮询超时（{TIMEOUT_MINUTES}分钟）'
        update_job_status(job_id, STATUS_FAILED, error_message=detail)
        notify_user(user_id, chat_id, job_id, STATUS_FAILED, error_message=detail, tool=tool)
        return

    elapsed = 0.0
    try:
        submitted_time = datetime.fromisoformat(submitted_at)
        elapsed = (datetime.now() - submitted_time).total_seconds() / 60
        if elapsed > TIMEOUT_MINUTES:
            detail = f'任务超时（{elapsed:.1f}分钟）'
            update_job_status(job_id, STATUS_FAILED, error_message=detail)
            notify_user(user_id, chat_id, job_id, STATUS_FAILED, error_message=detail, tool=tool)
            return
    except Exception as e:
        logger.error(f'parse submitted time failed {job_id}: {e}')

    logger.info(f'checking job={job_id} attempt={attempts + 1}/{MAX_ATTEMPTS} elapsed={elapsed:.1f}m')
    status = check_job_status(job_id)

    # 业务规则：只要状态不是 processing，就视为生成流程结束并立即拉取结果。
    if status == STATUS_PROCESSING:
        update_job_status(job_id, STATUS_PROCESSING)
        return

    result = fetch_result(job_id)
    if result.get('error') or not result.get('success', False):
        fetch_detail = result.get('error') or result.get('message') or 'fetch_failed'
        if status == 'auth_error':
            detail = 'Token 过期，请重新登录'
        else:
            detail = f'终态={status}, 拉取结果失败: {fetch_detail}'
        update_job_status(job_id, STATUS_FAILED, error_message=detail)
        notify_user(user_id, chat_id, job_id, STATUS_FAILED, error_message=detail, tool=tool)
        return

    output_urls = result.get('output_urls', [])
    thumbnail_url = result.get('thumbnail_url', '')
    result_tool = result.get('toolset', tool)

    update_job_status(job_id, STATUS_COMPLETED, output_url=json.dumps(output_urls), thumbnail_url=thumbnail_url)
    notify_user(user_id, chat_id, job_id, STATUS_COMPLETED, output_urls=output_urls, tool=result_tool)
    return


def run():
    logger.info('=' * 60)
    logger.info('AiriLab worker starting')
    logger.info(f'data_dir={DATA_DIR}')
    logger.info(f'db={DB_PATH}')
    logger.info(f'poll_interval={POLL_INTERVAL}s timeout={TIMEOUT_MINUTES}m max_attempts={MAX_ATTEMPTS}')

    startup_self_check()
    init_db()
    acquire_worker_lock()

    try:
        logger.info(f'worker lock acquired pid={os.getpid()}')
        while True:
            jobs = get_pending_jobs()
            if jobs:
                logger.info(f'found {len(jobs)} pending/processing jobs')
                for job in jobs:
                    try:
                        process_job(job)
                    except Exception as e:
                        logger.error(f'process job failed {job["job_id"]}: {e}')
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        logger.info('worker stopped')
    finally:
        release_worker_lock()


if __name__ == '__main__':
    try:
        run()
    except WorkerLockError as e:
        logger.error(str(e))
        sys.exit(1)
