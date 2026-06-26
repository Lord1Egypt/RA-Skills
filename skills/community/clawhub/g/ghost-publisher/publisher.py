#!/usr/bin/env python3
"""
Ghost Publisher -- reference implementation of Publisher Interface v1 for Ghost 5.x.

Reads GHOST_URL and GHOST_ADMIN_API_KEY from environment variables.
Optionally reads a JSON config file via GHOST_PUBLISHER_CONFIG for non-secret
settings (default author, agent->author map, newsletter ID, max image size).

Exposes both:
  (a) A Python class `GhostPublisher` implementing the seven Publisher
      Interface v1 methods (createPost, updatePost, publishPost,
      schedulePost, deletePost, uploadImage, getPost).
  (b) A CLI wrapper for one-shot invocations (create-draft, update-content,
      set-image, publish, schedule, delete, get, upload-image, create-publish).

See INTERFACE.md for the full interface spec.
"""

import sys
import os
import json
import time
import re
import hashlib
import hmac
import base64
import argparse
import mimetypes
import urllib.request
import urllib.error
import uuid
from pathlib import Path


# =============================================================================
# Config
# =============================================================================

DEFAULT_MAX_IMAGE_MB = 2


def load_config(path=None):
    """Load optional non-secret config from JSON file. Returns a dict with
    safe defaults if the file is missing."""
    cfg = {
        "default_author_id": None,
        "agent_author_map": {},
        "newsletter_id": None,
        "max_image_size_mb": DEFAULT_MAX_IMAGE_MB,
    }
    if path is None:
        path = os.environ.get("GHOST_PUBLISHER_CONFIG")
    if not path:
        return cfg
    p = Path(path)
    if not p.exists():
        return cfg
    try:
        user_cfg = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"WARN: could not parse config at {path}: {e}", file=sys.stderr)
        return cfg
    for k in cfg:
        if k in user_cfg:
            cfg[k] = user_cfg[k]
    return cfg


def get_env_config():
    url = os.environ.get("GHOST_URL", "").rstrip("/")
    key = os.environ.get("GHOST_ADMIN_API_KEY", "")
    if not url:
        raise RuntimeError(
            "GHOST_URL environment variable not set. "
            "Set it to your Ghost site URL, e.g. https://yoursite.com"
        )
    if not key or ":" not in key:
        raise RuntimeError(
            "GHOST_ADMIN_API_KEY environment variable not set or malformed. "
            "Expected format <key_id>:<hex_secret> from Ghost Admin > Integrations."
        )
    return url, key


# =============================================================================
# JWT generation
# =============================================================================

def generate_jwt(admin_api_key):
    key_id, secret_hex = admin_api_key.split(":", 1)
    secret = bytes.fromhex(secret_hex)
    now = int(time.time())
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "kid": key_id, "typ": "JWT"}).encode()
    ).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(
        json.dumps({"iat": now, "exp": now + 300, "aud": "/admin/"}).encode()
    ).rstrip(b"=").decode()
    signing_input = f"{header}.{payload}"
    sig = base64.urlsafe_b64encode(
        hmac.new(secret, signing_input.encode(), hashlib.sha256).digest()
    ).rstrip(b"=").decode()
    return f"{signing_input}.{sig}"


# =============================================================================
# Lexical node builders
# =============================================================================

def _text_node(text, fmt=0):
    return {"detail": 0, "format": fmt, "mode": "normal",
            "style": "", "text": text, "type": "text", "version": 1}


def _link_node(children, url):
    return {"children": children, "direction": "ltr", "format": "",
            "indent": 0, "rel": "noopener noreferrer", "target": None,
            "title": None, "type": "link", "url": url, "version": 1}


def _paragraph_node(children):
    return {"children": children, "direction": "ltr", "format": "",
            "indent": 0, "type": "paragraph", "version": 1}


def _heading_node(children, tag):
    return {"children": children, "direction": "ltr", "format": "",
            "indent": 0, "tag": tag, "type": "heading", "version": 1}


def _listitem_node(children, value):
    return {"children": children, "direction": "ltr", "format": "",
            "indent": 0, "type": "listitem", "value": value, "version": 1}


