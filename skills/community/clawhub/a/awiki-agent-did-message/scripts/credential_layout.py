"""Credential storage layout helpers for multi-credential support.

[INPUT]: SDKConfig (credentials_dir), credential metadata, credential names
[OUTPUT]: CredentialPaths, index/legacy path helpers, validated legacy-layout
          detection helpers
[POS]: Shared storage layout module used by credential_store, e2ee_store, and
       credential migration logic to manage indexed per-credential directories

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import logging
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils.config import SDKConfig

logger = logging.getLogger(__name__)

INDEX_SCHEMA_VERSION = 3
INDEX_FILE_NAME = "index.json"
LEGACY_BACKUP_DIR_NAME = ".legacy-backup"
IDENTITY_FILE_NAME = "identity.json"
AUTH_FILE_NAME = "auth.json"
DID_DOCUMENT_FILE_NAME = "did_document.json"
KEY1_PRIVATE_FILE_NAME = "key-1-private.pem"
KEY1_PUBLIC_FILE_NAME = "key-1-public.pem"
E2EE_SIGNING_PRIVATE_FILE_NAME = "e2ee-signing-private.pem"
E2EE_AGREEMENT_PRIVATE_FILE_NAME = "e2ee-agreement-private.pem"
E2EE_STATE_FILE_NAME = "e2ee-state.json"

_SAFE_PATH_COMPONENT = re.compile(r"[^A-Za-z0-9._-]+")
_LEGACY_E2EE_PREFIX = "e2ee_"

LEGACY_LAYOUT_HINT = (
    "Legacy credential layout detected. Run "
    "'uv run python scripts/check_status.py' once to migrate credentials."
)


@dataclass(frozen=True, slots=True)
class CredentialPaths:
    """Resolved paths for a single credential directory."""

    root_dir: Path
    dir_name: str
    credential_dir: Path
    identity_path: Path
    auth_path: Path
    did_document_path: Path
    key1_private_path: Path
    key1_public_path: Path
    e2ee_signing_private_path: Path
    e2ee_agreement_private_path: Path
    e2ee_state_path: Path


def _get_credentials_root(config: SDKConfig | None = None) -> Path:
    """Return the credential storage root directory."""
    resolved_config = config or SDKConfig()
    return resolved_config.credentials_dir


def ensure_credentials_root(config: SDKConfig | None = None) -> Path:
    """Create the credential storage root directory with secure permissions."""
    root_dir = _get_credentials_root(config)
    root_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(root_dir, stat.S_IRWXU)
    return root_dir


def index_path(config: SDKConfig | None = None) -> Path:
    """Return the credential index file path."""
    return ensure_credentials_root(config) / INDEX_FILE_NAME


def legacy_backup_root(config: SDKConfig | None = None) -> Path:
    """Return the legacy backup directory path."""
    return ensure_credentials_root(config) / LEGACY_BACKUP_DIR_NAME


def _default_index() -> dict[str, Any]:
    """Return an empty credential index payload."""
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "default_credential_name": None,
        "credentials": {},
    }


def _normalize_index_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize older index payloads into the current schema shape."""
    credentials = data.get("credentials")
    if not isinstance(credentials, dict):
        raise ValueError("Credential index 'credentials' must be a dict")

    default_credential_name = data.get("default_credential_name")
    if default_credential_name is None and "default" in credentials:
        default_credential_name = "default"

    normalized_credentials: dict[str, Any] = {}
    for credential_name, entry in credentials.items():
        if not isinstance(entry, dict):
            raise ValueError(f"Credential index entry must be a dict: {credential_name}")
        normalized_entry = dict(entry)
        normalized_entry["credential_name"] = credential_name
        normalized_entry["is_default"] = credential_name == default_credential_name
        normalized_credentials[credential_name] = normalized_entry

    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "default_credential_name": default_credential_name,
        "credentials": normalized_credentials,
    }


def load_index(config: SDKConfig | None = None) -> dict[str, Any]:
    """Load the credential index, or return an empty default index."""
    path = index_path(config)
    if not path.exists():
        return _default_index()

    data = json.loads(path.read_text(encoding="utf-8"))
    schema_version = data.get("schema_version")
    if schema_version not in (2, 3):
        raise ValueError(
            f"Unsupported credential index schema: {schema_version}"
        )
    return _normalize_index_payload(data)


def save_index(index: dict[str, Any], config: SDKConfig | None = None) -> Path:
    """Persist the credential index with secure permissions."""
    payload = _normalize_index_payload(dict(index))
    path = index_path(config)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    logger.debug("Saved credential index path=%s entries=%d", path, len(payload["credentials"]))
    return path


