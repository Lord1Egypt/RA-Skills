#!/usr/bin/env python3
"""Self-validate the dualgap skill without calling an LLM API."""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import validate_outputs


REQUIRED_FILES = [
    "SKILL.md",
    "HOW_TO_USE.md",
    "scripts/run_literature_workflow.py",
    "scripts/validate_outputs.py",
    "scripts/self_validate_skill.py",
    "references/note_schema.md",
    "references/config.example.json",
    "evals/evals.json",
    "requirements.txt",
]


def run_quick_validate(skill_dir: Path) -> dict[str, Any]:
    quick_validate = skill_dir.parent / "skill-creator" / "scripts" / "quick_validate.py"
    if not quick_validate.exists():
        return internal_skill_validate(skill_dir, f"Missing skill-creator validator: {quick_validate}")
    result = subprocess.run(
        [sys.executable, str(quick_validate), str(skill_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0 and "No module named 'yaml'" in (result.stdout + result.stderr):
        return internal_skill_validate(skill_dir, "skill-creator quick_validate.py could not import PyYAML; used built-in fallback validator.")
    return {
        "passed": result.returncode == 0,
        "evidence": (result.stdout + result.stderr).strip(),
    }


def internal_skill_validate(skill_dir: Path, reason: str) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"passed": False, "fallback": True, "reason": reason, "evidence": "SKILL.md missing"}
    text = skill_md.read_text(encoding="utf-8-sig", errors="ignore")
    match = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    if not match:
        return {"passed": False, "fallback": True, "reason": reason, "evidence": "YAML frontmatter block missing"}
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, flags=re.M)
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, flags=re.M)
    errors = []
    if not name_match:
        errors.append("name missing")
    elif not re.match(r"^[a-z0-9-]+$", name_match.group(1).strip()):
        errors.append("name is not kebab-case")
    if not description_match:
        errors.append("description missing")
    elif len(description_match.group(1).strip()) > 1024:
        errors.append("description is too long")
    return {
        "passed": not errors,
        "fallback": True,
        "reason": reason,
        "evidence": "Built-in frontmatter validator passed." if not errors else "; ".join(errors),
    }


def compile_scripts(skill_dir: Path) -> dict[str, Any]:
    scripts = sorted((skill_dir / "scripts").glob("*.py"))
    failures = []
    for script in scripts:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append({"script": str(script.relative_to(skill_dir)), "error": str(exc)})
    return {
        "passed": not failures,
        "checked": [str(script.relative_to(skill_dir)) for script in scripts],
        "failures": failures,
    }


def validate_evals(skill_dir: Path) -> dict[str, Any]:
    path = skill_dir / "evals" / "evals.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    errors = []
    if data.get("skill_name") != "dualgap":
        errors.append("skill_name must be dualgap")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 3:
        errors.append("at least three evals are expected")
    for item in evals or []:
        if not item.get("prompt"):
            errors.append(f"eval {item.get('id')} missing prompt")
        expectations = item.get("expectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"eval {item.get('id')} missing expectations")
    return {"passed": not errors, "errors": errors}


def write_fake_output(out_dir: Path) -> None:
    (out_dir / "notes" / "direction_a").mkdir(parents=True)
    (out_dir / "notes" / "direction_b").mkdir(parents=True)
    (out_dir / "reviews").mkdir()
    (out_dir / "syntheses").mkdir()
    (out_dir / "synthesis_reviews").mkdir()

    manifest = {
        "direction_a": "Direction A",
        "direction_b": "Direction B",
        "count_a": 1,
        "count_b": 1,
        "model": "offline-self-test",
        "agenda_supplied": True,
    }
    (out_dir / "workflow_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    note_template = """# Offline Test Paper

## 1. Basic Information
- File: fake.pdf
- Direction: {direction}
- Paper type: offline validator fixture
- Strictly belongs to this direction: yes
- Main task: verify output structure
- Data / benchmark: synthetic
- Confidence: high

## 2. Background And Motivation
This fixture exists to test validation plumbing, not paper quality.

## 3. Core Challenge
The validator must distinguish a complete workflow output from missing files.

## 4. Method: Step-By-Step Mechanism
The fixture creates notes, reviews, synthesis files, synthesis reviews, a manifest, and an audit report.

## 5. Why The Method Could Work
The validator checks required files and pass statuses deterministically.

## 6. Experiments And Evidence
The self-test calls validate_outputs.validate on this fixture.

## 7. Assumptions And Failure Modes
It does not test LLM quality, only the workflow contract.

## 8. Implications For The Cross-Direction Research Agenda
This is a validation harness for the skill.

## 9. Open Questions To Verify
Real runs still require human inspection of sampled notes. A reviewer should verify that each note contains concrete paper-specific mechanisms, assumptions, and failure modes rather than generic prose. The reviewer should also check that synthesis outputs distinguish author evidence from model inference and uncertain hypotheses. This longer section is intentional: it prevents the deterministic validator from accepting notes that are visibly truncated right after the final heading.
"""
    (out_dir / "notes" / "direction_a" / "001_fake_a.md").write_text(note_template.format(direction="Direction A"), encoding="utf-8")
    (out_dir / "notes" / "direction_b" / "001_fake_b.md").write_text(note_template.format(direction="Direction B"), encoding="utf-8")

    review = {"pass": True, "score": 9, "failure_reasons": [], "rewrite_instructions": [], "evidence": "offline fixture"}
    for direction, paper_id in [("direction_a", "001_fake_a"), ("direction_b", "001_fake_b")]:
        row = {"paper_id": paper_id, "note_path": f"notes/{direction}/{paper_id}.md", "review": review}
        (out_dir / "reviews" / f"{direction}_batch_001.jsonl").write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")

    long_body = "\n".join(
        [
            "# Offline Synthesis",
            "",
            "This synthetic document is intentionally long enough for validation.",
            "It states a gap, why adjacent work does not solve it, a validation experiment, and a risk.",
        ]
        + [f"- Evidence line {i}: concrete mechanism, target bottleneck, and validation plan." for i in range(80)]
    )
    for name in validate_outputs.REQUIRED_SYNTHESES:
        (out_dir / "syntheses" / name).write_text(long_body, encoding="utf-8")
        review_name = name.replace(".md", ".json")
        (out_dir / "synthesis_reviews" / review_name).write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")

    (out_dir / "audit_report.md").write_text("# Workflow Audit Report\n\nOffline self-test fixture.\n", encoding="utf-8")


def validate_fake_output() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="paper_research_gap_selftest_") as tmp:
        out_dir = Path(tmp)
        write_fake_output(out_dir)
        ok, errors = validate_outputs.validate(out_dir)
        return {"passed": ok, "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", default="", help="Optional path to write the validation report")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    results = {
        "skill_dir": str(skill_dir),
        "required_files": {
            "passed": all((skill_dir / rel).exists() for rel in REQUIRED_FILES),
            "missing": [rel for rel in REQUIRED_FILES if not (skill_dir / rel).exists()],
        },
        "quick_validate": run_quick_validate(skill_dir),
        "compile_scripts": compile_scripts(skill_dir),
        "evals": validate_evals(skill_dir),
        "fake_output_validation": validate_fake_output(),
    }
    results["passed"] = all(section.get("passed") for key, section in results.items() if isinstance(section, dict) and "passed" in section)

    text = json.dumps(results, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
