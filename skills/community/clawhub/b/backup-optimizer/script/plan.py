#!/usr/bin/env python3
import argparse, json, os

def generate_package_plan(inventory_path):
    with open(inventory_path, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    files = inventory.get('critical_files', [])
    project_dir = inventory.get('project_path', '')

    env_config_files = []
    cicd_files = []

    for f in files:
        ftype = f['type']
        fpath = f['path']

        if ftype in ('environment', 'credentials', 'configuration'):
            env_config_files.append(f)
            print(f"  [ENV-CONFIG] {fpath} ({ftype})")
        elif ftype == 'ci-cd':
            cicd_files.append(f)
            print(f"  [CI-CD]      {fpath}")

    plan = {
        "project_path": project_dir,
        "plan_timestamp": __import__('datetime').datetime.now().isoformat(),
        "packages": []
    }

    if env_config_files:
        plan["packages"].append({
            "package_name": "environment-config-bundle",
            "description": "Environment files, credentials, and configuration for deployment consistency. Includes .env, config files, credential files, and database configs.",
            "files": [f["path"] for f in env_config_files],
            "rationale": "Configuration files must travel with deployment to ensure environment consistency. This bundle includes all environment variables, credentials, and service account keys needed at runtime."
        })

    if cicd_files:
        plan["packages"].append({
            "package_name": "ci-cd-config-bundle",
            "description": "CI/CD pipeline configuration files for build server consistency.",
            "files": [f["path"] for f in cicd_files],
            "rationale": "Pipeline configuration ensures consistent build and deployment behavior across environments."
        })

    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output-dir', default='./data/plan')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"[Backup Optimizer] Generating packaging plan from: {args.input}\n")
    plan = generate_package_plan(args.input)

    output_path = os.path.join(args.output_dir, 'packaging_plan.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] {len(plan['packages'])} package(s) planned")
    for pkg in plan['packages']:
        print(f"      {pkg['package_name']}: {len(pkg['files'])} files")
    print(f"[OK] Plan: {output_path}")


if __name__ == '__main__':
    main()
