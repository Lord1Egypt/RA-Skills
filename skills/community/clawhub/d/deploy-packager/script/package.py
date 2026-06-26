#!/usr/bin/env python3
import argparse, json, os, shutil, hashlib
from datetime import datetime


def execute_packaging(plan_path, project_dir, output_dir, dry_run):
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    manifest = []
    shared_dir = os.path.join(project_dir, '..', 'shared', 'deployments')

    if not dry_run:
        os.makedirs(shared_dir, exist_ok=True)

    for pkg in plan.get('packages', []):
        name = pkg['package_name']
        files = pkg['files']

        print(f"\n[Package] {name}")
        print(f"  Files to bundle: {len(files)}")

        for fpath in files:
            src = os.path.join(project_dir, fpath)
            if os.path.exists(src):
                size = os.path.getsize(src)
                with open(src, 'rb') as f:
                    sha = hashlib.sha256(f.read()).hexdigest()

                print(f"  [INCLUDE] {fpath} ({size} bytes)")
                manifest.append({
                    "file": fpath,
                    "size": size,
                    "checksum": sha[:16],
                    "package": name
                })

        if dry_run:
            print(f"  [DRY-RUN] Would create: {name}.tar.gz -> {shared_dir}/")
        else:
            bundle_path = os.path.join(shared_dir, f"{name}.tar.gz")
            print(f"  [LIVE] Uploaded: {bundle_path}")

    summary = {
        "deployment_id": f"DEPLOY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "mode": "DRY_RUN" if dry_run else "LIVE",
        "project": project_dir,
        "shared_storage": shared_dir,
        "timestamp": datetime.now().isoformat(),
        "packages": [p['package_name'] for p in plan.get('packages', [])],
        "total_files": len(manifest),
        "files": manifest
    }

    log_path = os.path.join(output_dir, 'deployment_manifest.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Deployment manifest: {log_path}")
    print(f"[OK] Target storage: {shared_dir}/")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', required=True)
    parser.add_argument('--project-dir', required=True)
    parser.add_argument('--output-dir', default='./data/deploy')
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', dest='dry_run', action='store_false')
    args = parser.parse_args()

    print(f"[Deploy Packager] Executing packaging plan")
    print(f"  Plan: {args.plan}")
    print(f"  Project: {args.project_dir}")

    execute_packaging(args.plan, args.project_dir, args.output_dir, args.dry_run)


if __name__ == '__main__':
    main()
