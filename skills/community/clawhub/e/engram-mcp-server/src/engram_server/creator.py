from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_MISSING_MARKERS = {
    "",
    "没有",
    "你来",
    "都可以",
    "随便",
    "无",
    "none",
    "n/a",
    "na",
}


def _is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in _MISSING_MARKERS


def _normalize_name(name: str | None, topic: str) -> str:
    raw = topic if _is_missing(name) else str(name)
    candidate = re.sub(r"[\\/]+", "-", raw.strip())
    candidate = re.sub(r"\s+", "-", candidate)
    candidate = candidate.strip("-.")
    if not candidate or candidate in {".", ".."}:
        return "new-engram"
    return candidate


def _extract_insights(text: str | None) -> list[str]:
    if _is_missing(text):
        return []
    parts = re.split(r"[。\n！？!?；;]+", text or "")
    insights: list[str] = []
    for part in parts:
        line = part.strip(" -\t")
        if len(line) < 6:
            continue
        insights.append(line)
    return insights[:6]


def _render_knowledge_index(
    knowledge_items: list[dict[str, str]],
) -> tuple[str, dict[str, str]]:
    top_level: list[dict[str, str]] = []
    grouped: dict[str, list[dict[str, str]]] = {}
    for item in knowledge_items:
        rel = item["path"]
        if not rel.startswith("knowledge/"):
            continue
        parts = Path(rel.removeprefix("knowledge/")).parts
        if len(parts) <= 1:
            top_level.append(item)
            continue
        group = "/".join(parts[:-1])
        grouped.setdefault(group, []).append(item)

    lines = ["## 知识索引", ""]
    if top_level:
        lines.append("### 核心主题")
        for item in top_level:
            lines.append(f"- `{item['path']}` - {item['summary']}")
        lines.append("")

    sub_indexes: dict[str, str] = {}
    if grouped:
        lines.append("### 分组目录")
        for group in sorted(grouped):
            index_path = f"knowledge/{group}/_index.md"
            lines.append(f"- `{index_path}` - {group} 主题分组。")
            lines.append(f"  → 详见 {index_path}")

            sub_lines = [f"## {group} 索引", ""]
            for item in grouped[group]:
                sub_lines.append(f"- `{item['path']}` - {item['summary']}")
            sub_indexes[index_path] = "\n".join(sub_lines).rstrip() + "\n"
        lines.append("")

    return "\n".join(lines).rstrip() + "\n", sub_indexes


def _render_examples_index(example_items: list[dict[str, Any]]) -> str:
    lines = ["## 案例索引", "", "### 自动生成案例"]
    for item in example_items:
        uses = ", ".join(item.get("uses", []))
        lines.append(f"- `{item['path']}` - {item['summary']}")
        lines.append(f"  uses: {uses}")
    return "\n".join(lines).rstrip() + "\n"


