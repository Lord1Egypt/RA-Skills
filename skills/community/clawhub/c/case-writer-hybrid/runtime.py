from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from skill_runtime.writing_core import (
    STRUCTURE_TYPES,
    build_ending_cta,
    build_ending_options,
    build_opening_options,
    build_quality_gate_notice,
    build_share_copy_options,
    build_summary_points,
    bullet_values,
    choose_structure,
    clean_text,
    critique_article,
    derive_primary_pain_point,
    derive_reader_profile,
    dump_json,
    extract_highlight_quotes,
    generate_title_options,
    humanize_markdown,
    judge_article,
    parse_markdown_sections,
    quality_gate_path,
    read_text,
    score_topic_material,
    slugify,
    truncate_text,
    write_text,
)


def parse_brief(path: Path) -> dict[str, Any]:
    text = read_text(path)
    sections = parse_markdown_sections(text)
    base = "\n".join(sections.get("基础信息", []))

    def field(name: str) -> str:
        match = re.search(rf"`?{re.escape(name)}`?\s*[：:]\s*(.+)", base)
        return match.group(1).strip() if match else ""

    core_view = "\n".join(
        line.strip()
        for line in sections.get("核心观点", [])
        if line.strip() and not line.strip().startswith(">")
    ).strip()
    if not core_view:
        quoted = [
            line.strip("> ").strip()
            for line in sections.get("核心观点", [])
            if line.strip().startswith(">")
        ]
        core_view = "\n".join(quoted).strip()

    topic = field("topic") or path.stem
    slug = field("slug") or slugify(topic)
    date = field("date") or datetime.now().strftime("%Y%m%d")

    return {
        "topic": topic,
        "slug": slug,
        "date": date,
        "target_reader": field("target_reader"),
        "publish_goal": field("publish_goal"),
        "core_view": core_view,
        "background": bullet_values(sections.get("背景与语境", [])),
        "arguments": bullet_values(sections.get("论证方向", [])),
        "cases": bullet_values(sections.get("可用案例 / 素材", [])),
        "avoid": bullet_values(sections.get("明确不要写什么", [])),
        "style": bullet_values(sections.get("风格要求", [])),
        "visual": bullet_values(sections.get("配图方向", [])),
        "notes": bullet_values(sections.get("备注", [])),
        "source_path": str(path),
    }


def article_output_path(workspace_root: Path, slug: str) -> Path:
    return workspace_root / "content-production" / "drafts" / f"{slug}-article.md"


def writing_pack_md_path(workspace_root: Path, slug: str) -> Path:
    return workspace_root / "content-production" / "drafts" / f"{slug}-writing-pack.md"


def writing_pack_json_path(workspace_root: Path, slug: str) -> Path:
    return workspace_root / "content-production" / "drafts" / f"{slug}-writing-pack.json"


def review_trace_path(workspace_root: Path, slug: str) -> Path:
    return workspace_root / "content-production" / "drafts" / f"{slug}-review-trace.json"


def _argument_label(index: int, total: int, structure_type: str) -> str:
    if structure_type == "what_why_how":
        return ["What：问题到底是什么", "Why：为什么现在必须重视", "How：普通人怎么落地"][min(index - 1, 2)]
    if structure_type == "story":
        return ["故事先讲到这里", "问题真正卡在哪里", "这件事最后怎么落地"][min(index - 1, 2)]
    if structure_type == "listicle":
        return f"清单 {index}"
    return f"论证 {index}"


