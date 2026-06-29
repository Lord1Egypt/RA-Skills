from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
import system_config as sc
from utils import json_fail, now_str, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary_file", required=True)
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_url", default="")
    parser.add_argument("--source_commit", default="")
    parser.add_argument("--project_id", default="")
    parser.add_argument("--brief", default="")
    parser.add_argument("--job_id", default="")
    args = parser.parse_args()
    src = Path(args.summary_file)
    if not src.exists():
        out(json_fail("summary_file_not_found", f"找不到代码总览草稿：{src}"))
        return
    safe = sanitize_filename(args.title)
    path = f"summaries/codebases/{safe}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb codebase: {safe}")
        cat = catalog.read(args.owner, args.repo)
        entry = {
            "title": args.title,
            "file": path,
            "type_key": "codebase",
            "doc_type": "代码仓库总览",
            "brief": args.brief,
            "project_id": args.project_id,
            "source_type": "gitea_repo",
            "source_id": args.source_id,
            "source_url": args.source_url,
            "source_commit": args.source_commit,
            "created_at": now_str(),
            "updated_at": now_str(),
        }
        replaced = catalog.upsert_document(cat, entry)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
        if args.job_id:
            def mutate_jobs(current: dict) -> dict:
                job = current.get(args.job_id)
                if not job:
                    return current
                job["codebase_result"] = {
                    "path": path,
                    "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}",
                    "source_commit": args.source_commit,
                    "updated_at": now_str(),
                }
                job["updated_at"] = now_str()
                current[args.job_id] = job
                return current

            sc.update_json("jobs.json", mutate_jobs, default={})
    except Exception as exc:
        out(json_fail("save_codebase_failed", str(exc)))
        return
    out({"success": True, "replaced": replaced, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
