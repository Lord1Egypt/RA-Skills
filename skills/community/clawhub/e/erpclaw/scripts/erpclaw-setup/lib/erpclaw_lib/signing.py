"""Registry signature verification for foundation reconciliation.

The published `module_registry.json` is signed with ed25519. The public key
is embedded here. Reconciliation refuses to trust an unsigned, tampered, or
downgraded registry.

Trust root: ed25519 keypair held by the publisher (Nik). The key list below
supports rotation: new key added with valid_from; old key kept for grace
period; the verifier accepts any currently-valid key.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

__all__ = [
    "TrustedKey",
    "TRUSTED_KEYS",
    "verify_registry_signature",
    "fingerprint",
    "REGISTRY_VERSION_FIELD",
    "SIGNED_AT_FIELD",
]


@dataclass(frozen=True)
class TrustedKey:
    """A public key the verifier accepts as a valid signer.

    public_key_hex: 64 hex chars (32 raw bytes) of an ed25519 public key.
    valid_until: ISO 8601 date or None for indefinite. Keys past their
        valid_until are NOT accepted.
    label: human-friendly identifier for logging / fingerprint output.
    """

    public_key_hex: str
    valid_until: Optional[str]
    label: str


# Production trust root.
# Fingerprint d471:335b:0e4d:75ce — generated 2026-05-04 for v4.1.6.
TRUSTED_KEYS: tuple[TrustedKey, ...] = (
    TrustedKey(
        public_key_hex="d471335b0e4d75ce9a4cc58e34446bbfdd1c1fd77fbe2d73e300c3850c0827c5",
        valid_until=None,
        label="erpclaw-foundation-signer-2026-05-04",
    ),
)


REGISTRY_VERSION_FIELD = "registry_version"
SIGNED_AT_FIELD = "signed_at"


def fingerprint(public_key_hex: str) -> str:
    """Short human-readable fingerprint of an ed25519 public key.

    Returns first 16 hex chars in 4:4:4:4 colon format. Use for CHANGELOG
    documentation and out-of-band verification.
    """
    h = public_key_hex.lower()
    return f"{h[0:4]}:{h[4:8]}:{h[8:12]}:{h[12:16]}"


def verify_registry_signature(
    registry_bytes: bytes,
    signature_hex: str,
    *,
    accepted_keys: tuple[TrustedKey, ...] = TRUSTED_KEYS,
    today_iso: Optional[str] = None,
) -> TrustedKey:
    """Verify ed25519 signature against registry bytes.

    Returns the TrustedKey that successfully verified, or raises
    InvalidSignature.

    today_iso: ISO date for valid_until comparison; defaults to current UTC.
        Tests inject deterministic dates.
    """
    if not signature_hex:
        raise InvalidSignature("empty signature")
    try:
        sig_bytes = bytes.fromhex(signature_hex.strip())
    except ValueError as e:
        raise InvalidSignature(f"signature is not valid hex: {e}")
    if len(sig_bytes) != 64:
        raise InvalidSignature(f"ed25519 signature must be 64 bytes, got {len(sig_bytes)}")

    if today_iso is None:
        from datetime import datetime, timezone
        today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    last_err: Optional[Exception] = None
    for trusted in accepted_keys:
        if trusted.valid_until is not None and today_iso > trusted.valid_until:
            continue
        try:
            pub_bytes = bytes.fromhex(trusted.public_key_hex)
        except ValueError:
            continue
        if len(pub_bytes) != 32:
            continue
        try:
            pk = Ed25519PublicKey.from_public_bytes(pub_bytes)
            pk.verify(sig_bytes, registry_bytes)
            return trusted
        except (InvalidSignature, ValueError) as e:
            last_err = e
            continue

    raise InvalidSignature(
        f"no trusted key verified the signature; last error: {last_err}"
    )
