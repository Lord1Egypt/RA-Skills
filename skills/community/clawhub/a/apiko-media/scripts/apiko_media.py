#!/usr/bin/env python3
"""Generate images and videos with the APIKO API: submit async, poll, save the result.

Standard library only (Python 3.8+). The API key is read from APIKO_API_KEY and is
sent only to the APIKO API host; it is never printed or written to disk.

  python3 apiko_media.py image --model gpt-image-2.5-sunburst --prompt "..." --size 16:9 -o out.png
  python3 apiko_media.py image --model nano-banana-2.1 --prompt "..." --image ./product.jpg --resolution 2k
  python3 apiko_media.py video --model wan3.0-reference-video --prompt "Image 1 ..." \
      --ref-image ./character.png --ref-video https://example.com/style.mp4 --duration 5 --resolution 720p
  python3 apiko_media.py status task_abc123 -o out.mp4
  python3 apiko_media.py upload ./reference.png
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = os.environ.get("APIKO_BASE_URL", "https://api.apiko.app").rstrip("/")
USER_AGENT = "apiko-media-skill/1.0 (+https://apiko.app/)"
UPLOAD_MAX_BYTES = 10 * 1024 * 1024
UPLOAD_TYPES = {"image/jpeg", "image/png", "image/webp"}
DONE = {"completed", "failed"}


class ApiError(Exception):
    pass


def api_key():
    base = urllib.parse.urlsplit(API_BASE)
    if base.scheme != "https" and base.hostname not in ("127.0.0.1", "localhost"):
        raise ApiError(f"Refusing to send the API key to a non-HTTPS base URL: {API_BASE}")
    key = os.environ.get("APIKO_API_KEY", "").strip()
    if not key:
        raise ApiError("APIKO_API_KEY is not set. Create a key at https://apiko.app/ and export it.")
    return key


def is_api_host(url):
    return urllib.parse.urlsplit(url).netloc == urllib.parse.urlsplit(API_BASE).netloc


def request(method, url, body=None, content_type="application/json", timeout=120):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if is_api_host(url):
        headers["Authorization"] = "Bearer " + api_key()
    data = None
    if body is not None:
        data = json.dumps(body).encode() if content_type == "application/json" else body
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        raw = err.read().decode(errors="replace")
        try:
            msg = json.loads(raw).get("error", {}).get("message") or raw
        except ValueError:
            msg = raw
        raise ApiError(f"HTTP {err.code} from {urllib.parse.urlsplit(url).path}: {msg[:500]}")
    except urllib.error.URLError as err:
        raise ApiError(f"Network error calling {urllib.parse.urlsplit(url).path}: {err.reason}")


def upload(path):
    """Upload a local JPEG/PNG/WebP (free, kept 72 hours) and return its public URL."""
    size = os.path.getsize(path)
    if size > UPLOAD_MAX_BYTES:
        raise ApiError(f"{path} is {size / 1048576:.1f} MB; uploads are limited to 10 MB.")
    ctype = mimetypes.guess_type(path)[0] or ""
    if ctype not in UPLOAD_TYPES:
        raise ApiError(f"{path}: only JPEG, PNG or WebP can be uploaded (got {ctype or 'unknown type'}).")
    with open(path, "rb") as fh:
        res = request("POST", API_BASE + "/v1/uploads/images", fh.read(), content_type=ctype)
    if not res.get("url"):
        raise ApiError("Upload returned no URL.")
    return res["url"]


def as_url(ref):
    """Public HTTPS URLs pass through; local image files are uploaded first."""
    if ref.startswith("https://"):
        return ref
    if os.path.isfile(ref):
        url = upload(ref)
        print(f"uploaded {ref} -> {url}", file=sys.stderr)
        return url
    raise ApiError(f"{ref} is neither an https:// URL nor a local file.")


def result_url(task):
    for item in task.get("data") or []:
        if isinstance(item, dict) and item.get("url"):
            return item["url"]
    return task.get("video_url")


def poll(task_id, interval, timeout):
    deadline = time.time() + timeout
    last = None
    while True:
        task = request("GET", f"{API_BASE}/v1/tasks/{urllib.parse.quote(task_id)}", timeout=30)
        status = str(task.get("status", "")).lower()
        if status != last:
            print(f"{task_id}: {status} {task.get('progress', '')}".rstrip(), file=sys.stderr)
            last = status
        if status in DONE:
            return task
        if time.time() + interval > deadline:
            raise ApiError(
                f"Still {status} after {timeout} s. Do not resubmit (that would bill again); "
                f"check later with: apiko_media.py status {task_id}"
            )
        time.sleep(interval)


def save(url, out):
    headers = {"User-Agent": USER_AGENT}
    if is_api_host(url):
        headers["Authorization"] = "Bearer " + api_key()
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=300) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if not out:
            ext = mimetypes.guess_extension(ctype.split(";")[0].strip()) or ".bin"
            out = f"apiko-{time.strftime('%Y%m%d-%H%M%S')}{ext}"
        with open(out, "wb") as fh:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                fh.write(chunk)
    return out


def finish(task, out):
    if str(task.get("status")).lower() == "failed":
        raise ApiError(f"Task failed (refunded in full): {task.get('fail_reason') or 'no reason given'}")
    url = result_url(task)
    if not url:
        raise ApiError("Task completed but returned no result URL.")
    try:
        path = save(url, out)
    except (urllib.error.URLError, OSError) as err:
        raise ApiError(f"Task completed but the download failed ({err}). Result URL, valid for 24 hours: {url}")
    print(json.dumps({"task_id": task.get("id") or task.get("task_id"), "file": path, "url": url}))


def cmd_image(a):
    body = {"model": a.model, "prompt": a.prompt, "async": True}
    if a.resolution:
        body["resolution"] = a.resolution
    if a.size:
        body["size"] = a.size
    endpoint = "/v1/images/generations"
    if a.image:
        body["images"] = [as_url(r) for r in a.image]
        endpoint = "/v1/images/edits"
    job = request("POST", API_BASE + endpoint, body)
    print(f"submitted {job.get('id')}", file=sys.stderr)
    finish(poll(job["id"], a.interval or 5, a.timeout or 600), a.out)


def cmd_video(a):
    body = {"model": a.model, "prompt": a.prompt}
    for key, val in (("duration", a.duration), ("resolution", a.resolution), ("aspect_ratio", a.aspect_ratio)):
        if val is not None:
            body[key] = val
    if a.ref_image:
        body["reference_image_urls"] = [as_url(r) for r in a.ref_image]
    if a.ref_video:
        for r in a.ref_video:
            if not r.startswith("https://"):
                raise ApiError("Reference videos must be public https:// URLs (only images can be uploaded).")
        body["reference_videos"] = a.ref_video
    if a.callback_url:
        body["callback_url"] = a.callback_url
    job = request("POST", API_BASE + "/v1/videos", body)
    print(f"submitted {job.get('id')}", file=sys.stderr)
    finish(poll(job["id"], a.interval or 10, a.timeout or 1200), a.out)


def cmd_status(a):
    finish(poll(a.task_id, a.interval or 10, a.timeout or 1200), a.out)


def cmd_upload(a):
    print(upload(a.path))


def main():
    p = argparse.ArgumentParser(description="APIKO image and video generation (async submit, poll, save).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("-o", "--out", help="output file (default: apiko-<time>.<ext>)")
        sp.add_argument("--timeout", type=int, help="seconds to keep polling (image 600, video 1200)")
        sp.add_argument("--interval", type=int, help="seconds between polls (image 5, video 10)")

    im = sub.add_parser("image", help="text to image, or edit when --image is given")
    im.add_argument("--model", required=True)
    im.add_argument("--prompt", required=True)
    im.add_argument("--image", action="append", help="reference image: https URL or local file (repeatable)")
    im.add_argument("--resolution", help="e.g. 1k, 2k, 4k (Nano Banana)")
    im.add_argument("--size", help="aspect ratio such as 16:9, or a table size such as 1024x1024 (GPT Image)")
    common(im)
    im.set_defaults(func=cmd_image)

    vd = sub.add_parser("video", help="text, image or reference to video")
    vd.add_argument("--model", required=True)
    vd.add_argument("--prompt", required=True)
    vd.add_argument("--duration", type=int)
    vd.add_argument("--resolution", help="480p, 720p or 1080p")
    vd.add_argument("--aspect-ratio", dest="aspect_ratio", help="adaptive, 16:9, 9:16 or 1:1")
    vd.add_argument("--ref-image", action="append", help="reference image: https URL or local file (repeatable)")
    vd.add_argument("--ref-video", action="append", help="reference video https URL (repeatable; billed by length)")
    vd.add_argument("--callback-url", dest="callback_url")
    common(vd)
    vd.set_defaults(func=cmd_video)

    st = sub.add_parser("status", help="resume polling an existing task and save its result")
    st.add_argument("task_id")
    common(st)
    st.set_defaults(func=cmd_status)

    up = sub.add_parser("upload", help="upload a local JPEG/PNG/WebP and print its public URL")
    up.add_argument("path")
    up.set_defaults(func=cmd_upload)

    args = p.parse_args()
    try:
        args.func(args)
    except ApiError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
