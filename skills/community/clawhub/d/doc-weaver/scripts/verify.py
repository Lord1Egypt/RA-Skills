#!/usr/bin/env python3
"""Release verification for Doc Weaver."""

import subprocess
import sys
import tempfile
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEAVER = ROOT / "scripts" / "weaver.py"
EXAMPLES = ROOT / "examples"


def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def main():
    skill_json = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    meta_json = json.loads((ROOT / "_meta.json").read_text(encoding="utf-8"))
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if meta_json["version"] != skill_json["version"]:
        raise SystemExit("_meta.json version must match skill.json")
    if f"version: {skill_json['version']}" not in skill_md:
        raise SystemExit("SKILL.md frontmatter version must match skill.json")

    print("[verify] checking runtime")
    doctor = run([sys.executable, str(WEAVER), "--doctor"])

    print("[verify] rendering preview")
    preview = run([
        sys.executable,
        str(WEAVER),
        "--input",
        str(EXAMPLES / "chat-feature-prd.md"),
        "--template",
        "prd",
        "--preview",
    ])
    required_preview_markers = [
        "Doc Weaver -- Template: Product Requirements Document",
        "Table of Contents",
        "API Design",
    ]
    for marker in required_preview_markers:
        if marker not in preview:
            raise SystemExit(f"preview missing expected marker: {marker}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        docx_out = tmp_path / "ChatFeaturePRD.docx"
        pdf_out = tmp_path / "SprintPlanning.pdf"

        print("[verify] generating docx")
        run([
            sys.executable,
            str(WEAVER),
            "--input",
            str(EXAMPLES / "chat-feature-prd.md"),
            "--template",
            "prd",
            "--output",
            str(docx_out),
        ])
        if not docx_out.exists() or docx_out.stat().st_size < 1000:
            raise SystemExit("docx output was not created or is unexpectedly small")

        if ".pdf generation:  available" in doctor:
            print("[verify] generating pdf")
            run([
                sys.executable,
                str(WEAVER),
                "--input",
                str(EXAMPLES / "sprint-planning-minutes.md"),
                "--template",
                "meeting-minutes",
                "--output",
                str(pdf_out),
            ])
            if not pdf_out.exists() or pdf_out.stat().st_size < 1000:
                raise SystemExit("pdf output was not created or is unexpectedly small")
        else:
            print("[verify] skipping pdf generation; optional dependencies missing")

    print("[verify] ok")


if __name__ == "__main__":
    main()
