#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = "https://ai.fun.tv"
DEFAULT_MODEL = "tencent-gpt-img-v2"
DEFAULT_TOKEN_FILE = Path(__file__).resolve().parents[1] / "authorization.txt"

MODEL_ALIASES = {
    "gpt": DEFAULT_MODEL,
    "gpt-image2": DEFAULT_MODEL,
    "fun-gp-image2": DEFAULT_MODEL,
    "tencent-gpt-img-v2": DEFAULT_MODEL,
    "fun-nb pro": "tencent-gem-banana-pro",
    "fun-nb 2.0": "tencent-gem-banana2",
    "即梦 5.0": "doubao-seedream-5.0",
    "即梦 4.5": "doubao-seedream-4.5",
    "即梦 4.0": "doubao-seedream-4.0",
    "qwen-image-2.0": "qwen-image-2.0",
    "wan 2.7": "wan2.7-image",
    "wan 2.6": "wan2.6-image",
}

VALID_RATIOS = {"16:9", "9:16", "4:3", "3:4", "1:1"}
VALID_CLARITY = {"1K", "2K", "4K"}


def normalize_model(model):
    return MODEL_ALIASES.get(model.strip().lower(), model.strip())


def read_saved_token(token_file):
    if token_file.exists():
        return token_file.read_text(encoding="utf-8").strip()
    return None


def save_token(token_file, token):
    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(token.strip() + "\n", encoding="utf-8")
    try:
        token_file.chmod(0o600)
    except OSError:
        pass


def request_json(method, path, token, body=None):
    data = None
    headers = {"authorization": token, "content-type": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        BASE_URL + path,
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {payload}") from exc

    result = json.loads(payload)
    if result.get("code") != 200:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    return result


def download_file(url, output_path):
    req = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        output_path.write_bytes(resp.read())


def create_project(token):
    result = request_json("POST", "/service/workflow/project/appbox/create", token, {"appId": 100100})
    return result["data"]["id"]


def submit_task(token, project_id, prompt, model, ratio, clarity, count):
    body = {
        "userProjectId": project_id,
        "tabAppCode": "text2image",
        "aspectRatio": ratio,
        "model": model,
        "clarity": clarity,
        "prompt": prompt,
        "imageCount": count,
    }
    result = request_json("POST", "/service/workflow/project/appbox/image/task", token, body)
    return result["data"]["taskId"]


def poll_result(token, project_id, task_id, interval, max_attempts):
    query = urllib.parse.urlencode({
        "page": 1,
        "pageSize": 50,
        "projectId": project_id,
        "tabAppCode": "text2image",
    })
    path = f"/service/workflow/resource/project/{project_id}?{query}"
    latest = None

    for _ in range(max_attempts):
        result = request_json("GET", path, token)
        content = result.get("data", {}).get("content", [])
        matches = [item for item in content if str(item.get("taskId")) == str(task_id)]
        latest = matches[0] if matches else (content[0] if content else None)

        if latest and latest.get("taskStatus") == "SUCCESS":
            urls = []
            for item in matches or content:
                data = item.get("data") or {}
                if data.get("url"):
                    urls.append(data["url"])
            if urls:
                return urls, latest
        time.sleep(interval)

    raise TimeoutError(json.dumps(latest or {}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Generate images with ai.fun.tv text-to-image API.")
    parser.add_argument("prompt", help="Image prompt")
    parser.add_argument("--authorization", help="JWT token; saved locally for later runs when provided")
    parser.add_argument("--token-file", default=str(DEFAULT_TOKEN_FILE), help="Local token file path")
    parser.add_argument("--no-save-authorization", action="store_true", help="Do not save a provided token")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model label, alias, or API value; GPT/GPT-image2 default to Fun-GP-image2")
    parser.add_argument("--ratio", default="16:9", choices=sorted(VALID_RATIOS))
    parser.add_argument("--clarity", default="1K", choices=sorted(VALID_CLARITY))
    parser.add_argument("--count", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--output-dir", help="Directory for downloaded images")
    parser.add_argument("--poll-interval", type=int, default=5)
    parser.add_argument("--max-attempts", type=int, default=120)
    args = parser.parse_args()

    token_file = Path(args.token_file).expanduser()
    saved_token = read_saved_token(token_file)
    authorization = args.authorization or os.getenv("AI_FUN_TV_AUTHORIZATION") or saved_token

    if not authorization:
        print("缺少 ai.fun.tv 鉴权 token。请打开 https://ai.fun.tv/openclaw 登录并获取 token，然后通过 --authorization 传入。", file=sys.stderr)
        return 2
    if authorization.lower().startswith("bearer "):
        print("authorization 必须是原始 JWT，不要添加 Bearer 前缀。", file=sys.stderr)
        return 2

    if args.authorization and not args.no_save_authorization:
        save_token(token_file, authorization)

    model = normalize_model(args.model)
    project_id = create_project(authorization)
    task_id = submit_task(authorization, project_id, args.prompt, model, args.ratio, args.clarity, args.count)
    urls, latest = poll_result(authorization, project_id, task_id, args.poll_interval, args.max_attempts)

    saved_files = []
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for index, url in enumerate(urls, 1):
            suffix = Path(urllib.parse.urlparse(url).path).suffix or ".jpg"
            output_path = output_dir / f"ai_fun_tv_{task_id}_{index}{suffix}"
            try:
                download_file(url, output_path)
                saved_files.append(str(output_path))
            except Exception as exc:
                saved_files.append(f"download failed for {url}: {exc}")

    print(json.dumps({
        "projectId": project_id,
        "taskId": task_id,
        "model": model,
        "taskStatus": latest.get("taskStatus"),
        "urls": urls,
        "savedFiles": saved_files,
        "tokenFile": str(token_file),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
