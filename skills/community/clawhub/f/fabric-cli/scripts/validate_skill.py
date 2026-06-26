#!/usr/bin/env python3
"""Validate the fabric-cli skill package structure.

This authoring helper checks common Agent Skill packaging issues without any
external dependencies. It is intentionally conservative and does not replace an
official skills-ref validator.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH_RE = re.compile(r"(?<![\w/.-])((?:references|scripts|assets|evals)/[A-Za-z0-9_./-]+)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_simple_yaml(frontmatter: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_map: dict[str, str] | None = None
    for raw in frontmatter.splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  ") and current_map is not None:
            if ":" not in raw:
                raise ValueError(f"Invalid nested frontmatter line: {raw!r}")
            key, value = raw.strip().split(":", 1)
            current_map[key.strip()] = value.strip().strip('"')
            continue
        current_map = None
        if ":" not in raw:
            raise ValueError(f"Invalid frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            current_map = {}
            data[key] = current_map
        else:
            data[key] = value.strip('"')
    return data


def add(result: list[dict[str, object]], ok: bool, check: str, detail: str = "") -> None:
    result.append({"ok": ok, "check": check, "detail": detail})


def validate(root: Path, run_script_help: bool) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    skill_md = root / "SKILL.md"
    add(results, skill_md.exists(), "SKILL.md exists", str(skill_md))
    if not skill_md.exists():
        return results

    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    add(results, bool(match), "SKILL.md has YAML frontmatter delimiters")
    if not match:
        return results

    try:
        fm = parse_simple_yaml(match.group(1))
        add(results, True, "frontmatter parses with simple validator")
    except Exception as exc:
        add(results, False, "frontmatter parses with simple validator", str(exc))
        return results

    name = str(fm.get("name", ""))
    desc = str(fm.get("description", ""))
    compat = str(fm.get("compatibility", "")) if "compatibility" in fm else ""
    add(results, bool(name), "name present")
    add(results, bool(NAME_RE.fullmatch(name)), "name is kebab-case lowercase alphanumeric", name)
    add(results, name == root.name, "name matches parent directory", f"name={name!r}, dir={root.name!r}")
    add(results, 1 <= len(desc) <= 1024, "description length is 1-1024 chars", f"length={len(desc)}")
    add(results, "Use this skill" in desc or "Use" in desc, "description has use/trigger phrasing")
    add(results, len(compat) <= 500, "compatibility length is at most 500 chars", f"length={len(compat)}")
    add(results, "<" not in match.group(1) and ">" not in match.group(1), "frontmatter contains no angle brackets")
    add(results, not (root / "README.md").exists(), "no root README.md inside skill folder")

    for path in sorted(root.glob("evals/*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            add(results, True, f"valid JSON: {path.relative_to(root)}")
        except Exception as exc:
            add(results, False, f"valid JSON: {path.relative_to(root)}", str(exc))

    docs = [skill_md] + sorted((root / "references").glob("*.md"))
    seen_paths: set[str] = set()
    for doc in docs:
        content = doc.read_text(encoding="utf-8")
        for link in LINK_RE.findall(content):
            if re.match(r"https?://|mailto:", link):
                continue
            seen_paths.add(link.split("#", 1)[0])
        for local in LOCAL_PATH_RE.findall(content):
            seen_paths.add(local)
    for rel in sorted(seen_paths):
        if not rel or rel.startswith("/"):
            continue
        add(results, (root / rel).exists(), f"referenced local path exists: {rel}")

    for script in sorted((root / "scripts").glob("*.py")):
        add(results, os.access(script, os.X_OK), f"script executable bit set: {script.relative_to(root)}")
        if run_script_help:
            try:
                proc = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, timeout=8, check=False)
                add(results, proc.returncode == 0 and "usage" in proc.stdout.lower(), f"script --help works: {script.relative_to(root)}")
            except Exception as exc:
                add(results, False, f"script --help works: {script.relative_to(root)}", str(exc))

    return results


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Fabric CLI Agent Skill package.")
    parser.add_argument("root", nargs="?", default=".", help="Skill root directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    parser.add_argument("--run-script-help", action="store_true", help="Run each script with --help.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    results = validate(root, args.run_script_help)
    ok = all(item["ok"] for item in results)
    if args.json:
        print(json.dumps({"ok": ok, "results": results}, indent=2, sort_keys=True))
    else:
        for item in results:
            mark = "PASS" if item["ok"] else "FAIL"
            detail = f" — {item['detail']}" if item.get("detail") else ""
            print(f"{mark}: {item['check']}{detail}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
