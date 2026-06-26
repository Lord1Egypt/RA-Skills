"""
Cutout.Pro Visual API Skill — Configuration Management

Manages: API Key, endpoint URLs, output directory.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── API Configuration ─────────────────────────────────────────────────────────

API_BASE = "https://www.cutout.pro"
USER_AGENT = "CutoutPro-Skill/1.0"

ENDPOINTS = {
    # Background Remover (mattingType=6)
    "bg_remover_binary": "/api/v1/matting",
    "bg_remover_base64": "/api/v1/matting2",
    "bg_remover_url": "/api/v1/mattingByUrl",
    # Face Cutout (mattingType=3)
    "face_cutout_binary": "/api/v1/matting",
    "face_cutout_base64": "/api/v1/matting2",
    "face_cutout_url": "/api/v1/mattingByUrl",
    # Photo Enhancer
    "photo_enhancer_binary": "/api/v1/photoEnhance",
    "photo_enhancer_base64": "/api/v1/photoEnhance2",
    "photo_enhancer_url": "/api/v1/photoEnhanceByUrl",
}

# mattingType mapping
MATTING_TYPE = {
    "bg-remover": 6,
    "face-cutout": 3,
}

# ── Output Configuration ──────────────────────────────────────────────────────

OUTPUT_SETTINGS = {
    "format": "png",
    "save_metadata": True,
}

# ── Utility Functions ─────────────────────────────────────────────────────────


def _parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse a .env file and return a key=value dictionary."""
    result: dict[str, str] = {}
    if not env_path.exists():
        return result
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and v:
                    result[k] = v
    except (OSError, UnicodeDecodeError):
        pass
    return result


def get_api_key() -> str | None:
    """Get the API Key in priority order: environment variable > .env file."""
    key = os.environ.get("CUTOUT_API_KEY")
    if key:
        return key
    env_data = _parse_env_file(ROOT_DIR / ".env")
    return env_data.get("CUTOUT_API_KEY")


def validate_image_file(filepath: str | Path) -> Path:
    """Validate that the image file exists and has a supported format."""
    supported = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    if path.suffix.lower() not in supported:
        raise ValueError(
            f"Unsupported format: {path.suffix}. Supported: {', '.join(supported)}"
        )
    if path.stat().st_size == 0:
        raise ValueError(f"File is empty: {path}")
    if path.stat().st_size > 15 * 1024 * 1024:
        raise ValueError(
            f"File too large ({path.stat().st_size / 1024 / 1024:.1f} MB). Maximum: 15 MB"
        )
    return path