def get_index_entry(
    credential_name: str,
    config: SDKConfig | None = None,
) -> dict[str, Any] | None:
    """Return the index entry for a credential name.

    When callers request the argparse default credential name ``"default"``,
    first honor a literal ``"default"`` entry if one exists. Otherwise, fall
    back to the configured ``default_credential_name`` stored in the index so
    all scripts consistently resolve the user-selected default credential.
    """
    index = load_index(config)
    entry = index["credentials"].get(credential_name)
    if entry is None and credential_name == "default":
        fallback_name = index.get("default_credential_name")
        if fallback_name and fallback_name != "default":
            entry = index["credentials"].get(fallback_name)
    return entry


def set_index_entry(
    credential_name: str,
    entry: dict[str, Any],
    config: SDKConfig | None = None,
) -> Path:
    """Upsert a credential index entry."""
    index = load_index(config)
    index["credentials"][credential_name] = entry
    if entry.get("is_default"):
        index["default_credential_name"] = credential_name
    elif index.get("default_credential_name") == credential_name:
        index["default_credential_name"] = None
    return save_index(index, config)


def remove_index_entry(
    credential_name: str,
    config: SDKConfig | None = None,
) -> bool:
    """Remove a credential index entry if it exists."""
    index = load_index(config)
    if credential_name not in index["credentials"]:
        return False
    del index["credentials"][credential_name]
    if index.get("default_credential_name") == credential_name:
        index["default_credential_name"] = None
    save_index(index, config)
    return True


def sanitize_credential_dir_name(raw_value: str) -> str:
    """Convert a preferred directory label into a safe filesystem name."""
    sanitized = _SAFE_PATH_COMPONENT.sub("_", raw_value).strip("._-")
    if not sanitized:
        raise ValueError(f"Unable to derive a safe credential directory name from: {raw_value!r}")
    return sanitized


def preferred_credential_dir_name(
    *,
    handle: str | None,
    unique_id: str,
) -> str:
    """Select the preferred credential directory name.

    The credential directory name is always derived from the DID unique_id so
    it remains stable even if the Handle changes or is removed later.
    """
    if not unique_id:
        raise ValueError("Credential directory name requires unique_id")
    return sanitize_credential_dir_name(unique_id)


def build_credential_paths(
    dir_name: str,
    config: SDKConfig | None = None,
) -> CredentialPaths:
    """Build all storage paths for a credential directory name."""
    root_dir = ensure_credentials_root(config)
    credential_dir = root_dir / dir_name
    return CredentialPaths(
        root_dir=root_dir,
        dir_name=dir_name,
        credential_dir=credential_dir,
        identity_path=credential_dir / IDENTITY_FILE_NAME,
        auth_path=credential_dir / AUTH_FILE_NAME,
        did_document_path=credential_dir / DID_DOCUMENT_FILE_NAME,
        key1_private_path=credential_dir / KEY1_PRIVATE_FILE_NAME,
        key1_public_path=credential_dir / KEY1_PUBLIC_FILE_NAME,
        e2ee_signing_private_path=credential_dir / E2EE_SIGNING_PRIVATE_FILE_NAME,
        e2ee_agreement_private_path=credential_dir / E2EE_AGREEMENT_PRIVATE_FILE_NAME,
        e2ee_state_path=credential_dir / E2EE_STATE_FILE_NAME,
    )


def resolve_credential_paths(
    credential_name: str,
    config: SDKConfig | None = None,
) -> CredentialPaths | None:
    """Resolve credential paths from the top-level index."""
    entry = get_index_entry(credential_name, config)
    if entry is None:
        return None
    return build_credential_paths(entry["dir_name"], config)


def ensure_credential_directory(paths: CredentialPaths) -> Path:
    """Create a credential directory with secure permissions."""
    paths.credential_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(paths.credential_dir, stat.S_IRWXU)
    return paths.credential_dir


