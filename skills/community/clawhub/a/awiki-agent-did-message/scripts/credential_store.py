"""Credential persistence: indexed multi-credential storage with per-credential directories.

[INPUT]: DIDIdentity object, DIDWbaAuthHeader (ANP SDK), SDKConfig (credentials_dir),
         credential_layout helpers
[OUTPUT]: save_identity(), load_identity(), list_identities(), delete_identity(),
         extract_auth_files(), create_authenticator()
[POS]: Core credential management module supporting cross-session identity reuse,
       indexed multi-credential storage, and DIDWbaAuthHeader factory

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from credential_layout import (
    get_index_entry,
    has_legacy_layout,
    legacy_layout_hint,
    list_legacy_credential_names,
    preferred_credential_dir_name,
    remove_index_entry,
    resolve_credential_paths,
    set_index_entry,
    write_secure_json,
    write_secure_text,
    ensure_credential_directory,
    build_credential_paths,
)
from utils.config import SDKConfig

logger = logging.getLogger(__name__)


def _coerce_text(value: bytes | str) -> str:
    """Normalize bytes/str content into a UTF-8 string."""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def _read_json_if_exists(path: Path) -> dict[str, Any] | None:
    """Read JSON content when the path exists."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text_if_exists(path: Path) -> str | None:
    """Read text content when the path exists."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _build_index_entry(
    credential_name: str,
    *,
    dir_name: str,
    did: str,
    unique_id: str,
    user_id: str | None,
    display_name: str | None,
    handle: str | None,
    created_at: str,
) -> dict[str, Any]:
    """Build a normalized credential index entry."""
    return {
        "credential_name": credential_name,
        "dir_name": dir_name,
        "did": did,
        "unique_id": unique_id,
        "user_id": user_id,
        "name": display_name,
        "handle": handle,
        "created_at": created_at,
        "is_default": credential_name == "default",
    }


def _validate_target_directory(
    credential_name: str,
    *,
    dir_name: str,
    did: str,
) -> None:
    """Ensure the target directory name is not already owned by another credential."""
    index_credentials = {
        name: entry
        for name, entry in list_identities_by_name().items()
        if name != credential_name
    }
    for existing_name, entry in index_credentials.items():
        if entry["dir_name"] == dir_name:
            if entry.get("did") == did:
                continue
            raise ValueError(
                f"Credential directory '{dir_name}' is already used by "
                f"credential '{existing_name}' ({entry.get('did')})"
            )

    paths = build_credential_paths(dir_name)
    if paths.credential_dir.exists() and any(paths.credential_dir.iterdir()):
        if any(
            entry.get("dir_name") == dir_name and entry.get("did") == did
            for entry in index_credentials.values()
        ):
            return
        raise ValueError(
            f"Credential directory '{dir_name}' already exists but is not indexed; "
            f"refusing to overwrite for DID {did}"
        )


def _credential_reference_count(dir_name: str) -> int:
    """Count how many credential names reference the same directory."""
    return sum(
        1
        for entry in list_identities_by_name().values()
        if entry.get("dir_name") == dir_name
    )


def prune_unreferenced_credential_dir(dir_name: str) -> bool:
    """Delete a credential directory when it is no longer referenced by the index."""
    if _credential_reference_count(dir_name) > 0:
        return False
    paths = build_credential_paths(dir_name)
    if not paths.credential_dir.exists():
        return False
    shutil.rmtree(paths.credential_dir)
    logger.info("Pruned unreferenced credential dir=%s", paths.credential_dir)
    return True


def list_identities_by_name() -> dict[str, dict[str, Any]]:
    """Return the raw credential index mapping."""
    from credential_layout import load_index

    return load_index()["credentials"]


def save_identity(
    did: str,
    unique_id: str,
    user_id: str | None,
    private_key_pem: bytes,
    public_key_pem: bytes,
    jwt_token: str | None = None,
    display_name: str | None = None,
    handle: str | None = None,
    name: str = "default",
    did_document: dict[str, Any] | None = None,
    e2ee_signing_private_pem: bytes | None = None,
    e2ee_agreement_private_pem: bytes | None = None,
    replace_existing: bool = False,
) -> Path:
    """Save a DID identity into the indexed multi-credential layout."""
    dir_name = preferred_credential_dir_name(handle=handle, unique_id=unique_id)
    existing_entry = get_index_entry(name)
    if existing_entry is not None:
        if existing_entry.get("did") != did:
            if not replace_existing:
                raise ValueError(
                    f"Credential '{name}' already exists for DID {existing_entry.get('did')}; "
                    f"refusing to overwrite with DID {did}"
                )
            _validate_target_directory(name, dir_name=dir_name, did=did)
        else:
            dir_name = existing_entry["dir_name"]
    else:
        _validate_target_directory(name, dir_name=dir_name, did=did)

    paths = build_credential_paths(dir_name)
    ensure_credential_directory(paths)

    existing_identity = _read_json_if_exists(paths.identity_path) or {}
    created_at = existing_identity.get("created_at") or datetime.now(timezone.utc).isoformat()

    identity_payload: dict[str, Any] = {
        "did": did,
        "unique_id": unique_id,
        "created_at": created_at,
    }
    if user_id is not None:
        identity_payload["user_id"] = user_id
    if display_name is not None:
        identity_payload["name"] = display_name
    if handle is not None:
        identity_payload["handle"] = handle

    write_secure_json(paths.identity_path, identity_payload)
    write_secure_json(paths.auth_path, {"jwt_token": jwt_token})
    if did_document is not None:
        write_secure_json(paths.did_document_path, did_document)

    write_secure_text(paths.key1_private_path, _coerce_text(private_key_pem))
    write_secure_text(paths.key1_public_path, _coerce_text(public_key_pem))
    if e2ee_signing_private_pem is not None:
        write_secure_text(
            paths.e2ee_signing_private_path,
            _coerce_text(e2ee_signing_private_pem),
        )
    if e2ee_agreement_private_pem is not None:
        write_secure_text(
            paths.e2ee_agreement_private_path,
            _coerce_text(e2ee_agreement_private_pem),
        )

    index_entry = _build_index_entry(
        name,
        dir_name=dir_name,
        did=did,
        unique_id=unique_id,
        user_id=user_id,
        display_name=display_name,
        handle=handle,
        created_at=created_at,
    )
    set_index_entry(name, index_entry)
    logger.info(
        "Saved credential name=%s did=%s handle=%s dir=%s",
        name,
        did,
        handle,
        paths.credential_dir,
    )
    return paths.identity_path


def load_identity(name: str = "default") -> dict[str, Any] | None:
    """Load a DID identity from the indexed multi-credential layout."""
    paths = resolve_credential_paths(name)
    if paths is None:
        if has_legacy_layout():
            logger.error("%s", legacy_layout_hint())
        return None

    identity_payload = _read_json_if_exists(paths.identity_path)
    if identity_payload is None or not identity_payload.get("did"):
        logger.warning("Credential metadata missing name=%s path=%s", name, paths.identity_path)
        return None

    auth_payload = _read_json_if_exists(paths.auth_path) or {}
    data: dict[str, Any] = {
        "did": identity_payload["did"],
        "unique_id": identity_payload.get("unique_id", ""),
        "user_id": identity_payload.get("user_id"),
        "created_at": identity_payload.get("created_at"),
    }
    if "name" in identity_payload:
        data["name"] = identity_payload["name"]
    if "handle" in identity_payload:
        data["handle"] = identity_payload["handle"]

    jwt_token = auth_payload.get("jwt_token")
    if jwt_token is not None:
        data["jwt_token"] = jwt_token

    did_document = _read_json_if_exists(paths.did_document_path)
    if did_document is not None:
        data["did_document"] = did_document

    private_key_pem = _read_text_if_exists(paths.key1_private_path)
    if private_key_pem is not None:
        data["private_key_pem"] = private_key_pem

    public_key_pem = _read_text_if_exists(paths.key1_public_path)
    if public_key_pem is not None:
        data["public_key_pem"] = public_key_pem

    e2ee_signing_private_pem = _read_text_if_exists(paths.e2ee_signing_private_path)
    if e2ee_signing_private_pem is not None:
        data["e2ee_signing_private_pem"] = e2ee_signing_private_pem

    e2ee_agreement_private_pem = _read_text_if_exists(paths.e2ee_agreement_private_path)
    if e2ee_agreement_private_pem is not None:
        data["e2ee_agreement_private_pem"] = e2ee_agreement_private_pem

    logger.debug("Loaded credential name=%s dir=%s", name, paths.credential_dir)
    return data


def list_identities() -> list[dict[str, Any]]:
    """List all saved identities from the credential index."""
    if has_legacy_layout() and not list_identities_by_name():
        logger.error("%s", legacy_layout_hint())
        return []

    identities = []
    for credential_name, entry in sorted(list_identities_by_name().items()):
        paths = resolve_credential_paths(credential_name)
        identities.append({
            "credential_name": credential_name,
            "did": entry.get("did", ""),
            "unique_id": entry.get("unique_id", ""),
            "name": entry.get("name", ""),
            "handle": entry.get("handle", ""),
            "user_id": entry.get("user_id", ""),
            "created_at": entry.get("created_at", ""),
            "is_default": bool(entry.get("is_default")),
            "dir_name": entry.get("dir_name", ""),
            "has_jwt": bool((_read_json_if_exists(paths.auth_path) or {}).get("jwt_token")) if paths is not None else False,
        })

    logger.debug("Listed %d credentials", len(identities))
    return identities


def delete_identity(name: str) -> bool:
    """Delete a saved identity and its credential directory."""
    paths = resolve_credential_paths(name)
    if paths is None:
        if has_legacy_layout():
            logger.error("%s", legacy_layout_hint())
        return False

    reference_count = _credential_reference_count(paths.dir_name)
    if paths.credential_dir.exists() and reference_count <= 1:
        shutil.rmtree(paths.credential_dir)
    removed = remove_index_entry(name)
    if removed:
        logger.info(
            "Deleted credential name=%s dir=%s shared_dir_references_before_delete=%d",
            name,
            paths.credential_dir,
            reference_count,
        )
    return removed


def backup_identity(name: str) -> Path | None:
    """Backup the current credential directory before destructive changes."""
    paths = resolve_credential_paths(name)
    if paths is None or not paths.credential_dir.exists():
        return None

    backup_root = (
        paths.root_dir
        / ".recovery-backup"
        / name
        / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_dir = backup_root / paths.dir_name
    shutil.copytree(paths.credential_dir, backup_dir)

    index_entry = get_index_entry(name) or {}
    write_secure_json(backup_root / "index_entry.json", index_entry)
    logger.info("Backed up credential name=%s backup_dir=%s", name, backup_root)
    return backup_root


def update_jwt(name: str, jwt_token: str) -> bool:
    """Update the JWT token of a saved identity."""
    paths = resolve_credential_paths(name)
    if paths is None:
        if has_legacy_layout():
            logger.error("%s", legacy_layout_hint())
        else:
            logger.warning("Cannot update JWT; credential not found name=%s", name)
        return False

    auth_payload = _read_json_if_exists(paths.auth_path) or {}
    auth_payload["jwt_token"] = jwt_token
    write_secure_json(paths.auth_path, auth_payload)
    logger.info("Updated JWT for credential name=%s dir=%s", name, paths.credential_dir)
    return True


def extract_auth_files(name: str = "default") -> tuple[Path, Path] | None:
    """Return credential DID document and key-1 private key paths for auth."""
    paths = resolve_credential_paths(name)
    if paths is None:
        if has_legacy_layout():
            logger.error("%s", legacy_layout_hint())
        return None

    if not paths.did_document_path.exists() or not paths.key1_private_path.exists():
        logger.debug(
            "Auth file extraction skipped name=%s has_did_document=%s has_private_key=%s",
            name,
            paths.did_document_path.exists(),
            paths.key1_private_path.exists(),
        )
        return None

    return (paths.did_document_path, paths.key1_private_path)


def create_authenticator(
    name: str = "default",
    config: Any = None,
) -> tuple[Any, dict[str, Any]] | None:
    """Create a DIDWbaAuthHeader instance from a saved credential."""
    from anp.authentication import DIDWbaAuthHeader

    data = load_identity(name)
    if data is None:
        logger.warning("Cannot create authenticator; credential not found name=%s", name)
        return None

    auth_files = extract_auth_files(name)
    if auth_files is None:
        logger.warning("Cannot create authenticator; auth files missing name=%s", name)
        return None

    did_doc_path, key_path = auth_files
    auth = DIDWbaAuthHeader(str(did_doc_path), str(key_path))

    if data.get("jwt_token") and config is not None:
        server_url = config.user_service_url
        auth.update_token(server_url, {"Authorization": f"Bearer {data['jwt_token']}"})
        if hasattr(config, "molt_message_url"):
            auth.update_token(
                config.molt_message_url,
                {"Authorization": f"Bearer {data['jwt_token']}"},
            )

    logger.debug("Created authenticator for credential name=%s did=%s", name, data.get("did"))
    return (auth, data)


__all__ = [
    "backup_identity",
    "create_authenticator",
    "delete_identity",
    "extract_auth_files",
    "list_identities",
    "load_identity",
    "prune_unreferenced_credential_dir",
    "save_identity",
    "update_jwt",
]
