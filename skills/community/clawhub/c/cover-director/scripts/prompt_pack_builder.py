#!/usr/bin/env python3
"""Prompt pack builder for cover briefs.

Input: a structured JSON brief.
Output: Markdown prompt pack with:
- universal Chinese prompt
- English prompt
- Midjourney-style prompt
- SD/ComfyUI positive prompt
- negative prompt
- post-production layout checklist

This script does not call any image generation API.

Usage:
  python scripts/prompt_pack_builder.py tests/sample_brief.json --out prompt_pack.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


def get(d: Dict[str, Any], key: str, default: str = "") -> str:
    value = d.get(key, default)
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value if v)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value or default)


def palette(d: Dict[str, Any]) -> str:
    p = d.get("color_palette") or {}
    if not isinstance(p, dict):
        return str(p)
    parts = []
    for label in ["primary", "secondary", "accent"]:
        if p.get(label):
            parts.append(f"{label}: {p[label]}")
    return ", ".join(parts) if parts else "high contrast, clean palette"


def negative_list(d: Dict[str, Any]) -> List[str]:
    base = [
        "text in image",
        "watermark",
        "logo",
        "messy background",
        "blurry face",
        "low resolution",
        "distorted hands",
        "extra fingers",
        "over-smoothed plastic skin",
        "cartoon style unless requested",
    ]
    user_neg = d.get("negative") or []
    if isinstance(user_neg, str):
        user_neg = [user_neg]
    return list(dict.fromkeys([*base, *[str(x) for x in user_neg]]))


def render_pack(d: Dict[str, Any]) -> str:
    title = get(d, "title", "未命名封面")
    platform = get(d, "platform", "短视频平台")
    ratio = get(d, "ratio", "9:16")
    field = get(d, "field", "未指定领域")
    goal = get(d, "cover_goal", "涨点击")
    title_type = get(d, "title_type", "待判断")
    main_keyword = get(d, "main_keyword", "待提炼")
    support_text = get(d, "support_text", "")
    subject = get(d, "subject", "封面主体")
    expression = get(d, "expression", "匹配标题的清晰表情")
    gesture = get(d, "gesture", "指向标题区的自然手势")
    composition = get(d, "composition", "主体突出，标题区留白清晰")
    background = get(d, "background", "干净背景")
    lighting = get(d, "lighting", "明亮商业摄影光线")
    colors = palette(d)
    text_safe_area = get(d, "text_safe_area", "侧边或上方预留标题空间")
    style = get(d, "style", "真实商业封面摄影，高对比度，高清锐利")
    negatives = negative_list(d)

    cn_prompt = (
        f"为{platform}生成一张{ratio}比例的无字封面底图，主题领域是{field}，目标是{goal}。"
        f"封面主体：{subject}。表情：{expression}。动作：{gesture}。"
        f"构图：{composition}，{text_safe_area}，画面主焦点清晰。"
        f"背景：{background}。光影：{lighting}。色彩：{colors}。"
        f"整体风格：{style}。不要在图片中生成任何中文或英文文字，不要水印、logo、二维码，避免杂乱背景和畸形手。"
    )

    en_prompt = (
        f"Create a no-text thumbnail background for {platform}, aspect ratio {ratio}, field: {field}, goal: {goal}. "
        f"Main subject: {subject}. Expression: {expression}. Gesture: {gesture}. "
        f"Composition: {composition}, reserve clean text-safe area at {text_safe_area}, clear single focal point. "
        f"Background: {background}. Lighting: {lighting}. Color palette: {colors}. "
        f"Style: {style}, realistic commercial thumbnail photography, high contrast, sharp details. No text, no watermark, no logo."
    )

    mj_prompt = (
        f"{subject}, {expression}, {gesture}, {composition}, text-safe empty space at {text_safe_area}, "
        f"{background}, {lighting}, {colors}, {style}, realistic commercial thumbnail photography, high contrast, sharp details "
        f"--ar {ratio.replace(':', ':')} --style raw"
    )

    positive = (
        f"{subject}, {expression}, {gesture}, {composition}, clean text-safe area, {background}, {lighting}, "
        f"{colors}, {style}, realistic commercial photography, high contrast, sharp focus, detailed face"
    )
    negative = ", ".join(negatives)

    lines = [
        f"# Prompt Pack：{title}",
        "",
        "## 1. Brief",
        f"- 平台：{platform}",
        f"- 比例：{ratio}",
        f"- 领域：{field}",
        f"- 目标：{goal}",
        f"- 标题类型：{title_type}",
        f"- 最大关键词：{main_keyword}",
        f"- 辅助信息：{support_text}",
        "",
        "## 2. 通用中文无字底图提示词",
        "```text",
        cn_prompt,
        "```",
        "",
        "## 3. English Prompt",
        "```text",
        en_prompt,
        "```",
        "",
        "## 4. Midjourney-style Prompt",
        "```text",
        mj_prompt,
        "```",
        "",
        "## 5. SD/ComfyUI Positive Prompt",
        "```text",
        positive,
        "```",
        "",
        "## 6. Negative Prompt",
        "```text",
        negative,
        "```",
        "",
        "## 7. 后期排版清单",
        f"- 标题最大关键词：{main_keyword}",
        f"- 辅助信息：{support_text}",
        f"- 标题安全区：{text_safe_area}",
        "- 最大关键词使用粗黑体或标题黑，加入描边/色块保证小屏可读。",
        "- 辅助信息降级，不要抢最大关键词。",
        "- 缩小到手机缩略图后检查 3 秒内是否能看清主题。",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build multi-tool prompt pack from JSON brief.")
    parser.add_argument("input", type=Path, help="Structured JSON brief.")
    parser.add_argument("--out", type=Path, default=Path("prompt_pack.md"), help="Markdown output path.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Input not found: {args.input}", file=sys.stderr)
        return 2

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Input JSON must be an object.")
    except Exception as exc:
        print(f"Error reading JSON: {exc}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_pack(data), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
