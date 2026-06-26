from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

TRACKED_FILES = [
    "SKILL.md",
    "canon.md",
    "persona.md",
    "style_examples.md",
    "meta.json",
]
DEFAULT_INSTALL_ROOT = Path(".agents") / "skills"
DEFAULT_ARCHIVE_ROOT = Path("characters")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def snapshot_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_scope(value: str) -> str:
    allowed = {"codex", "archive", "both"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(f"Unsupported scope: {value}")
    return value


def resolve_root(base_root: Path, value: str | None, fallback: Path) -> Path:
    if not value:
        return base_root / fallback
    path = Path(value)
    return path if path.is_absolute() else base_root / path


def copy_sources(source_dir: Path, target_dir: Path) -> None:
    if source_dir.exists():
        shutil.copytree(source_dir, target_dir / "sources", dirs_exist_ok=True)


def load_manifest(path: Path) -> list[dict]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def write_manifest(path: Path, payload: list[dict]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def take_snapshot(skill_dir: Path) -> dict:
    versions_dir = skill_dir / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)
    sid = snapshot_id()
    target = versions_dir / sid
    target.mkdir(parents=True, exist_ok=False)
    for filename in TRACKED_FILES:
        src = skill_dir / filename
        if src.exists():
            shutil.copy2(src, target / filename)
    copy_sources(skill_dir / "sources", target)
    manifest_path = versions_dir / "index.json"
    manifest = load_manifest(manifest_path)
    entry = {"snapshot_id": sid, "created_at": utc_now()}
    manifest.append(entry)
    write_manifest(manifest_path, manifest)
    return entry


def rollback(skill_dir: Path, sid: str) -> dict:
    source = skill_dir / "versions" / sid
    if not source.exists():
        raise FileNotFoundError(f"Snapshot not found: {sid}")
    for filename in TRACKED_FILES:
        src = source / filename
        if src.exists():
            shutil.copy2(src, skill_dir / filename)
    sources_dir = source / "sources"
    if sources_dir.exists():
        shutil.copytree(sources_dir, skill_dir / "sources", dirs_exist_ok=True)
    return {"snapshot_id": sid, "rolled_back_at": utc_now()}


def action_for_dir(skill_dir: Path, action: str, snapshot_value: str | None) -> dict:
    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill package not found: {skill_dir}")
    if action == "snapshot":
        return take_snapshot(skill_dir)
    if not snapshot_value:
        raise SystemExit("--snapshot-id is required for rollback")
    return rollback(skill_dir, snapshot_value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and restore skill package snapshots.")
    parser.add_argument("--action", required=True, choices=["snapshot", "rollback"], help="Operation to run.")
    parser.add_argument("--slug", required=True, help="Character slug.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--output-root", help="Override the package root.")
    parser.add_argument(
        "--scope",
        default="codex",
        type=parse_scope,
        help="Which package root to manage: codex, archive, or both. Default is codex.",
    )
    parser.add_argument("--snapshot-id", help="Snapshot id for rollback.")
    args = parser.parse_args()

    root = Path(args.root)
    results: dict[str, dict] = {}

    if args.scope in {"codex", "both"}:
        codex_root = resolve_root(root, args.output_root, DEFAULT_INSTALL_ROOT)
        results["codex"] = action_for_dir(codex_root / args.slug, args.action, args.snapshot_id)

    if args.scope in {"archive", "both"}:
        archive_root = resolve_root(root, args.output_root if args.scope == "archive" else None, DEFAULT_ARCHIVE_ROOT)
        results["archive"] = action_for_dir(archive_root / args.slug, args.action, args.snapshot_id)

    print(json.dumps(results if args.scope == "both" else next(iter(results.values())), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