def _list_node(items, ordered=False):
    return {"children": items, "direction": "ltr", "format": "", "indent": 0,
            "listType": "number" if ordered else "bullet",
            "start": 1, "tag": "ol" if ordered else "ul",
            "type": "list", "version": 1}


def _blockquote_node(children):
    return {"children": children, "direction": "ltr", "format": "",
            "indent": 0, "type": "quote", "version": 1}


def _hr_node():
    return {"type": "horizontalrule", "version": 1}


# =============================================================================
# Markdown -> Lexical
# =============================================================================

INLINE_RE = re.compile(
    r'\*\*\*(.+?)\*\*\*'
    r'|\*\*(.+?)\*\*'
    r'|___(.+?)___'
    r'|__(.+?)__'
    r'|\[([^\]]+)\]\(([^)\s]+)\)'
    r'|(?<!\*)\*([^*\n]+?)\*(?!\*)'
    r'|_([^_\n]+?)_'
    r'|`([^`]+)`'
)


def parse_inline(text):
    nodes = []
    last = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > last:
            plain = text[last:m.start()]
            if plain:
                nodes.append(_text_node(plain))
        g = m.groups()
        if g[0]:
            nodes.append(_text_node(g[0], 3))
        elif g[1]:
            nodes.append(_text_node(g[1], 1))
        elif g[2]:
            nodes.append(_text_node(g[2], 3))
        elif g[3]:
            nodes.append(_text_node(g[3], 1))
        elif g[4] and g[5]:
            nodes.append(_link_node([_text_node(g[4])], g[5]))
        elif g[6]:
            nodes.append(_text_node(g[6], 2))
        elif g[7]:
            nodes.append(_text_node(g[7], 2))
        elif g[8]:
            nodes.append(_text_node(g[8], 16))
        last = m.end()
    if last < len(text):
        tail = text[last:]
        if tail:
            nodes.append(_text_node(tail))
    return nodes or [_text_node(text)]


UL_LINE = re.compile(r'^[-*+]\s+(.+)$')
OL_LINE = re.compile(r'^\d+\.\s+(.+)$')
BQ_LINE = re.compile(r'^>\s*(.*)$')


def parse_blocks(md_text):
    md_text = md_text.replace('\r\n', '\n').strip()
    lines_all = md_text.split('\n')
    if lines_all and lines_all[0].startswith('# '):
        lines_all = lines_all[1:]
    md_text = '\n'.join(lines_all).lstrip('\n')

    raw_blocks = re.split(r'\n\n+', md_text)
    nodes = []

    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue

        if re.match(r'^[-*_]{3,}$', block):
            nodes.append(_hr_node())
            continue

        m = re.match(r'^(#{1,4})\s+(.+)$', block, re.DOTALL)
        if m:
            tag = f"h{len(m.group(1))}"
            nodes.append(_heading_node(parse_inline(m.group(2).strip()), tag))
            continue

        lines = [l for l in block.split('\n') if l.strip()]

        if lines and all(BQ_LINE.match(l.strip()) for l in lines):
            combined = ' '.join(BQ_LINE.match(l.strip()).group(1) for l in lines)
            nodes.append(_blockquote_node(parse_inline(combined)))
            continue

        if lines and all(OL_LINE.match(l.strip()) for l in lines):
            items = [_listitem_node(parse_inline(OL_LINE.match(l.strip()).group(1)), i + 1)
                     for i, l in enumerate(lines)]
            nodes.append(_list_node(items, ordered=True))
            continue

        if lines and all(UL_LINE.match(l.strip()) for l in lines):
            items = [_listitem_node(parse_inline(UL_LINE.match(l.strip()).group(1)), i + 1)
                     for i, l in enumerate(lines)]
            nodes.append(_list_node(items, ordered=False))
            continue

        has_list = any(UL_LINE.match(l.strip()) or OL_LINE.match(l.strip()) for l in lines)
        if has_list:
            para_acc, list_acc = [], []
            ordered = [False]  # boxed so nested closures can mutate

            def flush_para():
                if para_acc:
                    nodes.append(_paragraph_node(parse_inline(' '.join(para_acc))))
                    para_acc.clear()

            def flush_list():
                if list_acc:
                    items = [_listitem_node(parse_inline(t), i + 1)
                             for i, t in enumerate(list_acc)]
                    nodes.append(_list_node(items, ordered=ordered[0]))
                    list_acc.clear()

            for line in lines:
                ul = UL_LINE.match(line.strip())
                ol = OL_LINE.match(line.strip())
                if ul:
                    flush_para(); ordered[0] = False; list_acc.append(ul.group(1))
                elif ol:
                    flush_para(); ordered[0] = True; list_acc.append(ol.group(1))
                else:
                    flush_list(); para_acc.append(line.strip())
            flush_para()
            flush_list()
            continue

        para_text = ' '.join(l.strip() for l in lines)
        nodes.append(_paragraph_node(parse_inline(para_text)))

    return nodes


