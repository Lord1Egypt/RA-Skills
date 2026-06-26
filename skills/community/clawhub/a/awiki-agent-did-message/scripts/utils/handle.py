"""Handle (short name) registration and resolution utilities.

[INPUT]: httpx.AsyncClient, SDKConfig, DIDIdentity, rpc_call(), create_identity(), register_did()
[OUTPUT]: send_otp(), register_handle(), register_handle_with_email(),
          send_email_verification(), check_email_verified(),
          ensure_email_verification(), wait_for_email_verification(),
          recover_handle(), resolve_handle(), lookup_handle(), normalize_phone(),
          bind_email_send(), bind_phone_send_otp(), bind_phone_verify(),
          EmailVerificationResult
[POS]: Wraps Handle registration and resolution flows, built on top of auth.py and identity.py.
       Uses JSON-RPC 2.0 endpoints: /user-service/handle/rpc and /user-service/did-auth/rpc.
       Uses REST endpoints: /user-service/auth/email-send and /user-service/auth/email-status.

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import re
import time
from typing import Any

import httpx

from utils.config import SDKConfig
from utils.identity import DIDIdentity, create_identity
from utils.rpc import JsonRpcError, rpc_call
from utils.auth import get_jwt_via_wba


HANDLE_RPC = "/user-service/handle/rpc"
DID_AUTH_RPC = "/user-service/did-auth/rpc"

# ==================== Email verification REST endpoints ====================

EMAIL_SEND_REST = "/user-service/auth/email-send"
EMAIL_STATUS_REST = "/user-service/auth/email-status"

# ==================== Account binding REST endpoints ====================

PHONE_BIND_SEND_REST = "/user-service/auth/phone-bind-send"
PHONE_BIND_VERIFY_REST = "/user-service/auth/phone-bind-verify"


def _sanitize_otp(code: str) -> str:
    """Strip all whitespace (spaces, newlines, tabs) from an OTP code."""
    return re.sub(r"\s+", "", code)

# International phone format: +{country_code}{number}
_PHONE_INTL_RE = re.compile(r"^\+\d{1,3}\d{6,14}$")
# China local format: 11 digits starting with 1
_PHONE_CN_LOCAL_RE = re.compile(r"^1[3-9]\d{9}$")
DEFAULT_COUNTRY_CODE = "+86"


def normalize_phone(phone: str) -> str:
    """Normalize a phone number to international format.

    - Already international (+XX...) -> return as-is if valid.
    - China local format (1XXXXXXXXXX) -> prepend +86.
    - Otherwise -> raise ValueError with guidance.

    Args:
        phone: Raw phone number input.

    Returns:
        Phone number in international format (e.g., +8613800138000).

    Raises:
        ValueError: Invalid phone number format.
    """
    phone = phone.strip()

    if phone.startswith("+"):
        if _PHONE_INTL_RE.fullmatch(phone):
            return phone
        raise ValueError(
            f"Invalid international phone number: {phone}. "
            f"Expected format: +<country_code><number> (e.g., +8613800138000, +14155552671). "
            f"Please check the country code."
        )

    if _PHONE_CN_LOCAL_RE.fullmatch(phone):
        return f"{DEFAULT_COUNTRY_CODE}{phone}"

    raise ValueError(
        f"Invalid phone number: {phone}. "
        f"Use international format with country code: +<country_code><number> "
        f"(e.g., +8613800138000 for China, +14155552671 for US). "
        f"China local numbers (11 digits starting with 1) are auto-prefixed with +86."
    )


async def send_otp(
    client: httpx.AsyncClient,
    phone: str,
) -> dict[str, Any]:
    """Send OTP verification code for Handle registration.

    Args:
        client: HTTP client pointing to user-service.
        phone: Phone number in international format (e.g., +8613800138000).
               China local numbers (11 digits) are auto-prefixed with +86.

    Returns:
        RPC result dict.

    Raises:
        ValueError: Invalid phone number format.
        JsonRpcError: When sending fails (may indicate wrong country code).
    """
    normalized = normalize_phone(phone)
    try:
        return await rpc_call(client, HANDLE_RPC, "send_otp", {"phone": normalized})
    except JsonRpcError as e:
        raise JsonRpcError(
            e.code,
            f"{e.message}. Please verify the phone number and country code "
            f"(current: {normalized}).",
            e.data,
        ) from e


async def register_handle(
    client: httpx.AsyncClient,
    config: SDKConfig,
    phone: str,
    otp_code: str,
    handle: str,
    invite_code: str | None = None,
    name: str | None = None,
    is_public: bool = False,
    services: list[dict[str, Any]] | None = None,
) -> DIDIdentity:
    """One-stop Handle registration: create identity -> register DID with Handle -> obtain JWT.

    Creates a key-bound DID with Handle as path prefix (e.g., did:wba:awiki.ai:alice:k1_<fp>),
    then calls did_auth.register with Handle parameters.

    Args:
        client: HTTP client pointing to user-service.
        config: SDK configuration.
        phone: Phone number in international format (e.g., +8613800138000).
               China local numbers (11 digits) are auto-prefixed with +86.
        otp_code: OTP verification code.
        handle: Handle local-part (e.g., "alice").
        invite_code: Invite code (required for short handles <= 4 chars).
        name: Display name.
        is_public: Whether publicly visible.
        services: Custom service entry list for DID document.

    Returns:
        DIDIdentity with user_id and jwt_token populated.

    Raises:
        ValueError: Invalid phone number format.
        JsonRpcError: When registration fails.
    """
    normalized = normalize_phone(phone)

    # 1. Create key-bound DID identity with handle as path prefix
    identity = create_identity(
        hostname=config.did_domain,
        path_prefix=[handle],
        proof_purpose="authentication",
        domain=config.did_domain,
        services=services,
    )

    # 2. Register DID with Handle parameters
    payload: dict[str, Any] = {
        "did_document": identity.did_document,
        "handle": handle,
        "phone": normalized,
        "otp_code": _sanitize_otp(otp_code),
    }
    if invite_code is not None:
        payload["invite_code"] = invite_code
    if name is not None:
        payload["name"] = name
    if is_public:
        payload["is_public"] = True

    reg_result = await rpc_call(client, DID_AUTH_RPC, "register", payload)
    identity.user_id = reg_result["user_id"]

    # 3. Registration returns access_token for handle mode
    if reg_result.get("access_token"):
        identity.jwt_token = reg_result["access_token"]
    else:
        identity.jwt_token = await get_jwt_via_wba(client, identity, config.did_domain)

    return identity


# ==================== Email verification functions ====================


async def send_email_verification(
    client: httpx.AsyncClient,
    email: str,
) -> dict[str, Any]:
    """Send email verification (activation link) for Handle registration.

    Args:
        client: HTTP client pointing to user-service.
        email: Email address.

    Returns:
        Response dict with "message" field.

    Raises:
        httpx.HTTPStatusError: On HTTP error (429 rate limit, 400 bad request, etc).
    """
    resp = await client.post(EMAIL_SEND_REST, json={"email": email.strip().lower()})
    resp.raise_for_status()
    return resp.json()


async def check_email_verified(
    client: httpx.AsyncClient,
    email: str,
) -> tuple[bool, str | None]:
    """Check if an email has been verified.

    Args:
        client: HTTP client pointing to user-service.
        email: Email address.

    Returns:
        (verified: bool, verified_at: str | None)
    """
    resp = await client.get(EMAIL_STATUS_REST, params={"email": email.strip().lower()})
    resp.raise_for_status()
    data = resp.json()
    return data.get("verified", False), data.get("verified_at")


@dataclass(frozen=True)
class EmailVerificationResult:
    """Result of a non-interactive email verification attempt."""

    verified: bool
    activation_sent: bool
    verified_at: str | None = None


async def ensure_email_verification(
    client: httpx.AsyncClient,
    email: str,
    send_fn: Any | None = None,
    *,
    wait: bool = False,
    timeout: int = 300,
    poll_interval: float = 5.0,
) -> EmailVerificationResult:
    """Ensure email verification using a pure non-interactive flow.

    Shared helper that encapsulates the common "check status -> send email if
    needed -> optionally poll for verification" flow used by register_handle.py
    and bind_contact.py.

    Args:
        client: HTTP client pointing to user-service.
        email: Email address to verify.
        send_fn: Async callable to send the activation email.
                 If None, uses send_email_verification(client, email).
                 For binding flow, pass a lambda that includes jwt_token.
        wait: Whether to poll until the email becomes verified.
        timeout: Maximum number of seconds to wait when wait=True.
        poll_interval: Seconds between verification checks when wait=True.

    Raises:
        httpx.HTTPStatusError: On HTTP error from send or check calls.
        ValueError: If timeout or poll_interval is invalid.
    """
    normalized_email = email.strip().lower()
    verified, verified_at = await check_email_verified(client, normalized_email)
    if verified:
        return EmailVerificationResult(
            verified=True,
            activation_sent=False,
            verified_at=verified_at,
        )

    print(f"\nSending activation email to {normalized_email}...")
    if send_fn is not None:
        await send_fn()
    else:
        await send_email_verification(client, normalized_email)
    print("Activation email sent. Please check your inbox and click the activation link.")

    if not wait:
        return EmailVerificationResult(
            verified=False,
            activation_sent=True,
            verified_at=None,
        )

    if timeout < 0:
        raise ValueError("email verification timeout must be >= 0 seconds.")
    if poll_interval <= 0:
        raise ValueError("email verification poll interval must be > 0 seconds.")

    print(
        "Waiting for email verification "
        f"(timeout: {timeout}s, poll interval: {poll_interval:g}s)..."
    )
    deadline = time.monotonic() + timeout
    while True:
        verified, verified_at = await check_email_verified(client, normalized_email)
        if verified:
            return EmailVerificationResult(
                verified=True,
                activation_sent=True,
                verified_at=verified_at,
            )

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return EmailVerificationResult(
                verified=False,
                activation_sent=True,
                verified_at=None,
            )

        await asyncio.sleep(min(poll_interval, remaining))


async def wait_for_email_verification(
    client: httpx.AsyncClient,
    email: str,
    send_fn: Any | None = None,
    timeout: int = 300,
    poll_interval: float = 5.0,
) -> EmailVerificationResult:
    """Backward-compatible wrapper for fully waiting on email verification."""
    return await ensure_email_verification(
        client,
        email,
        send_fn=send_fn,
        wait=True,
        timeout=timeout,
        poll_interval=poll_interval,
    )


async def register_handle_with_email(
    client: httpx.AsyncClient,
    config: SDKConfig,
    email: str,
    handle: str,
    invite_code: str | None = None,
    name: str | None = None,
    is_public: bool = False,
    services: list[dict[str, Any]] | None = None,
) -> DIDIdentity:
    """One-stop Handle registration with email: create identity -> register DID with Handle -> obtain JWT.

    Email must be verified via activation link before calling this function.

    Args:
        client: HTTP client pointing to user-service.
        config: SDK configuration.
        email: Verified email address.
        handle: Handle local-part (e.g., "alice").
        invite_code: Invite code (required for short handles <= 4 chars).
        name: Display name.
        is_public: Whether publicly visible.
        services: Custom service entry list for DID document.

    Returns:
        DIDIdentity with user_id and jwt_token populated.

    Raises:
        JsonRpcError: When registration fails (email not verified, handle taken, etc).
    """
    # 1. Create key-bound DID identity with handle as path prefix
    identity = create_identity(
        hostname=config.did_domain,
        path_prefix=[handle],
        proof_purpose="authentication",
        domain=config.did_domain,
        services=services,
    )

    # 2. Register DID with Handle + email parameters (no phone/otp_code needed)
    payload: dict[str, Any] = {
        "did_document": identity.did_document,
        "handle": handle,
        "email": email.strip().lower(),
    }
    if invite_code is not None:
        payload["invite_code"] = invite_code
    if name is not None:
        payload["name"] = name
    if is_public:
        payload["is_public"] = True

    reg_result = await rpc_call(client, DID_AUTH_RPC, "register", payload)
    identity.user_id = reg_result["user_id"]

    # 3. Registration returns access_token for handle mode
    if reg_result.get("access_token"):
        identity.jwt_token = reg_result["access_token"]
    else:
        identity.jwt_token = await get_jwt_via_wba(client, identity, config.did_domain)

    return identity


# ==================== Account binding functions ====================


async def bind_email_send(
    client: httpx.AsyncClient,
    email: str,
    jwt_token: str,
) -> dict[str, Any]:
    """Send email verification for binding email to an existing account.

    Reuses the /auth/email-send endpoint with JWT header.
    After this call, user must click the activation link in their email.
    Then call check_email_verified() to confirm binding status.

    Args:
        client: HTTP client pointing to user-service.
        email: Email address to bind.
        jwt_token: User's JWT access token.

    Returns:
        Response dict with "message" field.

    Raises:
        httpx.HTTPStatusError: On HTTP error (429 rate limit, 400 bad request, etc).
    """
    resp = await client.post(
        EMAIL_SEND_REST,
        json={"email": email.strip().lower()},
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    resp.raise_for_status()
    return resp.json()


async def bind_phone_send_otp(
    client: httpx.AsyncClient,
    phone: str,
    jwt_token: str,
) -> dict[str, Any]:
    """Send OTP for binding phone to an existing account.

    Args:
        client: HTTP client pointing to user-service.
        phone: Phone number (e.g., +8613800138000 or 13800138000).
        jwt_token: User's JWT access token.

    Returns:
        Response dict with "message" field.

    Raises:
        httpx.HTTPStatusError: 401 invalid JWT, 409 phone taken, 429 rate limit.
    """
    normalized = normalize_phone(phone)
    resp = await client.post(
        PHONE_BIND_SEND_REST,
        json={"phone": normalized},
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    resp.raise_for_status()
    return resp.json()


async def bind_phone_verify(
    client: httpx.AsyncClient,
    phone: str,
    otp_code: str,
    jwt_token: str,
) -> dict[str, Any]:
    """Verify OTP and bind phone to existing account.

    Args:
        client: HTTP client pointing to user-service.
        phone: Phone number (same as sent to bind_phone_send_otp).
        otp_code: 6-digit OTP code.
        jwt_token: User's JWT access token.

    Returns:
        Response dict with "success" and "phone" fields.

    Raises:
        httpx.HTTPStatusError: 401 invalid JWT/OTP, 409 phone taken.
    """
    normalized = normalize_phone(phone)
    resp = await client.post(
        PHONE_BIND_VERIFY_REST,
        json={"phone": normalized, "code": _sanitize_otp(otp_code)},
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    resp.raise_for_status()
    return resp.json()


async def recover_handle(
    client: httpx.AsyncClient,
    config: SDKConfig,
    phone: str,
    otp_code: str,
    handle: str,
    *,
    services: list[dict[str, Any]] | None = None,
) -> tuple[DIDIdentity, dict[str, Any]]:
    """Recover a Handle by rebinding it to a newly generated DID."""
    normalized = normalize_phone(phone)

    identity = create_identity(
        hostname=config.did_domain,
        path_prefix=[handle],
        proof_purpose="authentication",
        domain=config.did_domain,
        services=services,
    )

    payload: dict[str, Any] = {
        "did_document": identity.did_document,
        "handle": handle,
        "phone": normalized,
        "otp_code": _sanitize_otp(otp_code),
    }
    recover_result = await rpc_call(client, DID_AUTH_RPC, "recover_handle", payload)

    identity.user_id = recover_result["user_id"]
    if recover_result.get("access_token"):
        identity.jwt_token = recover_result["access_token"]
    else:
        identity.jwt_token = await get_jwt_via_wba(client, identity, config.did_domain)

    return identity, recover_result


async def resolve_handle(
    client: httpx.AsyncClient,
    handle: str,
) -> dict[str, Any]:
    """Resolve a Handle to its DID mapping.

    Args:
        client: HTTP client pointing to user-service.
        handle: Handle local-part (e.g., "alice").

    Returns:
        Lookup result dict (contains handle, did, status, etc.).

    Raises:
        JsonRpcError: When lookup fails (e.g., handle not found).
    """
    return await rpc_call(client, HANDLE_RPC, "lookup", {"handle": handle})


async def lookup_handle(
    client: httpx.AsyncClient,
    did: str,
) -> dict[str, Any]:
    """Look up a Handle by DID.

    Args:
        client: HTTP client pointing to user-service.
        did: DID identifier.

    Returns:
        Lookup result dict (contains handle, did, status, etc.).

    Raises:
        JsonRpcError: When lookup fails (e.g., no handle for this DID).
    """
    return await rpc_call(client, HANDLE_RPC, "lookup", {"did": did})


__all__ = [
    "EmailVerificationResult",
    "normalize_phone",
    "send_otp",
    "register_handle",
    "register_handle_with_email",
    "send_email_verification",
    "check_email_verified",
    "ensure_email_verification",
    "wait_for_email_verification",
    "recover_handle",
    "resolve_handle",
    "lookup_handle",
    "bind_email_send",
    "bind_phone_send_otp",
    "bind_phone_verify",
]
