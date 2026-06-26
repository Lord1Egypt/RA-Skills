#!/usr/bin/env python3
"""Redact an OpenClaw config file for safer sharing.

The active OpenClaw config is often JSON5-like (`~/.openclaw/openclaw.json` by
default), so this script tries strict JSON first, then an optional JSON5 parser,
then falls back to regex-based redaction on the raw text.

What it redacts (best-effort):
- Secret-like keys: token, password, secret, api key, cookie, session key, etc.
- String values that strongly resemble long secrets or JWT-style tokens.
- Query-string secrets in URLs such as ?token=... or ?access_token=...

Examples:
  python3 "{baseDir}/scripts/redact_openclaw_config.py" ~/.openclaw/openclaw.json > openclaw.json.redacted
  cat ~/.openclaw/openclaw.json | python3 "{baseDir}/scripts/redact_openclaw_config.py" - > openclaw.json.redacted

Always review the redacted output before sharing it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Callable, Optional

SENSITIVE_KEY_RE = re.compile(
    r"(token|password|secret|api[_-]?key|apikey|client[_-]?secret|private[_-]?key|session[_-]?key|cookie|bearer|access[_-]?token|refresh[_-]?token)\b",
    re.IGNORECASE,
)

JWT_LIKE_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")
HEXISH_RE = re.compile(r"^[A-Fa-f0-9]{32,}$")
ALNUMISH_RE = re.compile(r"^[A-Za-z0-9_\-]{24,}$")

URL_QS_SECRET_RE = re.compile(
    r"(?P<prefix>[?&](?:token|password|api[_-]?key|apikey|key|access_token|refresh_token|session[_-]?key)=)(?P<val>[^&\s#]+)",
    re.IGNORECASE,
)


def mask(s: str) -> str:
    s = s or ""
    if len(s) <= 8:
        return "***"
    return f"{s[:4]}…{s[-4:]}"


def looks_secret(s: str) -> bool:
    if len(s) < 24:
        return False
    if s.startswith(("http://", "https://", "/", "./", "../", "~/")):
        return False
    return bool(JWT_LIKE_RE.match(s) or HEXISH_RE.match(s) or ALNUMISH_RE.match(s))


def redact_string(s: str) -> str:
    if looks_secret(s):
        return mask(s)
    return URL_QS_SECRET_RE.sub(lambda m: m.group("prefix") + mask(m.group("val")), s)


def redact_obj(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, value in obj.items():
            skey = str(key)
            if SENSITIVE_KEY_RE.search(skey):
                if isinstance(value, str):
                    out[skey] = redact_string(value)
                else:
                    out[skey] = "***"
            else:
                out[skey] = redact_obj(value)
        return out

    if isinstance(obj, list):
        return [redact_obj(item) for item in obj]

    if isinstance(obj, str):
        return redact_string(obj)

    return obj


def try_json5_parser() -> Optional[Callable[[str], Any]]:
    for module_name in ("json5", "pyjson5"):
        try:
            module = __import__(module_name)
            loads = getattr(module, "loads", None)
            if callable(loads):
                return loads  # type: ignore[return-value]
        except Exception:
            continue
    return None


def text_fallback_redact(raw: str) -> str:
    redacted = URL_QS_SECRET_RE.sub(lambda m: m.group("prefix") + mask(m.group("val")), raw)

    quoted_kv_re = re.compile(
        r"(?P<key>\b[\w.-]*(?:token|password|secret|api[_-]?key|apikey|client[_-]?secret|private[_-]?key|session[_-]?key|cookie|bearer|access[_-]?token|refresh[_-]?token)[\w.-]*\b)"
        r"(?P<ws>\s*:\s*)"
        r"(?P<val>(?:\"[^\"]*\"|'[^']*'))",
        re.IGNORECASE,
    )

    def repl_quoted(match: re.Match[str]) -> str:
        key = match.group("key")
        ws = match.group("ws")
        val = match.group("val")
        if val.startswith('"'):
            inner = val[1:-1]
            return f'{key}{ws}"{mask(inner)}"'
        inner = val[1:-1]
        return f"{key}{ws}'{mask(inner)}'"

    redacted = quoted_kv_re.sub(repl_quoted, redacted)

    bare_kv_re = re.compile(
        r"(?P<key>\b[\w.-]*(?:token|password|secret|api[_-]?key|apikey|client[_-]?secret|private[_-]?key|session[_-]?key|cookie|bearer|access[_-]?token|refresh[_-]?token)[\w.-]*\b)"
        r"(?P<ws>\s*:\s*)"
        r"(?P<val>[A-Za-z0-9._-]{12,})",
        re.IGNORECASE,
    )

    def repl_bare(match: re.Match[str]) -> str:
        value = match.group("val")
        redacted_value = mask(value) if looks_secret(value) else value
        return f"{match.group('key')}{match.group('ws')}{redacted_value}"

    return bare_kv_re.sub(repl_bare, redacted)


def load_raw(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Redact an OpenClaw config file before sharing it.",
        epilog="The tool prefers structured JSON/JSON5 redaction when possible and falls back to raw-text redaction otherwise.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="Path to the config file, or '-' to read from stdin.",
    )
    parser.add_argument(
        "--text-fallback-only",
        action="store_true",
        help="Skip JSON/JSON5 parsing and redact the raw text directly.",
    )
    args = parser.parse_args()

    raw = load_raw(args.path)

    if args.text_fallback_only:
        sys.stdout.write(text_fallback_redact(raw))
        if not raw.endswith("\n"):
            sys.stdout.write("\n")
        return

    parsed = False
    obj: Any = None

    try:
        obj = json.loads(raw)
        parsed = True
    except Exception:
        parsed = False

    if not parsed:
        json5_loads = try_json5_parser()
        if json5_loads is not None:
            try:
                obj = json5_loads(raw)
                parsed = True
            except Exception:
                parsed = False

    if parsed:
        json.dump(redact_obj(obj), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return

    sys.stdout.write(text_fallback_redact(raw))
    if not raw.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
