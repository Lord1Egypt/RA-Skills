from __future__ import annotations


def classify_path(
    path: str,
    keep_protected_prefixes: list[str],
    review_carefully_prefixes: list[str],
) -> str:
    normalized_path = _normalize_path(path)
    for prefix in keep_protected_prefixes:
        normalized = _normalize_path(prefix)
        if normalized_path == normalized or normalized_path.startswith(f"{normalized}/"):
            return "keep protected"

    if _is_obvious_review_first(normalized_path):
        return "review first"

    for prefix in review_carefully_prefixes:
        normalized = _normalize_path(prefix)
        if normalized_path == normalized or normalized_path.startswith(f"{normalized}/"):
            return "review carefully"

    return "review carefully"


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").rstrip("/").lower()


def _is_obvious_review_first(normalized_path: str) -> bool:
    review_first_exact_paths = {
        "/tmp",
        "/var/tmp",
    }
    if normalized_path in review_first_exact_paths:
        return True
    if _has_cache_or_trash_signature(normalized_path):
        return True
    if any(fragment in normalized_path for fragment in ("/appdata/local/temp/", "/tmp/", "/var/tmp/")):
        return True
    return normalized_path.endswith((".filepart", ".part", ".partial", ".tmp", ".cache"))


def _has_cache_or_trash_signature(normalized_path: str) -> bool:
    if normalized_path.endswith(("/.cache", "/trash", "/.trash", "/appdata/local/temp")):
        return True
    segments = [segment for segment in normalized_path.split("/") if segment]
    return any(
        segment in {"trash", ".trash", ".cache"}
        or segment.endswith("_cache")
        for segment in segments
    )
