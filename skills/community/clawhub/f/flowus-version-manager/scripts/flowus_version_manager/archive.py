from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path

from . import SCHEMA_VERSION, __version__
from .common import Conflict, GateError, ManagerError, canonical, digest, file_hash, now, safe_relative, stable_id
from .manager import snapshot
from .store import TABLES
from .transport import MAX_FILE


def write_archive(output, manifest, blobs):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never overwrite an existing backup.
    with output.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", canonical({"manifest": manifest, "sha256": digest(manifest)}))
            for key, content in blobs.items():
                if hashlib.sha256(content).hexdigest() != key:
                    raise ManagerError("Backup blob hash mismatch")
                archive.writestr("blobs/" + key, content)


def read_archive(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or any(i.file_size > 128 * 1024 * 1024 for i in archive.infolist()):
            raise ManagerError("Invalid or oversized backup entries")
        envelope = json.loads(archive.read("manifest.json"))
        manifest = envelope["manifest"]
        if digest(manifest) != envelope["sha256"] or manifest.get("schema_version") != SCHEMA_VERSION:
            raise ManagerError("Backup manifest checksum or schema mismatch")
        blobs = {}
        for key in manifest["blob_hashes"]:
            if len(key) != 64 or any(c not in "0123456789abcdef" for c in key):
                raise ManagerError("Invalid blob key")
            content = archive.read("blobs/" + key)
            if hashlib.sha256(content).hexdigest() != key:
                raise ManagerError("Backup file checksum mismatch")
            blobs[key] = content
        return manifest, blobs


def cloud_backup(manager, output, *, dry_run=False):
    records = {table: [{"key": r.key, "id": r.id, "data": r.data} for r in manager.store.list(table)
                       if r.data.get("kind") != "probe"] for table in TABLES}
    if dry_run:
        return {"dry_run": True, "counts": {k: len(v) for k, v in records.items()}}
    before = digest(records)
    blobs = {}
    for version in records["versions"]:
        if version["data"].get("upload_state") != "verified":
            raise GateError("Unfinished uploads exist; reconcile them before creating a full backup")
        record = manager.store.get("versions", version["key"])
        content = manager.store.download(record)
        if hashlib.sha256(content).hexdigest() != record.data["sha256"]:
            raise ManagerError("Cloud backup hash mismatch")
        blobs[record.data["sha256"]] = content
    after = {table: [{"key": r.key, "id": r.id, "data": r.data} for r in manager.store.list(table)
                     if r.data.get("kind") != "probe"] for table in TABLES}
    if digest(after) != before:
        raise Conflict("Cloud changed during backup; retry to obtain a consistent snapshot")
    manifest = {"kind": "cloud", "schema_version": SCHEMA_VERSION, "tool_version": __version__,
                "vault_id": manager.config["vault_id"], "source_databases": manager.config["databases"],
                "created_at": now(), "records": records, "blob_hashes": sorted(blobs)}
    if manager.config.get("remote_profile"):
        from .profiles import export_profile
        manifest["shared_profile"] = export_profile(manager.config, manager.config["remote_profile"]["config_version"])
    write_archive(output, manifest, blobs)
    return {"backup": str(Path(output).resolve()), "files": len(records["versions"]), "sha256": file_hash(Path(output))}


def cloud_restore(manager, path, *, dry_run=False):
    manifest, blobs = read_archive(path)
    if manifest.get("kind") != "cloud":
        raise ManagerError("Use migrate for a local vault; restore accepts cloud backups")
    shared = manifest.get("shared_profile")
    if shared is not None:
        from .profiles import validate_profile
        if not isinstance(shared, dict) or not isinstance(shared.get("settings"), dict):
            raise GateError("Backup shared configuration is malformed")
        validate_profile(shared, shared["settings"].get("business_parent_id"))
        if shared["settings"]["vault_id"] != manifest["vault_id"] or shared["settings"]["databases"] != manifest["source_databases"]:
            raise GateError("Backup shared configuration does not match its source records")
    if set(manager.config["databases"].values()) & set(manifest["source_databases"].values()):
        raise GateError("Restore requires separate target databases; refusing to overwrite the source")
    restore_id = digest(manifest)
    for table in ("documents", "versions", "events", "proposals"):
        existing = manager.store.list(table)
        if any(r.data.get("kind") != "probe" and r.data.get("restore_id") != restore_id for r in existing):
            raise GateError("Restore target must be empty, or contain only this interrupted restore")
    if dry_run:
        return {"dry_run": True, "counts": {k: len(v) for k, v in manifest["records"].items()}}
    manager.guard()
    # Approval records are archived as evidence, never activated as new permissions in another vault.
    for version in manifest["records"]["versions"]:
        data = {**version["data"], "restore_id": restore_id}
        manager.stage_version(version["key"], data, blobs[data["sha256"]], "restore:" + restore_id)
    for table in ("documents", "events", "proposals"):
        for row in manifest["records"][table]:
            data = {**row["data"], "restore_id": restore_id}
            if table == "proposals":
                data.update(status="restored_evidence", approval_code="")
            manager.store.create(table, row["key"], data)
    for row in manifest["records"]["approvals"]:
        manager.event("restore:" + restore_id + ":" + row["key"], "historical_approval", row["data"])
    for table in ("documents", "events", "proposals"):
        for row in manifest["records"][table]:
            expected_data = {**row["data"], "restore_id": restore_id}
            if table == "proposals":
                expected_data.update(status="restored_evidence", approval_code="")
            actual = manager.store.get(table, row["key"])
            if not actual or actual.data != expected_data:
                raise Conflict("Restore target was edited; reconciliation stopped without overwriting it")
    verify = manager.latest()
    expected = sum(1 for r in manifest["records"]["documents"] if r["data"].get("status") == "active" and r["data"].get("latest"))
    if len(verify) != expected:
        raise ManagerError("Restore latest count mismatch")
    if shared is not None:
        # Only restore business rules. Target IDs, vault identity, governance and local
        # credential/capability bindings remain those of the independently verified destination.
        import copy
        manager.config["rules"] = copy.deepcopy(shared["settings"]["rules"])
        manager.config["pending_profile_publish"] = True
    return {"status": "restored", "versions": len(manifest["records"]["versions"]), "latest": len(verify),
            "shared_configuration": "rules restored; run layout to publish remapped target configuration" if shared else "legacy backup without shared profile",
            "approvals": "Archived as historical evidence; no active approvals imported"}


def read_local(vault):
    vault = Path(vault).resolve()
    path = vault / "Index" / "metadata.sqlite3"
    conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("BEGIN")
        files = [dict(r) for r in conn.execute("SELECT * FROM files ORDER BY series_key,version_sort,id")]
        notes = [dict(r) for r in conn.execute("SELECT * FROM notes ORDER BY id")]
        activity = [dict(r) for r in conn.execute("SELECT * FROM activity ORDER BY id")]
        text = {r["file_id"]: r["body"] for r in conn.execute("SELECT * FROM doc_text")}
    finally:
        conn.close()
    rules_path = vault / "Index" / "rules.json"
    rules = json.loads(rules_path.read_text()) if rules_path.exists() else {}
    blobs = {}
    for row in files:
        source = safe_relative(vault, row["stored_path"])
        if source.is_file() and source.stat().st_size > MAX_FILE:
            raise GateError("Local source exceeds the FlowUs API file limit; migration stopped before upload")
        if not source.is_file() or file_hash(source) != row["sha256"]:
            raise ManagerError("Local source hash mismatch or missing archive copy; migration stopped")
        content = source.read_bytes()
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise Conflict("Local source changed during migration preview")
        blobs[row["sha256"]] = content
    manifest = {"kind": "local", "schema_version": SCHEMA_VERSION, "files": files, "notes": notes,
                "activity": activity, "text": text, "rules": rules, "blob_hashes": sorted(blobs)}
    return manifest, blobs


def migrate(manager, vault, output=None, *, dry_run=False):
    manifest, blobs = read_local(vault)
    source_id = digest(manifest)
    files = manifest["files"]
    summary = {"files": len(files), "series": len({r["series_key"] for r in files}),
               "latest": sum(r["is_latest"] for r in files), "notes": len(manifest["notes"]),
               "activity": len(manifest["activity"]), "bytes": sum(r["size"] for r in files)}
    if dry_run:
        return {"dry_run": True, "summary": summary, "source_id": source_id,
                "files": [{k: r[k] for k in ("id", "original_name", "source_path", "sha256", "series_key", "is_latest")} for r in files]}
    manager.guard()
    if not output:
        raise ManagerError("migrate requires --backup with a new private backup path")
    if Path(output).exists():
        backup_manifest, _ = read_archive(output)
        if digest(backup_manifest) != source_id:
            raise Conflict("Existing backup belongs to a different source snapshot")
    else:
        write_archive(output, manifest, blobs)
    for table in ("documents", "versions"):
        if any(r.data.get("kind") != "probe" and r.data.get("migration_id") != source_id for r in manager.store.list(table)):
            raise GateError("Migration needs empty target databases or the same interrupted migration")
    version_map, documents = {}, {}
    for row in files:
        doc_key = digest({"legacy_series": row["series_key"]})
        version_key = "legacy:" + row["id"]
        raw_meta = json.loads(row["metadata_json"])
        data = {**raw_meta, "title": row["original_name"], "original_name": row["original_name"],
                "series_key": row["series_key"], "series_title": row["series_title"],
                "document_key": doc_key, "category": row["category"], "version_label": row["version_label"],
                "version_sort": row["version_sort"], "sha256": row["sha256"], "size": row["size"],
                "source": row["source_path"], "status": row["status"], "is_final": bool(row["is_final"]),
                "reason": row.get("reason"), "text": manifest["text"].get(row["id"], "")[:24000],
                "migration_id": source_id, "legacy_record": row, "added_at": row["added_at"]}
        manager.stage_version(version_key, data, blobs[row["sha256"]], "migration:" + source_id)
        version_map[row["id"]] = version_key
        doc = documents.setdefault(doc_key, {"title": row["series_title"], "series_key": row["series_key"],
            "category": row["category"], "latest": "", "locked": False, "status": "active", "migration_id": source_id})
        if row["is_latest"]:
            if doc["latest"]:
                raise Conflict("Source has multiple latest versions in one series")
            doc.update(latest=version_key, locked=bool(row["locked"]))
    for key, data in documents.items():
        manager.store.create("documents", key, manager.stamped(data))
    for kind in ("notes", "activity"):
        for row in manifest[kind]:
            manager.event("migration:" + source_id + ":" + kind + ":" + str(row["id"]),
                          "legacy_" + kind, {"legacy": row, "version_key": version_map.get(row.get("file_id"))})
    actual = [r for r in manager.store.list("versions") if r.data.get("migration_id") == source_id]
    actual_docs = [r for r in manager.store.list("documents") if r.data.get("migration_id") == source_id]
    if len(actual) != summary["files"] or len(actual_docs) != summary["series"] or len(manager.latest()) != summary["latest"]:
        raise ManagerError("Migration reconciliation failed")
    for key, expected in documents.items():
        actual_doc = manager.store.get("documents", key)
        if any(actual_doc.data.get(field) != value for field, value in expected.items()):
            raise Conflict("Migrated directory changed; reconciliation stopped")
    for kind in ("notes", "activity"):
        for row in manifest[kind]:
            event = manager.store.get("events", "migration:" + source_id + ":" + kind + ":" + str(row["id"]) + ":legacy_" + kind)
            if not event or event.data.get("details", {}).get("legacy") != row:
                raise ManagerError("Historical notes/activity reconciliation failed")
    for row in actual:
        if hashlib.sha256(manager.store.download(row)).hexdigest() != row.data["sha256"]:
            raise ManagerError("Post-migration file verification failed")
    manager.event("migration:" + source_id, "migration_completed", summary)
    return {"status": "migrated", "summary": summary, "source_id": source_id, "backup": str(Path(output).resolve()),
            "local_originals": "preserved"}
