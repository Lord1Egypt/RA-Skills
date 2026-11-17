"""Small, dependency-free locale and message helper for design-guide CLIs."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Mapping, Sequence


SUPPORTED_LOCALES = ("en", "zh-CN")
DEFAULT_LOCALE = "en"
_ALIASES = {
    "en": "en",
    "en-us": "en",
    "en_us": "en",
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh_cn": "zh-CN",
}
_LOCALE_DIR = Path(__file__).resolve().parent.parent / "locales"
_CATALOG_CACHE: dict[str, dict[str, str]] = {}


def normalize_locale(value: str | None) -> str:
    """Normalize common locale spellings and fall back to English."""
    if not value:
        return DEFAULT_LOCALE
    normalized = value.strip().replace(".", "-").lower()
    return _ALIASES.get(normalized, DEFAULT_LOCALE)


def resolve_locale(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> str:
    """Resolve the CLI locale using explicit flag, project env, then system env."""
    values = list(argv if argv is not None else sys.argv[1:])
    for index, value in enumerate(values):
        if value == "--locale" and index + 1 < len(values):
            return normalize_locale(values[index + 1])
        if value.startswith("--locale="):
            return normalize_locale(value.split("=", 1)[1])

    environment = env if env is not None else os.environ
    for name in ("F_DESIGN_LOCALE", "LC_ALL", "LANG"):
        candidate = environment.get(name)
        if candidate:
            return normalize_locale(candidate)
    return DEFAULT_LOCALE


def add_locale_argument(parser: argparse.ArgumentParser, *, suppress_default: bool = False) -> None:
    """Add the common locale flag. Suppress defaults on subparsers."""
    parser.add_argument(
        "--locale",
        choices=SUPPORTED_LOCALES,
        default=argparse.SUPPRESS if suppress_default else resolve_locale(),
        help=t("Output language (en or zh-CN). Defaults to F_DESIGN_LOCALE or LANG.", resolve_locale()),
    )


def _catalog(locale: str) -> dict[str, str]:
    locale = normalize_locale(locale)
    if locale not in _CATALOG_CACHE:
        path = _LOCALE_DIR / f"{locale}.json"
        try:
            _CATALOG_CACHE[locale] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            _CATALOG_CACHE[locale] = {}
    return _CATALOG_CACHE[locale]


def t(message: str, locale: str | None = None, **values: object) -> str:
    """Translate a message, falling back to the English source string."""
    translated = _catalog(locale or resolve_locale()).get(message, message)
    try:
        return translated.format(**values)
    except (KeyError, IndexError, ValueError):
        return translated
