#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://civitai.com/api/v1"
DOWNLOAD_BASE_URL = "https://civitai.com/api/download/models"


def load_env_file(start: Path) -> None:
    candidates = [start / ".env", start.parent / ".env"]
    for env_path in candidates:
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
        return


def build_url(path: str, params: dict | None = None) -> str:
    url = f"{BASE_URL}{path}"
    if params:
        params = {k: v for k, v in params.items() if v not in (None, "", False)}
        if params:
            url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    return url


def request_json(url: str, token: str | None = None) -> dict:
    headers = {"User-Agent": "openclaw-civitai-skill/1.0", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_models(args, token):
    params = {
        "query": args.query,
        "limit": args.limit,
        "page": args.page,
        "cursor": args.cursor,
        "types": args.types,
        "sort": args.sort,
        "period": args.period,
        "username": args.username,
        "tag": args.tag,
        "nsfw": str(args.nsfw).lower() if args.nsfw is not None else None,
    }
    print_json(request_json(build_url("/models", params), token))


def cmd_model(args, token):
    print_json(request_json(build_url(f"/models/{args.model_id}"), token))


def cmd_version(args, token):
    print_json(request_json(build_url(f"/model-versions/{args.version_id}"), token))


def cmd_hash(args, token):
    print_json(request_json(build_url(f"/model-versions/by-hash/{args.hash_value}"), token))


def cmd_creators(args, token):
    params = {"query": args.query, "limit": args.limit, "page": args.page, "cursor": args.cursor}
    print_json(request_json(build_url("/creators", params), token))


def cmd_tags(args, token):
    params = {"query": args.query, "limit": args.limit, "page": args.page, "cursor": args.cursor}
    print_json(request_json(build_url("/tags", params), token))


def cmd_images(args, token):
    params = {
        "postId": args.post_id,
        "modelId": args.model_id,
        "modelVersionId": args.model_version_id,
        "username": args.username,
        "limit": args.limit,
        "page": args.page,
        "cursor": args.cursor,
        "sort": args.sort,
        "period": args.period,
        "nsfw": str(args.nsfw).lower() if args.nsfw is not None else None,
    }
    print_json(request_json(build_url("/images", params), token))


def cmd_download(args, token):
    params = {}
    if args.type:
        params["type"] = args.type
    if args.format:
        params["format"] = args.format
    if args.size:
        params["size"] = args.size
    if args.fp:
        params["fp"] = args.fp
    if token:
        params["token"] = token
    url = f"{DOWNLOAD_BASE_URL}/{args.version_id}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    print(url)


def main():
    script_dir = Path(__file__).resolve().parent
    load_env_file(script_dir)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Query the Civitai public REST API.")
    parser.add_argument("--token", default=os.getenv("CIVITAI_API_KEY"), help="Civitai API token. Defaults to CIVITAI_API_KEY from .env or the environment.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("models", help="Search or list models")
    p.add_argument("--query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--page", type=int)
    p.add_argument("--cursor")
    p.add_argument("--types")
    p.add_argument("--sort")
    p.add_argument("--period")
    p.add_argument("--username")
    p.add_argument("--tag")
    p.add_argument("--nsfw", choices=["true", "false"])
    p.set_defaults(func=cmd_models)

    p = subparsers.add_parser("model", help="Get one model by id")
    p.add_argument("model_id", type=int)
    p.set_defaults(func=cmd_model)

    p = subparsers.add_parser("version", help="Get one model version by id")
    p.add_argument("version_id", type=int)
    p.set_defaults(func=cmd_version)

    p = subparsers.add_parser("by-hash", help="Get one model version by file hash")
    p.add_argument("hash_value")
    p.set_defaults(func=cmd_hash)

    p = subparsers.add_parser("creators", help="Search or list creators")
    p.add_argument("--query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--page", type=int)
    p.add_argument("--cursor")
    p.set_defaults(func=cmd_creators)

    p = subparsers.add_parser("tags", help="Search or list tags")
    p.add_argument("--query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--page", type=int)
    p.add_argument("--cursor")
    p.set_defaults(func=cmd_tags)

    p = subparsers.add_parser("images", help="Search or list images")
    p.add_argument("--post-id", type=int)
    p.add_argument("--model-id", type=int)
    p.add_argument("--model-version-id", type=int)
    p.add_argument("--username")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--page", type=int)
    p.add_argument("--cursor")
    p.add_argument("--sort")
    p.add_argument("--period")
    p.add_argument("--nsfw", choices=["true", "false"])
    p.set_defaults(func=cmd_images)

    p = subparsers.add_parser("download-url", help="Build an authenticated model download URL for a model version")
    p.add_argument("version_id", type=int)
    p.add_argument("--type")
    p.add_argument("--format")
    p.add_argument("--size")
    p.add_argument("--fp")
    p.set_defaults(func=cmd_download)

    args = parser.parse_args()
    try:
        args.func(args, args.token)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
