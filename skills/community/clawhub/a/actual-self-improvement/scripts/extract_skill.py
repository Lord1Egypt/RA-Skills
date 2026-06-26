#!/usr/bin/env python3
"""Create a new skill scaffold from a proven learning."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OUTPUT_FORMATS = ["json", "text", "markdown"]


class CliError(Exception):
    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def print_output(payload: Any, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    if fmt == "markdown":
        if isinstance(payload, dict):
            for key, value in payload.items():
                print(f"- **{key}**: {value}")
            return
    if isinstance(payload, dict):
        for key, value in payload.items():
            print(f"{key}: {value}")
        return
    print(payload)


def resolve_root(path_str: str) -> Path:
    root = Path(path_str).expanduser().resolve()
    if not root.exists():
        raise CliError(f"Workspace root does not exist: {root}", 2)
    if not root.is_dir():
        raise CliError(f"Workspace root is not a directory: {root}", 2)
    return root


def validate_output_dir(output_dir: str) -> str:
    if output_dir.startswith("/"):
        raise CliError("--output-dir must be relative to --root")
    if ".." in Path(output_dir).parts:
        raise CliError("--output-dir must not contain '..' path segments")
    cleaned = output_dir.strip() or "skills"
    return cleaned


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def skill_template(args: argparse.Namespace) -> str:
    lines: List[str] = ["---", f"name: {args.name}"]
    lines.append(f"description: {args.description or '[TODO: describe what this skill does and when to use it]'}")
    if args.compatibility:
        lines.append(f"compatibility: {args.compatibility}")
    lines.append("metadata:")
    lines.append(f"  version: \"{args.version}\"")
    if args.from_learning_id:
        lines.append(f"  source_learning: \"{args.from_learning_id}\"")
    if args.author:
        lines.append(f"  author: \"{args.author}\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# {args.title or title_from_name(args.name)}")
    lines.append("")
    lines.append("One-sentence explanation of the problem this skill solves.")
    lines.append("")
    lines.append("## When to use")
    lines.append("")
    lines.append("Use this skill when:")
    lines.append("- trigger or situation 1")
    lines.append("- trigger or situation 2")
    lines.append("- trigger or situation 3")
    lines.append("")
    lines.append("Do not use it for:")
    lines.append("- adjacent case 1")
    lines.append("- adjacent case 2")
    lines.append("")
    lines.append("## Workflow")
    lines.append("")
    lines.append("1. Step one")
    lines.append("2. Step two")
    lines.append("3. Verify the result")
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append("Move long documentation into `references/` once the skill grows.")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"- Learning ID: {args.from_learning_id or '[TODO: add learning id]'}")
    return "\n".join(lines) + "\n"


def evals_template(skill_name: str) -> str:
    return json.dumps(
        {
            "skill_name": skill_name,
            "evals": [
                {
                    "id": 1,
                    "prompt": "[TODO] realistic user request this new skill should handle",
                    "expected_output": "[TODO] what success looks like",
                    "assertions": [
                        "[TODO] output contains the required artefact or result",
                        "[TODO] workflow followed the expected structure",
                    ],
                }
            ],
        },
        indent=2,
    ) + "\n"


def create_files(skill_path: Path, args: argparse.Namespace) -> Dict[str, Any]:
    created: List[str] = []

    skill_path.mkdir(parents=True, exist_ok=True)
    created.append(str(skill_path))

    skill_md = skill_path / "SKILL.md"
    skill_md.write_text(skill_template(args), encoding="utf-8")
    created.append(str(skill_md))

    references_dir = skill_path / "references"
    references_dir.mkdir(exist_ok=True)
    created.append(str(references_dir))

    examples_md = references_dir / "examples.md"
    examples_md.write_text("# Examples\n\nAdd concrete examples here.\n", encoding="utf-8")
    created.append(str(examples_md))

    if args.scaffold_evals:
        evals_dir = skill_path / "evals"
        evals_dir.mkdir(exist_ok=True)
        created.append(str(evals_dir))
        evals_json = evals_dir / "evals.json"
        evals_json.write_text(evals_template(args.name), encoding="utf-8")
        created.append(str(evals_json))

    return {"created": created}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new Agent Skill scaffold from a proven learning.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("name", help="Skill name in lowercase kebab-case")
    parser.add_argument("--root", required=True, help="Workspace root where the new skill should be created")
    parser.add_argument("--output-dir", default="skills", help="Relative output directory under --root")
    parser.add_argument("--description", help="Skill description for frontmatter")
    parser.add_argument("--title", help="Human-readable title")
    parser.add_argument("--from-learning-id", help="Source learning ID, e.g. LRN-20260313-001")
    parser.add_argument("--compatibility", help="Optional compatibility frontmatter")
    parser.add_argument("--author", help="Optional metadata author value")
    parser.add_argument("--version", default="1.0.0", help="Initial version metadata")
    parser.add_argument("--scaffold-evals", action="store_true", help="Create evals/evals.json scaffold")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing scaffold if present")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be created without writing files")
    parser.add_argument("--format", choices=OUTPUT_FORMATS, default="json", help="Output format")
    args = parser.parse_args()

    try:
        if not NAME_RE.fullmatch(args.name):
            raise CliError("Invalid skill name. Use lowercase letters, numbers, and single hyphens only.")
        root = resolve_root(args.root)
        output_dir = validate_output_dir(args.output_dir)
        skill_path = root / output_dir / args.name

        if skill_path.exists() and not args.force:
            raise CliError(f"Skill path already exists: {skill_path}. Use --force to overwrite.")

        preview = {
            "ok": True,
            "workspace_root": str(root),
            "skill_path": str(skill_path),
            "scaffold_evals": args.scaffold_evals,
        }

        if args.dry_run:
            preview["sketch"] = skill_template(args)
            print_output(preview, args.format)
            return 0

        if skill_path.exists() and args.force:
            for child in sorted(skill_path.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()

        created = create_files(skill_path, args)
        preview.update(created)
        print_output(preview, args.format)
        return 0
    except CliError as exc:
        eprint(f"Error: {exc}")
        return exc.exit_code


if __name__ == "__main__":
    sys.exit(main())
