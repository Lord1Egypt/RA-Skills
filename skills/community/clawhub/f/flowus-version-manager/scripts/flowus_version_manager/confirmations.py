"""Confirmation evidence supplied by a trusted chat client, not server-side authentication."""
from __future__ import annotations

import datetime as dt
import re

from .common import GateError, digest


def validate_confirmation(value, *, vault_id, proposal_key):
    if not isinstance(value, dict):
        raise GateError("A structured human chat confirmation is required")
    expected = {"vault_id": vault_id, "proposal_key": proposal_key,
                "source": "current_chat", "author_role": "user", "decision": "Approved"}
    if any(value.get(key) != wanted for key, wanted in expected.items()):
        raise GateError("Confirmation must come from the human user in the current chat and match this proposal/vault")
    for field in ("thread_id", "message_id", "text", "confirmed_at"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise GateError("Confirmation is missing its human message reference, quote or timestamp")
    try:
        timestamp = dt.datetime.fromisoformat(value["confirmed_at"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("Timezone is required")
    except ValueError:
        raise GateError("Confirmation timestamp must be ISO 8601 with a timezone") from None
    quote = value["text"].strip()
    # Reject obvious uncertainty/negation. The trusted client must still check semantic intent
    # against the actual user message; a local JSON file is not an unforgeable authorization.
    negative = r"不同意|不批准|不确认|不要|别执行|取消|拒绝|暂不|再看看|考虑|等等|稍后|[?？]|\b(no|not|maybe|later|reject|cancel)\b"
    positive = r"同意|批准|确认|可以执行|执行这个|\b(yes|approve|approved|confirm|confirmed)\b"
    short_approval = re.fullmatch(r"(好|好的|可以|行|没问题|ok|okay)[。.!！\s]*", quote, re.I)
    if re.search(negative, quote, re.I) or not (re.search(positive, quote, re.I) or short_approval):
        raise GateError("The quoted message is not an explicit approval; ask the user about this exact proposal")
    evidence = {key: value[key] for key in (*expected, "thread_id", "message_id", "text", "confirmed_at")}
    return {**evidence, "evidence_hash": digest(evidence)}


def change_summary(plan):
    action, changes = plan["action"], plan["changes"]
    rows = []
    for key, snapshot in plan["snapshots"].items():
        if key.startswith("version:"):
            continue
        before = snapshot["data"]
        after = {}
        if action in ("reclassify", "reclassify_batch"):
            before = {"category": before.get("category")}
            after = {"category": changes["category"]}
        elif action == "replace_final":
            before = {"latest": before.get("latest"), "locked": before.get("locked")}
            version = plan["snapshots"]["version:" + changes["version_key"]]["data"]
            after = {"latest": changes["version_key"], "locked": bool(version.get("is_final"))}
        elif action == "logical_delete":
            before = {"status": before.get("status"), "latest": before.get("latest")}
            after = {"status": "deleted", "latest": ""}
        elif action == "merge":
            if key == plan["target"]:
                before = {"status": before.get("status"), "latest": before.get("latest")}
                after = {"status": "merged", "latest": "", "merged_into": changes["destination"]}
            else:
                before = {"latest": before.get("latest"), "merged_sources": before.get("merged_sources", [])}
                after = {"latest": before["latest"], "merged_sources": sorted(set(before["merged_sources"] + [plan["target"]]))}
        rows.append({"document_key": key, "title": snapshot["data"].get("title"),
                     "url": "https://flowus.cn/" + snapshot["id"], "before": before, "after": after})
    return {"action": action, "affected_documents": len(rows), "changes": rows}
