"""Data models for agent-pay-client."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PaymentProtocol(str, Enum):
    X402 = "x402"
    L402 = "l402"
    UNKNOWN = "unknown"


@dataclass
class PaymentRequirement:
    """Parsed terms of a single payment option from a 402 response."""
    protocol: PaymentProtocol
    network: str | None = None          # e.g. "base" for x402
    asset: str | None = None            # token contract address (x402)
    pay_to: str | None = None           # receiving address (x402)
    amount_atomic: str | None = None    # x402: atomic units of `asset`
    amount_sats: int | None = None      # L402: Lightning invoice amount
    invoice: str | None = None          # L402: BOLT11 invoice string
    token: str | None = None            # L402: payment_hash / macaroon token
    resource: str | None = None
    description: str | None = None
    raw: dict = field(default_factory=dict)


@dataclass
class PaymentResult:
    success: bool
    protocol: PaymentProtocol
    proof_header_name: str | None = None   # header name to attach on retry
    proof_header_value: str | None = None  # header value to attach on retry
    tx_hash: str | None = None
    error: str | None = None


@dataclass
class PayerConfig:
    """Explicit, user-provided credentials. Nothing here has a default —
    every field must be deliberately supplied. No spending is possible
    without the caller having configured one of these themselves."""
    # x402 (EVM)
    evm_private_key: str | None = None   # hex private key, from env var only
    evm_rpc_url: str | None = None
    max_x402_atomic: str | None = None   # hard ceiling per single payment
    # L402 (Lightning) — manual-approval mode by default
    lightning_auto_pay: bool = False     # must be explicitly opted in
    lnd_rest_url: str | None = None
    lnd_macaroon_hex: str | None = None
    max_l402_sats: int | None = None     # hard ceiling per single payment
