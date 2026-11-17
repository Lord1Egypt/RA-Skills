from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

FIELD_ALIASES = {
    "topic_id": ["topic_id", "id", "page_id", "页面ID"],
    "title": ["title", "topic_title", "选题标题", "标题"],
    "source_date": ["source_date", "date", "日期", "事件日期"],
    "captured_at": ["captured_at", "created_at", "采集日期"],
    "status": ["status", "lifecycle", "状态"],
    "current_priority": ["current_priority", "priority", "推荐优先级"],
    "topic_type": ["topic_type", "type", "主题类型"],
    "collection": ["collection", "合集", "所属合集"],
    "hypothesis": ["hypothesis", "value_judgment", "核心论点", "价值判断"],
    "evidence": ["evidence", "sources", "事实锚点"],
    "existing_coverage": ["existing_coverage", "coverage", "已有覆盖"],
    "related_published_content": ["related_published_content", "published", "关联已发内容"],
    "required_trigger": ["required_trigger", "trigger", "触发条件"],
    "private_notes": ["private_notes", "notes", "备注"],
}


def stable_id(record: dict[str, Any]) -> str:
    raw = "|".join(str(record.get(key, "")) for key in ("title", "source_date", "collection"))
    return "topic-" + sha256(raw.encode("utf-8")).hexdigest()[:16]


def pick(row: dict[str, Any], aliases: list[str]) -> Any:
    for key in aliases:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return ""


def parse_list(value: Any) -> list[Any]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
        return [item.strip() for item in re.split(r"[\n;；|]", value) if item.strip()]
    return [value]


def normalize(row: dict[str, Any]) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for target, aliases in FIELD_ALIASES.items():
        value = pick(row, aliases)
        record[target] = parse_list(value) if target in {"evidence", "existing_coverage", "related_published_content"} else value
    record["topic_id"] = record["topic_id"] or stable_id(record)
    record["captured_at"] = record["captured_at"] or datetime.now(timezone.utc).isoformat()
    record["status"] = record["status"] or "new"
    record["current_priority"] = record["current_priority"] or None
    return record


def read_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("topics", [])
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    text = path.read_text(encoding="utf-8", errors="ignore")
    rows: list[dict[str, Any]] = []
    heading = None
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+)$", line)
        if match:
            heading = match.group(1).strip()
            rows.append({"选题标题": heading})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize topic inputs")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = read_rows(Path(args.input))
    normalized = [normalize(row) for row in rows if pick(row, FIELD_ALIASES["title"])]
    Path(args.output).write_text(json.dumps({"topics": normalized}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"topics": len(normalized)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
