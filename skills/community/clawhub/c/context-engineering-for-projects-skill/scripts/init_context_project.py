#!/usr/bin/env python3
"""Initialize a team-style project context directory.

Usage:
  python scripts/init_context_project.py \
    --project chrome_extension_timestamp \
    --code-dir /Users/laojiaqi/personal_projects/chrome_extension_timestamp \
    --target-root /Users/laojiaqi/context_engineering/team
"""

import argparse
from pathlib import Path
from datetime import datetime


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str):
    if path.exists():
        return False
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    return True


def append_project_index(projects_index: Path, project_name: str):
    ensure_parent(projects_index)
    if not projects_index.exists():
        projects_index.write_text(
            "# Projects\n\n- All project contexts live under this folder.\n\n## Index\n",
            encoding="utf-8",
        )
    text = projects_index.read_text(encoding="utf-8")
    entry = f"- {project_name} → projects/{project_name}/readme.md"
    if entry in text:
        return False
    new_text = text.rstrip() + "\n" + entry + "\n"
    projects_index.write_text(new_text, encoding="utf-8")
    return True


TEMPLATE_README = """# {project}

- Code directory: {code_dir}
- Context root: {project_root}

## Scope
- Describe what this project is about.
- Record any constraints or boundaries.
"""

TEMPLATE_GOALS = """# Goals

- [ ] Define current goals and priorities.
"""

TEMPLATE_SKILL = """# Project Skill Notes

- If this project needs a dedicated skill, document triggers and workflows here.
"""

TEMPLATE_STATUS = """# Project Status

- Status: not started
- Last updated: {date}
"""

TEMPLATE_DECISIONS = """# Decisions

- {date}: Initialize project context.
"""

TEMPLATE_AGENTS = """# Agents

- Agent notes for this project live here.
"""

TEMPLATE_MODULES_README = """# Modules

- Place analysis outputs here.
- Suggested structure depends on tech stack.
- Common buckets: modules/backend/, modules/frontend/, modules/qa/, modules/reviewer/
- Each module folder can contain multiple detailed documents.
"""


def infer_modules(code_dir: Path):
    candidates = set()
    lower_names = {p.name.lower() for p in code_dir.iterdir() if p.is_dir()}

    # Heuristics by common folder names
    if {"frontend", "web", "client", "app", "ui"} & lower_names:
        candidates.add("frontend")
    if {"backend", "server", "api", "services"} & lower_names:
        candidates.add("backend")
    if {"test", "tests", "qa"} & lower_names:
        candidates.add("qa")
    if {"mobile", "ios", "android"} & lower_names:
        candidates.add("mobile")
    if {"data", "analytics", "ml", "model"} & lower_names:
        candidates.add("data")
    if {"ops", "infra", "devops", "deploy", "helm", "k8s"} & lower_names:
        candidates.add("ops")

    # Heuristics by key files
    files = {p.name for p in code_dir.iterdir() if p.is_file()}
    if "package.json" in files:
        candidates.add("frontend")
    if "pom.xml" in files or "build.gradle" in files or "build.gradle.kts" in files:
        candidates.add("backend")
    if "go.mod" in files or "requirements.txt" in files or "pyproject.toml" in files:
        candidates.add("backend")
    if "Dockerfile" in files or "docker-compose.yml" in files:
        candidates.add("ops")

    if not candidates:
        candidates.update({"backend", "frontend", "qa", "reviewer"})

    # Always include reviewer bucket
    candidates.add("reviewer")
    return sorted(candidates)


def main():
    parser = argparse.ArgumentParser(description="Initialize a team-style project context directory.")
    parser.add_argument("--project", required=True, help="Project name (folder name).")
    parser.add_argument("--code-dir", required=True, help="Absolute path to the code directory.")
    parser.add_argument(
        "--target-root",
        default=str(Path.home() / "clawDir" / "team"),
        help="Target root for team context (default: ~/clawDir/team).",
    )
    args = parser.parse_args()

    target_root = Path(args.target_root).expanduser().resolve()
    code_dir = Path(args.code_dir).expanduser().resolve()
    project_root = target_root / "projects" / args.project
    date = datetime.now().strftime("%Y-%m-%d")

    created = []
    created.append(write_if_missing(target_root / "readme.md", "# Team Directory Guide\n\n- Keep navigation here.\n"))
    append_project_index(target_root / "projects" / "projects.md", args.project)

    write_if_missing(project_root / "readme.md", TEMPLATE_README.format(project=args.project, code_dir=code_dir, project_root=project_root))
    write_if_missing(project_root / "goals.md", TEMPLATE_GOALS)
    write_if_missing(project_root / "skill.md", TEMPLATE_SKILL)
    write_if_missing(project_root / "project_status.md", TEMPLATE_STATUS.format(date=date))
    write_if_missing(project_root / "decisions.md", TEMPLATE_DECISIONS.format(date=date))
    write_if_missing(project_root / "agents" / "agents.md", TEMPLATE_AGENTS)
    write_if_missing(project_root / "modules" / "README.md", TEMPLATE_MODULES_README)
    write_if_missing(project_root / "references" / "entrypoints.md", "# Entrypoints\n\n- TODO: record key entrypoints and indices.\n")

    modules = infer_modules(code_dir)
    for module in modules:
        write_if_missing(project_root / "modules" / module / "README.md", f"# {module}\n")
        write_if_missing(project_root / "modules" / module / f"{module}.md", f"# {module} Module\n\n## Scope\n- TODO: define boundaries and ownership.\n\n## Key Responsibilities\n- TODO: list core responsibilities.\n\n## Important Notes\n- TODO: add critical constraints, gotchas, or decisions.\n\n## Interfaces & Dependencies\n- TODO: list internal/external dependencies and key interfaces.\n")

    # Create agent folders based on inferred modules + reviewer
    agent_names = sorted(set(modules + ["reviewer"]))
    for agent in agent_names:
        agent_dir = project_root / "agents" / agent
        write_if_missing(
            agent_dir / "README.md",
            f"# {agent.title()} — {agent.title()} Agent\n\n## Role\n- TODO: define role and scope.\n\n## Principles\n- TODO: list guiding principles.\n\n## Responsibilities\n- TODO: list responsibilities.\n\n## Deliverables\n- TODO: list expected outputs.\n\n## Working Style\n- TODO: describe working preferences.\n\n## Notes\n- TODO: add project-specific context.\n",
        )
        write_if_missing(agent_dir / "tools.md", "# Tools\n\n- TODO: tool usage notes.\n")
        write_if_missing(agent_dir / "memory.md", "# Memory\n\n- TODO: long-term notes.\n")
        write_if_missing(agent_dir / "decisions.jsonl", "")
        write_if_missing(agent_dir / "fails.jsonl", "")

    print(f"Initialized context for {args.project} at {project_root}")


if __name__ == "__main__":
    main()
