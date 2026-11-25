from __future__ import annotations

import copy
import hashlib
import uuid
from pathlib import Path

from . import SCHEMA_VERSION, __version__
from .common import Conflict, GateError, ManagerError, MissingAttachment, canonical, digest, file_hash, now, stable_id, governance_mode, transport_mode
from .confirmations import change_summary, validate_confirmation
from .rules import decide, normalize_key
from .transport import MAX_FILE


def binding(config):
    return digest({key: config.get(key) for key in
        ("vault_id", "databases", "business_parent_id", "approval_parent_id", "approval_probe_id", "governance_mode", "network_mode", "transport", "rest_auth")})


def require_gate(config):
    receipt = config.get("capability_receipt", {})
    required = ["upload_roundtrip", "optimistic_lock", "idempotent_create"]
    if governance_mode(config) == "isolated_approval":
        required.append("approval_isolation")
    if receipt.get("binding") != binding(config) or not all(receipt.get("checks", {}).get(k) for k in required):
        raise GateError("Cloud writes/migration blocked. Run doctor --verify-writes after setup.")
    if receipt.get("tool_version", __version__) != __version__:
        raise GateError("Tool changed since capability verification; run doctor --verify-writes again")


def snapshot(record):
    return {"id": record.id, "key": record.key, "etag": record.etag, "data": copy.deepcopy(record.data)}


