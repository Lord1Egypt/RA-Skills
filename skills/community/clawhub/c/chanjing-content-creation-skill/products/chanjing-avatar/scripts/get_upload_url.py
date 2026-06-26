#!/usr/bin/env python3
"""
获取上传链接。与 chanjing-credentials-guard 使用同一配置文件获取 Token。
用法: get_upload_url --service lip_sync_video --name 1.mp4
输出: JSON { "sign_url", "mime_type", "file_id" } 或错误到 stderr
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
    parser = argparse.ArgumentParser(description="获取蝉镜文件上传链接")
    parser.add_argument("--service", required=True, help="lip_sync_video 或 lip_sync_audio")
    parser.add_argument("--name", required=True, help="文件名，如 1.mp4")
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
