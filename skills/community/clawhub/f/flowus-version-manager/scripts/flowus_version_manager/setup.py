from __future__ import annotations

import hashlib
import os
import uuid

from . import SCHEMA_VERSION, __version__
from .common import APIError, Conflict, GateError, ManagerError, NetworkError, atomic_json, digest, now, governance_mode, network_mode, transport_mode, stable_id, credential_names, credential_value
from .manager import binding
from .store import FIELDS, TABLES, properties, rich, schema
from .transport import HTTP


def provision(config, path, writer, setup=None):
    business = config.get("business_parent_id")
    approval = config.get("approval_parent_id")
    trusted = governance_mode(config) == "trusted_client"
    if not business:
        raise GateError("Configure the business root page")
    if not trusted and (not approval or business == approval):
        raise GateError("Configure two distinct root pages, with no shared write-authorized ancestor")
    owner = (setup or writer) if trusted else (setup or HTTP(os.environ.get("FLOWUS_SETUP_TOKEN", ""), network_mode=network_mode(config)))
    config.setdefault("databases", {})
    for table, title in TABLES.items():
        if table in config["databases"]:
            continue
        client = owner if table == "approvals" else writer
        parent = approval if table == "approvals" and not trusted else business
        # Fail closed after an ambiguous database POST. The owner can adopt the created ID in config.
        response, _ = client.request("POST", "/databases", {
            "parent": {"page_id": parent}, "title": rich(title), "properties": schema()})
        config["databases"][table] = response["id"]
        atomic_json(path, config)
    if not trusted and not config.get("approval_probe_id"):
        response, _ = owner.request("POST", "/pages", {
            "parent": {"database_id": config["databases"]["approvals"]},
            "properties": properties("permission-probe", {"title": "权限验证专用记录（勿审批）", "decision": "Pending"})},
            idempotency=str(uuid.uuid5(uuid.UUID(config["vault_id"]), "approval-probe")))
        config["approval_probe_id"] = response["id"]
        atomic_json(path, config)
    if not config.get("inbox_page_id"):
        response, _ = writer.request("POST", "/pages", {
            "parent": {"page_id": business}, "properties": {"title": {"type": "title", "title": rich("文件收件区")}}},
            idempotency=str(uuid.uuid5(uuid.UUID(config["vault_id"]), "inbox")))
        config["inbox_page_id"] = response["id"]
        atomic_json(path, config)
    from .views import provision_views
    provision_views(config, path, writer)
    return {"status": "provisioned", "databases": config["databases"],
            "governance_mode": governance_mode(config),
            "next": ("Run doctor --verify-writes; human changes use apply-confirmed" if trusted else
                     "Revoke setup credential; grant approval-reader read access only, then run doctor --verify-writes")}


def error_details(error):
    details = {"error": error.code, "message": str(error)}
    if isinstance(error, APIError):
        details["http_status"] = error.status
    if isinstance(error, NetworkError):
        details.update(kind=error.kind, network_mode=error.network_mode, operation=error.operation)
    return details


def download_preflight(store, config, block_id, expected_sha256):
    """GET-only technical gate, usable before any business database exists."""
    uuid.UUID(block_id)
    expected_sha256 = expected_sha256.lower()
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in expected_sha256):
        raise ManagerError("Expected SHA-256 must be 64 hexadecimal characters")
    names = ("api_access", "public_contract", "attachment_metadata", "download_url",
             "storage_network", "file_integrity", "idempotent_create", "optimistic_lock")
    checks = {name: {"status": "not_run"} for name in names}
    report = {"read_only": True, "writes_enabled": False, "network_mode": network_mode(config),
              "block_id": block_id, "checks": checks,
              "full_capability_verification": "Requires doctor --verify-writes after provisioning"}
    stage = "api_access"
    try:
        checks[stage]["status"] = "running"
        identity, _ = store.writer.request("GET", "/users/me")
        if not identity.get("id"):
            raise GateError("FlowUs identity is missing")
        checks[stage] = {"status": "passed"}
        stage = "public_contract"
        checks[stage]["status"] = "running"
        spec, _ = store.writer.request("GET", "/openapi.json")
        store._download_spec = spec
        paths = spec.get("paths", {})
        report["public_api"] = {"path_count": len(paths),
            "contract_source": spec.get("x-contract-source", "public_openapi"),
            "download_route_declared": "get" in paths.get("/v2/files/download-url", {}),
            "markdown_download_route_declared": "get" in paths.get("/v2/pages/{page_id}/content/markdown", {}),
            "file_routes": {p: [m for m in operations if m in ("get", "post", "patch", "put")]
                            for p, operations in paths.items() if "/files/" in p}}
        checks[stage] = {"status": "passed"}
        stage = "attachment_metadata"
        checks[stage]["status"] = "running"
        block, _ = store.writer.request("GET", "/blocks/" + block_id)
        if block.get("id") != block_id:
            raise GateError("FlowUs returned a different attachment block")
        checks[stage] = {"status": "passed"}
        stage = "download_url"
        checks[stage]["status"] = "running"
        # No caller-supplied URL accepted, and no expiring link included in the report.
        store.download_url(block)
        checks[stage] = {"status": "passed", "source": "official_api"}
        stage = "storage_network"
        checks[stage]["status"] = "running"
        content = store.download_block(block)
        checks[stage] = {"status": "passed"}
        stage = "file_integrity"
        actual = hashlib.sha256(content).hexdigest()
        report.update(bytes=len(content), sha256=actual)
        if actual != expected_sha256:
            raise GateError("Downloaded attachment does not match the expected SHA-256")
        checks[stage] = {"status": "passed"}
        report["status"] = "passed"
    except ManagerError as error:
        checks[stage] = {"status": "failed", **error_details(error)}
        report["status"] = "blocked"
    return report


