#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import signal
import subprocess
import sys
import time


def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _active_workers(handoff_dir: pathlib.Path, stale_seconds: int) -> tuple[int, list[dict]]:
    now = int(time.time())
    active: list[dict] = []
    for f in sorted(handoff_dir.glob('*.json')):
        try:
            row = json.loads(f.read_text())
        except Exception:
            continue
        pid = row.get('worker_pid')
        started = int(row.get('worker_started_at_s') or 0)
        if not isinstance(pid, int) or pid <= 0:
            continue
        alive = _is_pid_alive(pid)
        stale = bool(started and (now - started > stale_seconds))
        if stale and alive:
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.2)
                if _is_pid_alive(pid):
                    os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            alive = _is_pid_alive(pid)
            row['orphan_cleanup'] = {'stale_seconds': stale_seconds, 'cleaned_at_s': now, 'terminated': not alive}
            f.write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
        if alive:
            active.append({'pid': pid, 'request_id': row.get('request_id'), 'file': str(f)})
    return len(active), active


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', required=True)
    p.add_argument('--count', type=int, required=True)
    p.add_argument('--out-dir', required=True)
    p.add_argument('--prefix', default='image')
    p.add_argument('--ext', default='png')
    p.add_argument('--model', default='google/gemini-3.1-flash-image-preview')
    p.add_argument('--image-size', choices=['low', 'medium', 'high'], default='')
    p.add_argument('--clarify-hints', action='store_true')
    p.add_argument('--strict-clarify', action='store_true')
    p.add_argument('--baseline-image', default='')
    p.add_argument('--baseline-source-kind', choices=['current_attachment', 'reply_attachment', 'explicit_path_or_url'], default='')
    p.add_argument('--variation-strength', choices=['low', 'medium', 'high'], default='')
    p.add_argument('--must-keep', action='append', default=[])
    p.add_argument('--lock-palette', action='store_true')
    p.add_argument('--lock-composition', action='store_true')
    p.add_argument('--confirm-external-upload', action='store_true')
    p.add_argument('--queue-dir', default='generated/imagegen-queue')
    p.add_argument('--request-id', required=True)
    p.add_argument('--start-index', type=int, default=1)
    p.add_argument('--base-dir', default=str(pathlib.Path(__file__).resolve().parents[1]))
    p.add_argument('--dry-run-worker', action='store_true')
    p.add_argument('--max-background-workers', type=int, default=2)
    p.add_argument('--orphan-timeout-sec', type=int, default=1800)
    args = p.parse_args()

    scripts_dir = pathlib.Path(__file__).resolve().parent
    enqueue_variants = scripts_dir / 'enqueue_variants.py'
    run_queue = scripts_dir / 'run_image_queue.py'

    cmd = [
        sys.executable,
        str(enqueue_variants),
        '--prompt', args.prompt,
        '--count', str(args.count),
        '--out-dir', args.out_dir,
        '--prefix', args.prefix,
        '--ext', args.ext,
        '--model', args.model,
        '--queue-dir', args.queue_dir,
        '--request-id', args.request_id,
        '--start-index', str(args.start_index),
    ]
    if args.image_size:
        cmd.extend(['--image-size', args.image_size])
    if args.clarify_hints:
        cmd.append('--clarify-hints')
    if args.strict_clarify:
        cmd.append('--strict-clarify')
    if args.baseline_image:
        cmd.extend(['--baseline-image', args.baseline_image])
    if args.baseline_source_kind:
        cmd.extend(['--baseline-source-kind', args.baseline_source_kind])
    if args.variation_strength:
        cmd.extend(['--variation-strength', args.variation_strength])
    for mk in args.must_keep:
        cmd.extend(['--must-keep', mk])
    if args.lock_palette:
        cmd.append('--lock-palette')
    if args.lock_composition:
        cmd.append('--lock-composition')
    if args.confirm_external_upload:
        cmd.append('--confirm-external-upload')

    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        print(cp.stderr.strip() or cp.stdout.strip(), file=sys.stderr)
        return cp.returncode

    queue_dir = pathlib.Path(args.queue_dir)
    handoff_dir = queue_dir / 'handoff'
    handoff_dir.mkdir(parents=True, exist_ok=True)

    worker_cmd = [
        sys.executable,
        str(run_queue),
        '--queue-dir', args.queue_dir,
        '--request-id', args.request_id,
        '--handoff-mode', 'background',
    ]

    pid = None
    worker_log = handoff_dir / f'{args.request_id}.worker.log'
    active_count, active_workers = _active_workers(handoff_dir, stale_seconds=args.orphan_timeout_sec)
    worker_state = 'spawned'
    worker_skip_reason = ''
    if active_count >= args.max_background_workers:
        worker_state = 'skipped'
        worker_skip_reason = f'active_workers={active_count} >= max_background_workers={args.max_background_workers}'
    elif not args.dry_run_worker:
        with worker_log.open('ab') as logf:
            proc = subprocess.Popen(worker_cmd, stdout=logf, stderr=logf, stdin=subprocess.DEVNULL, start_new_session=True)
            pid = proc.pid

    handoff = {
        'request_id': args.request_id,
        'queued_at_ms': int(time.time() * 1000),
        'handoff_mode': 'background',
        'worker_cmd': worker_cmd,
        'worker_pid': pid,
        'worker_log': str(worker_log),
        'worker_started_at_s': int(time.time()) if pid else None,
        'worker_state': worker_state,
        'worker_skip_reason': worker_skip_reason,
        'active_workers_before_spawn': active_workers,
        'max_background_workers': args.max_background_workers,
        'orphan_timeout_sec': args.orphan_timeout_sec,
        'enqueue_stdout': cp.stdout.strip(),
    }
    handoff_path = handoff_dir / f'{args.request_id}.json'
    handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + '\n')

    # Contract: return immediately with queued ack payload.
    ack = {
        'status': 'queued',
        'request_id': args.request_id,
        'handoff_mode': 'background',
        'handoff_file': str(handoff_path),
        'worker_state': worker_state,
    }
    if worker_state == 'skipped':
        ack['status'] = 'queued_no_worker'
        ack['reason'] = worker_skip_reason
    print(json.dumps(ack, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
