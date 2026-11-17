"""Share project scanning, language detection, review-unit discovery and reporting using Python 3.11+."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
import re
import sys
from pathlib import Path

MINIMUM_PYTHON = (3, 11)
VALID_LANGS = ("auto", "c", "cpp", "rust", "python", "javascript", "go", "java")
MANIFEST_MARKERS = {
    "rust": ("Cargo.toml",),
    "python": ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile"),
    "javascript": ("package.json",),
    "go": ("go.mod",),
    "java": (
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "settings.gradle",
        "settings.gradle.kts",
    ),
}
NATIVE_BUILD_NAMES = (
    "CMakeLists.txt",
    "meson.build",
    "Makefile",
    "makefile",
    "vcpkg.json",
    "conanfile.py",
    "conanfile.txt",
)
BUILD_NAMES = set(NATIVE_BUILD_NAMES).union(*MANIFEST_MARKERS.values())
UNIT_LANGUAGE = {name: lang for lang, names in MANIFEST_MARKERS.items() for name in names}
SOURCE_SUFFIXES = {
    "c": {".c", ".h"},
    "cpp": {".c", ".h", ".cc", ".cpp", ".cxx", ".hpp", ".hh", ".hxx"},
    "rust": {".rs"},
    "python": {".py"},
    "javascript": {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts"},
    "go": {".go"},
    "java": {".java", ".kt", ".kts", ".scala"},
}
IGNORED_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        "node_modules",
        "target",
        "build",
        "builddir",
        "out",
        "dist",
        ".next",
        ".cache",
        "_deps",
        "third_party",
        "vendor",
    }
)
NON_PRODUCTION_PARTS = {
    "test",
    "tests",
    "testing",
    "fixture",
    "fixtures",
    "example",
    "examples",
    "sample",
    "samples",
    "doc",
    "docs",
    "bench",
    "benchmarks",
    "eval",
    "evals",
}
MAX_UNITS = 200


def python_version_error(
    version: tuple[int, ...] | None = None, executable: str | None = None
) -> str | None:
    """Explain an unsupported interpreter before a later import fails with a raw traceback."""
    version = tuple(sys.version_info[:3]) if version is None else tuple(version)
    if version[:2] >= MINIMUM_PYTHON:
        return None
    found = ".".join(str(part) for part in version[:3])
    return (
        f"CodeSift helpers require Python 3.11+; found {found} at "
        f"{executable or sys.executable}. Run them with a newer python3, or set "
        "CODESIFT_PYTHON=/path/to/python3.11 for the .sh entry points."
    )


def require_python() -> None:
    """Exit with the missing-prerequisite status (2) when the interpreter is too old."""
    message = python_version_error()
    if message:
        print(message, file=sys.stderr)
        raise SystemExit(2)


def positive_int(value: str) -> int:
    """Require a positive integer so invalid limits cannot silently bypass execution."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def scan_files(
    root: Path,
    limit: int = 10000,
    pruned: list[dict] | None = None,
    ignored: frozenset[str] | set[str] = IGNORED_DIRS,
) -> tuple[list[Path], list[str]]:
    """Scan regular files under explicit exclusions without following symbolic links.

    When a list is passed as pruned, every excluded directory is recorded with its reason
    so a report can show what the exclusion policy skipped.
    """
    files: list[Path] = []
    warnings: list[str] = []

    def on_error(error: OSError) -> None:
        """Expose traversal errors as coverage gaps instead of empty results."""
        warnings.append(f"scan error: {error}")

    for directory, dirs, names in os.walk(root, followlinks=False, onerror=on_error):
        kept = []
        for name in sorted(dirs):
            path = Path(directory) / name
            if path.is_symlink():
                reason = "symlink"
            elif name in ignored or name.startswith("cmake-build-"):
                reason = "default_exclude"
            else:
                kept.append(name)
                continue
            if pruned is not None:
                pruned.append({"path": path.relative_to(root).as_posix(), "reason": reason})
        dirs[:] = kept
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_symlink() or not path.is_file():
                warnings.append(
                    f"non-regular or symlink file excluded: {path.relative_to(root)}"
                )
                continue
            if len(files) >= limit:
                warnings.append(
                    f"file limit {limit} reached; narrow --root or raise --max-files"
                )
                return files, warnings
            files.append(path)
    return files, warnings


def native_language(root: Path, suffixes: set[str]) -> str | None:
    """Infer C or C++ from source suffixes and build declarations without guessing build logic."""
    if suffixes & (SOURCE_SUFFIXES["cpp"] - SOURCE_SUFFIXES["c"]):
        return "cpp"
    if ".c" in suffixes:
        return "c"
    cmake = root / "CMakeLists.txt"
    try:
        text = cmake.read_text(encoding="utf-8-sig") if cmake.is_file() else ""
    except (OSError, UnicodeError):
        return "cpp"  # The native inventory reports unreadable build declarations.
    text = re.sub(r"(?m)^\s*#.*$", "", text)
    match = re.search(r"\bproject\s*\(([^)]*)\)", text, re.I | re.S)
    explicit = match.group(1) if match else ""
    if re.search(r"\bCXX\b", explicit, re.I):
        return "cpp"
    if re.search(r"\bC\b", explicit):
        return "c"
    if match and "LANGUAGES" not in explicit.upper():
        return "cpp"  # Bare project(NAME) enables both C and CXX.
    if any(
        (root / name).is_file()
        for name in ("vcpkg.json", "conanfile.py", "conanfile.txt")
    ):
        return "cpp"
    return None


