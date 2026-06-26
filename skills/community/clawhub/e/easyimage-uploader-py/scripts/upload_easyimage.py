#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib import error, request

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.json"


def eprint(*args):
    print(*args, file=sys.stderr)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Upload an image to an EasyImages 2.0 server and print normalized JSON output."
    )
    parser.add_argument("image", help="Path to the image file to upload")
    parser.add_argument("--server", help="EasyImages base URL, e.g. https://img.example.com")
    parser.add_argument("--token", help="EasyImages API token")
    parser.add_argument(
        "--config",
        help="Path to config JSON file. Defaults to ../config.json next to this skill.",
    )
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds")
    return parser


def getenv_first(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def load_config_file(path: Path):
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in config file: {path} ({exc})") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a JSON object: {path}")

    return data


def resolve_config(args):
    config_path = resolve_user_path(args.config) if args.config else DEFAULT_CONFIG_PATH
    config = load_config_file(config_path)

    server = (
        args.server
        or config.get("server")
        or getenv_first("EASYIMAGE_URL", "EASYIMAGE_SERVER", "EASYIMAGE_BASE_URL")
    )
    token = args.token or config.get("token") or getenv_first("EASYIMAGE_TOKEN")

    if not server:
        raise ValueError(
            f"Missing EasyImages server URL. Pass --server, set it in {config_path}, or set EASYIMAGE_URL."
        )
    if not token:
        raise ValueError(
            f"Missing EasyImages token. Pass --token, set it in {config_path}, or set EASYIMAGE_TOKEN."
        )

    server = server.rstrip("/")
    if not server.startswith(("http://", "https://")):
        raise ValueError("EasyImages server URL must start with http:// or https://")

    return server, token, config_path


def guess_content_type(path: Path):
    content_type, _ = mimetypes.guess_type(str(path))
    return content_type or "application/octet-stream"


def encode_multipart(fields, files):
    boundary = "----OpenClawEasyImageBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")

    for name, filename, content_type, data in files:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
        body.extend(data)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return boundary, bytes(body)


def resolve_user_path(raw_path: str, *, base_dir: Path | None = None) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    anchor = base_dir or Path.cwd()
    return (anchor / path).resolve()


def main():
    parser = build_parser()
    args = parser.parse_args()

    image_path = resolve_user_path(args.image)
    if not image_path.exists() or not image_path.is_file():
        eprint(f"Image file not found: {image_path}")
        sys.exit(2)

    try:
        server, token, config_path = resolve_config(args)
    except ValueError as exc:
        eprint(str(exc))
        sys.exit(2)

    endpoint = f"{server}/api/index.php"
    image_bytes = image_path.read_bytes()
    boundary, body = encode_multipart(
        {"token": token},
        [("image", image_path.name, guess_content_type(image_path), image_bytes)],
    )

    req = request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "Accept": "application/json, text/plain, */*",
        },
    )

    try:
        with request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({
            "ok": False,
            "http_status": exc.code,
            "error": "http_error",
            "response_text": raw,
            "endpoint": endpoint,
            "config_path": str(config_path),
        }, ensure_ascii=False))
        sys.exit(1)
    except error.URLError as exc:
        print(json.dumps({
            "ok": False,
            "error": "network_error",
            "message": str(exc.reason),
            "endpoint": endpoint,
            "config_path": str(config_path),
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({
            "ok": False,
            "http_status": status,
            "error": "invalid_json",
            "response_text": raw,
            "endpoint": endpoint,
            "config_path": str(config_path),
        }, ensure_ascii=False))
        sys.exit(1)

    result = payload.get("result")
    code = payload.get("code")
    url = payload.get("url")

    ok = (status == 200) and (result == "success") and bool(url)
    output = {
        "ok": ok,
        "http_status": status,
        "endpoint": endpoint,
        "config_path": str(config_path),
        "result": result,
        "code": code,
        "url": url,
        "thumb": payload.get("thumb"),
        "delete_url": payload.get("del"),
        "src_name": payload.get("srcName"),
        "raw": payload,
    }
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
