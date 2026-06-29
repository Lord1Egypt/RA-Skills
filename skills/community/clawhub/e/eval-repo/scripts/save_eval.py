from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
from utils import json_fail, now_str, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--eval_file", required=True)
    parser.add_argument("--brief", default="")
    parser.add_argument("--keywords", default="")
    parser.add_argument("--score", default="")
    parser.add_argument("--source_url", default="")
    parser.add_argument("--scope", default="personal")
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()
    src = Path(args.eval_file)
    if not src.exists():
        out(json_fail("eval_file_not_found", f"找不到评估草稿：{src}"))
        return
    safe = sanitize_filename(args.title)
    path = f"summaries/projects/{safe}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb eval repo: {safe}")
        cat = catalog.read(args.owner, args.repo)
        entry = {
            "title": args.title,
            "file": path,
            "type_key": "project",
            "doc_type": "开源项目",
            "brief": args.brief,
            "keywords": [x.strip() for x in args.keywords.split(",") if x.strip()],
            "score": args.score,
            "scope": args.scope,
            "project_id": args.project_id,
            "source_type": "GitHub",
            "source_url": args.source_url,
            "created_at": now_str(),
            "updated_at": now_str(),
        }
        replaced = catalog.upsert_document(cat, entry)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_eval_failed", str(exc)))
        return
    out({"success": True, "replaced": replaced, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
