"""
First-run setup for the OCR Document Extraction skill.

Checks Python dependencies and .env configuration, creates local config
templates when needed, and validates that the configured model is likely
a vision-capable (multi-modal) model.

This script never installs packages automatically. When dependencies are
missing it prints the exact `pip install` command for the current Python
interpreter so users can review and run it explicitly.

Usage:
    python scripts/ocr_setup.py           # interactive setup/check
    python scripts/ocr_setup.py --check   # non-interactive check only (exit 0 = ready, 1 = not ready)
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_REQUIREMENTS = _SKILL_ROOT / "requirements.txt"
_ENV_FILE = _SKILL_ROOT / ".env"
_ENV_EXAMPLE = _SKILL_ROOT / ".env.example"

REQUIRED_PACKAGES: list[tuple[str, str]] = [
    ("openai", "openai"),
    ("dotenv", "python-dotenv"),
    ("fitz", "PyMuPDF"),
    ("PIL", "Pillow"),
    ("pdf2image", "pdf2image"),
    ("markdown2", "markdown2"),
    ("docx", "python-docx"),
    ("bs4", "beautifulsoup4"),
    ("lxml", "lxml"),
    ("latex2mathml", "latex2mathml"),
    ("openpyxl", "openpyxl"),
    ("unicodeit", "unicodeit"),
]

REQUIRED_ENV_VARS = ["API_KEY", "BASE_URL", "VLM_MODEL"]


def mock_ocr_enabled() -> bool:
    """Return True when OCR responses are being mocked for local smoke tests."""
    return bool(
        (os.getenv("OCR_MOCK_RESPONSE_FILE") or "").strip()
        or (os.getenv("OCR_MOCK_RESPONSE_TEXT") or "").strip()
    )


def _is_placeholder_env_value(value: str | None) -> bool:
    """Return True when *value* looks like an unedited template placeholder."""
    if not value:
        return True
    lowered = value.strip().lower()
    placeholders = (
        "your-api-key-here",
        "https://your-api-endpoint/v1",
        "your-vision-model-here",
    )
    if lowered.startswith("your-"):
        return True
    return lowered in placeholders


def check_packages() -> list[str]:
    """Return list of missing pip package names."""
    missing = []
    for import_name, pip_name in REQUIRED_PACKAGES:
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pip_name)
    return missing


def python_install_command() -> str:
    """Return the explicit install command for the current interpreter."""
    return f'"{sys.executable}" -m pip install -r "{_REQUIREMENTS}"'


def check_env() -> list[str]:
    """Return list of missing environment variable names."""
    if mock_ocr_enabled():
        return []

    if _ENV_FILE.exists():
        from dotenv import dotenv_values
        values = dotenv_values(_ENV_FILE)
    else:
        values = {}

    missing = []
    for var in REQUIRED_ENV_VARS:
        val = os.getenv(var) or values.get(var)
        if _is_placeholder_env_value(val):
            missing.append(var)
    return missing


def bootstrap_env() -> None:
    """Create .env from .env.example if it doesn't exist."""
    if _ENV_FILE.exists():
        return
    if _ENV_EXAMPLE.exists():
        shutil.copy2(_ENV_EXAMPLE, _ENV_FILE)
        print(f"[setup] Created {_ENV_FILE} from template.")
    else:
        _ENV_FILE.write_text(
            "API_KEY=your-api-key-here\n"
            "BASE_URL=https://your-api-endpoint/v1\n"
            "VLM_MODEL=your-vision-model-here\n",
            encoding="utf-8",
        )
        print(f"[setup] Created {_ENV_FILE} with placeholder values.")


def find_soffice_binary() -> Path | None:
    """Return the local LibreOffice binary when available."""
    found = shutil.which("soffice")
    if found:
        return Path(found)

    for path in (
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
        "/usr/local/bin/soffice",
        "/snap/bin/soffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ):
        candidate = Path(path)
        if candidate.exists():
            return candidate

    return None


def check_system_deps() -> list[str]:
    """Check for optional but recommended system-level binaries."""
    missing = []
    if find_soffice_binary() is None:
        missing.append("LibreOffice (needed for DOC/DOCX/PPT/PPTX conversion)")
    if not (shutil.which("pdftoppm") or shutil.which("pdftocairo")):
        missing.append("Poppler (recommended for pdf2image fallback on difficult PDF pages)")
    return missing


def run_check() -> bool:
    """Run all checks silently. Returns True if the skill is ready to use."""
    ok = True

    pkg_missing = check_packages()
    if pkg_missing:
        print(f"[check] Missing packages: {', '.join(pkg_missing)}")
        ok = False

    env_missing = check_env()
    if env_missing:
        print(f"[check] Missing env vars: {', '.join(env_missing)}")
        ok = False

    if ok:
        print("[check] Skill is ready to use.")
    return ok


def run_setup() -> None:
    """Interactive first-run setup."""
    print("=" * 56)
    print("  OCR Document Extraction — First-Run Setup")
    print("=" * 56)

    # 1. Python packages
    missing_pkgs = check_packages()
    if missing_pkgs:
        print(f"\n[1/3] Missing Python packages: {', '.join(missing_pkgs)}")
        print("      Automatic installation is intentionally disabled.")
        print(f"      Please review and run manually:\n      {python_install_command()}")
    else:
        print("\n[1/3] Python dependencies — OK")

    # 2. .env file
    bootstrap_env()
    env_missing = check_env()
    if env_missing:
        print(f"\n[2/3] Please configure these in {_ENV_FILE}:")
        for var in env_missing:
            print(f"      - {var}")
        print()
        print("      IMPORTANT: This skill requires a VISION (multi-modal) model.")
        print("      The model must accept image inputs alongside text prompts.")
        print("      Please confirm with your provider that the model is vision-capable.")
        print("      Text-only models will NOT work.")
    else:
        print("\n[2/3] Environment configuration — OK")
        print("      NOTE: This skill requires a vision-capable (multi-modal) model")
        print("      that accepts image inputs alongside text prompts.")
        print("      Text-only models will NOT work.")

    # 3. System dependencies
    sys_missing = check_system_deps()
    if sys_missing:
        print(f"\n[3/3] Optional system dependencies not found:")
        for dep in sys_missing:
            print(f"      - {dep}")
        print("      (LibreOffice is needed for office documents; Poppler improves PDF fallback rendering)")
    else:
        print("\n[3/3] System dependencies — OK")

    print()
    if missing_pkgs:
        print("Setup incomplete. Install the missing Python packages, then re-run the check.")
    elif not env_missing:
        print("Setup complete. Ready to use!")
    else:
        print(f"Edit {_ENV_FILE} with your credentials, then you're ready.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OCR skill setup & dependency check.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Non-interactive check only (exit 0 = ready, 1 = not ready).",
    )
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if run_check() else 1)
    else:
        run_setup()
