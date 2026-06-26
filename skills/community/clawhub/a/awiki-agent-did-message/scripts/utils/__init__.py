"""awiki-sdk: General SDK for DID identity creation, DID document updates,
WBA authentication, JWT acquisition, Handle registration, WebSocket client,
and shared runtime logging configuration.

[INPUT]: ANP library
[OUTPUT]: Public API (DIDIdentity, create_identity, register_did,
          update_did_document, register_handle, WsClient, configure_logging, ...)
[POS]: Package entry point, centralizes export of all public interfaces

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

# Core types
from utils.config import SDKConfig
from utils.identity import DIDIdentity, create_identity, load_private_key
from utils.auth import (
    generate_wba_auth_header,
    register_did,
    update_did_document,
    get_jwt_via_wba,
    create_authenticated_identity,
)
from utils.client import create_user_service_client, create_molt_message_client
from utils.e2ee import E2eeClient
from utils.rpc import JsonRpcError, rpc_call, authenticated_rpc_call
from utils.handle import (
    send_otp,
    register_handle,
    recover_handle,
    resolve_handle,
    lookup_handle,
    normalize_phone,
)
from utils.logging_config import (
    cleanup_log_files,
    configure_logging,
    find_latest_log_file,
    get_log_dir,
    get_log_file_path,
)
from utils.ws import WsClient
from utils.resolve import resolve_to_did

__all__ = [
    # config
    "SDKConfig",
    # identity
    "DIDIdentity",
    "create_identity",
    "load_private_key",
    # auth
    "generate_wba_auth_header",
    "register_did",
    "update_did_document",
    "get_jwt_via_wba",
    "create_authenticated_identity",
    # client
    "create_user_service_client",
    "create_molt_message_client",
    # e2ee
    "E2eeClient",
    # rpc
    "JsonRpcError",
    "rpc_call",
    "authenticated_rpc_call",
    # handle
    "send_otp",
    "register_handle",
    "recover_handle",
    "resolve_handle",
    "lookup_handle",
    "normalize_phone",
    # logging
    "cleanup_log_files",
    "configure_logging",
    "find_latest_log_file",
    "get_log_dir",
    "get_log_file_path",
    # ws
    "WsClient",
    # resolve
    "resolve_to_did",
]
