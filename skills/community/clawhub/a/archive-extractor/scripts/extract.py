#!/usr/bin/env python3
"""
Recursive Archive Extractor — Zero local-dependency edition
============================================================
Works on Windows, Linux, macOS with any Python 3.8+.
Does NOT call 7-Zip, unrar, or any other system executable.

Backends (all pure-Python):
  stdlib  : zip, tar, tar.gz, tar.bz2, tar.xz, tgz, gz, bz2, xz
  rarfile : .rar  (pip install rarfile  — pure-Python RAR parser)
  py7zr   : .7z   (pip install py7zr   — pure-Python 7-Zip reader)

Auto-installs rarfile / py7zr on first use; no other network calls.
"""

from __future__ import annotations

import argparse
import bz2
import gzip
import glob
import importlib
import logging
import lzma
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── Pure-Python optional backends ────────────────────────────────────────────

def _pip_install(package: str) -> bool:
    """Install *package* into the current interpreter's site-packages."""
    logger.info("Installing %s ...", package)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        importlib.invalidate_caches()
        return True
    except subprocess.CalledProcessError as exc:
        logger.warning("pip install %s failed: %s", package,
                       getattr(exc, "stderr", b"").decode(errors="replace").strip())
        return False


def _import_optional(import_name: str, pip_name: str):
    """Try to import *import_name*; auto-install via pip if missing. Returns module or None."""
    try:
        return importlib.import_module(import_name)
    except ImportError:
        pass
    if _pip_install(pip_name):
        importlib.invalidate_caches()
        try:
            return importlib.import_module(import_name)
        except ImportError:
            pass
    logger.warning("Could not load '%s' even after installing '%s'.", import_name, pip_name)
    return None


# Lazy-load: only triggered when the format is actually encountered.
_rarfile_mod = None   # pip: rarfile
_py7zr_mod   = None   # pip: py7zr

def _get_rarfile():
    global _rarfile_mod
    if _rarfile_mod is None:
        _rarfile_mod = _import_optional("rarfile", "rarfile")
        if _rarfile_mod is not None:
            # Tell rarfile NOT to call unrar (pure-Python mode)
            _rarfile_mod.UNRAR_TOOL = None
            _rarfile_mod.ALT_TOOL   = None
    return _rarfile_mod

def _get_py7zr():
    global _py7zr_mod
    if _py7zr_mod is None:
        _py7zr_mod = _import_optional("py7zr", "py7zr")
    return _py7zr_mod

# ─── Constants ─────────────────────────────────────────────────────────────────
MARKER_FILE = ".extracted_success"
MAX_DEPTH   = 20

# (suffix, handler_key)  — longest suffix first so ".tar.gz" wins over ".gz"
SUPPORTED_EXTS: list[tuple[str, str]] = [
    (".tar.gz",  "tar"),
    (".tar.bz2", "tar"),
    (".tar.xz",  "tar"),
    (".tgz",     "tar"),
    (".tbz2",    "tar"),
    (".tbz",     "tar"),
    (".tar",     "tar"),
    (".zip",     "zip"),
    (".rar",     "rar"),
    (".7z",      "7z"),
    (".gz",      "gz"),
    (".bz2",     "bz2"),
    (".xz",      "xz"),
]

# ─── Archive detection ─────────────────────────────────────────────────────────

def _match_ext(name_lower: str) -> tuple[str | None, str | None]:
    """Return (handler_key, stem) or (None, None)."""
    for ext, handler in SUPPORTED_EXTS:
        if name_lower.endswith(ext):
            stem = name_lower[: -len(ext)]
            return handler, (stem or name_lower + "_extracted")
    return None, None


def is_archive(path: Path) -> bool:
    if not path.is_file():
        return False
    handler, _ = _match_ext(path.name.lower())
    return handler is not None

# ─── Extraction helpers ────────────────────────────────────────────────────────

def _safe_tar_extract(tf: tarfile.TarFile, dest: Path) -> None:
    """Use 'data' filter on Python 3.12+ for security; fall back gracefully."""
    if hasattr(tarfile, "data_filter"):
        try:
            tf.extractall(dest, filter="data")
            return
        except TypeError:
            pass
    tf.extractall(dest)


def _extract_single_compressed(src: Path, dest_dir: Path, stem: str,
                                open_fn) -> None:
    """Generic single-file decompressor (.gz / .bz2 / .xz)."""
    out = dest_dir / stem
    with open_fn(src, "rb") as fin, open(out, "wb") as fout:
        shutil.copyfileobj(fin, fout)


def _extract_zip(src: Path, dest_dir: Path) -> None:
    if not zipfile.is_zipfile(src):
        raise ValueError(f"Not a valid ZIP file: {src.name}")
    with zipfile.ZipFile(src, "r") as zf:
        zf.extractall(dest_dir)


def _extract_tar(src: Path, dest_dir: Path) -> None:
    if not tarfile.is_tarfile(src):
        raise ValueError(f"Not a valid TAR file: {src.name}")
    with tarfile.open(src, "r:*") as tf:
        _safe_tar_extract(tf, dest_dir)


