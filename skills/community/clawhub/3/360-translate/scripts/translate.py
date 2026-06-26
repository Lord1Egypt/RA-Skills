#!/usr/bin/env python3
"""360 AI Translation CLI — text, image, and document translation.

Usage:
  translate.py text   --tl <lang> [--sl <lang>] <text>...
  translate.py image  --tl <lang> (--url <url> | --file <path>) [--out <path>]
  translate.py doc    --tl <lang> --file <path> [--out <dir>] [--poll-interval <sec>] [--timeout <sec>]

Environment:
  TRANSLATE_360_API_KEY  — required API key

Examples:
  translate.py text --tl zh "Hello world" "Good morning"
  translate.py image --tl en --file photo.jpg --out translated.png
  translate.py doc --tl zh --file report.pdf --out ./output/
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import mimetypes
import uuid

API_BASE = "https://api.360.cn/v1"


def get_api_key():
    key = os.environ.get("TRANSLATE_360_API_KEY", "").strip()
    if not key:
        print("Error: TRANSLATE_360_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method, url, headers=None, data=None, json_data=None):
    """Make HTTP request using only stdlib."""
    if headers is None:
        headers = {}
    if json_data is not None:
        data = json.dumps(json_data).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
        except json.JSONDecodeError:
            err = {"raw": body}
        print(f"HTTP {e.code} error: {json.dumps(err, ensure_ascii=False, indent=2)}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def multipart_encode(fields, files):
    """Build multipart/form-data body using stdlib only."""
    boundary = uuid.uuid4().hex
    lines = []
    for key, value in fields.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"'.encode())
        lines.append(b"")
        lines.append(value.encode() if isinstance(value, str) else value)
    for key, (filename, filedata, content_type) in files.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode())
        lines.append(f"Content-Type: {content_type}".encode())
        lines.append(b"")
        lines.append(filedata)
    lines.append(f"--{boundary}--".encode())
    lines.append(b"")
    body = b"\r\n".join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


# ── Text Translation ──

def translate_text(api_key, texts, tl, sl=None):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"input": texts, "tl": tl}
    if sl:
        payload["sl"] = sl
    result = api_request("POST", f"{API_BASE}/translate", headers=headers, json_data=payload)
    if "error" in result:
        print(f"Error: {result['error'].get('message', result['error'])}", file=sys.stderr)
        sys.exit(1)
    return result.get("output", [])


# ── Image Translation ──

def translate_image(api_key, tl, url=None, file_path=None, out_path=None):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"model": "360/image-translate", "target_lang": tl}

    if url:
        payload["image_format"] = "url"
        payload["init_image"] = url
    elif file_path:
        with open(file_path, "rb") as f:
            raw = f.read()
        payload["image_format"] = "base64"
        payload["init_image"] = base64.b64encode(raw).decode("ascii")
    else:
        print("Error: provide --url or --file for image translation", file=sys.stderr)
        sys.exit(1)

    result = api_request("POST", f"{API_BASE}/images/translate", headers=headers, json_data=payload)

    if result.get("code") not in (0, "0"):
        print(f"Error: {result.get('message', result)}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {})
    res = data.get("res", {})
    img_urls = res.get("img_res", [])
    word_res = res.get("word_res", [])

    if not img_urls:
        print("No translated image returned.", file=sys.stderr)
        sys.exit(1)

    img_url = img_urls[0]

    # Download translated image
    if out_path:
        download_file(img_url, out_path)
        print(f"Translated image saved to: {out_path}")
    else:
        print(f"Translated image URL: {img_url}")

    if word_res:
        print(f"Extracted text: {word_res[0]}")

    return {"img_url": img_url, "word_res": word_res, "size": data.get("size"), "time_ms": data.get("time_cost_ms")}


# ── Document Translation ──

WORD_EXTENSIONS = {".doc", ".docx"}


def _is_word_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in WORD_EXTENSIONS


def _translate_doc_v2(api_key, file_path, tl, out_dir=None, poll_interval=5, timeout=3600):
    """Word (doc/docx) translation via deepdoc v2 API."""
    DOC_API = "https://api.360.cn/deepdoc/v2/translate"

    filename = os.path.basename(file_path)
    mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        file_data = f.read()

    body, content_type = multipart_encode({}, {"file": (filename, file_data, mime)})

    create_url = f"{DOC_API}?target_lang={urllib.parse.quote(tl)}&srcg=api"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
    }

    req = urllib.request.Request(create_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            upload_result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Upload failed (HTTP {e.code}): {err_body}", file=sys.stderr)
        sys.exit(1)

    task_id = upload_result.get("task_id") or upload_result.get("data", {}).get("task_id") or upload_result.get("data", {}).get("taskId")
    if not task_id:
        print(f"Upload error: no task_id in response: {json.dumps(upload_result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(f"Task created (deepdoc v2): {task_id}")

    start = time.time()
    while True:
        if time.time() - start > timeout:
            print(f"Timeout after {timeout}s", file=sys.stderr)
            sys.exit(1)

        time.sleep(poll_interval)
        poll_url = f"{DOC_API}?task_id={urllib.parse.quote(task_id)}&srcg=api"
        poll_headers = {"Authorization": f"Bearer {api_key}"}
        result = api_request("GET", poll_url, headers=poll_headers)

        status = result.get("status") or result.get("data", {}).get("state") or result.get("state") or "unknown"
        progress = result.get("progress") or result.get("data", {}).get("progress") or 0
        print(f"  Status: {status}, Progress: {progress}%")

        if status in ("success", "done", "completed", "finish"):
            download_url = (
                result.get("download_url")
                or result.get("data", {}).get("download_url")
                or result.get("data", {}).get("output", {}).get("data", {}).get("s3url")
                or result.get("url")
            )
            pages = result.get("pages") or result.get("data", {}).get("pages") or "?"

            if download_url:
                print(f"Done! Pages: {pages}")
                if out_dir:
                    os.makedirs(out_dir, exist_ok=True)
                    base = os.path.splitext(filename)[0]
                    out_file = os.path.join(out_dir, f"{base}_translated.pdf")
                    download_file(download_url, out_file)
                    print(f"Saved to: {out_file}")
                else:
                    print(f"Download URL: {download_url}")
                return {"download_url": download_url, "pages": pages}
            else:
                print(f"Done but no download URL found: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)

        elif status in ("fail", "failed", "error"):
            desc = result.get("message") or result.get("data", {}).get("message") or "Unknown error"
            print(f"Translation failed: {desc}", file=sys.stderr)
            sys.exit(1)


def _translate_doc_v1(api_key, file_path, tl, out_dir=None, poll_interval=5, timeout=3600):
    """Non-Word document translation via v1 API."""
    filename = os.path.basename(file_path)
    mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        file_data = f.read()

    body, content_type = multipart_encode({}, {"file": (filename, file_data, mime)})

    upload_url = f"{API_BASE}/documents/translate/upload?target_lang={urllib.parse.quote(tl)}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
    }

    req = urllib.request.Request(upload_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            upload_result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Upload failed (HTTP {e.code}): {err_body}", file=sys.stderr)
        sys.exit(1)

    if upload_result.get("errno", -1) != 0:
        print(f"Upload error: {upload_result.get('errmsg', upload_result)}", file=sys.stderr)
        sys.exit(1)

    task_id = upload_result["data"]["taskId"]
    print(f"Task created (v1): {task_id}")

    poll_headers = {"Authorization": f"Bearer {api_key}"}
    start = time.time()
    while True:
        if time.time() - start > timeout:
            print(f"Timeout after {timeout}s", file=sys.stderr)
            sys.exit(1)

        time.sleep(poll_interval)
        poll_url = f"{API_BASE}/documents/translate/result?task_id={urllib.parse.quote(task_id)}"
        result = api_request("GET", poll_url, headers=poll_headers)

        state = result.get("data", {}).get("state", "unknown")
        progress = result.get("data", {}).get("output", {}).get("progress", 0)
        print(f"  State: {state}, Progress: {progress}%")

        if state == "success":
            output = result["data"]["output"]["data"]
            s3url = output["s3url"]
            pages = output.get("pageCount", "?")
            trans_pages = output.get("transPageCount", "?")
            print(f"Done! Pages: {pages}, Translated pages: {trans_pages}")

            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                base = os.path.splitext(filename)[0]
                out_file = os.path.join(out_dir, f"{base}_translated.pdf")
                download_file(s3url, out_file)
                print(f"Saved to: {out_file}")
            else:
                print(f"Download URL: {s3url}")
            return {"s3url": s3url, "pages": pages, "trans_pages": trans_pages}

        elif state == "fail":
            desc = result.get("data", {}).get("output", {}).get("desc", "Unknown error")
            print(f"Translation failed: {desc}", file=sys.stderr)
            sys.exit(1)


def translate_doc(api_key, file_path, tl, out_dir=None, poll_interval=5, timeout=600):
    """Route to v2 (deepdoc) for Word files, v1 for everything else."""
    if _is_word_file(file_path):
        return _translate_doc_v2(api_key, file_path, tl, out_dir, poll_interval, timeout)
    else:
        return _translate_doc_v1(api_key, file_path, tl, out_dir, poll_interval, timeout)


def download_file(url, path):
    """Download a file from URL to local path."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(path, "wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)


