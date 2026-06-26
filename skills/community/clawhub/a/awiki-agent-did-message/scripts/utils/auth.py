"""Registration + DID document update + WBA authentication + JWT acquisition.

[INPUT]: httpx.AsyncClient, DIDIdentity, ANP auth functions, rpc_call(), services
[OUTPUT]: register_did(), update_did_document(), get_jwt_via_wba(),
          generate_wba_auth_header(), create_authenticated_identity()
[POS]: Wraps the complete DID authentication flow, all based on ANP, communicating with
       user-service via JSON-RPC 2.0.
       RPC paths use /user-service prefix (compatible with nginx reverse proxy and localhost direct connection)

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

from typing import Any

import httpx
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

from anp.authentication import generate_auth_header

from utils.config import SDKConfig
from utils.identity import DIDIdentity, create_identity
from utils.rpc import JsonRpcError, rpc_call


def _secp256k1_sign_callback(
    private_key: ec.EllipticCurvePrivateKey,
) -> callable:
    """Create a secp256k1 signing callback (adapts to ANP generate_auth_header interface).

    ANP generate_auth_header requires sign_callback(content: bytes, vm_fragment: str) -> bytes,
    returning DER-encoded signature.
    """

    def _callback(content: bytes, verification_method_fragment: str) -> bytes:
        return private_key.sign(content, ec.ECDSA(hashes.SHA256()))

    return _callback


def generate_wba_auth_header(
    identity: DIDIdentity,
    service_domain: str,
) -> str:
    """Generate DID WBA Authorization header.

    Args:
        identity: DID identity.
        service_domain: Target service domain.

    Returns:
        Authorization header value (DIDWba format).
    """
    private_key = identity.get_private_key()
    return generate_auth_header(
        did_document=identity.did_document,
        service_domain=service_domain,
        sign_callback=_secp256k1_sign_callback(private_key),
    )


async def register_did(
    client: httpx.AsyncClient,
    identity: DIDIdentity,
    name: str | None = None,
    is_public: bool = False,
    is_agent: bool = False,
    role: str | None = None,
    endpoint_url: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Register a DID identity.

    Sends identity.did_document directly (already contains ANP-generated authentication proof),
    calling user-service's did-auth.register method via JSON-RPC.

    Args:
        client: HTTP client pointing to user-service.
        identity: DID identity (did_document already contains authentication proof).
        name: Display name.
        is_public: Whether publicly visible.
        is_agent: Whether this is an AI Agent.
        role: Role.
        endpoint_url: Connection endpoint.
        description: Description.

    Returns:
        Registration response dict (contains did, user_id, message).

    Raises:
        JsonRpcError: When registration fails.
        httpx.HTTPStatusError: On HTTP layer errors.
    """
    payload: dict[str, Any] = {"did_document": identity.did_document}
    if name is not None:
        payload["name"] = name
    if is_public:
        payload["is_public"] = True
    if is_agent:
        payload["is_agent"] = True
    if role is not None:
        payload["role"] = role
    if endpoint_url is not None:
        payload["endpoint_url"] = endpoint_url
    if description is not None:
        payload["description"] = description

    return await rpc_call(client, "/user-service/did-auth/rpc", "register", payload)


async def update_did_document(
    client: httpx.AsyncClient,
    identity: DIDIdentity,
    domain: str,
    *,
    is_public: bool = False,
    is_agent: bool = False,
    role: str | None = None,
    endpoint_url: str | None = None,
) -> dict[str, Any]:
    """Update an existing DID document via DID WBA authentication.

    Args:
        client: HTTP client pointing to user-service.
        identity: DID identity with the updated did_document.
        domain: Service domain used for DID WBA authentication.
        is_public: Whether publicly visible.
        is_agent: Whether this is an AI Agent.
        role: Role.
        endpoint_url: Connection endpoint.

    Returns:
        Update response dict (contains did, user_id, message, optional access_token).

    Raises:
        JsonRpcError: When the server returns a JSON-RPC error.
        httpx.HTTPStatusError: On HTTP layer errors.
    """
    payload: dict[str, Any] = {"did_document": identity.did_document}
    if is_public:
        payload["is_public"] = True
    if is_agent:
        payload["is_agent"] = True
    if role is not None:
        payload["role"] = role
    if endpoint_url is not None:
        payload["endpoint_url"] = endpoint_url

    auth_header = generate_wba_auth_header(identity, domain)
    response = await client.post(
        "/user-service/did-auth/rpc",
        json={
            "jsonrpc": "2.0",
            "method": "update_document",
            "params": payload,
            "id": 1,
        },
        headers={"Authorization": auth_header},
    )
    response.raise_for_status()
    body = response.json()
    if body.get("error") is not None:
        error = body["error"]
        raise JsonRpcError(
            error["code"],
            error["message"],
            error.get("data"),
        )

    result = body["result"]
    auth_value = response.headers.get("authorization", "").strip()
    if auth_value.lower().startswith("bearer ") and not result.get("access_token"):
        result["access_token"] = auth_value.split(" ", 1)[1]
    return result


async def get_jwt_via_wba(
    client: httpx.AsyncClient,
    identity: DIDIdentity,
    domain: str,
) -> str:
    """Obtain JWT token via DID WBA signature.

    Args:
        client: HTTP client pointing to user-service.
        identity: DID identity.
        domain: Service domain.

    Returns:
        JWT access token string.
    """
    auth_header = generate_wba_auth_header(identity, domain)
    result = await rpc_call(
        client,
        "/user-service/did-auth/rpc",
        "verify",
        {"authorization": auth_header, "domain": domain},
    )
    return result["access_token"]


async def create_authenticated_identity(
    client: httpx.AsyncClient,
    config: SDKConfig,
    name: str | None = None,
    is_public: bool = False,
    is_agent: bool = False,
    role: str | None = None,
    endpoint_url: str | None = None,
    services: list[dict[str, Any]] | None = None,
) -> DIDIdentity:
    """One-stop creation of a complete DID identity (generate keys -> register -> obtain JWT).

    Uses key-bound DID: public key fingerprint automatically becomes the last segment
    of the DID path (k1_{fp}), no manual unique_id needed. path_prefix is fixed to
    ["user"] (required by the server).

    Args:
        client: HTTP client pointing to user-service.
        config: SDK configuration.
        name: Display name.
        is_public: Whether publicly visible.
        is_agent: Whether this is an AI Agent.
        role: Role.
        endpoint_url: Connection endpoint.
        services: Custom service entry list, written into DID document and covered by proof signing.

    Returns:
        DIDIdentity with user_id and jwt_token populated.
    """
    # 1. Create key-bound DID identity (with authentication proof, bound to service domain)
    #    path_prefix fixed to ["user"]: server requires DID format did:wba:{domain}:user:{id}
    identity = create_identity(
        hostname=config.did_domain,
        path_prefix=["user"],
        proof_purpose="authentication",
        domain=config.did_domain,
        services=services,
    )

    # 2. Register (send ANP-generated document directly)
    reg_result = await register_did(
        client,
        identity,
        name=name,
        is_public=is_public,
        is_agent=is_agent,
        role=role,
        endpoint_url=endpoint_url,
    )
    identity.user_id = reg_result["user_id"]

    # 3. Obtain JWT
    identity.jwt_token = await get_jwt_via_wba(client, identity, config.did_domain)

    return identity


__all__ = [
    "generate_wba_auth_header",
    "register_did",
    "update_did_document",
    "get_jwt_via_wba",
    "create_authenticated_identity",
]
