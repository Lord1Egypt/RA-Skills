#!/usr/bin/env python3
"""Execute KB commands through the remote HTTP execute service."""

from __future__ import annotations

import argparse
import mimetypes
import json
import os
import sys
import uuid
import urllib.error
import urllib.parse
import urllib.request


EXECUTE_PATH = "/kb/atomix/execute"


def parse_header(raw_header: str) -> tuple[str, str]:
    if "=" in raw_header:
        key, value = raw_header.split("=", 1)
    elif ":" in raw_header:
        key, value = raw_header.split(":", 1)
    else:
        raise ValueError(f"invalid header format: {raw_header!r}")

    key = key.strip()
    value = value.strip()
    if not key:
        raise ValueError(f"header key is empty: {raw_header!r}")
    return key, value


def print_response(body: bytes) -> None:
    text = body.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        print(text)
        return

    print(json.dumps(parsed, ensure_ascii=False, indent=2))


def parse_json_body(body: bytes) -> object | None:
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def read_command_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def normalize_execute_url(raw_url: str) -> str:
    parsed = urllib.parse.urlparse(raw_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"invalid KB execute URL: {raw_url!r}")
    if parsed.path == EXECUTE_PATH:
        return urllib.parse.urlunparse(parsed)
    if parsed.path in ("", "/"):
        return urllib.parse.urlunparse(parsed._replace(path=EXECUTE_PATH, params="", query="", fragment=""))
    return urllib.parse.urlunparse(parsed)


def build_auth_headers(token: str) -> dict[str, str]:
    normalized = token.strip()
    if normalized.startswith("tk"):
        return {"Authorization": f"Bearer {normalized}"}
    if normalized.startswith("Bearer"):
        return {"Authorization": f"{normalized}"}
    return {"token": normalized}


def build_file_url(base_url: str, endpoint_path: str, **query: str) -> str:
    from urllib.parse import urlencode, urljoin

    url = urljoin(base_url, endpoint_path)
    if query:
        return f"{url}?{urlencode(query)}"
    return url


def encode_multipart(fields: dict[str, str], file_field: str, file_name: str, file_bytes: bytes, content_type: str) -> tuple[bytes, str]:
    boundary = f"----kbatomix{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )

    chunks.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'.encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return b"".join(chunks), boundary