# ── CLI ──

def main():
    parser = argparse.ArgumentParser(description="360 AI Translation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # text
    p_text = sub.add_parser("text", help="Translate text")
    p_text.add_argument("texts", nargs="+", help="Text(s) to translate")
    p_text.add_argument("--tl", required=True, help="Target language code")
    p_text.add_argument("--sl", help="Source language code (auto-detect if omitted)")

    # image
    p_img = sub.add_parser("image", help="Translate image")
    p_img.add_argument("--tl", required=True, help="Target language code")
    g = p_img.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="Image URL")
    g.add_argument("--file", help="Local image file path")
    p_img.add_argument("--out", help="Output path for translated image")

    # doc
    p_doc = sub.add_parser("doc", help="Translate document")
    p_doc.add_argument("--tl", required=True, help="Target language code")
    p_doc.add_argument("--file", required=True, help="Document file path")
    p_doc.add_argument("--out", help="Output directory")
    p_doc.add_argument("--poll-interval", type=int, default=5, help="Poll interval in seconds (default 5)")
    p_doc.add_argument("--timeout", type=int, default=3600, help="Max wait time in seconds (default 3600)")

    args = parser.parse_args()
    api_key = get_api_key()

    if args.command == "text":
        results = translate_text(api_key, args.texts, args.tl, args.sl)
        for i, (src, tgt) in enumerate(zip(args.texts, results)):
            if len(args.texts) > 1:
                print(f"[{i+1}] {src}")
                print(f"    → {tgt}")
            else:
                print(tgt)

    elif args.command == "image":
        translate_image(api_key, args.tl, url=args.url, file_path=args.file, out_path=args.out)

    elif args.command == "doc":
        translate_doc(api_key, args.file, args.tl, out_dir=args.out,
                      poll_interval=args.poll_interval, timeout=args.timeout)


if __name__ == "__main__":
    main()
