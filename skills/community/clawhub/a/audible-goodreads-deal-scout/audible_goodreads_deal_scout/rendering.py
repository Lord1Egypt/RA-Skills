from __future__ import annotations

import re
from typing import Any

from .constants import UNICODE_BOLD_TRANSLATION
from .delivery import normalize_delivery_policy
from .settings import SUPPORTED_MARKETPLACES
from .shared import normalize_space


def price_display(audible: dict[str, Any], marketplace_key: str) -> str:
    spec = SUPPORTED_MARKETPLACES.get(marketplace_key, SUPPORTED_MARKETPLACES["us"])
    currency_symbol = spec.get("currencySymbol") or ""
    sale_price = audible.get("salePrice")
    list_price = audible.get("listPrice")
    if sale_price is not None and list_price is not None and float(list_price) > 0:
        discount = max(0, round((1 - (float(sale_price) / float(list_price))) * 100))
        return f"Price: {currency_symbol}{float(sale_price):.2f} (-{discount}%, list price {currency_symbol}{float(list_price):.2f})"
    if sale_price is not None:
        return f"Price: {currency_symbol}{float(sale_price):.2f}"
    if audible.get("memberHidden"):
        return "Price: member deal / hidden"
    return "Price: unavailable"


def offer_description(audible: dict[str, Any]) -> str:
    summary = normalize_space(str(audible.get("summary") or ""))
    if not summary:
        return ""
    if len(summary) <= 520:
        return summary
    return summary[:517].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"


def format_runtime(runtime: str) -> str:
    raw = normalize_space(runtime)
    match = re.fullmatch(r"(\d+)\s*hrs?\s*and\s*(\d+)\s*mins?", raw, re.I)
    if not match:
        return raw
    hours = int(match.group(1))
    minutes = int(match.group(2))
    return f"{hours}:{minutes:02d} hrs"


def bold_visible_text(value: str) -> str:
    return str(value or "").translate(UNICODE_BOLD_TRANSLATION)


def render_message_layout(
    *,
    header: str,
    title_line: str,
    metadata_lines: list[str],
    description_text: str,
    fit_text: str | None,
    footer_lines: list[str],
    warnings: list[str],
) -> str:
    parts: list[str] = [header, "", title_line, *metadata_lines]
    if description_text:
        parts.extend(["", description_text])
    if fit_text:
        parts.extend(["", fit_text])
    if footer_lines:
        parts.extend(["", *footer_lines])
    if warnings:
        parts.extend(["", "Warnings: " + " ".join(warnings)])
    return "\n".join(parts).strip()


def summary_fit_text(final_result: dict[str, Any]) -> str:
    reason_code = str(final_result.get("reasonCode") or "")
    mapping = {
        "suppress_already_read": "Fit: You marked it as read on Goodreads.",
        "suppress_currently_reading": "Fit: You marked it as currently reading on Goodreads.",
        "suppress_below_goodreads_threshold": "Fit: Goodreads is below your cutoff.",
        "suppress_no_goodreads_match": "Fit: Goodreads could not confirm a matching book.",
        "suppress_no_active_promotion": "Fit: No daily promotion could be confirmed.",
        "suppress_duplicate_scheduled_run": "Fit: This deal was already handled today.",
        "error_goodreads_lookup_failed": "Fit: Goodreads could not be verified right now.",
        "error_audible_fetch_failed": "Fit: Audible could not be verified right now.",
        "error_audible_parse_failed": "Fit: Audible could not be verified right now.",
        "error_audible_blocked": "Fit: Audible could not be verified right now.",
        "error_ambiguous_personal_match": "Fit: Goodreads has conflicting shelf information for this title.",
        "error_csv_unreadable": "Fit: Goodreads data could not be read right now.",
        "error_missing_notes_file": "Fit: Preference notes could not be read right now.",
        "error_missing_csv": "Fit: Goodreads data is not available right now.",
    }
    return mapping.get(reason_code, "Fit: This deal could not be verified right now.")


