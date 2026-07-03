#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_to_wechat.py — Self-contained WeChat Official Account draft publisher.

Uploads HTML articles with cover images to the WeChat Official Account draft box
via the draft/add API. Handles access token, image upload to WeChat CDN, and
HTML image URL replacement.

Usage:
    WECHAT_APP_ID=wxXXX WECHAT_APP_SECRET=xxx \
    python publish_to_wechat.py \
        --file article.html \
        --title "Article Title" \
        --cover cover.png \
        --digest "Article summary" \
        --author "Author Name"

Environment Variables:
    WECHAT_APP_ID       - WeChat Official Account AppID (required)
    WECHAT_APP_SECRET   - WeChat Official Account AppSecret (required)
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("[INFO] Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


class WeChatPublisher:
    """WeChat Official Account HTML draft publisher."""

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def get_access_token(self) -> bool:
        """Fetch access token from WeChat API."""
        url = f"{self.BASE_URL}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            if "access_token" in data:
                self.access_token = data["access_token"]
                print("[OK] Access token obtained successfully")
                return True
            else:
                errcode = data.get("errcode", "unknown")
                errmsg = data.get("errmsg", "unknown error")

                # Specific error handling
                if errcode == 40164:
                    # IP whitelist error
                    ip_match = re.search(r"ipv6?\s+::ffff:([\d.]+)", errmsg)
                    if not ip_match:
                        ip_match = re.search(r"ip\s+([\d.]+)", errmsg)
                    ip_addr = ip_match.group(1) if ip_match else "unknown"
                    print(f"[ERROR] IP not in whitelist: {ip_addr}")
                    print(f"[ACTION] Please add IP {ip_addr} to your WeChat IP whitelist:")
                    print(f"         WeChat Backend -> Settings -> Basic Config -> IP Whitelist")
                    print(f"         URL: https://mp.weixin.qq.com/")
                elif errcode == 40125:
                    print("[ERROR] Invalid AppSecret. Please check your WECHAT_APP_SECRET.")
                elif errcode == 40120:
                    print("[ERROR] Invalid AppID. Please check your WECHAT_APP_ID.")
                else:
                    print(f"[ERROR] Failed to get access token: {errmsg} (errcode: {errcode})")
                return False
        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out. Please check your network connection.")
            return False
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            return False

    def upload_image(self, image_path: str):
        """
        Upload an image to WeChat CDN.

        Args:
            image_path: Local file path or HTTP(S) URL.

        Returns:
            Tuple of (media_id, url) on success, (None, None) on failure.
        """
        if not self.access_token:
            print("[ERROR] No access token. Call get_access_token() first.")
            return None, None

        # Handle URL vs local file
        if image_path.startswith(("http://", "https://")):
            try:
                resp = requests.get(image_path, timeout=15)
                resp.raise_for_status()
                image_data = resp.content
                filename = os.path.basename(urlparse(image_path).path) or "image.jpg"
            except Exception as e:
                print(f"[ERROR] Failed to download image {image_path}: {e}")
                return None, None
        else:
            path = Path(image_path)
            if not path.exists():
                print(f"[ERROR] Image file not found: {image_path}")
                return None, None
            with open(path, "rb") as f:
                image_data = f.read()
            filename = path.name

        # Determine content type
        ext = Path(filename).suffix.lower()
        content_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
        }
        content_type = content_types.get(ext, "image/jpeg")

        # Upload to WeChat material API
        url = f"{self.BASE_URL}/material/add_material"
        params = {"access_token": self.access_token, "type": "image"}
        files = {"media": (filename, image_data, content_type)}

        try:
            resp = requests.post(url, params=params, files=files, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if "url" in data and "media_id" in data:
                print(f"[OK] Image uploaded: {filename} -> {data['media_id'][:20]}...")
                return data["media_id"], data["url"]
            else:
                errmsg = data.get("errmsg", "unknown error")
                errcode = data.get("errcode", "unknown")
                print(f"[ERROR] Image upload failed: {errmsg} (errcode: {errcode})")
                return None, None
        except requests.exceptions.Timeout:
            print(f"[ERROR] Image upload timed out: {filename}")
            return None, None
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None, None

    def upload_content_image(self, image_path: str) -> str:
        """
        Upload an image for use within article content (not as cover).
        Returns the WeChat CDN URL for embedding in HTML.

        Args:
            image_path: Local file path or HTTP(S) URL.

        Returns:
            WeChat CDN URL on success, empty string on failure.
        """
        if not self.access_token:
            return ""

        if image_path.startswith(("http://", "https://")):
            try:
                resp = requests.get(image_path, timeout=15)
                resp.raise_for_status()
                image_data = resp.content
                filename = os.path.basename(urlparse(image_path).path) or "image.jpg"
            except Exception:
                return ""
        else:
            path = Path(image_path)
            if not path.exists():
                return ""
            with open(path, "rb") as f:
                image_data = f.read()
            filename = path.name

        url = f"{self.BASE_URL}/media/uploadimg"
        params = {"access_token": self.access_token}
        files = {"media": (filename, image_data, "image/jpeg")}

        try:
            resp = requests.post(url, params=params, files=files, timeout=30)
            data = resp.json()
            return data.get("url", "")
        except Exception:
            return ""

    def process_html_images(self, html_content: str, html_dir: str) -> str:
        """
        Find all images in HTML, upload to WeChat CDN, and replace URLs.

        Args:
            html_content: The HTML string to process.
            html_dir: Base directory for resolving relative image paths.

        Returns:
            HTML with all image URLs replaced to WeChat CDN URLs.
        """
        img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')

        def replace_image(match):
            src = match.group(1)

            # Skip already-hosted WeChat images
            if "mmbiz.qpic.cn" in src or "wx.qlogo.cn" in src:
                return match.group(0)

            # Skip data URIs
            if src.startswith("data:"):
                return match.group(0)

            # Resolve relative paths
            if not src.startswith(("http://", "https://", "/")):
                src = os.path.join(html_dir, src)

            print(f"[UPLOAD] Processing image: {src}")
            _, new_url = self.upload_image(src)

            if new_url:
                return match.group(0).replace(match.group(1), new_url)
            else:
                print(f"[WARN] Image upload failed, keeping original URL: {src}")
                return match.group(0)

        return img_pattern.sub(replace_image, html_content)

    def publish_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: str,
        author: str = "",
        digest: str = "",
        source_url: str = "",
    ) -> str:
        """
        Publish an article to the WeChat draft box.

        Args:
            title: Article title.
            content: HTML content (must use inline styles).
            thumb_media_id: Media ID of the cover/thumbnail image.
            author: Optional author name.
            digest: Optional article summary (shown in article list).
            source_url: Optional "Read More" link URL.

        Returns:
            Media ID of the created draft on success, empty string on failure.
        """
        if not self.access_token:
            print("[ERROR] No access token. Call get_access_token() first.")
            return ""

        url = f"{self.BASE_URL}/draft/add"
        params = {"access_token": self.access_token}

        data = {
            "articles": [
                {
                    "title": title,
                    "author": author,
                    "digest": digest,
                    "content": content,
                    "content_source_url": source_url,
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 0,
                    "only_fans_can_comment": 0,
                }
            ]
        }

        try:
            json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
            headers = {"Content-Type": "application/json; charset=utf-8"}

            resp = requests.post(url, params=params, data=json_data, headers=headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()

            if "media_id" in result:
                print("[SUCCESS] Draft published successfully!")
                print(f"[INFO] Media ID: {result['media_id']}")
                return result["media_id"]
            else:
                errcode = result.get("errcode", "unknown")
                errmsg = result.get("errmsg", "unknown error")
                print(f"[ERROR] Publish failed: {errmsg} (errcode: {errcode})")

                if errcode == 45009:
                    print("[ERROR] API call limit reached. Please wait and try again.")
                elif errcode == 45028:
                    print("[ERROR] No publishing quota left for today.")
                elif errcode == 48001:
                    print("[ERROR] API not authorized. Check your account permissions.")
                return ""
        except requests.exceptions.Timeout:
            print("[ERROR] Publish request timed out.")
            return ""
        except Exception as e:
            print(f"[ERROR] Publish request failed: {e}")
            return ""


def validate_html(file_path: str) -> tuple:
    """
    Validate HTML file for WeChat compatibility.

    Returns:
        Tuple of (is_valid, warnings_list)
    """
    content = Path(file_path).read_text(encoding="utf-8")
    warnings = []

    # Check file size (2MB limit)
    size = len(content.encode("utf-8"))
    if size > 2 * 1024 * 1024:
        warnings.append(f"HTML file is {size / 1024 / 1024:.1f}MB, exceeds WeChat's 2MB limit")

    # Check for style tags
    if re.search(r"<style", content, re.IGNORECASE):
        warnings.append("Contains <style> tags — WeChat will strip these. Run convert_for_wechat.py first.")

    # Check for CSS variables
    if "var(--" in content:
        warnings.append("Contains CSS variables (var(--...)) — WeChat will strip these.")

    # Check for scripts
    if re.search(r"<script", content, re.IGNORECASE):
        warnings.append("Contains <script> tags — not supported by WeChat.")

    is_valid = len([w for w in warnings if "exceeds" in w or "strip" in w]) == 0
    return is_valid, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Publish HTML article to WeChat Official Account draft box",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic publish
  python publish_to_wechat.py --file article.html --title "My Article" --cover cover.jpg

  # With author and digest
  python publish_to_wechat.py --file article.html --title "My Article" \\
      --cover cover.jpg --author "Author" --digest "Article summary"

  # Validate only (no publish)
  python publish_to_wechat.py --file article.html --validate-only

Environment Variables:
  WECHAT_APP_ID       WeChat Official Account AppID (required)
  WECHAT_APP_SECRET   WeChat Official Account AppSecret (required)
        """,
    )
    parser.add_argument("--file", required=True, help="HTML file path (must use inline styles)")
    parser.add_argument("--title", help="Article title (required unless --validate-only)")
    parser.add_argument("--cover", required=True, help="Cover image path (local file or URL)")
    parser.add_argument("--author", default="", help="Author name (optional)")
    parser.add_argument("--digest", default="", help="Article summary for preview (optional, max 120 chars)")
    parser.add_argument("--source-url", default="", help='"Read More" link URL (optional)')
    parser.add_argument("--validate-only", action="store_true", help="Only validate HTML, do not publish")
    parser.add_argument("--skip-image-upload", action="store_true", help="Skip uploading images in HTML content")

    args = parser.parse_args()

    # Validate file exists
    html_file = Path(args.file)
    if not html_file.exists():
        print(f"[ERROR] HTML file not found: {args.file}")
        sys.exit(1)

    # Validate HTML
    is_valid, warnings = validate_html(args.file)
    if warnings:
        print("[WARN] HTML validation warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("[OK] HTML validation passed")

    if args.validate_only:
        sys.exit(0 if is_valid else 1)

    if not is_valid:
        print("[ERROR] HTML validation failed. Fix the issues above or run convert_for_wechat.py first.")
        sys.exit(1)

    # Check required args
    if not args.title:
        print("[ERROR] --title is required for publishing")
        sys.exit(1)

    # Get credentials
    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if not app_id or not app_secret:
        print()
        print("=" * 60)
        print("  WeChat Official Account credentials required")
        print("=" * 60)
        print()
        print("  To get your credentials:")
        print("  1. Log in to https://mp.weixin.qq.com/")
        print("  2. Go to: Settings -> Basic Config")
        print("  3. Copy your AppID and reset/view AppSecret")
        print("  4. Add your server IP to the IP whitelist")
        print()
        print("  Or set environment variables to skip this prompt:")
        print('    export WECHAT_APP_ID="your_appid"')
        print('    export WECHAT_APP_SECRET="your_appsecret"')
        print()

        if not app_id:
            app_id = input("  AppID: ").strip()
        if not app_secret:
            app_secret = input("  AppSecret: ").strip()

        if not app_id or not app_secret:
            print("[ERROR] Credentials cannot be empty.")
            sys.exit(1)

        print()
        print("[OK] Credentials received. Proceeding...")

    # Read HTML
    html_content = html_file.read_text(encoding="utf-8")
    print(f"[FILE] Loaded HTML: {args.file} ({len(html_content)} chars)")

    # Initialize publisher
    publisher = WeChatPublisher(app_id, app_secret)

    # Get access token
    if not publisher.get_access_token():
        sys.exit(1)

    # Upload cover image
    print(f"[UPLOAD] Uploading cover image: {args.cover}")
    thumb_media_id, cover_url = publisher.upload_image(args.cover)
    if not thumb_media_id:
        print("[ERROR] Cover image upload failed. Cannot proceed without cover.")
        sys.exit(1)

    # Process HTML images (upload embedded images)
    if not args.skip_image_upload:
        print("[PROCESS] Processing images in HTML...")
        html_dir = str(html_file.parent)
        html_content = publisher.process_html_images(html_content, html_dir)

    # Truncate digest if too long
    digest = args.digest[:120] if args.digest else ""

    # Publish draft
    print("[PUBLISH] Publishing to draft box...")
    media_id = publisher.publish_draft(
        title=args.title,
        content=html_content,
        thumb_media_id=thumb_media_id,
        author=args.author,
        digest=digest,
        source_url=args.source_url,
    )

    if media_id:
        print()
        print("=" * 50)
        print("  PUBLISHED SUCCESSFULLY!")
        print(f"  Media ID: {media_id}")
        print(f"  Review at: https://mp.weixin.qq.com/")
        print("=" * 50)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
