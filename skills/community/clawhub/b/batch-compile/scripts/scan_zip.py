from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import file_classifier as fc
from utils import json_fail, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def file_digest(path: Path) -> str:
    digest = hashlib.sha1()
    digest.update(str(path.resolve()).encode("utf-8"))
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def safe_members(zf: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = []
    for info in zf.infolist():
        name = info.filename.replace("\\", "/")
        if not name or name.endswith("/"):
            continue
        parts = [p for p in name.split("/") if p]
        if not parts or any(part in {"..", "."} for part in parts):
            continue
        if Path(name).is_absolute():
            continue
        members.append(info)
    return members


def classify_files(raw_items: list[tuple[zipfile.ZipInfo, str]]) -> list[tuple[zipfile.ZipInfo, dict]]:
    classified = []
    has_code = False
    for info, rel in raw_items:
        cls = fc.classify(rel, info.file_size)
        if cls["kind"] == "code":
            has_code = True
        classified.append((info, cls))
    normalized = []
    for info, cls in classified:
        rel = info.filename.replace("\\", "/")
        if not has_code and rel.rsplit("/", 1)[-1].lower().startswith("readme"):
            cls = {"kind": "markdown", "action": "document", "reason": "README in document-only archive"}
        normalized.append((info, cls))
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip_file", required=True)
    parser.add_argument("--source_label", default="")
    parser.add_argument("--extract_dir", default="/tmp/paperkb/manual_zip")
    parser.add_argument("--save_to", default="", help="optional path to write the JSON scan result")
    parser.add_argument("--max_files", type=int, default=1000)
    parser.add_argument("--max_file_mb", type=int, default=80)
    parser.add_argument("--max_total_mb", type=int, default=500)
    parser.add_argument("--max_compression_ratio", type=float, default=100.0)
    args = parser.parse_args()

    zip_path = Path(args.zip_file)
    if not zip_path.exists():
        out(json_fail("zip_file_not_found", f"找不到上传的 zip 文件：{zip_path}"))
        return
    if not zipfile.is_zipfile(zip_path):
        out(json_fail("bad_zip_file", "该文件不是有效 zip。"))
        return

    digest = file_digest(zip_path)
    label = args.source_label or zip_path.stem
    target_dir = Path(args.extract_dir) / f"{sanitize_filename(label)}_{digest}"
    target_dir.mkdir(parents=True, exist_ok=True)

    files = []
    fingerprints = {}
    stats = {"markdown": 0, "text": 0, "pdf": 0, "docx": 0, "xlsx": 0, "xls": 0, "code": 0, "dependency": 0, "skipped": 0, "total": 0}
    try:
        with zipfile.ZipFile(zip_path) as zf:
            members = safe_members(zf)
            if len(members) > args.max_files:
                out(json_fail("zip_too_many_files", f"zip 文件数 {len(members)} 超过上限 {args.max_files}。"))
                return
            max_file_bytes = args.max_file_mb * 1024 * 1024
            max_total_bytes = args.max_total_mb * 1024 * 1024
            total_size = sum(info.file_size for info in members)
            if total_size > max_total_bytes:
                out(json_fail("zip_too_large", f"zip 解压后总大小超过 {args.max_total_mb} MB。"))
                return
            too_large = [info.filename for info in members if info.file_size > max_file_bytes]
            if too_large:
                out(json_fail("zip_file_too_large", f"zip 中存在超过 {args.max_file_mb} MB 的文件。"))
                return
            suspicious = [
                info.filename for info in members
                if info.compress_size > 0 and (info.file_size / info.compress_size) > args.max_compression_ratio
            ]
            if suspicious:
                out(json_fail("zip_suspicious_compression_ratio", "zip 中存在压缩比异常的文件，已拒绝处理。"))
                return
            raw_items = [(info, info.filename.replace("\\", "/")) for info in members]
            for info, cls in classify_files(raw_items):
                rel = info.filename.replace("\\", "/")
                raw = zf.read(info)
                local_path = target_dir / rel
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_bytes(raw)
                sha = hashlib.sha1(raw).hexdigest()
                fingerprints[rel] = sha
                stats["total"] += 1
                kind = cls["kind"]
                if cls["action"] == "skip":
                    stats["skipped"] += 1
                elif kind == "code":
                    stats["code"] += 1
                elif kind == "dependency":
                    stats["dependency"] += 1
                elif kind in stats:
                    stats[kind] += 1
                files.append({
                    "path": rel,
                    "sha": sha,
                    "size": info.file_size,
                    "local_path": str(local_path),
                    **cls,
                })
    except Exception as exc:
        out(json_fail("scan_zip_failed", str(exc)))
        return

    result = {
        "success": True,
        "source": {
            "type": "manual_zip",
            "label": label,
            "url": str(zip_path.resolve()),
            "owner": "",
            "repo": label,
            "ref": "",
            "latest_commit": digest,
            "extract_dir": str(target_dir),
        },
        "stats": stats,
        "files": files,
        "current_fingerprints": fingerprints,
    }
    if args.save_to:
        save_path = Path(args.save_to)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["saved_to"] = str(save_path)
    out(result)


if __name__ == "__main__":
    main()
