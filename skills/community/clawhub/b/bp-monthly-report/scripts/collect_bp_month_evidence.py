#!/usr/bin/env python3
"""Collect month-relevant BP-linked reports into a lightweight manifest.

Current API chain:

1. BP `/bp/task/relation/pageAllReports` returns linked report ids (`bizId`) and
   coarse type info.
2. Work-report `/work-report/report/info` returns正文与回复列表。
3. Work-report `/work-report/report/getReportNodeDetail` returns汇报标题、
   汇报人、发起时间、节点状态与处理意见。

The drafting evidence object remains the online report itself. The script keeps
minimal metadata and direct report references instead of dumping one local JSON
snapshot per report.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://sg-al-cwork-web.mediportal.com.cn/open-api"
PRIORITY_RANK = {"summary_only": 0, "auxiliary": 1, "secondary": 2, "primary": 3}


def api_post(app_key: str, endpoint: str, payload: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        headers={"appKey": app_key, "Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def api_get(app_key: str, endpoint: str, params: dict | None = None) -> dict:
    resp = requests.get(
        f"{BASE_URL}{endpoint}",
        params=params or {},
        headers={"appKey": app_key, "Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def month_pattern(report_month: str) -> re.Pattern[str]:
    year, month = report_month.split("-")
    month_no_zero = str(int(month))
    return re.compile(
        rf"({year}年{month_no_zero}月|{year}-{month}|{month_no_zero}月|{int(month)}月)",
        re.IGNORECASE,
    )


def sanitize(name: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", name.strip())
    return cleaned[:80].strip("_") or "report"


def extract_report_id(item: dict) -> str:
    for key in ("reportId", "id", "bizId", "sourceId", "relationId"):
        value = item.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def report_link_md(title: str, report_id: str) -> str:
    if report_id:
        safe_title = title.replace("[", "\\[").replace("]", "\\]")
        return f"[{safe_title}](reportId={report_id}&linkType=report)"
    return title


def normalize_batch_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        return title

    stripped = re.sub(r"^【[^】]+】(?=关于)", "", title)
    stripped = re.sub(r"^[^-【】\s]{1,40}-(?=关于)", "", stripped)

    batch_markers = {
        "关于启动2026年度薪酬调整工作及《薪酬调整与职级晋升管理办法》意见征询的通知（请勿转发）",
        "关于启动2026年1月薪酬调整工作及《薪酬调整与职级晋升管理办法》意见征询的通知（请勿转发）",
        "关于确认2026年1月调薪方案（V3.0版）的通知",
    }
    if stripped in batch_markers:
        return stripped
    return title


def cluster_rows(rows: list[dict]) -> tuple[list[dict], int]:
    raw_hit_count = len(rows)
    grouped: dict[tuple[str, str, str], dict] = {}

    for row in rows:
        canonical_title = normalize_batch_title(row["report_title"])
        key = (row["task_id"], row["report_type"], canonical_title)
        existing = grouped.get(key)
        if existing is None:
            cloned = dict(row)
            cloned["canonical_title"] = canonical_title
            cloned["raw_hit_count"] = 1
            cloned["raw_titles"] = [row["report_title"]]
            grouped[key] = cloned
            continue

        existing["raw_hit_count"] += 1
        if row["report_title"] not in existing["raw_titles"]:
            existing["raw_titles"].append(row["report_title"])
        if PRIORITY_RANK.get(row["author_priority"], -1) > PRIORITY_RANK.get(existing["author_priority"], -1):
            existing["author_priority"] = row["author_priority"]
            existing["write_emp_name"] = row["write_emp_name"]
            existing["report_id"] = row["report_id"]
            existing["report_link_md"] = row["report_link_md"]
            existing["report_link_status"] = row["report_link_status"]
        if not existing.get("report_create_time") and row.get("report_create_time"):
            existing["report_create_time"] = row["report_create_time"]

    clustered = list(grouped.values())
    clustered.sort(
        key=lambda row: (
            row.get("report_create_time") or "",
            row["evidence_id"],
        )
    )
    for idx, row in enumerate(clustered, start=1):
        row["evidence_id"] = f"R{idx:03d}"
    return clustered, raw_hit_count


def dedupe(items: list[str]) -> list[str]:
    out = []
    seen = set()
    for item in items:
        item = re.sub(r"\s+", " ", item or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def split_progress(content: str) -> dict:
    text = normalize_text(content)
    progress_facts = []
    completed_items = []
    in_flight_items = []
    blockers = []
    next_steps = []

    clauses = re.split(r"[；;。]\s*", text)
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue
        if any(tag in clause for tag in ["已完成", "完成了", "形成", "已形成", "已进入", "已推进", "已修复", "已优化", "通过", "发布", "上线", "落地", "同意"]):
            completed_items.append(clause)
            progress_facts.append(clause)
            continue
        if any(tag in clause for tag in ["正在", "推进", "开展", "组织", "测试", "试点", "沟通", "评估", "待", "拟", "计划", "请示", "征询", "讨论", "确认"]):
            in_flight_items.append(clause)
            progress_facts.append(clause)
            continue
        if any(tag in clause for tag in ["问题", "风险", "不足", "漏洞", "卡点", "延迟", "待评估", "需关注", "缺乏", "未完成", "异常"]):
            blockers.append(clause)
            progress_facts.append(clause)
            continue
        if any(tag in clause for tag in ["下一步", "后续", "下周", "下月", "将", "拟于", "继续推进"]):
            next_steps.append(clause)
            progress_facts.append(clause)

    return {
        "progress_facts": dedupe(progress_facts),
        "completed_items": dedupe(completed_items),
        "in_flight_items": dedupe(in_flight_items),
        "blockers": dedupe(blockers),
        "next_steps": dedupe(next_steps),
    }


def priority(author: str, report_type: str, owner_name: str) -> str:
    if author == owner_name and report_type == "manual":
        return "primary"
    if report_type == "manual":
        return "auxiliary"
    return "summary_only"


def collect_attachments(item: dict) -> tuple[list, str]:
    attachment_keys = [
        "attachments",
        "attachmentList",
        "attachList",
        "fileList",
        "files",
        "annexList",
        "accessoryList",
    ]
    attachments = []
    for key in attachment_keys:
        val = item.get(key)
        if isinstance(val, list) and val:
            attachments.extend(val)
    if attachments:
        return attachments, "exposed_in_detail_api"
    return [], "not_exposed_in_current_report_detail_api"


def normalize_report_type(raw_type: str | None, raw_type_desc: str | None) -> str:
    value = (raw_type or "").strip().lower()
    if value in {"manual", "ai"}:
        return value
    desc = (raw_type_desc or "").strip()
    if desc == "AI汇报":
        return "ai"
    return "manual"


def extract_month_from_time(text: str | None) -> str:
    value = (text or "").strip()
    if not value:
        return ""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt)
            return f"{dt.year:04d}-{dt.month:02d}"
        except ValueError:
            continue
    match = re.search(r"(\d{4})-(\d{2})", value)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return ""


def stringify_replies(replies: list[dict[str, Any]]) -> list[str]:
    out = []
    for reply in replies or []:
        name = reply.get("replyEmpName") or ""
        content = normalize_text(reply.get("content") or "")
        time = reply.get("createTime") or ""
        if not content:
            continue
        prefix = f"{name}于{time}回复：" if name or time else ""
        out.append(prefix + content)
    return out


def stringify_node_ops(node_list: list[dict[str, Any]]) -> list[str]:
    out = []
    for node in node_list or []:
        node_name = node.get("nodeName") or ""
        node_type = node.get("type") or ""
        for user in node.get("userList") or []:
            name = user.get("name") or ""
            operate = user.get("operate") or user.get("status") or ""
            content = normalize_text(user.get("content") or "")
            finish_time = user.get("finishTime") or ""
            parts = [x for x in [node_name, node_type, name, finish_time, operate] if x]
            prefix = "/".join(parts)
            if content:
                out.append(f"{prefix}：{content}" if prefix else content)
            elif prefix:
                out.append(prefix)
    return out


def fetch_report_details(app_key: str, report_id: str) -> dict:
    info_obj = api_get(app_key, "/work-report/report/info", {"reportId": report_id})
    node_obj = api_get(app_key, "/work-report/report/getReportNodeDetail", {"reportId": report_id})
    info = info_obj.get("data") or {}
    node = node_obj.get("data") or {}

    replies = info.get("replies") or []
    node_list = node.get("nodeList") or []
    attachments, attachment_status = collect_attachments(info)
    if attachment_status.startswith("not_exposed"):
        attachments, attachment_status = collect_attachments(node)

    reply_lines = stringify_replies(replies)
    node_lines = stringify_node_ops(node_list)
    combined_parts = [
        node.get("main") or "",
        info.get("content") or node.get("content") or "",
        *reply_lines,
        *node_lines,
    ]
    combined_text = "；".join(part for part in combined_parts if normalize_text(part))

    return {
        "report_id": str(info.get("reportId") or node.get("id") or report_id),
        "report_title": (node.get("main") or "").strip(),
        "content": info.get("content") or node.get("content") or "",
        "write_emp_name": node.get("writeEmpName") or "",
        "report_create_time": node.get("createTime") or info.get("createTime") or "",
        "replies": replies,
        "reply_lines": reply_lines,
        "node_list": node_list,
        "node_lines": node_lines,
        "attachments": attachments,
        "attachment_fetch_status": attachment_status,
        "combined_text": combined_text,
    }


def fetch_task_report_rows(
    app_key: str,
    report_month: str,
    owner_name: str,
    task_ids: list[str],
    page_size: int = 100,
) -> tuple[list[dict], dict[str, list[dict]], dict[str, int]]:
    exported: list[dict] = []
    seen_task_report = set()
    detail_cache: dict[str, dict] = {}
    raw_hit_count = 0
    candidate_count = 0

    for task_id in task_ids:
        page_index = 1
        while True:
            data = api_post(
                app_key,
                "/bp/task/relation/pageAllReports",
                {
                    "taskId": task_id,
                    "pageIndex": page_index,
                    "pageSize": page_size,
                    "sortBy": "business_time",
                    "sortOrder": "desc",
                },
            ).get("data") or {}
            items = data.get("records") or data.get("list") or data.get("rows") or []
            if not items:
                break

            raw_hit_count += len(items)
            for item in items:
                report_id = extract_report_id(item)
                if not report_id:
                    continue
                raw_type = item.get("type")
                raw_type_desc = item.get("typeDesc")
                report_type = normalize_report_type(raw_type, raw_type_desc)
                cache_key = f"{report_id}"
                if cache_key not in detail_cache:
                    detail_cache[cache_key] = fetch_report_details(app_key, report_id)
                detail = detail_cache[cache_key]
                report_month_actual = extract_month_from_time(detail.get("report_create_time"))
                if report_month_actual != report_month:
                    continue
                candidate_count += 1
                key = (task_id, report_id)
                if key in seen_task_report:
                    continue
                seen_task_report.add(key)

                combined_text = detail["combined_text"]
                exported.append(
                    {
                        "evidence_id": f"R{len(exported)+1:03d}",
                        "task_id": task_id,
                        "report_month": report_month,
                        "report_title": detail["report_title"] or f"汇报{report_id}",
                        "write_emp_name": detail["write_emp_name"],
                        "report_type": report_type,
                        "author_priority": priority(detail["write_emp_name"], report_type, owner_name),
                        "report_id": report_id,
                        "report_link_md": report_link_md(detail["report_title"] or f"汇报{report_id}", report_id),
                        "report_link_status": "ready" if report_id else "missing_report_id",
                        "report_create_time": detail["report_create_time"],
                        "progress": split_progress(combined_text),
                        "attachments": detail["attachments"],
                        "attachment_fetch_status": detail["attachment_fetch_status"],
                        "reply_count": len(detail["replies"]),
                        "node_count": len(detail["node_list"]),
                        "reply_lines": detail["reply_lines"],
                        "node_lines": detail["node_lines"],
                    }
                )

            total = int(data.get("total") or 0)
            actual_page_size = int(data.get("pageSize") or data.get("size") or page_size or 0)
            if actual_page_size <= 0 or page_index * actual_page_size >= total:
                break
            page_index += 1

    clustered_rows, clustered_raw_hit_count = cluster_rows(exported)
    rows_by_task: dict[str, list[dict]] = {}
    for row in clustered_rows:
        rows_by_task.setdefault(row["task_id"], []).append(row)

    stats = {
        "raw_report_hit_count": raw_hit_count,
        "candidate_report_count": candidate_count,
        "adopted_report_count": len(clustered_rows),
        "adopted_primary_report_count": sum(1 for row in clustered_rows if row["author_priority"] == "primary"),
        "adopted_other_manual_report_count": sum(
            1 for row in clustered_rows if row["report_type"] == "manual" and row["author_priority"] != "primary"
        ),
        "adopted_ai_report_count": sum(1 for row in clustered_rows if row["report_type"] == "ai"),
        "clustered_raw_hit_count": clustered_raw_hit_count,
    }
    return clustered_rows, rows_by_task, stats


def write_manifest_md(path: Path, rows: list[dict], report_month: str, owner_name: str, stats: dict[str, int]) -> None:
    total = len(rows)
    primary = sum(1 for row in rows if row["author_priority"] == "primary")
    auxiliary_manual = sum(
        1
        for row in rows
        if row["report_type"] == "manual" and row["author_priority"] != "primary"
    )
    ai_count = sum(1 for row in rows if row["report_type"] == "ai")
    lines = [
        "# Report Manifest",
        "",
        f"> report_month: {report_month}",
        f"> owner_name: {owner_name}",
        "> note: 主证据对象为在线汇报链接；当前通过 BP 关联接口取 `bizId/reportId`，再用工作协同详情接口补正文、回复与节点意见。",
        f"> raw_report_hit_count: {stats['raw_report_hit_count']}",
        f"> candidate_report_count: {stats['candidate_report_count']}",
        f"> adopted_report_count: {total}",
        f"> adopted_primary_report_count: {primary}",
        f"> adopted_other_manual_report_count: {auxiliary_manual}",
        f"> adopted_ai_report_count: {ai_count}",
        "> month_attribution_mode: report_time",
        "> batch_collapse_rule: 批量分发且正文模板一致的通知/确认类汇报，按同一动作模板归并，不按分发对象重复计数。",
        "",
        "| ref | title | raw_hits | author | priority | link_status | task_id | report_time | replies | nodes | attachment_status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {ref} | {title} | {raw_hits} | {author} | {priority} | {link_status} | {task_id} | {report_time} | {replies} | {nodes} | {attachment_status} |".format(
                ref=row["evidence_id"],
                title=row["canonical_title"].replace("|", "\\|"),
                raw_hits=row["raw_hit_count"],
                author=row["write_emp_name"] or "",
                priority=row["author_priority"],
                link_status=row["report_link_status"],
                task_id=row["task_id"],
                report_time=(row.get("report_create_time") or "").replace("|", "\\|"),
                replies=row.get("reply_count", 0),
                nodes=row.get("node_count", 0),
                attachment_status=row["attachment_fetch_status"],
            )
        )

    for row in rows:
        lines.extend(
            [
                "",
                f"## {row['evidence_id']}",
                "",
                f"- 标题：{row['report_link_md']}",
                f"- 原始命中数：`{row['raw_hit_count']}`",
                f"- 作者：{row['write_emp_name'] or ''}",
                f"- 类型：{row['report_type'] or ''}",
                f"- 任务ID：`{row['task_id']}`",
                f"- 优先级：{row['author_priority']}",
                f"- report_id：`{row['report_id'] or 'missing'}`",
                f"- report_time：`{row.get('report_create_time') or ''}`",
                f"- report_link_status：`{row['report_link_status']}`",
                f"- attachment_fetch_status：`{row['attachment_fetch_status']}`",
                f"- 回复数：`{row.get('reply_count', 0)}`",
                f"- 节点数：`{row.get('node_count', 0)}`",
                "- 归并标题：",
            ]
        )
        for raw_title in row["raw_titles"]:
            lines.append(f"  - {raw_title}")
        if row.get("reply_lines"):
            lines.append("- 回复摘录：")
            for item in row["reply_lines"][:4]:
                lines.append(f"  - {item}")
        if row.get("node_lines"):
            lines.append("- 节点/意见摘录：")
            for item in row["node_lines"][:4]:
                lines.append(f"  - {item}")
        lines.append("- 进展事实：")
        facts = row["progress"]["progress_facts"] or ["未从正文与回复中抽出稳定进展事实"]
        for fact in facts:
            lines.append(f"  - {fact}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-key", required=True)
    parser.add_argument("--report-month", required=True, help="YYYY-MM")
    parser.add_argument("--owner-name", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--task-id", action="append", required=True)
    parser.add_argument("--size", type=int, default=100)
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, _rows_by_task, stats = fetch_task_report_rows(
        app_key=args.app_key,
        report_month=args.report_month,
        owner_name=args.owner_name,
        task_ids=args.task_id,
        page_size=args.size,
    )
    manifest = out_dir / "manifest.md"
    write_manifest_md(manifest, rows, args.report_month, args.owner_name, stats)
    print(manifest)


if __name__ == "__main__":
    main()
