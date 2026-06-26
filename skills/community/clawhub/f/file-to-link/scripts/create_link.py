
import os
import argparse
import sys
import time
import json
from pathlib import Path
from typing import Optional

# Try to import qiniu, and provide a helpful error message if it's not installed.
try:
    from qiniu import Auth, put_file
except ImportError:
    print("Error: The 'qiniu' package is not installed. Please install it by running 'pip install qiniu'", file=sys.stderr)
    sys.exit(1)

# --- Qiniu Configuration ---
# WARNING: For production, these should be moved to environment variables
# or a secure configuration management system.
def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """从 ~/.openclaw/config.json 安全地读取配置值"""
    config_path = Path.home() / '.openclaw' / 'config.json'
    if not config_path.exists():
        return default
    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
        return config.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default

QINIU_ACCESS_KEY = get_config_value("qiniu_access_key")
QINIU_SECRET_KEY = get_config_value("qiniu_secret_key")
QINIU_BUCKET_NAME = get_config_value("qiniu_bucket_name")
QINIU_DOMAIN = get_config_value("qiniu_domain")

def upload_file_to_qiniu(file_path):
    """
    Uploads a file to Qiniu Kodo and returns the public URL.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        return None

    # Create a unique object key for Qiniu using the original filename and a timestamp
    key = f"{os.path.basename(file_path)}_{int(time.time())}"

    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    token = q.upload_token(QINIU_BUCKET_NAME, key, 3600)

    print(f"Uploading '{os.path.basename(file_path)}' to Qiniu Kodo...", file=sys.stderr)
    try:
        # The user's working code used put_file, so we stick to it for consistency,
        # while acknowledging the deprecation warning.
        ret, info = put_file(token, key, file_path)

        if info and info.status_code == 200:
            encoded_key = urllib.parse.quote(key)
            file_url = f"{QINIU_DOMAIN}/{encoded_key}"
            print(f"Upload successful. URL created.", file=sys.stderr)
            return file_url
        else:
            print(f"Error: Qiniu upload failed. Status: {getattr(info, 'status_code', 'N/A')}, Info: {info}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"An unexpected error occurred during Qiniu upload: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Uploads a local file to Qiniu Cloud Storage and returns a public URL.',
        epilog='SECURITY WARNING: Files uploaded may be publicly accessible depending on bucket settings. Do not upload sensitive data.'
    )
    parser.add_argument("--file", required=True, help="The full local path of the file to upload.")

    args = parser.parse_args()

    # The user's working code from check_video.py showed a deprecation warning for put_file.
    # We add a warning here to be transparent about it.
    print("Note: This script uses a Qiniu SDK function (put_file) that may be deprecated. Consider upgrading to put_file_v2 in the future.", file=sys.stderr)

    url = upload_file_to_qiniu(args.file)

    if url:
        print(url)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

