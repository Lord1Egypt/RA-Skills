#!/usr/bin/env python3
import argparse
import json
import pathlib
import time
import uuid


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', required=True)
    p.add_argument('--out', required=True)
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
    args = p.parse_args()

    queue_dir = pathlib.Path(args.queue_dir)
    pending = queue_dir / 'pending'
    pending.mkdir(parents=True, exist_ok=True)

    ts = int(time.time() * 1000)
    job_id = f"img-{ts}-{uuid.uuid4().hex[:8]}"
    job = {
        'job_id': job_id,
        'created_at_ms': ts,
        'prompt': args.prompt,
        'out': args.out,
        'model': args.model,
        'image_size': args.image_size,
        'clarify_hints': args.clarify_hints,
        'strict_clarify': args.strict_clarify,
        'baseline_image': args.baseline_image,
        'baseline_source_kind': args.baseline_source_kind,
        'variation_strength': args.variation_strength,
        'must_keep': args.must_keep,
        'lock_palette': args.lock_palette,
        'lock_composition': args.lock_composition,
        'confirm_external_upload': args.confirm_external_upload,
        'request_id': args.request_id,
        'status': 'queued',
    }

    job_path = pending / f'{job_id}.json'
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n')

    print(json.dumps({'job_id': job_id, 'job_path': str(job_path)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
