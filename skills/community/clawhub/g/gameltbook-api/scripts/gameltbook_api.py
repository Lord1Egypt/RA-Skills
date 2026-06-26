#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("method")
    parser.add_argument("url")
    parser.add_argument("--token", required=True)
    parser.add_argument("--data")
    parser.add_argument("--form", action="append", default=[], help="Multipart field, format key=value or key=@/path/file")
    parser.add_argument("--insecure", action="store_true")
    args = parser.parse_args()

    headers = {"X-GameltBook-Token": args.token}
    context = ssl._create_unverified_context() if args.insecure else None

    if args.form:
        return _send_multipart(args, headers, context)

    body = None
    if args.data is not None:
        body = args.data.encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(args.url, data=body, method=args.method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, context=context) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            print(json.dumps({"status": resp.status, "body": _try_json(raw)}, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": e.code, "body": _try_json(raw)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)


def _send_multipart(args, headers, context):
    boundary = "----OpenClawGameltBookBoundary" + os.urandom(8).hex()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    body = bytearray()

    for field in args.form:
        if "=" not in field:
            raise SystemExit(f"Invalid --form field: {field}")
        key, value = field.split("=", 1)
        if value.startswith("@"):
            path = value[1:]
            with open(path, "rb") as f:
                file_bytes = f.read()
            filename = os.path.basename(path)
            body.extend(_part(boundary, key, file_bytes, filename=filename, is_file=True))
        else:
            body.extend(_part(boundary, key, value.encode("utf-8")))

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    req = urllib.request.Request(args.url, data=bytes(body), method=args.method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, context=context) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            print(json.dumps({"status": resp.status, "body": _try_json(raw)}, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": e.code, "body": _try_json(raw)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)


def _part(boundary, name, data, filename=None, is_file=False):
    out = bytearray()
    out.extend(f"--{boundary}\r\n".encode("utf-8"))
    if is_file and filename:
        content_type = _guess_content_type(filename)
        out.extend(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8"))
        out.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        out.extend(data)
        out.extend(b"\r\n")
    else:
        out.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        out.extend(data)
        out.extend(b"\r\n")
    return out


def _guess_content_type(filename):
    lower = filename.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".gif"):
        return "image/gif"
    if lower.endswith(".webp"):
        return "image/webp"
    return "application/octet-stream"


def _try_json(raw):
    try:
        return json.loads(raw)
    except Exception:
        return raw


if __name__ == "__main__":
    main()
