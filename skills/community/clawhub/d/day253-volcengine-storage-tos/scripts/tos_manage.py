#!/usr/bin/env python3
"""Manage Volcengine TOS buckets and objects using the official TOS Python SDK.

Usage:
  python scripts/tos_manage.py list-buckets
  python scripts/tos_manage.py upload --bucket my-bucket --key path/obj.txt --file ./local.txt
  python scripts/tos_manage.py download --bucket my-bucket --key path/obj.txt --file ./out.txt
  python scripts/tos_manage.py presign --bucket my-bucket --key path/obj.txt --expires 3600

Env: VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_TOS_ENDPOINT, VOLCENGINE_TOS_REGION
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import tos
except ImportError:
    print("Error: tos SDK is not installed. Run: pip install tos", file=sys.stderr)
    sys.exit(1)


def _find_repo_root(start: Path) -> Path | None:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_dotenv(Path.cwd() / ".env")
    repo_root = _find_repo_root(Path(__file__).resolve())
    if repo_root:
        _load_dotenv(repo_root / ".env")


def _get_client() -> tos.TosClientV2:
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
    sk = os.environ.get("VOLCENGINE_SECRET_KEY", "")
    endpoint = os.environ.get("VOLCENGINE_TOS_ENDPOINT", "")
    region = os.environ.get("VOLCENGINE_TOS_REGION", "")

    missing = []
    if not ak:
        missing.append("VOLCENGINE_ACCESS_KEY")
    if not sk:
        missing.append("VOLCENGINE_SECRET_KEY")
    if not endpoint:
        missing.append("VOLCENGINE_TOS_ENDPOINT")
    if not region:
        missing.append("VOLCENGINE_TOS_REGION")
    if missing:
        print(f"Error: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("Example .env:", file=sys.stderr)
        print("  VOLCENGINE_ACCESS_KEY=AKLTxxxx", file=sys.stderr)
        print("  VOLCENGINE_SECRET_KEY=xxxx", file=sys.stderr)
        print("  VOLCENGINE_TOS_ENDPOINT=tos-cn-beijing.volces.com", file=sys.stderr)
        print("  VOLCENGINE_TOS_REGION=cn-beijing", file=sys.stderr)
        sys.exit(1)

    return tos.TosClientV2(ak, sk, endpoint, region)


def _json_out(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


# ── Subcommands ──────────────────────────────────────────────────────────────


def cmd_list_buckets(args: argparse.Namespace) -> None:
    client = _get_client()
    resp = client.list_buckets()
    buckets = []
    for b in resp.buckets:
        buckets.append({
            "name": b.name,
            "location": b.location,
            "creation_date": str(b.creation_date),
        })
    if args.print_json:
        _json_out({"buckets": buckets, "count": len(buckets)})
    else:
        print(f"Found {len(buckets)} bucket(s):")
        for b in buckets:
            print(f"  {b['name']}  ({b['location']})  created {b['creation_date']}")


def cmd_create_bucket(args: argparse.Namespace) -> None:
    client = _get_client()
    client.create_bucket(args.bucket)
    result = {"action": "create_bucket", "bucket": args.bucket, "status": "ok"}
    if args.print_json:
        _json_out(result)
    else:
        print(f"Bucket '{args.bucket}' created successfully.")


def cmd_delete_bucket(args: argparse.Namespace) -> None:
    if not args.confirm:
        print("Error: --confirm is required for delete-bucket", file=sys.stderr)
        sys.exit(1)
    client = _get_client()
    client.delete_bucket(args.bucket)
    result = {"action": "delete_bucket", "bucket": args.bucket, "status": "ok"}
    if args.print_json:
        _json_out(result)
    else:
        print(f"Bucket '{args.bucket}' deleted.")


def cmd_list_objects(args: argparse.Namespace) -> None:
    client = _get_client()
    resp = client.list_objects_type2(
        args.bucket,
        prefix=args.prefix or "",
        max_keys=args.max_keys,
    )
    objects = []
    for obj in resp.contents:
        objects.append({
            "key": obj.key,
            "size": obj.size,
            "last_modified": str(obj.last_modified),
            "storage_class": getattr(obj, "storage_class", ""),
        })
    truncated = resp.is_truncated
    if args.print_json:
        _json_out({"bucket": args.bucket, "prefix": args.prefix, "objects": objects, "count": len(objects), "is_truncated": truncated})
    else:
        print(f"Objects in '{args.bucket}' (prefix='{args.prefix or ''}')  [{len(objects)} shown, truncated={truncated}]:")
        for o in objects:
            print(f"  {o['key']}  size={o['size']}  modified={o['last_modified']}")


def cmd_upload(args: argparse.Namespace) -> None:
    client = _get_client()
    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    resp = client.put_object_from_file(
        args.bucket,
        args.key,
        str(file_path),
        content_type=content_type,
    )
    result = {
        "action": "upload",
        "bucket": args.bucket,
        "key": args.key,
        "file": str(file_path.resolve()),
        "size": file_path.stat().st_size,
        "content_type": content_type,
        "etag": getattr(resp, "etag", ""),
        "status_code": getattr(resp, "status_code", 200),
    }
    if args.print_json:
        _json_out(result)
    else:
        print(f"Uploaded '{file_path}' -> tos://{args.bucket}/{args.key}  ({result['size']} bytes, etag={result['etag']})")


def cmd_download(args: argparse.Namespace) -> None:
    client = _get_client()
    output_path = Path(args.file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    client.get_object_to_file(args.bucket, args.key, str(output_path))
    size = output_path.stat().st_size
    result = {
        "action": "download",
        "bucket": args.bucket,
        "key": args.key,
        "file": str(output_path.resolve()),
        "size": size,
    }
    if args.print_json:
        _json_out(result)
    else:
        print(f"Downloaded tos://{args.bucket}/{args.key} -> '{output_path}' ({size} bytes)")


def cmd_delete(args: argparse.Namespace) -> None:
    if not args.confirm:
        print("Error: --confirm is required for delete", file=sys.stderr)
        sys.exit(1)
    client = _get_client()
    client.delete_object(args.bucket, args.key)
    result = {"action": "delete", "bucket": args.bucket, "key": args.key, "status": "ok"}
    if args.print_json:
        _json_out(result)
    else:
        print(f"Deleted tos://{args.bucket}/{args.key}")


def cmd_head(args: argparse.Namespace) -> None:
    client = _get_client()
    resp = client.head_object(args.bucket, args.key)
    result = {
        "bucket": args.bucket,
        "key": args.key,
        "content_length": resp.content_length,
        "content_type": getattr(resp, "content_type", ""),
        "etag": getattr(resp, "etag", ""),
        "last_modified": str(getattr(resp, "last_modified", "")),
        "storage_class": getattr(resp, "storage_class", ""),
    }
    if args.print_json:
        _json_out(result)
    else:
        print(f"tos://{args.bucket}/{args.key}")
        for k, v in result.items():
            if k not in ("bucket", "key"):
                print(f"  {k}: {v}")


def cmd_presign(args: argparse.Namespace) -> None:
    client = _get_client()
    url = client.pre_signed_url("GET", args.bucket, args.key, expires=args.expires)
    result = {
        "bucket": args.bucket,
        "key": args.key,
        "method": "GET",
        "expires_seconds": args.expires,
        "url": url.signed_url,
    }
    if args.print_json:
        _json_out(result)
    else:
        print(f"Presigned URL (GET, {args.expires}s):")
        print(f"  {url.signed_url}")


def cmd_copy(args: argparse.Namespace) -> None:
    client = _get_client()
    src_bucket = args.src_bucket or args.bucket
    client.copy_object(args.bucket, args.key, src_bucket, args.src_key)
    result = {
        "action": "copy",
        "src": f"tos://{src_bucket}/{args.src_key}",
        "dst": f"tos://{args.bucket}/{args.key}",
        "status": "ok",
    }
    if args.print_json:
        _json_out(result)
    else:
        print(f"Copied {result['src']} -> {result['dst']}")


# ── CLI ──────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tos_manage",
        description="Volcengine TOS object storage management (uses official tos SDK)",
    )
    parser.add_argument("--print-json", action="store_true", help="Output JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-buckets", help="List all buckets")

    p = sub.add_parser("create-bucket", help="Create a bucket")
    p.add_argument("--bucket", required=True)

    p = sub.add_parser("delete-bucket", help="Delete a bucket")
    p.add_argument("--bucket", required=True)
    p.add_argument("--confirm", action="store_true", help="Required to confirm deletion")

    p = sub.add_parser("list-objects", help="List objects in a bucket")
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", default="")
    p.add_argument("--max-keys", type=int, default=100)

    p = sub.add_parser("upload", help="Upload a local file")
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--file", required=True)

    p = sub.add_parser("download", help="Download an object to local file")
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--file", required=True)

    p = sub.add_parser("delete", help="Delete an object")
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--confirm", action="store_true", help="Required to confirm deletion")

    p = sub.add_parser("head", help="Get object metadata")
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)

    p = sub.add_parser("presign", help="Generate presigned URL")
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--expires", type=int, default=3600, help="Expiry in seconds (default 3600)")

    p = sub.add_parser("copy", help="Copy an object")
    p.add_argument("--bucket", required=True, help="Destination bucket")
    p.add_argument("--key", required=True, help="Destination key")
    p.add_argument("--src-bucket", default="", help="Source bucket (default: same as --bucket)")
    p.add_argument("--src-key", required=True, help="Source key")

    return parser


DISPATCH = {
    "list-buckets": cmd_list_buckets,
    "create-bucket": cmd_create_bucket,
    "delete-bucket": cmd_delete_bucket,
    "list-objects": cmd_list_objects,
    "upload": cmd_upload,
    "download": cmd_download,
    "delete": cmd_delete,
    "head": cmd_head,
    "presign": cmd_presign,
    "copy": cmd_copy,
}


def main() -> None:
    _load_env()
    parser = build_parser()
    args = parser.parse_args()
    handler = DISPATCH.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)
    try:
        handler(args)
    except tos.exceptions.TosClientError as e:
        print(f"TOS client error: {e}", file=sys.stderr)
        sys.exit(1)
    except tos.exceptions.TosServerError as e:
        print(f"TOS server error: code={e.code}, message={e.message}, request_id={e.request_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
