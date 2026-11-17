"""Setup diagnostics.

CHAMPRO gates `PlaceOrder` on an **IP allowlist** maintained per account on the
Account & Contact Info page (error code 15). On a hosted or containerised agent
the egress IP is not the machine's own address and may change, which turns a
correct order into an unexplained rejection.

`check-access` answers "is this environment set up" before an order is at
stake: it reports the egress IP to paste into the allowlist, and probes the
read endpoints to tell an invalid key apart from an un-allowlisted IP — two
failures with very different fixes.
"""

from __future__ import annotations

from typing import Any

from client import ChamproClient, resolve_cb_key
from errors import ChamproAPIError, ChamproConfigError, ChamproError

# ProductInfo is a read: it validates the key without placing anything. A
# master that does not exist still authenticates, so any value works — this one
# comes from CHAMPRO's own documented example.
_PROBE_MASTER = "JSBJ8"


def _mask(key: str) -> str:
    return f"{key[:8]}…{key[-4:]}" if len(key) > 14 else "set"


def check_access(
    product_master: str = _PROBE_MASTER,
    *,
    show_egress_ip: bool = True,
    **credentials: Any,
) -> dict[str, Any]:
    """Report credential and network readiness. Places nothing, orders nothing."""

    client = ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base"),
    )

    report: dict[str, Any] = {"checks": {}, "ready_to_order": False}

    # -- API customer key ----------------------------------------------------
    try:
        key = client.api_key
        report["checks"]["api_customer_key"] = {"present": True, "value": _mask(key)}
    except ChamproConfigError as exc:
        report["checks"]["api_customer_key"] = {"present": False, "message": str(exc)}

    # -- Custom Builder embed key (optional) ---------------------------------
    try:
        report["checks"]["cb_customer_key"] = {
            "present": True,
            "value": _mask(resolve_cb_key(credentials.get("cb_customer_key"))),
        }
    except ChamproConfigError as exc:
        report["checks"]["cb_customer_key"] = {
            "present": False,
            "message": str(exc),
            "impact": "Custom Builder actions only; REST actions are unaffected.",
        }

    # -- authenticated read --------------------------------------------------
    if report["checks"]["api_customer_key"].get("present"):
        try:
            client.product_info(product_master)
            report["checks"]["authenticated_read"] = {
                "ok": True,
                "endpoint": "ProductInfo",
                "product_master": product_master,
            }
        except ChamproAPIError as exc:
            report["checks"]["authenticated_read"] = {
                "ok": False,
                "endpoint": "ProductInfo",
                "message": str(exc),
                "codes": exc.codes,
                "setup_problem": exc.is_setup_problem,
                "fix": (
                    "Regenerate the API Customer Key on "
                    "https://champrosports.com/AccountAndContactInfo"
                    if exc.is_setup_problem
                    else f"ProductMaster {product_master!r} may not exist; try another."
                ),
            }
        except ChamproError as exc:
            report["checks"]["authenticated_read"] = {"ok": False, "message": str(exc)}

    # -- egress IP -----------------------------------------------------------
    #
    # Reported, never auto-registered: adding an IP to the allowlist is an
    # account change on CHAMPRO's website, and the account owner makes it.
    if show_egress_ip:
        report["checks"]["egress_ip"] = _egress_ip()

    read_ok = report["checks"].get("authenticated_read", {}).get("ok")
    report["ready_to_order"] = bool(read_ok)
    report["next_steps"] = _next_steps(report)
    return report


def _egress_ip() -> dict[str, Any]:
    try:
        import requests  # noqa: PLC0415

        response = requests.get("https://api.ipify.org", timeout=15)
        response.raise_for_status()
        return {
            "ip": response.text.strip(),
            "note": (
                "PlaceOrder requires this IP on your CHAMPRO allowlist (error code 15). Add it "
                "under API Allowed IP Addresses at "
                "https://champrosports.com/AccountAndContactInfo. On a hosted agent this address "
                "can change between runs — re-check it if a previously working order starts "
                "failing with code 15."
            ),
        }
    except Exception as exc:  # noqa: BLE001 - diagnostics must never be the failure
        return {"ip": None, "message": f"Could not determine egress IP: {exc}"}


def _next_steps(report: dict[str, Any]) -> list[str]:
    steps: list[str] = []
    checks = report["checks"]
    if not checks.get("api_customer_key", {}).get("present"):
        steps.append(
            "Set CHAMPRO_API_CUSTOMER_KEY (generate it on "
            "https://champrosports.com/AccountAndContactInfo)."
        )
    read = checks.get("authenticated_read")
    if read and not read.get("ok"):
        steps.append(read.get("fix") or "Resolve the ProductInfo failure above.")
    ip = checks.get("egress_ip", {}).get("ip")
    if ip and report["ready_to_order"]:
        steps.append(
            f"Reads work. Before placing a PRODUCTION order, confirm {ip} is on the API Allowed "
            "IP Addresses list — reads do not require it, PlaceOrder does."
        )
    if not steps:
        steps.append("Setup looks complete. Rehearse with place-order against the sandbox first.")
    return steps
