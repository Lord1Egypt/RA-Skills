#!/usr/bin/env python3
"""Skill Forge CLI — generate Skills and task suites.

Two primary modes:

Mode A: Generate task suite for existing skill
  python3 scripts/forge.py --from-skill /path/to/skill --output /path/to/output

Mode B: Generate skill + task suite from spec
  python3 scripts/forge.py --from-spec spec.yaml --output /path/to/output

Common flags:
  --mock       Use mock LLM (for testing)
  --evaluate   Run evaluator after generation (requires improvement-evaluator)
  --auto-improve  Run orchestrator if below SOLID (requires improvement-orchestrator)
"""

import argparse
import sys
import yaml
import json
from pathlib import Path

# Add parent directory to path so we can import sibling modules
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_DIR = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.task_suite_generator import generate_task_suite, write_task_suite
from scripts.skill_generator import generate_skill_from_spec
from interfaces.spec_schema import SkillSpec


def main():
    parser = argparse.ArgumentParser(
        description="Skill Forge: generate Skills and task suites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--from-skill",
        type=Path,
        help="Path to an existing skill directory (with SKILL.md). "
        "Generates task_suite.yaml only.",
    )
    group.add_argument(
        "--from-spec",
        type=Path,
        help="Path to a skill_spec.yaml. Generates SKILL.md + task_suite.yaml.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for generated files. "
        "Defaults to current directory.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock LLM (for testing without API calls).",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run improvement-evaluator after generation.",
    )
    parser.add_argument(
        "--auto-improve",
        action="store_true",
        help="Run improvement-orchestrator if score below SOLID.",
    )

    args = parser.parse_args()

    # Determine output directory
    output_dir = args.output or Path(".")

    if args.from_skill:
        # Mode A: Generate task suite for existing skill
        return handle_from_skill(args.from_skill, output_dir, args)
    elif args.from_spec:
        # Mode B: Generate skill + task suite from spec
        return handle_from_spec(args.from_spec, output_dir, args)


def handle_from_skill(
    skill_path: Path, output_dir: Path, args: argparse.Namespace
) -> int:
    """Mode A: Generate task suite for an existing SKILL.md."""
    skill_path = skill_path.resolve()

    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory", file=sys.stderr)
        return 1

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: No SKILL.md found at {skill_md}", file=sys.stderr)
        return 1

    print(f"Analyzing SKILL.md at {skill_path}...")
    suite = generate_task_suite(skill_path, mock=args.mock)

    task_count = len(suite.get("tasks", []))
    print(f"Generated {task_count} test tasks.")

    out_file = write_task_suite(suite, output_dir)
    print(f"Task suite written to {out_file}")

    if args.evaluate:
        return run_evaluation(output_dir, suite["skill_id"])
    return 0


def handle_from_spec(
    spec_path: Path, output_dir: Path, args: argparse.Namespace
) -> int:
    """Mode B: Generate skill + task suite from a spec."""
    spec_path = spec_path.resolve()

    if not spec_path.exists():
        print(f"Error: Spec file not found: {spec_path}", file=sys.stderr)
        return 1

    # Load and validate spec
    spec = SkillSpec.from_yaml(spec_path)
    errors = spec.validate()
    if errors:
        for e in errors:
            print(f"Spec validation error: {e}", file=sys.stderr)
        return 1

    print(f"Generating skill '{spec.name}' from spec...")

    # Create skill directory
    skill_dir = output_dir / spec.name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Generate SKILL.md
    spec_dict = yaml.safe_load(spec_path.read_text())
    skill_md_content = generate_skill_from_spec(spec_dict)
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content)
    print(f"SKILL.md written to {skill_md_path}")

    # Generate task suite from the generated SKILL.md
    suite = generate_task_suite(skill_dir, mock=args.mock)
    task_count = len(suite.get("tasks", []))
    print(f"Generated {task_count} test tasks.")

    out_file = write_task_suite(suite, skill_dir)
    print(f"Task suite written to {out_file}")

    if args.evaluate:
        return run_evaluation(skill_dir, suite["skill_id"])
    if args.auto_improve:
        return run_auto_improve(skill_dir, suite["skill_id"])
    return 0


def run_evaluation(output_dir: Path, skill_id: str) -> int:
    """Run improvement-evaluator on the generated task suite."""
    evaluator_script = (
        Path.home()
        / ".claude/skills/improvement-evaluator/scripts/evaluate.py"
    )
    if not evaluator_script.exists():
        print(
            "Warning: improvement-evaluator not found. "
            "Skipping evaluation.",
            file=sys.stderr,
        )
        return 0

    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            str(evaluator_script),
            "--skill",
            skill_id,
            "--suite",
            str(output_dir / "task_suite.yaml"),
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def run_auto_improve(output_dir: Path, skill_id: str) -> int:
    """Run improvement-orchestrator if score is below SOLID."""
    orchestrator_script = (
        Path.home()
        / ".claude/skills/improvement-orchestrator/scripts/orchestrate.py"
    )
    if not orchestrator_script.exists():
        print(
            "Warning: improvement-orchestrator not found. "
            "Skipping auto-improve.",
            file=sys.stderr,
        )
        return 0

    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            str(orchestrator_script),
            "--skill",
            skill_id,
            "--target-grade",
            "SOLID",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main() or 0)
