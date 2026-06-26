#!/usr/bin/env python3
import json, time, subprocess
from pathlib import Path

QUEUE_DIR = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/callback-queue')
DONE_DIR = QUEUE_DIR / 'done'
FAIL_DIR = QUEUE_DIR / 'failed'
FINALIZER = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/scripts/card_callback_finalize.py')
PID_FILE = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/callback-queue-worker.pid')


def claim_job(path: Path):
    processing = path.with_suffix('.processing')
    try:
        path.rename(processing)
        return processing
    except Exception:
        return None


def run_job(job_file: Path):
    data = json.loads(job_file.read_text(encoding='utf-8'))
    cmd = [
        'python3', str(FINALIZER),
        '--channel', data.get('channel', 'feishu'),
        '--user-id', data['user_id'],
        '--account-id', str(data.get('account_id', '1')),
        '--payload', json.dumps(data['payload'], ensure_ascii=False),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180)


def recover_orphan_processing_files():
    for p in QUEUE_DIR.glob('*.processing'):
        try:
            target = QUEUE_DIR / (p.stem + '.json')
            p.rename(target)
        except Exception:
            try:
                fail = FAIL_DIR / (p.stem + '.recover-fail.json')
                fail.write_text(json.dumps({'ok': False, 'error': 'orphan_processing_recover_failed', 'file': str(p)}, ensure_ascii=False), encoding='utf-8')
            except Exception:
                pass


def cleanup_history(max_done=500, max_failed=500):
    for d, cap in ((DONE_DIR, max_done), (FAIL_DIR, max_failed)):
        files = sorted([p for p in d.glob('*') if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        for p in files[cap:]:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


def main():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAIL_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(__import__('os').getpid()), encoding='utf-8')
    recover_orphan_processing_files()
    cleanup_history()

    last_cleanup = time.time()
    while True:
        jobs = sorted([p for p in QUEUE_DIR.glob('*.json') if p.is_file()])
        if time.time() - last_cleanup > 300:
            cleanup_history()
            last_cleanup = time.time()
        if not jobs:
            time.sleep(0.2)
            continue

        for job in jobs:
            claimed = claim_job(job)
            if not claimed:
                continue
            try:
                res = run_job(claimed)
                if res.returncode == 0:
                    target = DONE_DIR / (claimed.stem + '.done.json')
                    target.write_text(json.dumps({'ok': True, 'stdout': res.stdout.strip()}, ensure_ascii=False), encoding='utf-8')
                else:
                    target = FAIL_DIR / (claimed.stem + '.fail.json')
                    target.write_text(json.dumps({'ok': False, 'code': res.returncode, 'stdout': res.stdout, 'stderr': res.stderr}, ensure_ascii=False), encoding='utf-8')
            except Exception as ex:
                target = FAIL_DIR / (claimed.stem + '.fail.json')
                target.write_text(json.dumps({'ok': False, 'error': str(ex)}, ensure_ascii=False), encoding='utf-8')
            finally:
                try:
                    claimed.unlink(missing_ok=True)
                except Exception:
                    pass


if __name__ == '__main__':
    main()