def render_final_message(final_result: dict[str, Any]) -> str:
    audible = final_result.get("audible") or {}
    metadata = final_result.get("metadata") or {}
    goodreads = final_result.get("goodreads") or {}
    warnings = list(final_result.get("warnings") or [])
    marketplace_label = metadata.get("marketplaceLabel") or f"Audible {str(metadata.get('marketplace') or '').upper()}"
    store_date = normalize_space(str(metadata.get("storeLocalDate") or ""))
    header = f"{marketplace_label} Daily Promotion" + (f" — {store_date}" if store_date else "")
    marketplace_key = str(metadata.get("marketplace") or "us")
    title_line = f"{bold_visible_text(str(audible.get('title', 'Unknown Title')))} — {audible.get('author', 'Unknown Author')}"
    if audible.get("year"):
        title_line += f" ({audible['year']})"
    metadata_lines = [price_display(audible, marketplace_key)]
    if goodreads.get("status") == "resolved" and goodreads.get("averageRating") is not None:
        rating_line = f"Goodreads rating: {goodreads['averageRating']:.2f}"
        ratings_count = goodreads.get("ratingsCount")
        if ratings_count:
            rating_line += f" ({int(ratings_count):,} ratings)"
        metadata_lines.append(rating_line)
    runtime = format_runtime(str(audible.get("runtime") or ""))
    if runtime and runtime.lower() != "unknown":
        metadata_lines.append(f"Length: {runtime}")
    genres = [normalize_space(str(label)) for label in list(audible.get("genres") or []) if normalize_space(str(label))]
    if genres:
        metadata_lines.append(f"Genre: {', '.join(genres)}")
    if final_result["status"] != "recommend":
        metadata_lines.append(f"Reason: {final_result.get('reasonText') or final_result.get('reasonCode')}")
    fit_sentence = normalize_space(str(final_result.get("fitSentence") or ""))
    footer_lines: list[str] = []
    if audible.get("audibleUrl"):
        footer_lines.append(f"Audible: {audible['audibleUrl']}")
    if goodreads.get("url"):
        footer_lines.append(f"Goodreads: {goodreads['url']}")
    return render_message_layout(
        header=header,
        title_line=title_line,
        metadata_lines=metadata_lines,
        description_text=offer_description(audible),
        fit_text=fit_sentence or None,
        footer_lines=footer_lines,
        warnings=warnings,
    )


def render_delivery_summary_message(final_result: dict[str, Any]) -> str:
    audible = final_result.get("audible") or {}
    metadata = final_result.get("metadata") or {}
    warnings = list(final_result.get("warnings") or [])
    marketplace_label = metadata.get("marketplaceLabel") or f"Audible {str(metadata.get('marketplace') or '').upper()}"
    store_date = normalize_space(str(metadata.get("storeLocalDate") or ""))
    header = f"{marketplace_label} Daily Promotion" + (f" — {store_date}" if store_date else "")
    title_line = f"{bold_visible_text(str(audible.get('title', 'Unknown Title')))} — {audible.get('author', 'Unknown Author')}"
    if audible.get("year"):
        title_line += f" ({audible['year']})"
    footer_lines: list[str] = []
    if audible.get("audibleUrl"):
        footer_lines.append(f"Audible: {audible['audibleUrl']}")
    return render_message_layout(
        header=header,
        title_line=title_line,
        metadata_lines=[],
        description_text="",
        fit_text=summary_fit_text(final_result),
        footer_lines=footer_lines,
        warnings=warnings,
    )


def build_delivery_plan(final_result: dict[str, Any], policy: str) -> dict[str, Any]:
    normalized_policy = normalize_delivery_policy(policy)
    status = str(final_result.get("status") or "")
    if normalized_policy == "positive_only":
        if status == "recommend":
            return {
                "policy": normalized_policy,
                "mode": "full",
                "shouldDeliver": True,
                "message": str(final_result.get("message") or ""),
                "skipReason": None,
            }
        return {
            "policy": normalized_policy,
            "mode": "skip",
            "shouldDeliver": False,
            "message": None,
            "skipReason": f"Delivery policy {normalized_policy} skips {status} results.",
        }
    if normalized_policy == "always_full":
        return {
            "policy": normalized_policy,
            "mode": "full",
            "shouldDeliver": True,
            "message": str(final_result.get("message") or ""),
            "skipReason": None,
        }
    if status == "recommend":
        return {
            "policy": normalized_policy,
            "mode": "full",
            "shouldDeliver": True,
            "message": str(final_result.get("message") or ""),
            "skipReason": None,
        }
    return {
        "policy": normalized_policy,
        "mode": "summary",
        "shouldDeliver": True,
        "message": render_delivery_summary_message(final_result),
        "skipReason": None,
    }
