from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import gitea_api as g
from utils import json_fail, sanitize_filename


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
    parser.add_argument("--path", required=True)
    parser.add_argument("--ref", default="")
    parser.add_argument("--out_dir", default="/tmp/paperkb/source_files")
    args = parser.parse_args()

    repo = parse_repo(args.source_url)
    if not repo:
        out(json_fail("bad_source_url", "无法识别 Gitea 仓库链接。"))
        return
    owner, name = repo
    ref = args.ref or g.default_branch(owner, name)
    result = g.get_file_bytes(owner, name, args.path, ref=ref)
    if not result:
        out(json_fail("source_file_not_found", f"资料源文件不存在或不可读取：{args.path}"))
        return
    raw, sha = result
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(args.path).suffix
    stem = sanitize_filename(args.path.replace("/", "__"), max_len=140)
    local_path = out_dir / f"{stem}{suffix if suffix and not stem.endswith(suffix) else ''}"
    local_path.write_bytes(raw)
    out({
        "success": True,
        "source_owner": owner,
        "source_repo": name,
        "source_path": args.path,
        "ref": ref,
        "sha": sha,
        "local_path": str(local_path),
        "size": len(raw),
    })


if __name__ == "__main__":
    main()