def markdown_to_lexical(md_text):
    children = parse_blocks(md_text)
    return json.dumps({
        "root": {
            "children": children,
            "direction": "ltr", "format": "", "indent": 0,
            "type": "root", "version": 1
        }
    })


# =============================================================================
# HTTP helpers
# =============================================================================

def _ghost_get(ghost_url, jwt, path):
    url = f"{ghost_url}/ghost/api/admin/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Ghost {jwt}", "Accept": "application/json"
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def _ghost_send(ghost_url, jwt, path, body_dict, method="POST"):
    url = f"{ghost_url}/ghost/api/admin/{path}"
    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Ghost {jwt}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as r:
            data = r.read()
            return json.loads(data) if data else {}
    except urllib.error.HTTPError as e:
        body_err = e.read().decode(errors="replace")
        raise RuntimeError(f"Ghost API HTTP {e.code}: {body_err}") from e


def _ghost_multipart_upload(ghost_url, jwt, file_bytes, filename, mime_type,
                            purpose="image", alt=None):
    """Upload a file to Ghost's /images/upload/ endpoint using multipart/form-data.
    Returns the Ghost-hosted URL."""
    boundary = f"----ghostpublisher{uuid.uuid4().hex}"
    crlf = b"\r\n"
    parts = []

    def add_field(name, value):
        parts.append(f"--{boundary}".encode())
        parts.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        parts.append(b"")
        parts.append(str(value).encode())

    parts.append(f"--{boundary}".encode())
    parts.append(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode()
    )
    parts.append(f"Content-Type: {mime_type}".encode())
    parts.append(b"")
    parts.append(file_bytes)

    add_field("purpose", purpose)
    if alt:
        add_field("ref", alt)

    parts.append(f"--{boundary}--".encode())
    parts.append(b"")
    body = crlf.join(parts)

    url = f"{ghost_url}/ghost/api/admin/images/upload/"
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Ghost {jwt}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_err = e.read().decode(errors="replace")
        raise RuntimeError(f"Ghost image upload HTTP {e.code}: {body_err}") from e
    images = data.get("images") or []
    if not images or "url" not in images[0]:
        raise RuntimeError(f"Ghost image upload returned unexpected payload: {data}")
    return images[0]["url"]


# =============================================================================
# Standard post <-> Ghost post mapping
# =============================================================================

def _resolve_author(post, config):
    """Map `author` (caller-side ID) to a Ghost staff ID via agent_author_map.
    Returns a Ghost-shaped authors list or None if nothing to set."""
    author = post.get("author")
    if not author:
        default_id = config.get("default_author_id")
        return [{"id": default_id}] if default_id else None
    mapping = config.get("agent_author_map") or {}
    staff_id = mapping.get(author)
    if staff_id:
        return [{"id": staff_id}]
    # Fall back to slug-style match (Ghost also accepts slug lookups)
    default_id = config.get("default_author_id")
    if default_id:
        return [{"id": default_id}]
    return None


