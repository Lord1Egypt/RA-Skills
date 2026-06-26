#!/usr/bin/env python3
"""Ghost-Writer Sync — Pull published blog posts into a local knowledge vault.

Supports:
  - Substack (via public RSS feed)
  - Ghost (via Content API with Admin API key)

Outputs:
  - Markdown files compatible with Obsidian and Logseq
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# HTML → Markdown converter (stdlib only)
# ---------------------------------------------------------------------------

class HTMLToMarkdown(HTMLParser):
    """Minimal HTML-to-Markdown converter using only the stdlib."""

    BLOCK_TAGS = {"p", "div", "section", "article", "blockquote", "li"}
    VOID_TAGS = {"br", "hr", "img", "input", "meta", "link"}

    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._tag_stack: list[str] = []
        self._in_pre = False
        self._in_code = False
        self._in_list = False
        self._list_type: str | None = None  # "ul" or "ol"
        self._list_counter = 0
        self._in_link = False
        self._link_href = ""
        self._link_text_parts: list[str] = []
        self._in_image = False
        self._image_attrs: dict = {}

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)
        self._tag_stack.append(tag)

        if tag == "h1":
            self._parts.append("\n# ")
        elif tag == "h2":
            self._parts.append("\n## ")
        elif tag == "h3":
            self._parts.append("\n### ")
        elif tag == "h4":
            self._parts.append("\n#### ")
        elif tag == "h5":
            self._parts.append("\n##### ")
        elif tag == "h6":
            self._parts.append("\n###### ")
        elif tag == "p":
            self._parts.append("\n\n")
        elif tag == "br":
            self._parts.append("\n")
        elif tag == "hr":
            self._parts.append("\n---\n")
        elif tag == "strong" or tag == "b":
            self._parts.append("**")
        elif tag == "em" or tag == "i":
            self._parts.append("*")
        elif tag == "code":
            self._in_code = True
            if self._in_pre:
                self._parts.append("```")  # skip inline code inside pre
            else:
                self._parts.append("`")
        elif tag == "pre":
            self._in_pre = True
            self._parts.append("\n```\n")
        elif tag == "blockquote":
            self._parts.append("\n> ")
        elif tag == "ul":
            self._in_list = True
            self._list_type = "ul"
        elif tag == "ol":
            self._in_list = True
            self._list_type = "ol"
            self._list_counter = 1
        elif tag == "li":
            if self._list_type == "ol":
                self._parts.append(f"\n{self._list_counter}. ")
                self._list_counter += 1
            else:
                self._parts.append("\n- ")
        elif tag == "a":
            self._in_link = True
            self._link_href = attrs_dict.get("href", "")
            self._link_text_parts = []
        elif tag == "img":
            alt = attrs_dict.get("alt", "")
            src = attrs_dict.get("src", "")
            self._parts.append(f"\n![{alt}]({src})\n")
        elif tag in ("figure", "figcaption"):
            pass  # handled by children

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()

        if tag == "strong" or tag == "b":
            self._parts.append("**")
        elif tag == "em" or tag == "i":
            self._parts.append("*")
        elif tag == "code":
            self._in_code = False
            if self._in_pre:
                pass
            else:
                self._parts.append("`")
        elif tag == "pre":
            self._in_pre = False
            self._parts.append("\n```\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._parts.append("\n")
        elif tag == "a":
            self._in_link = False
            link_text = "".join(self._link_text_parts).strip()
            if self._link_href and link_text:
                self._parts.append(f"[{link_text}]({self._link_href})")
            elif link_text:
                self._parts.append(link_text)
        elif tag == "ul" or tag == "ol":
            self._in_list = False
            self._list_type = None
        elif tag == "blockquote":
            self._parts.append("\n")

    def handle_data(self, data):
        if self._in_link:
            self._link_text_parts.append(data)
        else:
            self._parts.append(data)

    def get_markdown(self) -> str:
        raw = "".join(self._parts)
        # Collapse 3+ newlines to 2
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_markdown(html: str) -> str:
    """Convert an HTML string to Markdown."""
    converter = HTMLToMarkdown()
    converter.feed(html)
    return converter.get_markdown()


# ---------------------------------------------------------------------------
# Slug / filename helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Turn a title into a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def post_id_from_url(url: str) -> str:
    """Derive a short stable ID from a URL (first 12 chars of SHA-256)."""
    return hashlib.sha256(url.encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Substack source — uses the public RSS feed (no API key needed)
# ---------------------------------------------------------------------------

def fetch_substack_posts(publication_url: str, limit: int = 50) -> list[dict]:
    """Fetch published posts from a Substack RSS feed.

    Args:
        publication_url: e.g. "https://example.substack.com"
        limit: max posts to return (default 50)
    """
    feed_url = publication_url.rstrip("/") + "/feed"
    posts = []

    try:
        req = urllib.request.Request(feed_url, headers={"User-Agent": "Ghost-Writer-Sync/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            rss_data = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"Error fetching Substack feed: {e}", file=sys.stderr)
        return []

    root = ET.fromstring(rss_data)
    channel = root.find("channel")
    if channel is None:
        return []

    for item in channel.findall("item")[:limit]:
        title_el = item.find("title")
        link_el = item.find("link")
        date_el = item.find("pubDate")
        desc_el = item.find("description")
        content_el = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")

        title = title_el.text if title_el is not None else "Untitled"
        link = link_el.text if link_el is not None else ""
        pub_date = ""
        if date_el is not None and date_el.text:
            try:
                dt = parsedate_to_datetime(date_el.text)
                pub_date = dt.strftime("%Y-%m-%d")
            except Exception:
                pub_date = date_el.text[:10]

        html_body = ""
        if content_el is not None and content_el.text:
            html_body = content_el.text
        elif desc_el is not None and desc_el.text:
            html_body = desc_el.text

        posts.append({
            "title": title,
            "url": link,
            "published_at": pub_date,
            "source": "substack",
            "html_body": html_body,
            "post_id": post_id_from_url(link),
        })

    return posts


# ---------------------------------------------------------------------------
# Ghost source — uses the Content API
# ---------------------------------------------------------------------------

def _ghost_jwt_token(api_key: str) -> str:
    """Build a Ghost Admin API JWT from an id:secret key (no external deps).

    Uses only stdlib to create an unsigned HS256 JWT. The Ghost Content API
    accepts these tokens for authentication.
    """
    import base64
    import hmac
    import struct

    parts = api_key.split(":")
    if len(parts) != 2:
        raise ValueError("Ghost API key must be in 'id:secret' format")

    key_id, secret_hex = parts
    secret = bytes.fromhex(secret_hex)

    now = int(time.time())
    # JWT header
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).rstrip(b"=")
    # JWT payload
    payload = base64.urlsafe_b64encode(
        json.dumps({"iat": now, "exp": now + 300, "aud": "/admin/"}).encode()
    ).rstrip(b"=")

    signing_input = header + b"." + payload
    signature = base64.urlsafe_b64encode(
        hmac.new(secret, signing_input, hashlib.sha256).digest()
    ).rstrip(b"=")

    return signing_input.decode() + "." + signature.decode()


def fetch_ghost_posts(site_url: str, api_key: str, limit: int = 50) -> list[dict]:
    """Fetch published posts from a Ghost CMS via Content API.

    Args:
        site_url: e.g. "https://myblog.ghost.io"
        api_key: Ghost Content API key ("id:secret" format)
        limit: max posts to return (default 50)
    """
    token = _ghost_jwt_token(api_key)
    api_url = site_url.rstrip("/") + f"/ghost/api/admin/posts/?limit={limit}&order=published_at%20desc&formats=html"

    try:
        req = urllib.request.Request(
            api_url,
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "Ghost-Writer-Sync/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Error fetching Ghost posts: {e}", file=sys.stderr)
        return []

    posts = []
    for p in data.get("posts", []):
        url = p.get("url", "")
        posts.append({
            "title": p.get("title", "Untitled"),
            "url": url,
            "published_at": (p.get("published_at") or "")[:10],
            "source": "ghost",
            "html_body": p.get("html", ""),
            "post_id": post_id_from_url(url),
            "tags": [t.get("name", "") for t in p.get("tags", [])],
            "excerpt": p.get("excerpt", ""),
            "feature_image": p.get("feature_image", ""),
        })

    return posts


# ---------------------------------------------------------------------------
# Markdown file writer
# ---------------------------------------------------------------------------

def _yaml_quote(value: str) -> str:
    """Quote a YAML scalar if it contains special characters."""
    if not value:
        return '""'
    if any(c in value for c in (":", "#", '"', "'", "\n", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`")):
        return json.dumps(value)
    return value


def _frontmatter(post: dict) -> str:
    """Build a YAML frontmatter block for a post."""
    lines = ["---"]
    lines.append(f"title: {_yaml_quote(post['title'])}")
    lines.append(f"source: {post['source']}")
    lines.append(f"url: {post['url']}")
    lines.append(f"published: {post.get('published_at', '')}")
    lines.append(f"synced: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"post_id: {post['post_id']}")

    tags = post.get("tags", [])
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {_yaml_quote(t)}")

    feature = post.get("feature_image", "")
    if feature:
        lines.append(f"feature_image: {feature}")

    excerpt = post.get("excerpt", "")
    if excerpt:
        lines.append(f"excerpt: {_yaml_quote(excerpt)}")

    lines.append("---")
    return "\n".join(lines)


def write_post(post: dict, vault_dir: str, fmt: str = "obsidian") -> str:
    """Write a single post as a Markdown file in the vault.

    Args:
        post: post dict from fetch_*_posts()
        vault_dir: path to Obsidian/Logseq vault
        fmt: "obsidian" (YAML frontmatter) or "logseq" (org-style properties)

    Returns:
        Path of the written file.
    """
    slug = slugify(post["title"])
    date_prefix = post.get("published_at", "unknown")
    if fmt == "logseq":
        filename = f"{date_prefix} {slug}.md"
    else:
        filename = f"{slug}.md"

    out_dir = Path(vault_dir) / "Ghost-Writer"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    body = html_to_markdown(post["html_body"])

    if fmt == "logseq":
        # Logseq format: properties block at the top
        prop_lines = [
            f"title:: {post['title']}",
            f"source:: {post['source']}",
            f"url:: {post['url']}",
            f"published:: {post.get('published_at', '')}",
            f"synced:: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        ]
        tags = post.get("tags", [])
        if tags:
            prop_lines.append(f"tags:: {', '.join(tags)}")
        content = "\n".join(prop_lines) + "\n\n" + body
    else:
        # Obsidian format: YAML frontmatter
        content = _frontmatter(post) + "\n\n" + body

    out_path.write_text(content, encoding="utf-8")
    return str(out_path)


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "vault_path": "",
    "format": "obsidian",
    "sources": {
        "substack": [],
        "ghost": [],
    },
}


def load_config(config_path: str) -> dict:
    """Load sync config from JSON file, creating default if missing."""
    path = Path(config_path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return dict(DEFAULT_CONFIG)


def save_config(config: dict, config_path: str) -> None:
    """Save config to JSON file."""
    Path(config_path).write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Sync engine
# ---------------------------------------------------------------------------

def sync(config: dict, config_path: str | None = None) -> list[str]:
    """Run a full sync according to config. Returns list of written file paths."""
    vault = config.get("vault_path", "")
    if not vault:
        print("Error: vault_path not set in config.", file=sys.stderr)
        return []

    fmt = config.get("format", "obsidian")
    sources = config.get("sources", {})
    written = []

    # Substack sources
    for entry in sources.get("substack", []):
        url = entry if isinstance(entry, str) else entry.get("url", "")
        if not url:
            continue
        print(f"Fetching Substack: {url}")
        posts = fetch_substack_posts(url)
        print(f"  Found {len(posts)} post(s)")
        for post in posts:
            path = write_post(post, vault, fmt)
            written.append(path)

    # Ghost sources
    for entry in sources.get("ghost", []):
        if isinstance(entry, dict):
            url = entry.get("url", "")
            key = entry.get("api_key", "")
        else:
            continue
        if not url or not key:
            continue
        print(f"Fetching Ghost: {url}")
        posts = fetch_ghost_posts(url, key)
        print(f"  Found {len(posts)} post(s)")
        for post in posts:
            path = write_post(post, vault, fmt)
            written.append(path)

    print(f"\nSync complete. {len(written)} file(s) written to {vault}")
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Ghost-Writer Sync — pull blog posts into your vault"
    )
    parser.add_argument(
        "command",
        choices=["sync", "add-substack", "add-ghost", "config", "list"],
        help="Action to perform",
    )
    parser.add_argument("--config", default="ghost-writer-sync.json", help="Config file path")
    parser.add_argument("--vault", help="Vault directory (overrides config)")
    parser.add_argument("--format", choices=["obsidian", "logseq"], help="Output format")
    parser.add_argument("--url", help="Publication URL (for add-substack/add-ghost)")
    parser.add_argument("--api-key", help="Ghost API key (for add-ghost)")
    parser.add_argument("--limit", type=int, default=50, help="Max posts per source")

    args = parser.parse_args()
    cfg = load_config(args.config)

    # Override config with CLI flags
    if args.vault:
        cfg["vault_path"] = args.vault
    if args.format:
        cfg["format"] = args.format

    if args.command == "config":
        print(json.dumps(cfg, indent=2))
    elif args.command == "list":
        sources = cfg.get("sources", {})
        subs = sources.get("substack", [])
        ghosts = sources.get("ghost", [])
        print(f"Vault: {cfg.get('vault_path', '(not set)')}")
        print(f"Format: {cfg.get('format', 'obsidian')}")
        print(f"\nSubstack sources ({len(subs)}):")
        for s in subs:
            url = s if isinstance(s, str) else s.get("url", "?")
            print(f"  - {url}")
        print(f"\nGhost sources ({len(ghosts)}):")
        for g in ghosts:
            if isinstance(g, dict):
                print(f"  - {g.get('url', '?')}")
            else:
                print(f"  - {g}")
    elif args.command == "add-substack":
        if not args.url:
            print("Error: --url is required for add-substack", file=sys.stderr)
            sys.exit(1)
        cfg.setdefault("sources", {}).setdefault("substack", []).append(args.url)
        save_config(cfg, args.config)
        print(f"Added Substack source: {args.url}")
    elif args.command == "add-ghost":
        if not args.url or not args.api_key:
            print("Error: --url and --api-key are required for add-ghost", file=sys.stderr)
            sys.exit(1)
        cfg.setdefault("sources", {}).setdefault("ghost", []).append({
            "url": args.url,
            "api_key": args.api_key,
        })
        save_config(cfg, args.config)
        print(f"Added Ghost source: {args.url}")
    elif args.command == "sync":
        paths = sync(cfg)
        if not paths:
            if not cfg.get("vault_path"):
                print("No vault configured. Run: sync.py add-substack --url <URL> --vault <PATH>")
            else:
                print("No posts found or no sources configured.")


if __name__ == "__main__":
    main()
