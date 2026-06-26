#!/usr/bin/env python3
"""Fetch and analyze reference Skill candidates for factory design work."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))

from _common import json_print, run_command, utc_now


IGNORED_DIRS = {
    ".git",
    ".clawhub",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}
TEXT_EXTENSIONS = {
    ".cjs",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SENSITIVE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bapi[_-]?key\b",
        r"\bsecret\b",
        r"\btoken\b",
        r"\bpassword\b",
        r"\bcredential\b",
    )
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    return re.sub(r"-{2,}", "-", slug).strip("-") or "reference-skill"


def derive_slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name
    if name.endswith(".git"):
        name = name[:-4]
    return slugify(name)


def safe_destination(out_dir: Path, slug: str) -> Path:
    out_dir = out_dir.resolve()
    destination = (out_dir / slugify(slug)).resolve()
    if out_dir != destination and out_dir not in destination.parents:
        raise ValueError("destination must stay inside --out")
    return destination


def copy_local_skill(source: Path, destination: Path) -> None:
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"local source is not a directory: {source}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(*IGNORED_DIRS),
    )


def clone_github_skill(url: str, destination: Path) -> dict[str, Any]:
    result = run_command(
        ["git", "clone", "--depth", "1", url, str(destination)],
        timeout=180,
    )
    if not result["ok"]:
        raise RuntimeError(result["stderr"] or "git clone failed")
    return {
        "command": result["command"],
        "returncode": result["returncode"],
    }


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def read_text(path: Path, limit: int = 250_000) -> str:
    try:
        data = path.read_bytes()[:limit]
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    content = read_text(skill_md)
    if not content.startswith("---"):
        return {}
    match = re.match(r"^---\r?\n(?P<body>[\s\S]*?)\r?\n---", content)
    if not match:
        return {}

    frontmatter: dict[str, Any] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        cleaned = value.strip().strip("\"'")
        frontmatter[key.strip()] = cleaned
    return frontmatter


def classify_file(root: Path, file_path: Path) -> str:
    relative_parts = file_path.relative_to(root).parts
    if relative_parts[0] == "scripts":
        return "script"
    if relative_parts[0] == "references":
        return "reference"
    if relative_parts[0] == "assets":
        return "asset"
    if relative_parts[0] in {"agents", "platform-manifests"}:
        return "manifest"
    if file_path.name in {"package.json", "requirements.txt", "pyproject.toml"}:
        return "dependency"
    if file_path.name == "SKILL.md":
        return "skill"
    return "other"


def find_sensitive_hints(root: Path, files: list[Path]) -> list[dict[str, str]]:
    hints: list[dict[str, str]] = []
    for file_path in files:
        if file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        content = read_text(file_path, limit=80_000)
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(content):
                hints.append(
                    {
                        "file": str(file_path.relative_to(root)),
                        "pattern": pattern.pattern,
                    }
                )
                break
    return hints[:20]


def analyze_skill(skill_path: Path) -> dict[str, Any]:
    root = skill_path.resolve()
    files = iter_files(root)
    skill_md = root / "SKILL.md"
    buckets: dict[str, list[str]] = {
        "scripts": [],
        "references": [],
        "assets": [],
        "manifests": [],
        "dependencies": [],
        "other": [],
    }

    for file_path in files:
        relative = str(file_path.relative_to(root))
        kind = classify_file(root, file_path)
        if kind == "script":
            buckets["scripts"].append(relative)
        elif kind == "reference":
            buckets["references"].append(relative)
        elif kind == "asset":
            buckets["assets"].append(relative)
        elif kind == "manifest":
            buckets["manifests"].append(relative)
        elif kind == "dependency":
            buckets["dependencies"].append(relative)
        elif kind != "skill":
            buckets["other"].append(relative)

    frontmatter = parse_frontmatter(skill_md) if skill_md.exists() else {}
    sensitive_hints = find_sensitive_hints(root, files)
    warnings = []
    if not skill_md.exists():
        warnings.append("SKILL.md is missing")
    if sensitive_hints:
        warnings.append("sensitive-name hints found; review before reuse")
    if not buckets["scripts"] and not buckets["references"]:
        warnings.append("no scripts or references found")

    return {
        "tool": "reference-skill",
        "action": "analyze",
        "status": "ok" if skill_md.exists() else "degraded",
        "generated_at": utc_now(),
        "skill_path": str(root),
        "summary": {
            "has_skill_md": skill_md.exists(),
            "frontmatter": frontmatter,
            "file_count": len(files),
            "script_count": len(buckets["scripts"]),
            "reference_count": len(buckets["references"]),
            "asset_count": len(buckets["assets"]),
            "manifest_count": len(buckets["manifests"]),
            "dependency_files": buckets["dependencies"],
            "warnings": warnings,
        },
        "evidence_files": buckets,
        "sensitive_hints": sensitive_hints,
    }


def write_markdown_report(analysis: dict[str, Any], output_path: Path) -> None:
    summary = analysis["summary"]
    evidence = analysis["evidence_files"]
    frontmatter = summary.get("frontmatter") or {}

    def lines_for(items: list[str]) -> list[str]:
        return [f"- `{item}`" for item in items] or ["- None found"]

    content = [
        "# Reference Skill Analysis",
        "",
        f"- path: `{analysis['skill_path']}`",
        f"- status: `{analysis['status']}`",
        f"- name: `{frontmatter.get('name', '')}`",
        f"- description: {frontmatter.get('description', '')}",
        f"- files: `{summary['file_count']}`",
        f"- scripts: `{summary['script_count']}`",
        f"- references: `{summary['reference_count']}`",
        f"- assets: `{summary['asset_count']}`",
        f"- manifests: `{summary['manifest_count']}`",
        "",
        "## Scripts",
        "",
        *lines_for(evidence["scripts"]),
        "",
        "## References",
        "",
        *lines_for(evidence["references"]),
        "",
        "## Manifests",
        "",
        *lines_for(evidence["manifests"]),
        "",
        "## Dependencies",
        "",
        *lines_for(evidence["dependencies"]),
        "",
        "## Warnings",
        "",
        *lines_for(summary["warnings"]),
        "",
    ]
    output_path.write_text("\n".join(content), encoding="utf-8")


def command_fetch(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.slug
    if not slug:
        slug = derive_slug_from_url(args.url) if args.source == "github" else slugify(Path(args.path).name)
    destination = safe_destination(out_dir, slug)
    if destination.exists():
        if not args.overwrite:
            raise FileExistsError(f"destination already exists: {destination}")
        shutil.rmtree(destination)

    fetch_meta: dict[str, Any] = {
        "tool": "reference-skill",
        "action": "fetch",
        "source": args.source,
        "fetched_at": utc_now(),
        "destination": str(destination),
    }
    if args.source == "local":
        fetch_meta["input"] = str(Path(args.path).resolve())
        copy_local_skill(Path(args.path).resolve(), destination)
    elif args.source == "github":
        fetch_meta["input"] = args.url
        fetch_meta.update(clone_github_skill(args.url, destination))
    else:
        raise ValueError(f"unsupported source: {args.source}")

    (destination / "_fetch-meta.json").write_text(
        json.dumps(fetch_meta, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    analysis = analyze_skill(destination)
    (destination / "_reference-analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(analysis, destination / "_reference-analysis.md")

    payload = {
        **fetch_meta,
        "status": analysis["status"],
        "analysis_path": str(destination / "_reference-analysis.json"),
        "markdown_path": str(destination / "_reference-analysis.md"),
        "summary": analysis["summary"],
    }
    return json_print(payload)


def command_analyze(args: argparse.Namespace) -> int:
    analysis = analyze_skill(Path(args.path))
    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown_report(analysis, Path(args.markdown))
    return json_print(analysis)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and analyze reference Skill candidates.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch = subparsers.add_parser("fetch", help="Fetch a local or GitHub Skill into an evidence directory.")
    fetch.add_argument("--source", choices=("local", "github"), required=True)
    fetch.add_argument("--path", default="", help="Local Skill directory when --source local.")
    fetch.add_argument("--url", default="", help="GitHub repository URL when --source github.")
    fetch.add_argument("--slug", default="", help="Stable destination folder name.")
    fetch.add_argument("--out", required=True, help="Directory where reference evidence should be stored.")
    fetch.add_argument("--overwrite", action="store_true")
    fetch.set_defaults(func=command_fetch)

    analyze = subparsers.add_parser("analyze", help="Analyze an already fetched Skill directory.")
    analyze.add_argument("--path", required=True)
    analyze.add_argument("--json-out", default="")
    analyze.add_argument("--markdown", default="")
    analyze.set_defaults(func=command_analyze)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "fetch":
        if args.source == "local" and not args.path:
            parser.error("fetch --source local requires --path")
        if args.source == "github" and not args.url:
            parser.error("fetch --source github requires --url")
    try:
        return args.func(args)
    except Exception as exc:
        json_print(
            {
                "tool": "reference-skill",
                "action": args.command,
                "status": "error",
                "generated_at": utc_now(),
                "error": str(exc),
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
