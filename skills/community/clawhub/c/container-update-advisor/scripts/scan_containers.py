#!/usr/bin/env python3
"""
scan_containers.py — List running Docker containers with image info.
Outputs JSON array of container objects to stdout.
"""

import subprocess
import json
import sys
import re
from datetime import datetime


def check_docker():
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, None
    except FileNotFoundError:
        return False, "Docker is not installed or not in PATH."
    except subprocess.TimeoutExpired:
        return False, "Docker daemon timed out. Is Docker running?"


def parse_image_parts(image_str):
    """
    Parse image string into registry, namespace, repo, and tag.
    Examples:
      nginx:1.25.3          -> namespace=library, repo=nginx, tag=1.25.3
      myuser/myapp:latest   -> namespace=myuser, repo=myapp, tag=latest
      ghcr.io/org/app:sha   -> registry=ghcr.io, namespace=org, repo=app, tag=sha
    """
    registry = None
    tag = "latest"

    # Split off tag
    if ":" in image_str.split("/")[-1]:
        image_str, tag = image_str.rsplit(":", 1)

    parts = image_str.split("/")

    # Detect registry (contains a dot or colon, or is "localhost")
    if len(parts) >= 2 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
        registry = parts[0]
        parts = parts[1:]

    if len(parts) == 1:
        namespace = "library"
        repo = parts[0]
    elif len(parts) == 2:
        namespace = parts[0]
        repo = parts[1]
    else:
        # e.g. ghcr.io/org/sub/repo — join remainder
        namespace = parts[0]
        repo = "/".join(parts[1:])

    return {
        "registry": registry,
        "namespace": namespace,
        "repo": repo,
        "tag": tag,
    }


def get_containers():
    format_str = (
        '{"id":"{{.ID}}",'
        '"name":"{{.Names}}",'
        '"image":"{{.Image}}",'
        '"status":"{{.Status}}",'
        '"created":"{{.CreatedAt}}"}'
    )
    result = subprocess.run(
        ["docker", "ps", "--format", format_str],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        raise RuntimeError(f"docker ps failed: {result.stderr.strip()}")

    containers = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
        except json.JSONDecodeError:
            continue

        image_str = c.get("image", "")
        parsed = parse_image_parts(image_str)

        containers.append({
            "id": c.get("id", ""),
            "name": c.get("name", ""),
            "image_raw": image_str,
            "registry": parsed["registry"],
            "namespace": parsed["namespace"],
            "repo": parsed["repo"],
            "tag": parsed["tag"],
            "status": c.get("status", ""),
            "created": c.get("created", ""),
        })

    return containers


def main():
    ok, err = check_docker()
    if not ok:
        output = {"error": err, "containers": []}
        print(json.dumps(output, indent=2))
        sys.exit(1)

    try:
        containers = get_containers()
    except RuntimeError as e:
        output = {"error": str(e), "containers": []}
        print(json.dumps(output, indent=2))
        sys.exit(1)

    if not containers:
        output = {"error": None, "containers": [], "message": "No running containers found."}
    else:
        output = {"error": None, "containers": containers}

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
