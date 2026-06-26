#!/usr/bin/env python3
"""
Feishu image pipeline filter.

Reads text from stdin, finds Markdown images ![alt](url),
downloads each image, uploads to Feishu to get an image_key,
and optionally sends each image as a Feishu image message.

Credentials are read from environment variables:
  FEISHU_APP_ID      — Feishu app ID
  FEISHU_APP_SECRET  — Feishu app secret

Usage:
  # Just replace URLs with image_keys (pipe mode):
  python3 web_search.py --images "query" | python3 feishu_image.py

  # Replace URLs AND send each image to a Feishu chat:
  python3 web_search.py --images "query" | python3 feishu_image.py --send --chat-id oc_xxxxx
"""
import sys
import os
import re
import json
import time
import tempfile
import ssl
import argparse
import urllib.request
import urllib.parse

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

TOKEN_CACHE_PATH = "/tmp/feishu_token.json"

FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_UPLOAD_URL = "https://open.feishu.cn/open-apis/im/v1/images"
FEISHU_SEND_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

MD_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def load_feishu_credentials():
    """Load credentials from env vars, with fallback to openclaw.json."""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if app_id and app_secret:
        return app_id, app_secret

    # Fallback: try openclaw.json in common locations
    for config_path in [
        os.path.join(os.path.dirname(__file__), "..", "..", "openclaw.json"),
        os.path.expanduser("~/openclaw/openclaw.json"),
        "/home/openclaw/openclaw.json",
    ]:
        config_path = os.path.realpath(config_path)
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    cfg = json.load(f)
                feishu = cfg["channels"]["feishu"]
                return feishu["appId"], feishu["appSecret"]
            except (json.JSONDecodeError, KeyError):
                continue

    print("Error: FEISHU_APP_ID and FEISHU_APP_SECRET not set.", file=sys.stderr)
    sys.exit(1)


def get_tenant_access_token(app_id, app_secret):
    """Get tenant_access_token, using a file cache to avoid repeated requests."""
    if os.path.exists(TOKEN_CACHE_PATH):
        try:
            with open(TOKEN_CACHE_PATH, "r") as f:
                cache = json.load(f)
            if cache.get("expire_at", 0) > time.time() + 60:
                return cache["token"]
        except (json.JSONDecodeError, KeyError):
            pass

    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret,
    }).encode("utf-8")

    req = urllib.request.Request(
        FEISHU_TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10, context=_ssl_ctx) as resp:
        data = json.loads(resp.read())

    if data.get("code") != 0:
        raise RuntimeError(f"Failed to get token: {data}")

    token = data["tenant_access_token"]
    expire = data.get("expire", 7200)

    with open(TOKEN_CACHE_PATH, "w") as f:
        json.dump({"token": token, "expire_at": time.time() + expire}, f)

    return token


def download_image(url, dest):
    """Download an image URL to a local file. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; FeishuImageBot/1.0)",
        })
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
            with open(dest, "wb") as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"[feishu_image] download failed {url}: {e}", file=sys.stderr)
        return False


def upload_image_to_feishu(filepath, token):
    """Upload a local image to Feishu and return its image_key."""
    import mimetypes
    boundary = "----FeishuImageBoundary"
    filename = os.path.basename(filepath)
    content_type = mimetypes.guess_type(filepath)[0] or "image/jpeg"

    with open(filepath, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image_type"\r\n\r\n'
        f"message\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        FEISHU_UPLOAD_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
        data = json.loads(resp.read())

    if data.get("code") != 0:
        raise RuntimeError(f"Upload failed: {data}")

    return data["data"]["image_key"]


def send_image_message(token, chat_id, image_key, receive_id_type="chat_id"):
    """Send an image message to a Feishu chat via /im/v1/messages API."""
    url = f"{FEISHU_SEND_MSG_URL}?receive_id_type={receive_id_type}"
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}),
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
        data = json.loads(resp.read())

    if data.get("code") != 0:
        print(f"[feishu_image] send failed: {data}", file=sys.stderr)
        return False

    msg_id = data.get("data", {}).get("message_id", "unknown")
    print(f"[feishu_image] sent image {image_key} -> msg {msg_id}", file=sys.stderr)
    return True


def process_text(text, send=False, chat_id=None, receive_id_type="chat_id"):
    """Replace ![alt](url) with ![alt](image_key) and optionally send images."""
    matches = list(MD_IMAGE_RE.finditer(text))
    if not matches:
        return text

    app_id, app_secret = load_feishu_credentials()
    token = get_tenant_access_token(app_id, app_secret)

    url_to_key = {}
    sent_keys = set()
    tmpdir = tempfile.mkdtemp(prefix="feishu_img_")

    try:
        for i, m in enumerate(matches):
            url = m.group(2)
            if url in url_to_key:
                continue
            if url.startswith("img_"):
                url_to_key[url] = url
                continue

            ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or ".jpg"
            dest = os.path.join(tmpdir, f"img_{i}{ext}")

            if download_image(url, dest):
                try:
                    image_key = upload_image_to_feishu(dest, token)
                    url_to_key[url] = image_key
                    print(f"[feishu_image] uploaded {url[:80]}... -> {image_key}", file=sys.stderr)
                except Exception as e:
                    print(f"[feishu_image] upload failed: {e}", file=sys.stderr)
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    if send and chat_id:
        for url in url_to_key:
            image_key = url_to_key[url]
            if image_key not in sent_keys:
                send_image_message(token, chat_id, image_key, receive_id_type)
                sent_keys.add(image_key)

    def replacer(m):
        alt = m.group(1)
        url = m.group(2)
        key = url_to_key.get(url, url)
        return f"![{alt}]({key})"

    return MD_IMAGE_RE.sub(replacer, text)


def main():
    p = argparse.ArgumentParser(description="Feishu image pipeline filter")
    p.add_argument("--send", action="store_true",
                   help="Send each image as a Feishu image message")
    p.add_argument("--chat-id", type=str, default=None,
                   help="Feishu chat_id / open_id to send images to")
    p.add_argument("--id-type", type=str, default="chat_id",
                   choices=["chat_id", "open_id", "user_id", "union_id", "email"],
                   help="receive_id_type (default: chat_id)")
    args = p.parse_args()

    if args.send and not args.chat_id:
        print("Error: --send requires --chat-id", file=sys.stderr)
        sys.exit(1)

    text = sys.stdin.read()
    result = process_text(text, send=args.send, chat_id=args.chat_id,
                          receive_id_type=args.id_type)
    print(result, end="")


if __name__ == "__main__":
    main()
