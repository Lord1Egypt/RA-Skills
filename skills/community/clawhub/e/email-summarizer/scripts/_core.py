#!/usr/bin/env python3
"""
_core.py — Shared low-level utilities for email-summarizer.

NOT a standalone script. Imported by other scripts in this package.

Provides:
  decode_header(raw)        → str
  parse_addr(raw)           → (name, address)
  get_domain(addr)          → str
  strip_html(text)          → str
  html_esc(text)            → str
  get_body(msg)             → str   (from email.message.Message)
  IMAP_DATE_FMT             = "%d-%b-%Y"
"""

import email
import email.header
import email.utils
import re

IMAP_DATE_FMT = "%d-%b-%Y"


def decode_header(raw: str) -> str:
    """Decode an RFC 2047-encoded header value to a plain string."""
    parts = email.header.decode_header(raw or "")
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(str(part))
    return "".join(decoded).strip()


def parse_addr(raw: str):
    """
    Parse a single address string → (display_name, email_address).

    Handles both 'Name <addr>' and bare address forms.
    Returns ('', '') if the input is empty or has no address.
    """
    raw = (raw or "").strip()
    m = re.match(r'^"?([^"<]+?)"?\s*<([^>]+)>', raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    if "@" in raw:
        return raw, raw
    return raw, ""


def get_domain(addr: str) -> str:
    """Extract the domain part of an email address (lowercased)."""
    m = re.search(r"@([\w.\-]+)", addr)
    return m.group(1).lower() if m else ""


def strip_html(text: str) -> str:
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def html_esc(t: object) -> str:
    """Escape special HTML characters."""
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def get_body(msg) -> str:
    """
    Extract the plain-text body from an email.message.Message object.

    Prefers text/plain parts; falls back to HTML-stripped text/html.
    Returns up to 2000 characters.
    """
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            if ctype == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                try:
                    body = part.get_payload(decode=True).decode(charset, errors="replace")
                    break
                except Exception:
                    pass
            elif ctype == "text/html" and not body:
                charset = part.get_content_charset() or "utf-8"
                try:
                    html = part.get_payload(decode=True).decode(charset, errors="replace")
                    body = strip_html(html)
                except Exception:
                    pass
    else:
        charset = msg.get_content_charset() or "utf-8"
        try:
            body = msg.get_payload(decode=True).decode(charset, errors="replace")
        except Exception:
            body = ""
    return body[:2000]
