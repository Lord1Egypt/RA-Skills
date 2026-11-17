"""Main entrypoint: fetch a paywalled resource, pay if needed, retry once."""
from __future__ import annotations

from .models import PayerConfig, PaymentProtocol
from .parser import parse_402
from .payer import pay_l402, pay_x402

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class AgentPayClient:
    """Fetch resources behind x402 or L402 paywalls.

    Requires an explicit PayerConfig with real credentials and spending
    ceilings — see models.PayerConfig. Without one, this client can still
    detect and describe a paywall (get_payment_options) but cannot pay.
    """

    def __init__(self, config: PayerConfig | None = None):
        self.config = config or PayerConfig()

    def get_payment_options(self, url: str, method: str = "POST", **kwargs) -> dict:
        """Make one request and, if it's a 402, return the parsed payment
        options without paying anything. Useful for inspecting what a
        server charges before deciding whether to proceed."""
        if not HAS_REQUESTS:
            return {"error": "requests not installed"}
        resp = requests.request(method, url, timeout=15, **kwargs)
        if resp.status_code != 402:
            return {"status_code": resp.status_code, "paywalled": False}
        options = parse_402(resp.status_code, dict(resp.headers), resp.content)
        return {
            "status_code": 402,
            "paywalled": True,
            "options": [o.__dict__ for o in options],
        }

    def fetch(self, url: str, method: str = "POST", **kwargs) -> dict:
        """Fetch a resource, automatically paying via x402 or L402 if the
        server returns 402 AND the configured PayerConfig allows it.
        Returns the final response (paid or not) plus a `payment` field
        describing what happened.
        """
        if not HAS_REQUESTS:
            return {"error": "requests not installed"}

        resp = requests.request(method, url, timeout=15, **kwargs)
        if resp.status_code != 402:
            return {"status_code": resp.status_code, "body": resp.text, "payment": None}

        options = parse_402(resp.status_code, dict(resp.headers), resp.content)
        if not options:
            return {"status_code": 402, "body": resp.text, "payment": {"error": "Could not parse payment requirements"}}

        # Prefer x402 if we have EVM credentials configured, else fall back to L402.
        x402_opts = [o for o in options if o.protocol == PaymentProtocol.X402]
        l402_opts = [o for o in options if o.protocol == PaymentProtocol.L402]

        result = None
        if x402_opts and self.config.evm_private_key:
            result = pay_x402(x402_opts[0], self.config)
        elif l402_opts:
            result = pay_l402(l402_opts[0], self.config)
        elif x402_opts:
            result = pay_x402(x402_opts[0], self.config)  # will report the missing-credential error

        if not result or not result.success:
            return {
                "status_code": 402, "body": resp.text,
                "payment": {"success": False, "error": result.error if result else "No payable option found"},
            }

        headers = dict(kwargs.pop("headers", {}) or {})
        headers[result.proof_header_name] = result.proof_header_value
        retry = requests.request(method, url, headers=headers, timeout=15, **kwargs)
        return {
            "status_code": retry.status_code, "body": retry.text,
            "payment": {"success": True, "protocol": result.protocol.value, "tx_hash": result.tx_hash},
        }
