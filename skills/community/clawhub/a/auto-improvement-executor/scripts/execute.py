#!/usr/bin/env python3
"""Executor for low-risk generic-skill candidates."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import (
    EXECUTOR_SUPPORTED_CATEGORIES,
    SCHEMA_VERSION,
    read_json,
    read_text,
    utc_now_iso,
    write_json,
    write_text,
)
from lib.state_machine import (
    DEFAULT_STATE_ROOT,
    backup_file,
    ensure_tree,
    update_state,
)


def capture_execution_trace(candidate: dict, result: dict, error: str | None = None) -> dict:
    """Capture structured execution trace for GEPA feedback."""
    return {
        "type": "execution_trace",
        "candidate_id": candidate.get("id", "unknown"),
        "category": candidate.get("category", "unknown"),
        "target_path": candidate.get("target_path", ""),
        "action": candidate.get("execution_plan", {}).get("action", "unknown"),
        "execution_status": result.get("status", "unknown"),
        "modified": result.get("modified", False),
        "diff_summary": result.get("diff_summary", {}),
        "error": error,
        "timestamp": utc_now_iso(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute a ranked generic-skill candidate")
    parser.add_argument("--input", required=True, help="Ranking artifact JSON")
    parser.add_argument("--candidate-id", required=True, help="Candidate id to execute")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--output", default=None)
    parser.add_argument("--force", action="store_true", help="Allow execution even when critic did not accept")
    return parser.parse_args()


def append_markdown_section(target_path: Path, plan: dict) -> dict:
    before = read_text(target_path)
    heading = plan["section_heading"].strip()
    content_lines = plan.get("content_lines", [])
    if heading in before:
        return {
            "status": "no_change",
            "modified": False,
            "diff": "",
            "diff_summary": {
                "reason": f"section `{heading}` already present",
                "added_lines": 0,
            },
            "after_content": before,
        }
    section = heading + "\n\n" + "\n".join(f"- {line}" for line in content_lines)
    after = before.rstrip() + "\n\n" + section + "\n"
    write_text(target_path, after)
    diff = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=str(target_path),
            tofile=str(target_path),
        )
    )
    return {
        "status": "success",
        "modified": True,
        "diff": diff,
        "diff_summary": {
            "reason": f"appended markdown section `{heading}`",
            "added_lines": len(content_lines) + 2,
        },
        "after_content": after,
    }



def _make_diff(before, after, path):
    """Generate a unified diff string between before/after content."""
    return "\n".join(difflib.unified_diff(
        before.split("\n"), after.split("\n"),
        fromfile=str(path), tofile=str(path), lineterm="",
    ))


def replace_markdown_section(target_path, plan):
    """Replace a section identified by heading with new content."""
    content = read_text(target_path)
    heading = plan.get("section_heading", "")
    new_lines = plan.get("content_lines", [])
    lines = content.split("\n")
    start_idx = None
    end_idx = len(lines)
    heading_level = len(heading) - len(heading.lstrip("#"))
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start_idx = i
        elif start_idx is not None and line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
            end_idx = i
            break
    if start_idx is None:
        return {"status": "no_change", "modified": False, "diff": "", "diff_summary": {"reason": f"section '{heading}' not found", "changed_lines": 0}}
    replacement = [heading] + [f"- {line}" if not line.startswith("-") else line for line in new_lines]
    new_content = "\n".join(lines[:start_idx] + replacement + lines[end_idx:])
    diff = _make_diff(content, new_content, target_path)
    write_text(target_path, new_content)
    return {"status": "success", "modified": True, "diff": diff, "diff_summary": {"reason": "replaced_section", "changed_lines": len(new_lines)}}


def insert_before_section(target_path, plan):
    """Insert content before a specified section heading."""
    content = read_text(target_path)
    heading = plan.get("section_heading", "")
    new_lines = plan.get("content_lines", [])
    lines = content.split("\n")
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            insert_idx = i
            break
    if insert_idx is None:
        return {"status": "no_change", "modified": False, "diff": "", "diff_summary": {"reason": f"section '{heading}' not found", "changed_lines": 0}}
    insertion = [f"- {line}" if not line.startswith("-") and not line.startswith("#") else line for line in new_lines]
    insertion.append("")
    new_content = "\n".join(lines[:insert_idx] + insertion + lines[insert_idx:])
    diff = _make_diff(content, new_content, target_path)
    write_text(target_path, new_content)
    return {"status": "success", "modified": True, "diff": diff, "diff_summary": {"reason": "inserted_before_section", "changed_lines": len(new_lines)}}


def update_yaml_frontmatter(target_path, plan):
    """Update YAML frontmatter fields in a markdown file."""
    content = read_text(target_path)
    updates = plan.get("frontmatter_updates", {})
    if not content.startswith("---"):
        return {"status": "no_change", "modified": False, "diff": "", "diff_summary": {"reason": "no frontmatter found", "changed_lines": 0}}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"status": "no_change", "modified": False, "diff": "", "diff_summary": {"reason": "malformed frontmatter", "changed_lines": 0}}
    try:
        import yaml
    except ImportError:
        return {"status": "error", "modified": False, "diff": "", "diff_summary": {"reason": "PyYAML not available", "changed_lines": 0}}
    frontmatter = yaml.safe_load(parts[1]) or {}
    frontmatter.update(updates)
    new_fm = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    new_content = "---\n" + new_fm + "---" + parts[2]
    diff = _make_diff(content, new_content, target_path)
    write_text(target_path, new_content)
    return {"status": "success", "modified": True, "diff": diff, "diff_summary": {"reason": "updated_frontmatter", "changed_lines": len(updates)}}


ACTION_HANDLERS = {
    "append_markdown_section": append_markdown_section,
    "replace_markdown_section": replace_markdown_section,
    "insert_before_section": insert_before_section,
    "update_yaml_frontmatter": update_yaml_frontmatter,
}


def main() -> int:
    args = parse_args()
    state_root = Path(args.state_root).expanduser().resolve()
    paths = ensure_tree(state_root)

    ranking_artifact = read_json(Path(args.input).expanduser().resolve())
    run_id = ranking_artifact["run_id"]
    target_path = ranking_artifact["target"]["path"]
    candidate = next((item for item in ranking_artifact.get("scored_candidates", []) if item["id"] == args.candidate_id), None)
    if not candidate:
        raise SystemExit(f"candidate not found: {args.candidate_id}")

    recommendation = candidate.get("recommendation")
    if recommendation != "accept_for_execution" and not args.force:
        execution_artifact = {
            "schema_version": SCHEMA_VERSION,
            "lane": ranking_artifact.get("lane", "generic-skill"),
            "run_id": run_id,
            "stage": "executed",
            "status": "unsupported",
            "created_at": utc_now_iso(),
            "candidate_id": candidate["id"],
            "candidate": candidate,
            "source_ranking_artifact": args.input,
            "result": {
                "status": "unsupported",
                "modified": False,
                "reason": f"critic recommendation is `{recommendation}`; use --force to override",
            },
            "next_step": "apply_gate",
            "next_owner": "gate",
        }
        output_path = Path(args.output).expanduser().resolve() if args.output else paths["executions"] / f"{run_id}-{candidate['id']}.json"
        execution_artifact["truth_anchor"] = str(output_path)
        write_json(output_path, execution_artifact)
        update_state(
            state_root,
            run_id=run_id,
            stage="executed",
            status="unsupported",
            target_path=target_path,
            truth_anchor=str(output_path),
            extra={"candidate_id": candidate["id"]},
        )
        print(str(output_path))
        return 0

    category = candidate.get("category")
    if category not in EXECUTOR_SUPPORTED_CATEGORIES:
        result = {
            "status": "unsupported",
            "modified": False,
            "reason": f"category `{category}` is not supported by the first runnable executor",
        }
        output_path = Path(args.output).expanduser().resolve() if args.output else paths["executions"] / f"{run_id}-{candidate['id']}.json"
        artifact = {
            "schema_version": SCHEMA_VERSION,
            "lane": ranking_artifact.get("lane", "generic-skill"),
            "run_id": run_id,
            "stage": "executed",
            "status": result["status"],
            "created_at": utc_now_iso(),
            "candidate_id": candidate["id"],
            "candidate": candidate,
            "source_ranking_artifact": args.input,
            "result": result,
            "next_step": "apply_gate",
            "next_owner": "gate",
            "truth_anchor": str(output_path),
        }
        write_json(output_path, artifact)
        update_state(
            state_root,
            run_id=run_id,
            stage="executed",
            status="unsupported",
            target_path=target_path,
            truth_anchor=str(output_path),
            extra={"candidate_id": candidate["id"]},
        )
        print(str(output_path))
        return 0

    target_file = Path(candidate["target_path"]).expanduser().resolve()
    if not target_file.exists() or not target_file.is_file():
        raise SystemExit(f"target file not found: {target_file}")

    backup_path = paths["executions"] / "backups" / run_id / f"{candidate['id']}-{target_file.name}"
    backup_file(target_file, backup_path)

    plan = candidate.get("execution_plan", {})
    action = plan.get("action")
    handler = ACTION_HANDLERS.get(action)
    if handler is not None:
        result = handler(target_file, plan)
    else:
        result = {
            "status": "unsupported",
            "modified": False,
            "reason": f"action `{action}` is not supported",
        }

    error_msg = None if result["status"] == "success" else result.get("reason")
    execution_trace = capture_execution_trace(candidate, result, error=error_msg)

    output_path = Path(args.output).expanduser().resolve() if args.output else paths["executions"] / f"{run_id}-{candidate['id']}.json"
    execution_artifact = {
        "schema_version": SCHEMA_VERSION,
        "lane": ranking_artifact.get("lane", "generic-skill"),
        "run_id": run_id,
        "stage": "executed",
        "status": result["status"],
        "created_at": utc_now_iso(),
        "candidate_id": candidate["id"],
        "candidate": candidate,
        "source_ranking_artifact": args.input,
        "result": {
            **{key: value for key, value in result.items() if key != "after_content"},
            "backup_path": str(backup_path),
            "rollback_pointer": {
                "method": "restore_backup_file",
                "backup_path": str(backup_path),
                "target_path": str(target_file),
            },
        },
        "execution_trace": execution_trace,
        "next_step": "apply_gate",
        "next_owner": "gate",
        "truth_anchor": str(output_path),
    }
    write_json(output_path, execution_artifact)
    update_state(
        state_root,
        run_id=run_id,
        stage="executed",
        status=result["status"],
        target_path=target_path,
        truth_anchor=str(output_path),
        extra={
            "candidate_id": candidate["id"],
            "execution_modified": result.get("modified", False),
        },
    )
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
