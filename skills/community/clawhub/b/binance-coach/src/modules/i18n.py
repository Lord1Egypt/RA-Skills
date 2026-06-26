"""
i18n.py — Thin locale loader

Loads strings and lessons from modules/locales/<lang>.py
Adding a new language = adding a new file (e.g. modules/locales/fr.py)

Usage:
    from modules.i18n import t, set_lang, get_lang, tlesson, AVAILABLE_LANGS
    set_lang("nl")
    print(t("portfolio.total"))
    lesson = tlesson("dca")
"""

import importlib
import os
from functools import lru_cache

# Active language
_LANG = "en"

# Registry: code → display name
# To add a language: create modules/locales/<code>.py and add an entry here
AVAILABLE_LANGS: dict[str, str] = {
    "en": "🇬🇧 English",
    "nl": "🇳🇱 Nederlands",
    # "fr": "🇫🇷 Français",   ← uncomment after adding modules/locales/fr.py
    # "de": "🇩🇪 Deutsch",
    # "es": "🇪🇸 Español",
}


@lru_cache(maxsize=None)
def _load(lang: str):
    """Load and cache a locale module. Returns (STRINGS, LESSONS)."""
    try:
        mod = importlib.import_module(f"modules.locales.{lang}")
        return mod.STRINGS, mod.LESSONS
    except ModuleNotFoundError:
        # Fallback to English if locale file missing
        mod = importlib.import_module("modules.locales.en")
        return mod.STRINGS, mod.LESSONS


def set_lang(lang: str):
    """Set the active language. Raises ValueError for unknown codes."""
    global _LANG
    lang = lang.lower().strip()
    if lang not in AVAILABLE_LANGS:
        raise ValueError(
            f"Unsupported language: '{lang}'. "
            f"Available: {list(AVAILABLE_LANGS.keys())}"
        )
    _LANG = lang


def get_lang() -> str:
    """Return current language code."""
    return _LANG


def t(key: str, **kwargs) -> str:
    """
    Translate a key to the current language.
    Falls back to English if key missing in active locale.
    Supports .format()-style keyword arguments.

    Example:
        t("portfolio.sug.diversify", n=3)
    """
    strings, _ = _load(_LANG)
    text = strings.get(key)

    # Fallback to English
    if text is None and _LANG != "en":
        en_strings, _ = _load("en")
        text = en_strings.get(key)

    if text is None:
        return f"[MISSING:{key}]"

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text


def tlesson(topic: str) -> dict | None:
    """
    Get a lesson dict {title, content} in the current language.
    Falls back to English if lesson missing in active locale.
    Returns None if topic doesn't exist at all.
    """
    _, lessons = _load(_LANG)
    lesson = lessons.get(topic)

    # Fallback to English
    if lesson is None and _LANG != "en":
        _, en_lessons = _load("en")
        lesson = en_lessons.get(topic)

    if lesson is None:
        return None

    return {
        "title":   lesson.get("title", topic),
        "content": lesson.get("content", ""),
    }


# Convenience: iterate lesson keys without caring about language
def lesson_keys() -> list[str]:
    """Return all available lesson topic keys."""
    _, lessons = _load("en")
    return list(lessons.keys())


# For backwards-compat: modules that import LESSONS directly
class _LessonsProxy:
    """Allows `for key in LESSONS` and `LESSONS.get(key)`."""
    def keys(self):
        return lesson_keys()
    def get(self, key, default=None):
        _, lessons = _load("en")
        return lessons.get(key, default)
    def __iter__(self):
        return iter(lesson_keys())
    def __contains__(self, key):
        return key in lesson_keys()
    def __len__(self):
        return len(lesson_keys())

LESSONS = _LessonsProxy()
