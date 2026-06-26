"""
Search and browse Bohrium public images.

Usage:
    python search_images.py search deepmd
    python search_images.py search lammps --limit 10
    python search_images.py browse
    python search_images.py build --project_id 154 --name my-image --dockerfile Dockerfile
"""

import argparse
import json
import os
import sys

import requests

AK = os.environ.get("ACCESS_KEY", "")
BASE_V2 = "https://openapi.dp.tech/openapi/v2/image"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}


def search_versions(keyword: str, limit: int = 5):
    """Search public image versions by keyword."""
    r = requests.get(
        f"{BASE_V2}/public/version/search",
        headers=HEADERS,
        params={"keyword": keyword, "page": 1, "pageSize": limit},
    )
    data = r.json().get("data", {})
    items = data.get("items", [])

    if not items:
        print(f"No results for '{keyword}'")
        return

    print(f"Search results for '{keyword}' ({len(items)} found):\n")
    for item in items:
        name = item.get("imageName", "?")
        version = item.get("version", "?")
        url = item.get("url", "?")
        size = item.get("size", 0)
        size_mb = size / (1024 * 1024) if size else 0
        print(f"  {name}:{version}")
        print(f"    URL:  {url}")
        if size_mb > 0:
            print(f"    Size: {size_mb:.0f} MB")
        print()


def browse_public(limit: int = 10):
    """Browse public image categories."""
    r = requests.get(
        f"{BASE_V2}/public",
        headers=HEADERS,
        params={"page": 1, "pageSize": limit},
    )
    data = r.json().get("data", {})
    items = data.get("items", [])

    print(f"Public image categories ({len(items)}):\n")
    for item in items:
        name = item.get("name", "?")
        image_id = item.get("id", "?")
        desc = item.get("desc", "")[:60]
        print(f"  [{image_id}] {name}")
        if desc:
            print(f"       {desc}")


def build_image(project_id: int, name: str, dockerfile_path: str, desc: str = ""):
    """Build a custom image from a Dockerfile."""
    with open(dockerfile_path) as f:
        dockerfile_content = f.read()

    # Validate Dockerfile first
    check = requests.post(
        f"{BASE_V2}/dockerfile/check",
        headers=HEADERS_JSON,
        json={"dockerfile": dockerfile_content},
    )
    check_data = check.json()
    if check_data.get("code") != 0:
        print(f"Dockerfile validation failed: {check_data}")
        return

    print("Dockerfile validation passed.")

    # Build
    r = requests.post(
        f"{BASE_V2}/private",
        headers=HEADERS_JSON,
        json={
            "name": name,
            "projectId": project_id,
            "device": "container",
            "desc": desc or f"Custom image: {name}",
            "buildType": 1,
            "dockerfile": dockerfile_content,
        },
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"Image build started! Check status with: bohr image list")
        print(f"Response: {json.dumps(result.get('data', {}), indent=2)}")
    else:
        print(f"Build failed: {result}")


def main():
    parser = argparse.ArgumentParser(description="Bohrium image tools")
    sub = parser.add_subparsers(dest="cmd")

    p_search = sub.add_parser("search", help="Search public image versions")
    p_search.add_argument("keyword", type=str)
    p_search.add_argument("--limit", type=int, default=5)

    p_browse = sub.add_parser("browse", help="Browse public image categories")
    p_browse.add_argument("--limit", type=int, default=10)

    p_build = sub.add_parser("build", help="Build image from Dockerfile")
    p_build.add_argument("--project_id", type=int, required=True)
    p_build.add_argument("--name", type=str, required=True)
    p_build.add_argument("--dockerfile", type=str, required=True)
    p_build.add_argument("--desc", type=str, default="")

    args = parser.parse_args()

    if not AK:
        print("ERROR: ACCESS_KEY environment variable not set")
        sys.exit(1)

    if args.cmd == "search":
        search_versions(args.keyword, args.limit)
    elif args.cmd == "browse":
        browse_public(args.limit)
    elif args.cmd == "build":
        build_image(args.project_id, args.name, args.dockerfile, args.desc)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