def _argument_paragraphs(
    *,
    argument: str,
    case_line: str,
    brief: dict[str, Any],
    focus_areas: list[str],
    round_index: int,
) -> list[str]:
    normalized_argument = argument.rstrip("。！？!?. ")
    paragraphs = [
        f"{normalized_argument}。如果只把这个问题看成一个表面动作，你会误以为卡点在执行力；可一旦把它放回真实语境里看，真正决定结果的常常是背后的结构。",
    ]
    if case_line:
        paragraphs.append(f"最能说明这一点的案例是：{case_line}。案例之所以有价值，不是因为它够热闹，而是它能把问题具体化。")
    if "evidence_substance" in focus_areas or round_index >= 2:
        paragraphs.append(
            "这不是抽象判断。至少可以从三个层面去看：一是实际案例有没有重复出现，二是论证里有没有可验证的事实，三是这些事实能不能支撑你最后那个结论。"
        )
    if "reader_value" in focus_areas or round_index >= 2:
        reader = brief["target_reader"] or "读者"
        paragraphs.append(f"对{reader}来说，真正有用的地方不只是听懂一个观点，而是知道自己接下来应该往哪一步补。")
    if "pacing_length" in focus_areas and round_index >= 2:
        paragraphs.append("换句话说，别急着加动作，先把结构补齐。")
    return paragraphs


def compose_article(
    *,
    brief: dict[str, Any],
    package: dict[str, Any],
    round_index: int,
    focus_areas: list[str],
) -> str:
    arguments = brief["arguments"][:3] or [
        "为什么这个问题值得现在讨论",
        "为什么它不是一个单点动作问题",
        "为什么最后还是要回到系统和结构",
    ]
    cases = brief["cases"][:3]
    title_candidates = package["title_options"]
    title = brief["topic"] if round_index == 1 else title_candidates[min(round_index - 2, len(title_candidates) - 1)]["title"]
    if "headline_hook" in focus_areas and title_candidates:
        title = title_candidates[0]["title"]

    opening_options = package["opening_options"]
    ending_options = package["ending_options"]
    opening_text = opening_options[min(round_index - 1, len(opening_options) - 1)]["text"]
    ending_text = ending_options[0]["text"] if "reader_value" not in focus_areas else ending_options[min(1, len(ending_options) - 1)]["text"]
    topic = brief["topic"]
    core_view = clean_text(brief["core_view"]) or f"{topic}不是表面技巧，而是一套能复用的结构。"
    structure_label = STRUCTURE_TYPES[package["chosen_structure"]["type"]]

    argument_blocks: list[str] = []
    for index, argument in enumerate(arguments, start=1):
        case_line = cases[index - 1] if index - 1 < len(cases) else ""
        section_title = _argument_label(index, len(arguments), package["chosen_structure"]["type"])
        if not section_title.startswith(("论证", "What", "Why", "How", "故事", "清单")):
            section_title = f"论证 {index}"
        paragraphs = _argument_paragraphs(
            argument=argument,
            case_line=case_line,
            brief=brief,
            focus_areas=focus_areas,
            round_index=round_index,
        )
        argument_blocks.extend([f"## {section_title}", "", *paragraphs, ""])

    action_lines = [
        "先明确这篇内容到底要替谁解决什么问题，别上来就堆信息。",
        f"优先采用 `{structure_label}`，先把结构搭好，再补素材和标题。",
        "发布前至少再过一遍标题、开头、证据和结尾互动，不要只改错别字。",
    ]

    spread_lines = [f"- {item}" for item in package["highlight_quotes"][:3]]
    background_hint = truncate_text("；".join(brief["background"][:2]), 140)

    article = [
        f"# {title}",
        "",
        f"> 目标读者：{brief['target_reader'] or '关注该议题的公众号读者'}",
        f"> 发布目标：{brief['publish_goal'] or '形成一篇可发布的公众号长文'}",
        "",
        "## 导语",
        "",
        opening_text,
        "",
        "## 问题提出",
        "",
        background_hint or "很多内容之所以没有结果，不是因为作者不努力，而是因为题目、结构、包装和质量门控并没有形成闭环。",
        "",
        "## 核心判断",
        "",
        f"{core_view} 这也是为什么这篇文章不打算只停留在现象判断，而是要把背后的结构说清楚。",
        "",
        *argument_blocks,
        "## 你现在可以怎么做",
        "",
        *[f"- {item}" for item in action_lines],
        "",
        "## 结论",
        "",
        ending_text,
        "",
        "## 可传播总结",
        "",
        *spread_lines,
        "",
    ]
    return "\n".join(article).rstrip() + "\n"


