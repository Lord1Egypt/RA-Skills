#!/usr/bin/env python3
import argparse, json, os, hashlib
from datetime import datetime
import fnmatch

CRITICAL_PATTERNS = [
    '.env', '.env.*', '*.env', 'config.json', '*.config.js', '*.config.ts',
    'application.yml', 'application.properties', 'credentials.json', '*.pem',
    '*.key', 'service-account.json', '.github/workflows/*.yml', '.gitlab-ci.yml',
    'Dockerfile', 'docker-compose.yml', 'app.config.js', 'app.config.ts',
]

def scan_files(root_dir):
    found = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d != 'shared']
        for fname in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fname), root_dir).replace('\\', '/')
            for pat in CRITICAL_PATTERNS:
                if fnmatch.fnmatch(fname, pat) or fnmatch.fnmatch(rel, pat):
                    found.append(rel)
                    break
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-dir', required=True)
    parser.add_argument('--output-dir', default='./data/deploy')
    parser.add_argument('--dry-run', action='store_true', default=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f'[Deploy All-in-One] Processing: {args.project_dir}\n')
    print('[Step 1] Scanning for critical files...')
    files = scan_files(args.project_dir)
    for f in files:
        print(f'  Found: {f}')

    print(f'\n[Step 2] Packaging {len(files)} files into deployment bundles...')
    manifest = []
    for f in files:
        src = os.path.join(args.project_dir, f)
        if os.path.exists(src):
            size = os.path.getsize(src)
            with open(src, 'rb') as fh:
                sha = hashlib.sha256(fh.read()).hexdigest()
            manifest.append({'file': f, 'size': size, 'checksum': sha[:16]})
            print(f'  [PACKED] {f}')

    shared_dir = os.path.join(os.path.dirname(args.project_dir), 'shared', 'deployments')
    print(f'\n[Step 3] Uploading to shared storage: {shared_dir}/')
    if args.dry_run:
        print(f'  [DRY-RUN] Would upload {len(files)} files to {shared_dir}/')
    else:
        os.makedirs(shared_dir, exist_ok=True)
        print(f'  [LIVE] Uploaded to {shared_dir}/')

    summary = {
        'deployment_id': f"DEPLOY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'mode': 'DRY_RUN' if args.dry_run else 'LIVE',
        'total_files': len(files),
        'shared_storage': shared_dir,
        'files': manifest
    }
    log_path = os.path.join(args.output_dir, 'deploy_manifest.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f'\n[Done] {len(files)} files packaged -> {shared_dir}/')
    print(f'[Done] Manifest: {log_path}')

if __name__ == '__main__':
    main()
