#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--readme", required=True)
    ap.add_argument("--visibility", choices=["private", "public"], default="private")
    args = ap.parse_args()

    repo = f"{args.owner}/{args.name}"
    vis_flag = "--private" if args.visibility == "private" else "--public"

    with tempfile.TemporaryDirectory(prefix="awesome-research-") as td:
        tdp = Path(td)
        shutil.copyfile(args.readme, tdp / "README.md")
        run(["git", "init", "-b", "main"], cwd=td)
        run(["git", "config", "user.name", "OpenClaw Assistant"], cwd=td)
        run(["git", "config", "user.email", "assistant@local"], cwd=td)
        run(["git", "add", "README.md"], cwd=td)
        run(["git", "commit", "-m", "docs: initialize awesome papers README"], cwd=td)

        exists = subprocess.run(["gh", "repo", "view", repo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if not exists:
            run(["gh", "repo", "create", repo, vis_flag, "--source", td, "--remote", "origin", "--push"], cwd=td)
        else:
            remotes = subprocess.check_output(["git", "remote"], cwd=td).decode()
            if "origin" not in remotes:
                run(["git", "remote", "add", "origin", f"https://github.com/{repo}.git"], cwd=td)
            run(["git", "push", "-u", "origin", "main"], cwd=td)
            run(["gh", "repo", "edit", repo, vis_flag])

    print(f"Published: https://github.com/{repo}")


if __name__ == "__main__":
    main()
