"""
OpenClaw Skill: File Router
============================
Single entry point for all incoming files.
Detects file type and dispatches to the correct skill.

This is the only skill you need to register in OpenClaw.
It calls the four individual skills internally.

Register in openclaw config as:
    skill_name: file_router
    trigger: [file_upload, attachment]
    entry: route_file(file_path)

File → Skill mapping:
    .pdf              → skill_pdf.process_pdf()
    .xlsx / .xls      → skill_excel.process_excel()
    .csv              → skill_csv.process_csv()
    .jpg / .jpeg / .png → skill_image.process_image()
"""

import json
from pathlib import Path

from skill_pdf   import process_pdf
from skill_excel import process_excel
from skill_csv   import process_csv
from skill_image import process_image


# ── ROUTING TABLE ─────────────────────────────────────────────────────────────

ROUTING_TABLE = {
    ".pdf":  process_pdf,
    ".xlsx": process_excel,
    ".xls":  process_excel,
    ".csv":  process_csv,
    ".jpg":  process_image,
    ".jpeg": process_image,
    ".png":  process_image,
}

SUPPORTED_EXTENSIONS = list(ROUTING_TABLE.keys())


# ── MAIN ENTRY POINT ─────────────────────────────────────────────────────────

def route_file(file_path: str) -> dict:
    """
    Detect file type and dispatch to the appropriate skill.

    Returns skill output dict, always including:
        {
          "file":      str,
          "skill_used": str,
          "success":   bool,
          ... (skill-specific fields)
        }
    """
    path = Path(file_path)

    if not path.exists():
        return _error(file_path, f"File not found: {file_path}")

    ext = path.suffix.lower()

    if ext not in ROUTING_TABLE:
        return _error(
            file_path,
            f"Unsupported file type: '{ext}'. "
            f"Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    skill_fn = ROUTING_TABLE[ext]
    skill_name = skill_fn.__module__  # e.g. "skill_pdf"

    try:
        result = skill_fn(file_path)
        result["skill_used"] = skill_name
        result["success"] = "error" not in result
        return result

    except Exception as e:
        return _error(file_path, f"Skill '{skill_name}' raised: {type(e).__name__}: {e}")


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _error(file_path: str, message: str) -> dict:
    return {
        "file": file_path,
        "success": False,
        "skill_used": None,
        "error": message,
    }


def get_supported_formats() -> list:
    """Returns list of supported file extensions."""
    return SUPPORTED_EXTENSIONS


# ── OPENCLAW SKILL METADATA ───────────────────────────────────────────────────

SKILL_METADATA = {
    "name": "file_router",
    "version": "1.0.0",
    "description": "Master router: detects file type and calls the correct processing skill.",
    "triggers": ["file_upload", "attachment", "any file received"],
    "entry_function": "route_file",
    "routes": ROUTING_TABLE,
}


# ── QUICK TEST ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python skill_router.py <file_path>")
        print(f"Supported: {', '.join(SUPPORTED_EXTENSIONS)}")
        sys.exit(1)

    result = route_file(sys.argv[1])
    # Print everything except large data fields
    skip_keys = {"text", "data", "sheets", "rows"}
    print(json.dumps(
        {k: v for k, v in result.items() if k not in skip_keys},
        indent=2
    ))