def _extract_rar(src: Path, dest_dir: Path) -> None:
    rf = _get_rarfile()
    if rf is None:
        raise RuntimeError(
            "rarfile not available — cannot extract .rar files. "
            "Run: pip install rarfile"
        )
    # rarfile pure-Python mode requires no external binary
    with rf.RarFile(str(src)) as archive:
        archive.extractall(str(dest_dir))


def _extract_7z(src: Path, dest_dir: Path) -> None:
    p7 = _get_py7zr()
    if p7 is None:
        raise RuntimeError(
            "py7zr not available — cannot extract .7z files. "
            "Run: pip install py7zr"
        )
    with p7.SevenZipFile(str(src), mode="r") as archive:
        archive.extractall(str(dest_dir))

# ─── Core extraction ───────────────────────────────────────────────────────────

def extract_archive(archive: Path, dest_parent: Path, force: bool) -> Path | None:
    """
    Extract *archive* into a subdirectory of *dest_parent*.
    Returns the output directory on success, None on failure.
    """
    handler, stem = _match_ext(archive.name.lower())
    if handler is None:
        return None

    out_dir = dest_parent / stem
    marker  = out_dir / MARKER_FILE

    # ── Idempotency ──
    if out_dir.exists():
        if not force and marker.exists():
            logger.info("[SKIP]   %s (already extracted)", archive.name)
            return out_dir
        if force:
            logger.info("[FORCE]  Cleaning %s", out_dir)
            shutil.rmtree(out_dir, ignore_errors=True)
        else:
            logger.info("[RESUME] Incomplete extraction: %s", archive.name)

    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info("[EXTRACT] %s  →  %s/", archive.name, out_dir.name)

    try:
        if handler == "zip":
            _extract_zip(archive, out_dir)

        elif handler == "tar":
            _extract_tar(archive, out_dir)

        elif handler == "rar":
            _extract_rar(archive, out_dir)

        elif handler == "7z":
            _extract_7z(archive, out_dir)

        elif handler == "gz":
            _extract_single_compressed(archive, out_dir, stem,
                                        lambda p, m: gzip.open(p, m))

        elif handler == "bz2":
            _extract_single_compressed(archive, out_dir, stem,
                                        lambda p, m: bz2.open(p, m))

        elif handler == "xz":
            _extract_single_compressed(archive, out_dir, stem,
                                        lambda p, m: lzma.open(p, m))

        else:
            logger.warning("Unknown handler '%s' for %s", handler, archive.name)
            return None

        marker.touch()
        logger.info("[OK]     %s", out_dir.name)
        return out_dir

    except Exception as exc:
        logger.error("[FAIL]   %s: %s", archive.name, exc)
        shutil.rmtree(out_dir, ignore_errors=True)
        return None

# ─── Recursive scanner ─────────────────────────────────────────────────────────

def process_dir(directory: Path, force: bool, depth: int = 0) -> None:
    """DFS: extract every archive, then recurse into extracted output."""
    if depth > MAX_DEPTH:
        logger.warning("Max recursion depth (%d) reached at %s", MAX_DEPTH, directory)
        return

    try:
        items = sorted(directory.iterdir())
    except (PermissionError, NotADirectoryError):
        return

    for item in items:
        if item.name == MARKER_FILE:
            continue
        if item.is_dir():
            process_dir(item, force, depth)
        elif item.is_file() and is_archive(item):
            out = extract_archive(item, item.parent, force)
            if out:
                process_dir(out, force, depth + 1)

# ─── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Recursive archive extractor — zero local-software dependency.\n"
            "Supports: zip, tar, tar.gz, tar.bz2, tar.xz, tgz, rar, 7z, gz, bz2, xz"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path",
                        help="File, directory, or glob pattern (e.g. 'downloads/', '*.rar')")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Re-extract even when a success marker exists")
    parser.add_argument("-d", "--dest", metavar="DIR",
                        help="Root output directory (default: alongside source file)")
    args = parser.parse_args()

    # ── Resolve targets ──
    if any(c in args.path for c in "*?[]"):
        targets = [Path(p) for p in glob.glob(args.path, recursive=True)]
    else:
        p = Path(args.path)
        if not p.exists():
            logger.error("Path not found: %s", args.path)
            sys.exit(1)
        targets = [p]

    if not targets:
        logger.warning("No matching targets for: %s", args.path)
        sys.exit(0)

    logger.info("Found %d target(s).", len(targets))

    dest_root = Path(args.dest) if args.dest else None
    if dest_root:
        dest_root.mkdir(parents=True, exist_ok=True)

    for target in targets:
        if target.is_dir():
            process_dir(target, args.force)
        elif target.is_file() and is_archive(target):
            parent = dest_root or target.parent
            out = extract_archive(target, parent, args.force)
            if out:
                process_dir(out, args.force)
        else:
            logger.warning("Skipping non-archive: %s", target.name)

    logger.info("Done.")


if __name__ == "__main__":
    main()
