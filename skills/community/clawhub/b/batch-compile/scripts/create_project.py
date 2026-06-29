from __future__ import annotations

import argparse
import hashlib
import json
import re

import catalog
import gitea_api as g
import kb_schema as schema
import system_config as sc
from utils import json_fail, now_str, slugify


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def make_project_id(name: str, requested: str = "") -> str:
    raw = requested or name
    slug = slugify(raw, "project").lower()
    ascii_slug = re.sub(r"[^0-9a-zA-Z-]+", "", slug).strip("-").lower()
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    if len(ascii_slug) >= 3:
        return ascii_slug[:48]
    if ascii_slug:
        return f"{ascii_slug}-{digest}"
    return f"project-{digest}"


def ensure_project_files(owner: str, repo: str, project_id: str, name: str, brief: str) -> None:
    for filename, content in schema.PROJECT_FILES.items():
        if filename == "index.md":
            content = f"# {name}\n\n{brief}\n"
        g.ensure_file(owner, repo, f"projects/{project_id}/{filename}", content, f"init project {project_id} {filename}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--project_name", required=True)
    parser.add_argument("--brief", default="")
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()

    sc.ensure_system_repo()
    users = sc.users()
    user = users.get(args.open_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return
    team_id = user.get("team_id", "")
    if not team_id:
        out(json_fail("not_in_team", "当前用户还没有加入团队，不能创建团队项目。"))
        return
    teams = sc.teams()
    team = teams.get(team_id)
    if not team:
        out(json_fail("team_not_found", "system-config 中找不到该团队。"))
        return
    if args.open_id not in team.get("admins", []):
        out(json_fail("permission_denied", "只有团队管理员可以创建新项目。"))
        return

    project_id = make_project_id(args.project_name, args.project_id)
    projects = team.setdefault("projects", {})
    if project_id in projects:
        out(json_fail("project_exists", f"项目 {project_id} 已存在。"))
        return

    owner = team["team_kb_owner"]
    repo = team["team_kb_repo"]
    try:
        ensure_project_files(owner, repo, project_id, args.project_name, args.brief)
        cat = catalog.read(owner, repo)
        project_entry = {
            "project_id": project_id,
            "name": args.project_name,
            "folder": f"projects/{project_id}",
            "brief": args.brief,
            "documents": [],
            "people": [],
            "created_at": now_str(),
            "updated_at": now_str(),
        }
        projects_in_catalog = cat.setdefault("projects", [])
        for idx, existing in enumerate(projects_in_catalog):
            if existing.get("project_id") == project_id:
                projects_in_catalog[idx] = {**existing, **project_entry}
                break
        else:
            projects_in_catalog.append(project_entry)
        catalog.write(owner, repo, cat)
        catalog.regen_index(owner, repo, repo, cat)

        def mutate_teams(current: dict) -> dict:
            current_team = current.get(team_id, team)
            current_projects = current_team.setdefault("projects", {})
            current_projects[project_id] = {
                "name": args.project_name,
                "description": args.brief,
                "created_by": args.open_id,
                "created_at": now_str(),
            }
            current[team_id] = current_team
            return current

        sc.update_json("teams.json", mutate_teams, default={})
    except Exception as exc:
        out(json_fail("create_project_failed", str(exc)))
        return

    out({
        "success": True,
        "project_id": project_id,
        "project_name": args.project_name,
        "project_url": f"{g.GITEA_URL}/{owner}/{repo}/src/branch/main/projects/{project_id}/index.md",
    })


if __name__ == "__main__":
    main()
