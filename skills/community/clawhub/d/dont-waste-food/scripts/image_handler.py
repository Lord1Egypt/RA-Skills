#!/usr/bin/env python3
"""
Dont Waste Food — Image Handler
Downloads or reads images for ingredient analysis.
Handles: local files, URLs, Telegram file paths.
"""
import os
import sys
import re
import urllib.request
import urllib.error

WORKSPACE = os.path.expanduser("~/.qclaw-oversea/workspace/dont-waste-food")
os.makedirs(WORKSPACE, exist_ok=True)


def download_image(url: str, timeout: int = 15) -> tuple:
    """
    Download an image from URL.
    Returns (local_path, error).
    """
    os.makedirs(f"{WORKSPACE}/images", exist_ok=True)
    filename = f"{WORKSPACE}/images/img_{os.getpid()}.jpg"

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; DontWasteFoodBot/1.0)"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type", "image/jpeg")
            ext = ".jpg" if "jpeg" in content_type or "jpg" in content_type else ".png"
            filename = filename.replace(".jpg", ext)
            with open(filename, "wb") as f:
                f.write(data)
            size = os.path.getsize(filename)
            if size < 500:
                os.remove(filename)
                return None, "File too small — not a valid image"
            return filename, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP error {e.code}: {url}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, f"Download error: {e}"


def save_base64_image(base64_data: str) -> tuple:
    """Save a base64-encoded image. Returns (path, error)."""
    import base64
    os.makedirs(f"{WORKSPACE}/images", exist_ok=True)
    filename = f"{WORKSPACE}/images/img_{os.getpid()}.jpg"
    try:
        # Remove data URL prefix if present
        if "," in base64_data:
            base64_data = base64_data.split(",", 1)[1]
        data = base64.b64decode(base64_data)
        with open(filename, "wb") as f:
            f.write(data)
        return filename, None
    except Exception as e:
        return None, f"Base64 decode error: {e}"


def is_telegram_file(path: str) -> bool:
    """Check if path is a Telegram file reference."""
    return path.startswith("/") and ("telegram" in path.lower() or "photo" in path.lower())


def is_url(path: str) -> bool:
    """Check if path is a URL."""
    return path.lower().startswith(("http://", "https://"))


def save_image(source: str) -> tuple:
    """
    Main entry point. Accepts:
    - A URL (https://...)
    - A local file path
    - A Telegram file path
    - A data: URL

    Returns (saved_path_or_None, error_or_None).
    """
    source = source.strip()

    if source.startswith("data:"):
        return save_base64_image(source)

    if is_url(source):
        return download_image(source)

    if os.path.exists(source):
        # Copy local file to workspace
        os.makedirs(f"{WORKSPACE}/images", exist_ok=True)
        ext = os.path.splitext(source)[1] or ".jpg"
        dest = f"{WORKSPACE}/images/img_{os.getpid()}{ext}"
        import shutil
        shutil.copy2(source, dest)
        return dest, None

    if is_telegram_file(source):
        if os.path.exists(source):
            import shutil
            os.makedirs(f"{WORKSPACE}/images", exist_ok=True)
            ext = os.path.splitext(source)[1] or ".jpg"
            dest = f"{WORKSPACE}/images/img_{os.getpid()}{ext}"
            shutil.copy2(source, dest)
            return dest, None
        return None, f"Telegram file not found: {source}"

    return None, f"Unknown image source: {source[:100]}"


def cleanup_old_images(max_age_hours: int = 1):
    """Remove images older than max_age_hours."""
    import time
    import shutil
    img_dir = f"{WORKSPACE}/images"
    if not os.path.exists(img_dir):
        return
    now = time.time()
    for fname in os.listdir(img_dir):
        fpath = os.path.join(img_dir, fname)
        if os.path.isfile(fpath):
            age = now - os.path.getmtime(fpath)
            if age > max_age_hours * 3600:
                os.remove(fpath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: image_handler.py <url|path>")
        sys.exit(1)

    source = sys.argv[1]
    path, err = save_image(source)
    if err:
        print(f"ERROR: {err}")
        sys.exit(1)
    else:
        print(f"OK: {path}")
        size = os.path.getsize(path)
        print(f"Size: {size} bytes")
