#!/usr/bin/env python3
"""snapshot_book - 创建书籍状态快照。

默认支持 dry-run。验证所有目标路径都位于当前书根目录。
禁止覆盖已有快照。支持验证快照哈希。快照文件清单来自 file-contract.json（_contract）。
"""

import argparse
import json
import os
import shutil
import sys

import _contract
from _contract import file_sha256, now_iso, safe_join

SNAPSHOT_VERSION = "1.1.0"


def create_snapshot(book_dir: str, chapter: int, dry_run: bool = False,
                    force: bool = False) -> dict:
    """创建快照。"""
    snapshots_dir = os.path.join(book_dir, "story", "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)

    snap_name = f"{chapter:04d}"
    snap_dir = safe_join(snapshots_dir, snap_name)

    if os.path.exists(snap_dir) and not force:
        return {
            "ok": False,
            "error": f"快照 {snap_name} 已存在，使用 --force 覆盖（禁止静默覆盖）",
        }

    # 收集文件（清单来自 _contract.resolve_snapshot_files(book_dir)，
    # 支持 story/roles/** glob；非通配路径缺失时计入 missing）
    included_files = []
    file_hashes = {}
    missing = []
    for fpath in _contract.resolve_snapshot_files(book_dir):
        src = os.path.join(book_dir, fpath)
        if os.path.isfile(src):
            included_files.append(fpath)
            file_hashes[fpath] = file_sha256(src)
        else:
            missing.append(fpath)

    manifest = {
        "snapshotVersion": SNAPSHOT_VERSION,
        "chapter": chapter,
        "createdAt": now_iso(),
        "includedFiles": included_files,
        "fileHashes": file_hashes,
        "skillVersion": _contract.skill_version(),
        "schemaVersion": "1.0.0",
    }

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "snapshot_dir": snap_name,
            "included_files": included_files,
            "missing_files": missing,
        }

    # 创建快照目录，按书根相对路径保留结构（story/... 与 chapters/...）
    for fpath in included_files:
        src = os.path.join(book_dir, fpath)
        dst = safe_join(snap_dir, fpath)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    # 写 manifest
    with open(os.path.join(snap_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return {
        "ok": True,
        "snapshot_dir": snap_name,
        "included_files": included_files,
        "missing_files": missing,
    }


def verify_snapshot(book_dir: str, chapter: int) -> dict:
    """验证快照哈希（按 manifest 自身键校验，兼容新旧布局）。"""
    snap_name = f"{chapter:04d}"
    snap_dir = os.path.join(book_dir, "story", "snapshots", snap_name)
    manifest_path = os.path.join(snap_dir, "manifest.json")

    if not os.path.isfile(manifest_path):
        return {"ok": False, "error": f"快照 {snap_name} 缺少 manifest.json"}

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    mismatches = []
    missing = []
    for fpath, expected_hash in manifest.get("fileHashes", {}).items():
        full = os.path.join(snap_dir, fpath)
        if not os.path.isfile(full):
            missing.append(fpath)
        else:
            actual = file_sha256(full)
            if actual != expected_hash:
                mismatches.append({"file": fpath, "expected": expected_hash, "actual": actual})

    return {
        "ok": not mismatches and not missing,
        "snapshot_dir": snap_name,
        "mismatches": mismatches,
        "missing": missing,
    }


def main():
    parser = argparse.ArgumentParser(description="创建/验证书籍快照")
    parser.add_argument("book_dir", help="书籍根目录")
    parser.add_argument("--chapter", type=int, required=True, help="章节编号")
    parser.add_argument("--dry-run", action="store_true", help="默认支持 dry-run")
    parser.add_argument("--force", action="store_true", help="强制覆盖已有快照")
    parser.add_argument("--verify", action="store_true", help="验证快照哈希而非创建")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args()

    if args.verify:
        result = verify_snapshot(args.book_dir, args.chapter)
    else:
        result = create_snapshot(args.book_dir, args.chapter, dry_run=args.dry_run, force=args.force)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result["ok"]:
            print(f"[FAIL] 失败：{result.get('error', '未知错误')}", file=sys.stderr)
            sys.exit(1)
        if args.verify:
            print(f"[OK] 快照 {result['snapshot_dir']} 验证通过")
            for m in result.get("mismatches", []):
                print(f"  [哈希不匹配] {m['file']}")
            for m in result.get("missing", []):
                print(f"  [文件缺失] {m}")
        else:
            action = "（dry-run）" if result.get("dry_run") else ""
            print(f"[OK] 快照 {result['snapshot_dir']} 创建成功 {action}")
            print(f"  包含文件：{', '.join(result['included_files'])}")
            if result.get("missing_files"):
                print(f"  缺失文件：{', '.join(result['missing_files'])}")

    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