def detect_languages(root: Path, files: list[Path] | None = None) -> list[str]:
    """Prefer root manifests and report mixed packages instead of choosing a language arbitrarily."""
    langs = {
        lang
        for lang, names in MANIFEST_MARKERS.items()
        if any((root / name).is_file() for name in names)
    }
    has_native = any((root / name).is_file() for name in NATIVE_BUILD_NAMES)
    if has_native or not langs:
        if files is None:
            files, _ = scan_files(root)
        suffixes = {p.suffix.lower() for p in files}
        native = native_language(root, suffixes)
        if native:
            langs.add(native)
        if not langs:
            langs.update(
                lang
                for lang in ("python", "javascript", "rust", "go", "java")
                if suffixes & SOURCE_SUFFIXES[lang]
            )
    return sorted(langs)


def subtree_suffixes(root: Path, files: list[Path]) -> dict[Path, set[str]]:
    """Map every directory to the file suffixes beneath it in one pass over the scan."""
    table: dict[Path, set[str]] = defaultdict(set)
    for path in files:
        suffix = path.suffix.lower()
        for parent in path.parents:
            table[parent].add(suffix)
            if parent == root:
                break
    return table


def discover_units(root: Path, files: list[Path]) -> tuple[list[dict], bool]:
    """Group package and build manifests by directory so nested packages become review units.

    A nested native build file inside a native build tree that already has a detectable
    language belongs to that tree, so CMake subdirectories do not become separate units.
    """
    manifests: dict[Path, set[str]] = {}
    for path in files:
        if path.name in UNIT_LANGUAGE or path.name in NATIVE_BUILD_NAMES:
            manifests.setdefault(path.parent, set()).add(path.name)
    suffixes = subtree_suffixes(root, files)
    units: list[dict] = []
    native_roots: list[Path] = []
    for directory in sorted(
        manifests, key=lambda item: (len(item.relative_to(root).parts), str(item))
    ):
        names = manifests[directory]
        languages = {UNIT_LANGUAGE[name] for name in names if name in UNIT_LANGUAGE}
        if names & set(NATIVE_BUILD_NAMES) and not any(
            directory.is_relative_to(parent) for parent in native_roots
        ):
            native = native_language(directory, suffixes.get(directory, set()))
            if native:
                native_roots.append(directory)
                languages.add(native)
        if not languages:
            continue
        relative = directory.relative_to(root)
        unit = {
            "path": relative.as_posix(),
            "languages": sorted(languages),
            "manifests": sorted(names),
        }
        if NON_PRODUCTION_PARTS & {part.lower() for part in relative.parts}:
            unit["likely_non_production"] = True
        units.append(unit)
    units.sort(key=lambda unit: unit["path"])
    return units[:MAX_UNITS], len(units) > MAX_UNITS


def detect_lang(root: Path | None = None) -> str:
    """Return one detected package language or an explicit mixed or unknown result."""
    langs = detect_languages(root or Path.cwd())
    return langs[0] if len(langs) == 1 else ("mixed" if langs else "unknown")


def select_language(root: Path, requested: str) -> str:
    """Validate the language option and detect the package language only when requested."""
    if requested not in VALID_LANGS:
        raise ValueError(f"unsupported language: {requested}")
    return detect_lang(root) if requested == "auto" else requested


def add_project_arguments(parser: argparse.ArgumentParser) -> None:
    """Provide consistent project-root and language arguments for command-line helpers."""
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--lang", choices=VALID_LANGS, default="auto")


def print_text(text: str) -> None:
    """Print at the CLI boundary, escaping characters unsupported by the output stream."""
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding:
        text = text.encode(encoding, errors="backslashreplace").decode(encoding)
    print(text)


def print_report(report: dict, as_json: bool = False) -> None:
    """Render the same report as JSON or readable text without changing its meaning."""
    if as_json:
        print_text(json.dumps(report, indent=2, ensure_ascii=True))
        return
    for key, value in report.items():
        text = (
            json.dumps(value, ensure_ascii=True)
            if isinstance(value, (dict, list, bool))
            else value
        )
        print_text(f"{key}: {text}")


def markdown_report(report: dict, title: str) -> str:
    """Render a report as Markdown: scalar fields in a table, nested values as JSON blocks."""
    lines = [f"# {title}", "", "| Field | Value |", "|---|---|"]
    nested = []
    for key, value in report.items():
        if isinstance(value, (dict, list)):
            nested.append((key, value))
            continue
        text = json.dumps(value) if isinstance(value, bool) or value is None else str(value)
        escaped = text.replace("|", "\\|")
        lines.append(f"| {key} | {escaped} |")
    for key, value in nested:
        lines += ["", f"## {key}", "", "```json"]
        lines.append(json.dumps(value, indent=2, ensure_ascii=True))
        lines.append("```")
    return "\n".join(lines)