def _standard_to_ghost(post, config):
    """Translate a standard Publisher Interface v1 post object into a Ghost
    posts[] payload."""
    g = {}
    if "title" in post:
        g["title"] = post["title"]
    if "seo_title" in post:
        g["meta_title"] = post["seo_title"]
    if "excerpt" in post:
        g["custom_excerpt"] = post["excerpt"]
    if "body_md" in post and post["body_md"] is not None:
        g["lexical"] = markdown_to_lexical(post["body_md"])
    if "tags" in post and post["tags"] is not None:
        g["tags"] = [{"name": t} for t in post["tags"]]
    if "status" in post:
        g["status"] = post["status"]
    if "scheduled_at" in post and post["scheduled_at"]:
        g["published_at"] = post["scheduled_at"]
    if "featured_image_url" in post:
        g["feature_image"] = post["featured_image_url"]
    if "image_alt_text" in post:
        g["feature_image_alt"] = post["image_alt_text"]
    if "canonical_url" in post and post["canonical_url"]:
        g["canonical_url"] = post["canonical_url"]
    authors = _resolve_author(post, config)
    if authors is not None:
        g["authors"] = authors
    return g


def _ghost_to_standard(ghost_post):
    """Translate a Ghost post object back to the standard schema.
    Note: body_md is not recovered (Ghost stores Lexical, not markdown)."""
    tags = [t.get("name", t.get("slug", "")) for t in ghost_post.get("tags") or []]
    authors = ghost_post.get("authors") or []
    author = None
    if authors:
        author = authors[0].get("slug") or authors[0].get("id")
    return {
        "id": ghost_post.get("id"),
        "title": ghost_post.get("title"),
        "seo_title": ghost_post.get("meta_title"),
        "excerpt": ghost_post.get("custom_excerpt"),
        "body_md": None,
        "tags": tags,
        "author": author,
        "status": ghost_post.get("status"),
        "scheduled_at": ghost_post.get("published_at") if ghost_post.get("status") == "scheduled" else None,
        "featured_image_url": ghost_post.get("feature_image"),
        "image_alt_text": ghost_post.get("feature_image_alt"),
        "canonical_url": ghost_post.get("canonical_url"),
        "url": ghost_post.get("url"),
        "updated_at": ghost_post.get("updated_at"),
    }


# =============================================================================
# Publisher Interface v1 implementation
# =============================================================================

