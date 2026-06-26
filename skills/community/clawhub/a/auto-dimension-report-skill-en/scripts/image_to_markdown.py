#!/usr/bin/env python3
"""
Auto Dimension Report Skill - Image OCR Recognition Script v4
- Default: direct call to Herdsman HTTP API
- Fallback to external ocr.py on failure
- Supports batch processing, resume capability, and progress ETA
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib import error as urllib_error
from urllib import request as urllib_request


_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_DIR = _SCRIPT_DIR.parent
_WORKSPACE_SKILLS_DIR = _SKILL_DIR.parent
_CONFIG_FILE = _SCRIPT_DIR / "config.json"

DEFAULT_OCR_MODEL = "paddleocr-ppocrv5-server"
DEFAULT_BASE_URL = "http://127.0.0.1:8080"
SUPPORTED_IMAGE_EXTS = set([".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"])


def load_config():
    config = {
        "base_url": DEFAULT_BASE_URL,
        "ocr_model": DEFAULT_OCR_MODEL,
        "timeout": 120,
        "retry_count": 2,
        "retry_delay": 5,
        "ocr_script_dir": "",
        "transport": "auto",
    }
    if _CONFIG_FILE.exists():
        try:
            with open(_CONFIG_FILE, encoding="utf-8") as handle:
                data = json.load(handle)
            config["base_url"] = data.get("base_url", config["base_url"])
            config["ocr_model"] = data.get("ocr_model") or data.get("vl_model", config["ocr_model"])
            config["timeout"] = data.get("request_timeout", config["timeout"])
            config["retry_count"] = data.get("retry_count", config["retry_count"])
            config["retry_delay"] = data.get("retry_delay", config["retry_delay"])
            config["ocr_script_dir"] = (data.get("ocr_script_dir") or "").strip()
            config["transport"] = (data.get("ocr_transport") or config["transport"]).strip() or "auto"
        except (OSError, ValueError):
            pass

    env_url = os.environ.get("HERDSMAN_BASE_URL", "").strip()
    env_skill_dir = os.environ.get("HERDSMAN_SKILL_DIR", "").strip()
    env_transport = os.environ.get("HERDSMAN_OCR_TRANSPORT", "").strip()
    if env_url:
        config["base_url"] = env_url
    if env_skill_dir:
        config["ocr_script_dir"] = env_skill_dir
    if env_transport:
        config["transport"] = env_transport
    return config


def normalize_base_url(base_url):
    return (base_url or DEFAULT_BASE_URL).rstrip("/")


def build_ocr_candidates(config):
    candidates = []
    custom_dir = config.get("ocr_script_dir", "").strip()
    if custom_dir:
        candidates.append(Path(custom_dir))

    search_roots = [
        _WORKSPACE_SKILLS_DIR,
        Path.home() / ".openclaw" / "skills",
    ]
    for root in search_roots:
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            if child.is_dir():
                candidates.append(child)

    unique = []
    seen = set()
    for item in candidates:
        key = str(item).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def resolve_ocr_script(config):
    searched = []
    for skill_dir in build_ocr_candidates(config):
        script_path = skill_dir / "scripts" / "ocr.py"
        searched.append(script_path)
        if script_path.exists():
            return script_path, searched
    return None, searched


def find_images(image_dir):
    images = []
    for file_path in sorted(image_dir.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_IMAGE_EXTS:
            images.append(file_path)
    return images


def build_multipart_body(fields, file_field_name, file_path):
    boundary = "----AutoDimensionBoundary{0}".format(uuid.uuid4().hex)
    body = bytearray()
    for key, value in fields.items():
        body.extend(("--{0}\r\n".format(boundary)).encode("utf-8"))
        body.extend(('Content-Disposition: form-data; name="{0}"\r\n\r\n'.format(key)).encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    mime_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    filename = file_path.name
    body.extend(("--{0}\r\n".format(boundary)).encode("utf-8"))
    body.extend(
        (
            'Content-Disposition: form-data; name="{0}"; filename="{1}"\r\n'.format(
                file_field_name, filename
            )
        ).encode("utf-8")
    )
    body.extend(("Content-Type: {0}\r\n\r\n".format(mime_type)).encode("utf-8"))
    body.extend(file_path.read_bytes())
    body.extend(b"\r\n")
    body.extend(("--{0}--\r\n".format(boundary)).encode("utf-8"))
    return bytes(body), boundary


def extract_text_from_response(payload):
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, list):
        parts = [extract_text_from_response(item) for item in payload]
        parts = [item for item in parts if item]
        return "\n".join(parts).strip()
    if isinstance(payload, dict):
        for key in ["text", "content", "markdown", "result"]:
            value = payload.get(key)
            text = extract_text_from_response(value)
            if text:
                return text
        for key in ["data", "output", "choices", "items", "lines"]:
            value = payload.get(key)
            text = extract_text_from_response(value)
            if text:
                return text
    return ""


def http_ocr_image(image_path, config):
    url = normalize_base_url(config["base_url"]) + "/v1/ocr"
    last_error = ""
    for file_field in ["file", "image"]:
        body, boundary = build_multipart_body(
            {"model": config["ocr_model"]},
            file_field,
            image_path,
        )
        request = urllib_request.Request(
            url=url,
            data=body,
            headers={"Content-Type": "multipart/form-data; boundary={0}".format(boundary)},
            method="POST",
        )
        try:
            with urllib_request.urlopen(request, timeout=int(config.get("timeout", 120))) as response:
                payload = response.read().decode("utf-8", errors="replace")
        except urllib_error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            last_error = "HTTP {0}: {1}".format(exc.code, payload[:200])
            continue
        except Exception as exc:
            last_error = str(exc)
            continue

        try:
            decoded = json.loads(payload)
        except ValueError:
            if payload.strip():
                return payload.strip()
            last_error = "OCR HTTP returned empty"
            continue

        text = extract_text_from_response(decoded) or ""
        return text

    raise RuntimeError(last_error or "HTTP OCR call failed")


def script_ocr_image(image_path, ocr_script, config):
    if not ocr_script:
        raise RuntimeError("No fallback OCR script found")
    proc_env = os.environ.copy()
    proc_env["HERDSMAN_BASE_URL"] = normalize_base_url(config["base_url"])
    proc = subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(ocr_script),
            str(image_path),
            "--model",
            config["ocr_model"],
            "--json",
            "--timeout",
            str(int(config.get("timeout", 120))),
        ],
        capture_output=True,
        text=True,
        timeout=int(config.get("timeout", 120)) + 60,
        env=proc_env,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError((proc.stderr or "").strip() or (proc.stdout or "").strip() or "OCR subprocess execution failed")
    try:
        payload = json.loads(proc.stdout)
    except ValueError:
        return proc.stdout.strip()
    text = extract_text_from_response(payload) or ""
    return text


def ocr_image(image_path, config, ocr_script):
    retry_count = max(int(config.get("retry_count", 0)), 0)
    retry_delay = max(int(config.get("retry_delay", 0)), 0)
    transport = (config.get("transport") or "auto").lower()
    last_error = ""

    for attempt in range(retry_count + 1):
        try:
            if transport == "http":
                return http_ocr_image(image_path, config), "http"
            if transport == "script":
                return script_ocr_image(image_path, ocr_script, config), "script"
            try:
                return http_ocr_image(image_path, config), "http"
            except Exception as exc:
                last_error = str(exc)
                if ocr_script:
                    return script_ocr_image(image_path, ocr_script, config), "script"
                raise
        except Exception as exc:
            last_error = str(exc)
            if attempt < retry_count:
                time.sleep(retry_delay)

    raise RuntimeError(last_error or "OCR execution failed")


def select_pending_images(all_images, task_dir, imagetomd_dir, force):
    pending = []
    skipped = []
    for img_path in all_images:
        rel_to_image = img_path.relative_to(task_dir / "image")
        md_path = imagetomd_dir / rel_to_image.parent / (rel_to_image.name + ".md")
        if not force and md_path.exists():
            skipped.append((img_path, md_path))
        else:
            pending.append((img_path, md_path))
    return pending, skipped


def format_eta(seconds):
    if seconds is None:
        return "-"
    seconds = max(int(seconds), 0)
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return "{0}h{1:02d}m{2:02d}s".format(hours, minutes, secs)
    if minutes:
        return "{0}m{1:02d}s".format(minutes, secs)
    return "{0}s".format(secs)


def main():
    parser = argparse.ArgumentParser(description="Image OCR Recognition -> Markdown (Auto Dimension Report Skill v4)")
    parser.add_argument("--dir", "-d", required=True, help="Task folder path (parent of image/)")
    parser.add_argument("--force", action="store_true", help="Force re-process existing files")
    parser.add_argument("--model", default="", help="Override OCR model ID")
    parser.add_argument("--timeout", type=int, default=None, help="Override per-image request timeout (seconds)")
    parser.add_argument("--transport", choices=["auto", "http", "script"], default="", help="OCR transport method")
    parser.add_argument("--batch-size", type=int, default=0, help="Max N pending images to process this run; 0 = all")
    args = parser.parse_args()

    config = load_config()
    if args.model:
        config["ocr_model"] = args.model
    if args.timeout is not None:
        config["timeout"] = args.timeout
    if args.transport:
        config["transport"] = args.transport

    task_dir = Path(args.dir).resolve()
    if not task_dir.exists():
        print("[Error] Directory does not exist: {0}".format(task_dir), file=sys.stderr)
        sys.exit(1)

    image_dir = task_dir / "image"
    if not image_dir.exists():
        print("[Error] image/ directory not found: {0}".format(image_dir), file=sys.stderr)
        sys.exit(1)

    ocr_script, searched_paths = resolve_ocr_script(config)
    transport = (config.get("transport") or "auto").lower()
    if transport == "script" and not ocr_script:
        print("[Error] Transport set to script mode but no `scripts/ocr.py` found", file=sys.stderr)
        print("Searched paths:", file=sys.stderr)
        for item in searched_paths:
            print("  - {0}".format(item), file=sys.stderr)
        print("Set via `HERDSMAN_SKILL_DIR` env var or `ocr_script_dir` in config.json.", file=sys.stderr)
        sys.exit(1)

    imagetomd_dir = task_dir / "imagetomd"
    imagetomd_dir.mkdir(parents=True, exist_ok=True)

    all_images = find_images(image_dir)
    if not all_images:
        print("[Info] No supported image files found under image/")
        return

    pending, skipped = select_pending_images(all_images, task_dir, imagetomd_dir, args.force)
    total_pending_before_batch = len(pending)
    if args.batch_size and args.batch_size > 0:
        pending = pending[: args.batch_size]

    print("=" * 60)
    print("Auto Dimension Report Skill - Image OCR Recognition v4")
    print("=" * 60)
    print("Task directory: {0}".format(task_dir))
    print("Image directory: {0}".format(image_dir))
    print("Output directory: {0}".format(imagetomd_dir))
    print("OCR model: {0}".format(config["ocr_model"]))
    print("OCR URL: {0}".format(normalize_base_url(config["base_url"])))
    print("OCR transport: {0}".format(transport))
    print("Fallback script: {0}".format(ocr_script if ocr_script else "Not found"))
    print("Total images: {0}".format(len(all_images)))
    print("Skipped (existing): {0}".format(len(skipped) if not args.force else 0))
    print("Pending: {0}".format(len(pending)))
    if args.batch_size and total_pending_before_batch > len(pending):
        print("Batch limit: processing first {0} only, {1} remaining".format(len(pending), total_pending_before_batch - len(pending)))
    print("=" * 60)

    stats = {"success": 0, "skipped": len(skipped) if not args.force else 0, "failed": 0}
    start_all = time.time()
    processed_elapsed = []

    for index, item in enumerate(pending, start=1):
        img_path, md_path = item
        md_path.parent.mkdir(parents=True, exist_ok=True)
        rel = img_path.relative_to(task_dir)
        avg = (sum(processed_elapsed) / len(processed_elapsed)) if processed_elapsed else None
        remaining = len(pending) - index + 1
        eta = (avg * remaining) if avg is not None else None
        print("[{0}/{1}] Processing {2} | ETA {3}".format(index, len(pending), rel, format_eta(eta)))

        item_start = time.time()
        try:
            text, used_transport = ocr_image(img_path, config, ocr_script)
        except Exception as exc:
            elapsed = time.time() - item_start
            processed_elapsed.append(elapsed)
            stats["failed"] += 1
            print("    [Failed] {0:.1f}s -> {1}".format(elapsed, str(exc)[:200]), file=sys.stderr)
            continue

        elapsed = time.time() - item_start
        processed_elapsed.append(elapsed)
        with open(md_path, "w", encoding="utf-8") as handle:
            handle.write("# OCR Recognition Result\n\n")
            handle.write("Source file: `{0}`  \n".format(img_path.name))
            handle.write("Model: `{0}`  \n".format(config["ocr_model"]))
            handle.write("Engine URL: `{0}`  \n".format(normalize_base_url(config["base_url"])))
            handle.write("Transport: `{0}`  \n".format(used_transport))
            handle.write("Duration: {0:.1f}s  \n\n".format(elapsed))
            handle.write("---\n\n")
            handle.write(text if text else "(No text recognized)")
            handle.write("\n")

        stats["success"] += 1
        preview = (text or "")[:60].replace("\n", " ")
        print("    [Done] {0:.1f}s -> {1} chars: {2}{3}".format(
            elapsed, len(text or ""), preview, "..." if len(text or "") > 60 else ""
        ))

    total_elapsed = time.time() - start_all
    print()
    print("=" * 60)
    print("Processing complete:")
    print("  Success: {0} | Skipped: {1} | Failed: {2}".format(stats["success"], stats["skipped"], stats["failed"]))
    print("  Total images: {0}".format(len(all_images)))
    print("  Elapsed: {0}".format(format_eta(total_elapsed)))
    if processed_elapsed:
        print("  Average per image: {0:.1f}s".format(sum(processed_elapsed) / len(processed_elapsed)))
    if args.batch_size and total_pending_before_batch > len(pending):
        print("  Remaining: {0}".format(total_pending_before_batch - len(pending)))
    print("  Output directory: {0}".format(imagetomd_dir))
    print("=" * 60)


if __name__ == "__main__":
    main()
