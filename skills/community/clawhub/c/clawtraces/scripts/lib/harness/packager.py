# FILE_META
# INPUT:  iterable of HarnessFile(src, arc, scrub)
# OUTPUT: HarnessBundle(zip_bytes, scrub_report, file_count)
# POS:    skill lib harness — shared packaging core, called by each adapter's harness.py
# MISSION: Build a zip from a file manifest with optional PII scrubbing and uniform stats.

"""Generic harness zip packager.

Adapters declare *what files* go into the bundle via ``HarnessFile``; this
module handles zip construction, PII scrubbing, and scrub reporting.
"""

from __future__ import annotations

import io
import os
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    from lib.pii_scrubber import scrub_text_with_stats
except ImportError:  # allow running as scripts/lib/harness standalone
    from ..pii_scrubber import scrub_text_with_stats  # type: ignore


@dataclass(frozen=True)
class HarnessFile:
    """One entry in a harness bundle.

    Attributes:
        src: Absolute path on disk. If missing, the entry is silently skipped.
        arc: Relative path inside the resulting zip (e.g. ``config.yaml``,
            ``memory/notes.md``). Must use forward slashes.
        scrub: Whether to run PII scrubbing on the content. Binary files are
            detected by UTF-8 decode failure and stored as-is regardless.
    """

    src: Path
    arc: str
    scrub: bool = False


@dataclass
class HarnessBundle:
    zip_bytes: bytes
    file_count: int
    scrub_report: dict = field(default_factory=dict)


def _read_and_scrub(path: Path, scrub: bool) -> tuple[bytes, dict[str, int] | None]:
    """Read a file and optionally PII-scrub its text content.

    Returns ``(content_bytes, scrub_counts_or_None)``.
    ``scrub_counts_or_None`` is ``None`` when the file is treated as binary
    (no scrubbing possible) or when ``scrub`` is False.
    """
    raw = path.read_bytes()
    if not scrub:
        return raw, None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw, None
    scrubbed, counts = scrub_text_with_stats(text)
    return scrubbed.encode("utf-8"), counts


def build_bundle(files: Iterable[HarnessFile]) -> HarnessBundle:
    """Materialize a zip bundle from a file manifest.

    Missing source files are silently skipped (adapters commonly declare
    optional files). Empty bundles produce ``file_count=0`` but still return
    a valid (empty) zip — callers decide whether to upload.
    """
    buf = io.BytesIO()
    files_scrubbed: list[dict] = []
    totals: dict[str, int] = {}
    count = 0

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in files:
            if not entry.src.is_file():
                continue
            try:
                content, counts = _read_and_scrub(entry.src, entry.scrub)
            except OSError:
                continue
            zf.writestr(entry.arc, content)
            count += 1
            if counts:
                files_scrubbed.append({"file": entry.arc, "redactions": counts})
                for k, v in counts.items():
                    totals[k] = totals.get(k, 0) + v

    report: dict = {}
    if files_scrubbed:
        report = {
            "files_scrubbed": files_scrubbed,
            "total_redactions": sum(totals.values()),
            "by_category": totals,
        }

    return HarnessBundle(zip_bytes=buf.getvalue(), file_count=count, scrub_report=report)


def walk_directory(root: Path, arc_prefix: str, scrub: bool = True) -> list[HarnessFile]:
    """Helper: enumerate every file under ``root`` as HarnessFile entries.

    Adapters use this for "include the whole ~/.foo/ directory" semantics.
    Hidden files (``.git`` etc.) are kept; callers filter if needed.
    """
    if not root.is_dir():
        return []
    out: list[HarnessFile] = []
    for dirpath, _dirs, filenames in os.walk(root):
        for fname in filenames:
            full = Path(dirpath) / fname
            rel = full.relative_to(root).as_posix()
            out.append(HarnessFile(src=full, arc=f"{arc_prefix}/{rel}", scrub=scrub))
    return out
