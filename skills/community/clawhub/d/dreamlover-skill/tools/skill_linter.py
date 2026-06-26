from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CANON_HEADERS = [
    "## Basic Identity",
    "## Setting Attributes",
    "## Key Plot Events",
    "## Confirmed Relationships",
    "## Official Statements And Notes",
]
PERSONA_HEADERS = [
    "## Behavior Patterns",
    "## Emotional Tendencies",
    "## Interaction Style",
    "## Relationship Progression",
    "## Boundaries And Preferences",
]
STYLE_HEADERS = [
    "## Address Patterns",
    "## Rhythm And Sentence Shape",
    "## Verbal Tics",
    "## Short Example Lines",
]
DEFAULT_INSTALL_ROOT = Path(".agents") / "skills"
DEFAULT_ARCHIVE_ROOT = Path("characters")
REQUIRED_FILES = [
    "SKILL.md",
    "canon.md",
    "persona.md",
    "style_examples.md",
    "meta.json",
]
META_FIELDS = [
    "slug",
    "character_name",
    "source_work",
    "target_use",
    "source_types",
    "allow_low_confidence_persona",
    "source_decision_policy",
    "input_mode",
    "search_scope",
    "archive_mirror",
    "source_paths",
    "layout_version",
    "created_at",
    "updated_at",
    "primary_path",
    "archive_path",
    "install_scope",
    "canonical_source",
    "export_targets",
    "generated_for",
    "openclaw_exported_at",
]
SECTION_RULES = {
    "canon.md": {
        "expected": CANON_HEADERS,
        "forbidden": PERSONA_HEADERS + STYLE_HEADERS,
    },
    "persona.md": {
        "expected": PERSONA_HEADERS,
        "forbidden": CANON_HEADERS + STYLE_HEADERS,
    },
    "style_examples.md": {
        "expected": STYLE_HEADERS,
        "forbidden": CANON_HEADERS + PERSONA_HEADERS,
    },
}
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"No confirmed .* recorded yet\.", re.IGNORECASE),
    re.compile(r"No summarized .* recorded yet\.", re.IGNORECASE),
    re.compile(r"No style .* recorded yet\.", re.IGNORECASE),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_scope(value: str) -> str:
    allowed = {"codex", "archive", "both"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(f"Unsupported scope: {value}")
    return value


def resolve_root(base_root: Path, value: str | None, fallback: Path) -> Path:
    if not value:
        return base_root / fallback
    path = Path(value)
    return path if path.is_absolute() else base_root / path


def find_header_occurrences(text: str, header: str) -> list[int]:
    return [
        index
        for index, line in enumerate(text.splitlines(), start=1)
        if line.strip().lstrip("\ufeff") == header
    ]


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML front matter.")
    closing_marker = text.find("\n---\n", 4)
    if closing_marker == -1:
        raise ValueError("SKILL.md front matter is not closed.")
    front_matter = text[4:closing_marker]
    data: dict[str, str] = {}
    for raw_line in front_matter.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front matter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def add_message(messages: list[dict], path: Path, level: str, message: str) -> None:
    messages.append(
        {
            "level": level,
            "file": path.name,
            "path": str(path),
            "message": message,
        }
    )


def lint_section_file(path: Path, messages: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    rules = SECTION_RULES[path.name]
    lines = text.splitlines()

    for header in rules["expected"]:
        positions = find_header_occurrences(text, header)
        if not positions:
            add_message(messages, path, "error", f"Missing required section header: {header}")
        elif len(positions) > 1:
            add_message(messages, path, "error", f"Duplicate section header: {header}")

    ordered_positions: list[int] = []
    for header in rules["expected"]:
        positions = find_header_occurrences(text, header)
        if positions:
            ordered_positions.append(positions[0])
    if ordered_positions != sorted(ordered_positions):
        add_message(messages, path, "error", "Section headers are out of order.")

    for header in rules["forbidden"]:
        if header in text:
            add_message(messages, path, "error", f"Contains forbidden section header: {header}")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            add_message(messages, path, "warning", f"Contains placeholder content matching `{pattern.pattern}`.")

    nonempty_sections = [line for line in lines if line.strip() and not line.startswith("## ")]
    if not nonempty_sections:
        add_message(messages, path, "warning", "File has section headers but no content lines.")


def lint_skill_markdown(path: Path, expected_slug: str | None, messages: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    try:
        front_matter = parse_front_matter(text)
    except ValueError as exc:
        add_message(messages, path, "error", str(exc))
        return

    for field in ("name", "description"):
        if not front_matter.get(field):
            add_message(messages, path, "error", f"Missing front matter field: {field}")

    if expected_slug and front_matter.get("name") and front_matter["name"] != expected_slug:
        add_message(messages, path, "error", f"Front matter name must match slug `{expected_slug}`.")

    description = front_matter.get("description", "").lower()
    if description and "roleplay" not in description and "voice" not in description:
        add_message(messages, path, "warning", "Description should mention roleplay or character voice.")
    metadata_blob = front_matter.get("metadata", "")
    if "openclaw" not in metadata_blob.lower() or "python3" not in metadata_blob.lower():
        add_message(messages, path, "warning", "Child skill should declare OpenClaw python3 requirements in front matter.")
    if "openclaw" not in description:
        add_message(messages, path, "warning", "Description should mention OpenClaw compatibility.")
    if "memory_prepare.py" not in text:
        add_message(messages, path, "warning", "Child skill should mention memory_prepare.py for conditional memory gating.")
    if "memory_commit.py" not in text:
        add_message(messages, path, "warning", "Child skill should mention memory_commit.py for conditional memory writes.")
    if "memory_summarize.py" not in text:
        add_message(messages, path, "warning", "Child skill should mention memory_summarize.py for threshold summaries.")
    if ".dreamlover-data" not in text:
        add_message(messages, path, "warning", "Child skill should point dynamic memory storage to .dreamlover-data.")
    if "python3" not in text or "no-memory mode" not in text:
        add_message(messages, path, "warning", "Child skill should describe python3 dependency and no-memory fallback.")
    lowered = text.lower()
    if "i will check memory first" in lowered or "i am running the memory gate" in lowered:
        add_message(messages, path, "warning", "Child skill should not instruct user-visible internal flow narration.")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            add_message(messages, path, "warning", f"Contains placeholder content matching `{pattern.pattern}`.")


def lint_meta(path: Path, messages: list[dict]) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_message(messages, path, "error", f"Invalid JSON: {exc}")
        return {}

    for field in META_FIELDS:
        if field not in payload:
            add_message(messages, path, "error", f"Missing meta field: {field}")
    return payload


def lint_skill_dir(skill_dir: Path) -> dict:
    messages: list[dict] = []
    meta_payload: dict = {}

    for required in REQUIRED_FILES:
        path = skill_dir / required
        if not path.exists():
            add_message(messages, path, "error", f"Missing required file: {required}")

    if not skill_dir.exists():
        add_message(messages, skill_dir, "error", "Skill directory does not exist.")
    else:
        meta_path = skill_dir / "meta.json"
        if meta_path.exists():
            meta_payload = lint_meta(meta_path, messages)

        skill_path = skill_dir / "SKILL.md"
        if skill_path.exists():
            lint_skill_markdown(skill_path, meta_payload.get("slug", skill_dir.name), messages)

        for filename in ("canon.md", "persona.md", "style_examples.md"):
            path = skill_dir / filename
            if path.exists():
                lint_section_file(path, messages)

    errors = [item for item in messages if item["level"] == "error"]
    warnings = [item for item in messages if item["level"] == "warning"]
    return {
        "skill_dir": str(skill_dir),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def resolve_skill_dirs(
    root: Path,
    slug: str | None,
    skill_dir: str | None,
    output_root: str | None,
    scope: str,
) -> dict[str, Path]:
    if skill_dir:
        return {"custom": Path(skill_dir)}
    if not slug:
        raise SystemExit("--slug is required when --skill-dir is not provided")

    resolved: dict[str, Path] = {}
    if scope in {"codex", "both"}:
        resolved["codex"] = resolve_root(root, output_root, DEFAULT_INSTALL_ROOT) / slug
    if scope in {"archive", "both"}:
        fallback_output = output_root if scope == "archive" else None
        resolved["archive"] = resolve_root(root, fallback_output, DEFAULT_ARCHIVE_ROOT) / slug
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated child skill packages.")
    parser.add_argument("--slug", help="Character slug to inspect.")
    parser.add_argument("--skill-dir", help="Direct path to a child skill directory.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--output-root", help="Override the inspected root.")
    parser.add_argument(
        "--scope",
        default="codex",
        type=parse_scope,
        help="Which package root to inspect: codex, archive, or both. Default is codex.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    reports = {
        location: lint_skill_dir(path)
        for location, path in resolve_skill_dirs(root, args.slug, args.skill_dir, args.output_root, args.scope).items()
    }
    payload = reports if len(reports) > 1 else next(iter(reports.values()))
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if any(not report["valid"] for report in reports.values()):
        raise SystemExit(1)
    if any(report["warnings"] for report in reports.values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
