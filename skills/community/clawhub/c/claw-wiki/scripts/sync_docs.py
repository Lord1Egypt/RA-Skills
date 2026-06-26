from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from common import dump_json, docs_root, root_docs_json, skill_root, state_root


UPSTREAM_REPO_URL = "https://github.com/openclaw/openclaw"
UPSTREAM_REPO_ALIASES = {
    UPSTREAM_REPO_URL,
    "https://github.com/openclaw/openclaw.git",
    "git@github.com:openclaw/openclaw.git",
}
ALLOWED_SUBDIR = "docs"
REF_RE = re.compile(r"^(main|[0-9a-fA-F]{7,40}|[A-Za-z0-9._/-]{1,128})$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync OpenClaw docs into the local skill snapshot.")
    parser.add_argument("--source-path", help="Path to a local OpenClaw checkout.")
    parser.add_argument(
        "--repo-url",
        help=f"Git repo URL for OpenClaw. Only {UPSTREAM_REPO_URL} is allowed.",
    )
    parser.add_argument("--ref", default="main", help="Git ref to sync when using --repo-url.")
    parser.add_argument(
        "--subdir",
        default=ALLOWED_SUBDIR,
        help=f"Docs directory inside the upstream repo. Only {ALLOWED_SUBDIR!r} is allowed.",
    )
    parser.add_argument("--mode", choices=["pinned", "tracking"], default="pinned")
    parser.add_argument("--keep-assets", action="store_true", help="Keep non-markdown assets instead of text-first sync.")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.source_path and args.repo_url:
        raise ValueError("Use either --source-path or --repo-url, not both.")
    if args.subdir != ALLOWED_SUBDIR:
        raise ValueError(f"Unsupported docs subdir: {args.subdir!r}. Only {ALLOWED_SUBDIR!r} is allowed.")
    if not REF_RE.match(args.ref):
        raise ValueError(f"Unsupported ref format: {args.ref!r}.")
    if args.repo_url and args.repo_url not in UPSTREAM_REPO_ALIASES:
        raise ValueError(
            f"Unsupported repo URL: {args.repo_url!r}. Only the OpenClaw upstream repository is allowed."
        )


def run_git_clone(repo_url: str, ref: str, destination: Path) -> Path:
    cmd = ["git", "clone", "--depth", "1", "--branch", ref, repo_url, str(destination)]
    subprocess.run(cmd, check=True)
    return destination


def copy_docs(source_docs: Path, destination: Path, keep_assets: bool) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    for item in source_docs.iterdir():
        if item.name == "docs.json":
            continue
        target = destination / item.name
        if item.is_dir():
            if keep_assets:
                shutil.copytree(item, target)
                continue
            markdown_like = [
                path for path in item.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".mdx", ".json"}
            ]
            if not markdown_like:
                continue
            for path in markdown_like:
                rel = path.relative_to(item)
                out = target / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, out)
            continue
        if keep_assets or item.suffix.lower() in {".md", ".mdx", ".json"}:
            shutil.copy2(item, target)


def detect_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def ensure_within_skill_root(path: Path) -> Path:
    resolved = path.resolve()
    root = skill_root().resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"Refusing to write outside skill root: {resolved}")
    return resolved


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not args.source_path and not args.repo_url:
        print("ERROR: Provide --source-path or --repo-url.")
        return 1

    root = skill_root()
    state = state_root()
    state.mkdir(parents=True, exist_ok=True)
    current_manifest = state / "docs-manifest.json"
    previous_manifest = state / "docs-manifest.previous.json"
    if current_manifest.exists():
        shutil.copy2(current_manifest, previous_manifest)

    with tempfile.TemporaryDirectory(prefix="openclaw-sync-") as tmp:
        tmp_path = Path(tmp)
        if args.source_path:
            repo_root = Path(args.source_path).resolve()
            source_type = "local_repo"
        else:
            repo_root = run_git_clone(args.repo_url or UPSTREAM_REPO_URL, args.ref, tmp_path / "repo")
            source_type = "git_clone"

        source_docs = repo_root / args.subdir
        source_docs_json = source_docs / "docs.json"
        if not source_docs.exists():
            print(f"ERROR: Docs directory not found: {source_docs}")
            return 1
        if not source_docs_json.exists():
            print(f"ERROR: docs.json not found: {source_docs_json}")
            return 1

        staged_docs = tmp_path / "staged_docs"
        copy_docs(source_docs, staged_docs, keep_assets=args.keep_assets)

        live_docs = ensure_within_skill_root(docs_root())
        backup_docs = ensure_within_skill_root(root / "openclaw_docs.previous")
        live_docs_json = ensure_within_skill_root(root_docs_json())
        if backup_docs.exists():
            shutil.rmtree(backup_docs)
        if live_docs.exists():
            shutil.move(str(live_docs), str(backup_docs))
        shutil.move(str(staged_docs), str(live_docs))
        shutil.copy2(source_docs_json, live_docs_json)

        source_lock = {
            "repo_url": args.repo_url or UPSTREAM_REPO_URL,
            "source_type": source_type,
            "source_path": str(Path(args.source_path).resolve()) if args.source_path else None,
            "tracked_ref": args.ref,
            "resolved_commit": detect_commit(repo_root),
            "docs_subdir": args.subdir,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "mode": args.mode,
            "keep_assets": bool(args.keep_assets),
            "previous_manifest_present": previous_manifest.exists(),
        }
        dump_json(state / "source-lock.json", source_lock)
    print("Docs sync completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