class Manager:
    def __init__(self, store, config):
        self.store, self.config = store, config

    def guard(self):
        require_gate(self.config)
        if self.config.get("rest_auth") == "flowus_cli":
            self.store.writer.verify_identity(self.config["capability_receipt"].get("identities", {}).get("writer"))
        if transport_mode(self.config) == "mcp_relay":
            identity, _ = self.store.writer.request("GET", "/users/me")
            if identity.get("id") != self.config["capability_receipt"].get("identities", {}).get("writer"):
                raise GateError("Native MCP identity changed; repeat doctor --verify-writes")
        from .setup import credential_binding
        expected = self.config.get("capability_receipt", {}).get("credential_binding")
        if expected and expected != credential_binding(self.config):
            raise GateError("Credentials changed; repeat doctor --verify-writes for this client")

    def stamped(self, data):
        return {**data, "schema_version": SCHEMA_VERSION, "tool_version": __version__}

    def check(self, record):
        if record and record.data.get("schema_version") != SCHEMA_VERSION:
            raise GateError("Cloud record schema incompatible; refusing to write")
        return record

    def event(self, operation, action, data):
        # Stable event keys make recovery safe after an ambiguous API response.
        return self.store.create("events", operation + ":" + action, self.stamped({
            "title": action, "operation_id": operation, "action": action,
            "agent_id": self.config["agent_id"], "at": now(), "details": data, "status": "recorded",
            "config_version": self.config.get("remote_profile", {}).get("config_version"),
            "config_fingerprint": self.config.get("remote_profile", {}).get("fingerprint")}))

    def stage_version(self, key, metadata, content, operation):
        record = self.check(self.store.create("versions", key, self.stamped({
            **metadata, "operation_id": operation, "upload_state": "pending"})))
        if record.data.get("sha256") != hashlib.sha256(content).hexdigest():
            raise Conflict("Existing version content differs from the requested version")
        if record.data.get("upload_state") != "verified":
            try:
                downloaded = self.store.download(record)
                okay = hashlib.sha256(downloaded).hexdigest() == record.data["sha256"]
            except MissingAttachment:
                okay = False
            if not okay:
                self.store.upload(record, content, metadata["original_name"])
            # Appending an attachment can change the parent page's revision. Refresh its
            # ETag, but never absorb a concurrent human edit into a verified update.
            refreshed = self.check(self.store.get("versions", key))
            if not refreshed or refreshed.data != record.data:
                raise Conflict("Version metadata changed during file verification; review before resuming")
            record = refreshed
            data = {**record.data, "upload_state": "verified"}
            record = self.store.update("versions", record, data)
        return record

    def ingest(self, path: Path, *, dry_run=False, source_ref=None):
        path = Path(path).resolve()
        if not path.is_file() or path.stat().st_size > MAX_FILE:
            raise ManagerError("Input must be a regular file of at most 100 MiB")
        known_documents = {r.key: r for r in self.store.list("documents")}
        history = []
        stored_versions = self.store.list("versions")
        for record in stored_versions:
            if record.data.get("upload_state") != "verified":
                continue
            item = copy.deepcopy(record.data)
            document = known_documents.get(item.get("document_key"))
            if document and document.data.get("status") == "merged":
                document = known_documents.get(document.data.get("merged_into"), document)
            if document:
                item.update(category=document.data.get("category"), document_key=document.key,
                            series_key=document.data.get("series_key", item.get("series_key")))
            history.append(item)
        metadata = decide(path, self.config.get("rules", {}), history)
        content_hash = file_hash(path)
        doc_key = metadata.get("matched_document_key") or digest({"category": metadata["category"], "series_key": metadata["series_key"]})
        version_key = digest({"document": doc_key, "sha256": content_hash})
        current = self.check(self.store.get("documents", doc_key))
        canonical_duplicate = any(record.key == version_key and record.data.get("upload_state") == "verified"
                                  for record in stored_versions)
        # Migration deliberately preserves distinct legacy keys, including equal-content history.
        # A later submission must reuse a verified record in this document, without merging lines
        # or promoting an old migrated version over the authoritative Latest reference.
        legacy_candidates = [record for record in stored_versions if record.key.startswith("legacy:")
                             and record.data.get("document_key") == doc_key
                             and record.data.get("sha256") == content_hash
                             and record.data.get("upload_state") == "verified"]
        legacy_duplicate = bool(legacy_candidates and not canonical_duplicate)
        if legacy_duplicate:
            latest_key = current.data.get("latest") if current else None
            legacy_candidates.sort(key=lambda record: (
                record.key != latest_key, record.data.get("original_name") != path.name,
                record.data.get("version_label") != metadata.get("version_label"), record.key))
            version_key = legacy_candidates[0].key
        operation = stable_id(self.config["vault_id"], "ingest", version_key)
        if current and current.data.get("locked"):
            metadata["status"] = "needs_review"
            metadata["reason"] = "New version after locked final; approval required"
        if current and current.data.get("category") != metadata["category"]:
            metadata.update(status="needs_review", reason="Directory classification changed; confirmation required")
        metadata.update({"sha256": content_hash, "size": path.stat().st_size, "source": source_ref or str(path),
                         "document_key": doc_key, "added_at": now()})
        if dry_run:
            return {"dry_run": True, "operation_id": operation, "version_key": version_key,
                    "duplicate": canonical_duplicate or legacy_duplicate, "decision": metadata}
        self.guard()
        existing = self.store.get("versions", version_key)
        duplicate = bool(existing and existing.data.get("upload_state") == "verified")
        if current and current.data.get("status") != "active":
            raise GateError("Document is deleted or merged; review the target document before ingestion")
        self.event(operation, "ingest_started", {"source": metadata["source"], "sha256": content_hash})
        self.event(operation + ":" + digest(metadata["source"]), "source_seen", {
            "source": metadata["source"], "version_key": version_key, "sha256": content_hash})
        try:
            if not current:
                current = self.store.create("documents", doc_key, self.stamped({
                    "title": metadata["series_title"], "series_key": metadata["series_key"],
                    "category": metadata["category"], "latest": "", "locked": False, "status": "active"}))
                current = self.store.get("documents", doc_key)
            content = path.read_bytes()
            if hashlib.sha256(content).hexdigest() != content_hash:
                raise Conflict("Source changed during ingestion; retry when the file is stable")
            version = self.stage_version(version_key, metadata, content, operation)
            # Reuse the original decision on recovery; never promote a review item through a retry.
            metadata = version.data
            latest_key = current.data.get("latest")
            latest = self.check(self.store.get("versions", latest_key)) if latest_key else None
            promote = not legacy_duplicate and metadata.get("status") == "indexed" and (
                not latest or metadata["version_sort"] > latest.data["version_sort"])
            if promote and not current.data.get("locked"):
                self.store.update("documents", current, {**current.data, "latest": version.key,
                    "locked": bool(metadata.get("is_final")), "last_operation": operation})
            self.event(operation, "ingest_completed", {"version_key": version.key, "document_key": doc_key})
            return {"operation_id": operation, "version_key": version.key, "status": metadata["status"],
                    "outcome": "duplicate" if duplicate else ("needs_review" if metadata["status"] == "needs_review" else "added"),
                    "reason": metadata.get("reason"), "url": version.url, "source": metadata["source"],
                    "became_latest": self.store.get("documents", doc_key).data.get("latest") == version.key,
                    "warnings": metadata.get("warnings", [])}
        except ManagerError as exc:
            try:
                self.event(operation, "ingest_failed", {"error_code": exc.code, "version_key": version_key})
            except ManagerError:
                pass
            raise

    def latest(self, query=""):
        results = []
        for doc in self.store.list("documents"):
            if doc.data.get("status") != "active" or not doc.data.get("latest"):
                continue
            if query and normalize_key(query) not in normalize_key(canonical(doc.data)):
                continue
            version = self.store.get("versions", doc.data["latest"])
            if not version or version.data.get("upload_state") != "verified":
                raise Conflict("Latest points to a missing/unverified version; run doctor")
            if version.data.get("document_key") != doc.key:
                raise Conflict("Latest points to a version owned by another document")
            results.append({"document_key": doc.key, "version_key": version.key, **version.data,
                            "category": doc.data.get("category"), "url": version.url})
        return results

    def timeline(self, query=""):
        records = self.store.list("documents")
        docs = {r.key for r in records
                if not query or query == r.key or normalize_key(query) in normalize_key(canonical(r.data))}
        for record in records:
            if record.key in docs:
                docs.update(record.data.get("merged_sources", []))
        rows = [{"version_key": r.key, **r.data, "url": r.url} for r in self.store.list("versions")
                if r.data.get("document_key") in docs]
        return sorted(rows, key=lambda r: (r.get("version_sort", 0), r["version_key"]))

    def ask(self, question):
        import re
        words = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", normalize_key(question))
        terms = set(words)
        for word in words:
            if len(word) > 4:
                terms.update(word[i:i + 2] for i in range(len(word) - 1))
        rows = self.timeline()
        scored = []
        for row in rows:
            haystack = normalize_key(row.get("text", "") + " " + row.get("series_title", ""))
            score = sum(1 for word in terms if word in haystack)
            if score:
                scored.append((score, {"version_key": row["version_key"], "version_label": row.get("version_label"),
                    "title": row.get("original_name"), "excerpt": row.get("text", "")[:600], "url": row["url"]}))
        citations = [r for _, r in sorted(scored, key=lambda item: item[0], reverse=True)[:8]]
        return {"question": question, "kind": "retrieved_evidence", "citations": citations,
                "answer": "以下是可用于回答问题的原文片段。" if citations else "未找到相关资料。"}

    def note(self, version_key, text, operation=None, dry_run=False):
        record = self.check(self.store.get("versions", version_key))
        if not record:
            raise ManagerError("Unknown version key")
        if not text.strip():
            raise ManagerError("Note must not be blank")
        operation = operation or stable_id(self.config["vault_id"], "note", digest([version_key, text]))
        if dry_run:
            return {"version_key": version_key, "text": text, "dry_run": True}
        self.guard()
        event = self.event(operation, "note", {"version_key": version_key, "body": text})
        return {"operation_id": operation, "url": event.url}

    def propose(self, action, target, changes, *, dry_run=False):
        if action not in {"replace_final", "merge", "reclassify", "reclassify_batch", "logical_delete"}:
            raise ManagerError("Unsupported proposal action")
        allowed = {"replace_final": {"version_key"}, "merge": {"destination"},
                   "reclassify": {"category"}, "reclassify_batch": {"category", "document_keys"},
                   "logical_delete": set()}[action]
        if not isinstance(changes, dict) or set(changes) != allowed:
            raise ManagerError("Proposal changes must contain exactly the fields required for this action")
        doc = self.check(self.store.get("documents", target))
        if not doc or doc.data.get("status") != "active":
            raise ManagerError("Proposal target must be an active document")
        snapshots = {target: snapshot(doc)}
        if action == "replace_final":
            version = self.check(self.store.get("versions", changes.get("version_key", "")))
            if not version or version.data.get("document_key") != target or version.data.get("upload_state") != "verified":
                raise ManagerError("Replacement must be a verified version of the target document")
            snapshots["version:" + version.key] = snapshot(version)
        elif action == "merge":
            other = self.check(self.store.get("documents", changes.get("destination", "")))
            if not other or other.key == target or other.data.get("status") != "active":
                raise ManagerError("Merge destination must be a different active document")
            snapshots[other.key] = snapshot(other)
        elif action in ("reclassify", "reclassify_batch"):
            if not isinstance(changes.get("category"), str) or not changes["category"].strip():
                raise ManagerError("New category must not be blank")
            if action == "reclassify_batch":
                keys = changes["document_keys"]
                if (not isinstance(keys, list) or not keys or not all(isinstance(k, str) and k for k in keys)
                        or target not in keys or len(set(keys)) != len(keys)):
                    raise ManagerError("Batch document keys must be unique and include the target")
                for key in sorted(keys):
                    record = self.check(self.store.get("documents", key))
                    if not record or record.data.get("status") != "active":
                        raise ManagerError("Every batch target must be an active document")
                    snapshots[key] = snapshot(record)
        plan = {"action": action, "target": target, "changes": changes, "snapshots": snapshots}
        code = digest(plan)
        proposal_key = code
        summary = change_summary(plan)
        data = self.stamped({"title": action, "status": "pending", "plan": plan, "approval_code": code,
                             "change_summary": summary})
        if not dry_run:
            self.guard()
            self.store.create("proposals", proposal_key, data)
        return {"proposal_key": proposal_key, "approval_code": code, "plan": plan,
                "change_summary": summary, "dry_run": dry_run,
                "approval_instruction": ("在当前聊天向用户展示提案编号和具体差异，获得明确同意后引用真实用户消息执行 apply-confirmed。"
                    if governance_mode(self.config) == "trusted_client" else
                    "在独立审批库中新建记录，将 ApprovalCode 设为此审批码，并将 Decision 设为 Approved。")}

    def apply_confirmed(self, proposal_key, confirmation, *, dry_run=False):
        if governance_mode(self.config) != "trusted_client":
            raise GateError("Chat confirmation requires an explicit trusted_client configuration")
        evidence = validate_confirmation(confirmation, vault_id=self.config["vault_id"], proposal_key=proposal_key)
        proposal = self.check(self.store.get("proposals", proposal_key))
        return self._apply_proposal(proposal, dry_run=dry_run, confirmation=evidence)

    def apply_approved(self, proposal_key, *, dry_run=False):
        if governance_mode(self.config) == "trusted_client":
            raise GateError("This vault uses chat confirmation; use apply-confirmed with human evidence")
        proposal = self.check(self.store.get("proposals", proposal_key))
        return self._apply_proposal(proposal, dry_run=dry_run)

    def _apply_proposal(self, proposal, *, dry_run=False, confirmation=None):
        if not proposal:
            raise ManagerError("Unknown proposal")
        plan = proposal.data["plan"]
        if proposal.key != digest(plan) or proposal.data.get("approval_code") != digest(plan):
            raise GateError("Proposal content changed; submit a new proposal")
        if proposal.data.get("status") == "applied":
            return {"proposal_key": proposal.key, "status": "already_applied"}
        if proposal.data.get("status") != "pending":
            raise GateError("Only a pending proposal can be executed")
        operation = stable_id(self.config["vault_id"], "approval", proposal.key)
        if confirmation is None:
            approvals = [r for r in self.store.list("approvals") if r.data.get("approval_code") == proposal.key]
            if len(approvals) != 1 or approvals[0].data.get("decision") != "Approved":
                raise GateError("Missing, ambiguous or rejected human approval")
        current = {}
        for key, expected in plan["snapshots"].items():
            table, lookup = ("versions", key[8:]) if key.startswith("version:") else ("documents", key)
            record = self.check(self.store.get(table, lookup))
            # Idempotent recovery after a document update succeeded but the proposal update failed.
            if record and record.data.get("last_operation") == operation:
                # The full expected postimage must still match; last_operation alone is not authority.
                post = self.approval_postimage(plan, key, operation)
                if record.data != post:
                    raise Conflict("Applied target was edited after partial execution; manual review required")
                current[key] = record
                continue
            if not record or snapshot(record) != expected:
                raise Conflict("Approved target changed; approval is stale and must be renewed")
            current[key] = record
        if dry_run:
            return {"dry_run": True, "plan": plan, "change_summary": change_summary(plan)}
        self.guard()
        action, changes = plan["action"], plan["changes"]
        if confirmation is not None:
            self.event(operation, "human_confirmation", {"proposal_key": proposal.key, "evidence": confirmation,
                                                       "change_summary": change_summary(plan)})
        self.event(operation, "approval_started", {"proposal_key": proposal.key})
        keys = ([changes["destination"], plan["target"]] if action == "merge" else
                sorted(current) if action == "reclassify_batch" else [plan["target"]])
        for key in keys:
            record = current[key]
            if record.data.get("last_operation") != operation:
                self.store.update("documents", record, self.approval_postimage(plan, key, operation))
        self.store.update("proposals", proposal, {**proposal.data, "status": "applied", "operation_id": operation})
        self.event(operation, "approval_completed", {"proposal_key": proposal.key,
                                                   "change_summary": change_summary(plan)})
        return {"proposal_key": proposal.key, "status": "applied", "operation_id": operation}

    @staticmethod
    def approval_postimage(plan, key, operation):
        data = {**plan["snapshots"][key]["data"], "last_operation": operation}
        changes = plan["changes"]
        if key != plan["target"] and plan["action"] == "merge":
            data["merged_sources"] = sorted(set(data.get("merged_sources", []) + [plan["target"]]))
        elif plan["action"] == "replace_final":
            version = plan["snapshots"]["version:" + changes["version_key"]]["data"]
            data.update(latest=changes["version_key"], locked=bool(version.get("is_final")))
        elif plan["action"] == "logical_delete":
            data.update(status="deleted", latest="")
        elif plan["action"] in ("reclassify", "reclassify_batch"):
            data["category"] = changes["category"]
        elif plan["action"] == "merge":
            data.update(status="merged", merged_into=changes["destination"], latest="")
        return data
