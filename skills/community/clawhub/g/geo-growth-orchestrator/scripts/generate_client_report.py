#!/usr/bin/env python3
"""Generate client-facing GEO delivery reports from orchestrator JSON outputs.

Usage:
    python3 scripts/generate_client_report.py geo_orchestrator_v2 --output-dir geo_orchestrator_v2
    python3 scripts/generate_client_report.py workflow_state.json --output client_delivery_report.md
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


KNOWN_FILES = {
    "workflow_state": "workflow_state.json",
    "brand_profile": "brand_profile.json",
    "geo_audit_report": "geo_audit_report.json",
    "content_gap_report": "content_gap_report.json",
    "content_tasks": "content_tasks.json",
    "platform_drafts": "platform_drafts.json",
    "publish_plan": "publish_plan.json",
}

PLATFORM_LABELS = {
    "zhihu": "知乎",
    "toutiao": "今日头条",
    "csdn": "CSDN",
    "juejin": "掘金",
    "website": "官网",
    "generic": "通用内容",
    "other": "其他平台",
}

INTERNAL_PATTERNS = [
    (r"\bblocked\b", "建议补充资料后发布"),
    (r"\bmanual_check\b", "人工复核记录"),
    (r"\binferred_estimate\b", "初步判断"),
    (r"\bunverified_assumption\b", "待补充资料"),
    (r"\bworkflow_state\b", "工作流结果"),
    (r"\bschema\b", "结构"),
    (r"DeepSeek API\s*未配置", ""),
    (r"API key\s*未配置", ""),
    (r"API\s*未配置", ""),
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return "、".join(as_text(item) for item in value if as_text(item))
    if isinstance(value, dict):
        return "、".join(as_text(item) for item in value.values() if as_text(item))
    return str(value)


def sanitize_client_text(value: Any) -> str:
    text = as_text(value).strip()
    for pattern, replacement in INTERNAL_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def truncate(text: str, length: int = 90) -> str:
    text = sanitize_client_text(text)
    if len(text) <= length:
        return text
    return text[: length - 1].rstrip() + "…"


def load_bundle(input_path: Path) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "workflow_state": {},
        "brand_profile": {},
        "geo_audit_report": [],
        "content_gap_report": {},
        "content_tasks": [],
        "platform_drafts": [],
        "publish_plan": {},
    }

    if input_path.is_dir():
        for key, filename in KNOWN_FILES.items():
            file_path = input_path / filename
            if file_path.exists():
                bundle[key] = load_json(file_path)
    else:
        payload = load_json(input_path)
        if isinstance(payload, dict):
            bundle["workflow_state"] = payload
            for key in bundle:
                if key in payload:
                    bundle[key] = payload[key]
            if "brand_profile" in payload and isinstance(payload["brand_profile"], dict):
                bundle["brand_profile"] = payload["brand_profile"]
        elif isinstance(payload, list):
            bundle["platform_drafts"] = payload

    workflow_state = bundle.get("workflow_state") or {}
    if isinstance(workflow_state, dict):
        for key in ("brand_profile", "geo_audit_report", "content_gap_report", "content_tasks", "platform_drafts", "publish_plan"):
            if not bundle.get(key) and workflow_state.get(key):
                bundle[key] = workflow_state[key]

    return bundle


def brand_name(bundle: dict[str, Any]) -> str:
    profile = bundle.get("brand_profile") or {}
    if isinstance(profile, dict):
        return sanitize_client_text(profile.get("brand_name")) or "品牌"
    return "品牌"


def target_keywords(bundle: dict[str, Any]) -> list[str]:
    values: list[str] = []
    profile = bundle.get("brand_profile") or {}
    if isinstance(profile, dict):
        values.extend(as_list(profile.get("target_keywords")))
    for item in as_list(bundle.get("geo_audit_report")):
        if isinstance(item, dict) and item.get("keyword"):
            values.append(as_text(item.get("keyword")))
    for task in as_list(bundle.get("content_tasks")):
        if isinstance(task, dict) and task.get("keyword"):
            values.append(as_text(task.get("keyword")))
    return dedupe([sanitize_client_text(item) for item in values if sanitize_client_text(item)])


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def platform_label(platform: Any) -> str:
    value = as_text(platform).lower()
    return PLATFORM_LABELS.get(value, sanitize_client_text(platform) or "其他平台")


def group_by_platform(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        platform = as_text(item.get("platform") or item.get("target_platform") or "other").lower()
        grouped.setdefault(platform, []).append(item)
    return grouped


def task_by_id(tasks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {as_text(task.get("task_id")): task for task in tasks if as_text(task.get("task_id"))}


def plan_item_by_draft_id(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items = plan.get("items") if isinstance(plan, dict) else []
    return {as_text(item.get("draft_id")): item for item in as_list(items) if isinstance(item, dict) and as_text(item.get("draft_id"))}


def draft_keyword(draft: dict[str, Any], task: dict[str, Any]) -> str:
    return sanitize_client_text(draft.get("keyword") or draft.get("target_keyword") or task.get("keyword") or "核心关键词")


def draft_role(draft: dict[str, Any], task: dict[str, Any]) -> str:
    value = (
        draft.get("content_role")
        or draft.get("content_angle")
        or task.get("content_angle")
        or task.get("source_gap")
        or "补充用户决策所需的关键信息"
    )
    return truncate(value, 80)


def draft_summary(draft: dict[str, Any], task: dict[str, Any]) -> str:
    value = (
        draft.get("summary")
        or draft.get("abstract")
        or draft.get("excerpt")
        or draft.get("body")
        or task.get("content_angle")
        or "围绕用户关心的问题，补充清晰的品牌答案和出行/选型信息。"
    )
    return truncate(value, 110)


def collect_publish_notes(*items: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        for key in ("blocking_items", "fact_check_items", "review_notes", "preconditions"):
            for value in as_list(item.get(key)):
                text = sanitize_client_text(value)
                if text:
                    notes.append(text)
        gate = item.get("publish_gate")
        if isinstance(gate, dict):
            for value in as_list(gate.get("blocking_items")) + as_list(gate.get("preconditions")):
                text = sanitize_client_text(value)
                if text:
                    notes.append(text)
    return dedupe(notes)


def friendly_confirmation_note(value: str) -> str:
    text = sanitize_client_text(value)
    for prefix in ("发布前人工审核并确认", "发布前人工审核", "发布前确认", "人工审核并确认", "人工审核", "确认"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip("：: ，,。")
    return text or sanitize_client_text(value)


def publish_advice(draft: dict[str, Any], task: dict[str, Any], plan_item: dict[str, Any]) -> str:
    notes = [friendly_confirmation_note(note) for note in collect_publish_notes(draft, task, plan_item)]
    notes = dedupe([note for note in notes if note])
    readiness = as_text(draft.get("publish_readiness") or plan_item.get("publish_readiness") or task.get("publish_gate", {}).get("readiness"))
    if "blocked" in readiness.lower() or plan_item.get("blocking_items") or draft.get("blocking_items"):
        if notes:
            return f"建议补充{truncate('、'.join(notes), 45)}后发布"
        return "建议补充关键资料后发布"
    if notes:
        return f"人工审核，并确认{truncate('、'.join(notes), 42)}后发布"
    return "人工审核后可发布"


def draft_rows(bundle: dict[str, Any]) -> list[dict[str, str]]:
    drafts = [item for item in as_list(bundle.get("platform_drafts")) if isinstance(item, dict)]
    tasks = [item for item in as_list(bundle.get("content_tasks")) if isinstance(item, dict)]
    task_lookup = task_by_id(tasks)
    plan_lookup = plan_item_by_draft_id(bundle.get("publish_plan") or {})
    rows: list[dict[str, str]] = []

    source_items = drafts
    if not source_items:
        source_items = tasks

    for item in source_items:
        task = task_lookup.get(as_text(item.get("task_id")), item if item in tasks else {})
        plan_item = plan_lookup.get(as_text(item.get("draft_id")), {})
        rows.append(
            {
                "platform": as_text(item.get("platform") or task.get("platform") or "other").lower(),
                "title": sanitize_client_text(item.get("title") or task.get("title") or "待定标题"),
                "keyword": draft_keyword(item, task),
                "role": draft_role(item, task),
                "summary": draft_summary(item, task),
                "advice": publish_advice(item, task, plan_item),
                "priority": as_text(item.get("priority") or task.get("priority") or plan_item.get("priority") or "medium"),
            }
        )
    return rows


def priority_rank(value: str) -> int:
    return {"high": 0, "urgent": 0, "p0": 0, "medium": 1, "normal": 1, "low": 2}.get(value.lower(), 1)


def content_asset_markdown(rows: list[dict[str, str]]) -> str:
    grouped = group_by_platform([dict(row) for row in rows])
    sections = ["# 内容资产摘要", ""]
    for platform in ("zhihu", "toutiao", "csdn", "juejin", "website", "generic", "other"):
        items = grouped.get(platform, [])
        if not items:
            continue
        sections.append(f"## {platform_label(platform)}内容草稿")
        sections.append("")
        sections.append("| 标题 | 目标关键词 | 内容摘要 | 内容作用 | 发布建议 |")
        sections.append("|---|---|---|---|---|")
        for row in items:
            sections.append(f"| {row['title']} | {row['keyword']} | {row['summary']} | {row['role']} | {row['advice']} |")
        sections.append("")
    if len(sections) == 2:
        sections.extend(["暂未生成平台草稿。", ""])
    return "\n".join(sections).rstrip() + "\n"


def supplement_items(bundle: dict[str, Any], rows: list[dict[str, str]]) -> list[tuple[str, str, str]]:
    collected: list[str] = []
    plan = bundle.get("publish_plan") or {}
    if isinstance(plan, dict):
        for item in as_list(plan.get("blocking_items")):
            if isinstance(item, dict):
                collected.append(sanitize_client_text(item.get("item") or item.get("reason")))
            else:
                collected.append(sanitize_client_text(item))
        for item in as_list(plan.get("items")):
            if isinstance(item, dict):
                collected.extend(collect_publish_notes(item))

    for task in as_list(bundle.get("content_tasks")):
        if isinstance(task, dict):
            collected.extend(sanitize_client_text(value) for value in as_list(task.get("fact_dependencies")))
            gate = task.get("publish_gate")
            if isinstance(gate, dict):
                collected.extend(sanitize_client_text(value) for value in as_list(gate.get("blocking_items")))
                collected.extend(sanitize_client_text(value) for value in as_list(gate.get("preconditions")))

    for row in rows:
        if "补充" in row["advice"] or "确认" in row["advice"]:
            collected.append(row["advice"])

    normalized = dedupe([friendly_confirmation_note(item) for item in collected if item])
    defaults = [
        ("门票价格", "用户做出行或购买决策时最关心", "攻略文、FAQ、知乎问答"),
        ("营业时间", "影响用户是否立即行动", "头条攻略、AI 搜索回答"),
        ("项目安全说明", "亲子游、高空项目或专业服务需要信任背书", "亲子游内容、FAQ"),
        ("真实用户评价或案例", "增强推荐理由和内容可信度", "推荐理由、案例内容"),
        ("交通方式或服务流程", "降低用户决策成本", "攻略文、FAQ"),
    ]
    if not normalized:
        return defaults

    rows_out: list[tuple[str, str, str]] = []
    for item in normalized[:8]:
        label = item
        reason = "让内容表达更具体、更容易被用户采信"
        usage = "平台草稿、FAQ、发布前审核"
        rows_out.append((label, reason, usage))
    return rows_out


def growth_opportunities(bundle: dict[str, Any], keywords: list[str]) -> list[str]:
    report = bundle.get("content_gap_report") or {}
    opportunities: list[str] = []
    if isinstance(report, dict):
        for gap in as_list(report.get("content_gaps")):
            if isinstance(gap, dict):
                keyword = sanitize_client_text(gap.get("keyword"))
                recommended = sanitize_client_text(gap.get("recommended_content") or gap.get("gap_type") or gap.get("evidence"))
                if keyword or recommended:
                    opportunities.append(f"用户关心“{keyword or '核心问题'}”，建议补充{recommended or '更清晰的解释和决策信息'}。")
    if opportunities:
        return dedupe(opportunities)[:6]

    if keywords:
        return [
            f"围绕“{keywords[0]}”这类问题，需要让用户更快看到品牌的核心推荐理由。",
            "用户在做决策时更需要结构化答案，建议补充 FAQ、攻略、对比型内容和真实问题回应。",
            "平台内容应覆盖“适合谁、为什么值得选、怎么行动、有哪些注意事项”四类信息。",
        ]
    return [
        "用户需要更明确的品牌介绍、适用场景和决策理由。",
        "建议补充 FAQ、攻略、对比型内容和真实问题回应，让 AI 搜索更容易引用清晰答案。",
    ]


def deliverable_table(rows: list[dict[str, str]], platforms: list[str]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["platform"]] = counts.get(row["platform"], 0) + 1
    zhihu_count = counts.get("zhihu", 0)
    toutiao_count = counts.get("toutiao", 0)
    return "\n".join(
        [
            "| 交付项 | 本轮结果 | 客户可直接使用什么 |",
            "|---|---|---|",
            "| 品牌信息梳理 | 已完成 | 可作为后续 AI 内容和客服知识库基础 |",
            "| AI 搜索诊断 | 已完成 | 明确知道哪些关键词需要补内容 |",
            "| 内容机会分析 | 已完成 | 得到优先内容方向 |",
            f"| 知乎草稿 | {zhihu_count} 篇 | 可人工审核后发布 |",
            f"| 今日头条草稿 | {toutiao_count} 篇 | 可人工审核后发布 |",
            "| 发布计划 | 已完成 | 可按建议节奏执行 |",
        ]
    )


def priority_plan_markdown(rows: list[dict[str, str]], supplement: list[tuple[str, str, str]]) -> str:
    if not rows:
        return "暂未生成平台草稿，建议先完成首批内容资产后再安排发布顺序。\n"
    sorted_rows = sorted(rows, key=lambda row: (priority_rank(row["priority"]), row["platform"], row["title"]))
    lines: list[str] = []
    for index, row in enumerate(sorted_rows[:6], start=1):
        confirm = row["advice"].replace("人工审核并确认", "").replace("后发布", "").strip("。")
        confirm = confirm.replace("人工审核，并确认", "").replace("建议补充", "").strip("：: ，,。")
        if confirm in ("人工审核", "人工审核后可发布", ""):
            confirm = "标题、联系方式和品牌事实"
        window = "信息确认后 24 小时内发布" if index == 1 else "第一篇发布后 1 到 2 天内发布"
        reason = row["role"].rstrip("。；;，,")
        lines.extend(
            [
                f"{index}. 《{row['title']}》",
                f"   平台：{platform_label(row['platform'])}",
                f"   为什么先发：{reason}，适合覆盖“{row['keyword']}”相关用户问题。",
                f"   发布前需要确认：{confirm}",
                f"   建议发布时间窗口：{window}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def publish_plan_client_markdown(rows: list[dict[str, str]], supplement: list[tuple[str, str, str]]) -> str:
    lines = ["# 客户版发布计划", "", "## 推荐优先发布顺序", "", priority_plan_markdown(rows, supplement).rstrip(), ""]
    lines.extend(["## 为了让内容更容易被用户和 AI 搜索采信，建议补充以下资料", ""])
    lines.extend(["| 资料 | 为什么重要 | 用在哪里 |", "|---|---|---|"])
    for item, reason, usage in supplement:
        lines.append(f"| {sanitize_client_text(item)} | {sanitize_client_text(reason)} | {sanitize_client_text(usage)} |")
    lines.extend(
        [
            "",
            "## 下一步执行计划",
            "",
            "### 立即可做",
            "",
            "- 审核已生成草稿。",
            "- 确认标题、联系方式和品牌事实。",
            "- 发布不依赖关键价格或时间信息的内容。",
            "- 补充价格、营业时间、安全说明、案例或交通方式等资料。",
            "",
            "### 3 天内",
            "",
            "- 发布第一批优先内容。",
            "- 整理评论区和私信里的高频问题。",
            "- 把新增问题补充进 FAQ 和下一批选题。",
            "",
            "### 2 周后",
            "",
            "- 再次检测目标 AI 搜索环境中的品牌提及变化。",
            "- 对比品牌描述是否更准确。",
            "- 根据新问题生成第二批内容。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def client_report_markdown(bundle: dict[str, Any]) -> tuple[str, str, str]:
    name = brand_name(bundle)
    keywords = target_keywords(bundle)
    rows = draft_rows(bundle)
    supplement = supplement_items(bundle, rows)
    opportunities = growth_opportunities(bundle, keywords)
    keyword_text = "、".join(f"“{keyword}”" for keyword in keywords[:6]) if keywords else "核心关键词"

    report: list[str] = [
        f"# {name} AI 搜索可见度与内容增长交付报告",
        "",
        "## 1. 本轮交付结论",
        "",
        f"本轮已围绕 {keyword_text} 等关键词，完成品牌信息梳理、AI 搜索可见度诊断、内容机会分析，并形成首批平台内容资产。",
        "当前最重要的机会是：让用户在搜索相关问题时，更快看到清晰、可信、可行动的品牌答案。",
        f"本轮已整理出 {len(rows)} 个内容资产或内容方向，可用于知乎、今日头条等平台的人工审核发布。",
        "客户下一步只需要确认关键事实、审核草稿并按建议顺序发布，2 周后再复盘 AI 搜索和平台反馈变化。",
        "",
        "## 2. 一眼看到本轮成果",
        "",
        deliverable_table(rows, []),
        "",
        "## 3. AI 搜索中发现的增长机会",
        "",
    ]
    report.extend(f"- {item}" for item in opportunities)
    report.extend(["", "## 4. 本轮生成的内容资产", ""])

    grouped_rows = group_by_platform([dict(row) for row in rows])
    for platform in ("zhihu", "toutiao", "csdn", "juejin", "website", "generic", "other"):
        items = grouped_rows.get(platform, [])
        if not items:
            continue
        report.extend([f"### {platform_label(platform)}内容草稿", "", "| 标题 | 目标关键词 | 内容作用 | 发布建议 |", "|---|---|---|---|"])
        for row in items:
            report.append(f"| {row['title']} | {row['keyword']} | {row['role']} | {row['advice']} |")
        report.append("")
        for row in items:
            report.append(f"内容摘要：{row['summary']}")
        report.append("")

    if not rows:
        report.extend(["暂未生成平台草稿，建议先完成首批内容资产。", ""])

    report.extend(["## 5. 推荐优先发布顺序", "", priority_plan_markdown(rows, supplement).rstrip(), ""])
    report.extend(["## 6. 为了让内容更容易被用户和 AI 搜索采信，建议补充以下资料", ""])
    report.extend(["| 资料 | 为什么重要 | 用在哪里 |", "|---|---|---|"])
    for item, reason, usage in supplement:
        report.append(f"| {sanitize_client_text(item)} | {sanitize_client_text(reason)} | {sanitize_client_text(usage)} |")

    report.extend(
        [
            "",
            "## 7. 预计改善方向",
            "",
            "- 提升品牌在目标关键词相关问题中的内容覆盖度。",
            "- 增加 AI 搜索可引用的结构化内容。",
            "- 让用户常问问题拥有更清晰的品牌答案。",
            "- 为知乎、今日头条、小红书、抖音等后续内容分发打基础。",
            "- 为 AI 客服和官网 FAQ 积累标准答案。",
            "",
            "## 8. 下一步执行计划",
            "",
            "### 立即可做",
            "",
            "- 审核已生成草稿。",
            "- 确认标题和联系方式。",
            "- 发布不依赖关键价格或时间信息的内容。",
            "- 补充价格、营业时间、安全说明、案例或交通方式等资料。",
            "",
            "### 3 天内",
            "",
            "- 发布第一批知乎/今日头条内容。",
            "- 整理评论和用户问题。",
            "- 补充 FAQ。",
            "",
            "### 2 周后",
            "",
            "- 再次检测目标 AI 搜索环境中的品牌提及变化。",
            "- 对比品牌是否被更准确提及。",
            "- 根据新问题生成第二批内容。",
            "",
            "## 9. 附录：交付文件",
            "",
            "- 品牌内容基础资料",
            "- AI 搜索诊断摘要",
            "- 内容机会清单",
            "- 知乎内容草稿",
            "- 今日头条内容草稿",
            "- 发布计划",
        ]
    )
    client_report = "\n".join(report).rstrip() + "\n"
    return client_report, content_asset_markdown(rows), publish_plan_client_markdown(rows, supplement)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate client-facing GEO delivery reports.")
    parser.add_argument("input", help="Input workflow_state JSON file or directory containing orchestrator JSON outputs.")
    parser.add_argument("--output", default=None, help="Output path for client_delivery_report.md.")
    parser.add_argument("--output-dir", default=None, help="Directory for client_delivery_report.md, content_asset_summary.md, and publish_plan_client.md.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}")
        return 2

    bundle = load_bundle(input_path)
    client_report, asset_summary, publish_plan = client_report_markdown(bundle)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        client_path = output_dir / "client_delivery_report.md"
        asset_path = output_dir / "content_asset_summary.md"
        publish_path = output_dir / "publish_plan_client.md"
    else:
        client_path = Path(args.output or "client_delivery_report.md")
        asset_path = client_path.with_name("content_asset_summary.md")
        publish_path = client_path.with_name("publish_plan_client.md")

    client_path.write_text(client_report, encoding="utf-8")
    asset_path.write_text(asset_summary, encoding="utf-8")
    publish_path.write_text(publish_plan, encoding="utf-8")
    print(f"Wrote {client_path}")
    print(f"Wrote {asset_path}")
    print(f"Wrote {publish_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
