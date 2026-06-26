import sys
import os
import requests
import json
import argparse


def upload_file(file_path, token=None):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        sys.exit(1)

    url = "https://ziya.dfwytech.com/dfwy_api/lsxx/openclaw/upload"
    files = {"file": open(file_path, "rb")}
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    # Priority: argument > env var
    final_token = token or os.environ.get("ZY_TOKEN")
    if final_token:
        headers["Authorization"] = f"Bearer {final_token}"

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200 and data.get("data"):
            print(json.dumps(data["data"], ensure_ascii=False, indent=4))
        else:
            if data.get("code") == 400:
                print("api_key无效")
            else:
                msg = data.get("msg", "Unknown error")
                print(f"Error: {msg}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload file to server")
    parser.add_argument("token", help="API Token")
    parser.add_argument("file_path", help="Local file path")
    args = parser.parse_args()
    upload_file(args.file_path, args.token)
