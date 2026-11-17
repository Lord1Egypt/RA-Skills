"""Word entitlement and generation-estimate helpers."""

SUGGESTED_TOTAL_PAGES = 200
DEFAULT_MAX_TOTAL_PAGES = 1200
ESTIMATED_WORDS_PER_PAGE = 500
ESTIMATE_RESERVE_FACTOR = 1.05


def shortage_detail(error=None):
    error = error or {}
    required = error.get("required_words") or error.get("estimated_words")
    available = error.get("available_words", error.get("wallet_balance"))
    if required is None and available is None:
        return ""
    parts = []
    if required is not None:
        parts.append(f"预计/本次需要约 {int(required):,} 字")
    if available is not None:
        parts.append(f"当前可用 {int(available):,} 字")
    return "，".join(parts) + "。"


def generation_pages(args):
    total_pages = getattr(args, "total_pages", None)
    if total_pages:
        return int(total_pages)
    if getattr(args, "use_suggested_pages", False):
        return int(getattr(args, "suggested_pages", None) or SUGGESTED_TOTAL_PAGES)
    return SUGGESTED_TOTAL_PAGES


def generation_max_pages(args):
    value = getattr(args, "max_total_pages", None)
    return int(value) if value is not None else None


def estimate_generation_words(total_pages):
    return int(max(0, int(total_pages or 0)) * ESTIMATED_WORDS_PER_PAGE * ESTIMATE_RESERVE_FACTOR)
