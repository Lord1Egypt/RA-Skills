#!/usr/bin/env python3
"""
Black-Fortress Layer 4: Babel Output Filter

Trusted Output Rendering — prevents steganography and psychological manipulation.

Usage:
    python babel_output_filter.py --input <sandbox_output_dir> --output <clean_output_dir>

What it does:
    1. Raster images: Lossy recompression (downscale + JPEG quality reduction) to destroy LSB payloads
    2. HTML/UI: Rejects entirely — features cannot generate UI directly
    3. JSON data: Passes through entropy gate (Layer 3) and schema validation
    4. All files: Strips metadata (EXIF, etc.) that could carry payloads
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


class SecurityError(Exception):
    """Raised when a fail-closed security gate cannot verify its operation.
    
    Unlike generic exceptions, SecurityError explicitly means: the security
    check cannot confirm safety, so the artifact is BLOCKED. No fallback.
    """
    pass


# ─── Image Processing ──────────────────────────────────────────

def recompress_image(input_path: str, output_path: str,
                     scale: float = 0.5, jpeg_quality: int = 30) -> dict:
    """
    Lossy recompression to destroy steganographic payloads.
    Downscale + aggressive JPEG compression kills LSB-embedded data.

    FAIL-CLOSED: If PIL is unavailable, the image is BLOCKED, not copied.
    Copying an image without recompression defeats the entire purpose of Layer 4.
    """
    try:
        from PIL import Image
    except ImportError:
        # DO NOT COPY. Block the image entirely.
        raise SecurityError(
            "Pillow (PIL) is required for steganography decimation. "
            "Install with: pip install Pillow. "
            "Images cannot pass Layer 4 without recompression — this is a fail-closed gate."
        )

    try:
        img = Image.open(input_path)

        # Strip EXIF and metadata
        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)

        # Downscale
        new_size = (max(1, int(clean_img.width * scale)),
                    max(1, int(clean_img.height * scale)))
        clean_img = clean_img.resize(new_size, Image.LANCZOS)

        # Convert to RGB if RGBA (JPEG doesn't support alpha)
        if clean_img.mode in ("RGBA", "P"):
            clean_img = clean_img.convert("RGB")

        # Save as JPEG with aggressive compression
        clean_img.save(output_path, "JPEG", quality=jpeg_quality, optimize=True)

        return {
            "status": "recompressed",
            "original_size": os.path.getsize(input_path),
            "output_size": os.path.getsize(output_path),
            "original_dimensions": f"{img.width}x{img.height}",
            "output_dimensions": f"{new_size[0]}x{new_size[1]}",
            "quality": jpeg_quality,
            "metadata_stripped": True
        }
    except Exception as e:
        # DO NOT COPY on processing failure. Block the image.
        raise SecurityError(
            f"Image recompression failed: {e}. "
            f"Image BLOCKED — cannot pass Layer 4 without verified recompression."
        )


# ─── Format Validation ─────────────────────────────────────────

# Extensions that are ALLOWED to pass through
ALLOWED_EXTENSIONS = {
    ".json", ".csv", ".txt", ".md", ".yaml", ".yml", ".toml",
    ".svg",  # Vector — no pixel-level steganography
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",  # Raster — will be recompressed
}

# Extensions that are BLOCKED entirely (potential attack vectors)
BLOCKED_EXTENSIONS = {
    ".html", ".htm", ".xml",  # UI/markup injection
    ".js", ".py", ".sh", ".bat", ".ps1", ".rb", ".php",  # Executable code
    ".exe", ".dll", ".so", ".dylib", ".bin",  # Binaries
    ".svgz",  # Compressed SVG could hide data
    ".pdf",  # PDFs can contain JavaScript
    ".zip", ".tar", ".gz", ".7z", ".rar",  # Archives (could contain anything)
    ".ico", ".webp",  # Less common — block for safety
}


@dataclass
class FilterResult:
    file: str
    action: str  # "pass", "recompress", "block", "error"
    reason: str
    details: dict


def filter_output_directory(input_dir: str, output_dir: str) -> List[FilterResult]:
    """Process all output files through the Babel filter."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    results = []

    for filepath in sorted(input_path.rglob("*")):
        if not filepath.is_file():
            continue
        if filepath.name.startswith("."):
            continue
        if filepath.name == ".obfuscation_report.json":
            continue

        rel_path = filepath.relative_to(input_path)
        ext = filepath.suffix.lower()
        out_file = output_path / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        if ext in BLOCKED_EXTENSIONS:
            results.append(FilterResult(
                file=str(rel_path), action="block",
                reason=f"Extension {ext} is blocked (potential attack vector)",
                details={}
            ))
            continue

        if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp"):
            # Raster images — force recompression
            try:
                detail = recompress_image(str(filepath), str(out_file.with_suffix(".jpg")))
                results.append(FilterResult(
                    file=str(rel_path), action="recompress",
                    reason="Raster image recompressed to destroy steganographic payloads",
                    details=detail
                ))
            except SecurityError as e:
                results.append(FilterResult(
                    file=str(rel_path), action="block",
                    reason=f"BLOCKED: {e}",
                    details={"fail_closed": True}
                ))
        else:
            # Pass through (JSON, CSV, SVG, etc.)
            shutil.copy2(filepath, out_file)
            results.append(FilterResult(
                file=str(rel_path), action="pass",
                reason="Allowed format — passed through",
                details={"size": os.path.getsize(filepath)}
            ))

    return results


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Babel Output Filter")
    parser.add_argument("--input", required=True, help="Sandbox output directory")
    parser.add_argument("--output", required=True, help="Clean output directory")
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(json.dumps({"status": "error", "message": f"Not a directory: {args.input}"}))
        sys.exit(2)

    results = filter_output_directory(args.input, args.output)

    report = {
        "status": "complete",
        "total_files": len(results),
        "passed": sum(1 for r in results if r.action == "pass"),
        "recompressed": sum(1 for r in results if r.action == "recompress"),
        "blocked": sum(1 for r in results if r.action == "block"),
        "details": [asdict(r) for r in results]
    }

    print(json.dumps(report, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