def _render_example_markdown(example: dict[str, Any], engram_name: str, idx: int) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = example.get("title", f"案例{idx}")
    uses = example.get("uses", [])
    tags = example.get("tags", [])
    if not tags:
        tags = [engram_name, "example", "auto-generated"]
    example_id = str(example.get("id", f"example_{engram_name}_{idx}")).strip()
    if not example_id:
        example_id = f"example_{engram_name}_{idx}"

    problem = str(example.get("problem", "待补充背景")).strip() or "待补充背景"
    assessment = str(example.get("assessment", "待补充评估过程")).strip() or "待补充评估过程"
    plan = str(example.get("plan", "待补充执行方案")).strip() or "待补充执行方案"
    review = str(example.get("review", "待补充结果复盘")).strip() or "待补充结果复盘"

    lines = [
        "---",
        f"id: {example_id}",
        f"title: {title}",
        "uses:",
    ]
    for use in uses:
        lines.append(f"  - {use}")
    lines.append("tags:")
    for tag in tags:
        lines.append(f"  - {tag}")
    lines.extend(
        [
            f"updated_at: {today}",
            "---",
            "",
            f"# {title}",
            "",
            "## 背景",
            problem,
            "",
            "## 评估过程",
            assessment,
            "",
            "## 最终方案",
            plan,
            "",
            "## 结果复盘",
            review,
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_engram_draft(
    *,
    mode: str,
    name: str | None = None,
    topic: str | None = None,
    audience: str | None = None,
    style: str | None = None,
    constraints: str | None = None,
    language: str = "zh-CN",
    conversation: str | None = None,
) -> dict[str, Any]:
    if mode not in {"guided", "from_conversation"}:
        raise ValueError("mode 必须是 guided 或 from_conversation")

    insights = _extract_insights(conversation)
    auto_filled: list[str] = []

    if _is_missing(topic):
        if insights:
            topic_value = insights[0][:24]
        else:
            topic_value = "通用专家"
        auto_filled.append("topic")
    else:
        topic_value = str(topic).strip()

    if _is_missing(audience):
        audience_value = "希望获得可执行建议的用户"
        auto_filled.append("audience")
    else:
        audience_value = str(audience).strip()

    if _is_missing(style):
        style_value = "专业、清晰、可执行"
        auto_filled.append("style")
    else:
        style_value = str(style).strip()

    if _is_missing(constraints):
        constraints_value = "超出专业边界时先说明限制并建议求助专业人士"
        auto_filled.append("constraints")
    else:
        constraints_value = str(constraints).strip()

    engram_name = _normalize_name(name, topic_value)
    if _is_missing(name):
        auto_filled.append("name")

    insight_lines = insights[:4]
    if not insight_lines:
        insight_lines = [
            f"围绕 {topic_value} 输出分步骤建议",
            "优先给出低风险、可验证、可执行的方案",
            "每次建议都附带复盘和调整机制",
        ]
        auto_filled.append("conversation_insights")

    role_md = (
        "# 角色定位\n"
        f"你是 {topic_value} 方向的专家，面向 {audience_value} 提供建议。\n\n"
        "## 沟通风格\n"
        f"- {style_value}\n"
        "- 先给结论，再给步骤，再给注意事项。\n"
    )

    workflow_md = (
        "# 工作流程\n"
        "1. 明确目标、约束和成功标准\n"
        "2. 基于现有信息给出可执行方案\n"
        "3. 提供风险提示与替代方案\n"
        "4. 约定复盘节点，持续迭代\n"
    )

    rules_md = (
        "# 运作规则\n"
        f"- 边界：{constraints_value}\n"
        "- 结论必须可执行，避免空泛建议\n"
        "- 信息不足时先提澄清问题\n\n"
        "## 知识提取规则\n"
        "- 对话中形成完整方法论时，主动提议 add_knowledge\n"
        "- 用户纠正知识库错误时，提议用 add_knowledge 更新\n"
    )

    group = "核心主题"
    knowledge_items = [
        {
            "path": f"knowledge/{group}/方法论总览.md",
            "summary": f"{topic_value} 的核心方法论与判断框架",
            "content": (
                f"# {topic_value} 方法论总览\n\n"
                "## 关键洞察\n"
                + "\n".join(f"- {line}" for line in insight_lines)
                + "\n"
            ),
        },
        {
            "path": f"knowledge/{group}/执行清单.md",
            "summary": f"{topic_value} 的落地步骤与检查清单",
            "content": (
                f"# {topic_value} 执行清单\n\n"
                "## 建议步骤\n"
                "- 明确目标与约束\n"
                "- 拆解关键动作并设定里程碑\n"
                "- 每周复盘并根据反馈调整\n"
            ),
        },
    ]

    example_items: list[dict[str, Any]] = [
        {
            "id": f"example_{engram_name}_典型场景",
            "path": "examples/典型场景.md",
            "summary": f"{topic_value} 的典型用户场景与解决方案",
            "title": "典型场景",
            "uses": [item["path"] for item in knowledge_items],
            "problem": f"用户希望获得 {topic_value} 的可执行建议，但信息不完整。",
            "assessment": "先澄清目标、资源、限制，再判断优先级。",
            "plan": "给出最小可执行方案 + 风险提示 + 复盘节点。",
            "review": "根据用户反馈迭代方案，并沉淀为可复用知识。",
            "tags": [engram_name, "auto-generated"],
        }
    ]

    description = (
        f"自动生成的 {topic_value} 专家 Engram（mode={mode}），建议创建后再人工补充细节。"
    )

    return {
        "mode": mode,
        "auto_filled_fields": auto_filled,
        "meta": {
            "name": engram_name,
            "description": description,
            "author": "auto-generated",
            "version": "1.0.0",
            "tags": [topic_value, "auto-generated"],
            "language": language or "zh-CN",
        },
        "role_md": role_md,
        "workflow_md": workflow_md,
        "rules_md": rules_md,
        "knowledge": knowledge_items,
        "examples": example_items,
    }


def draft_response_payload(draft: dict[str, Any]) -> dict[str, Any]:
    auto_filled = draft.get("auto_filled_fields", [])
    return {
        "requires_confirmation": True,
        "mode": draft.get("mode"),
        "name": draft.get("meta", {}).get("name"),
        "summary": {
            "description": draft.get("meta", {}).get("description", ""),
            "knowledge_files": [item["path"] for item in draft.get("knowledge", [])],
            "example_files": [item["path"] for item in draft.get("examples", [])],
        },
        "incomplete_notice": (
            "以下字段由系统自动补全，可能不完整，请确认后再落盘："
            + ", ".join(auto_filled)
            if auto_filled else ""
        ),
        "draft": draft,
    }


def parse_draft_payload(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if isinstance(data, dict) and isinstance(data.get("draft"), dict):
        return data["draft"]
    if isinstance(data, dict):
        return data
    raise ValueError("draft_json 必须是 JSON object")


def materialize_draft(engram_dir: Path, draft: dict[str, Any]) -> None:
    engram_dir.mkdir(parents=True, exist_ok=True)

    meta = draft.get("meta", {})
    meta_path = engram_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (engram_dir / "role.md").write_text(str(draft.get("role_md", "")).rstrip() + "\n", encoding="utf-8")
    (engram_dir / "workflow.md").write_text(
        str(draft.get("workflow_md", "")).rstrip() + "\n",
        encoding="utf-8",
    )
    (engram_dir / "rules.md").write_text(str(draft.get("rules_md", "")).rstrip() + "\n", encoding="utf-8")

    knowledge_dir = engram_dir / "knowledge"
    if knowledge_dir.exists():
        shutil.rmtree(knowledge_dir)
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    knowledge_items = draft.get("knowledge", [])
    for item in knowledge_items:
        rel = Path(str(item["path"]))
        target = (engram_dir / rel).resolve()
        target.relative_to(engram_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(item.get("content", "")).rstrip() + "\n", encoding="utf-8")

    top_index, sub_indexes = _render_knowledge_index(knowledge_items)
    (knowledge_dir / "_index.md").write_text(top_index, encoding="utf-8")
    for index_path, content in sub_indexes.items():
        target = engram_dir / index_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    examples_dir = engram_dir / "examples"
    if examples_dir.exists():
        shutil.rmtree(examples_dir)
    examples_dir.mkdir(parents=True, exist_ok=True)

    example_items = draft.get("examples", [])
    for idx, item in enumerate(example_items, start=1):
        rel = Path(str(item["path"]))
        target = (engram_dir / rel).resolve()
        target.relative_to(engram_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            _render_example_markdown(item, meta.get("name", "engram"), idx),
            encoding="utf-8",
        )

    (examples_dir / "_index.md").write_text(
        _render_examples_index(example_items),
        encoding="utf-8",
    )

    memory_index = engram_dir / "memory" / "_index.md"
    memory_index.parent.mkdir(parents=True, exist_ok=True)
    if not memory_index.exists():
        memory_index.write_text("", encoding="utf-8")
