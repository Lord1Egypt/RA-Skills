#!/usr/bin/env python3
"""Generate scheme-v2 monthly BP reports in batch.

This script now uses:

1. BP `/bp/task/relation/pageAllReports` only as report-id discovery.
2. Work-report detail APIs for正文、回复、节点意见.
3. Fine-grained card output:
   - `04_cards/kr_cards/*.md`
   - `04_cards/action_cards/*.md`
   - `05_review_queue/*.md`
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from collect_bp_month_evidence import (
    api_get,
    fetch_task_report_rows,
    report_link_md,
)
from dump_bp_anchor_map import build_anchor_map


GREEN = "#2e7d32"
YELLOW = "#b26a00"
RED = "#d32f2f"
BLACK = "#111111"
COLOR = {"🟢": GREEN, "🟡": YELLOW, "🔴": RED, "⚫": BLACK}
LIGHT_NAME = {"🟢": "green", "🟡": "yellow", "🔴": "red", "⚫": "black"}

SEVERE_MARKERS = ["无法推进", "已终止", "不可逆", "严重失控", "目标失效"]
YELLOW_MARKERS = ["风险", "问题", "不一致", "纠偏", "争议", "压力", "不足", "缺少", "待审批", "待确认", "待推进", "补位"]


def strip_html(text: str) -> str:
    return (
        (text or "")
        .replace("<p>", "")
        .replace("</p>", "")
        .replace("<strong>", "")
        .replace("</strong>", "")
        .replace("<br>", " ")
        .replace("<br/>", " ")
        .replace("<br />", " ")
        .replace("&nbsp;", " ")
    )


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", strip_html(text)).strip()


def write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", value)
    return cleaned.strip("_")[:100] or "item"


def dedupe_rows(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for row in rows:
        key = (row["task_id"], row["report_id"], row["canonical_title"])
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def priority_score(value: str) -> int:
    return {"primary": 3, "secondary": 2, "auxiliary": 1, "summary_only": 0}.get(value, 0)


def sort_rows(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -priority_score(row["author_priority"]),
            row.get("report_create_time") or "",
            row["evidence_id"],
        ),
    )


def shorten(text: str, limit: int = 88) -> str:
    value = normalize_text(text).strip(" -:：;；，,。")
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def progress_lines(rows: list[dict], limit: int = 3) -> list[str]:
    out = []
    seen = set()
    for row in rows:
        facts = row["progress"].get("progress_facts") or []
        source = facts[:3] or [f"已采纳证据：{row['report_link_md']}"]
        for fact in source:
            fact = shorten(fact)
            if not fact or fact in seen:
                continue
            seen.add(fact)
            out.append(fact)
            if len(out) >= limit:
                return out
    return out


def evidence_md(rows: list[dict], limit: int = 4) -> str:
    if not rows:
        return "未检索到稳定证据"
    parts = []
    for row in rows[:limit]:
        parts.append(
            f"`{row['evidence_id']}`{row['report_link_md']}({row['write_emp_name'] or ''}/{row['author_priority']})"
        )
    return "；".join(parts)


def earliest_due_month(text: str) -> int | None:
    values = [int(x) for x in re.findall(r"([1-9]|1[0-2])月", normalize_text(text))]
    return min(values) if values else None


def detect_light(text: str, has_rows: bool, current_month: int, due_month: int | None, primary_count: int) -> str:
    if not has_rows:
        return "⚫"
    if any(marker in text for marker in SEVERE_MARKERS):
        return "🔴"
    if any(marker in text for marker in YELLOW_MARKERS):
        return "🟡"
    if primary_count == 0 and (due_month is None or due_month <= current_month + 2):
        return "🟡"
    if due_month is not None and due_month <= current_month + 2:
        return "🟡"
    return "🟢"


def status_block(light: str, reason: str) -> list[str]:
    color = COLOR[light]
    lines = [
        f"- <span style=\"color:{color}; font-weight:700;\">灯色判断：{light}</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">判断理由：{reason}</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">人工判断：待确认（请填写：同意 / 不同意）</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">若同意：请明确填写“同意”。</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>",
    ]
    if light == "⚫":
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">黑灯类型：需人工复核后选择（未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕）</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">请人工回答：当前属于哪一种黑灯类型？</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若未开展：请回答下月/下周期准备怎么做。</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若已开展但未关联：请回答需补关联的材料/汇报是什么。</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若体外开展但无留痕：请回答需补什么留痕、何时补齐。</span>",
            ]
        )
    if light in {"🟡", "🔴", "⚫"}:
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">整改方案：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">承诺完成时间：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">下周期具体举措：待补充</span>",
            ]
        )
    if light == "⚫":
        lines.append(f"  <span style=\"color:{color}; font-weight:700;\">持续提醒至下周期：是</span>")
    return lines


def aggregate_kr_rows(kr: dict, rows_by_task: dict[str, list[dict]]) -> list[dict]:
    rows = []
    rows.extend(rows_by_task.get(kr["result_id"], []))
    for action in kr.get("actions") or []:
        rows.extend(rows_by_task.get(action["action_id"], []))
    return dedupe_rows(sort_rows(rows))


def kr_reason(light: str, kr: dict, current_month: int) -> str:
    if light == "⚫":
        return f"{current_month} 月没有有效汇报或可信证据来判断“{kr['result_name']}”是否真实推进，当前应判黑灯。"
    if light == "🔴":
        return f"当前证据已显示“{kr['result_name']}”出现明显异常或严重偏离，按版本二应判红灯。"
    if light == "🟡":
        return f"“{kr['result_name']}”已有真实推进证据，但当前偏差或风险已对后续按时达成构成实质压力，按版本二应判黄灯。"
    return f"“{kr['result_name']}”已有真实推进证据，且当前偏差尚未实质影响最终按时达成信心，按版本二可判绿灯。"


def action_reason(light: str, action_name: str, current_month: int) -> str:
    if light == "⚫":
        return f"当前没有检索到能直接支撑“{action_name}”的有效汇报，无法判断该举措在 {current_month} 月是否真实推进。"
    if light == "🔴":
        return f"当前证据已显示“{action_name}”存在严重异常或明显失控信号，按版本二应判红灯。"
    if light == "🟡":
        return f"“{action_name}”已有真实推进，但当前偏差或风险已对后续关键结果达成形成实质威胁，按版本二应判黄灯。"
    return f"“{action_name}”已有真实推进证据，当前虽未完全闭环，但整体仍处于可按计划推进的正常区间。"


def overall_light(kr_cards: list[dict]) -> str:
    lights = {card["light"] for card in kr_cards}
    if "🔴" in lights:
        return "🔴"
    if "🟡" in lights or "⚫" in lights:
        return "🟡"
    return "🟢"


def result_judgment_text(card: dict) -> str:
    if card["light"] == "🟢":
        return "<span style=\"color:#2e7d32; font-weight:700;\">🟢 当前整体仍处于可按计划推进的正常区间。</span>"
    if card["light"] == "🟡":
        return "<span style=\"color:#b26a00; font-weight:700;\">🟡 已有真实推进，但当前偏差或风险已构成实质压力。</span>"
    if card["light"] == "🔴":
        return "<span style=\"color:#d32f2f; font-weight:700;\">🔴 已出现明显异常或严重偏离。</span>"
    return "<span style=\"color:#111111; font-weight:700;\">⚫ 当前缺少有效证据，无法判断进展。</span>"


def resolve_group_meta(app_key: str, period_id: str, group_id: str) -> tuple[str, str]:
    tree = api_get(app_key, "/bp/group/getTree", {"periodId": period_id}).get("data") or []

    def walk(nodes: list[dict[str, Any]], parents: list[str]) -> tuple[str, str] | None:
        for node in nodes or []:
            node_id = str(node.get("id") or "")
            name = node.get("name") or ""
            path = parents + [name]
            if node_id == str(group_id):
                return name, "/".join(path)
            found = walk(node.get("children") or [], path)
            if found:
                return found
        return None

    found = walk(tree, [])
    if found:
        return found
    return group_id, group_id


def build_cards(anchor_map: list[dict], rows_by_task: dict[str, list[dict]], current_month: int) -> tuple[list[dict], list[dict]]:
    kr_cards = []
    action_cards = []
    for goal_idx, goal in enumerate(anchor_map, start=1):
        section_key = f"2.{goal_idx}"
        for kr_idx, kr in enumerate(goal.get("key_results") or [], start=1):
            rows = aggregate_kr_rows(kr, rows_by_task)
            text = " ".join(
                [goal["goal_name"], kr["result_name"], kr.get("measure_standard", "")]
                + [action.get("action_name", "") for action in kr.get("actions") or []]
                + [
                    row["canonical_title"] + " " + " ".join(row["progress"].get("progress_facts") or [])
                    for row in rows
                ]
            )
            due_month = earliest_due_month(
                kr.get("measure_standard", "") + " " + " ".join(action["action_name"] for action in kr.get("actions") or [])
            )
            primary_count = sum(1 for row in rows if row["author_priority"] == "primary")
            light = detect_light(text, bool(rows), current_month, due_month, primary_count)
            card = {
                "card_id": f"{section_key}_kr_{kr_idx:02d}",
                "section_key": section_key,
                "goal_id": goal["goal_id"],
                "goal_name": goal["goal_name"],
                "result_id": kr["result_id"],
                "result_name": kr["result_name"],
                "measure_standard": normalize_text(kr.get("measure_standard", "")),
                "rows": rows,
                "progress": progress_lines(rows, limit=4),
                "light": light,
                "reason": kr_reason(light, kr, current_month),
            }
            kr_cards.append(card)

            for action_idx, action in enumerate(kr.get("actions") or [], start=1):
                action_rows = dedupe_rows(sort_rows(rows_by_task.get(action["action_id"], [])))
                action_text = action["action_name"] + " " + " ".join(
                    row["canonical_title"] + " " + " ".join(row["progress"].get("progress_facts") or [])
                    for row in action_rows
                )
                action_due = earliest_due_month(action["action_name"])
                action_primary = sum(1 for row in action_rows if row["author_priority"] == "primary")
                action_light = detect_light(action_text, bool(action_rows), current_month, action_due, action_primary)
                action_cards.append(
                    {
                        "card_id": f"4.{goal_idx}_action_{len([c for c in action_cards if c['goal_id']==goal['goal_id']])+1:02d}",
                        "section_key": f"4.{goal_idx}",
                        "goal_id": goal["goal_id"],
                        "goal_name": goal["goal_name"],
                        "result_id": kr["result_id"],
                        "result_name": kr["result_name"],
                        "action_id": action["action_id"],
                        "action_name": normalize_text(action["action_name"]),
                        "rows": action_rows,
                        "progress": progress_lines(action_rows, limit=4),
                        "light": action_light,
                        "reason": action_reason(action_light, action["action_name"], current_month),
                    }
                )
    return kr_cards, action_cards


def render_source_inventory(path: Path, rows: list[dict], stats: dict[str, int]) -> None:
    lines = [
        "# Source Inventory",
        "",
        "> 当前先通过 BP 关联接口拿 `bizId/reportId`，再通过工作协同详情接口补正文、回复与节点意见。",
        "> 月份归集口径：仅按汇报日期（report_time）按月取数。",
        "",
        f"- 命中原始工作汇报数：`{stats['raw_report_hit_count']}`",
        f"- 月份归集后候选汇报数：`{stats['candidate_report_count']}`",
        f"- 最终采纳证据数：`{stats['adopted_report_count']}`",
        f"- 本人主证据：`{stats['adopted_primary_report_count']}`",
        f"- 他人手动汇报：`{stats['adopted_other_manual_report_count']}`",
        f"- AI 汇报：`{stats['adopted_ai_report_count']}`",
        "",
        "| ref | title | author | task_id | priority | report_time | replies | nodes | attachment_status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['evidence_id']}` | {row['report_link_md'].replace('|', '\\|')} | {row['write_emp_name'] or ''} | `{row['task_id']}` | {row['author_priority']} | `{row.get('report_create_time') or ''}` | `{row.get('reply_count', 0)}` | `{row.get('node_count', 0)}` | `{row['attachment_fetch_status']}` |"
        )
    write_text(path, lines)


def render_evidence_ledger(path: Path, kr_cards: list[dict], stats: dict[str, int]) -> None:
    lines = [
        "# Evidence Ledger",
        "",
        "## 汇总",
        "",
        f"- 命中原始工作汇报：`{stats['raw_report_hit_count']}` 份",
        f"- 月份归集后候选汇报：`{stats['candidate_report_count']}` 份",
        f"- 最终采纳证据：`{stats['adopted_report_count']}` 份",
        f"- 本人主证据：`{stats['adopted_primary_report_count']}` 份",
        f"- 他人手动汇报：`{stats['adopted_other_manual_report_count']}` 份",
        f"- AI 汇报：`{stats['adopted_ai_report_count']}` 份",
        "",
    ]
    for card in kr_cards:
        lines.extend(
            [
                f"## {card['section_key']} / {card['result_name']}",
                "",
                "- 采用证据：",
            ]
        )
        if card["rows"]:
            for row in card["rows"][:6]:
                lines.append(
                    f"  - `{row['evidence_id']}` {row['report_link_md']} `{row['write_emp_name'] or ''} / {row['author_priority']}`"
                )
        else:
            lines.append("  - 未检索到稳定证据")
        lines.append("- 抽取事实：")
        for item in card["progress"] or ["待补充"]:
            lines.append(f"  - {item}")
        lines.extend(["- 结论：", f"  - {card['reason']}", ""])
    write_text(path, lines)


def render_card_file(path: Path, header: str, meta_lines: list[str], progress: list[str], rows: list[dict], light: str, reason: str) -> None:
    lines = [header, ""]
    lines.extend(meta_lines)
    lines.append("- 当前进展：")
    for item in progress or ["当前未检索到稳定进展事实。"]:
        lines.append(f"  - {item}")
    lines.append(f"- 证据：{evidence_md(rows, limit=6)}")
    lines.extend(status_block(light, reason))
    write_text(path, lines)


def render_cards_and_queue(run_dir: Path, anchor_map: list[dict], kr_cards: list[dict], action_cards: list[dict]) -> None:
    cards_root = run_dir / "04_cards"
    kr_dir = cards_root / "kr_cards"
    action_dir = cards_root / "action_cards"
    queue_dir = run_dir / "05_review_queue"
    cards_root.mkdir(parents=True, exist_ok=True)
    kr_dir.mkdir(parents=True, exist_ok=True)
    action_dir.mkdir(parents=True, exist_ok=True)
    queue_dir.mkdir(parents=True, exist_ok=True)

    review_items = []
    goal_by_id = {goal["goal_id"]: goal for goal in anchor_map}

    index_lines = ["# Cards Index", "", "## KR Cards", ""]
    for card in kr_cards:
        path = kr_dir / f"{sanitize_filename(card['card_id'])}.md"
        render_card_file(
            path,
            f"# {card['section_key']} / 关键成果卡",
            [
                f"- 卡片ID：`{card['card_id']}`",
                f"- 目标：`{card['goal_name']}`",
                f"- 关键成果：`{card['result_name']}`",
                f"- 衡量标准：{card['measure_standard'] or '待补充'}",
            ],
            card["progress"],
            card["rows"],
            card["light"],
            card["reason"],
        )
        index_lines.append(f"- [{card['card_id']}]({path}) `{card['light']}` {card['result_name']}")
        if card["light"] in {"🟡", "🔴", "⚫"}:
            review_items.append(
                {
                    "card_id": card["card_id"],
                    "card_path": path,
                    "anchor_type": "key_result",
                    "title": card["result_name"],
                    "light": card["light"],
                    "reason": card["reason"],
                }
            )

    index_lines.extend(["", "## Action Cards", ""])
    for card in action_cards:
        path = action_dir / f"{sanitize_filename(card['card_id'])}.md"
        render_card_file(
            path,
            f"# {card['section_key']} / 关键举措卡",
            [
                f"- 卡片ID：`{card['card_id']}`",
                f"- 对应目标：`{goal_by_id[card['goal_id']]['goal_name']}`",
                f"- 对应关键成果：`{card['result_name']}`",
                f"- 关键举措：`{card['action_name']}`",
            ],
            card["progress"],
            card["rows"],
            card["light"],
            card["reason"],
        )
        index_lines.append(f"- [{card['card_id']}]({path}) `{card['light']}` {card['action_name']}")
        if card["light"] in {"🟡", "🔴", "⚫"}:
            review_items.append(
                {
                    "card_id": card["card_id"],
                    "card_path": path,
                    "anchor_type": "key_action",
                    "title": card["action_name"],
                    "light": card["light"],
                    "reason": card["reason"],
                }
            )
    write_text(cards_root / "INDEX.md", index_lines)

    for item in review_items:
        queue_path = queue_dir / f"{sanitize_filename(item['card_id'])}_{LIGHT_NAME[item['light']]}.md"
        color = COLOR[item["light"]]
        lines = [
            f"# 复盘卡 / {item['title']}",
            "",
            f"- 来源卡片：[{item['card_id']}]({item['card_path']})",
            f"- 类型：`{item['anchor_type']}`",
            f"- 当前灯色：`{item['light']}`",
            f"- AI判断理由：{item['reason']}",
            "",
            f"<span style=\"color:{color}; font-weight:700;\">用户可修改任何内容，但该判断块必须补充解释。</span>",
            "",
            "- 用户需要回答：",
            "  - 是否同意当前判断（同意 / 不同意）？",
            "  - 若不同意：理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。",
            "  - 整改方案是什么？",
            "  - 承诺完成时间是什么？",
            "  - 下周期具体举措是什么？",
        ]
        if item["light"] == "⚫":
            lines.extend(
                [
                    "  - 黑灯类型（需人工复核后选择）：未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕。",
                    "  - 若未开展：下月/下周期准备怎么做？",
                    "  - 若已开展但未关联：需补关联的材料/汇报是什么？",
                    "  - 若体外开展但体系内无留痕：需补什么留痕、何时补齐？",
                    "  - 是否持续提醒至下周期？",
                ]
            )
        write_text(queue_path, lines)


def render_section_cards_summary(path: Path, anchor_map: list[dict], kr_cards: list[dict], action_cards: list[dict]) -> None:
    kr_by_goal = defaultdict(list)
    for card in kr_cards:
        kr_by_goal[card["goal_id"]].append(card)
    action_by_goal = defaultdict(list)
    for card in action_cards:
        action_by_goal[card["goal_id"]].append(card)

    lines = ["# Section Cards Summary", ""]
    for goal_idx, goal in enumerate(anchor_map, start=1):
        lines.extend([f"## 2.{goal_idx} {goal['goal_name']}", ""])
        for card in kr_by_goal.get(goal["goal_id"], []):
            lines.extend(
                [
                    f"### {card['result_name']}",
                    f"- 灯色：{card['light']}",
                    f"- 判断依据：{card['reason']}",
                    f"- 证据：{evidence_md(card['rows'])}",
                    "",
                ]
            )
        lines.extend([f"## 4.{goal_idx} {goal['goal_name']}", ""])
        for card in action_by_goal.get(goal["goal_id"], []):
            lines.extend(
                [
                    f"### {card['action_name']}",
                    f"- 灯色：{card['light']}",
                    f"- 判断依据：{card['reason']}",
                    f"- 证据：{evidence_md(card['rows'])}",
                    "",
                ]
            )
    write_text(path, lines)


def render_report(
    path: Path,
    bp_period: str,
    owner_name: str,
    group_id: str,
    report_month: str,
    stats: dict[str, int],
    anchor_map: list[dict],
    kr_cards: list[dict],
    action_cards: list[dict],
) -> None:
    goal_by_id = {goal["goal_id"]: goal for goal in anchor_map}
    overall = overall_light(kr_cards)
    top_progress = [card for card in kr_cards if card["light"] in {"🟢", "🟡"}]
    top_progress.sort(key=lambda card: (-len(card["rows"]), card["section_key"]))
    top_progress = top_progress[:3]
    concern_cards = [card for card in kr_cards if card["light"] in {"🟡", "🔴", "⚫"}][:5]

    lines = [
        f"# {owner_name} {report_month.replace('-', '年', 1)}月月报（AI基准草稿）（版本二）",
        "",
        f"> 周期：`{bp_period}`",
        f"> 节点：`{owner_name}`",
        f"> groupId：`{group_id}`",
        "> 取数方式：按 `periodId + groupId/BP组织节点ID + report_month` 直接取 BP、成果、举措与关联汇报",
        "> 月份归集口径：仅按汇报日期（report_time）按汇报月份取数",
        "> 汇报链路：BP 关联接口返回 `bizId/reportId`，再调用工作协同详情接口获取正文、回复与节点处理意见",
        "> 证据说明：本稿中的汇报引用均直接指向在线汇报",
        "> 灯规则版本：`版本二（黄灯必须整改，但绿灯和黄灯标准均放宽）`",
        "",
        "## 1. 汇报综述",
        "",
        "- **本月参考工作汇报数：**",
        f"  命中原始工作汇报 `{stats['raw_report_hit_count']}` 份，月份归集后候选 `{stats['candidate_report_count']}` 份，最终采纳 `{stats['adopted_report_count']}` 份，其中本人主证据 `{stats['adopted_primary_report_count']}` 份、他人手动汇报 `{stats['adopted_other_manual_report_count']}` 份、AI 汇报 `{stats['adopted_ai_report_count']}` 份。",
        "",
        "- **本月总体判断：**",
        f"  {overall} 本月整体判断依据关键成果推进证据、关键举措留痕以及回复/节点处理意见综合形成。",
    ]
    lines.extend("  " + line for line in status_block(overall, "整体判断综合考虑关键成果推进证据、举措留痕与黑灯缺口；当前仍存在部分需重点跟踪事项。"))
    lines.extend(["", "- **本月最关键的进展：**"])
    for card in top_progress:
        lines.append(f"  - {card['result_name']}：{'；'.join(card['progress'][:2]) or '已形成推进动作'}。证据：{evidence_md(card['rows'], limit=2)}")
    if not top_progress:
        lines.append("  - 本月未检索到足以支撑关键成果推进判断的稳定证据。")
    lines.extend(["", "- **本月最需要关注的问题：**"])
    for card in concern_cards:
        lines.append(f"  - {card['result_name']}：{card['reason']}")
    lines.extend(["", "## 2. BP目标承接与对齐情况", ""])

    kr_by_goal = defaultdict(list)
    for card in kr_cards:
        kr_by_goal[card["goal_id"]].append(card)
    for idx, goal in enumerate(anchor_map, start=1):
        section_key = f"2.{idx}"
        lines.extend([f"### {section_key} {goal['goal_name']}", "", f"**对标BP：** {goal['goal_name']}", "", "**本月承接重点：**"])
        goal_rows = dedupe_rows(sort_rows([row for card in kr_by_goal[goal['goal_id']] for row in card["rows"]]))
        focus_items = progress_lines(goal_rows, limit=2) or ["当前更多体现为年度前期准备，尚未形成稳定月度事实。"]
        for item in focus_items:
            lines.append(f"- {item}")
        lines.append("")
        for card in kr_by_goal[goal["goal_id"]]:
            lines.extend(
                [
                    f"**关键成果：** {card['result_name']}",
                    f"- 衡量标准：{card['measure_standard'] or '待补充'}",
                    "- 当前状态：",
                ]
            )
            for item in card["progress"] or ["当前未检索到稳定进展事实。"]:
                lines.append(f"  - {item}")
            lines.append(f"- 证据：{evidence_md(card['rows'])}")
            lines.extend(status_block(card["light"], card["reason"]))
            lines.append("")

    non_black_cards = [card for card in kr_cards if card["light"] != "⚫"]
    lines.extend(["## 3. 核心结果与经营表现", ""])
    if not non_black_cards:
        lines.extend(
            [
                "### 3.1 本月缺少可稳定支撑结果判断的证据",
                "",
                "- 本月结果：当前未形成可稳定支撑结果判断的有效证据。",
                "- 结果判断：",
                f"  - {result_judgment_text({'light': '⚫'})}",
                "",
            ]
        )
    else:
        for idx, card in enumerate(non_black_cards, start=1):
            lines.extend(
                [
                    f"### 3.{idx} {card['result_name']}",
                    "",
                    f"- 组织 BP 锚点：`{goal_by_id[card['goal_id']]['goal_name']}`",
                    f"- 个人 BP 锚点：`{card['result_name']}`",
                    "- 本月成果：",
                ]
            )
            for item in card["progress"][:3] or ["待补充"]:
                lines.append(f"  - {item}")
            lines.extend(
                [
                    f"- 衡量标准 / 指标变化：{card['measure_standard'] or '待补充'}",
                    "- 结果判断：",
                    f"  - {result_judgment_text(card)}",
                    f"- 证据：{evidence_md(card['rows'])}",
                    "",
                ]
            )

    lines.extend(["## 4. 关键举措推进情况", ""])
    actions_by_goal = defaultdict(list)
    for card in action_cards:
        actions_by_goal[card["goal_id"]].append(card)
    for idx, goal in enumerate(anchor_map, start=1):
        section_no = f"4.{idx}"
        lines.extend([f"### {section_no} {goal['goal_name']}", ""])
        for action_idx, card in enumerate(actions_by_goal.get(goal["goal_id"], []), start=1):
            block_no = f"{section_no}.{action_idx}"
            lines.extend(
                [
                    f"#### {block_no} {card['action_name']}",
                    "",
                    f"- 对应关键成果：`{card['result_name']}`",
                    "- 当前进展：",
                ]
            )
            for item in card["progress"] or ["当前未检索到稳定进展事实。"]:
                lines.append(f"  - {item}")
            lines.append(f"- 证据：{evidence_md(card['rows'])}")
            lines.extend(status_block(card["light"], card["reason"]))
            lines.append("")

    lines.extend(["## 5. 问题、偏差与原因分析", ""])
    issue_cards = [card for card in kr_cards if card["light"] in {"🟡", "🔴", "⚫"}]
    if not issue_cards:
        lines.extend(["- 本月未识别出需要单列的问题或偏差。", ""])
    else:
        for idx, card in enumerate(issue_cards, start=1):
            lines.extend(
                [
                    f"### 5.{idx} {card['result_name']}",
                    "",
                    f"- 对应 BP：`{goal_by_id[card['goal_id']]['goal_name']}`",
                    f"- 当前问题：{card['reason']}",
                    f"- 原因分析：{card['reason']}",
                    "- 影响范围：影响后续对该关键成果的达成判断与节奏控制。",
                ]
            )
            lines.extend(status_block(card["light"], card["reason"]))
            lines.append("")

    lines.extend(["## 6. 风险预警与资源需求", ""])
    if not issue_cards:
        lines.extend(["- 当前未识别出需单列的风险预警。", ""])
    else:
        for idx, card in enumerate(issue_cards[:4], start=1):
            lines.extend(
                [
                    f"### 6.{idx} {card['result_name']} 风险",
                    "",
                    f"- 风险内容：{card['reason']}",
                    f"- 对应 BP：`{goal_by_id[card['goal_id']]['goal_name']}`",
                    f"- 风险等级：{'高' if card['light'] == '🔴' else '中' if card['light'] == '🟡' else '待人工确认'}",
                    "- 当前应对动作：待补充",
                    "- 所需支持 / 资源：待补充",
                ]
            )
            lines.extend(status_block(card["light"], card["reason"]))
            lines.append("")

    lines.extend(["## 7. 下月重点安排", ""])
    if issue_cards:
        for card in issue_cards[:5]:
            if card["light"] == "⚫":
                lines.append(f"- 优先完成“{card['result_name']}”的人工复核、补关联或补留痕，消灭黑灯。")
            elif card["light"] == "🟡":
                lines.append(f"- 针对“{card['result_name']}”落实整改动作，降低对后续结果达成的实质压力。")
            else:
                lines.append(f"- 针对“{card['result_name']}”立即开展纠偏和资源协调。")
    else:
        lines.append("- 按既定节奏推进当前工作安排。")

    lines.extend(["", "## 8. 需决策 / 需协同事项", ""])
    if issue_cards:
        lines.append("- 需拍板事项：围绕黄灯 / 红灯项明确节奏、资源与优先级。")
        lines.append("- 需协调事项：请相关协同部门与主责人补齐关键留痕、确认行动边界。")
        lines.append("- 需要支持事项：对黑灯项明确是未开展、未关联还是体外无留痕，并给出后续处理要求。")
    else:
        lines.append("- 当前未识别出需要单列的拍板或协同事项。")

    write_text(path, lines)


def write_intake(path: Path, bp_period: str, period_id: str, report_month: str, owner_name: str, group_id: str, org_path: str) -> None:
    lines = [
        f"bp_period: {bp_period}",
        f'period_id: "{period_id}"',
        f"report_month: {report_month}",
        f"node_name: {owner_name}",
        f'group_id: "{group_id}"',
        f"org_path: {org_path}",
        "template_path: /Users/hou/Documents/UGit/BP- writer/bp-monthly-report-skill/assets/P001-T001-MONTH-TPL-01_月报模板_v1.md",
        "spec_path: /Users/hou/Documents/UGit/BP- writer/bp-monthly-report-skill/assets/人力资源中心_月报填写规范_组织示例_v1.md",
        "month_attribution_mode: report_time",
        "scheme: version2",
    ]
    write_text(path, lines)


def run_one(app_key: str, bp_period: str, period_id: str, report_month: str, owner_name: str, group_id: str, org_path: str, root_dir: Path) -> Path:
    run_dir = root_dir / f"{bp_period}_{owner_name}" / report_month
    run_dir.mkdir(parents=True, exist_ok=True)
    write_intake(run_dir / "00_intake.yaml", bp_period, period_id, report_month, owner_name, group_id, org_path)

    anchor_map = build_anchor_map(app_key, period_id, group_id)
    (run_dir / "01_bp_anchor_map.yaml").write_text(json.dumps(anchor_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    all_task_ids = []
    for goal in anchor_map:
        all_task_ids.append(goal["goal_id"])
        for kr in goal.get("key_results") or []:
            all_task_ids.append(kr["result_id"])
            for action in kr.get("actions") or []:
                all_task_ids.append(action["action_id"])
    all_task_ids = list(dict.fromkeys(all_task_ids))

    rows, rows_by_task, stats = fetch_task_report_rows(
        app_key=app_key,
        report_month=report_month,
        owner_name=owner_name,
        task_ids=all_task_ids,
        page_size=100,
    )

    manifest_dir = run_dir / "_manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    from collect_bp_month_evidence import write_manifest_md  # local import to avoid cycle confusion

    write_manifest_md(manifest_dir / "manifest.md", rows, report_month, owner_name, stats)

    current_month = int(report_month.split("-")[1])
    kr_cards, action_cards = build_cards(anchor_map, rows_by_task, current_month)

    render_source_inventory(run_dir / "02_source_inventory.md", rows, stats)
    render_evidence_ledger(run_dir / "03_evidence_ledger.md", kr_cards, stats)
    render_cards_and_queue(run_dir, anchor_map, kr_cards, action_cards)
    render_section_cards_summary(run_dir / "04_section_cards.md", anchor_map, kr_cards, action_cards)

    baseline_path = run_dir / "05_ai_baseline_report_scheme_v2.md"
    render_report(baseline_path, bp_period, owner_name, group_id, report_month, stats, anchor_map, kr_cards, action_cards)

    review_path = run_dir / "07_user_review_report.md"
    review_lines = baseline_path.read_text(encoding="utf-8").splitlines()
    if review_lines and review_lines[0].startswith("# "):
        review_lines[0] = review_lines[0].replace("（AI基准草稿）（版本二）", "（用户复盘版）（版本二）")
    review_lines.insert(1, "")
    review_lines.insert(2, "> 说明：本文件为用户复盘版底稿，用户可以修改任何内容；但所有 `🟡 / 🔴 / ⚫` 判断块都必须补充解释。")
    write_text(review_path, review_lines)
    return baseline_path


def parse_specs(app_key: str, period_id: str, person_specs: list[str], group_ids: list[str]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for spec in person_specs:
        parts = spec.split("|")
        if len(parts) == 3:
            out.append((parts[0], parts[1], parts[2]))
        elif len(parts) == 2:
            name, group_id = parts
            resolved_name, org_path = resolve_group_meta(app_key, period_id, group_id)
            out.append((name or resolved_name, group_id, org_path))
        else:
            group_id = spec
            name, org_path = resolve_group_meta(app_key, period_id, group_id)
            out.append((name, group_id, org_path))
    for group_id in group_ids:
        name, org_path = resolve_group_meta(app_key, period_id, group_id)
        out.append((name, group_id, org_path))
    deduped = []
    seen = set()
    for item in out:
        key = item[1]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-key", required=True)
    parser.add_argument("--bp-period", required=True)
    parser.add_argument("--period-id", required=True)
    parser.add_argument("--report-month", required=True)
    parser.add_argument("--person", action="append", default=[], help="name|groupId|orgPath or name|groupId or groupId")
    parser.add_argument("--group-id", action="append", default=[], help="Direct BP group id")
    parser.add_argument("--root-dir", required=True)
    args = parser.parse_args()

    specs = parse_specs(args.app_key, args.period_id, args.person or [], args.group_id or [])
    if not specs:
        raise SystemExit("Need at least one --person or --group-id")

    outputs = []
    for name, group_id, org_path in specs:
        outputs.append(
            {
                "name": name,
                "groupId": group_id,
                "report": str(
                    run_one(
                        app_key=args.app_key,
                        bp_period=args.bp_period,
                        period_id=args.period_id,
                        report_month=args.report_month,
                        owner_name=name,
                        group_id=group_id,
                        org_path=org_path,
                        root_dir=Path(args.root_dir),
                    )
                ),
            }
        )
    print(json.dumps(outputs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
