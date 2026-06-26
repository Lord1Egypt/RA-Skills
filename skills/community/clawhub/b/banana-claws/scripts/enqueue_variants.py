#!/usr/bin/env python3
import argparse
import json
import pathlib
import subprocess
import sys
import time


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', required=True, help='Base prompt for all variants')
    p.add_argument('--count', type=int, required=True, help='Number of variants to enqueue')
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
    p.add_argument('--request-id', default='')
    p.add_argument('--start-index', type=int, default=1)
    args = p.parse_args()

    if args.count < 1:
        print('--count must be >= 1', file=sys.stderr)
        return 2

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    enqueue_script = pathlib.Path(__file__).resolve().parent / 'enqueue_image_job.py'
    if not enqueue_script.exists():
        print(f'Missing enqueue script: {enqueue_script}', file=sys.stderr)
        return 2

    enqueued = 0
    manifest = {
        'created_at_ms': int(time.time() * 1000),
        'request_id': args.request_id,
        'baseline_image': args.baseline_image,
        'baseline_source_kind': args.baseline_source_kind,
        'variation_strength': args.variation_strength,
        'must_keep': args.must_keep,
        'lock_palette': args.lock_palette,
        'lock_composition': args.lock_composition,
        'confirm_external_upload': args.confirm_external_upload,
        'image_size': args.image_size,
        'variants': [],
    }

    for i in range(args.start_index, args.start_index + args.count):
        out_path = out_dir / f"{args.prefix}-{i:02d}.{args.ext.lstrip('.')}"
        prompt = f"{args.prompt}\n\nVariant {i}. Keep composition distinct from other variants."
        cmd = [
            sys.executable,
            str(enqueue_script),
            '--prompt',
            prompt,
            '--out',
            str(out_path),
            '--model',
            args.model,
            '--queue-dir',
            args.queue_dir,
            '--request-id',
            args.request_id,
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

        job_info = json.loads((cp.stdout or '{}').strip())
        manifest['variants'].append({
            'variant_index': i,
            'job_id': job_info.get('job_id'),
            'job_path': job_info.get('job_path'),
            'out': str(out_path),
        })
        enqueued += 1

    manifest_path = out_dir / f"{args.prefix}-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    print(f'Enqueued {enqueued} jobs to {args.queue_dir}')
    print(str(manifest_path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
