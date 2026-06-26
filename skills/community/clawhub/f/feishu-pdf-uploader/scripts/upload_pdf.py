#!/usr/bin/env python3
"""
Upload files to Feishu (Lark) cloud drive.
Supports PDF and any file types.

Usage:
    python3 upload_pdf.py <file_path> [options]
    
Options:
    --folder-token    Target folder token
    --app-id          Feishu app ID
    --app-secret      Feishu app secret
    
Example:
    python3 upload_pdf.py report.pdf --folder-token VnTdf2MNglfgPtdrhCxcSTdOnZd
"""
import requests
import json
import os
import sys
import argparse


def get_tenant_token(app_id: str, app_secret: str) -> str:
    """Get tenant access token from Feishu."""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"Failed to get token: {result.get('msg')}")
    
    return result["tenant_access_token"]


def upload_file_to_feishu(
    file_path: str,
    folder_token: str,
    app_id: str,
    app_secret: str
) -> dict:
    """
    Upload a file to Feishu cloud drive.
    
    Args:
        file_path: Local file path
        folder_token: Target folder token
        app_id: Feishu app ID
        app_secret: Feishu app secret
        
    Returns:
        dict with success status and file info
    """
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"\n📄 Uploading: {file_name}")
    print(f"Size: {file_size} bytes")
    
    # Get token
    token = get_tenant_token(app_id, app_secret)
    
    # Read file content
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Step 1: Prepare upload
    prepare_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_prepare"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    prepare_data = {
        "file_name": file_name,
        "parent_type": "explorer",
        "parent_node": folder_token,
        "size": file_size
    }
    
    resp = requests.post(prepare_url, headers=headers, json=prepare_data)
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"Prepare failed: {result.get('msg')}")
    
    upload_id = result["data"]["upload_id"]
    print(f"✅ Prepare OK, upload_id: {upload_id}")
    
    # Step 2: Upload part
    # ⚠️ IMPORTANT: Do NOT include checksum parameter!
    # It causes "1061002 params error" or "1062008 checksum param Invalid"
    upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_part"
    
    boundary = f"----FormBoundary{os.urandom(8).hex()}"
    
    # Build multipart body
    body = b""
    
    # upload_id field
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="upload_id"\r\n\r\n'
    body += upload_id.encode() + b'\r\n'
    
    # seq field (0 for single-part upload)
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="seq"\r\n\r\n'
    body += b'0\r\n'
    
    # size field
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="size"\r\n\r\n'
    body += str(file_size).encode() + b'\r\n'
    
    # file field
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'.encode()
    body += b'Content-Type: application/octet-stream\r\n\r\n'
    body += file_data
    body += b'\r\n'
    
    # End boundary
    body += f"--{boundary}--\r\n".encode()
    
    upload_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    
    resp = requests.post(upload_url, headers=upload_headers, data=body)
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"Upload failed: {result.get('msg')}")
    
    print(f"✅ Upload part OK")
    
    # Step 3: Finish upload
    finish_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_finish"
    finish_data = {"upload_id": upload_id, "block_num": 1}
    
    resp = requests.post(finish_url, headers=headers, json=finish_data)
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"Finish failed: {result.get('msg')}")
    
    file_token = result["data"].get("file_token")
    url = result["data"].get("url")
    
    print(f"✅ Uploaded successfully!")
    print(f"   File token: {file_token}")
    print(f"   URL: {url}")
    
    return {
        "success": True,
        "file_token": file_token,
        "url": url,
        "name": file_name
    }


def load_config_from_openclaw():
    """Load Feishu credentials from OpenClaw config."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    
    if not os.path.exists(config_path):
        return None, None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        feishu_config = config.get("channels", {}).get("feishu", {})
        
        # Try accounts format first
        accounts = feishu_config.get("accounts", {})
        for account_id, account in accounts.items():
            return account.get("appId"), account.get("appSecret")
        
        # Fall back to direct appId/appSecret format
        app_id = feishu_config.get("appId")
        app_secret = feishu_config.get("appSecret")
        if app_id and app_secret:
            return app_id, app_secret
            
    except Exception as e:
        print(f"Warning: Failed to load config: {e}")
    
    return None, None


def main():
    parser = argparse.ArgumentParser(description="Upload files to Feishu cloud drive")
    parser.add_argument("file", help="Path to file to upload")
    parser.add_argument("--folder-token", help="Target folder token", default=os.environ.get("FEISHU_FOLDER_TOKEN"))
    parser.add_argument("--app-id", help="Feishu app ID", default=os.environ.get("FEISHU_APP_ID"))
    parser.add_argument("--app-secret", help="Feishu app secret", default=os.environ.get("FEISHU_APP_SECRET"))
    
    args = parser.parse_args()
    
    # Load from config if not provided
    app_id = args.app_id
    app_secret = args.app_secret
    
    if not app_id or not app_secret:
        config_app_id, config_app_secret = load_config_from_openclaw()
        app_id = app_id or config_app_id
        app_secret = app_secret or config_app_secret
    
    if not app_id or not app_secret:
        print("❌ Error: Feishu credentials required")
        print("Set FEISHU_APP_ID and FEISHU_APP_SECRET environment variables,")
        print("or ensure channels.feishu.accounts exists in ~/.openclaw/openclaw.json")
        sys.exit(1)
    
    if not args.folder_token:
        print("❌ Error: Folder token required (--folder-token or FEISHU_FOLDER_TOKEN)")
        sys.exit(1)
    
    if not os.path.exists(args.file):
        print(f"❌ Error: File not found: {args.file}")
        sys.exit(1)
    
    try:
        result = upload_file_to_feishu(args.file, args.folder_token, app_id, app_secret)
        print(f"\n✅ Success: {result['name']}")
        print(f"   URL: {result['url']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
