#!/usr/bin/env python3
"""Manage federated Agent Asset indexes. English is normative; ZH-CN is paired. / 管理联邦 Agent Asset 索引；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import runtime_paths


REGISTRY_SCHEMA_VERSION = 1
DEFAULT_REGISTRY_PATH = runtime_paths.DEFAULT_PATHS.asset_registry
MANIFEST_RELATIVE_PATH = Path(".cleanup-extracted") / "asset-manifest.jsonl"
DOCUMENTS_FILENAME = "documents.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def workspace_id(workspace_root: Path) -> str:
    value = canonical(workspace_root).as_posix().encode("utf-8")
    return "asset-workspace-" + hashlib.sha256(value).hexdigest()[:16]


def manifest_path(workspace_root: Path) -> Path:
    return canonical(workspace_root) / MANIFEST_RELATIVE_PATH


def documents_path(index_path: Path) -> Path:
    candidate = canonical(index_path)
    return candidate / DOCUMENTS_FILENAME if candidate.is_dir() or candidate.suffix != ".jsonl" else candidate


def load_manifest_rows(workspace_root: Path) -> list[dict[str, Any]]:
    path = manifest_path(workspace_root)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def within_workspace(workspace_root: Path, raw_path: str) -> Path | None:
    root = canonical(workspace_root)
    candidate = Path(raw_path)
    path = canonical(candidate if candidate.is_absolute() else root / candidate)
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def ready_summary(workspace_root: Path) -> dict[str, Any]:
    rows = load_manifest_rows(workspace_root)
    candidate = [row for row in rows if str(row.get("index_status", "")).lower() == "candidate"]
    review = [row for row in rows if str(row.get("retention", "")).lower() == "review"]
    final_pii = [
        row
        for row in rows
        if str(row.get("index_status", "")).lower() == "final"
        and str(row.get("privacy", "")).lower() == "pii"
    ]
    missing_source: list[dict[str, Any]] = []
    missing_semantic: list[dict[str, Any]] = []
    for row in rows:
        retention = str(row.get("retention", "")).lower()
        if retention in {"delete", "delete_failed"}:
            continue
        if str(row.get("index_status", "")).lower() != "final":
            continue
        source_paths = [str(value) for value in row.get("source_paths", []) if value]
        if not source_paths or any(
            candidate_path is None or not candidate_path.exists()
            for candidate_path in (within_workspace(workspace_root, value) for value in source_paths)
        ):
            missing_source.append(row)
        semantic_formats = row.get("semantic_formats")
        semantic_paths = [str(value) for value in row.get("semantic_paths", []) if value]
        if semantic_formats != [] and (
            not semantic_paths
            or any(
                candidate_path is None or not candidate_path.exists()
                for candidate_path in (within_workspace(workspace_root, value) for value in semantic_paths)
            )
        ):
            missing_semantic.append(row)
    return {
        "assets": len(rows),
        "final": sum(str(row.get("index_status", "")).lower() == "final" for row in rows),
        "excluded": sum(str(row.get("index_status", "")).lower() == "excluded" for row in rows),
        "candidate": len(candidate),
        "review": len(review),
        "final_pii": len(final_pii),
        "missing_source": len(missing_source),
        "missing_semantic": len(missing_semantic),
        "ready_for_scope_index": not any((candidate, review, final_pii, missing_source, missing_semantic)),
    }


def load_registry(path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    path = canonical(path)
    if not path.exists():
        return {"schema_version": REGISTRY_SCHEMA_VERSION, "indexes": {}}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"schema_version": REGISTRY_SCHEMA_VERSION, "indexes": {}}
    if not isinstance(payload, dict) or not isinstance(payload.get("indexes"), dict):
        return {"schema_version": REGISTRY_SCHEMA_VERSION, "indexes": {}}
    payload["schema_version"] = REGISTRY_SCHEMA_VERSION
    return payload


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path = canonical(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def count_records(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def upsert_asset_index(
    workspace_root: Path,
    index_path: Path,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
) -> dict[str, Any]:
    workspace_root = canonical(workspace_root)
    index_file = documents_path(index_path)
    manifest = manifest_path(workspace_root)
    if not manifest.is_file():
        raise FileNotFoundError(f"Missing asset manifest / 缺少 asset manifest: {manifest}")
    if not index_file.is_file():
        raise FileNotFoundError(f"Missing asset index / 缺少 asset index: {index_file}")
    readiness = ready_summary(workspace_root)
    if not readiness["ready_for_scope_index"]:
        raise RuntimeError("Asset manifest is not index-ready / Asset manifest 尚未达到索引就绪状态: " + json.dumps(readiness, ensure_ascii=False))
    registry = load_registry(registry_path)
    identifier = workspace_id(workspace_root)
    entry = {
        "workspace_id": identifier,
        "workspace_label": workspace_root.name,
        "workspace_root": workspace_root.as_posix(),
        "manifest_path": manifest.as_posix(),
        "manifest_sha256": sha256_file(manifest),
        "index_path": index_file.as_posix(),
        "index_sha256": sha256_file(index_file),
        "record_count": count_records(index_file),
        "readiness": readiness,
        "registered_at": utc_now(),
    }
    indexes = registry.setdefault("indexes", {})
    indexes[identifier] = entry
    registry["updated_at"] = utc_now()
    atomic_json(registry_path, registry)
    return entry


def validate_entry(entry: dict[str, Any]) -> tuple[bool, str]:
    try:
        workspace_root = canonical(Path(str(entry["workspace_root"])))
        manifest = canonical(Path(str(entry["manifest_path"])))
        index_file = canonical(Path(str(entry["index_path"])))
    except (KeyError, TypeError, ValueError):
        return False, "invalid_entry"
    if not workspace_root.is_dir():
        return False, "workspace_missing"
    if not manifest.is_file():
        return False, "manifest_missing"
    if not index_file.is_file():
        return False, "index_missing"
    if entry.get("manifest_sha256") != sha256_file(manifest):
        return False, "manifest_changed"
    if entry.get("index_sha256") != sha256_file(index_file):
        return False, "index_changed"
    readiness = ready_summary(workspace_root)
    if not readiness["ready_for_scope_index"]:
        return False, "manifest_not_ready"
    if int(entry.get("record_count", -1)) != count_records(index_file):
        return False, "record_count_changed"
    return True, ""


def valid_asset_indexes(
    registry_path: Path = DEFAULT_REGISTRY_PATH,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    registry = load_registry(registry_path)
    valid: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for identifier, value in sorted(registry.get("indexes", {}).items()):
        if not isinstance(value, dict):
            skipped.append({"workspace_id": str(identifier), "reason": "invalid_entry"})
            continue
        accepted, reason = validate_entry(value)
        if accepted:
            valid.append(value)
        else:
            skipped.append({"workspace_id": str(value.get("workspace_id", identifier)), "reason": reason})
    return valid, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH, help="Registry path. / 注册表路径。")
    parser.add_argument("--upsert", action="store_true", help="Register or update one ready index. / 注册或更新一个已就绪索引。")
    parser.add_argument("--workspace", type=Path, help="Workspace root for --upsert. / `--upsert` 使用的 workspace 根目录。")
    parser.add_argument("--index", type=Path, help="Index path for --upsert. / `--upsert` 使用的索引路径。")
    parser.add_argument("--json", action="store_true", help="Print formatted JSON. / 打印格式化 JSON。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.upsert:
            if args.workspace is None or args.index is None:
                raise ValueError("--upsert requires --workspace and --index / `--upsert` 需要 `--workspace` 和 `--index`")
            payload: dict[str, Any] = {"entry": upsert_asset_index(args.workspace, args.index, args.registry)}
        else:
            valid, skipped = valid_asset_indexes(args.registry)
            payload = {"registry": canonical(args.registry).as_posix(), "valid": valid, "skipped": skipped}
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        payload = {"error": str(exc)}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(payload["error"])
        return 2
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
