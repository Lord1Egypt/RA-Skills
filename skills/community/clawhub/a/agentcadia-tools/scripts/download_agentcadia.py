#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

WORKSPACE_SIGNALS = {"AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download an Agentcadia agent package into a local OpenClaw-style workspace"
    )
    parser.add_argument("--agent-id", required=True, help="Agentcadia agent id")
    parser.add_argument("--token", required=True, help="Agentcadia download bearer token")
    parser.add_argument("--origin", required=True, help="Agentcadia origin, for example https://agentcadia.ai")
    parser.add_argument("--workspace", default="", help="Explicit workspace path")
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="Allow overwriting existing files in the target workspace",
    )
    return parser.parse_args()


def is_workspace(path: Path) -> bool:
    if not path.is_dir():
      return False
    entries = {p.name for p in path.iterdir()}
    return bool(entries.intersection(WORKSPACE_SIGNALS)) or (path / "skills").is_dir() or (path / "memory").is_dir()


def resolve_workspace(explicit: str) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path

    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if is_workspace(candidate):
            return candidate

    fallback = Path.home() / ".openclaw" / "workspace"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def parse_filename_from_headers(headers) -> str:
    disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename\*=UTF-8\'\'([^;]+)', disposition)
    if match:
        return urllib.parse.unquote(match.group(1))
    match = re.search(r'filename="?([^";]+)"?', disposition)
    if match:
        return match.group(1)
    content_type = headers.get_content_type()
    return "agentcadia-download.zip" if "zip" in content_type else "agent_download.md"


def safe_extract(zip_path: Path, target_dir: Path, allow_overwrite: bool):
    extracted = []
    conflicts = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                continue
            dest = target_dir / member_path
            if member.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and not allow_overwrite:
                conflicts.append(str(dest))
                continue
            with zf.open(member, "r") as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted.append(str(dest))
    return extracted, conflicts


def main():
    args = parse_args()
    origin = args.origin.rstrip("/")
    workspace = resolve_workspace(args.workspace)
    download_url = f"{origin}/api/agents/{args.agent_id}/download"
    req = urllib.request.Request(
        download_url,
        method="POST",
        headers={"Authorization": f"Bearer {args.token}"},
    )

    with urllib.request.urlopen(req) as response:
        filename = parse_filename_from_headers(response.headers)
        content_type = response.headers.get_content_type()
        data = response.read()

    with tempfile.TemporaryDirectory(prefix="agentcadia-download-") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        downloaded_path = temp_dir / filename
        downloaded_path.write_bytes(data)

        placed_files = []
        conflicts = []
        download_kind = "zip" if zipfile.is_zipfile(downloaded_path) or "zip" in content_type else "markdown"

        if download_kind == "zip":
            placed_files, conflicts = safe_extract(downloaded_path, workspace, args.allow_overwrite)
        else:
            destination = workspace / filename
            if destination.exists() and not args.allow_overwrite:
                conflicts.append(str(destination))
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(downloaded_path, destination)
                placed_files.append(str(destination))

    result = {
        "success": True,
        "mode": "download",
        "agentId": args.agent_id,
        "origin": origin,
        "workspace": str(workspace),
        "downloadUrl": download_url,
        "downloadKind": download_kind,
        "placedFiles": placed_files,
        "conflicts": conflicts,
        "allowOverwrite": args.allow_overwrite,
    }
    print(__import__("json").dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        print(__import__("json").dumps({"success": False, "error": f"HTTP {exc.code}", "body": body}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as exc:
        print(__import__("json").dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)
