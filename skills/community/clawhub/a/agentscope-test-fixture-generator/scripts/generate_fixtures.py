#!/usr/bin/env python3
"""Generate AgentScope test fixtures for common pipeline patterns."""

import argparse
import json
import os
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def agent_config_fixture(name: str, model: str = "gpt-4o") -> dict:
    return {
        "name": name,
        "type": "TextAgent",
        "model_config": {
            "model": model,
            "api_key": os.environ.get("OPENAI_API_KEY", "test-api-key"),
        },
        "sys_prompt": f"You are {name}, a helpful assistant for testing.",
    }


def sequential_fixtures(output_dir: Path) -> None:
    agents = [agent_config_fixture(f"agent_{i}") for i in range(1, 4)]
    pipeline = {
        "pipeline": "sequential",
        "agents": agents,
        "max_rounds": 10,
    }
    write(output_dir / "sequential" / "pipeline.json", json.dumps(pipeline, indent=2, ensure_ascii=False))
    write(output_dir / "sequential" / "test_sequential.py", '"""Sequential pipeline smoke test."""\nimport json\nfrom pathlib import Path\n\n\ndef test_pipeline_schema():\n    data = json.loads(Path(__file__).with_name("pipeline.json").read_text())\n    assert data["pipeline"] == "sequential"\n    assert len(data["agents"]) >= 1\n')


def parallel_fixtures(output_dir: Path) -> None:
    agents = [agent_config_fixture(f"parallel_agent_{i}") for i in range(1, 4)]
    pipeline = {
        "pipeline": "parallel",
        "agents": agents,
        "join": "concat",
    }
    write(output_dir / "parallel" / "pipeline.json", json.dumps(pipeline, indent=2, ensure_ascii=False))
    write(output_dir / "parallel" / "test_parallel.py", '"""Parallel pipeline smoke test."""\nimport json\nfrom pathlib import Path\n\n\ndef test_pipeline_schema():\n    data = json.loads(Path(__file__).with_name("pipeline.json").read_text())\n    assert data["pipeline"] == "parallel"\n    assert len(data["agents"]) >= 1\n')


def team_fixtures(output_dir: Path) -> None:
    leader = agent_config_fixture("team_leader")
    members = [agent_config_fixture(f"member_{i}") for i in range(1, 3)]
    pipeline = {
        "pipeline": "team",
        "leader": leader,
        "members": members,
        "max_rounds": 15,
    }
    write(output_dir / "team" / "pipeline.json", json.dumps(pipeline, indent=2, ensure_ascii=False))
    write(output_dir / "team" / "test_team.py", '"""Team pipeline smoke test."""\nimport json\nfrom pathlib import Path\n\n\ndef test_pipeline_schema():\n    data = json.loads(Path(__file__).with_name("pipeline.json").read_text())\n    assert data["pipeline"] == "team"\n    assert data["leader"]["name"] == "team_leader"\n    assert len(data["members"]) >= 1\n')


def dialogue_fixtures(output_dir: Path) -> None:
    dialogue = {
        "messages": [
            {"role": "user", "content": "Hello?"},
            {"role": "assistant", "content": "Hi, how can I help?"},
        ]
    }
    write(output_dir / "dialogue" / "dialogue.json", json.dumps(dialogue, indent=2, ensure_ascii=False))
    write(output_dir / "dialogue" / "test_dialogue.py", '"""Dialogue fixture smoke test."""\nimport json\nfrom pathlib import Path\n\n\ndef test_dialogue_schema():\n    data = json.loads(Path(__file__).with_name("dialogue.json").read_text())\n    assert "messages" in data\n    assert len(data["messages"]) >= 1\n')


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AgentScope test fixtures")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--pattern", default="all", choices=["all", "sequential", "parallel", "team", "dialogue"])
    args = parser.parse_args()

    generators = {
        "sequential": sequential_fixtures,
        "parallel": parallel_fixtures,
        "team": team_fixtures,
        "dialogue": dialogue_fixtures,
    }

    if args.pattern == "all":
        targets = generators.values()
    else:
        targets = [generators[args.pattern]]

    for generator in targets:
        generator(args.output)

    print(f"Generated test fixtures in: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
