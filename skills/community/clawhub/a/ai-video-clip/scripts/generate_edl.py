#!/usr/bin/env python3
"""Generate EDL — 基于 transcript 和剪辑策略生成 Edit Decision List。

使用:
  python3 generate_edl.py --transcript transcript.json --strategy remove_fillers --output edl.json
  python3 generate_edl.py --transcript transcript.json --strategy extract_highlights --num-clips 5
  python3 generate_edl.py --transcript transcript.json --strategy custom --prompt "只保留关于产品的部分"
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

import yaml


# ---- 内置剪辑策略（LLM prompt 模板） ----

STRATEGY_PROMPTS = {
    "remove_fillers": """你是一个专业的视频剪辑师。请分析以下视频转录文本，生成一个 Edit Decision List (EDL)。

目标: 去除所有口癖/填充词/长静音，同时保持内容流畅。

规则:
1. 删除包含以下填充词的独立短语: umm, uh, 嗯, 呃, 那个, 然后(作填充), 就是说, 就是, 对吧
2. 如果填充词嵌入在有效句子中间，保留该句子但缩小时间窗口以跳过填充词
3. 任何超过 {silence_threshold}s 的静音片段，裁剪为 {silence_keep}s
4. 保留说话人切换处的自然停顿
5. 保持原视频的叙事结构

转录:
{transcript_text}

请返回 JSON 格式的 Edit Decision List:
{{
  "edits": [
    {{"type": "keep", "source": "...", "start": 0.0, "end": 5.0, "reason": "开场白"}},
    {{"type": "keep", "source": "...", "start": 5.8, "end": 12.3, "reason": "核心观点"}}
  ]
}}""",

    "extract_highlights": """你是一个专业的视频剪辑师。请分析以下视频转录文本，提取 {num_clips} 个最精彩的高光片段。

目标: 从长视频中找出最有价值的片段 - 精彩观点/转折/总结/数据/笑声/惊喜时刻。

规则:
1. 每个片段 {min_duration}-{max_duration}s
2. 优先选择: 关键结论、精彩论述、数据展示、幽默时刻、转折点
3. 避免选择: 开场寒暄、重复内容、冗长铺垫
4. 片段应独立完整（自包含一个完整的意思）
5. 提供每个选择的理由

转录:
{transcript_text}

请返回 JSON:
{{
  "edits": [
    {{"type": "keep", "source": "...", "start": 120.5, "end": 155.0, "reason": "总结核心方法论，信息密度最高"}}
  ]
}}""",

    "condense": """你是一个专业的视频剪辑师。请将以下视频内容精简到约 {target_duration} 秒。

目标: 保留最核心信息，删除冗余铺陈。

规则:
1. 保留每个主题的主题句
2. 保留重要结论和关键数据
3. 删除重复表达和展开细节
4. 保持逻辑连贯性
5. 维持原来的叙述顺序

转录:
{transcript_text}

请返回 JSON 格式 EDL。""",

    "topic_splits": """你是一个专业的视频编辑。请将以下视频按主题拆分为独立片段。

目标: 识别语义边界，切分为独立主题。

规则:
1. 检测主题转换信号（总结类话语、过渡词、话题切换）
2. 每个主题片段 {min_segment_duration}s 以上
3. 切分点在自然停顿处
4. 每个片段开头重新引入背景

转录:
{transcript_text}

请返回 JSON EDL。""",

    "social_clip": """你是一个短视频剪辑师。请为 {platform} 平台制作一个 {max_duration}s 以内的短视频。

目标: 从长内容中提取最吸引人的片段，适配短视频平台。

规则:
1. 开头 3s 必须有 hook（亮点/悬念/问题）
2. 主体内容精简有力
3. 总时长不超过 {max_duration}s
4. 优先选高信息密度/强情绪的片段

转录:
{transcript_text}

请返回 JSON EDL。""",
}


def load_strategies_yaml(path: str) -> dict:
    """加载剪辑策略模板文件。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def load_transcript(path: str) -> dict:
    """加载转录 JSON 文件。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def transcript_to_text(transcript: dict) -> str:
    """将 transcript JSON 转为紧凑文本（供 LLM prompt 使用）。"""
    lines = []
    lines.append(f"Source: {transcript.get('source', 'unknown')}")
    lines.append(f"Duration: {transcript.get('duration', 0):.1f}s")
    lines.append(f"Language: {transcript.get('language', 'unknown')}")
    lines.append(f"Total phrases: {len(transcript.get('phrases', []))}")
    lines.append("")

    for phrase in transcript.get("phrases", []):
        start = phrase["start"]
        end = phrase["end"]
        speaker = phrase.get("speaker", "S0")
        text = phrase.get("text", "")
        conf = phrase.get("confidence", 0)
        lines.append(f"[{start:07.2f}-{end:07.2f}] {speaker} (conf:{conf:.2f}) {text}")

    return "\n".join(lines)


def build_prompt(strategy_name: str, transcript_text: str, params: dict,
                 strategies_yaml: dict) -> str:
    """构建发送给 LLM 的 prompt。"""
    if strategy_name in STRATEGY_PROMPTS:
        template = STRATEGY_PROMPTS[strategy_name]
    else:
        template = """你是一个专业的视频剪辑师。请根据以下要求分析视频转录并生成 EDL。

剪辑要求: {custom_prompt}

