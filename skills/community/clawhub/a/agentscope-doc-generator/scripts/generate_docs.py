#!/usr/bin/env python3
"""Generate documentation snippets from AgentScope project files."""

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def agent_summary(agent_config: dict) -> str:
    name = agent_config.get("name", "Unnamed Agent")
    model = agent_config.get("model_config", {}).get("model", "unknown")
    return f"- **{name}**: model=`{model}`"


def pipeline_summary(project_dir: Path) -> str:
    candidates = [
        project_dir / "run.py",
        project_dir / "pipeline.json",
        project_dir / "agent.json",
    ]
    found = [p for p in candidates if p.exists()]
    if not found:
        return "_No recognizable pipeline entrypoint found._"
    return "\n".join(f"- `{p.name}`" for p in found)


def generate_readme(project_dir: Path) -> str:
    agent_config = read_json(project_dir / "agent.json") or {}
    lines = [
        "# AgentScope Project Documentation",
        "",
        "## Agents",
        "",
    ]
    if agent_config:
        lines.append(agent_summary(agent_config))
    else:
        lines.append("_No agent configuration found._")
    lines.extend([
        "",
        "## Pipeline",
        "",
        pipeline_summary(project_dir),
        "",
        "## Notes",
        "",
        "- Review model names and API keys before sharing.",
        "- Update examples to match your runtime.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AgentScope docs")
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    readme = generate_readme(args.project)
    args.output.write_text(readme, encoding="utf-8")
    print(f"Generated docs: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
