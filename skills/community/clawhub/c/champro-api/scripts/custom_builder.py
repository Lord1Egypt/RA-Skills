"""Custom Builder: designs, proofs and design-driven orders.

The Custom Builder is CHAMPRO's web-to-print configurator. A shopper embeds it
in an iframe, designs a uniform, and saving produces a **Design Session ID**.
That id is then the handle for everything else: the roster the shopper entered,
the proof PDF, the four view renders, and placing the order.

None of this exists in PromoStandards in any form — there is no service for a
design session, and PO 1.0.0 has nowhere to reference one.

Two credentials are in play and they are not interchangeable:

* `CustomerKey` — the **Custom Builder Embed Key**, used by `GetOrderInfo`,
  `GetFile` and the iframe's `lic` parameter.
* `APICustomerKey` — the **API Customer Key**, used by `PlaceOrder`.

Both are generated on the Account & Contact Info page, and confusing them fails
quietly: verified live, `GetOrderInfo` answers a bad key with `[]` and HTTP 200
— identical to a design that genuinely has no items. Every read here reports
that ambiguity rather than calling an empty answer a result.

CHAMPRO documents the Order Methods (everything below except the embed URL) as
available to *advanced* embed customers, a tier marked "Coming Soon" at the
time of writing. The endpoints are live; entitlement is per account.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any
from urllib.parse import quote, urlencode

from client import CB_BASE, ChamproClient
from errors import ChamproAPIError, ChamproTransportError, ChamproValidationError
from schemas import ShipTo

_ASSET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "cb_categories.json",
)


@lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    with open(_ASSET, encoding="utf-8") as handle:
        return json.load(handle)


FILE_TYPES = {entry["type"]: entry for entry in _catalog()["file_types"]}


def list_categories(**_credentials: Any) -> dict[str, Any]:
    """The embeddable Custom Builder categories and the downloadable file types."""

    return {
        "base_url": _catalog()["base_url"],
        "categories": _catalog()["categories"],
        "file_types": _catalog()["file_types"],
    }


def embed_url(
    category: str | int | None = None,
    *,
    cb_customer_key: str | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Build the iframe `src` for a Custom Builder category.

    `category` is a name (`"FOOTBALL"`) or an id (`1158`); omit it for all
    categories. The embed key is a licence identifier that ships to the
    browser in the URL by design — it is not a secret in the way the API
    Customer Key is, but it does identify the account, so treat a page that
    carries it as account-scoped.
    """

    from client import resolve_cb_key  # noqa: PLC0415

    key = resolve_cb_key(cb_customer_key or credentials.get("cb_customer_key"))
    entries = _catalog()["categories"]

    chosen: dict[str, Any] | None = None
    if category in (None, "", "all", "All Categories"):
        chosen = next(e for e in entries if e["id"] is None)
    else:
        text = str(category).strip().casefold()
        chosen = next(
            (
                e
                for e in entries
                if str(e["id"]) == str(category).strip()
                or str(e["name"]).casefold() == text
            ),
            None,
        )
    if chosen is None:
        raise ChamproValidationError(
            f"Unknown Custom Builder category {category!r}. Known: "
            + ", ".join(str(e["name"]) for e in entries)
        )

    base = _catalog()["base_url"]
    if chosen["id"] is None:
        url = f"{base}?{urlencode({'lic': key})}"
    else:
        # The published table encodes the name itself (MEN%27S%20SOCCER) and
        # keeps `Name` ahead of `lic`; mirror that ordering exactly.
        url = f"{base}/{chosen['id']}?Name={quote(str(chosen['name']))}&{urlencode({'lic': key})}"

    return {
        "category": chosen["name"],
        "category_id": chosen["id"],
        "url": url,
        "iframe": (
            '<iframe id="RSIFrame" frameborder="0" '
            'style="overflow:hidden;height:100%;width:800px;position:absolute;" '
            f'src="{url}"></iframe>'
        ),
    }


