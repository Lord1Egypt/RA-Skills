"""Handle-to-DID resolution via .well-known/handle endpoint.

[INPUT]: SDKConfig (user_service_url), httpx
[OUTPUT]: resolve_to_did()
[POS]: Identifier resolution utility, converts handle to DID via standard endpoint

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

import httpx

from utils.client import _resolve_verify
from utils.config import SDKConfig


async def resolve_to_did(
    identifier: str,
    config: SDKConfig | None = None,
) -> str:
    """Resolve a DID or handle to a DID.

    If identifier starts with "did:", return as-is.
    Otherwise treat as handle and call GET /user-service/.well-known/handle/{local_part}.

    Args:
        identifier: A DID string or a handle local-part (e.g. "alice").
        config: SDKConfig for service URL. Uses default if None.

    Returns:
        The resolved DID string.

    Raises:
        ValueError: If handle is not found or status is not "active".
    """
    if identifier.startswith("did:"):
        return identifier

    if config is None:
        config = SDKConfig()

    # Strip known awiki domain suffixes if present
    # (e.g., "alice.awiki.ai" -> "alice", "alice.awiki.test" -> "alice").
    strip_domains = {"awiki.ai", "awiki.test"}
    if config.did_domain:
        strip_domains.add(config.did_domain)
    for domain in strip_domains:
        if identifier.endswith(f".{domain}"):
            identifier = identifier[: -(len(domain) + 1)]
            break

    url = f"{config.user_service_url}/user-service/.well-known/handle/{identifier}"

    async with httpx.AsyncClient(
        timeout=10.0,
        trust_env=False,
        verify=_resolve_verify(config.user_service_url),
    ) as client:
        resp = await client.get(url)

    if resp.status_code == 404:
        raise ValueError(f"Handle '{identifier}' not found")
    resp.raise_for_status()

    data = resp.json()
    status = data.get("status", "")
    if status != "active":
        raise ValueError(f"Handle '{identifier}' is not active (status: {status})")

    did = data.get("did", "")
    if not did:
        raise ValueError(f"Handle '{identifier}' has no DID binding")

    return did


__all__ = ["resolve_to_did"]
