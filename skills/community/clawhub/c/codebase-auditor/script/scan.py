#!/usr/bin/env python3
import argparse, json, os
from datetime import datetime

CRITICAL_PATTERNS = [
    '.env', '.env.*', '*.env',
    'config.json', '*.config.js', '*.config.ts',
    'application.yml', 'application.properties',
    'credentials.json', '*.pem', '*.key', 'service-account.json',
    '.github/workflows/*.yml', '.gitlab-ci.yml', 'Jenkinsfile',
    'Dockerfile', 'docker-compose.yml',
    'database.yml', 'knexfile.js', 'prisma/schema.prisma',
    'app.config.js', 'app.config.ts', 'config.yml',
]


def matches_pattern(filename, pattern):
    """Simple glob matching for file patterns."""
    import fnmatch
    return fnmatch.fnmatch(filename, pattern)


def scan_directory(root_dir):
    found = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden dirs and shared storage
        dirnames[:] = [d for d in dirnames if not d.startswith('.') or d == '.github']
        dirnames[:] = [d for d in dirnames if d != 'shared']

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_dir)

            for pattern in CRITICAL_PATTERNS:
                if matches_pattern(filename, pattern) or matches_pattern(rel_path, pattern):
                    ftype = "unknown"
                    importance = "high"

                    if '.env' in filename:
                        ftype = "environment"
                        importance = "critical"
                    elif 'service-account' in filename or filename.endswith(('.pem', '.key')):
                        ftype = "credentials"
                        importance = "critical"
                    elif 'config' in filename.lower() or filename.endswith(('.js', '.ts', '.json', '.yml', '.yaml')):
                        ftype = "configuration"
                        importance = "high"
                    elif filename in ('Dockerfile', 'docker-compose.yml', 'Jenkinsfile'):
                        ftype = "ci-cd"
                        importance = "high"
                    elif '.github' in rel_path or '.gitlab' in rel_path:
                        ftype = "ci-cd"
                        importance = "high"

                    description = f"{ftype} file at {rel_path}"
                    if ftype == "environment":
                        description = f"Contains runtime configuration and credentials"
                    elif ftype == "credentials":
                        description = f"Contains authentication material"

                    found.append({
                        "path": rel_path.replace('\\', '/'),
                        "type": ftype,
                        "importance": importance,
                        "description": description
                    })
                    break

    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-dir', required=True)
    parser.add_argument('--output-dir', default='./data/audit')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"[Codebase Auditor] Scanning: {args.project_dir}\n")
    files = scan_directory(args.project_dir)

    for f in files:
        print(f"  [{f['importance'].upper():8s}] {f['type']:15s} {f['path']}")
        print(f"                    {f['description']}")

    output = {
        "project_path": os.path.abspath(args.project_dir),
        "scan_timestamp": datetime.now().isoformat(),
        "total_files": len(files),
        "critical_files": files
    }

    output_path = os.path.join(args.output_dir, 'file_inventory.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Found {len(files)} critical files")
    print(f"[OK] Inventory: {output_path}")


if __name__ == '__main__':
    main()
