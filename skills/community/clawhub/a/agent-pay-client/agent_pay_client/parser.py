"""
Parse HTTP 402 responses from either the x402 protocol (JSON body with an
`accepts` array, per x402.org spec) or the L402 protocol (WWW-Authenticate
header, per lightning-l402 spec) into a common PaymentRequirement list.

This module only reads and interprets responses. It never sends a payment
by itself — see payer.py for that, which requires explicit credentials.
"""
from __future__ import annotations

import json
import re

from .models import PaymentProtocol, PaymentRequirement

L402_AUTH_RE = re.compile(
    r'L402\s+token="([^"]+)"\s*,\s*invoice="([^"]+)"', re.IGNORECASE
)


def parse_402(status_code: int, headers: dict, body: bytes | str) -> list[PaymentRequirement]:
    """Return a list of payment options offered by a 402 response.

    Prefers x402 (JSON body) if both are present, since it's checked first;
    callers can pick whichever PaymentRequirement.protocol they support.
    """
    if status_code != 402:
        return []

    options: list[PaymentRequirement] = []

    # ── Try x402 (JSON body with `accepts` array) ──
    try:
        text = body.decode("utf-8") if isinstance(body, bytes) else body
        data = json.loads(text)
        if isinstance(data, dict) and "accepts" in data:
            for opt in data["accepts"]:
                options.append(PaymentRequirement(
                    protocol=PaymentProtocol.X402,
                    network=opt.get("network"),
                    asset=opt.get("asset"),
                    pay_to=opt.get("payTo"),
                    amount_atomic=opt.get("maxAmountRequired"),
                    resource=opt.get("resource"),
                    description=opt.get("description"),
                    raw=opt,
                ))
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
        pass

    # ── Try L402 (WWW-Authenticate header) ──
    auth_header = headers.get("www-authenticate") or headers.get("WWW-Authenticate") or ""
    m = L402_AUTH_RE.search(auth_header)
    if m:
        token, invoice = m.group(1), m.group(2)
        sats = None
        try:
            text = body.decode("utf-8") if isinstance(body, bytes) else body
            data = json.loads(text)
            sats = data.get("amount_sats")
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            pass
        options.append(PaymentRequirement(
            protocol=PaymentProtocol.L402,
            amount_sats=sats,
            invoice=invoice,
            token=token,
            raw={"www_authenticate": auth_header},
        ))

    return options
