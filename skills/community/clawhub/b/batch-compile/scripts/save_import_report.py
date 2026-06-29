from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
from utils import json_fail, sanitize_filename, today_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--report_file", required=True)
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_url", default="")
    parser.add_argument("--status", default="completed")
    args = parser.parse_args()
    src = Path(args.report_file)
    if not src.exists():
        out(json_fail("report_file_not_found", f"找不到导入报告：{src}"))
        return
    name = sanitize_filename(f"{today_str()} {args.title}")
    path = f"imports/{name}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb import report: {name}")
        cat = catalog.read(args.owner, args.repo)
        item = {"name": args.title, "file": path, "brief": args.status, "source_id": args.source_id, "source_url": args.source_url}
        imports = cat.setdefault("imports", [])
        imports.append(item)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_import_report_failed", str(exc)))
        return
    out({"success": True, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
