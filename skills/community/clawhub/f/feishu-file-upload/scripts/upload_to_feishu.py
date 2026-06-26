#!/usr/bin/env python3
"""
Upload a local file to Feishu and send as file message.

Supports sending to:
- Group chats (chat_id)
- Individual users (open_id / user_id)
- Emails (email)

Usage:
    python upload_to_feishu.py <file_path> <receive_id> [--type chat_id|open_id|user_id|email]

Examples:
    # Send to group chat
    python upload_to_feishu.py /path/to/file.csv oc_xxxxxx --type chat_id
    
    # Send to individual user
    python upload_to_feishu.py /path/to/file.pdf ou_xxxxxx --type open_id
    
    # Send via email
    python upload_to_feishu.py /path/to/file.zip user@example.com --type email

Requires: app_id, app_secret from openclaw.json
"""

import json
import os
import sys
import argparse
import requests
from pathlib import Path

def get_openclaw_config():
    """Read Feishu credentials from openclaw.json"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    with open(config_path) as f:
        config = json.load(f)
    
    feishu = config.get("channels", {}).get("feishu", {})
    return {
        "app_id": feishu.get("appId"),
        "app_secret": feishu.get("appSecret")
    }

def get_tenant_access_token(app_id, app_secret):
    """Get tenant access token from Feishu API"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get token: {data}")
    return data["tenant_access_token"]

def get_file_type(file_path):
    """Determine Feishu file type from extension"""
    ext = Path(file_path).suffix.lower()
    type_map = {
        '.pdf': 'pdf',
        '.doc': 'doc',
        '.docx': 'stream',  # docx uses stream type
        '.xls': 'xls',
        '.xlsx': 'stream',  # xlsx uses stream type
        '.ppt': 'ppt',
        '.pptx': 'stream',  # pptx uses stream type
        '.mp3': 'opus',  # Need conversion
        '.mp4': 'mp4',
        '.wav': 'opus',  # Need conversion
        '.txt': 'stream',
        '.csv': 'stream',
        '.json': 'stream',
        '.xml': 'stream',
        '.md': 'stream',
        '.zip': 'stream',
        '.png': 'stream',
        '.jpg': 'stream',
        '.jpeg': 'stream',
        '.gif': 'stream',
        '.webp': 'stream',
    }
    return type_map.get(ext, 'stream')  # Default to stream for unknown types

def upload_file(file_path, token):
    """Upload file to Feishu IM and get file_key"""
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    file_type = get_file_type(file_path)
    file_name = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        files = {
            "file": f
        }
        data = {
            "file_type": file_type,
            "file_name": file_name
        }
        resp = requests.post(url, headers=headers, data=data, files=files)
    
    resp.raise_for_status()
    data = resp.json()
    
    if data.get("code") != 0:
        raise Exception(f"Upload failed: {data}")
    
    return data["data"]["file_key"]

def send_file_to_chat(receive_id, file_key, token, file_name, receive_id_type="chat_id"):
    """Send file message to Feishu chat/user
    
    Args:
        receive_id: The recipient ID (chat_id, open_id, user_id, or email)
        file_key: File key from upload
        token: Access token
        file_name: Original file name
        receive_id_type: Type of receive_id (chat_id, open_id, user_id, email)
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Create file share message
    content = {
        "file_key": file_key
    }
    
    payload = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps(content)
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    
    if data.get("code") != 0:
        raise Exception(f"Send failed: {data}")
    
    return data["data"]["message_id"]

def main():
    parser = argparse.ArgumentParser(
        description="Upload local file to Feishu and send as file message",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send to group chat
  python upload_to_feishu.py /path/to/file.csv oc_xxxxxx --type chat_id
  
  # Send to individual user
  python upload_to_feishu.py /path/to/file.pdf ou_xxxxxx --type open_id
  
  # Send via email
  python upload_to_feishu.py /path/to/file.zip user@example.com --type email
        """
    )
    
    parser.add_argument("file_path", help="Path to the file to upload")
    parser.add_argument("receive_id", nargs="?", help="Recipient ID (chat_id, open_id, user_id, or email)")
    parser.add_argument("--type", "-t", dest="receive_id_type", 
                       choices=["chat_id", "open_id", "user_id", "email"],
                       default="chat_id",
                       help="Recipient type (default: chat_id)")
    parser.add_argument("--env", action="store_true",
                       help="Get receive_id from OPENCLAW_CHAT_ID environment variable")
    
    args = parser.parse_args()
    
    # Get receive_id from argument or environment
    receive_id = args.receive_id
    if args.env:
        receive_id = os.environ.get("OPENCLAW_CHAT_ID")
        if not receive_id:
            print("Error: OPENCLAW_CHAT_ID environment variable not set")
            sys.exit(1)
    
    if not receive_id:
        print("Error: receive_id is required (use positional argument or --env)")
        parser.print_help()
        sys.exit(1)
    
    file_path = args.file_path
    receive_id_type = args.receive_id_type
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Get config
    config = get_openclaw_config()
    if not config["app_id"] or not config["app_secret"]:
        print("Error: Feishu credentials not found in openclaw.json")
        sys.exit(1)
    
    # Get token
    print("Getting access token...")
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    
    # Upload file
    print(f"Uploading {os.path.basename(file_path)}...")
    file_key = upload_file(file_path, token)
    
    # Send to chat/user
    print(f"Sending to {receive_id_type}={receive_id}...")
    file_name = os.path.basename(file_path)
    message_id = send_file_to_chat(receive_id, file_key, token, file_name, receive_id_type)
    
    print(f"✅ File sent successfully! Message ID: {message_id}")

if __name__ == "__main__":
    main()