def build_writing_pack_markdown(package: dict[str, Any], judge: dict[str, Any]) -> str:
    lines = [
        f"# 写作包：{package['topic']}",
        "",
        "## 写作定位",
        "",
        f"- `topic_score`：{package['topic_score']['total']}",
        f"- `reader_profile`：{package['reader_profile']}",
        f"- `primary_pain_point`：{package['primary_pain_point']}",
        "",
        "## 选用结构",
        "",
        f"- `type`：{package['chosen_structure']['type']}",
        f"- `label`：{STRUCTURE_TYPES[package['chosen_structure']['type']]}",
        f"- `reason`：{package['chosen_structure']['reason']}",
        "",
        "## 开头备选",
        "",
    ]
    for item in package["opening_options"]:
        lines.extend([f"### {item['label']}", "", item["text"], ""])

    lines.extend(["## 结尾备选", ""])
    for item in package["ending_options"]:
        lines.extend([f"### {item['label']}", "", item["text"], ""])

    lines.extend(["## 标题候选", ""])
    for item in package["title_options"]:
        driver_text = " / ".join(item["driver_labels"]) or "无"
        lines.append(f"- {item['title']} | {item['pattern_label']} | 驱动：{driver_text} | 分数：{item['score']}")

    lines.extend(["", "## 转发语候选", ""])
    for item in package["share_copy_options"]:
        lines.append(f"- {item}")

    lines.extend(["", "## 金句候选", ""])
    for item in package["highlight_quotes"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 裁判结论",
            "",
            f"- `score`：{judge['score']}",
            f"- `ai_trace_risk`：{judge['ai_trace_risk']}",
            f"- `pass`：{'true' if judge['pass'] else 'false'}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_case_writer_hybrid(input_path: Path, *, workspace_root: Path) -> dict[str, Any]:
    brief = parse_brief(input_path)
    topic_score = score_topic_material(
        topic=brief["topic"],
        core_view=brief["core_view"],
        background=brief["background"],
        arguments=brief["arguments"],
        cases=brief["cases"],
        notes=brief["notes"],
    )
    chosen_structure = choose_structure(
        topic=brief["topic"],
        core_view=brief["core_view"],
        arguments=brief["arguments"],
        cases=brief["cases"],
        background=brief["background"],
    )
    reader_profile = derive_reader_profile(brief)
    primary_pain_point = derive_primary_pain_point(brief)
    opening_options = build_opening_options(
        topic=brief["topic"],
        reader_profile=reader_profile,
        pain_point=primary_pain_point,
        core_view=brief["core_view"],
        chosen_structure=chosen_structure["type"],
        cases=brief["cases"],
    )
    ending_options = build_ending_options(
        topic=brief["topic"],
        reader_profile=reader_profile,
        core_view=brief["core_view"],
    )
    title_options = generate_title_options(
        topic=brief["topic"],
        core_view=brief["core_view"],
        reader_profile=reader_profile,
        pain_point=primary_pain_point,
    )
    share_copy_options = build_share_copy_options(
        topic=brief["topic"],
        core_view=brief["core_view"],
        reader_profile=reader_profile,
    )
    highlight_quotes = extract_highlight_quotes(
        topic=brief["topic"],
        core_view=brief["core_view"],
        arguments=brief["arguments"],
    )
    summary_points = build_summary_points(brief["arguments"], brief["core_view"])
    ending_cta = build_ending_cta(reader_profile, brief["topic"])

    package = {
        "topic": brief["topic"],
        "slug": brief["slug"],
        "topic_score": topic_score,
        "reader_profile": reader_profile or "关注该议题的公众号读者",
        "primary_pain_point": primary_pain_point,
        "chosen_structure": chosen_structure,
        "opening_options": opening_options,
        "ending_options": ending_options,
        "title_options": title_options,
        "share_copy_options": share_copy_options,
        "highlight_quotes": highlight_quotes,
        "summary_points": summary_points,
        "ending_cta": ending_cta,
    }

    best_article = ""
    best_judge: dict[str, Any] | None = None
    best_score = -1.0
    focus_areas: list[str] = []
    rounds: list[dict[str, Any]] = []

    for round_index in range(1, 4):
        draft = compose_article(
            brief=brief,
            package=package,
            round_index=round_index,
            focus_areas=focus_areas,
        )
        humanized = humanize_markdown(draft, mode="surgical")
        critique = critique_article(humanized["text"], chosen_structure=chosen_structure["type"])
        judge = judge_article(humanized["text"], critique=critique, humanizer_report=humanized)

        rounds.append(
            {
                "round": round_index,
                "title": clean_text(re.search(r"^#\s+(.+)$", humanized["text"], flags=re.MULTILINE).group(1)) if re.search(r"^#\s+(.+)$", humanized["text"], flags=re.MULTILINE) else brief["topic"],
                "score": judge["score"],
                "scores": judge["scores"],
                "ai_trace_risk": judge["ai_trace_risk"],
                "critic_issues": critique["issues"],
                "focus_areas": judge["focus_areas"],
                "humanizer": {
                    "changed_line_count": humanized["changed_line_count"],
                    "pattern_hit_count": humanized["pattern_hit_count"],
                    "changes": humanized["changes"],
                },
                "article_excerpt": truncate_text(humanized["text"], 260),
            }
        )

        if judge["score"] > best_score:
            best_score = judge["score"]
            best_article = humanized["text"]
            best_judge = judge

        if judge["pass"]:
            break
        focus_areas = judge["focus_areas"]

    assert best_judge is not None

    article_path = article_output_path(workspace_root, brief["slug"])
    pack_md_path = writing_pack_md_path(workspace_root, brief["slug"])
    pack_json_path = writing_pack_json_path(workspace_root, brief["slug"])
    trace_path = review_trace_path(workspace_root, brief["slug"])
    notice_path = quality_gate_path(workspace_root, date=brief["date"], slug=brief["slug"])

    publish_ready = bool(best_judge["pass"])
    run_status = "completed" if publish_ready else "quality_gate_failed"
    next_action = "" if publish_ready else "user_review_required"

    package["judge_summary"] = {
        "score": best_judge["score"],
        "scores": best_judge["scores"],
        "ai_trace_risk": best_judge["ai_trace_risk"],
        "pass": publish_ready,
    }
    package["publish_ready"] = publish_ready
    package["run_status"] = run_status
    package["next_action"] = next_action

    write_text(article_path, best_article)
    write_text(pack_md_path, build_writing_pack_markdown(package, best_judge))
    dump_json(pack_json_path, package)
    dump_json(
        trace_path,
        {
            "slug": brief["slug"],
            "topic": brief["topic"],
            "source_path": brief["source_path"],
            "publish_ready": publish_ready,
            "run_status": run_status,
            "next_action": next_action,
            "final_round": rounds[-1]["round"],
            "selected_round": max(rounds, key=lambda item: item["score"])["round"],
            "rounds": rounds,
            "latest_score": best_judge["score"],
            "latest_scores": best_judge["scores"],
            "ai_trace_risk": best_judge["ai_trace_risk"],
            "unresolved_issues": best_judge["unresolved_issues"],
        },
    )

    if not publish_ready:
        write_text(
            notice_path,
            build_quality_gate_notice(
                date=brief["date"],
                slug=brief["slug"],
                topic=brief["topic"],
                judge=best_judge,
                article_path=article_path,
                writing_pack_path=pack_md_path,
                review_trace_path=trace_path,
            ),
        )

    return {
        "slug": brief["slug"],
        "topic": brief["topic"],
        "article_path": article_path,
        "writing_pack_md_path": pack_md_path,
        "writing_pack_json_path": pack_json_path,
        "review_trace_path": trace_path,
        "quality_gate_notice_path": notice_path if not publish_ready else "",
        "publish_ready": publish_ready,
        "run_status": run_status,
        "blocking": not publish_ready,
        "next_action": next_action,
        "score": best_judge["score"],
        "scores": best_judge["scores"],
        "ai_trace_risk": best_judge["ai_trace_risk"],
        "message": "文章已通过质量门控。" if publish_ready else "文章连续三轮未达标，已中断并等待人工处理。",
    }
