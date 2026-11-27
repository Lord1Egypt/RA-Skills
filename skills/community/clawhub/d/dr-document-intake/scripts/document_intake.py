#!/usr/bin/env python3
"""Create traceable Markdown document extracts and audit workspace coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HEADER = "<!-- dr-document-intake "
SUFFIX = " -->"
DOCUMENTS = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".doc", ".ppt", ".odt", ".ods", ".odp", ".rtf", ".txt", ".md", ".csv", ".html", ".htm", ".eml", ".msg", ".zip", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".bmp"}
TEXT = {".txt", ".md", ".csv"}
UNSUPPORTED = {".doc", ".ppt", ".odt", ".ods", ".odp", ".rtf", ".zip", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".bmp"}
SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__", ".cache", ".trash", ".document-intake-quarantine", "skills", "context_pipeline"}
OPERATIONAL = {"AGENTS.md", "SOUL.md", "USER.md", "IDENTITY.md", "TOOLS.md", "HEARTBEAT.md", "MEMORY.md", "DREAMS.md", "BOOTSTRAP.md"}


def root_path(value: str) -> Path:
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("workspace must be an existing directory")
    return root


def relative_source(root: Path, value: str) -> tuple[Path, str]:
    p = Path(value).expanduser()
    if not p.is_absolute():
        p = root / p
    # Do not follow any symlink, even one pointing back into the workspace.
    lexical = Path(os.path.abspath(p))
    try:
        relative = lexical.relative_to(root)
    except ValueError as exc:
        raise ValueError("document is outside the workspace") from exc
    q = root
    for part in relative.parts:
        q = q / part
        if q.is_symlink():
            raise ValueError("symlinked documents require explicit review")
    if not lexical.is_file():
        raise ValueError("document does not exist or is not a regular file")
    if relative.parts[:2] == ("memory", "documents"):
        raise ValueError("derived extracts are not source documents")
    return lexical, relative.as_posix()


def digest(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def spreadsheet_cells(source: Path) -> tuple[str, list[str], int]:
    """List each populated XLSX cell, formula, cached value and comment."""
    try:
        import openpyxl
    except ImportError as exc:
        raise ValueError("openpyxl is required to verify XLSX extraction") from exc
    try:
        formulas = openpyxl.load_workbook(source, data_only=False)
        cached = openpyxl.load_workbook(source, data_only=True)
    except Exception as exc:
        raise ValueError(f"XLSX inspection failed: {type(exc).__name__}") from exc
    lines = ["## Complete spreadsheet cell listing"]
    limitations = []
    missing_formula_cache = 0
    cell_count = 0
    try:
        for sheet in formulas.worksheets:
            lines.append(f"\n### Sheet: {sheet.title}")
            values_sheet = cached[sheet.title]
            # openpyxl stores only materialized cells here. Iterating worksheet
            # dimensions can allocate millions of empty cells in sparse files.
            for coordinates, cell in sorted(sheet._cells.items()):
                if cell.value is None and cell.comment is None:
                    continue
                cell_count += 1
                lines.append(f"\nCell {cell.coordinate}:")
                if cell.value is not None:
                    if cell.data_type == "f" and hasattr(cell.value, "text"):
                        lines.append("Array formula: " + str(cell.value.text or ""))
                        lines.append("Formula range: " + str(cell.value.ref))
                    elif cell.data_type == "f" and not isinstance(cell.value, str):
                        lines.append("Formula attributes: " + json.dumps(dict(cell.value), ensure_ascii=False, sort_keys=True))
                    else:
                        lines.append(str(cell.value))
                if cell.data_type == "f":
                    cached_cell = values_sheet._cells.get(coordinates)
                    value = cached_cell.value if cached_cell is not None else None
                    if value is None:
                        missing_formula_cache += 1
                    else:
                        lines.append(f"Cached value: {value}")
                if cell.comment is not None:
                    lines.append("Comment:\n" + cell.comment.text)
            if sheet._images or sheet._charts:
                limitations.append(f"Sheet {sheet.title} contains images or charts requiring visual review")
        if missing_formula_cache:
            limitations.append(f"{missing_formula_cache} formula cells have no stored cached value")
    finally:
        formulas.close()
        cached.close()
    return "\n".join(lines), limitations, cell_count


def docx_missing_text(source: Path, content: str) -> tuple[str, list[str]]:
    """Recover Word body, header, footer, note and drawing text omitted by conversion."""
    word_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    drawing_ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    chart_ns = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
    normal = re.sub(r"\s+", "", content)
    missing = []
    limitations = []
    try:
        with zipfile.ZipFile(source) as package:
            names = package.namelist()
            parts = [n for n in names if re.fullmatch(r"word/(document|header[0-9]+|footer[0-9]+|footnotes|endnotes|comments)\.xml", n)]
            parts += [n for n in names if re.fullmatch(r"word/charts/chart[0-9]+\.xml", n)]
            for part in parts:
                root = ET.fromstring(package.read(part))
                values = []
                for paragraph in root.iter(word_ns + "p"):
                    values.append("".join(t.text or "" for t in paragraph.iter(word_ns + "t")).strip())
                values += [(t.text or "").strip() for t in root.iter(drawing_ns + "t")]
                if part.startswith("word/charts/"):
                    values += [(t.text or "").strip() for t in root.iter(chart_ns + "v")]
                for value in values:
                    compact = re.sub(r"\s+", "", value)
                    if compact and compact not in normal:
                        missing.append((part, value))
                        normal += compact
            if any(n.startswith("word/media/") and not n.endswith("/") for n in names):
                limitations.append("Document contains embedded images requiring visual review")
            if any(n.startswith("word/embeddings/") and not n.endswith("/") for n in names):
                limitations.append("Document contains embedded objects requiring separate extraction")
            if any(n.startswith("word/charts/") and n.endswith(".xml") for n in names):
                limitations.append("Document contains charts requiring visual review")
    except (OSError, zipfile.BadZipFile, ET.ParseError) as exc:
        raise ValueError(f"DOCX completeness inspection failed: {type(exc).__name__}") from exc
    if not missing:
        return "", limitations
    lines = ["## Additional document text"]
    for part, value in missing:
        lines.extend((f"\n### {part}", value))
    return "\n".join(lines), limitations


def target_path(root: Path, relative: str) -> Path:
    return root / "memory" / "documents" / (relative + ".md")


def has_symlink_ancestor(root: Path, p: Path) -> bool:
    for part in [p, *p.parents]:
        if part == root:
            return False
        if part.is_symlink():
            return True
    return True


def metadata(p: Path) -> dict | None:
    try:
        with p.open("r", encoding="utf-8") as f:
            line = f.readline().rstrip("\n")
        if not line.startswith(HEADER) or not line.endswith(SUFFIX):
            return None
        result = json.loads(line[len(HEADER):-len(SUFFIX)])
        return result if isinstance(result, dict) and result.get("version") == 1 else None
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def content_valid(p: Path, info: dict) -> bool:
    try:
        with p.open("r", encoding="utf-8") as f:
            f.readline()
            body = f.read()
        return hashlib.sha256(body.encode("utf-8")).hexdigest() == info.get("content_sha256")
    except (OSError, UnicodeError):
        return False


def inspect(root: Path, relative: str, source: Path) -> dict:
    if relative.startswith("memory/") and source.suffix.lower() == ".md":
        return {"source": relative, "status": "native_memory_markdown", "index_verified": False}
    out = target_path(root, relative)
    if has_symlink_ancestor(root, out):
        return {"source": relative, "status": "unsafe_extract", "index_verified": False}
    if not out.exists():
        return {"source": relative, "status": "missing", "index_verified": False}
    info = metadata(out)
    if not info or info.get("source") != relative:
        return {"source": relative, "status": "unmanaged_extract", "index_verified": False}
    if not content_valid(out, info):
        return {"source": relative, "status": "corrupt_extract", "index_verified": False}
    try:
        state = "fresh" if info.get("sha256") == digest(source) else "stale"
    except OSError:
        state = "unreadable_source"
    return {"source": relative, "extract": out.relative_to(root).as_posix(), "status": state, "index_verified": False}


def quarantine(root: Path, out: Path, relative: str) -> None:
    if not out.exists() or out.is_symlink():
        return
    info = metadata(out)
    if not info or info.get("source") != relative:
        raise ValueError("refusing to move an extract not owned by this helper")
    q = root / ".document-intake-quarantine"
    if q.is_symlink():
        raise ValueError("quarantine directory is a symlink")
    q.mkdir(mode=0o700, parents=True, exist_ok=True)
    if q.is_symlink() or not q.is_dir() or q.stat().st_uid != os.getuid():
        raise ValueError("quarantine must be a local directory owned by the current user")
    dest = q / (hashlib.sha256(relative.encode()).hexdigest() + "-" + str(time.time_ns()) + ".md")
    os.replace(out, dest)


def ingest(root: Path, value: str, markdown_from: str | None = None, source_sha256: str | None = None) -> dict:
    source, rel = relative_source(root, value)
    ext = source.suffix.lower()
    if ext not in DOCUMENTS:
        raise ValueError(f"unsupported document extension: {ext or '<none>'}")
    if rel.startswith("memory/") and ext == ".md":
        return {"source": rel, "status": "native_memory_markdown", "index_verified": False}
    out = target_path(root, rel)
    if has_symlink_ancestor(root, out):
        raise ValueError("extract path is a symlink")
    state = inspect(root, rel, source)
    if state["status"] == "unmanaged_extract":
        raise ValueError("extract path exists but is not managed by this helper")
    # Do not leave an old hash-indexed document searchable during failed refresh.
    if state["status"] in {"stale", "corrupt_extract"}:
        quarantine(root, out, rel)
    try:
        before = digest(source)
    except OSError:
        if out.exists() and metadata(out) and metadata(out).get("source") == rel:
            quarantine(root, out, rel)
        raise
    limitations: list[str] = []
    try:
        if markdown_from:
            if not source_sha256 or source_sha256 != before:
                raise ValueError("provided text requires the matching source hash captured before conversion")
            text_file = Path(markdown_from).expanduser()
            if text_file.is_symlink() or not text_file.is_file():
                raise ValueError("provided text must be a regular, non-symlink file")
            content = text_file.read_text(encoding="utf-8-sig")
        elif ext in UNSUPPORTED:
            raise ValueError(f"{ext} needs a suitable local converter or manual extraction")
        elif ext in TEXT:
            content = source.read_text(encoding="utf-8-sig")
        else:
            try:
                from markitdown import MarkItDown
            except ImportError as exc:
                raise ValueError("MarkItDown is not installed in this Python environment") from exc
            try:
                content = MarkItDown(enable_plugins=False).convert(str(source)).text_content
            except Exception as exc:
                raise ValueError(f"local conversion failed: {type(exc).__name__}") from exc
        if ext == ".xlsx":
            listing, limitations, cell_count = spreadsheet_cells(source)
            content = (content or "").rstrip()
            if content or cell_count:
                content = content + "\n\n" + listing
        elif ext == ".docx":
            extra, limitations = docx_missing_text(source, content or "")
            content = (content or "").rstrip()
            if extra:
                content = content + "\n\n" + extra
        if not content or not content.strip():
            raise ValueError("no text extracted; OCR or manual review may be required")
        if digest(source) != before:
            raise ValueError("original changed during extraction; retry")
    except (OSError, UnicodeError, ValueError):
        # A previously fresh output may have become stale while conversion ran.
        if out.exists() and not out.is_symlink():
            info = metadata(out)
            if info and info.get("source") == rel:
                try:
                    invalid = info.get("sha256") != digest(source)
                except OSError:
                    invalid = True
                if invalid:
                    quarantine(root, out, rel)
        raise
    # Check before creating directories; a symlink must never redirect writes.
    if has_symlink_ancestor(root, out.parent):
        raise ValueError("extract directory contains a symlink")
    out.parent.mkdir(parents=True, exist_ok=True)
    body = "\n" + content.rstrip() + "\n"
    hdr = json.dumps({"version": 1, "source": rel, "sha256": before, "content_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()}, ensure_ascii=True, separators=(",", ":"))
    data = HEADER + hdr + SUFFIX + "\n" + body
    fd, tmp = tempfile.mkstemp(prefix=".intake-", dir=out.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.chmod(tmp, source.stat().st_mode & 0o666)
        os.replace(tmp, out)
        try:
            after = digest(source)
        except OSError:
            quarantine(root, out, rel)
            raise
        if after != before:
            quarantine(root, out, rel)
            raise ValueError("original changed during publication; retry")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return {"source": rel, "extract": out.relative_to(root).as_posix(), "status": "extracted", "index_verified": False, "limitations": limitations}


def audit(root: Path) -> dict:
    items: list[dict] = []
    excluded: list[str] = []
    source_names: set[str] = set()
    output_root = root / "memory" / "documents"
    def walk_error(exc: OSError) -> None:
        items.append({"source": str(exc.filename), "status": "unreadable_directory", "index_verified": False})
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        current = Path(directory)
        keep = []
        for name in dirs:
            p = current / name
            if p.is_symlink():
                items.append({"source": p.relative_to(root).as_posix(), "status": "symlinked_directory_unscanned", "index_verified": False})
            elif name in SKIP_DIRS or name.startswith((".venv-", ".venv_")) or (current == root / "memory" and name in {".dreams", "dreaming"}):
                excluded.append(p.relative_to(root).as_posix())
            elif p != output_root:
                keep.append(name)
        dirs[:] = keep
        for name in files:
            p = current / name
            if p.suffix.lower() not in DOCUMENTS or (current == root and name in OPERATIONAL):
                continue
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                items.append({"source": rel, "status": "symlinked_document_unscanned", "index_verified": False})
                continue
            source_names.add(rel)
            item = inspect(root, rel, p)
            if item["status"] == "missing" and p.suffix.lower() in UNSUPPORTED:
                item["status"] = "unsupported"
            items.append(item)
    if output_root.is_dir() and not output_root.is_symlink():
        for directory, dirs, files in os.walk(output_root, followlinks=False, onerror=walk_error):
            current = Path(directory)
            for name in list(dirs):
                p = current / name
                if p.is_symlink():
                    items.append({"extract": p.relative_to(root).as_posix(), "status": "unsafe_extract_directory", "index_verified": False})
                    dirs.remove(name)
            for name in files:
                out = current / name
                if out.suffix.lower() != ".md":
                    continue
                if out.is_symlink():
                    items.append({"extract": out.relative_to(root).as_posix(), "status": "unsafe_extract", "index_verified": False})
                    continue
                info = metadata(out)
                if not info or not isinstance(info.get("source"), str):
                    items.append({"extract": out.relative_to(root).as_posix(), "status": "unmanaged_extract", "index_verified": False})
                elif info["source"] not in source_names:
                    try:
                        relative_source(root, info["source"])
                        state = "source_outside_audit_scope"
                    except ValueError:
                        state = "orphaned"
                    items.append({"source": info["source"], "extract": out.relative_to(root).as_posix(), "status": state, "index_verified": False})
    items.sort(key=lambda x: (x.get("source", ""), x.get("extract", "")))
    issues = [x for x in items if x["status"] not in {"fresh", "native_memory_markdown"}]
    return {"workspace": str(root), "items": items, "issue_count": len(issues), "excluded_directories": sorted(excluded), "scope_limitations": ["Only enumerated document extensions in the workspace were scanned; other types and external roots are unverified.", "Excluded operational directories were not scanned."], "index_verified": False}


def quarantine_extract(root: Path, value: str) -> dict:
    p = Path(value).expanduser()
    if not p.is_absolute():
        p = root / p
    p = Path(os.path.abspath(p))
    try:
        p.relative_to(root / "memory" / "documents")
    except ValueError as exc:
        raise ValueError("extract must be under memory/documents") from exc
    if has_symlink_ancestor(root, p) or not p.is_file():
        raise ValueError("extract must be a regular file without symlinked ancestors")
    info = metadata(p)
    if not info or not isinstance(info.get("source"), str) or target_path(root, info["source"]) != p:
        raise ValueError("extract is not managed by this helper")
    quarantine(root, p, info["source"])
    return {"source": info["source"], "status": "quarantined", "index_verified": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("ingest", "audit", "quarantine"):
        p = sub.add_parser(name)
        p.add_argument("--workspace", required=True)
        if name == "ingest":
            p.add_argument("source")
            p.add_argument("--markdown-from", help="local OCR/converter text file")
            p.add_argument("--source-sha256", help="source hash captured before creating the provided text")
        elif name == "quarantine":
            p.add_argument("extract")
    args = parser.parse_args()
    try:
        root = root_path(args.workspace)
        if args.command == "ingest":
            result = ingest(root, args.source, args.markdown_from, args.source_sha256)
        elif args.command == "quarantine":
            result = quarantine_extract(root, args.extract)
        else:
            result = audit(root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if args.command == "audit" and result["issue_count"] else 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc), "index_verified": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
