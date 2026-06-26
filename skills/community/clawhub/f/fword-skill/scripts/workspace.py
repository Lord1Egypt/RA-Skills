"""Fword workspace — stores round-trip context for bidirectional conversion.

When converting Word → LaTeX, a .fword/ workspace is created to store:
  - The original .docx as a reference template (for style recovery)
  - Document metadata
  - Conversion history manifest
"""

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_DIR = ".fword"
MANIFEST_FILE = "manifest.json"
REFERENCE_DOC = "reference.docx"


def create_workspace(original_docx: Path, output_dir: Path | None = None) -> Path:
    """Create a .fword workspace from the original Word document."""
    if output_dir is None:
        output_dir = original_docx.parent
    workspace = output_dir / WORKSPACE_DIR
    workspace.mkdir(parents=True, exist_ok=True)

    # Save original docx as reference template
    shutil.copy2(original_docx, workspace / REFERENCE_DOC)

    # Extract basic metadata
    try:
        from docx import Document
        doc = Document(str(original_docx))
        props = doc.core_properties
        metadata = {
            "title": props.title or "",
            "author": props.author or "",
            "created": str(props.created or ""),
            "modified": str(props.modified or ""),
        }
    except Exception:
        metadata = {}

    manifest = {
        "version": "1",
        "original_file": original_docx.name,
        "metadata": metadata,
        "conversions": [],
    }
    (workspace / MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return workspace


def get_workspace(search_dir: Path) -> Path | None:
    """Find the .fword workspace in the given directory or parents."""
    search_dir = Path(search_dir).resolve()
    for d in [search_dir, *search_dir.parents]:
        ws = d / WORKSPACE_DIR
        if ws.is_dir() and (ws / MANIFEST_FILE).exists():
            return ws
    return None


def get_reference_doc(workspace: Path) -> Path | None:
    """Get the reference .docx from the workspace."""
    ref = workspace / REFERENCE_DOC
    return ref if ref.exists() else None


def record_conversion(workspace: Path, direction: str, input_file: str, output_file: str):
    """Record a conversion in the manifest."""
    manifest_path = workspace / MANIFEST_FILE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["conversions"].append({
        "direction": direction,
        "input": input_file,
        "output": output_file,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