def write_secure_text(path: Path, content: str) -> None:
    """Write a text file with 600 permissions."""
    path.write_text(content, encoding="utf-8")
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def write_secure_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON with 600 permissions."""
    write_secure_text(path, json.dumps(payload, indent=2, ensure_ascii=False))


def write_secure_bytes(path: Path, content: bytes) -> None:
    """Write a binary file with 600 permissions."""
    path.write_bytes(content)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def legacy_identity_path(
    credential_name: str,
    config: SDKConfig | None = None,
) -> Path:
    """Return the legacy credential JSON path."""
    return ensure_credentials_root(config) / f"{credential_name}.json"


def legacy_e2ee_state_path(
    credential_name: str,
    config: SDKConfig | None = None,
) -> Path:
    """Return the legacy E2EE state JSON path."""
    return ensure_credentials_root(config) / f"{_LEGACY_E2EE_PREFIX}{credential_name}.json"


def legacy_auth_export_paths(
    credential_name: str,
    config: SDKConfig | None = None,
) -> tuple[Path, Path]:
    """Return the legacy extracted DID document/private key paths."""
    root_dir = ensure_credentials_root(config)
    return (
        root_dir / f"{credential_name}_did_document.json",
        root_dir / f"{credential_name}_private_key.pem",
    )


def _is_legacy_identity_payload(payload: Any) -> bool:
    """Return whether a JSON payload matches the legacy credential shape."""
    if not isinstance(payload, dict):
        return False
    did = payload.get("did")
    private_key_pem = payload.get("private_key_pem")
    return isinstance(did, str) and bool(did) and isinstance(private_key_pem, str) and bool(private_key_pem)


def scan_legacy_layout(config: SDKConfig | None = None) -> dict[str, Any]:
    """Scan the root credential directory for legacy flat-file artifacts.

    A file counts as a migratable legacy credential only when its JSON payload
    matches the expected credential shape (at minimum: ``did`` and
    ``private_key_pem``). Standalone ``e2ee_<name>.json`` files are reported as
    orphan E2EE files unless a valid ``<name>.json`` credential exists.
    """
    root_dir = ensure_credentials_root(config)
    valid_credentials: dict[str, dict[str, Any]] = {}
    invalid_json_files: list[dict[str, str]] = []
    e2ee_candidates: dict[str, Path] = {}

    for path in sorted(root_dir.glob("*.json")):
        if path.name == INDEX_FILE_NAME:
            continue
        if path.name.endswith("_did_document.json"):
            continue
        if path.name.startswith(_LEGACY_E2EE_PREFIX):
            e2ee_candidates[path.stem[len(_LEGACY_E2EE_PREFIX):]] = path
            continue

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            invalid_json_files.append({
                "file": path.name,
                "reason": f"invalid_json: {exc}",
            })
            continue

        if not _is_legacy_identity_payload(payload):
            invalid_json_files.append({
                "file": path.name,
                "reason": "not_a_legacy_credential_payload",
            })
            continue

        valid_credentials[path.stem] = {
            "credential_name": path.stem,
            "path": str(path),
            "did": payload["did"],
            "unique_id": payload.get("unique_id") or payload["did"].rsplit(":", 1)[-1],
            "handle": payload.get("handle"),
        }

    orphan_e2ee_files = [
        {
            "credential_name": credential_name,
            "file": path.name,
        }
        for credential_name, path in sorted(e2ee_candidates.items())
        if credential_name not in valid_credentials
    ]

    unique_dids = sorted({
        entry["did"]
        for entry in valid_credentials.values()
        if entry.get("did")
    })

    return {
        "legacy_credentials": sorted(valid_credentials),
        "valid_credentials": valid_credentials,
        "invalid_json_files": invalid_json_files,
        "orphan_e2ee_files": orphan_e2ee_files,
        "unique_dids": unique_dids,
        "unique_did_count": len(unique_dids),
    }


def list_legacy_credential_names(config: SDKConfig | None = None) -> list[str]:
    """List validated legacy credential names still using the flat-file layout."""
    return scan_legacy_layout(config)["legacy_credentials"]


def has_legacy_layout(config: SDKConfig | None = None) -> bool:
    """Return whether any legacy flat-file artifacts remain."""
    scan_result = scan_legacy_layout(config)
    return bool(
        scan_result["legacy_credentials"]
        or scan_result["invalid_json_files"]
        or scan_result["orphan_e2ee_files"]
    )


def legacy_layout_hint() -> str:
    """Return the standard legacy-layout migration hint."""
    return LEGACY_LAYOUT_HINT


__all__ = [
    "AUTH_FILE_NAME",
    "CredentialPaths",
    "DID_DOCUMENT_FILE_NAME",
    "E2EE_AGREEMENT_PRIVATE_FILE_NAME",
    "E2EE_SIGNING_PRIVATE_FILE_NAME",
    "E2EE_STATE_FILE_NAME",
    "IDENTITY_FILE_NAME",
    "INDEX_FILE_NAME",
    "INDEX_SCHEMA_VERSION",
    "KEY1_PRIVATE_FILE_NAME",
    "KEY1_PUBLIC_FILE_NAME",
    "build_credential_paths",
    "ensure_credential_directory",
    "ensure_credentials_root",
    "get_index_entry",
    "has_legacy_layout",
    "index_path",
    "legacy_auth_export_paths",
    "legacy_backup_root",
    "legacy_e2ee_state_path",
    "legacy_identity_path",
    "legacy_layout_hint",
    "list_legacy_credential_names",
    "load_index",
    "preferred_credential_dir_name",
    "remove_index_entry",
    "resolve_credential_paths",
    "sanitize_credential_dir_name",
    "scan_legacy_layout",
    "save_index",
    "set_index_entry",
    "write_secure_bytes",
    "write_secure_json",
    "write_secure_text",
]
