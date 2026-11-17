#!/usr/bin/env python3
"""Shared text helpers for agent transcript dumpers.

Redaction is intentionally conservative: a false positive only hides a few
characters, while a false negative can leak a live credential into the model
context or a handoff file.
"""
import io
import re
import sys

REDACTED = "[REDACTED]"


def ensure_utf8_stdout():
    """Reconfigure stdout/stderr as UTF-8 so transcripts with characters
    outside the console codepage (e.g. GBK on zh-CN Windows) never crash
    the dumper. Call once at the start of main()."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None or getattr(stream, "_utf8_wrapped", False):
            continue
        encoding = (getattr(stream, "encoding", None) or "").lower()
        if encoding in ("utf-8", "utf8"):
            continue
        buffer = getattr(stream, "buffer", None)
        if buffer is None:
            continue
        wrapped = io.TextIOWrapper(buffer, encoding="utf-8", errors="replace")
        wrapped._utf8_wrapped = True
        setattr(sys, stream_name, wrapped)

_ASSIGNMENT = re.compile(
    r"""(?i)\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|"""
    r"""secret|password|passwd|auth[_-]?token|session[_-]?token)\b"""
    r"""(\s*[:=]\s*)(["']?)([^\s"',;]{6,})\3"""
)

_PATTERNS = [
    # Credential-bearing HTTP headers, including a whole Cookie line.
    (re.compile(r"(?im)(\b(?:proxy-)?authorization\s*:\s*)[^\r\n]+"), r"\1[REDACTED]"),
    (re.compile(r"(?im)(\b(?:set-)?cookie\s*:\s*)[^\r\n]+"), r"\1[REDACTED]"),
    # key=value / key: value assignments.
    (
        _ASSIGNMENT,
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}[REDACTED]{m.group(3)}",
    ),
    # Common provider token formats.
    (re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{20,}\b"), REDACTED),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), REDACTED),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), REDACTED),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"), REDACTED),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), REDACTED),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.I), "Bearer [REDACTED]"),
    (
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
        REDACTED,
    ),
    # Token query parameters.
    (
        re.compile(r"(?i)([?&](?:access_token|api_key|token|key)=)[^&\s\"']+"),
        r"\1[REDACTED]",
    ),
    # PEM private keys can span many lines.
    (
        re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----.*?"
            r"-----END (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
            re.S,
        ),
        "[REDACTED PRIVATE KEY]",
    ),
]


def redact_text(text):
    """Return (redacted_text, number_of_replacements)."""
    if not isinstance(text, str):
        return "", 0
    count = 0
    for pattern, replacement in _PATTERNS:
        text, n = pattern.subn(replacement, text)
        count += n
    return text, count


def blocks_text(content):
    """Extract text from a string or a list/dict of typed content blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        content = [content]
    if not isinstance(content, list):
        return ""
    out = []
    for block in content:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")
        # Typed blocks (codex/claude/zcode) plus bare {"text": ...} parts
        # used by Gemini CLI and similar shapes.
        if block.get("text") and (
            block_type in ("text", "input_text", "output_text") or block_type is None
        ):
            out.append(block["text"])
    return "\n".join(out)


def truncate_text(text, max_chars):
    """Truncate to max_chars; 0 or None means unlimited."""
    if max_chars and len(text) > max_chars:
        return text[:max_chars] + f"\n...[truncated, {len(text) - max_chars} more chars]"
    return text