def doctor(store, config, *, verify_writes=False):
    if verify_writes:
        config.pop("capability_receipt", None)
    checks = {}
    identities = {}
    trusted = governance_mode(config) == "trusted_client"
    if verify_writes:
        config["last_capability_report"] = {"checks": checks, "verified_at": now(),
            "governance_mode": governance_mode(config), "network_mode": network_mode(config),
            "status": "running", "stage": "api_access", "diagnostics": {
                name: {"status": "not_run"} for name in
                ("api_access", "schemas", "approval_isolation", "idempotent_create", "upload_roundtrip", "optimistic_lock")}}
    def stage(name, status="running"):
        if verify_writes:
            config["last_capability_report"]["stage"] = name
            config["last_capability_report"]["diagnostics"][name] = {"status": status}
    stage("api_access")
    roles = (("writer", store.writer),) if trusted else (("writer", store.writer), ("approval_reader", store.reader))
    for role, client in roles:
        identity, _ = client.request("GET", "/users/me")
        identities[role] = identity.get("id")
    if not all(identities.values()) or (not trusted and identities["writer"] == identities["approval_reader"]):
        raise GateError("Writer and approval reader must be different integrations")
    stage("api_access", "passed")
    stage("schemas")
    for table in TABLES:
        database, _ = store.client(table).request("GET", f"/databases/{store.database(table)}")
        expected = {"Name": "title", "ApprovalCode": "rich_text", "Decision": "select"} if table == "approvals" else FIELDS
        if any(database.get("properties", {}).get(name, {}).get("type") != kind for name, kind in expected.items()):
            raise GateError(f"{table} database schema is incompatible")
        store.list(table)
    checks["schemas_readable"] = True
    stage("schemas", "passed")
    if not trusted:
        stage("approval_isolation")
        try:
            store.writer.request("GET", f"/databases/{store.database('approvals')}")
        except APIError as exc:
            if exc.status not in (403, 404):
                raise
        else:
            raise GateError("Writer can access the approval database; isolate its parent permissions")
    if not verify_writes:
        return {"read_only": True, "checks": checks, "writes_enabled": False,
                "governance_mode": governance_mode(config)}
    if not trusted:
        probe_id = config.get("approval_probe_id")
        if not probe_id:
            raise GateError("Missing owner-created approval probe record")
        probe = store.by_id("approvals", probe_id)
        if not probe.etag:
            raise GateError("Approval GET did not return ETag")
        for client in (store.writer, store.reader):
            try:
                client.request("PATCH", f"/pages/{probe_id}",
                               {"properties": {"Name": {"type": "title", "title": rich(probe.data.get("title", "权限验证专用记录（勿审批）"))}}},
                               etag=probe.etag)
            except APIError as exc:
                if exc.status not in (403, 404):
                    raise
            else:
                raise GateError("An ordinary integration can write the approval probe; migration is blocked")
        checks["approval_isolation"] = True
        stage("approval_isolation", "passed")
    key = "capability-probe-" + str(uuid.uuid4())
    content = ("Synthetic FlowUs capability probe " + key).encode()
    data = {
        "schema_version": SCHEMA_VERSION, "tool_version": __version__, "kind": "probe", "title": key,
        "status": "probe", "sha256": hashlib.sha256(content).hexdigest(), "upload_state": "pending"}
    body = {"parent": {"database_id": store.database("versions")}, "properties": properties(key, data)}
    idempotency = stable_id(config["vault_id"], "capability", key)
    stage("idempotent_create")
    first, _ = store.writer.request("POST", "/pages", body, idempotency=idempotency)
    second, _ = store.writer.request("POST", "/pages", body, idempotency=idempotency)
    if first.get("id") != second.get("id"):
        raise GateError("Repeated page creation returned different records; migration is blocked")
    record = store.get("versions", key)
    if not record or record.id != first.get("id"):
        raise GateError("Page creation could not be reconciled")
    checks["idempotent_create"] = True
    stage("idempotent_create", "passed")
    stage("upload_roundtrip")
    store.upload(record, content, "capability-probe.txt")
    checks["upload_roundtrip"] = store.download(record) == content
    if not checks["upload_roundtrip"]:
        raise GateError("Downloaded capability probe does not match its original")
    stage("upload_roundtrip", "passed")
    stage("optimistic_lock")
    old = store.get("versions", key)
    store.update("versions", old, {**old.data, "probe_revision": 1})
    try:
        store.update("versions", old, {**old.data, "probe_revision": 2})
    except Conflict:
        checks["optimistic_lock"] = True
    else:
        raise GateError("Server accepted a stale ETag; migration is blocked")
    stage("optimistic_lock", "passed")
    for field in ("upload_roundtrip", "optimistic_lock", "idempotent_create"):
        if not checks.get(field):
            raise GateError(f"Failed capability check: {field}")
    config["capability_receipt"] = {"binding": binding(config), "checks": checks, "verified_at": now(),
                                    "tool_version": __version__, "identities": identities,
                                    "credential_binding": credential_binding(config)}
    config["last_capability_report"]["status"] = "passed"
    return {"checks": checks, "writes_enabled": True, "probe_key": key,
            "governance_mode": governance_mode(config)}


def credential_binding(config=None):
    if (config or {}).get("rest_auth") == "flowus_cli":
        # Runtime identity is independently checked by Manager.guard and the CLI adapter.
        return digest(["official_flowus_cli"])
    if transport_mode(config or {}) == "mcp_relay":
        return digest(["native_mcp_relay", "flowus"])
    names = credential_names(config or {})
    return digest([credential_value(name) for name in names])
