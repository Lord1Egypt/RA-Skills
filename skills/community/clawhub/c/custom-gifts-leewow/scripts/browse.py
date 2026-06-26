#!/usr/bin/env python3
"""Browse Leewow customizable product templates, output Markdown cards.

Cover images are downloaded to workspace so the agent can display them
in chat platforms that only support local file references.
"""

import argparse
import hashlib
import json
import os
import sys
from urllib.parse import urlparse

# Load environment variables from ~/.openclaw/.env
def _load_env_file():
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    if key not in os.environ:
                        os.environ[key] = value

_load_env_file()

import requests
from claw_auth import claw_get

CLAW_BASE_URL = os.getenv("CLAW_BASE_URL", "https://leewow.com")
CLAW_PATH_PREFIX = os.getenv("CLAW_PATH_PREFIX", "")
CLAW_SK = os.getenv("CLAW_SK", "")

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
TEMPLATE_IMG_DIR = os.path.join(WORKSPACE_DIR, "template_images")


def _download_cover_image(remote_url: str, template_id) -> str | None:
    """Download template cover image to workspace and return local path.

    Uses a content-hash filename so repeated calls are instant (cache hit).
    Returns None on failure — caller should fall back to remote URL.
    """
    if not remote_url:
        return None
    try:
        os.makedirs(TEMPLATE_IMG_DIR, exist_ok=True)
        url_hash = hashlib.md5(remote_url.encode()).hexdigest()[:10]
        parsed = urlparse(remote_url)
        ext = os.path.splitext(parsed.path)[1] or ".jpg"
        filename = f"template_{template_id}_{url_hash}{ext}"
        filepath = os.path.join(TEMPLATE_IMG_DIR, filename)

        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return filepath

        resp = requests.get(remote_url, timeout=15)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return filepath
    except Exception as e:
        print(f"Warning: failed to download cover image: {e}", file=sys.stderr)
        return None


def browse_templates(category: str = None, count: int = 10) -> list:
    """Return templates as a list of dicts, each with localImagePath for media sending."""
    if not CLAW_SK:
        return [{"error": "CLAW_SK environment variable is not set."}]

    count = min(max(count, 1), 20)
    url = f"{CLAW_BASE_URL}{CLAW_PATH_PREFIX}/claw/templates"

    try:
        resp = claw_get(CLAW_SK, url, timeout=15)
        data = resp.json()
    except Exception as e:
        return [{"error": f"Failed to fetch templates: {e}"}]

    if data.get("code") != 0:
        return [{"error": f"API returned: {data.get('message', 'Unknown error')}"}]

    templates = data.get("data", [])

    if category:
        cat_lower = category.lower()
        templates = [
            t for t in templates
            if cat_lower in (t.get("name", "") + t.get("description", "")).lower()
        ]

    templates = templates[:count]

    results = []
    for i, t in enumerate(templates, 1):
        tid = t.get("templateId", "?")
        name = t.get("name", "Unnamed Product")
        cover = t.get("coverImage", "")
        desc = t.get("description", "")
        sku_type = t.get("skuType", "")
        shipping = t.get("shippingOrigin", "CN")
        price_display = _extract_price(t.get("skuConfigs"))

        local_cover = _download_cover_image(cover, tid)

        results.append({
            "index": i,
            "templateId": tid,
            "name": name,
            "description": desc,
            "skuType": sku_type,
            "shippingOrigin": shipping,
            "price": price_display,
            "localImagePath": local_cover,
        })

    return results


def _extract_price(sku_configs) -> str:
    if not sku_configs:
        return ""
    try:
        skus = json.loads(sku_configs) if isinstance(sku_configs, str) else sku_configs
        if isinstance(skus, list) and skus:
            first = skus[0]
            price = first.get("priceOnSell") or first.get("price")
            origin = first.get("originPrice")
            currency = first.get("currency", "USD")
            if price:
                s = f"**${price} {currency}**"
                if origin and float(origin) > float(price):
                    s += f" ~~${origin}~~"
                return s
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
    return ""


def browse_templates_json(category: str = None, count: int = 10) -> list:
    """Return templates as JSON-serializable list."""
    if not CLAW_SK:
        return []

    count = min(max(count, 1), 20)
    url = f"{CLAW_BASE_URL}{CLAW_PATH_PREFIX}/claw/templates"

    try:
        resp = claw_get(CLAW_SK, url, timeout=15)
        data = resp.json()
    except Exception:
        return []

    if data.get("code") != 0:
        return []

    templates = data.get("data", [])

    if category:
        cat_lower = category.lower()
        templates = [
            t for t in templates
            if cat_lower in (t.get("name", "") + t.get("description", "")).lower()
        ]

    return templates[:count]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, default=None)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="(kept for compat, always outputs JSON)")
    args = parser.parse_args()

    templates = browse_templates(category=args.category, count=args.count)
    print(json.dumps(templates, ensure_ascii=False, indent=2))
