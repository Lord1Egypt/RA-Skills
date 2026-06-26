#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any


EXPECTED_NAME = "bibtex-literature-review"
FORBIDDEN_ARTIFACT_PATTERNS = (
    "__pycache__",
    "*.pyc",
    ".DS_Store",
    "tmp_*",
    "page-*.png",
    "*.pdf",
    "*.docx",
)


class CheckError(RuntimeError):
    pass


def log(message: str):
    print(f"[self-check] {message}")


def fail(message: str):
    raise CheckError(message)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("SKILL.md frontmatter is missing or malformed.")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"Invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def check_frontmatter(root: Path):
    frontmatter = parse_frontmatter(root / "SKILL.md")
    if set(frontmatter) != {"name", "description"}:
        fail(f"Frontmatter keys must be only name and description; got {sorted(frontmatter)}.")
    name = frontmatter["name"]
    description = frontmatter["description"]
    if name != EXPECTED_NAME:
        fail(f"Skill name must be {EXPECTED_NAME!r}; got {name!r}.")
    if root.name != name:
        fail(f"Folder name {root.name!r} must match skill name {name!r}.")
    if not re.match(r"^[a-z0-9-]+$", name):
        fail(f"Skill name is not lowercase hyphen-case: {name!r}.")
    if len(description) > 1024:
        fail(f"Description is too long: {len(description)} characters.")
    if "<" in description or ">" in description:
        fail("Description must not contain angle brackets.")
    log(f"frontmatter ok: name={name}, description_length={len(description)}")


def find_forbidden_artifacts(root: Path) -> list[Path]:
    found: list[Path] = []
    for pattern in FORBIDDEN_ARTIFACT_PATTERNS:
        found.extend(path for path in root.rglob(pattern) if path.exists())
    return sorted(set(found))


def check_package_hygiene(root: Path):
    artifacts = find_forbidden_artifacts(root)
    if artifacts:
        relative = ", ".join(str(path.relative_to(root)) for path in artifacts[:20])
        fail(f"Forbidden generated artifacts remain in skill package: {relative}")

    scanned = []
    for path in list(root.glob("*.md")) + list((root / "references").glob("*.md")) + list((root / "scripts").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[A-Za-z0-9_.-]+", text):
            fail(f"User-specific absolute path found in {path.relative_to(root)}.")
        scanned.append(path.relative_to(root).as_posix())
    log(f"package hygiene ok: scanned {len(scanned)} text/script files")


def compile_scripts_in_memory(root: Path):
    for path in sorted((root / "scripts").glob("*.py")):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    log("script syntax ok")


def run_cmd(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    log("run: " + " ".join(str(part) for part in cmd))
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        fail(f"Command failed with exit code {result.returncode}: {' '.join(cmd)}")
    return result


def assert_json_candidates(path: Path, min_count: int):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        fail("Candidate JSON is not a list.")
    if len(data) < min_count:
        fail(f"Expected at least {min_count} candidate references; found {len(data)}.")
    for idx, item in enumerate(data[:min_count], start=1):
        if not isinstance(item, dict):
            fail(f"Candidate {idx} is not an object.")
        for key in ("key", "type", "fields"):
            if key not in item:
                fail(f"Candidate {idx} missing {key!r}.")
        if not (item.get("gbt") or item.get("formatted") or item.get("text")):
            fail(f"Candidate {idx} missing formatted reference text.")
    log(f"candidate JSON ok: {len(data)} entries")


def create_review_json(candidates_path: Path, review_path: Path):
    candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
    selected = candidates[:5]
    review = {
        "title": "文献综述自检",
        "references": [
            {"key": item.get("key"), "formatted": item.get("formatted") or item.get("gbt")}
            for item in selected
        ],
        "paragraphs": [
            [
                "数字化转型与人力资源管理创新构成员工激励研究的重要背景",
                {"cite": 1},
                "，相关研究也提示企业需要以系统化方式优化绩效和员工体验",
                {"cite": 2},
                "。",
            ],
            [
                "围绕员工满意度、薪酬福利与激励工具，现有文献可形成连续的理论支撑",
                {"cite": [3, 4, 5]},
                "。",
            ],
            [
                "为验证非连续组合引用，自检同时生成逗号式组合",
                {"cite": [1, 5], "collapse": False},
                "。",
            ],
        ],
    }
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inspect_docx_xml(docx: Path):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        with zipfile.ZipFile(docx) as zf:
            zf.extractall(work)
        xml = (work / "word" / "document.xml").read_text(encoding="utf-8")
    required_snippets = [
        "REF _RefBib001 \\h",
        "REF _RefBib003 \\h",
        "REF _RefBib005 \\h",
        'w:vertAlign w:val="superscript"',
        "<w:numPr>",
        'w:name="_RefBib001"',
        'w:name="_RefBib005"',
    ]
    for snippet in required_snippets:
        if snippet not in xml:
            fail(f"DOCX XML missing required snippet: {snippet}")
    if "HYPERLINK" in xml or "<w:hyperlink" in xml:
        fail("DOCX XML contains forbidden hyperlink citation markup.")
    log("DOCX XML spot checks ok")


def integration_test(root: Path, bib: Path, tmpdir: Path, env: dict[str, str]):
    if not bib.exists():
        fail(f"BibTeX test file does not exist: {bib}")
    candidates = tmpdir / "candidates.json"
    review = tmpdir / "review.json"
    docx = tmpdir / "review.docx"

    run_cmd(
        [
            sys.executable,
            str(root / "scripts" / "sources_to_json.py"),
            str(bib),
            "--style",
            "gbt7714",
            "--limit",
            "5",
            "--out",
            str(candidates),
        ],
        cwd=tmpdir,
        env=env,
    )
    assert_json_candidates(candidates, min_count=5)
    create_review_json(candidates, review)

    run_cmd(
        [
            sys.executable,
            str(root / "scripts" / "build_docx_from_review_json.py"),
            str(review),
            "--out",
            str(docx),
        ],
        cwd=tmpdir,
        env=env,
    )
    run_cmd(
        [
            sys.executable,
            str(root / "scripts" / "validate_docx_crossrefs.py"),
            str(docx),
            "--expect-bib-count",
            "5",
            "--expect-ref-fields",
            "6",
            "--forbid-hyperlinks",
            "--require-ref",
            "--require-superscript",
            "--require-auto-numbered-bib",
        ],
        cwd=tmpdir,
        env=env,
    )
    inspect_docx_xml(docx)


def run_self_check(args: argparse.Namespace) -> int:
    root = skill_root()
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(root / "scripts")

    check_frontmatter(root)
    check_package_hygiene(root)
    compile_scripts_in_memory(root)

    if args.keep_temp:
        tmpdir = Path(tempfile.mkdtemp(prefix="bibtex-literature-review-self-check-"))
        log(f"temporary workspace kept: {tmpdir}")
        integration_test(root, args.bib, tmpdir, env)
    else:
        with tempfile.TemporaryDirectory(prefix="bibtex-literature-review-self-check-") as tmp:
            integration_test(root, args.bib, Path(tmp), env)

    check_package_hygiene(root)
    log("PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run an isolated, reproducible self-check for the bibtex-literature-review skill."
    )
    parser.add_argument("--bib", type=Path, required=True, help="Original BibTeX fixture path.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the temporary workspace for debugging.")
    args = parser.parse_args(argv)

    try:
        return run_self_check(args)
    except CheckError as exc:
        print(f"[self-check] FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
