#!/usr/bin/env python3
"""Validate lint, parser, diagram, smoke-test, and ClawHub bundle gates."""

from __future__ import annotations

import argparse
import configparser
import fnmatch
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, cast

try:
    import yaml
except ImportError:  # pragma: no cover - reported clearly at runtime
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "env", "ENV", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
URL_SAFE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".docx", ".ttf", ".otf", ".woff", ".woff2"}
TEXT_SUFFIXES = {
    "", ".css", ".cfg", ".csv", ".gitignore", ".gitattributes", ".html", ".ini", ".j2", ".js", ".json",
    ".md", ".mmd", ".ps1", ".py", ".sh", ".svg", ".toml", ".txt", ".yaml", ".yml",
}
SPECIAL_TEXT_FILES = {"LICENSE", "README", "SKILL.md", "QUALITY.md", "CLAW_HUB_PUBLISHING.md", ".clawhubignore"}
DEFAULT_CLAWHUBIGNORE_PATTERNS = [
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.ico", "*.pdf", "*.docx", "*.ipynb", "*.ttf", "*.otf", "*.woff", "*.woff2",
    "preview/", "output/", "__pycache__/", "*.py[cod]", "*$py.class", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/",
    ".venv/", "venv/", "env/", "ENV/", ".env", ".env.*", "secrets.json", "*_secret.ini", "*_local.ini", "*.tmp",
    ".DS_Store", "Thumbs.db", "desktop.ini",
]


def iter_files(*suffixes: str) -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in suffixes:
            files.append(path)
    return sorted(files)


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def run_ruff() -> None:
    if shutil.which("ruff"):
        run(["ruff", "check", "."])
        return
    if shutil.which("uvx"):
        run(["uvx", "ruff", "check", "."])
        return
    run([sys.executable, "-m", "ruff", "check", "."])


def compile_python() -> None:
    for path in iter_files(".py"):
        py_compile.compile(str(path), doraise=True)
    print("python compile ok")


def parse_structured_files() -> None:
    yaml_files = iter_files(".yaml", ".yml")
    yaml_module = cast(Any, yaml)
    if yaml_files and yaml_module is None:
        raise RuntimeError("PyYAML is required to parse YAML files")
    for path in yaml_files:
        yaml_module.safe_load(path.read_text(encoding="utf-8"))
    for path in iter_files(".json"):
        json.loads(path.read_text(encoding="utf-8"))
    for path in iter_files(".ini"):
        parser = configparser.RawConfigParser()
        with path.open(encoding="utf-8") as handle:
            parser.read_file(handle)
    print("structured files ok")


def mermaid_command() -> list[str] | None:
    if shutil.which("mmdc"):
        return ["mmdc"]
    return None


def validate_mermaid(skip: bool) -> None:
    diagrams = iter_files(".mmd")
    if not diagrams:
        print("mermaid skipped: no .mmd files")
        return
    cmd = mermaid_command()
    if skip or cmd is None:
        reason = "requested" if skip else "mmdc not available"
        print(f"mermaid skipped: {reason}")
        return
    with tempfile.TemporaryDirectory(prefix="skill-mermaid-") as tmp:
        out_dir = Path(tmp)
        for index, path in enumerate(diagrams, start=1):
            run([*cmd, "-i", str(path), "-o", str(out_dir / f"diagram-{index}.svg"), "-b", "white"])
    print("mermaid ok")


def smoke_generators() -> None:
    print("generator smoke skipped: discovery skill has no generate_*.py entry points")


def smoke_catalog_renderers() -> None:
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.exists():
        print("catalog smoke skipped: no scripts directory")
        return
    index_path = ROOT / "references" / "template-index.json"
    first_template = None
    if index_path.exists():
        templates = json.loads(index_path.read_text(encoding="utf-8")).get("templates", [])
        if templates:
            first_template = templates[0].get("id")
    path = scripts_dir / "render_discovery.py"
    if not path.exists():
        raise RuntimeError("scripts/render_discovery.py is required")
    run([sys.executable, str(path), "--list"])
    if first_template:
        run([sys.executable, str(path), "--template", first_template, "--var", "smoke=value", "--no-pdf"])
    print("catalog smoke ok")


def run_pyright() -> None:
    if not (ROOT / "pyrightconfig.json").exists():
        print("pyright skipped: no pyrightconfig.json")
        return
    if shutil.which("pyright"):
        run(["pyright"])
        return
    raise RuntimeError("pyrightconfig.json exists, but pyright is unavailable")


def frontmatter() -> dict[str, Any]:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise RuntimeError("SKILL.md must start with YAML frontmatter")
    yaml_module = cast(Any, yaml)
    if yaml_module is None:
        raise RuntimeError("PyYAML is required to parse SKILL.md frontmatter")
    data = yaml_module.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise RuntimeError("SKILL.md frontmatter must be a mapping")
    return data


