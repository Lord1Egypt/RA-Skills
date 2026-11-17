"""Normalized record schema, safety filters, and dedupe.

Every source adapter emits the SAME record shape, so downstream code
(dedupe, publish, training loaders) never needs to know where a row
came from. One JSON object per image, newline-delimited.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

SCHEMA_VERSION = 1

# --------------------------------------------------------------------------
# Rating normalization. Sites disagree; collapse to one 5-level scale.
# --------------------------------------------------------------------------
def norm_rating(raw: str) -> str:
    r = (raw or "").strip().lower()
    if r in {"s", "safe", "general", "g", "sensitive_safe"}:
        return "general"
    if r in {"q", "questionable"}:
        return "questionable"
    if r in {"e", "explicit", "explicit_only", "r18", "explicit_filtered"}:
        # pixiv reports "r18", which is its explicit tier. Without this it
        # normalized to "unknown" and slipped past every rating filter.
        return "explicit"
    if r in {"sensitive"}:
        return "sensitive"
    return "unknown"


# Severity order, lowest first. `--rating` is a CEILING against this, so
# "--rating sensitive" means "general or sensitive", not "sensitive only".
RATING_ORDER = {"general": 0, "sensitive": 1, "questionable": 2, "explicit": 3}

CEILING_CHOICES = (*RATING_ORDER, "any")


# --------------------------------------------------------------------------
# HARD safety excludes.
#
# These are applied to EVERY harvested item before it is written to disk,
# regardless of the user's query or the site's rating. They are not
# configurable by flag. Removing them requires editing this file, on
# purpose, so that no casual invocation can disable them.
# --------------------------------------------------------------------------
UNDERAGE_TAGS = {
    "loli", "lolicon", "shota", "shotacon", "child", "children", "underage",
    "toddler", "infant", "baby", "kodomo", "child_on_child", "young_girl",
    "young_boy", "female_child", "male_child", "child_only", "aged_down",
    "age_regression", "elementary_school", "kindergarten", "preschool",
    "little_sister", "brocon", "siscon", "1girl_child", "1boy_child",
}
BANNED_TAGS = {
    "guro", "snuff", "bestiality", "necrophilia", "scat", "vore",
    "amputee", "cub", "zoophilia", "corpse", "ryona",
}


def tagset(tags) -> set[str]:
    """Accept a space-delimited string or an iterable; return a lowercase set."""
    if tags is None:
        return set()
    if isinstance(tags, str):
        return {t.strip().lower() for t in tags.split() if t.strip()}
    return {str(t).strip().lower() for t in tags if str(t).strip()}


def safety_ok(tags) -> tuple[bool, str]:
    """Return (ok, reason). reason is empty when ok."""
    ts = tagset(tags)
    hit = ts & UNDERAGE_TAGS
    if hit:
        return False, "underage-tag:" + sorted(hit)[0]
    hit = ts & BANNED_TAGS
    if hit:
        return False, "banned-tag:" + sorted(hit)[0]
    return True, ""


def slug(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", (text or "").strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len]


def make_record(
    *,
    source: str,
    source_id: str,
    page_url: str,
    file_url: str,
    tags,
    artist: str = "",
    rating: str = "",
    width: int = 0,
    height: int = 0,
    file_ext: str = "",
    md5: str = "",
    caption: str = "",
    extra: dict | None = None,
) -> dict:
    """Build one normalized record. `tags` is the caption source for training."""
    tag_list = sorted(tagset(tags)) if not isinstance(tags, str) else tags.split()
    return {
        "schema_version": SCHEMA_VERSION,
        "source": source,
        "source_id": str(source_id),
        "page_url": page_url,
        "file_url": file_url,
        "md5": md5,
        "width": int(width or 0),
        "height": int(height or 0),
        "file_ext": (file_ext or "").lstrip("."),
        "rating": norm_rating(rating),
        "artist": artist or "",
        "tags": tag_list,
        # A ready-to-use training caption: space-joined tags, then free text.
        "caption": (caption or " ".join(tag_list)).strip(),
        # Local path is filled in after a successful download.
        # `file_name` mirrors it as a dataset-relative path so that
        # HuggingFace's `imagefolder` loader picks the images up directly.
        "file_path": "",
        "file_name": "",
        "provenance": {"harvester": "AgentEpstein", "schema": SCHEMA_VERSION},
        "extra": extra or {},
    }


def record_key(rec: dict) -> str:
    """Stable identity for dedupe: md5 when present, else source+id."""
    if rec.get("md5"):
        return "md5:" + rec["md5"].lower()
    return f"{rec.get('source')}:{rec.get('source_id')}"


def dedupe(records: list[dict]) -> tuple[list[dict], int]:
    """Drop duplicate images. Returns (kept, dropped_count)."""
    seen: set[str] = set()
    kept: list[dict] = []
    for r in records:
        k = record_key(r)
        if k in seen:
            continue
        seen.add(k)
        kept.append(r)
    return kept, len(records) - len(kept)


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