def _normalise_design(rows: Any) -> list[dict[str, Any]]:
    out = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        teams = []
        for team in row.get("Teams") or []:
            if not isinstance(team, dict):
                continue
            teams.append(
                {
                    "team_line_id": team.get("TeamLineId"),
                    "team_name": (str(team.get("TeamName") or "").strip() or None),
                    "quantity": team.get("Quantity"),
                    "players": [
                        {
                            "player_name": p.get("PlayerName"),
                            "player_number": p.get("PlayerNumber"),
                            "player_size": p.get("PlayerSize"),
                            "quantity": p.get("Quantity"),
                            "sku": p.get("SKU"),
                        }
                        for p in team.get("Players") or []
                        if isinstance(p, dict)
                    ],
                }
            )

        def _lead_time(value: Any) -> dict[str, Any] | None:
            if not isinstance(value, dict):
                return None
            return {
                "lead_time_id": value.get("LeadTimeId"),
                "name": value.get("LeadTimeName"),
                "days": value.get("LeadTimeDays"),
            }

        out.append(
            {
                "cart_item_id": row.get("KbCartItemId"),
                "created": row.get("CreatedDataTime"),
                "roster_line_id": row.get("RosterLineId"),
                "product_name": row.get("ProductName"),
                "design_name": row.get("DesignName"),
                "design_color": (str(row.get("DesignColor") or "").strip() or None),
                "fabric": (str(row.get("SelectedFabric") or "").strip() or None),
                "quantity": row.get("Quantity"),
                "selected_lead_time": _lead_time(row.get("SelectedLeadTime")),
                "available_lead_times": [
                    lt
                    for lt in (_lead_time(v) for v in row.get("AvailableLeadTimes") or [])
                    if lt
                ],
                "teams": teams,
            }
        )
    return out


def get_design(session_id: str | None = None, **credentials: Any) -> dict[str, Any]:
    """Roster and configuration for a saved design session.

    An empty answer is reported as `resolved: false` with an explicit note,
    because CHAMPRO returns a bare `[]` for a wrong embed key, an unknown
    session id, and a genuinely empty design alike — verified against the live
    service. Reporting "0 items" for what is actually an auth failure is how a
    caller ends up placing an order against nothing.
    """

    if not str(session_id or "").strip():
        raise ChamproValidationError("`session_id` (the saved Design Session ID) is required.")

    rows = _client(credentials).cb_order_info(str(session_id).strip())
    items = _normalise_design(rows)
    total = sum(int(i.get("quantity") or 0) for i in items)

    result: dict[str, Any] = {
        "session_id": session_id,
        "resolved": bool(items),
        "item_count": len(items),
        "total_quantity": total,
        "items": items,
        "players": [
            {**player, "team_name": team["team_name"], "product_name": item["product_name"]}
            for item in items
            for team in item["teams"]
            for player in team["players"]
        ],
    }
    if not items:
        result["note"] = (
            "GetOrderInfo returned an empty list. CHAMPRO uses the same empty response for an "
            "unknown session id, a wrong Custom Builder embed key, and a design with no items, "
            "so this does NOT confirm the design is empty. Re-check "
            "CHAMPRO_CB_CUSTOMER_KEY (the embed key, not the API key) and the session id."
        )
    return result