def ignore_patterns() -> list[str]:
    ignore_file = ROOT / ".clawhubignore"
    if not ignore_file.exists():
        if (ROOT / ".git").exists():
            raise RuntimeError(".clawhubignore is required for ClawHub publishing")
        print("clawhub ignore defaults used: .clawhubignore is not present in this installed package")
        return DEFAULT_CLAWHUBIGNORE_PATTERNS.copy()
    patterns = []
    for raw in ignore_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def ignored(rel: str, patterns: list[str]) -> bool:
    rel = rel.replace("\\", "/")
    for pattern in patterns:
        negated = pattern.startswith("!")
        candidate = pattern[1:] if negated else pattern
        if candidate.endswith("/"):
            matched = rel == candidate[:-1] or rel.startswith(candidate)
        elif "/" in candidate:
            matched = fnmatch.fnmatch(rel, candidate)
        else:
            matched = fnmatch.fnmatch(Path(rel).name, candidate)
        if matched:
            return not negated
    return False


def publish_candidate_files(patterns: list[str]) -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in Path(rel).parts):
            continue
        if ignored(rel, patterns):
            continue
        files.append(path)
    return sorted(files)


def assert_dependency(openclaw: dict[str, Any], package: str) -> None:
    installs = openclaw.get("install") or []
    packages = {package_name(str(item.get("package", ""))) for item in installs if isinstance(item, dict)}
    if package.lower() not in packages:
        raise RuntimeError(f"metadata.openclaw.install must declare {package}")


def package_name(spec: str) -> str:
    return re.split(r"[<>=!~]", spec, 1)[0].strip().lower()


def validate_clawhub_bundle() -> None:
    data = frontmatter()
    name = data.get("name")
    version = data.get("version")
    metadata = data.get("metadata") or {}
    openclaw = metadata.get("openclaw") or {}
    for field in ["name", "description", "version"]:
        if not data.get(field):
            raise RuntimeError(f"SKILL.md frontmatter missing {field}")
    if not URL_SAFE_RE.fullmatch(str(name)):
        raise RuntimeError(f"skill name is not a URL-safe ClawHub slug: {name}")
    if not SEMVER_RE.fullmatch(str(version)):
        raise RuntimeError(f"version is not semver: {version}")
    if openclaw.get("skillKey") != name:
        raise RuntimeError("metadata.openclaw.skillKey must match name")
    homepage = openclaw.get("homepage")
    if not homepage or not str(homepage).startswith("https://github.com/CompleteTech-LLC/"):
        raise RuntimeError("metadata.openclaw.homepage must point to the CompleteTech GitHub repo")
    requires = openclaw.get("requires") or {}
    bins = requires.get("bins") or []
    if list(ROOT.glob("*.py")) or list((ROOT / "scripts").glob("*.py")):
        if "python3" not in bins:
            raise RuntimeError("Python-backed skills must declare requires.bins: python3")
    py_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in iter_files(".py"))
    if re.search(r"(?m)^\s*(?:from|import)\s+reportlab\b", py_text):
        assert_dependency(openclaw, "reportlab")
    if re.search(r"(?m)^\s*(?:from|import)\s+jinja2\b", py_text):
        assert_dependency(openclaw, "jinja2")
    if re.search(r"(?m)^\s*import\s+yaml\b", py_text):
        assert_dependency(openclaw, "pyyaml")

    patterns = ignore_patterns()
    for required_pattern in ["*.png", "*.pdf", "*.docx", "*.ttf", "preview/", "output/", ".env", "*.tmp"]:
        if required_pattern not in patterns:
            raise RuntimeError(f".clawhubignore missing required pattern: {required_pattern}")
    candidate_files = publish_candidate_files(patterns)
    for path in candidate_files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in BINARY_SUFFIXES:
            raise RuntimeError(f"binary file would be included in ClawHub bundle: {rel}")
        if path.name in SPECIAL_TEXT_FILES or path.suffix.lower() in TEXT_SUFFIXES:
            continue
        raise RuntimeError(f"non-text or unknown file would be included in ClawHub bundle: {rel}")
    license_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if "per-skill pricing" in license_text.lower() or "paid skill" in license_text.lower():
        raise RuntimeError("SKILL.md appears to contain unsupported ClawHub pricing language")
    if not (ROOT / "CLAW_HUB_PUBLISHING.md").exists():
        raise RuntimeError("CLAW_HUB_PUBLISHING.md is required")
    print(f"clawhub bundle ok ({len(candidate_files)} text files)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-mermaid", action="store_true", help="Skip Mermaid render validation when local tooling is unavailable.")
    args = parser.parse_args()

    compile_python()
    run_ruff()
    parse_structured_files()
    validate_mermaid(args.skip_mermaid)
    smoke_generators()
    smoke_catalog_renderers()
    run_pyright()
    validate_clawhub_bundle()
    print("quality validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
