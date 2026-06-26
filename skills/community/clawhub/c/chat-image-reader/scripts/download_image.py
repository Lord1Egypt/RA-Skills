#!/usr/bin/env python3
"""
Universal image downloader for multiple chat platforms.
Supports: Feishu, DingTalk, WeChat, Discord, Telegram, WhatsApp, Slack, LINE

Usage:
    python download_image.py --platform feishu --message-id <id> --image-key <key> --output <path>
    python download_image.py --platform dingtalk --download-code <code> --output <path>
    python download_image.py --platform wechat --media-id <id> --output <path>
    python download_image.py --platform discord --url <attachment_url> --output <path>
    python download_image.py --platform telegram --file-id <id> --token <bot_token> --output <path>
    python download_image.py --url <direct_url> --output <path>
"""

import argparse
import os
import sys
import requests
import tempfile
import json
from pathlib import Path


def download_feishu_image(message_id: str, image_key: str, output_path: str) -> str:
    """Download image from Feishu."""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        raise ValueError("FEISHU_APP_ID and FEISHU_APP_SECRET must be set")
    
    # Get tenant token
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret}
    )
    resp.raise_for_status()
    token = resp.json()["tenant_access_token"]
    
    # Download image
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{image_key}"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params={"type": "file"}
    )
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_dingtalk_image(download_code: str, output_path: str) -> str:
    """Download image from DingTalk."""
    app_key = os.environ.get("DINGTALK_APP_KEY")
    app_secret = os.environ.get("DINGTALK_APP_SECRET")
    
    if not app_key or not app_secret:
        raise ValueError("DINGTALK_APP_KEY and DINGTALK_APP_SECRET must be set")
    
    # Get access token
    resp = requests.post(
        "https://api.dingtalk.com/v1.0/oauth2/accessToken",
        json={"appKey": app_key, "appSecret": app_secret}
    )
    resp.raise_for_status()
    token = resp.json()["accessToken"]
    
    # Download image
    url = f"https://api.dingtalk.com/v1.0/robot/messageFiles/download?downloadCode={download_code}"
    resp = requests.get(
        url,
        headers={"x-acs-dingtalk-access-token": token}
    )
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_wechat_image(media_id: str, output_path: str) -> str:
    """Download image from WeChat (WeCom/企业微信)."""
    corp_id = os.environ.get("WECHAT_CORP_ID")
    corp_secret = os.environ.get("WECHAT_CORP_SECRET")
    
    if not corp_id or not corp_secret:
        raise ValueError("WECHAT_CORP_ID and WECHAT_CORP_SECRET must be set")
    
    # Get access token
    resp = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken",
        params={"corpid": corp_id, "corpsecret": corp_secret}
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    
    # Download media
    resp = requests.get(
        "https://qyapi.weixin.qq.com/cgi-bin/media/get",
        params={"access_token": token, "media_id": media_id}
    )
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_telegram_image(file_id: str, token: str, output_path: str) -> str:
    """Download image from Telegram."""
    # Get file path
    url = f"https://api.telegram.org/bot{token}/getFile"
    resp = requests.get(url, params={"file_id": file_id})
    resp.raise_for_status()
    
    file_path = resp.json()["result"]["file_path"]
    
    # Download file
    download_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    resp = requests.get(download_url)
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_discord_image(url: str, output_path: str) -> str:
    """Download image from Discord (direct URL)."""
    resp = requests.get(url)
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_whatsapp_image(media_id: str, token: str, output_path: str) -> str:
    """Download image from WhatsApp Business API."""
    # Get media URL
    url = f"https://graph.facebook.com/v17.0/{media_id}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    
    media_url = resp.json()["url"]
    
    # Download media
    resp = requests.get(media_url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_slack_image(file_id: str, token: str, output_path: str) -> str:
    """Download image from Slack."""
    # Get file info
    url = f"https://slack.com/api/files.info"
    resp = requests.get(url, params={"file": file_id}, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    
    download_url = resp.json()["file"]["url_private_download"]
    
    # Download file
    resp = requests.get(download_url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_line_image(message_id: str, token: str, output_path: str) -> str:
    """Download image from LINE."""
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def download_direct_url(url: str, output_path: str, headers: dict = None) -> str:
    """Download image from direct URL."""
    resp = requests.get(url, headers=headers or {})
    resp.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(resp.content)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Download images from chat platforms")
    parser.add_argument("--platform", 
        choices=["feishu", "dingtalk", "wechat", "discord", "telegram", "whatsapp", "slack", "line"], 
        help="Chat platform")
    parser.add_argument("--url", help="Direct image URL (for Discord or any direct link)")
    parser.add_argument("--message-id", help="Message ID (Feishu, LINE)")
    parser.add_argument("--image-key", help="Image key (Feishu)")
    parser.add_argument("--download-code", help="Download code (DingTalk)")
    parser.add_argument("--media-id", help="Media ID (WeChat, WhatsApp)")
    parser.add_argument("--file-id", help="File ID (Telegram, Slack)")
    parser.add_argument("--token", help="Bot/API token (Telegram, WhatsApp, Slack, LINE)")
    parser.add_argument("--output", default=None, help="Output file path")
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        fd, output_path = tempfile.mkstemp(suffix=".jpg", prefix="chat_img_")
        os.close(fd)
    
    try:
        if args.platform == "feishu":
            if not args.message_id or not args.image_key:
                print("Error: --message-id and --image-key required for Feishu", file=sys.stderr)
                sys.exit(1)
            download_feishu_image(args.message_id, args.image_key, output_path)
        
        elif args.platform == "dingtalk":
            if not args.download_code:
                print("Error: --download-code required for DingTalk", file=sys.stderr)
                sys.exit(1)
            download_dingtalk_image(args.download_code, output_path)
        
        elif args.platform == "wechat":
            if not args.media_id:
                print("Error: --media-id required for WeChat", file=sys.stderr)
                sys.exit(1)
            download_wechat_image(args.media_id, output_path)
        
        elif args.platform == "telegram":
            if not args.file_id or not args.token:
                print("Error: --file-id and --token required for Telegram", file=sys.stderr)
                sys.exit(1)
            download_telegram_image(args.file_id, args.token, output_path)
        
        elif args.platform == "discord":
            if not args.url:
                print("Error: --url required for Discord", file=sys.stderr)
                sys.exit(1)
            download_discord_image(args.url, output_path)
        
        elif args.platform == "whatsapp":
            if not args.media_id or not args.token:
                print("Error: --media-id and --token required for WhatsApp", file=sys.stderr)
                sys.exit(1)
            download_whatsapp_image(args.media_id, args.token, output_path)
        
        elif args.platform == "slack":
            if not args.file_id or not args.token:
                print("Error: --file-id and --token required for Slack", file=sys.stderr)
                sys.exit(1)
            download_slack_image(args.file_id, args.token, output_path)
        
        elif args.platform == "line":
            if not args.message_id or not args.token:
                print("Error: --message-id and --token required for LINE", file=sys.stderr)
                sys.exit(1)
            download_line_image(args.message_id, args.token, output_path)
        
        elif args.url:
            # Direct URL download
            download_direct_url(args.url, output_path)
        
        else:
            print("Error: Must specify --platform or --url", file=sys.stderr)
            sys.exit(1)
        
        print(output_path)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()