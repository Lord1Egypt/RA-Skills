#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_mkdocs.py
================

Generic, parameterized renderer that converts any directory of Markdown files
into a static documentation website using **MkDocs** with the **Material** theme
and first-class **Mermaid** diagram rendering support.

Design goals (read carefully before modifying):
    * Sandbox isolation — all Python dependencies live inside a private
      `venv` created on the user's machine. Nothing leaks into the system
      Python or the user's global `site-packages`.
    * Fully parameterized — no hardcoded source/output paths. Everything is
      supplied through CLI arguments so that any agent or human can drive it.
    * Self-healing — the script will create the venv, install the required
      packages, generate the `mkdocs.yml`, copy the markdown tree, and run
      `mkdocs build`. If any step fails the script exits with a non-zero
      status code and a meaningful error message.
    * Mirrored installs — `pip` is forced to use the Aliyun mirror so that
      downloads are fast and reliable from within mainland China.

Usage:
    python3 render_mkdocs.py --src <markdown_dir> --out <output_dir>
    python3 render_mkdocs.py -s ./wiki -o ./mkdocs --force --clean

Required arguments:
    -s, --src   Source directory containing one or more `*.md` files. Sub
                directories are walked recursively; the relative structure
                becomes the navigation tree.
    -o, --out   Output directory. The static site will be written to
                `<out>/site`. A private virtual environment is created under
                `<out>/.venv` and the generated `mkdocs.yml` plus copied
                markdown live under `<out>/work`.

Optional flags:
    --force       Overwrite an existing `<out>` directory without prompting.
    --clean-venv  Re-create the virtual environment even if one already exists
                  (useful when dependency versions need to be refreshed).
    -h, --help    Show this help message and exit.

Exit codes:
    0 — build succeeded
    1 — invalid arguments / missing dependencies on the host
    2 — virtual environment creation failed
    3 — dependency installation failed
    4 — markdown discovery / copy failed
    5 — mkdocs build failed
