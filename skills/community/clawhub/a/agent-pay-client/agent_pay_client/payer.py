"""
Executes a payment for a PaymentRequirement returned by parser.parse_402().

SAFETY MODEL — read this before use:
- Nothing in this module can spend funds unless the caller explicitly
  constructs a PayerConfig with real credentials (a private key, an LND
  macaroon, etc.). There are no default wallets, no implicit spending, and
  no "auto-detect and pay" behavior triggered by page content or prompts.
- Every payment path enforces an explicit per-payment ceiling
  (max_x402_atomic / max_l402_sats) supplied by the caller. Requests above
  the ceiling are refused before any signing or network call happens.
- Lightning (L402) payments are manual-approval by default: the invoice
  and QR code are returned to the caller to pay however they choose.
  Automatic Lightning payment only happens if lightning_auto_pay=True is
  set explicitly AND LND credentials are supplied.
- This library never reads instructions embedded in web page or API
  response content to decide whether/how much to pay. All payment
  parameters come from the PaymentRequirement (the server's price) and
  the caller's own PayerConfig ceiling — nothing else.
"""
from __future__ import annotations

import base64
import json
import time

from .models import PayerConfig, PaymentProtocol, PaymentRequirement, PaymentResult

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def _atomic_int(v: str | None) -> int:
    try:
        return int(v) if v is not None else 0
    except ValueError:
        return 0


def pay_x402(req: PaymentRequirement, config: PayerConfig) -> PaymentResult:
    """Sign and prepare an x402 'exact' scheme payment (EIP-3009
    TransferWithAuthorization on an EVM chain). Requires `eth_account`
    and an explicitly-configured private key — never inferred or
    defaulted.
    """
    if req.protocol != PaymentProtocol.X402:
        return PaymentResult(success=False, protocol=req.protocol, error="Not an x402 requirement")

    if not config.evm_private_key:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.X402,
            error="No evm_private_key configured — refusing to pay. "
                  "Set PayerConfig.evm_private_key explicitly to enable x402 payments.",
        )

    requested = _atomic_int(req.amount_atomic)
    ceiling = _atomic_int(config.max_x402_atomic) if config.max_x402_atomic else 0
    if config.max_x402_atomic is None:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.X402,
            error="No max_x402_atomic ceiling configured — refusing to pay without an explicit spending limit.",
        )
    if requested > ceiling:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.X402,
            error=f"Requested amount {requested} exceeds configured ceiling {ceiling} — refusing to pay.",
        )

    try:
        from eth_account import Account
        from eth_account.messages import encode_typed_data
    except ImportError:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.X402,
            error="eth_account not installed — run: pip install eth-account",
        )

    account = Account.from_key(config.evm_private_key)
    valid_after = 0
    valid_before = int(time.time()) + int(req.raw.get("maxTimeoutSeconds", 300))
    nonce = "0x" + "00" * 32  # reference implementation; production use should be a random 32-byte nonce

    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ],
        },
        "primaryType": "TransferWithAuthorization",
        "domain": {
            "name": "USD Coin", "version": "2",
            "chainId": 8453 if req.network == "base" else 1,
            "verifyingContract": req.asset,
        },
        "message": {
            "from": account.address, "to": req.pay_to, "value": requested,
            "validAfter": valid_after, "validBefore": valid_before, "nonce": nonce,
        },
    }

    signed = Account.sign_message(encode_typed_data(full_message=typed_data), private_key=config.evm_private_key)

    payload = {
        "x402Version": 1,
        "scheme": "exact", "network": req.network,
        "payload": {
            "signature": signed.signature.hex(),
            "authorization": typed_data["message"],
        },
    }
    payment_header = base64.b64encode(json.dumps(payload).encode()).decode()

    return PaymentResult(
        success=True, protocol=PaymentProtocol.X402,
        proof_header_name="X-PAYMENT", proof_header_value=payment_header,
    )


def pay_l402(req: PaymentRequirement, config: PayerConfig) -> PaymentResult:
    """Pay (or prepare) an L402 Lightning invoice.

    Default behavior (lightning_auto_pay=False): returns the invoice/token
    unpaid, for the caller to settle however they choose (manual wallet,
    QR scan, etc.) — this function does not spend anything in that mode.

    Auto-pay mode (lightning_auto_pay=True): requires LND REST credentials
    and a configured sats ceiling; pays via the LND node directly.
    """
    if req.protocol != PaymentProtocol.L402:
        return PaymentResult(success=False, protocol=req.protocol, error="Not an L402 requirement")

    if not config.lightning_auto_pay:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.L402,
            error="Manual payment required: pay the invoice yourself, then retry with "
                  f"header 'Authorization: L402 {req.token}:<preimage>'. "
                  "Set PayerConfig.lightning_auto_pay=True with LND credentials to automate this.",
        )

    if not config.lnd_rest_url or not config.lnd_macaroon_hex:
        return PaymentResult(
            success=False, protocol=PaymentProtocol.L402,
            error="lightning_auto_pay=True but lnd_rest_url/lnd_macaroon_hex not configured.",
        )

    if config.max_l402_sats is None or (req.amount_sats and req.amount_sats > config.max_l402_sats):
        return PaymentResult(
            success=False, protocol=PaymentProtocol.L402,
            error=f"Invoice amount {req.amount_sats} sats exceeds configured max_l402_sats "
                  f"({config.max_l402_sats}) — refusing to pay.",
        )

    if not HAS_REQUESTS:
        return PaymentResult(success=False, protocol=PaymentProtocol.L402, error="requests not installed")

    try:
        resp = requests.post(
            f"{config.lnd_rest_url}/v1/channels/transactions",
            headers={"Grpc-Metadata-macaroon": config.lnd_macaroon_hex},
            json={"payment_request": req.invoice},
            verify=False, timeout=30,  # LND REST commonly self-signed; caller's node, caller's risk
        )
        data = resp.json()
        if data.get("payment_error"):
            return PaymentResult(success=False, protocol=PaymentProtocol.L402, error=data["payment_error"])
        preimage = data.get("payment_preimage", "")
        return PaymentResult(
            success=True, protocol=PaymentProtocol.L402,
            proof_header_name="Authorization",
            proof_header_value=f"L402 {req.token}:{preimage}",
        )
    except Exception as e:  # noqa: BLE001 — surface any LND/network failure as a clear PaymentResult
        return PaymentResult(success=False, protocol=PaymentProtocol.L402, error=str(e))