def get_design_file(
    session_id: str | None = None,
    file_type: str = "ProofPdf",
    *,
    output_path: str | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Download a proof PDF or a view render for a design session.

    `file_type` is one of ProofPdf, FrontImage, BackImage, LeftImage,
    RightImage. Saves to `output_path` (default: the current directory, named
    after the session).

    The proof is what a CUSTOM REST order's `ProofFileURL` must point at — and
    CHAMPRO fetches that URL server-side, so a `GetFile` link carrying your
    embed key is not usable there. Download it, host it somewhere CHAMPRO can
    reach, and pass that URL.
    """

    if not str(session_id or "").strip():
        raise ChamproValidationError("`session_id` is required.")
    if file_type not in FILE_TYPES:
        raise ChamproValidationError(
            f"Unknown file_type {file_type!r}. Valid: {', '.join(FILE_TYPES)}"
        )

    session_id = str(session_id).strip()
    entry = FILE_TYPES[file_type]
    try:
        response = _client(credentials).cb_file(session_id, file_type)
    except ChamproTransportError as exc:
        raise ChamproTransportError(
            f"{exc} — GetFile 404s on an unknown session id OR a wrong embed key; "
            "both look the same."
        ) from exc

    if response.status_code >= 400:
        raise ChamproAPIError(
            f"GetFile returned HTTP {response.status_code} for session {session_id} "
            f"({file_type}). CHAMPRO 404s an unknown session id and a wrong Custom Builder "
            "embed key identically — check both.",
            endpoint="GetFile",
        )

    path = output_path or os.path.join(os.getcwd(), f"{session_id}.{entry['extension']}")
    with open(path, "wb") as handle:
        handle.write(response.content)

    return {
        "session_id": session_id,
        "file_type": file_type,
        "path": path,
        "bytes": len(response.content),
        "content_type": response.headers.get("Content-Type"),
        "note": (
            "To use this as a CUSTOM order's ProofFileURL, host it at a URL CHAMPRO can fetch "
            "server-side; the GetFile URL itself carries your embed key and is not suitable."
        ),
    }


def place_design_order(
    session_id: str | None = None,
    ship_to: dict[str, Any] | None = None,
    *,
    po_number: str | None = None,
    lead_time_id: str | None = None,
    confirm: bool = False,
    production: bool = False,
    **credentials: Any,
) -> dict[str, Any]:
    """Place an order directly from a saved design session. **External write.**

    Unlike the REST API, the Custom Builder picks its environment with an
    `IsSandBox` boolean on the same URL, so `production` maps to
    `IsSandBox: false`. The gates are the same as `place-order`: `confirm`
    controls whether anything is sent at all, `production` whether it is real.

    CHAMPRO does not validate the ship-to address itself and requires it to
    satisfy UPS address rules (error 06 / 24 otherwise).
    """

    if not str(session_id or "").strip():
        raise ChamproValidationError("`session_id` is required.")
    if not ship_to:
        raise ChamproValidationError("`ship_to` is required (FirstName, LastName, Address1, ...).")

    from client import resolve_api_key  # noqa: PLC0415

    parsed = ShipTo.from_dict(ship_to)
    missing = [
        name
        for name, value in (
            ("first_name", parsed.first_name),
            ("last_name", parsed.last_name),
            ("address1", parsed.address1),
            ("city", parsed.city),
            ("state", parsed.state),
            ("zip", parsed.zip),
        )
        if not str(value or "").strip()
    ]
    if missing:
        raise ChamproValidationError(
            f"ship_to is missing required field(s): {', '.join(missing)} (error code 24)."
        )

    body = {
        "SessionId": str(session_id).strip(),
        "PONumber": str(po_number or "").strip(),
        "LeadTimeId": str(lead_time_id or "").strip(),
        "ShipTo": parsed.to_payload(),
        "IsSandBox": not production,
    }

    if not confirm:
        return {
            "outcome": "not_sent",
            "reason": "unconfirmed",
            "message": (
                "Nothing was sent. Pass confirm:true to submit"
                + (" as a PRODUCTION order." if production else " as a sandbox order.")
            ),
            "would_send_to": "production" if production else "sandbox",
            "request_body": body,
        }

    client = _client(credentials)
    payload = client.cb_place_order({**body, "APICustomerKey": resolve_api_key(client._api_key)})

    result_flag = str(payload.get("Result") or "").upper()
    if result_flag == "OK":
        address = payload.get("ValidatedShippingAddress") or {}
        return {
            "outcome": "placed",
            "environment": "production" if production else "sandbox",
            "order": payload.get("Order"),
            "session_id": payload.get("SessionID") or session_id,
            "validated_shipping_address": address.get("Description")
            if isinstance(address, dict)
            else address,
            "response": payload,
        }

    from errors import extract_envelope_errors  # noqa: PLC0415

    found = extract_envelope_errors(payload, "CB PlaceOrder")
    raise ChamproAPIError(
        payload.get("Message") or "Custom Builder rejected the order.",
        endpoint="CB PlaceOrder",
        errors=found,
        response=payload,
    )


def _client(credentials: dict[str, Any]) -> ChamproClient:
    return ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base") or CB_BASE,
    )
