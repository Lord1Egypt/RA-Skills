#!/usr/bin/env python3
"""Build a concise baton message for multi-agent brainstorming.

Generic version — role names are fully configurable.
Mention protocol ([[mention:...]] / [[next:...]]) is the default
but can be replaced with any platform-specific protocol.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


# ──────────────────────────────────────────────
#  Configurable defaults — override via CLI or env
# ──────────────────────────────────────────────

DEFAULT_FACILITATOR = "facilitator"
DEFAULT_STRATEGIST = "strategist"
DEFAULT_EXECUTOR = "executor"

# Mention template: {{speaker}} → mention markup (e.g. "[[mention:{{speaker}}]]" or "<@{{speaker}}>")
MENTION_TEMPLATE = "[[mention:{{speaker}}]]"
NEXT_TEMPLATE = "[[next:{{speaker}}]]"


@dataclass(frozen=True)
class BatonSpec:
    round_no: int
    round_total: int
    speaker: str
    next_speaker: str
    final_speaker: str
    facilitator: str
    topic: str
    mode: str
    focus: str
    custom_ask: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a concise baton message for agent-brainstorm-chair.",
    )
    parser.add_argument("--topic", required=True, help="Meeting topic.")
    parser.add_argument("--round-no", type=int, required=True)
    parser.add_argument("--round-total", type=int, required=True)
    parser.add_argument("--speaker", required=True, help="Current speaker name.")
    parser.add_argument("--next-speaker", required=True, help="Next speaker name.")
    parser.add_argument("--final-speaker", default="", help="Last peer speaker in the current round.")
    parser.add_argument("--facilitator", default=DEFAULT_FACILITATOR, help="Facilitator name.")
    parser.add_argument("--mode", choices=("discussion", "execution"), default="discussion")
    parser.add_argument("--focus", choices=("auto", "judgement", "rebuttal", "execution", "synthesis"), default="auto")
    parser.add_argument("--custom-ask", default="", help="Override the default ask body.")
    parser.add_argument("--mention-template", default=MENTION_TEMPLATE, help="Template for mentions (use {{speaker}}).")
    parser.add_argument("--next-template", default=NEXT_TEMPLATE, help="Template for next-speaker marker (use {{speaker}}).")
    return parser


def fmt_mention(speaker: str, template: str) -> str:
    return template.replace("{{speaker}}", speaker)


# ──────────────────────────────────────────────
#  Focus detection
# ──────────────────────────────────────────────

FOCUS_STRATEGIST_NAMES = {"strategist", "lvbu", "lübu", "吕布", "main", "libu"}
FOCUS_EXECUTOR_NAMES = {"executor", "zhangmiao", "张邈"}
FOCUS_FACILITATOR_NAMES = {"facilitator", "chengong", "陈宫"}


def _name_in_set(name: str, candidates: set[str]) -> bool:
    return name.strip().lower() in candidates


def normalize_focus(spec: BatonSpec) -> str:
    if spec.focus != "auto":
        return spec.focus
    speaker = spec.speaker.strip().lower()
    if _name_in_set(speaker, FOCUS_STRATEGIST_NAMES):
        return "judgement" if spec.round_no == 1 else "rebuttal"
    if _name_in_set(speaker, FOCUS_EXECUTOR_NAMES):
        return "rebuttal" if spec.mode == "discussion" else "execution"
    return "synthesis" if spec.round_no == spec.round_total else "rebuttal"


def build_default_ask(spec: BatonSpec) -> str:
    focus = normalize_focus(spec)
    if spec.custom_ask.strip():
        return spec.custom_ask.strip()
    if focus == "judgement":
        return "请直接给主判断，并补最关键的支撑点。不要重复背景，可顺带说明必要边界或保留条件。"
    if focus == "rebuttal":
        return "请只围绕上一棒最关键分歧补充反证、限制条件或修正意见，不要重复背景。"
    if focus == "execution":
        return "请只回答可否落地、关键约束、执行顺序，不展开无关背景。"
    return "请只收束本轮共识与分歧，并决定是否进入下一轮。"


def build_baton(spec: BatonSpec, mention_tpl: str = MENTION_TEMPLATE, next_tpl: str = NEXT_TEMPLATE) -> str:
    ask = build_default_ask(spec)
    facilitator = spec.facilitator
    is_final_baton = spec.next_speaker.strip() == facilitator
    final_speaker = spec.final_speaker.strip() or spec.next_speaker.strip()
    is_final_round = spec.round_no == spec.round_total

    order_line = (
        f"本轮顺序：{spec.speaker} -> {spec.next_speaker} -> {facilitator}"
        if not is_final_baton
        else f"本轮顺序：{spec.speaker} -> {facilitator}"
    )
    final_speaker_line = (
        f"本轮末棒：{final_speaker}"
        if final_speaker and final_speaker != facilitator
        else "本轮末棒：当前答题者"
    )

    if is_final_baton and not is_final_round:
        handback_line = (
            f"本轮结束后，请用 {fmt_mention(facilitator, next_tpl)} 回收主持。"
            "当前还未到最终轮次时，只允许主持人开启下一轮，不要请求直接收束全会或归拢成稿。"
        )
    elif is_final_baton:
        handback_line = (
            f"本轮结束后，请用 {fmt_mention(facilitator, next_tpl)} 回收主持，不要自己再开新轮。"
        )
    else:
        handback_line = f"完成后按末尾指令交棒给 {spec.next_speaker}，不要另写裸 @。"

    return "\n".join(
        [
            f"第 {spec.round_no}/{spec.round_total} 轮",
            f"当前答题者：{spec.speaker}",
            f"下一棒：{spec.next_speaker}",
            order_line,
            f"回收主持：{facilitator}",
            f"议题：{spec.topic}",
            f"本轮任务：{ask}",
            final_speaker_line,
            "你不是主持人，不要控场，不要替下一棒安排轮次。",
            "禁止回复接棒确认或轮到X；直接回答本轮任务。",
            f"若你是本轮末棒，完成本轮任务后只写 {fmt_mention(facilitator, next_tpl)}，不要自行总结整轮或开启下一轮。",
            "若当前不是第 N/N 轮，禁止要求主持人直接出制度稿、纪要、最终总结或宣布本次结束。",
            "若当前不是第 N/N 轮，末棒答完后只算交回主持，不算全会终结。",
            handback_line,
            fmt_mention(spec.speaker, mention_tpl),
            fmt_mention(spec.next_speaker, next_tpl),
        ]
    )


def main() -> int:
    args = build_parser().parse_args()
    if args.round_no < 1:
        raise SystemExit("--round-no must be >= 1")
    if args.round_total < args.round_no:
        raise SystemExit("--round-total must be >= --round-no")
    spec = BatonSpec(
        round_no=args.round_no,
        round_total=args.round_total,
        speaker=args.speaker.strip(),
        next_speaker=args.next_speaker.strip(),
        final_speaker=(args.final_speaker or args.next_speaker).strip(),
        facilitator=args.facilitator.strip(),
        topic=args.topic.strip(),
        mode=args.mode,
        focus=args.focus,
        custom_ask=args.custom_ask,
    )
    print(build_baton(spec, mention_tpl=args.mention_template, next_tpl=args.next_template))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
