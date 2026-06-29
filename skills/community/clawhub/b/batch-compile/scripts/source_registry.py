from __future__ import annotations

import system_config as sc
from utils import now_str

COMMON_MODULE_VERSION = "paperkb-v3.0"


def add_source(record: dict) -> str:
    found_id = ""

    def mutate(data: dict) -> dict:
        nonlocal found_id
        for sid, old in data.items():
            same = (
                old.get("source_url") == record.get("source_url")
                and old.get("target_kb_owner") == record.get("target_kb_owner")
                and old.get("target_kb_repo") == record.get("target_kb_repo")
                and old.get("target_project_id", "") == record.get("target_project_id", "")
            )
            if same:
                merged = {**old, **record, "source_id": sid}
                data[sid] = merged
                found_id = sid
                return data
        source_id = record.get("source_id") or sc.new_record_id("src")
        record["source_id"] = source_id
        record.setdefault("enabled", True)
        record.setdefault("auto_update", True)
        record.setdefault("scan_mode", "schedule_and_manual")
        record.setdefault("webhook_enabled", False)
        record.setdefault("created_at", now_str())
        data[source_id] = record
        found_id = source_id
        return data

    sc.update_json("sources.json", mutate, default={})
    return found_id


def get_source(source_id: str) -> dict | None:
    return sc.sources().get(source_id)