class GhostPublisher:
    """Reference implementation of Publisher Interface v1 for Ghost 5.x."""

    def __init__(self, ghost_url=None, admin_api_key=None, config=None):
        if ghost_url is None or admin_api_key is None:
            env_url, env_key = get_env_config()
            ghost_url = ghost_url or env_url
            admin_api_key = admin_api_key or env_key
        self.ghost_url = ghost_url.rstrip("/")
        self.admin_api_key = admin_api_key
        self.config = config if config is not None else load_config()

    def _jwt(self):
        return generate_jwt(self.admin_api_key)

    def _get_raw(self, post_id):
        return _ghost_get(self.ghost_url, self._jwt(), f"posts/{post_id}/")["posts"][0]

    # -- Interface v1 methods ------------------------------------------------

    def createPost(self, post):
        """Create a new post (default status: draft). Returns post_id."""
        body = _standard_to_ghost(post, self.config)
        if "status" not in body:
            body["status"] = "draft"
        result = _ghost_send(self.ghost_url, self._jwt(), "posts/",
                             {"posts": [body]}, method="POST")
        return result["posts"][0]["id"]

    def updatePost(self, post_id, fields):
        """Patch an existing post with the given fields. Returns the full
        updated post in standard schema."""
        current = self._get_raw(post_id)
        body = _standard_to_ghost(fields, self.config)
        body["updated_at"] = current["updated_at"]
        result = _ghost_send(self.ghost_url, self._jwt(), f"posts/{post_id}/",
                             {"posts": [body]}, method="PUT")
        return _ghost_to_standard(result["posts"][0])

    def publishPost(self, post_id, opts=None):
        """Transition post to published. Returns live URL."""
        opts = opts or {}
        current = self._get_raw(post_id)
        body = {"status": "published", "updated_at": current["updated_at"]}
        if opts.get("send_newsletter"):
            body["email_only"] = False
            body["send_email_when_published"] = True
            newsletter_id = self.config.get("newsletter_id")
            if newsletter_id:
                body["newsletter_id"] = newsletter_id
        # Ghost publishPost: some Ghost versions require ?newsletter=<slug>
        # query param; body flag works on 5.x for the default newsletter.
        result = _ghost_send(self.ghost_url, self._jwt(), f"posts/{post_id}/",
                             {"posts": [body]}, method="PUT")
        return result["posts"][0].get("url") or f"{self.ghost_url}/{post_id}/"

    def schedulePost(self, post_id, datetime_iso):
        """Transition post to scheduled at the given ISO 8601 timestamp."""
        current = self._get_raw(post_id)
        body = {
            "status": "scheduled",
            "published_at": datetime_iso,
            "updated_at": current["updated_at"],
        }
        result = _ghost_send(self.ghost_url, self._jwt(), f"posts/{post_id}/",
                             {"posts": [body]}, method="PUT")
        p = result["posts"][0]
        return {"id": p["id"], "status": p["status"],
                "scheduled_at": p.get("published_at")}

    def deletePost(self, post_id):
        """Delete a post. Returns a confirmation."""
        _ghost_send(self.ghost_url, self._jwt(), f"posts/{post_id}/",
                    {}, method="DELETE")
        return {"id": post_id, "deleted": True}

    def uploadImage(self, url_or_path, alt=None):
        """Upload an image from a URL or local path to Ghost's media store.
        Returns the Ghost-hosted URL."""
        max_bytes = int(self.config.get("max_image_size_mb", DEFAULT_MAX_IMAGE_MB)) * 1024 * 1024

        if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
            with urllib.request.urlopen(url_or_path) as r:
                file_bytes = r.read()
                mime_type = r.headers.get("Content-Type", "application/octet-stream").split(";")[0]
            filename = os.path.basename(url_or_path.split("?")[0]) or "upload.bin"
        else:
            p = Path(url_or_path)
            file_bytes = p.read_bytes()
            mime_type = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
            filename = p.name

        if len(file_bytes) > max_bytes:
            raise RuntimeError(
                f"Image is {len(file_bytes)} bytes, exceeds configured max of "
                f"{max_bytes} bytes ({self.config.get('max_image_size_mb')}MB)."
            )

        return _ghost_multipart_upload(
            self.ghost_url, self._jwt(),
            file_bytes=file_bytes, filename=filename,
            mime_type=mime_type, purpose="image", alt=alt,
        )

    def getPost(self, post_id):
        """Fetch a post in standard schema."""
        return _ghost_to_standard(self._get_raw(post_id))


# =============================================================================
# CLI
# =============================================================================

def _split_tags(s):
    return [t.strip() for t in (s or "").split(",") if t.strip()]


def cmd_create_draft(args, pub):
    post_id = pub.createPost({
        "title": args.title,
        "excerpt": args.excerpt or "",
        "tags": _split_tags(args.tags),
    })
    print(f"post_id: {post_id}")
    print(f"url:     {pub.ghost_url}/ghost/#/editor/post/{post_id}")


def cmd_update_content(args, pub):
    with open(args.markdown_file, encoding="utf-8") as f:
        md = f.read()
    updated = pub.updatePost(args.post_id, {"body_md": md})
    print(f"[ok] Content updated -- post: {updated.get('title')}")


def cmd_set_image(args, pub):
    # If the value looks like a local file or has alt handling, use uploadImage
    # to get a Ghost-hosted URL first; otherwise pass through the URL.
    image_url = args.image_url
    if args.upload:
        image_url = pub.uploadImage(args.image_url, alt=args.alt)
        print(f"[ok] Image uploaded to Ghost: {image_url}")
    updated = pub.updatePost(args.post_id, {
        "featured_image_url": image_url,
        "image_alt_text": args.alt or "",
    })
    print(f"[ok] Feature image set on: {updated.get('title')}")


def cmd_publish(args, pub):
    url = pub.publishPost(args.post_id,
                          {"send_newsletter": bool(args.newsletter)})
    print(f"[ok] Published: {url}")


def cmd_schedule(args, pub):
    conf = pub.schedulePost(args.post_id, args.datetime_iso)
    print(f"[ok] Scheduled: {conf}")


def cmd_delete(args, pub):
    conf = pub.deletePost(args.post_id)
    print(f"[ok] Deleted: {conf}")


def cmd_get(args, pub):
    print(json.dumps(pub.getPost(args.post_id), indent=2))


