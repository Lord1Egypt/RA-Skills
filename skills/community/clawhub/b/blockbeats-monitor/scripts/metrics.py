# 本文件负责统计 24h 提及次数、上一周期对比，以及确定“昨日重点相关内容”。

from collections import defaultdict
from datetime import timedelta

from content_identity import IMPORTANT_SOURCE_TYPES, canonical_content_key, pick_representative_record, source_priority
from keywords import KEYWORD_GROUPS, match_groups


def build_windows(now):
    """当前窗口为过去 24h，上一周期为再往前 24h。"""
    window_end = now
    window_start = window_end - timedelta(hours=24)
    previous_start = window_start - timedelta(hours=24)
    previous_end = window_start
    return window_start, window_end, previous_start, previous_end


def _group_rows(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["group_id"]].append(row)
    return grouped


def _pick_representative_rows(rows):
    """按内容归一化去重，并为每个归一化 key 选出最优展示行。"""
    grouped = defaultdict(list)
    for row in rows:
        grouped[canonical_content_key(row)].append(row)
    return [pick_representative_record(group_rows) for group_rows in grouped.values()]


def _unique_item_count(rows):
    return len({canonical_content_key(row) for row in rows})


def summarize_metrics(current_rows, previous_rows):
    """按关键词组统计当前和上一周期的唯一内容提及次数。"""
    current_by_group = _group_rows(current_rows)
    previous_by_group = _group_rows(previous_rows)
    summaries = []
    for group in KEYWORD_GROUPS:
        current_count = _unique_item_count(current_by_group.get(group.id, []))
        previous_count = _unique_item_count(previous_by_group.get(group.id, []))
        summaries.append({
            "group_id": group.id,
            "group_name": group.name,
            "mention_count": current_count,
            "previous_mention_count": previous_count,
            "delta": current_count - previous_count,
            "items": dedupe_items(current_by_group.get(group.id, [])),
        })
    group_order = {group.id: index for index, group in enumerate(KEYWORD_GROUPS)}
    summaries.sort(key=lambda item: (-item["mention_count"], group_order[item["group_id"]]))
    return summaries


def dedupe_items(rows):
    """同一内容可能同时来自多个端点，展示前按归一化内容去重。"""
    items = _pick_representative_rows(rows)
    items.sort(key=lambda row: row.get("published_at") or "", reverse=True)
    return items


def _title_and_body_hit(row):
    title = row.get("title") or ""
    body = "\n".join([row.get("abstract") or "", row.get("content") or ""])
    return bool(match_groups(title)) and bool(match_groups(body))


def select_important_items(current_rows, limit=5):
    """重点内容排序：important 来源优先、多组命中优先、标题正文双命中优先、发布时间新优先。"""
    by_item = {}
    for row in current_rows:
        key = canonical_content_key(row)
        item = by_item.get(key)
        if item is None:
            item = dict(row, group_names=set(), group_ids=set())
            by_item[key] = item
        elif source_priority(row) > source_priority(item):
            # 同一条内容如果同时出现在 important 和 24h，保留更适合展示的版本。
            item.update(row)
        item["group_names"].add(row["group_name"])
        item["group_ids"].add(row["group_id"])
    items = list(by_item.values())
    for item in items:
        item["group_names"] = sorted(item["group_names"])
        item["group_ids"] = sorted(item["group_ids"])
        item["is_important_source"] = item.get("source_type") in IMPORTANT_SOURCE_TYPES
        item["title_and_body_hit"] = _title_and_body_hit(item)
    # True 和更大的数值排在前面，确保 important、多关键词、标题正文双命中、新近内容优先。
    items.sort(
        key=lambda item: (
            item["is_important_source"],
            len(item["group_ids"]),
            item["title_and_body_hit"],
            item.get("published_at") or "",
        ),
        reverse=True,
    )
    return items[:limit]