def upload_file(url: str, token: str, headers: dict[str, str], local_path: str, path_name: str, file_name: str | None, timeout: float) -> int:
    if not os.path.isfile(local_path):
        print(f"upload source is not a file: {local_path}", file=sys.stderr)
        return 1

    actual_name = file_name or os.path.basename(local_path)
    content_type = mimetypes.guess_type(actual_name)[0] or "application/octet-stream"
    with open(local_path, "rb") as handle:
        file_bytes = handle.read()

    payload, boundary = encode_multipart(
        {"fileName": actual_name, "pathName": path_name},
        "file",
        actual_name,
        file_bytes,
        content_type,
    )
    request = urllib.request.Request(
        url=build_file_url(url, "/openapi/partner/sage/file/upload"),
        data=payload,
        headers={
            **headers,
            **build_auth_headers(token),
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    return send_request(request, timeout)


def download_file(
    url: str,
    token: str,
    headers: dict[str, str],
    code: str,
    local_path: str,
    extract_is: bool | None,
    overwrite: bool,
    timeout: float,
) -> int:
    query: dict[str, str] = {"code": code}
    if extract_is is not None:
        query["extractIs"] = "true" if extract_is else "false"

    request = urllib.request.Request(
        url=build_file_url(url, "/openapi/partner/sage/file/download", **query),
        headers={**headers, **build_auth_headers(token)},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            parsed = parse_json_body(body)
            if isinstance(parsed, dict):
                print(json.dumps(parsed, ensure_ascii=False, indent=2), file=sys.stderr)
                return 1
            target_path = resolve_download_path(local_path, response.headers.get("Content-Disposition"), code, overwrite)
            os.makedirs(os.path.dirname(target_path) or ".", exist_ok=True)
            mode = "wb" if overwrite else "xb"
            with open(target_path, mode) as handle:
                handle.write(body)
            print(
                json.dumps(
                    {
                        "savedPath": target_path,
                        "fileName": os.path.basename(target_path),
                        "size": len(body),
                        "contentType": response.headers.get("Content-Type", "application/octet-stream"),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
    except FileExistsError:
        print(f"download target already exists: {local_path}", file=sys.stderr)
        return 1
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}", file=sys.stderr)
        print_response(exc.read())
        return 1
    except urllib.error.URLError as exc:
        print(f"request failed: {exc.reason}", file=sys.stderr)
        return 1


def get_download_link(
    url: str,
    token: str,
    headers: dict[str, str],
    code: str,
    extract_is: bool | None,
    timeout: float,
) -> int:
    query: dict[str, str] = {"code": code}
    if extract_is is not None:
        query["extractIs"] = "true" if extract_is else "false"

    request = urllib.request.Request(
        url=build_file_url(url, "/openapi/partner/sage/file/downloadLink", **query),
        headers={**headers, **build_auth_headers(token)},
        method="GET",
    )
    return send_request(request, timeout)


def resolve_download_path(local_path: str, content_disposition: str | None, code: str, overwrite: bool) -> str:
    target_path = local_path
    if os.path.isdir(local_path):
        target_path = os.path.join(local_path, extract_download_name(content_disposition) or code)
    if not overwrite and os.path.exists(target_path):
        raise FileExistsError(target_path)
    return target_path


def extract_download_name(content_disposition: str | None) -> str | None:
    if not content_disposition:
        return None
    import re
    from urllib.parse import unquote

    utf8_match = re.search(r"filename\\*=UTF-8''([^;]+)", content_disposition, re.IGNORECASE)
    if utf8_match:
        return unquote(utf8_match.group(1))
    quoted_match = re.search(r'filename="([^"]+)"', content_disposition, re.IGNORECASE)
    if quoted_match:
        return quoted_match.group(1)
    plain_match = re.search(r"filename=([^;]+)", content_disposition, re.IGNORECASE)
    if plain_match:
        return plain_match.group(1).strip()
    return None


def send_request(request: urllib.request.Request, timeout: float) -> int:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            print_response(response.read())
            return 0
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}", file=sys.stderr)
        print_response(exc.read())
        return 1
    except urllib.error.URLError as exc:
        print(f"request failed: {exc.reason}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send a KB command string to the remote execute endpoint.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help='KB command string, for example: "kb cat --code 2031630406710923264"',
    )
    parser.add_argument(
        "--command",
        dest="command_flag",
        help='KB command string, for example: "kb ls"',
    )
    parser.add_argument(
        "--command-file",
        help="UTF-8 text file containing the KB command string.",
    )
    parser.add_argument(
        "--upload-file",
        help="Upload a local file from this machine to AIS.",
    )
    parser.add_argument(
        "--download-code",
        help="Download an AIS file by code.",
    )
    parser.add_argument(
        "--download-link-code",
        help="Generate an AIS file download link by code.",
    )
    parser.add_argument(
        "--save-to",
        help="Local file path or directory for --download-code.",
    )
    parser.add_argument(
        "--path-name",
        help="Remote AIS path name for --upload-file.",
    )
    parser.add_argument(
        "--file-name",
        help="Optional override file name for --upload-file.",
    )
    parser.add_argument(
        "--extract-is",
        choices=["true", "false"],
        help="Optional extractIs query flag for --download-code or --download-link-code.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing local files for --download-code.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds. Default: 30.",
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("KB_EXECUTE_URL"),
        help="AIS site URL or full KB execute endpoint. Defaults to env KB_EXECUTE_URL.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("KB_TOKEN"),
        help="KB token header value. Defaults to env KB_TOKEN.",
    )
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Additional request header in key=value or key:value format.",
    )
    args = parser.parse_args()

    modes = [
        bool(args.command),
        bool(args.command_flag),
        bool(args.command_file),
        bool(args.upload_file),
        bool(args.download_code),
        bool(args.download_link_code),
    ]
    if sum(modes) != 1:
        parser.error(
            "choose exactly one operation: command / --command / --command-file / --upload-file / --download-code / --download-link-code"
        )
    if not args.url:
        parser.error("missing KB execute URL; pass --url or set KB_EXECUTE_URL")
    if not args.token:
        parser.error("missing KB token; pass --token or set KB_TOKEN")

    try:
        args.url = normalize_execute_url(args.url)
    except ValueError as exc:
        parser.error(str(exc))

    headers: dict[str, str] = {}
    try:
        for raw_header in args.header:
            key, value = parse_header(raw_header)
            headers[key] = value
    except ValueError as exc:
        parser.error(str(exc))

    extract_is: bool | None = None
    if args.extract_is is not None:
        extract_is = args.extract_is == "true"

    if args.upload_file:
        if not args.path_name:
            parser.error("--upload-file requires --path-name")
        return upload_file(args.url, args.token, headers, args.upload_file, args.path_name, args.file_name, args.timeout)

    if args.download_code:
        if not args.save_to:
            parser.error("--download-code requires --save-to")
        return download_file(
            args.url,
            args.token,
            headers,
            args.download_code,
            args.save_to,
            extract_is,
            args.overwrite,
            args.timeout,
        )

    if args.download_link_code:
        return get_download_link(args.url, args.token, headers, args.download_link_code, extract_is, args.timeout)

    command = args.command_flag or args.command
    if args.command_file:
        command = read_command_file(args.command_file)
    if not command:
        parser.error("missing KB command string")

    headers = {"Content-Type": "application/json", **build_auth_headers(args.token), **headers}
    payload = json.dumps({"command": command}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url=args.url,
        data=payload,
        headers=headers,
        method="POST",
    )

    return send_request(request, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
