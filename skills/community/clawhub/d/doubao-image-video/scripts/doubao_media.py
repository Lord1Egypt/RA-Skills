#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_IMAGE_MODEL = os.getenv("DOUBAO_DEFAULT_IMAGE_MODEL", "doubao-seedream-4-5")
DEFAULT_VIDEO_MODEL = os.getenv("DOUBAO_DEFAULT_VIDEO_MODEL", "doubao-seedance-1.0-lite-t2v")
DEFAULT_IMAGE_ENDPOINT = os.getenv("DOUBAO_IMAGE_ENDPOINT_ID", "")
DEFAULT_VIDEO_ENDPOINT = os.getenv("DOUBAO_VIDEO_ENDPOINT_ID", "")


def fail(message, code=1, extra=None):
    payload = {"ok": False, "error": message}
    if extra is not None:
        payload["details"] = extra
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(code)


def request_json(method, url, api_key, body=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
            return {"http_status": resp.status, "body": parsed}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except Exception:
            parsed = {"raw": raw}
        fail(f"HTTP {e.code}", code=2, extra=parsed)
    except urllib.error.URLError as e:
        fail(f"request failed: {e.reason}", code=3)


def ensure_api_key():
    api_key = os.getenv("DOUBAO_API_KEY", "")
    if not api_key:
        fail("DOUBAO_API_KEY is required")
    return api_key


def append_video_flags(prompt, duration, fps, resolution):
    ratio = "16:9" if resolution == "720p" else "adaptive"
    text = prompt
    if "--dur" not in text:
        text += f" --dur {duration}"
    if "--fps" not in text:
        text += f" --fps {fps}"
    if "--rs" not in text:
        text += f" --rs {resolution}"
    if "--ratio" not in text:
        text += f" --ratio {ratio}"
    return text


def cmd_image(args):
    api_key = ensure_api_key()
    model_or_endpoint = args.endpoint_id or DEFAULT_IMAGE_ENDPOINT or args.model or DEFAULT_IMAGE_MODEL
    body = {
        "model": model_or_endpoint,
        "prompt": args.prompt,
        "size": args.size,
        "watermark": args.watermark,
    }
    if args.image_url:
        body["image_url"] = args.image_url
    if args.ref_image_url:
        body["ref_image_urls"] = args.ref_image_url
    if args.req_key:
        body["req_key"] = args.req_key
    result = request_json("POST", f"{BASE_URL}/images/generations", api_key, body)
    print(json.dumps({"ok": True, "kind": "image", "request": body, "response": result}, ensure_ascii=False))


def cmd_video(args):
    api_key = ensure_api_key()
    if len(args.prompt) > 500:
        fail("prompt must be <= 500 chars")
    model_or_endpoint = args.endpoint_id or DEFAULT_VIDEO_ENDPOINT or args.model or DEFAULT_VIDEO_MODEL
    content = [
        {
            "type": "text",
            "text": append_video_flags(args.prompt, args.video_duration, args.fps, args.resolution),
        }
    ]
    if args.first_frame_image_url:
        content.append({
            "type": "image_url",
            "image_url": {"url": args.first_frame_image_url},
        })
    for url in args.ref_image_url or []:
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
            "role": "reference_image",
        })
    body = {"model": model_or_endpoint, "content": content}
    if args.req_key:
        body["req_key"] = args.req_key
    result = request_json("POST", f"{BASE_URL}/contents/generations/tasks", api_key, body)
    print(json.dumps({"ok": True, "kind": "video", "request": body, "response": result}, ensure_ascii=False))


def fetch_task(api_key, task_id):
    encoded = urllib.parse.quote(task_id, safe="")
    return request_json("GET", f"{BASE_URL}/contents/generations/tasks/{encoded}", api_key)


def download_file(url, output_path):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)
        return {"path": output_path, "bytes": len(data)}
    except urllib.error.HTTPError as e:
        fail(f"download failed: HTTP {e.code}")
    except urllib.error.URLError as e:
        fail(f"download failed: {e.reason}")


def cmd_task(args):
    api_key = ensure_api_key()
    task_id = args.task_id.strip()
    if not task_id:
        fail("task_id is required")
    result = fetch_task(api_key, task_id)
    print(json.dumps({"ok": True, "kind": "task", "task_id": task_id, "response": result}, ensure_ascii=False))


def cmd_wait(args):
    api_key = ensure_api_key()
    task_id = args.task_id.strip()
    if not task_id:
        fail("task_id is required")
    deadline = time.time() + args.timeout
    attempts = 0
    last = None
    while True:
        attempts += 1
        last = fetch_task(api_key, task_id)
        body = last.get("body", {})
        status = body.get("status")
        if status in ("succeeded", "failed", "canceled"):
            result = {
                "ok": status == "succeeded",
                "kind": "wait",
                "task_id": task_id,
                "attempts": attempts,
                "status": status,
                "response": last,
            }
            video_url = ((body.get("content") or {}).get("video_url"))
            if status == "succeeded" and args.download_to and video_url:
                result["download"] = download_file(video_url, args.download_to)
            print(json.dumps(result, ensure_ascii=False))
            return
        if time.time() >= deadline:
            print(json.dumps({
                "ok": False,
                "kind": "wait",
                "task_id": task_id,
                "attempts": attempts,
                "status": status,
                "error": "timeout",
                "response": last,
            }, ensure_ascii=False))
            sys.exit(4)
        time.sleep(args.interval)


def build_parser():
    parser = argparse.ArgumentParser(description="Doubao native media skill helper")
    sub = parser.add_subparsers(dest="command")

    p_image = sub.add_parser("image", help="Generate image")
    p_image.add_argument("--prompt", required=True)
    p_image.add_argument("--endpoint-id")
    p_image.add_argument("--model")
    p_image.add_argument("--size", default="2560x1440")
    p_image.add_argument("--image-url")
    p_image.add_argument("--ref-image-url", action="append")
    p_image.add_argument("--req-key")
    p_image.add_argument("--watermark", action="store_true")
    p_image.set_defaults(func=cmd_image)

    p_video = sub.add_parser("video", help="Generate video task")
    p_video.add_argument("--prompt", required=True)
    p_video.add_argument("--endpoint-id")
    p_video.add_argument("--model")
    p_video.add_argument("--video-duration", type=int, default=5)
    p_video.add_argument("--fps", type=int, default=24)
    p_video.add_argument("--resolution", default="1080p")
    p_video.add_argument("--first-frame-image-url")
    p_video.add_argument("--ref-image-url", action="append")
    p_video.add_argument("--req-key")
    p_video.set_defaults(func=cmd_video)

    p_task = sub.add_parser("task", help="Query video task")
    p_task.add_argument("--task-id", required=True)
    p_task.set_defaults(func=cmd_task)

    p_wait = sub.add_parser("wait", help="Wait for video task completion")
    p_wait.add_argument("--task-id", required=True)
    p_wait.add_argument("--timeout", type=int, default=600)
    p_wait.add_argument("--interval", type=int, default=5)
    p_wait.add_argument("--download-to")
    p_wait.set_defaults(func=cmd_wait)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(2)
    args.func(args)


if __name__ == "__main__":
    main()