def cmd_upload_image(args, pub):
    hosted = pub.uploadImage(args.url_or_path, alt=args.alt)
    print(hosted)


def cmd_create_publish(args, pub):
    with open(args.markdown_file, encoding="utf-8") as f:
        md = f.read()
    post_id = pub.createPost({
        "title": args.title,
        "excerpt": args.excerpt or "",
        "tags": _split_tags(args.tags),
        "body_md": md,
    })
    print(f"[ok] Draft created: {post_id}")

    if args.image_url:
        image_url = args.image_url
        if args.upload_image:
            image_url = pub.uploadImage(args.image_url, alt=args.image_alt)
            print(f"[ok] Image uploaded: {image_url}")
        pub.updatePost(post_id, {
            "featured_image_url": image_url,
            "image_alt_text": args.image_alt or "",
        })
        print("[ok] Feature image set")

    url = pub.publishPost(post_id, {"send_newsletter": bool(args.newsletter)})
    print(f"[ok] Published: {url}")


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Ghost Publisher -- Publisher Interface v1 reference implementation for Ghost 5.x"
    )
    p.add_argument("--config", default=None,
                   help="Path to JSON config file (also: GHOST_PUBLISHER_CONFIG env var)")
    sub = p.add_subparsers(dest="command", required=True)

    cd = sub.add_parser("create-draft", help="Create a new draft post")
    cd.add_argument("--title", required=True)
    cd.add_argument("--excerpt", default="")
    cd.add_argument("--tags", default="", help="Comma-separated tag names")

    uc = sub.add_parser("update-content", help="Inject markdown body into a post")
    uc.add_argument("post_id")
    uc.add_argument("markdown_file")

    si = sub.add_parser("set-image", help="Set the feature image of a post")
    si.add_argument("post_id")
    si.add_argument("image_url", help="URL or local file path")
    si.add_argument("--alt", default="", help="Image alt text")
    si.add_argument("--upload", action="store_true",
                    help="Upload the image to Ghost first (required for local files)")

    pub_cmd = sub.add_parser("publish", help="Publish a draft post")
    pub_cmd.add_argument("post_id")
    pub_cmd.add_argument("--newsletter", action="store_true",
                         help="Trigger newsletter email to subscribers")

    sc = sub.add_parser("schedule", help="Schedule a post for future publication")
    sc.add_argument("post_id")
    sc.add_argument("datetime_iso", help="ISO 8601 timestamp, e.g. 2026-05-01T09:00:00Z")

    dl = sub.add_parser("delete", help="Delete a post")
    dl.add_argument("post_id")

    gt = sub.add_parser("get", help="Fetch a post in standard schema (JSON)")
    gt.add_argument("post_id")

    ui = sub.add_parser("upload-image", help="Upload an image to Ghost's media store")
    ui.add_argument("url_or_path", help="Remote URL or local file path")
    ui.add_argument("--alt", default="", help="Image alt text")

    cp = sub.add_parser("create-publish",
                        help="Full pipeline: create, inject, image, publish")
    cp.add_argument("markdown_file")
    cp.add_argument("--title", required=True)
    cp.add_argument("--excerpt", default="")
    cp.add_argument("--tags", default="", help="Comma-separated tag names")
    cp.add_argument("--image-url", default="", dest="image_url")
    cp.add_argument("--image-alt", default="", dest="image_alt")
    cp.add_argument("--upload-image", action="store_true", dest="upload_image",
                    help="Upload the --image-url to Ghost before attaching")
    cp.add_argument("--newsletter", action="store_true",
                    help="Trigger newsletter email to subscribers")

    args = p.parse_args(argv)

    try:
        config = load_config(args.config)
        publisher = GhostPublisher(config=config)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    handlers = {
        "create-draft": cmd_create_draft,
        "update-content": cmd_update_content,
        "set-image": cmd_set_image,
        "publish": cmd_publish,
        "schedule": cmd_schedule,
        "delete": cmd_delete,
        "get": cmd_get,
        "upload-image": cmd_upload_image,
        "create-publish": cmd_create_publish,
    }
    try:
        handlers[args.command](args, publisher)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