"""

from __future__ import annotations

# Standard library only — no third-party imports here, because this script
# must run with the bare system Python before the venv exists.
import argparse
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List

# -----------------------------------------------------------------------------
# Configuration constants
# -----------------------------------------------------------------------------

# Aliyun PyPI mirror. The user explicitly requested this so that pip installs
# are fast and reliable from within China. The `--index-url` and
# `--trusted-host` flags are applied to every `pip install` invocation.
PIP_INDEX_URL = "https://mirrors.aliyun.com/pypi/simple"
PIP_TRUSTED_HOST = "mirrors.aliyun.com"

# Pinned, known-good versions. Pinning keeps builds reproducible across hosts
# and protects us from upstream API churn between releases of Material.
REQUIREMENTS = [
    "mkdocs==1.6.1",
    "mkdocs-material==9.5.49",
    "mkdocs-mermaid2-plugin==1.1.1",
    "pyyaml==6.0.2",  # Explicit transitive pin for stability on macOS arm64.
]

# Site title shown in the rendered Material header. Override via the
# environment variable `MKDOCS_SITE_NAME` if a custom value is desired.
SITE_NAME_DEFAULT = "Documentation"


# -----------------------------------------------------------------------------
# CLI parsing & validation
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments.

    The script is designed to be agent-friendly: running it with no
    arguments, or with missing required arguments, prints a descriptive
    error and the full `--help` block, then exits with a non-zero status.
    """
    parser = argparse.ArgumentParser(
        prog="render_mkdocs.py",
        description=(
            "Render a Markdown documentation collection into a static "
            "MkDocs site (Material theme + Mermaid diagrams). "
            "Creates an isolated Python venv, installs dependencies from "
            "the Aliyun PyPI mirror, generates mkdocs.yml, and runs "
            "`mkdocs build` to produce a self-contained static site."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Example:\n"
            "  python3 render_mkdocs.py \\\n"
            "      --src /path/to/wiki \\\n"
            "      --out /path/to/mkdocs_output\n"
            "\n"
            "Re-run with --force to overwrite an existing output directory:\n"
            "  python3 render_mkdocs.py -s ./wiki -o ./mkdocs --force\n"
        ),
    )
    parser.add_argument(
        "-s", "--src",
        required=True,
        type=Path,
        metavar="SRC_DIR",
        help=(
            "Source directory containing Markdown (*.md) files. "
            "Sub-directories are walked recursively and their relative "
            "paths become the navigation tree."
        ),
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=Path,
        metavar="OUT_DIR",
        help=(
            "Output directory. The final static site is written to "
            "<OUT_DIR>/site. A private virtual environment is created "
            "under <OUT_DIR>/.venv and intermediate files under "
            "<OUT_DIR>/work."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output directory without prompting.",
    )
    parser.add_argument(
        "--clean-venv",
        action="store_true",
        help=(
            "Re-create the isolated virtual environment even if one already "
            "exists. Useful when refreshing pinned dependency versions."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Run mkdocs build with --strict. Cross-reference warnings become "
            "hard errors. Off by default because real-world documentation "
            "trees commonly contain links to non-documentation files."
        ),
    )
    return parser.parse_args()


def fail(message: str, code: int = 1) -> "None":
    """Print an error message to stderr and exit with the given code.

    Centralizing failure handling keeps the main flow readable while still
    giving callers a deterministic exit-code taxonomy (see module docstring).
    """
    sys.stderr.write(f"[render_mkdocs] ERROR: {message}\n")
    sys.exit(code)


# -----------------------------------------------------------------------------
# Virtual environment & dependency installation
# -----------------------------------------------------------------------------

def create_virtualenv(venv_path: Path, clean: bool) -> Path:
    """Create an isolated Python virtual environment under `venv_path`.

    If a venv already exists and `clean` is False, the existing venv is
    reused (which makes subsequent runs much faster). When `clean` is True
    the directory is removed first to force a fresh install.
    """
    if venv_path.exists():
        if not clean:
            print(f"[render_mkdocs] Reusing existing venv at {venv_path}")
            return venv_path
        print(f"[render_mkdocs] Removing existing venv at {venv_path}")
        shutil.rmtree(venv_path)

    print(f"[render_mkdocs] Creating virtual environment at {venv_path}")
    builder = venv.EnvBuilder(
        with_pip=True,        # Ensure pip is bundled inside the venv.
        clear=True,          # Never inherit from an existing env at this path.
        symlinks=True,       # Smaller footprint; same Python runtime.
        upgrade_deps=False,  # Skip network call to upgrade pip; aliyun used instead.
    )
    try:
        builder.create(str(venv_path))
    except Exception as exc:  # pragma: no cover — defensive
        fail(f"Failed to create virtual environment: {exc}", code=2)

    if not venv_path.exists():
        fail(f"Virtual environment was not created at {venv_path}", code=2)
    return venv_path


def venv_python(venv_path: Path) -> Path:
    """Return the absolute path to the venv's python interpreter."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def install_dependencies(venv_path: Path) -> None:
    """Install MkDocs, Material theme, and the Mermaid plugin into the venv.

    Uses the Aliyun PyPI mirror and the `--trusted-host` flag (the mirror
    serves over HTTPS but the trusted-host flag prevents certificate
    warnings on hosts with stale CA bundles).
    """
    py = venv_python(venv_path)
    cmd = [
        str(py),
        "-m", "pip", "install",
        "--index-url", PIP_INDEX_URL,
        "--trusted-host", PIP_TRUSTED_HOST,
        "--disable-pip-version-check",
        "--no-cache-dir",
        *REQUIREMENTS,
    ]
    print("[render_mkdocs] Installing dependencies (Aliyun mirror):")
    for req in REQUIREMENTS:
        print(f"    - {req}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        fail(
            f"pip install failed (exit={exc.returncode}). "
            f"Command: {' '.join(cmd)}",
            code=3,
        )


# -----------------------------------------------------------------------------
# Markdown discovery & mkdocs.yml generation
# -----------------------------------------------------------------------------

def discover_markdown(src: Path) -> List[Path]:
    """Return a sorted list of all `*.md` files under `src` (recursive).

    Sorting is performed by POSIX path so the navigation order is stable
    across operating systems and shells.
    """
    if not src.exists():
        fail(f"Source directory does not exist: {src}", code=1)
    if not src.is_dir():
        fail(f"Source path is not a directory: {src}", code=1)

    md_files = sorted(src.rglob("*.md"), key=lambda p: str(p.relative_to(src)))
    if not md_files:
        fail(
            f"No Markdown (*.md) files were found under {src}. "
            "Nothing to render.",
            code=4,
        )
    return md_files


def copy_markdown(src: Path, docs_dir: Path, force: bool) -> List[Path]:
    """Copy the entire `src` tree into `docs_dir`, preserving relative paths.

    All files (not only Markdown) are copied so that image references and
    other static assets referenced from the markdown remain intact. If
    `force` is set, an existing `docs_dir` is removed first.
    """
    if docs_dir.exists():
        if not force:
            fail(
                f"Output work directory already exists: {docs_dir}. "
                "Re-run with --force to overwrite.",
                code=1,
            )
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True, exist_ok=True)

    print(f"[render_mkdocs] Copying source tree to {docs_dir}")
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src)
        dst = docs_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)

    md_files = sorted(docs_dir.rglob("*.md"), key=lambda p: str(p.relative_to(docs_dir)))
    return md_files


def build_nav(md_files: List[Path], docs_dir: Path) -> list:
    """Build a MkDocs `nav` structure from a list of markdown paths.

    Returns a nested list of `{section: [...]}` dicts / `{'file': path}` or
    `[title, path]` pairs. The hierarchy mirrors the directory structure of
    the source tree, which is the most predictable mapping for an agent.
    """
    nav: list = []
    for md in md_files:
        rel = md.relative_to(docs_dir).with_suffix("")
        title = rel.name.replace("_", " ").replace("-", " ").title()
        nav.append({title: str(rel).replace("\\", "/") + ".md"})
    return nav


def write_index_if_missing(docs_dir: Path, md_files: List[Path]) -> None:
    """Generate a top-level `index.md` landing page if none exists.

    Material/MkDocs without an `index.md` at the docs root does not produce
    a `site/index.html`, which leaves the rendered site without a clear
    entry point. This generates a minimal landing page that lists every
    discovered markdown file so a human reader can navigate from a single
    place. The file is only written when it does NOT already exist — never
    overwrites user content.
    """
    index_path = docs_dir / "index.md"
    if index_path.exists():
        return

    lines = ["# Documentation Index", ""]
    for md in md_files:
        rel = md.relative_to(docs_dir).as_posix()
        title = (
            md.stem.replace("_", " ").replace("-", " ").title()
        )
        lines.append(f"- [{title}]({rel})")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[render_mkdocs] Generated landing page at {index_path}")


def write_mkdocs_yml(work: Path, docs_dir: Path, nav: list) -> Path:
    """Generate `mkdocs.yml` at the work directory root.

    The configuration enables:
      * Material theme with中文+English language support and code copy.
      * The Mermaid2 plugin so that ```mermaid fenced blocks render to SVG
        at build time (no client-side JavaScript required).
      * Auto top-level navigation discovery as a fallback.

    The file is emitted via string templating rather than `yaml.safe_dump`
    because the mermaid2 plugin requires a Python-specific tag
    (`!!python/name:mermaid2.fence_mermaid`) inside the superfences
    custom_fences block. `safe_dump` cannot emit that tag without
    serializing it as a quoted string, which mkdocs would reject.
    """
    site_name = os.environ.get("MKDOCS_SITE_NAME", SITE_NAME_DEFAULT)
    import yaml  # Deferred import: PyYAML lives inside the venv's sys.path
                 # after install_dependencies() has run. Deferring keeps the
                 # script importable by the bare system Python before the
                 # venv exists (e.g. for --help).
    nav_yaml = yaml.safe_dump(nav, allow_unicode=True, sort_keys=False)
    docs_rel = docs_dir.relative_to(work).as_posix()

    config = f"""# AUTO-GENERATED by render_mkdocs.py — do not edit by hand.
site_name: {site_name}
docs_dir: {docs_rel}
use_directory_urls: true

theme:
  name: material
  language: zh
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - toc.follow
    - content.code.copy
    - content.code.annotate
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:mermaid2.fence_mermaid
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.snippets
  - toc:
      permalink: true
  - def_list
  - footnotes
  - tables
  - attr_list
  - md_in_html

plugins:
  - search
  - mermaid2

nav:
{nav_yaml}
"""
    yml_path = work / "mkdocs.yml"
    yml_path.write_text(config, encoding="utf-8")
    print(f"[render_mkdocs] Wrote config: {yml_path}")
    return yml_path


# -----------------------------------------------------------------------------
# Build execution
# -----------------------------------------------------------------------------

def run_mkdocs_build(venv_path: Path, work: Path, site_dir: Path, strict: bool) -> None:
    """Invoke `mkdocs build` to render the static site.

    The venv's mkdocs binary is used so we never touch the system. The
    output is forced into `<out>/site` regardless of any local config.

    Strict mode is OFF by default because real-world wiki trees commonly
    contain cross-references to source files that are not part of the
    documentation set; turning those into hard failures would make the
    renderer unusable on otherwise-valid input. Pass `strict=True` to
    surface every warning as an error (useful for CI gating).
    """
    py = venv_python(venv_path)
    cmd = [
        str(py),
        "-m", "mkdocs",
        "build",
        "--clean",
    ]
    if strict:
        cmd.append("--strict")
    cmd.extend(["--site-dir", str(site_dir)])
    print(f"[render_mkdocs] Running: {' '.join(cmd)} (cwd={work})")
    try:
        subprocess.run(cmd, check=True, cwd=str(work))
    except subprocess.CalledProcessError as exc:
        fail(
            f"mkdocs build failed (exit={exc.returncode}). "
            "See the output above for details.",
            code=5,
        )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

import os  # noqa: E402  — used lazily after potential venv sys.path tweaks.


def main() -> None:
    args = parse_args()
    src: Path = args.src.expanduser().resolve()
    out: Path = args.out.expanduser().resolve()

    # ----- Step 1: validate inputs -----------------------------------------
    if not src.exists():
        fail(f"Source directory does not exist: {src}", code=1)
    if not src.is_dir():
        fail(f"Source path is not a directory: {src}", code=1)

    # ----- Step 2: prepare output dirs ------------------------------------
    if out.exists() and any(out.iterdir()):
        if not args.force:
            fail(
                f"Output directory is not empty: {out}. "
                "Re-run with --force to overwrite.",
                code=1,
            )
        print(f"[render_mkdocs] Removing existing output directory: {out}")
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    venv_path = out / ".venv"
    work = out / "work"
    docs_dir = work / "docs"
    site_dir = out / "site"

    # ----- Step 3: create venv & install deps -----------------------------
    create_virtualenv(venv_path, clean=args.clean_venv)

    # Ensure the venv is on sys.path so the deferred `import yaml` inside
    # write_mkdocs_yml() resolves. Adding to sys.path is harmless when the
    # import already resolves.
    site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    if site_packages.exists():
        sys.path.insert(0, str(site_packages))

    # Install only if mkdocs isn't already importable in the venv.
    py = venv_python(venv_path)
    probe = subprocess.run(
        [str(py), "-c", "import mkdocs, material, mermaid2"],
        capture_output=True,
    )
    if probe.returncode != 0:
        install_dependencies(venv_path)

    # ----- Step 4: discover & copy markdown -------------------------------
    md_files = copy_markdown(src, docs_dir, force=True)
    write_index_if_missing(docs_dir, md_files)
    # Re-discover after a possible auto-generated index.md was written so
    # the navigation includes the landing page at the top.
    md_files = sorted(docs_dir.rglob("*.md"), key=lambda p: str(p.relative_to(docs_dir)))
    nav = build_nav(md_files, docs_dir)
    write_mkdocs_yml(work, docs_dir, nav)

    # ----- Step 5: build the static site ----------------------------------
    run_mkdocs_build(venv_path, work, site_dir, strict=args.strict)

    # ----- Step 6: summarize ---------------------------------------------
    index_html = site_dir / "index.html"
    if not index_html.exists():
        fail(
            f"Build reported success but {index_html} was not produced.",
            code=5,
        )
    print()
    print("[render_mkdocs] Build succeeded.")
    print(f"  Static site : {site_dir}")
    print(f"  Entry point : {index_html}")
    print(f"  Open with   : open {index_html}")
    print(f"  Serve with  : {py} -m mkdocs serve --config-file {work / 'mkdocs.yml'}")


if __name__ == "__main__":
    main()
