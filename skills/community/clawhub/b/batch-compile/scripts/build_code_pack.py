from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import file_classifier as fc
import gitea_api as g
from utils import json_fail, sanitize_filename


TEXT_EXT = {
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp", ".go", ".rs",
    ".sh", ".bat", ".ps1", ".md", ".txt", ".json", ".toml", ".yml", ".yaml",
    ".cfg", ".ini", ".dockerfile",
}


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


def decode_text(owner: str, repo: str, path: str, ref: str, cap: int) -> str:
    result = g.get_file_bytes(owner, repo, path, ref=ref)
    if not result:
        return ""
    raw, _ = result
    return raw.decode("utf-8", errors="ignore")[:cap]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_url", required=True)
    parser.add_argument("--ref", default="")
    parser.add_argument("--out_dir", default="/tmp/paperkb")
    parser.add_argument("--max_chars", type=int, default=120000)
    parser.add_argument("--per_file_chars", type=int, default=4000)
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
        out(json_fail("cannot_read_source", str(exc)))
        return

    blobs = [item for item in tree if item.get("type") == "blob"]
    code_paths = []
    dep_paths = []
    readme_paths = []
    for item in blobs:
        path = item.get("path", "")
        cls = fc.classify(path, item.get("size") or 0)
        if cls["action"] == "dependency_context":
            dep_paths.append(path)
        elif cls["action"] == "code_context":
            if Path(path).name.lower().startswith("readme"):
                readme_paths.append(path)
            else:
                code_paths.append(path)

    lines = [
        f"# 代码仓库资料包：{owner}/{name}",
        f"资料源：{args.source_url}",
        f"分支：{ref}",
        f"最新提交：{latest_commit}",
        "",
        "## 文件统计",
        f"- 代码文件：{len(code_paths)}",
        f"- README：{len(readme_paths)}",
        f"- 依赖/配置：{len(dep_paths)}",
        "",
        "## 目录树",
    ]
    for item in blobs[:300]:
        lines.append(f"- {item.get('path')} ({item.get('size') or 0} bytes)")

    def add_section(title: str, paths: list[str]) -> None:
        lines.extend(["", f"## {title}"])
        for path in paths:
            ext = Path(path).suffix.lower()
            if ext and ext not in TEXT_EXT and Path(path).name not in fc.DEP_NAMES:
                continue
            text = decode_text(owner, name, path, ref, args.per_file_chars)
            if not text.strip():
                continue
            lines.extend([f"\n### {path}", "```", text, "```"])

    add_section("README", readme_paths)
    add_section("依赖与配置", dep_paths)
    add_section("代表性代码文件", code_paths[:60])

    content = "\n".join(lines)
    truncated = len(content) > args.max_chars
    if truncated:
        content = content[:args.max_chars] + "\n\n（code_pack 已按最大字符数截断）\n"
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pack_path = out_dir / f"code_pack_{sanitize_filename(owner + '_' + name)}.md"
    pack_path.write_text(content, encoding="utf-8")
    out({
        "success": True,
        "code_pack_path": str(pack_path),
        "ref": ref,
        "latest_commit": latest_commit,
        "code_files": len(code_paths),
        "dependency_files": len(dep_paths),
        "readme_files": len(readme_paths),
        "truncated": truncated,
    })


if __name__ == "__main__":
    main()
