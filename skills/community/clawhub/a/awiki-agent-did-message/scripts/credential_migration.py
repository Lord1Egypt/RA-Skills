"""Legacy credential migration into the indexed per-credential directory layout.

[INPUT]: Legacy flat credential JSON files, legacy E2EE state files,
         credential_layout validated scan helpers, credential_store, e2ee_store
[OUTPUT]: detect_legacy_layout(), migrate_legacy_credentials(),
          ensure_credential_storage_ready()
[POS]: Shared migration module used by check_status.py and the standalone
       migrate_credentials.py CLI

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
    legacy_auth_export_paths,
    legacy_backup_root,
    legacy_e2ee_state_path,
    legacy_identity_path,
    resolve_credential_paths,
    scan_legacy_layout,
)
from credential_store import save_identity
from e2ee_store import save_e2ee_state

logger = logging.getLogger(__name__)


def detect_legacy_layout() -> dict[str, Any]:
    """Inspect whether legacy credential files still exist."""
    scan_result = scan_legacy_layout()
    legacy_credentials = scan_result["legacy_credentials"]
    return {
        "status": (
            "legacy"
            if legacy_credentials
            else "legacy_issues"
            if scan_result["invalid_json_files"] or scan_result["orphan_e2ee_files"]
            else "new"
        ),
        "legacy_credentials": legacy_credentials,
        "unique_dids": scan_result["unique_dids"],
        "unique_did_count": scan_result["unique_did_count"],
        "invalid_json_files": scan_result["invalid_json_files"],
        "orphan_e2ee_files": scan_result["orphan_e2ee_files"],
    }


def _read_json(path: Path) -> dict[str, Any]:
    """Load JSON content from a path."""
    return json.loads(path.read_text(encoding="utf-8"))


def _backup_legacy_files(credential_name: str, run_id: str) -> Path:
    """Move legacy files into a timestamped backup directory."""
    backup_dir = legacy_backup_root() / run_id / credential_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    paths_to_archive = [
        legacy_identity_path(credential_name),
        legacy_e2ee_state_path(credential_name),
        *legacy_auth_export_paths(credential_name),
    ]

    for path in paths_to_archive:
        if not path.exists():
            continue
        shutil.move(str(path), str(backup_dir / path.name))

    logger.info(
        "Archived legacy credential artifacts credential=%s backup_dir=%s",
        credential_name,
        backup_dir,
    )
    return backup_dir


def _migrate_single_credential(
    credential_name: str,
    run_id: str,
) -> dict[str, Any]:
    """Migrate one legacy credential into the new layout."""
    legacy_path = legacy_identity_path(credential_name)
    if not legacy_path.exists():
        raise FileNotFoundError(
            f"Legacy credential file not found for '{credential_name}'"
        )

    legacy_data = _read_json(legacy_path)
    did = legacy_data["did"]
    unique_id = legacy_data.get("unique_id") or did.rsplit(":", 1)[-1]

    save_identity(
        did=did,
        unique_id=unique_id,
        user_id=legacy_data.get("user_id"),
        private_key_pem=legacy_data["private_key_pem"],
        public_key_pem=legacy_data.get("public_key_pem", ""),
        jwt_token=legacy_data.get("jwt_token"),
        display_name=legacy_data.get("name"),
        handle=legacy_data.get("handle"),
        name=credential_name,
        did_document=legacy_data.get("did_document"),
        e2ee_signing_private_pem=legacy_data.get("e2ee_signing_private_pem"),
        e2ee_agreement_private_pem=legacy_data.get("e2ee_agreement_private_pem"),
    )

    legacy_e2ee_path = legacy_e2ee_state_path(credential_name)
    if legacy_e2ee_path.exists():
        save_e2ee_state(_read_json(legacy_e2ee_path), credential_name)

    backup_dir = _backup_legacy_files(credential_name, run_id)
    resolved_paths = resolve_credential_paths(credential_name)
    return {
        "credential_name": credential_name,
        "did": did,
        "dir_name": resolved_paths.dir_name if resolved_paths else None,
        "backup_dir": str(backup_dir),
    }


def migrate_legacy_credentials(
    credential_name: str | None = None,
) -> dict[str, Any]:
    """Migrate legacy flat-file credentials into the new indexed layout."""
    scan_result = scan_legacy_layout()
    legacy_credentials = scan_result["legacy_credentials"]
    if credential_name is not None:
        legacy_credentials = [
            candidate for candidate in legacy_credentials
            if candidate == credential_name
        ]

    if not legacy_credentials:
        return {
            "status": "not_needed",
            "legacy_credentials": legacy_credentials,
            "unique_dids": scan_result["unique_dids"],
            "unique_did_count": scan_result["unique_did_count"],
            "migrated": [],
            "skipped": [],
            "conflicts": [],
            "errors": [],
            "invalid_json_files": scan_result["invalid_json_files"],
            "orphan_e2ee_files": scan_result["orphan_e2ee_files"],
        }

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    migrated: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for legacy_name in legacy_credentials:
        try:
            existing_entry = get_index_entry(legacy_name)
            legacy_path = legacy_identity_path(legacy_name)
            if existing_entry is not None and not legacy_path.exists():
                skipped.append({
                    "credential_name": legacy_name,
                    "reason": "already_migrated",
                })
                continue

            migrated.append(_migrate_single_credential(legacy_name, run_id))
        except ValueError as exc:
            conflicts.append({
                "credential_name": legacy_name,
                "reason": str(exc),
            })
            logger.warning("Credential migration conflict credential=%s error=%s", legacy_name, exc)
        except Exception as exc:  # pragma: no cover - defensive guard
            errors.append({
                "credential_name": legacy_name,
                "reason": str(exc),
            })
            logger.exception("Credential migration failed credential=%s", legacy_name)

    if conflicts or errors:
        status = "partial" if migrated else "error"
    else:
        status = "migrated"

    return {
        "status": status,
        "legacy_credentials": legacy_credentials,
        "unique_dids": scan_result["unique_dids"],
        "unique_did_count": scan_result["unique_did_count"],
        "migrated": migrated,
        "skipped": skipped,
        "conflicts": conflicts,
        "errors": errors,
        "invalid_json_files": scan_result["invalid_json_files"],
        "orphan_e2ee_files": scan_result["orphan_e2ee_files"],
    }


def ensure_credential_storage_ready(
    credential_name: str | None = None,
) -> dict[str, Any]:
    """Ensure the credential storage layout is ready for runtime use."""
    detection = detect_legacy_layout()
    if detection["status"] == "new":
        return {
            "status": "ready",
            "layout": "new",
            "credential_ready": True,
            "migration": None,
        }

    migration = migrate_legacy_credentials()
    target_in_legacy = (
        credential_name is not None
        and credential_name in detection["legacy_credentials"]
    )
    credential_ready = (
        not target_in_legacy
        or get_index_entry(credential_name) is not None
    )
    return {
        "status": migration["status"],
        "layout": "new" if not has_legacy_layout() else "legacy_remaining",
        "credential_ready": credential_ready,
        "migration": migration,
    }


__all__ = [
    "detect_legacy_layout",
    "ensure_credential_storage_ready",
    "migrate_legacy_credentials",
]