转录:
{transcript_text}

请返回 JSON 格式 EDL。"""

    # 从 YAML 模板填充默认参数
    yaml_params = {}
    raw_strategies = strategies_yaml.get("strategies", {})
    if strategy_name in raw_strategies:
        yaml_params = raw_strategies[strategy_name].get("parameters", {})

    # 用传入参数覆盖 YAML 默认值
    merged = {**yaml_params, **params}

    prompt = template.format(
        transcript_text=transcript_text,
        **merged,
        custom_prompt=params.get("custom_prompt", "无特殊要求"),
    )

    return prompt


def validate_edl(edl: dict, transcript: dict) -> tuple:
    """验证 EDL 的合理性。返回 (is_valid, issues)。"""
    issues = []
    total_duration = transcript.get("duration", 0)
    source = transcript.get("source", "unknown")

    edits = edl.get("edits", [])
    if not edits:
        return False, ["EDL 没有任何编辑指令"]

    for i, edit in enumerate(edits):
        start = edit.get("start", 0)
        end = edit.get("end", 0)

        if start < 0:
            issues.append(f"编辑 #{i}: start < 0")
        if end > total_duration:
            issues.append(f"编辑 #{i}: end ({end}) 超出视频时长 ({total_duration})")
        if end <= start:
            issues.append(f"编辑 #{i}: end ({end}) <= start ({start})")
        if edit.get("type") not in ("keep", "cut", "transition", "overlay",
                                     "caption", "color_grade", "audio_fade"):
            issues.append(f"编辑 #{i}: 未知类型 '{edit.get('type')}'")

    # 检查重叠
    sorted_edits = sorted(edits, key=lambda e: e.get("start", 0))
    for i in range(1, len(sorted_edits)):
        if sorted_edits[i].get("start", 0) < sorted_edits[i - 1].get("end", 0):
            issues.append(f"编辑 #{i} 与 #{i-1} 时间重叠")

    return len(issues) == 0, issues


def create_edl_template(transcript: dict, strategy_name: str,
                         params: dict) -> dict:
    """创建 EDL 模板框架。"""
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "sources": [
            {
                "id": "src0",
                "path": transcript.get("source", ""),
                "duration": transcript.get("duration", 0),
                "transcript": "",
            }
        ],
        "strategy": {
            "name": strategy_name,
            "description": "",
            "parameters": params,
        },
        "edits": [],
        "output": {
            "path": "edit/final.mp4",
            "format": "16:9",
        },
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="基于 transcript 生成 Edit Decision List (EDL)")
    p.add_argument("--transcript", required=True, help="转录 JSON 文件路径")
    p.add_argument("--strategy", default="remove_fillers",
                   choices=["remove_fillers", "extract_highlights", "condense",
                            "topic_splits", "social_clip", "custom"],
                   help="剪辑策略")
    p.add_argument("--num-clips", type=int, default=3, help="提取片段数")
    p.add_argument("--target-duration", type=float, default=300,
                   help="目标总时长（秒）")
    p.add_argument("--platform", default="douyin",
                   help="目标平台 (douyin/tiktok/bilibili/youtube)")
    p.add_argument("--prompt", default="",
                   help="自定义剪辑要求（strategy=custom 时使用）")
    p.add_argument("--strategies-yaml",
                   default=None,
                   help="剪辑策略模板文件路径")
    p.add_argument("--output", default="edl.json", help="输出 EDL 文件")
    p.add_argument("--dry-run", action="store_true",
                   help="仅生成 prompt，不调用 LLM")
    args = p.parse_args()

    transcript = load_transcript(args.transcript)
    transcript_text = transcript_to_text(transcript)

    # 加载策略模板
    strategies_yaml = {}
    if args.strategies_yaml:
        strategies_yaml = load_strategies_yaml(args.strategies_yaml)
    else:
        # 尝试默认路径
        default_yaml = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "templates", "clip_strategies.yaml")
        if os.path.exists(default_yaml):
            strategies_yaml = load_strategies_yaml(default_yaml)

    params = {
        "num_clips": args.num_clips,
        "target_duration": args.target_duration,
        "platform": args.platform,
        "min_duration": 15,
        "max_duration": 120,
        "silence_threshold": 1.5,
        "silence_keep": 0.3,
        "min_segment_duration": 60,
        "custom_prompt": args.prompt,
    }

    prompt = build_prompt(args.strategy, transcript_text, params, strategies_yaml)

    if args.dry_run:
        print("=" * 60)
        print("Generated Prompt for LLM:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        print(f"\nPrompt length: {len(prompt)} characters")
        print(f"Transcript: {len(transcript.get('phrases', []))} phrases")
        print(f"\n请将此 prompt 发送给 LLM，获取 EDL JSON，然后保存到 {args.output}")
    else:
        # 创建 EDL 模板
        edl = create_edl_template(transcript, args.strategy, params)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(edl, f, ensure_ascii=False, indent=2)
        print(f"EDL 模板已生成: {args.output}")
        print(f"策略: {args.strategy}")
        print(f"转录: {len(transcript.get('phrases', []))} phrases")
        print(f"\n下一步:")
        print(f"  1. 使用 --dry-run 查看 LLM prompt")
        print(f"  2. 将 prompt 发送给 LLM 获取完整的 EDL JSON")
        print(f"  3. 用 render_edl.py 渲染最终视频")
