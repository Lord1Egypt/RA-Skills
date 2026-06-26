"""
Dataset lifecycle management: detail, versions, quota, permissions.

Usage:
    python dataset_manager.py quota --project_id 154
    python dataset_manager.py detail --id 138201
    python dataset_manager.py versions --id 138201
    python dataset_manager.py new_version --id 138201 --desc "v2 with more data"
"""

import argparse
import json
import os
import sys

import requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://openapi.dp.tech/openapi/v1/ds"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}


def check_quota(project_id: int):
    """Check dataset quota for a project."""
    r = requests.get(
        f"{BASE}/quota/check",
        headers=HEADERS,
        params={"projectId": project_id},
    )
    data = r.json().get("data", {})
    limit = data.get("limit", "?")
    used = data.get("used", "?")
    available = data.get("result", "?")
    print(f"Dataset quota for project {project_id}:")
    print(f"  Limit:     {limit}")
    print(f"  Used:      {used}")
    print(f"  Available: {available}")


def get_detail(dataset_id: int):
    """Get dataset details."""
    r = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS)
    data = r.json().get("data", {})
    print(f"Dataset: {data.get('title', '?')}")
    print(f"  ID:      {data.get('id')}")
    print(f"  Path:    {data.get('path')}")
    print(f"  Project: {data.get('projectName')}")
    print(f"  Creator: {data.get('creatorName')}")
    print(f"  Status:  {data.get('status')}")
    print(f"  Version: {data.get('versionId')}")


def list_versions(dataset_id: int):
    """List all versions of a dataset."""
    r = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS)
    data = r.json().get("data", {})
    items = data if isinstance(data, list) else data.get("items", [])

    print(f"Versions for dataset {dataset_id}:\n")
    for v in items:
        version = v.get("version", "?")
        total_count = v.get("totalCount", 0)
        total_size = v.get("totalSize", 0)
        path = v.get("datasetPath", "?")
        size_mb = total_size / (1024 * 1024) if total_size else 0
        print(f"  v{version}: {total_count} files, {size_mb:.1f} MB")
        print(f"    Mount path: {path}")
        if v.get("downloadUri"):
            print(f"    Download:   {v['downloadUri']}")
        print()


def create_version(dataset_id: int, desc: str):
    """Create a new version of an existing dataset."""
    r = requests.post(
        f"{BASE}/{dataset_id}/version",
        headers=HEADERS_JSON,
        json={"versionDesc": desc},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"New version created for dataset {dataset_id}")
        print(f"Description: {desc}")
        print("Note: Version preparation may take a few minutes for large datasets.")
    else:
        print(f"Failed: {result}")


def check_permission(dataset_id: int):
    """Check dataset permissions."""
    r = requests.get(f"{BASE}/{dataset_id}/permission", headers=HEADERS)
    data = r.json().get("data", {})
    print(f"Permissions for dataset {dataset_id}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Bohrium dataset manager")
    sub = parser.add_subparsers(dest="cmd")

    p_quota = sub.add_parser("quota", help="Check dataset quota")
    p_quota.add_argument("--project_id", type=int, required=True)

    p_detail = sub.add_parser("detail", help="Get dataset details")
    p_detail.add_argument("--id", type=int, required=True)

    p_versions = sub.add_parser("versions", help="List dataset versions")
    p_versions.add_argument("--id", type=int, required=True)

    p_new = sub.add_parser("new_version", help="Create new version")
    p_new.add_argument("--id", type=int, required=True)
    p_new.add_argument("--desc", type=str, required=True)

    p_perm = sub.add_parser("permission", help="Check permissions")
    p_perm.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if not AK:
        print("ERROR: ACCESS_KEY environment variable not set")
        sys.exit(1)

    if args.cmd == "quota":
        check_quota(args.project_id)
    elif args.cmd == "detail":
        get_detail(args.id)
    elif args.cmd == "versions":
        list_versions(args.id)
    elif args.cmd == "new_version":
        create_version(args.id, args.desc)
    elif args.cmd == "permission":
        check_permission(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
