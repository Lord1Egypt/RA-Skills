# -*- coding: utf-8 -*-
"""
BGM Manager — Background Music Library Management Tool

Manage BGM audio files in the assets/bgm/<style>/ directory structure.
Supports: upload, list, remove, validate, and info operations.

Usage:
    python bgm_manager.py list
    python bgm_manager.py list --style corporate
    python bgm_manager.py upload --file music.mp3 --style corporate
    python bgm_manager.py upload --file music.mp3 --style corporate --name track01.mp3
    python bgm_manager.py remove --style corporate --file track01.mp3
    python bgm_manager.py validate --file music.mp3
    python bgm_manager.py info
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BGM_CONFIG, PATHS_CONFIG


# ============================================================
# Audio Validation
# ============================================================

def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """Validate an audio file using ffprobe, with ffmpeg fallback.

    Uses a multi-tier approach (consistent with measure_audio_duration):
    1. ffprobe (most precise, if system ffprobe is functional)
    2. ffmpeg -i stderr parsing (works with bundled imageio-ffmpeg)
    3. Basic checks (extension + size) as last resort

    Returns: (is_valid, message)
    """
    import re

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ('.mp3', '.m4a', '.wav'):
        return False, f"Unsupported format: {ext}. Supported: .mp3, .m4a, .wav"

    # Check file size (at least 10KB)
    size = os.path.getsize(file_path)
    if size < 10240:
        return False, f"File too small ({size} bytes). Minimum: 10KB"

    # Tier 1: Try ffprobe to verify audio stream
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffprobe"], "-v", "error",
             "-show_entries", "format=duration,bit_rate",
             "-show_entries", "stream=codec_name,channels,sample_rate",
             "-of", "json",
             file_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            info = json.loads(result.stdout)
            duration = float(info.get("format", {}).get("duration", 0))
            if duration < 5.0:
                return False, f"Audio too short ({duration:.1f}s). Minimum: 5s"

            # Check for audio stream
            streams = info.get("streams", [])
            if not streams:
                return False, "No audio stream found"

            codec = streams[0].get("codec_name", "unknown")
            return True, f"Valid audio: {codec}, {duration:.1f}s, {size/1024:.0f}KB"
    except FileNotFoundError:
        pass  # ffprobe not installed, fall through to Tier 2
    except Exception:
        pass  # ffprobe failed, fall through to Tier 2

    # Tier 2: Use bundled ffmpeg -i to check if the file has valid audio
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffmpeg"], "-i", file_path, "-f", "null", "-",
             "-t", "0.1"],  # Only decode 0.1s to speed up validation
            capture_output=True, text=True, timeout=10
        )
        stderr = result.stderr
        # ffmpeg returns non-zero for invalid files, but also for files it can
        # partially read. Check for "Audio:" stream indicator in stderr.
        if "Audio:" in stderr:
            # Extract duration from stderr if available
            dur_match = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2}\.\d+)", stderr)
            if dur_match:
                h, m, s = dur_match.groups()
                duration = int(h) * 3600 + int(m) * 60 + float(s)
                if duration < 5.0:
                    return False, f"Audio too short ({duration:.1f}s). Minimum: 5s"
                return True, f"Valid audio (ffmpeg): {duration:.1f}s, {size/1024:.0f}KB"
            # No duration found but Audio: stream exists — accept it
            return True, f"Valid audio (ffmpeg): {size/1024:.0f}KB"
        else:
            return False, f"ffmpeg: no audio stream found in file"
    except FileNotFoundError:
        pass  # ffmpeg not available, fall through to Tier 3
    except Exception:
        pass  # ffmpeg validation failed, fall through to Tier 3

    # Tier 3: Basic validation (extension + size only, no codec verification)
    return True, f"Basic validation passed (no ffprobe/ffmpeg): {size/1024:.0f}KB, {ext}"


# ============================================================
# BGM Directory Operations
# ============================================================

def get_bgm_base_dir() -> str:
    """Get the BGM base directory path."""
    return os.path.join(PATHS_CONFIG["assets_dir"], "bgm")


def get_style_dir(style_name: str) -> str:
    """Get the directory path for a specific BGM style."""
    style_info = BGM_CONFIG["styles"].get(style_name)
    if not style_info:
        return ""
    return os.path.join(get_bgm_base_dir(), style_info["dir"])


def list_bgm_files(style_name: str = None) -> dict:
    """List all BGM files, optionally filtered by style.

    Returns: dict mapping style_name -> list of file info dicts
    """
    result = {}
    styles = BGM_CONFIG["styles"]

    if style_name:
        if style_name not in styles:
            print(f"Error: Unknown style '{style_name}'")
            return {}
        styles = {style_name: styles[style_name]}

    for name, info in styles.items():
        style_dir = get_style_dir(name)
        files = []
        if os.path.exists(style_dir):
            for f in sorted(os.listdir(style_dir)):
                if f.lower().endswith(('.mp3', '.m4a', '.wav')):
                    fpath = os.path.join(style_dir, f)
                    files.append({
                        "filename": f,
                        "path": fpath,
                        "size_kb": round(os.path.getsize(fpath) / 1024, 1),
                    })
        result[name] = {
            "label": info["label"],
            "dir": info["dir"],
            "volume": info["volume"],
            "files": files,
            "count": len(files),
        }

    return result


def upload_bgm_file(source_path: str, style_name: str, rename: str = None,
                    force: bool = False) -> Tuple[bool, str]:
    """Upload (copy) an audio file to a BGM style directory.

    Args:
        source_path: Path to the source audio file
        style_name: Target BGM style (e.g. "corporate", "cinematic")
        rename: Optional new filename (if None, use original filename)
        force: If True, overwrite existing file with the same name

    Returns: (success, message)
    """
    # Validate style
    if style_name not in BGM_CONFIG["styles"]:
        return False, f"Unknown style: '{style_name}'. Available: {list(BGM_CONFIG['styles'].keys())}"

    # Validate source file
    is_valid, msg = validate_audio_file(source_path)
    if not is_valid:
        return False, f"Validation failed: {msg}"

    # Determine target filename
    if rename:
        if not rename.lower().endswith(('.mp3', '.m4a', '.wav')):
            ext = os.path.splitext(source_path)[1]
            rename = rename + ext
        target_filename = rename
    else:
        target_filename = os.path.basename(source_path)

    # Ensure ASCII-safe filename for FFmpeg compatibility
    target_filename = target_filename.replace(' ', '_').replace('/', '_')

    # Copy file
    style_dir = get_style_dir(style_name)
    os.makedirs(style_dir, exist_ok=True)
    target_path = os.path.join(style_dir, target_filename)

    # Check for existing file
    if os.path.exists(target_path):
        if not force:
            return False, f"File already exists: {target_path}. Use --force to overwrite."
        os.remove(target_path)

    shutil.copy2(source_path, target_path)
    return True, f"Uploaded: {target_path} ({os.path.getsize(target_path)/1024:.0f}KB)"


def remove_bgm_file(style_name: str, filename: str) -> Tuple[bool, str]:
    """Remove a BGM file from a style directory.

    Args:
        style_name: BGM style directory name
        filename: Filename to remove

    Returns: (success, message)
    """
    if style_name not in BGM_CONFIG["styles"]:
        return False, f"Unknown style: '{style_name}'"

    style_dir = get_style_dir(style_name)
    file_path = os.path.join(style_dir, filename)

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    # Safety check: only allow audio file extensions
    if not filename.lower().endswith(('.mp3', '.m4a', '.wav')):
        return False, f"Refusing to remove non-audio file: {filename}"

    os.remove(file_path)
    return True, f"Removed: {file_path}"


def get_bgm_info() -> dict:
    """Get BGM configuration summary.

    Returns: dict with config info and file counts
    """
    base_dir = get_bgm_base_dir()
    styles_info = {}
    total_files = 0

    for name, info in BGM_CONFIG["styles"].items():
        style_dir = get_style_dir(name)
        file_count = 0
        total_size_kb = 0
        if os.path.exists(style_dir):
            for f in os.listdir(style_dir):
                if f.lower().endswith(('.mp3', '.m4a', '.wav')):
                    file_count += 1
                    total_size_kb += os.path.getsize(os.path.join(style_dir, f)) / 1024
        total_files += file_count
        styles_info[name] = {
            "label": info["label"],
            "dir": info["dir"],
            "volume": info["volume"],
            "file_count": file_count,
            "total_size_mb": round(total_size_kb / 1024, 1),
        }

    # Build type_bgm_map display
    type_map = {}
    for content_type, bgm_style in BGM_CONFIG["type_bgm_map"].items():
        type_map[content_type] = {
            "bgm_style": bgm_style,
            "style_label": BGM_CONFIG["styles"].get(bgm_style, {}).get("label", "?"),
        }

    return {
        "base_dir": base_dir,
        "auto_select": BGM_CONFIG["auto_select"],
        "default_style": BGM_CONFIG["default_style"],
        "total_files": total_files,
        "styles": styles_info,
        "type_bgm_map": type_map,
    }


# ============================================================
# CLI Output Formatting
# ============================================================

def print_list(files_info: dict):
    """Print BGM file listing in a readable format."""
    if not files_info:
        print("No BGM files found.")
        return

    for style_name, info in files_info.items():
        print(f"\n{'='*50}")
        print(f"  Style: {style_name} ({info['label']})")
        print(f"  Volume: {info['volume']}")
        print(f"  Files: {info['count']}")
        print(f"{'='*50}")
        if info["files"]:
            for f in info["files"]:
                print(f"    {f['filename']:30s}  {f['size_kb']:8.1f} KB")
        else:
            print("    (empty)")


def print_info(info: dict):
    """Print BGM configuration info in a readable format."""
    print(f"\n{'='*60}")
    print(f"  BGM Configuration Summary")
    print(f"{'='*60}")
    print(f"  Base directory: {info['base_dir']}")
    print(f"  Auto-select: {'enabled' if info['auto_select'] else 'disabled'}")
    print(f"  Default style: {info['default_style']}")
    print(f"  Total files: {info['total_files']}")
    print(f"\n  {'='*56}")
    print(f"  Style Directories:")
    print(f"  {'='*56}")
    for name, s in info["styles"].items():
        print(f"    {name:15s} ({s['label']})  vol={s['volume']:8s}  "
              f"files={s['file_count']}  size={s['total_size_mb']:.1f}MB")
    print(f"\n  {'='*56}")
    print(f"  Content Type → BGM Style Mapping:")
    print(f"  {'='*56}")
    for content_type, m in info["type_bgm_map"].items():
        print(f"    {content_type:15s} → {m['bgm_style']:15s} ({m['style_label']})")


# ============================================================
# Main Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="BGM Library Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = subparsers.add_parser("list", help="List BGM files")
    p_list.add_argument("--style", "-s", default=None,
                        choices=list(BGM_CONFIG["styles"].keys()),
                        help="Filter by style")

    # upload
    p_upload = subparsers.add_parser("upload", help="Upload audio file to BGM library")
    p_upload.add_argument("--file", "-f", required=True, help="Source audio file path")
    p_upload.add_argument("--style", "-s", required=True,
                         choices=list(BGM_CONFIG["styles"].keys()),
                         help="Target BGM style")
    p_upload.add_argument("--name", "-n", default=None, help="Rename file (without extension)")
    p_upload.add_argument("--force", action="store_true", help="Overwrite existing file")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove BGM file")
    p_remove.add_argument("--style", "-s", required=True,
                          choices=list(BGM_CONFIG["styles"].keys()),
                          help="BGM style directory")
    p_remove.add_argument("--file", "-f", required=True, help="Filename to remove")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate audio file")
    p_validate.add_argument("--file", "-f", required=True, help="Audio file path")

    # info
    subparsers.add_parser("info", help="Show BGM configuration summary")

    args = parser.parse_args()

    try:
        if args.command == "list":
            files_info = list_bgm_files(args.style)
            print_list(files_info)

        elif args.command == "upload":
            success, msg = upload_bgm_file(args.file, args.style, args.name,
                                           force=args.force)
            if success:
                print(f"OK: {msg}")
            else:
                print(f"ERROR: {msg}")
                sys.exit(1)

        elif args.command == "remove":
            success, msg = remove_bgm_file(args.style, args.file)
            if success:
                print(f"OK: {msg}")
            else:
                print(f"ERROR: {msg}")
                sys.exit(1)

        elif args.command == "validate":
            is_valid, msg = validate_audio_file(args.file)
            if is_valid:
                print(f"VALID: {msg}")
            else:
                print(f"INVALID: {msg}")
                sys.exit(1)

        elif args.command == "info":
            info = get_bgm_info()
            print_info(info)

        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
