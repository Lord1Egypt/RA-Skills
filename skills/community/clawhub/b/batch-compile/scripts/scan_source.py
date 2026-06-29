from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import file_classifier as fc
import gitea_api as g
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def parse_repo(url: str) -> tuple[str, str] | None:
    value = (url or "").strip()
    if value.endswith(".git"):
        value = value[:-4]
    if value.startswith("git@") and ":" in value:
        path = value.split(":", 1)[1].strip("/")
    elif "://" in value:
        parsed = urlparse(value)
        path = parsed.path.strip("/")
    else:
        path = value.strip("/")
    parts = [p for p in path.split("/") if p]
    if len(parts) >= 2:
        return parts[0], parts[1].removesuffix(".git")
    m = re.fullmatch(r"([^/]+)/([^/]+)", value)
    return (m.group(1), m.group(2).removesuffix(".git")) if m else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_url", required=True)
    parser.add_argument("--source_type", default="gitea_repo")
    parser.add_argument("--ref", default="")
    parser.add_argument("--save_to", default="", help="optional path to write the JSON scan result")
    args = parser.parse_args()
    repo = parse_repo(args.source_url)
    if not repo:
        out(json_fail("bad_source_url", "无法识别 Gitea 仓库链接。"))
        return
    owner, name = repo
    try:
        ref = args.ref or g.default_branch(owner, name)
        latest_commit = g.branch_commit_sha(owner, name, ref)
        tree = g.list_tree(owner, name, ref, recursive=True)
    except Exception as exc:
        out(json_fail("cannot_read_source", f"无法读取资料源仓库，请确认 AIFusionBot 有 read 权限：{exc}"))
        return
    raw_files = []
    has_code = False
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        size = item.get("size") or 0
        cls = fc.classify(path, size)
        if cls["kind"] == "code":
            has_code = True
        raw_files.append((item, cls))

    files = []
    fingerprints = {}
    stats = {"markdown": 0, "text": 0, "pdf": 0, "docx": 0, "xlsx": 0, "code": 0, "dependency": 0, "skipped": 0, "total": 0}
    for item, cls in raw_files:
        path = item.get("path", "")
        sha = item.get("sha", "")
        size = item.get("size") or 0
        if not has_code and path.rsplit("/", 1)[-1].lower().startswith("readme"):
            cls = {"kind": "markdown", "action": "document", "reason": "README in document-only repository"}
        fingerprints[path] = sha
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
        files.append({"path": path, "sha": sha, "size": size, **cls})
    result = {
        "success": True,
        "source": {
            "type": args.source_type,
            "url": args.source_url,
            "owner": owner,
            "repo": name,
            "ref": ref,
            "latest_commit": latest_commit,
        },
        "stats": stats,
        "files": files,
        "current_fingerprints": fingerprints,
    }
    if args.save_to:
        target = Path(args.save_to)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["saved_to"] = str(target)
    out(result)


if __name__ == "__main__":
    main()
