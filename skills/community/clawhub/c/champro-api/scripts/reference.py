"""Offline lookups: shipping methods and the error-code table."""

from __future__ import annotations

from typing import Any

import shipping
from errors import (
    CB_MESSAGE_CODES,
    SETUP_MESSAGE_CODES,
    TERMINAL_MESSAGE_CODES,
    parse_message_code,
)

# What to actually do about each code. The API tells you what went wrong; this
# says where the fix lives, which is usually not in the order payload.
_REMEDIES: dict[str, str] = {
    "01": "CHAMPRO fetches ProofFileURL server-side. Host it somewhere publicly reachable — a "
    "signed/expiring or key-bearing URL will not work.",
    "02": "Re-export the proof as PDF, JPG, JPEG or PNG and make the URL end in that extension.",
    "03": "Field names or types are wrong. Run `preview-order` and compare against the reference.",
    "04": "Account-level: your CHAMPRO payment terms block API ordering. Contact CHAMPRO.",
    "05": "Account-level: the API Customer Key is not valid for ordering. Contact CHAMPRO support.",
    "06": "The address failed UPS verification. CHAMPRO does not correct addresses — validate at "
    "https://www.ups.com/us/en/support/shipping-support/shipping-costs-rates/calculate-time-cost.page "
    "before resubmitting.",
    "07": "One order cannot hold both custom and stock lines. Run `split-mixed-cart`.",
    "08": "The SKU is not in the product master's grid. Run `find-skus` to get the real one.",
    "09": "Same as 04 — payment terms. Account-level, not a payload problem.",
    "10": "Same as 05 — customer validation. Account-level.",
    "11": "Set `warehouse` on each STOCK line (IL/CA/DR), or pass autowarehouse:true. "
    "`plan-warehouses` picks one that can actually cover the quantity.",
    "12": "Server-side failure with no client fix. Do NOT blind-retry: check `get-order-status` "
    "for any SubOrderID first, then contact CHAMPRO.",
    "13": "The chosen warehouse cannot cover the line. Re-run `plan-warehouses`, split the line "
    "across warehouses, or use autowarehouse.",
    "14": "Same as 12 — verify before any retry.",
    "15": "Your egress IP is not on the allowlist. Run `check-access` to read it, then add it "
    "under API Allowed IP Addresses at https://champrosports.com/AccountAndContactInfo.",
    "16": "The API Customer Key is wrong. Regenerate it on the Account & Contact Info page.",
    "17": "PO number is missing or malformed. It is required and must be unique per order.",
    "18": "CHAMPRO could not persist the order. Check `get-order-status` before resubmitting.",
    "19": "The envelope shape is wrong. Compare `preview-order` output against the reference.",
    "20": "The key is well-formed but unknown to CHAMPRO. Regenerate it.",
    "21": "A CUSTOM order requires `lead_time`. Get valid names from `get-lead-times`.",
    "22": "The lead-time name is not offered for this product. `get-lead-times` lists what is.",
    "23": "Account-level: your payment terms do not permit API ordering. Contact CHAMPRO.",
    "24": "Recipient name or address is incomplete/invalid. All of first name, last name, address, "
    "city, 2-letter state, ZIP and phone are required.",
    "25": "Quantity must be a MULTIPLE of the MOQ, not merely above it. `validate-order` with "
    "`product_masters` catches this before sending.",
}

# The REST API embeds dotted codes in the message text rather than as a field.
_DOTTED_FAMILIES: dict[str, str] = {
    "E2": "Order processing — a line or order was rejected during placement.",
    "E3": "Catalog/SKU lookup — the SKU is unknown to CHAMPRO.",
    "E4": "Authentication — the API Customer Key or the calling IP was rejected.",
}


def list_shipping_methods(
    carrier: str | None = None,
    billing_type: str | None = None,
    **_credentials: Any,
) -> dict[str, Any]:
    """The published ShippingMethod values, with their billing coupling.

    Any method whose `billing_type` is set bills a party other than your
    CHAMPRO account and therefore requires `shipping_customer_account` on the
    order.
    """

    rows = shipping.methods()
    if carrier:
        rows = [m for m in rows if (m.get("carrier") or "").casefold() == carrier.casefold()]
    if billing_type:
        wanted = billing_type.casefold()
        if wanted in ("prepaid", "none", "null"):
            rows = [m for m in rows if not m.get("billing_type")]
        else:
            rows = [m for m in rows if (m.get("billing_type") or "").casefold() == wanted]

    return {
        "count": len(rows),
        "methods": rows,
        "requires_shipping_account": [m["name"] for m in rows if m.get("billing_type")],
        "warehouses": shipping.warehouses(),
        "note": (
            "ShippingMethod applies to STOCK orders only; a CUSTOM order is routed by its "
            "LeadTime. Methods with a billing_type require `shipping_customer_account`."
        ),
    }


def explain_error(
    code: str | None = None,
    message: str | None = None,
    **_credentials: Any,
) -> dict[str, Any]:
    """Look up a CHAMPRO error code, or pull one out of an error message."""

    resolved = str(code or "").strip()
    if not resolved and message:
        resolved = parse_message_code(message) or ""
    if not resolved:
        return {
            "code": None,
            "message": (
                "No error code found. Custom Builder codes are two digits ('25'); REST codes are "
                "dotted and embedded in the text ('E2.8.3: ...')."
            ),
            "known_codes": sorted(CB_MESSAGE_CODES),
        }

    if resolved.isdigit():
        padded = resolved.zfill(2)
        description = CB_MESSAGE_CODES.get(padded)
        if description is None:
            return {"code": padded, "known": False, "known_codes": sorted(CB_MESSAGE_CODES)}
        return {
            "code": padded,
            "known": True,
            "description": description,
            "remedy": _REMEDIES.get(padded),
            "account_level": padded in SETUP_MESSAGE_CODES,
            "retryable": padded not in TERMINAL_MESSAGE_CODES,
        }

    family = resolved.split(".")[0].upper()
    return {
        "code": resolved.upper(),
        "known": family in _DOTTED_FAMILIES,
        "family": family,
        "description": _DOTTED_FAMILIES.get(family, "Undocumented REST error family."),
        "remedy": (
            "REST codes are prefixes on a free-text message; the text after the colon names the "
            "SKU or field. Match it to the two-digit table via `explain-error` with that code."
        ),
        "retryable": False,
    }
