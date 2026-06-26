#!/usr/bin/env python3
"""
获取定制数字人素材上传链接。
用法: get_upload_url --name source.mp4 [--service customised_person]
输出: JSON，包含 sign_url / mime_type / file_id
"""
import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "common"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _auth import resolve_chanjing_access_token
from file_upload import fetch_create_upload_url_payload


def main():
    parser = argparse.ArgumentParser(description="获取定制数字人素材上传链接")
    parser.add_argument("--name", required=True, help="原始文件名，如 source.mp4")
    parser.add_argument(
        "--service",
        default="customised_person",
        help="文件用途，默认 customised_person",
    )
    args = parser.parse_args()

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    payload, fetch_err = fetch_create_upload_url_payload(token, args.service, args.name)
    if fetch_err:
        print(fetch_err, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
