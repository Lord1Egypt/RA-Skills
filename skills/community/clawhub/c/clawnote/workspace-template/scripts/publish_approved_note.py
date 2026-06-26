#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def toolkit_root() -> Path:
    value = os.getenv("XHS_TOOLKIT_ROOT", "").strip()
    if not value:
        raise SystemExit("Set XHS_TOOLKIT_ROOT before using publish_approved_note.py")
    return Path(value).expanduser()


def load_payload(path_arg):
    if path_arg:
        return json.loads(Path(path_arg).read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise SystemExit("Provide --input <json-file> or pipe JSON via stdin.")


def normalize_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.replace("，", ",").split(",") if part.strip()]
    return []


def build_command(root: Path, payload):
    tool = root / "xhs_toolkit.py"
    python_bin = root / ".venv313" / "bin" / "python"
    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    if not title or not body:
        raise SystemExit("Payload must include non-empty title and body.")
    cmd = [str(python_bin if python_bin.exists() else sys.executable), str(tool), "publish", title, body]
    tags = normalize_list(payload.get("tags", []))
    images = normalize_list(payload.get("images", []))
    if tags:
        cmd.extend(["--topics", ",".join(tag.lstrip("#") for tag in tags)])
    if images:
        cmd.extend(["--images", ",".join(images)])
    return cmd


def preview(payload):
    tags = normalize_list(payload.get("tags", []))
    images = normalize_list(payload.get("images", []))
    print("# Xiaohongshu Live Publish Preview\n")
    print(f"- Title: {payload.get('title', '').strip()}")
    print(f"- Images: {len(images)}")
    print(f"- Tags: {' '.join('#' + t.lstrip('#') for t in tags)}\n")
    print("## Body\n")
    print(payload.get("body", "").strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--allow-live", action="store_true")
    parser.add_argument("--confirm-title")
    args = parser.parse_args()

    payload = load_payload(args.input)
    title = str(payload.get("title", "")).strip()

    if not args.allow_live:
        preview(payload)
        print(f'\n[blocked] Re-run with --allow-live --confirm-title "{title}" after explicit approval.')
        return

    if args.confirm_title != title:
        raise SystemExit(f'Expected exact --confirm-title: {title}')

    root = toolkit_root()
    cmd = build_command(root, payload)
    env = os.environ.copy()
    env["XHS_CHROME_USER_DATA_DIR"] = tempfile.mkdtemp(prefix="xhs-publish-profile-")
    raise SystemExit(subprocess.run(cmd, cwd=root, env=env).returncode)


if __name__ == "__main__":
    main()
