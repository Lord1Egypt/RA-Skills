#!/usr/bin/env python3
"""Build dual-report artifacts for one monthly BP run.

This script upgrades a legacy run folder into the newer structure:

- 04_cards/
- 05_ai_baseline_report.md
- 05_review_queue/
- 07_user_review_report.md

It reuses the already fetched BP skeleton and evidence manifest instead of
rewriting BP fetch logic again.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


GREEN = "#2e7d32"
YELLOW = "#b26a00"
RED = "#d32f2f"
BLACK = "#111111"
LIGHT_COLOR = {"🟢": GREEN, "🟡": YELLOW, "🔴": RED, "⚫": BLACK}
LIGHT_NAME = {"🟢": "green", "🟡": "yellow", "🔴": "red", "⚫": "black"}


@dataclass
class EvidenceRow:
    ref: str
    title: str
    raw_hits: int
    author: str
    priority: str
    link_status: str
    task_id: str
    attachment_status: str
    facts: list[str]


@dataclass
class LegacyCard:
    section_key: str
    result_name: str
    light: str
    reason: str
    evidence_refs: list[str]
    progress_lines: list[str]
    raw_block: str


def load_yaml_via_ruby(path: Path) -> object:
    ruby = (
        "require 'yaml'; require 'json'; "
        f"data = YAML.load_file({json.dumps(str(path))}); "
        "puts JSON.generate(data)"
    )
    raw = subprocess.check_output(["ruby", "-e", ruby], text=True)
    return json.loads(raw)


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", value)
    return cleaned.strip("_")[:80] or "item"


def parse_manifest(path: Path) -> tuple[dict[str, EvidenceRow], dict[str, list[EvidenceRow]], dict[str, int]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    stats = {
        "raw_report_hit_count": int(re.search(r"raw_report_hit_count: (\d+)", text).group(1)),
        "adopted_report_count": int(re.search(r"adopted_report_count: (\d+)", text).group(1)),
        "adopted_primary_report_count": int(re.search(r"adopted_primary_report_count: (\d+)", text).group(1)),
        "adopted_other_manual_report_count": int(re.search(r"adopted_other_manual_report_count: (\d+)", text).group(1)),
        "adopted_ai_report_count": int(re.search(r"adopted_ai_report_count: (\d+)", text).group(1)),
    }

    evidence_by_ref: dict[str, EvidenceRow] = {}
    evidence_by_task: dict[str, list[EvidenceRow]] = {}
    current_ref = ""
    current_facts: list[str] = []

    for line in lines:
        if line.startswith("| R"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) < 8:
                continue
            row = EvidenceRow(
                ref=parts[0],
                title=parts[1],
                raw_hits=int(parts[2]),
                author=parts[3],
                priority=parts[4],
                link_status=parts[5],
                task_id=parts[6],
                attachment_status=parts[7],
                facts=[],
            )
            evidence_by_ref[row.ref] = row
            evidence_by_task.setdefault(row.task_id, []).append(row)
            continue

        if line.startswith("## R"):
            current_ref = line.replace("## ", "").strip()
            current_facts = []
            continue
        if current_ref and line.startswith("  - "):
            current_facts.append(line.strip()[2:].strip())
            continue
        if current_ref and line.startswith("- 标题："):
            title = line.split("：", 1)[1].strip()
            if current_ref in evidence_by_ref:
                evidence_by_ref[current_ref].title = title
            continue
        if current_ref and line.startswith("- 进展事实："):
            continue
        if current_ref and not line.strip():
            if current_ref in evidence_by_ref and current_facts:
                evidence_by_ref[current_ref].facts = current_facts[:]
            current_ref = ""
            current_facts = []

    if current_ref and current_ref in evidence_by_ref and current_facts:
        evidence_by_ref[current_ref].facts = current_facts[:]

    return evidence_by_ref, evidence_by_task, stats


def parse_legacy_section_cards(path: Path) -> list[LegacyCard]:
    lines = path.read_text(encoding="utf-8").splitlines()
    cards: list[LegacyCard] = []
    current_section = ""
    current_result = ""
    buffer: list[str] = []
    in_progress = False
    progress_lines: list[str] = []
    evidence_refs: list[str] = []

    def flush() -> None:
        nonlocal current_result, buffer, progress_lines, evidence_refs, in_progress
        if not current_result:
            return
        raw_block = "\n".join(buffer)
        light_match = re.search(r"灯色：([🟢🟡🔴⚫])", raw_block)
        reason_match = re.search(r"判断理由：([^<\n]+)", raw_block)
        cards.append(
            LegacyCard(
                section_key=current_section,
                result_name=current_result,
                light=light_match.group(1) if light_match else "⚫",
                reason=(reason_match.group(1).strip() if reason_match else "当前缺少稳定判断依据。"),
                evidence_refs=evidence_refs[:],
                progress_lines=progress_lines[:],
                raw_block=raw_block,
            )
        )
        current_result = ""
        buffer = []
        progress_lines = []
        evidence_refs = []
        in_progress = False

    for line in lines:
        sec_match = re.match(r"^##\s+(2\.\d+)\s+", line)
        if sec_match:
            flush()
            current_section = sec_match.group(1)
            buffer = [line]
            continue
        if current_section and re.match(r"^###\s+关键成果", line):
            flush()
            result_text = re.sub(r"^###\s+关键成果\s+\S+\s*", "", line).strip()
            current_result = result_text
            buffer = [line]
            continue
        if current_section and line.startswith("- 关键成果："):
            if current_result:
                flush()
            current_result = line.split("：", 1)[1].strip().strip("`")
            buffer.append(line)
            continue
        if not current_section:
            continue
        if current_result:
            buffer.append(line)
            if line.startswith("- 采用证据："):
                evidence_refs.extend(re.findall(r"`(R\d+)`", line))
            elif line.startswith("- 本月进展："):
                in_progress = True
            elif in_progress and line.startswith("  - "):
                progress_lines.append(line.strip()[2:].strip())
            elif in_progress and not line.startswith("  - "):
                in_progress = False
        else:
            buffer.append(line)

    flush()
    return cards


def action_light(rows: list[EvidenceRow]) -> str:
    if not rows:
        return "⚫"
    joined = " ".join(
        row.title + " " + " ".join(row.facts[:6]) for row in rows
    )
    if re.search(r"失败|停滞|终止|中断|严重|紧急|败诉|无法推进", joined):
        return "🔴"
    return "🟡"


def action_reason(light: str, action_name: str, rows: list[EvidenceRow]) -> str:
    if light == "⚫":
        return f"当前没有检索到能直接支撑“{action_name}”的有效汇报，无法判断该举措在本月是否真实推进。"
    if light == "🔴":
        return f"当前证据已暴露“{action_name}”存在明确异常或明显阻塞，需要按红灯处理。"
    return f"当前证据能够证明“{action_name}”已经启动或推进，但离举措闭环和稳定落地仍有距离，因此按黄灯处理。"


def build_action_progress(rows: list[EvidenceRow]) -> list[str]:
    facts: list[str] = []
    for row in rows:
        if row.facts:
            for fact in row.facts[:2]:
                if fact not in facts:
                    facts.append(fact)
        else:
            facts.append(f"已采纳证据：{row.ref}《{row.title}》")
    return facts[:4] or ["当前未检索到稳定进展事实。"]


def format_status_block(light: str, reason: str) -> list[str]:
    color = LIGHT_COLOR[light]
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
        lines.append(
            f"  <span style=\"color:{color}; font-weight:700;\">持续提醒至下周期：是</span>"
        )
    return lines


def write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_kr_cards(
    run_dir: Path,
    anchor_map: list[dict],
    legacy_cards: list[LegacyCard],
) -> tuple[list[dict], list[dict]]:
    cards_dir = run_dir / "04_cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    legacy_by_result = {card.result_name: card for card in legacy_cards}
    created: list[dict] = []
    review_items: list[dict] = []

    for goal in anchor_map:
        section_key = goal["section_key"]
        for idx, kr in enumerate(goal.get("key_results") or [], start=1):
            legacy = legacy_by_result.get(kr["result_name"])
            light = legacy.light if legacy else "⚫"
            reason = legacy.reason if legacy else "当前缺少稳定证据支撑该关键成果判断。"
            progress_lines = legacy.progress_lines if legacy else ["待补充"]
            evidence_refs = legacy.evidence_refs if legacy else []
            rel_id = f"{section_key}_kr_{idx:02d}"
            filename = cards_dir / f"{rel_id}.md"
            lines = [
                f"# {section_key} / 关键成果卡 {idx}",
                "",
                f"- 章节：`{section_key}`",
                f"- 目标：`{goal['goal_name']}`",
                f"- 关键成果：`{kr['result_name']}`",
                f"- 衡量标准：`{kr.get('measure_standard', '')}`",
                f"- 证据：{' '.join(f'`{ref}`' for ref in evidence_refs) if evidence_refs else '待补充'}",
                "- 本月进展：",
            ]
            for item in progress_lines:
                lines.append(f"  - {item}")
            lines.extend(format_status_block(light, reason))
            write_text(filename, lines)
            created.append(
                {
                    "id": rel_id,
                    "path": filename,
                    "title": kr["result_name"],
                    "light": light,
                    "reason": reason,
                    "anchor_type": "key_result",
                    "section_key": section_key,
                }
            )
            if light in {"🟡", "🔴", "⚫"}:
                review_items.append(created[-1])
    return created, review_items


def build_action_cards(
    run_dir: Path,
    anchor_map: list[dict],
    evidence_by_task: dict[str, list[EvidenceRow]],
) -> tuple[list[dict], list[dict], str]:
    cards_dir = run_dir / "04_cards"
    review_items: list[dict] = []
    created: list[dict] = []
    chapter_lines = ["## 4. 关键举措推进情况", ""]

    for goal_idx, goal in enumerate(anchor_map, start=1):
        section_no = f"4.{goal_idx}"
        chapter_lines.extend([f"### {section_no} {goal['goal_name']}", ""])
        action_index = 0
        for kr in goal.get("key_results") or []:
            for action in kr.get("actions") or []:
                action_index += 1
                block_no = f"{section_no}.{action_index}"
                rows = evidence_by_task.get(action["action_id"], [])
                light = action_light(rows)
                reason = action_reason(light, action["action_name"], rows)
                progress_lines = build_action_progress(rows)
                refs = [row.ref for row in rows]
                refs_md = (
                    "；".join(f"`{row.ref}`《{row.title}》({row.author}/{row.priority})" for row in rows[:4])
                    if rows
                    else "未检索到稳定证据"
                )

                filename = cards_dir / f"{section_no}_action_{action_index:02d}.md"
                lines = [
                    f"# {block_no} / 关键举措卡",
                    "",
                    f"- 章节：`{section_no}`",
                    f"- 对应目标：`{goal['goal_name']}`",
                    f"- 对应关键成果：`{kr['result_name']}`",
                    f"- 关键举措：`{action['action_name']}`",
                    f"- 证据：{refs_md}",
                    "- 当前进展：",
                ]
                for item in progress_lines:
                    lines.append(f"  - {item}")
                lines.extend(format_status_block(light, reason))
                write_text(filename, lines)

                card_meta = {
                    "id": f"{section_no}_action_{action_index:02d}",
                    "path": filename,
                    "title": action["action_name"],
                    "light": light,
                    "reason": reason,
                    "anchor_type": "key_action",
                    "section_key": section_no,
                }
                created.append(card_meta)
                if light in {"🟡", "🔴", "⚫"}:
                    review_items.append(card_meta)

                chapter_lines.extend(
                    [
                        f"#### {block_no} {action['action_name']}",
                        "",
                        f"- 对应关键成果：`{kr['result_name']}`",
                        "- 当前进展：",
                    ]
                )
                for item in progress_lines:
                    chapter_lines.append(f"  - {item}")
                chapter_lines.append(f"- 证据：{refs_md}")
                chapter_lines.extend(format_status_block(light, reason))
                chapter_lines.append("")
        chapter_lines.append("")

    return created, review_items, "\n".join(chapter_lines).rstrip() + "\n"


def build_review_queue(run_dir: Path, review_items: list[dict]) -> None:
    queue_dir = run_dir / "05_review_queue"
    if queue_dir.exists():
        shutil.rmtree(queue_dir)
    queue_dir.mkdir(parents=True, exist_ok=True)

    for item in review_items:
        light_slug = LIGHT_NAME[item["light"]]
        filename = queue_dir / f"{sanitize_filename(item['id'])}_{light_slug}.md"
        color = LIGHT_COLOR[item["light"]]
        lines = [
            f"# 复盘卡 / {item['title']}",
            "",
            f"- 卡片ID：`{item['id']}`",
            f"- 类型：`{item['anchor_type']}`",
            f"- 章节引用：`{item['section_key']}`",
            f"- 当前灯色：`{item['light']}`",
            f"- AI判断理由：{item['reason']}",
            f"- 来源卡片：[查看原卡]({item['path']})",
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
        write_text(filename, lines)


def rewrite_title(text: str, suffix: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        base_title = re.sub(r"（AI基准草稿）|（用户复盘版）", "", lines[0]).rstrip()
        lines[0] = f"{base_title}（{suffix}）"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_chapter_4(text: str, chapter_4: str) -> str:
    pattern = re.compile(r"^## 4\..*?(?=^## 5\.|\Z)", re.M | re.S)
    return pattern.sub(chapter_4.rstrip() + "\n\n", text, count=1)


def extract_base_title(text: str) -> str:
    first_line = text.splitlines()[0]
    return re.sub(r"（AI基准草稿）|（用户复盘版）", "", first_line).rstrip()


def set_title(text: str, title_line: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines[0] = title_line
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def build_dual_reports(run_dir: Path, chapter_4: str) -> tuple[Path, Path]:
    legacy_report = run_dir / "05_report.md"
    legacy_text = legacy_report.read_text(encoding="utf-8")
    base_title = extract_base_title(legacy_text)
    baseline_text = replace_chapter_4(legacy_text, chapter_4)
    baseline_text = set_title(baseline_text, f"{base_title}（AI基准草稿）")
    review_text = set_title(baseline_text, f"{base_title}（用户复盘版）")
    review_lines = review_text.splitlines()
    if len(review_lines) >= 2:
        review_lines.insert(
            1,
            "",
        )
        review_lines.insert(
            2,
            "> 说明：本文件为用户复盘版底稿，用户可以修改任何内容；但所有 `🟡 / 🔴 / ⚫` 判断块都必须补充解释。",
        )
        review_text = "\n".join(review_lines) + "\n"

    baseline_path = run_dir / "05_ai_baseline_report.md"
    review_path = run_dir / "07_user_review_report.md"
    baseline_path.write_text(baseline_text, encoding="utf-8")
    review_path.write_text(review_text, encoding="utf-8")
    return baseline_path, review_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    anchor_map = load_yaml_via_ruby(run_dir / "01_bp_anchor_map.yaml")
    evidence_by_ref, evidence_by_task, _stats = parse_manifest(run_dir / "_manifest" / "manifest.md")
    legacy_cards = parse_legacy_section_cards(run_dir / "04_section_cards.md")

    cards_dir = run_dir / "04_cards"
    if cards_dir.exists():
        shutil.rmtree(cards_dir)
    cards_dir.mkdir(parents=True, exist_ok=True)

    kr_cards, kr_review_items = build_kr_cards(run_dir, anchor_map, legacy_cards)
    action_cards, action_review_items, chapter_4 = build_action_cards(run_dir, anchor_map, evidence_by_task)
    build_review_queue(run_dir, kr_review_items + action_review_items)
    baseline_path, review_path = build_dual_reports(run_dir, chapter_4)

    print(json.dumps(
        {
            "run_dir": str(run_dir),
            "kr_cards": len(kr_cards),
            "action_cards": len(action_cards),
            "review_queue_items": len(kr_review_items) + len(action_review_items),
            "baseline_report": str(baseline_path),
            "user_review_report": str(review_path),
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
