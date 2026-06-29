#!/usr/bin/env python3
"""Create and optionally push the GitHub repository for OpenClaw Commons.

The script uses GH_TOKEN or GITHUB_TOKEN from the environment. It never prints
the token.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


def run(argv: list[str]) -> int:
    completed = subprocess.run(argv, check=False)
    return completed.returncode


def request_json(url: str, token: str, payload: dict[str, object]) -> tuple[int, dict[str, object]]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "openclaw-commons-memory",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"message": body}
        return exc.code, parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the GitHub repo for OpenClaw Commons Memory")
    parser.add_argument("--owner", required=True, help="GitHub user or org")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--description", default="Privacy-safe shared knowledge cards for OpenClaw agents")
    parser.add_argument("--public", action="store_true", help="Create a public repository")
    parser.add_argument("--push", action="store_true", help="Add origin and push main")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GH_TOKEN or GITHUB_TOKEN is required. No token was printed or read from disk.", file=sys.stderr)
        return 2

    user_status, user = request_json("https://api.github.com/user/repos", token, {})
    if user_status == 401:
        print("GitHub token rejected.", file=sys.stderr)
        return 1

    payload = {
        "name": args.repo,
        "description": args.description,
        "private": not args.public,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": False,
    }
    status, response = request_json("https://api.github.com/user/repos", token, payload)
    if status not in (200, 201):
        message = response.get("message", "unknown error")
        if status == 422 and "already exists" in str(message).lower():
            print(f"Repository already exists: {args.owner}/{args.repo}")
        else:
            print(f"GitHub create failed ({status}): {message}", file=sys.stderr)
            return 1
    else:
        print(f"Created repository: {response.get('html_url')}")

    remote_url = f"https://github.com/{args.owner}/{args.repo}.git"
    if args.push:
        run(["git", "remote", "remove", "origin"])
        if run(["git", "remote", "add", "origin", remote_url]) != 0:
            return 1
        if run(["git", "push", "-u", "origin", "main"]) != 0:
            return 1
        print(f"Pushed main to {remote_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
