from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


def _is_placeholder(text: str) -> bool:
    low = (text or "").strip().lower()
    if not low:
        return True
    return "(placeholder)" in low or "<!-- scaffold" in low or "todo" in low


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve()
    for _ in range(10):
        if (repo_root / "AGENTS.md").exists():
            break
        parent = repo_root.parent
        if parent == repo_root:
            break
        repo_root = parent
    sys.path.insert(0, str(repo_root))

    from tooling.common import dump_yaml, load_workspace_pipeline_spec, load_yaml, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["outline/taxonomy.yml", "GOAL.md"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/chapter_skeleton.yml"]
    taxonomy_path = workspace / inputs[0]
    goal_path = workspace / inputs[1] if len(inputs) > 1 else workspace / "GOAL.md"
    out_path = workspace / outputs[0]

    if out_path.exists() and out_path.stat().st_size > 0:
        if not _is_placeholder(out_path.read_text(encoding="utf-8", errors="ignore")):
            return 0

    taxonomy = load_yaml(taxonomy_path) if taxonomy_path.exists() else None
    if not isinstance(taxonomy, list) or not taxonomy:
        raise SystemExit(f"Invalid taxonomy in {taxonomy_path}")

    spec = load_workspace_pipeline_spec(workspace)
    target_h3 = int(getattr(spec, "core_chapter_h3_target", 0) or 3)
    goal_line = ""
    if goal_path.exists():
        for raw in goal_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                goal_line = line
                break

    skeleton: list[dict[str, Any]] = []
    section_no = 3
    for topic in taxonomy:
        if not isinstance(topic, dict):
            continue
        title = str(topic.get("name") or "").strip()
        if not title:
            continue
        desc = str(topic.get("description") or "").strip()
        children = topic.get("children") or []
        seed_topics = [
            str(child.get("name") or "").strip()
            for child in children
            if isinstance(child, dict) and str(child.get("name") or "").strip()
        ][: max(3, target_h3)]
        rationale = desc or (f"retrieval-informed chapter for {title}" if not goal_line else f"{title} within {goal_line}")
        skeleton.append(
            {
                "id": str(section_no),
                "title": title,
                "rationale": rationale,
                "seed_topics": seed_topics,
                "target_h3_count": target_h3,
            }
        )
        section_no += 1

    dump_yaml(out_path, skeleton)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
