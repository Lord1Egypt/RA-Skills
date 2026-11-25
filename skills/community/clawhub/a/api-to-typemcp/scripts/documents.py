"""Bounded extraction of evidenced operations from supplied Markdown or HTML."""
from __future__ import annotations

from html.parser import HTMLParser
import re
from typing import Any
from urllib.parse import unquote, urlsplit

MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
MAX_OPERATIONS = 500


class DocumentError(ValueError):
    """User-safe error for document extraction."""


_OPERATION_RE = re.compile(
    r"(?<![A-Za-z])(?P<method>GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(?P<path>(?:https?://[^\s<>]+|/[^\s<>`'\")]+))"
)
_TAG_RE = re.compile(r"<[^>]*>")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return "\n".join(self.parts)


def _document_text(content: str, source_kind: str) -> str:
    if source_kind == "markdown":
        return content
    if source_kind == "html":
        parser = _TextExtractor()
        parser.feed(content)
        parser.close()
        return parser.text()
    raise DocumentError("document source kind must be markdown or html")


def _validate_path_candidate(raw: str) -> str:
    """Reject paths whose parsing or URL normalization changes the target."""
    parsed = urlsplit(raw)
    if parsed.scheme:
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise DocumentError("absolute operation URL must be http(s) with a host")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise DocumentError("absolute operation URL must not contain credentials, query, or fragment")
        path = parsed.path or "/"
    else:
        if not raw.startswith("/") or "?" in raw or "#" in raw:
            raise DocumentError("operation path must be an absolute path without query or fragment")
        path = raw
    for segment in path.split("/"):
        if unquote(segment).lower() in {".", ".."}:
            raise DocumentError("operation path must not contain dot segments")
    return raw


def extract_operations(content: str, *, source_kind: str) -> list[dict[str, Any]]:
    """Extract only explicit METHOD + path candidates from supplied content.

    Evidence is generated solely from the matched method and path, never copied
    from surrounding source prose. Every candidate requires a receipt-gated
    confirmation; confidence is not an authorization grant.
    """
    if not isinstance(content, str):
        raise DocumentError("document input must be text")
    if len(content.encode("utf-8")) > MAX_DOCUMENT_BYTES:
        raise DocumentError(f"document exceeds {MAX_DOCUMENT_BYTES} byte limit")
    text = _document_text(content, source_kind)
    operations: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in _OPERATION_RE.finditer(line):
            method = match.group("method")
            path = _validate_path_candidate(match.group("path").rstrip(".,;:"))
            key = (method, path)
            if key in seen:
                continue
            seen.add(key)
            operations.append({
                "method": method,
                "path": path,
                "confidence": "explicit",
                "requires_confirmation": True,
                "evidence": {
                    "source": source_kind,
                    "line": line_number,
                    "snippet": _TAG_RE.sub("", f"{method} {path}"),
                },
            })
            if len(operations) > MAX_OPERATIONS:
                raise DocumentError("document exceeds operation extraction limit")
    return operations
