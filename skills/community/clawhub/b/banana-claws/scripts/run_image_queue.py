#!/usr/bin/env python3
import argparse
import json
import pathlib
import subprocess
import sys
import time


def _now_ms() -> int:
    return int(time.time() * 1000)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--queue-dir', default='generated/imagegen-queue')
    p.add_argument('--base-dir', default=str(pathlib.Path(__file__).resolve().parents[1]))
    p.add_argument('--max-jobs', type=int, default=0, help='0 means no limit')
    p.add_argument('--request-id', default='', help='Only process jobs matching this request id')
    p.add_argument('--handoff-mode', choices=['background', 'foreground'], default='foreground')
    args = p.parse_args()

    queue_dir = pathlib.Path(args.queue_dir)
    pending = queue_dir / 'pending'
    processing = queue_dir / 'processing'
    results = queue_dir / 'results'
    failed = queue_dir / 'failed'
    for d in (pending, processing, results, failed):
        d.mkdir(parents=True, exist_ok=True)

    gen_script = pathlib.Path(args.base_dir) / 'scripts' / 'generate_image.py'
    if not gen_script.exists():
        print(f'Missing generator script: {gen_script}', file=sys.stderr)
        return 2

    processed = 0
    pending_jobs = sorted(pending.glob('*.json'))

    for job_file in pending_jobs:
        if args.max_jobs and processed >= args.max_jobs:
            break

        proc_file = processing / job_file.name
        try:
            job_file.rename(proc_file)
        except FileNotFoundError:
            continue

        job = json.loads(proc_file.read_text())
        if args.request_id and job.get('request_id') != args.request_id:
            # Return unrelated jobs back to pending untouched.
            job_file_back = pending / proc_file.name
            proc_file.rename(job_file_back)
            continue
        job['status'] = 'processing'
        job['started_at_ms'] = _now_ms()
        job['handoff_mode'] = args.handoff_mode
        proc_file.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n')

        response_json_path = results / (proc_file.stem + '.provider-response.json')
        cmd = [
            sys.executable,
            str(gen_script),
            '--prompt',
            job['prompt'],
            '--out',
            job['out'],
            '--model',
            job.get('model') or 'google/gemini-3.1-flash-image-preview',
            '--output-format',
            'json',
            '--save-response-json',
            str(response_json_path),
        ]
        if job.get('image_size'):
            cmd.extend(['--image-size', job['image_size']])
        if job.get('clarify_hints'):
            cmd.append('--clarify-hints')
        if job.get('strict_clarify'):
            cmd.append('--strict-clarify')
        if job.get('baseline_image'):
            cmd.extend(['--baseline-image', job['baseline_image']])
        if job.get('baseline_source_kind'):
            cmd.extend(['--baseline-source-kind', job['baseline_source_kind']])
        if job.get('variation_strength'):
            cmd.extend(['--variation-strength', job['variation_strength']])
        for mk in (job.get('must_keep') or []):
            cmd.extend(['--must-keep', mk])
        if job.get('lock_palette'):
            cmd.append('--lock-palette')
        if job.get('lock_composition'):
            cmd.append('--lock-composition')
        if job.get('confirm_external_upload'):
            cmd.append('--confirm-external-upload')

        cp = subprocess.run(cmd, capture_output=True, text=True)
        job['finished_at_ms'] = _now_ms()
        job['exit_code'] = cp.returncode
        job['stdout'] = (cp.stdout or '').strip()
        job['stderr'] = (cp.stderr or '').strip()

        parsed = None
        if cp.stdout:
            try:
                parsed = json.loads(cp.stdout.strip())
            except Exception:
                parsed = None

        if isinstance(parsed, dict):
            job['generator_result'] = parsed
            job['provider_generation_id'] = parsed.get('provider_generation_id')
            job['provider_model'] = parsed.get('provider_model')
            job['provider_created'] = parsed.get('provider_created')
            job['provider_usage'] = parsed.get('provider_usage')
            job['edit_intent_detected'] = parsed.get('edit_intent_detected')
            job['baseline_applied'] = parsed.get('baseline_applied')
            job['baseline_source'] = parsed.get('baseline_source')
            job['baseline_source_kind'] = parsed.get('baseline_source_kind')
            job['baseline_resolution_policy'] = parsed.get('baseline_resolution_policy')
            job['rails_applied'] = parsed.get('rails_applied')
            job['clarify_hints'] = parsed.get('clarify_hints')
            if parsed.get('provider_response') is not None:
                job['provider_response'] = parsed.get('provider_response')

        if response_json_path.exists():
            job['provider_response_path'] = str(response_json_path)

        job['same_turn_drain_detected'] = args.handoff_mode == 'foreground'

        if cp.returncode == 0:
            job['status'] = 'succeeded'
            dest = results / proc_file.name
        else:
            job['status'] = 'failed'
            dest = failed / proc_file.name

        dest.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n')
        proc_file.unlink(missing_ok=True)

        processed += 1

    print(json.dumps({'processed': processed, 'queue_dir': str(queue_dir)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
