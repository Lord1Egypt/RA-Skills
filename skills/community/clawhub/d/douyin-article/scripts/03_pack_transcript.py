#!/usr/bin/env python3
"""阶段 3：打包转录稿 + 生成切分工作表。

按 90 秒窗口预打包的可读转录稿设计。

核心产物：
1. takes_packed_N.md —— 按 90 秒窗口预打包的可读转录稿（带时间戳）
2. boundary-review_N.md —— 指导主对话如何切分的工作表（含 6 路由规则）

注意：本脚本不切分！切分由 TRAE 主对话在阶段 4 完成，写 scene-boundaries_N.json。
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import (
    read_json, write_json, format_timestamp,
    detect_language, needs_translation as _needs_translation,
)


# 90 秒预打包窗口
PACK_WINDOW_SECONDS = 90.0


# 抖音 6 路由模型
ROUTE_RULES = {
    "lesson": {
        "name": "教学课",
        "unit": "每个完整知识点/例句解析/技巧",
        "rule": "在知识点切换、例句开始、作业布置处切分。一个完整的教学单元为一个场景，不要按固定时长切。",
        "applies_to": "教学课、知识分享、口播讲解（如英语课、编程课、考研课）",
    },
    "explainer": {
        "name": "科普解读",
        "unit": "完整论点/例子/视觉功能",
        "rule": "在论点完成+清晰停顿处切分。保留完整论证链，不要在论证中途切。",
        "applies_to": "科普解读、论文解析、干货总结",
    },
    "conversation": {
        "name": "访谈对话",
        "unit": "完整问答/话题单元",
        "rule": "不按每次发言切，按完整话题切。一个问答或话题单元为一个场景。",
        "applies_to": "访谈、对话、问答、直播切片",
    },
    "demo": {
        "name": "操作演示",
        "unit": "操作步骤+可观察结果",
        "rule": "保留前置条件和结果。一个操作步骤+其结果为一个场景。",
        "applies_to": "教程演示、产品使用、操作指南",
    },
    "narrative": {
        "name": "叙事讲述",
        "unit": "叙事段落/情节转换",
        "rule": "在场景/时间/情绪转换处切分。保留叙事完整性。",
        "applies_to": "Vlog、故事讲述、情感朗读、剧情",
    },
    "bulletin": {
        "name": "资讯速览",
        "unit": "资讯条目/要点",
        "rule": "每条资讯独立成段。不要合并多条资讯。",
        "applies_to": "资讯速览、新闻摘要、干货清单",
    },
}


def route_heuristic(title: str) -> str:
    """根据标题启发式判断路由。

    v3.1：扩充英语教学课识别关键词（Lecture / Day N / 训练营 / 句法 / 句子分析 等）。
    """
    title_lower = title.lower()
    # v3.1: 教学课 - 扩充关键词覆盖英语教学、句法课、训练营等
    if any(k in title for k in [
        "第", "讲", "课程", "教学", "技巧", "速通", "精讲", "节课",
        # 英语/学科教学相关
        "Lecture", "lecture",  # 大学讲座
        "Day ", "Day0", "Day1",  # 百日训练营 Day N
        "训练营", "打卡",  # 训练营系列
        "句法", "句子", "长难句",  # 句法分析课
        "语法", "单词", "词汇",  # 语言学习课
        "精读", "例题", "题目",  # 题目解析
    ]):
        return "lesson"
    if any(k in title for k in ["解读", "分析", "原理", "为什么", "揭秘", "拆解"]):
        return "explainer"
    if any(k in title for k in ["访谈", "对话", "问答", "采访", "连线", "直播"]):
        return "conversation"
    if any(k in title for k in ["教程", "演示", "操作", "怎么用", "手把手", "实操"]):
        return "demo"
    if any(k in title for k in ["vlog", "Vlog", "日常", "故事", "记录", "一日", "旅行"]):
        return "narrative"
    if any(k in title for k in ["速览", "盘点", "清单", "新闻", "资讯", "汇总"]):
        return "bulletin"
    return "explainer"  # 默认


def group_cues(segments: list[dict], target_seconds: float = PACK_WINDOW_SECONDS) -> list[dict]:
    """按时间窗口预打包 segments。

    按 90 秒窗口预打包设计：不是最终切分，只是把转录稿打包成可读段落给主对话读。
    """
    if not segments:
        return []
    groups = []
    current: list[dict] = []
    group_start = float(segments[0]["start"])
    for seg in segments:
        seg_start = float(seg["start"])
        if current and seg_start - group_start >= target_seconds:
            groups.append({
                "start_sec": group_start,
                "end_sec": float(current[-1]["end"]),
                "texts": [s["text"] for s in current],
            })
            current = []
            group_start = seg_start
        current.append(seg)
    if current:
        groups.append({
            "start_sec": group_start,
            "end_sec": float(current[-1]["end"]),
            "texts": [s["text"] for s in current],
        })
    return groups


def build_takes_packed(transcript: dict, groups: list[dict]) -> str:
    """生成 takes_packed_N.md（可读的预打包转录稿）。"""
    # v4.0: 语言信息
    language = transcript.get("language", "unknown")
    source_type = transcript.get("source_type", "whisper")
    needs_trans = _needs_translation(transcript)

    lines = [
        f"# {transcript['title']} - 打包转录稿",
        "",
        f"> 作者: {transcript.get('author', '未知')}",
        f"> 来源: {transcript.get('source_url', '')}",
        f"> 时长: {transcript.get('duration_sec', 0):.1f}s",
        f"> 路由建议: {route_heuristic(transcript['title'])}",
        f"> segments 数: {len(transcript['segments'])}",
        f"> 语言: {language}" + ("（需翻译为中文）" if needs_trans else ""),
        f"> 来源: {source_type}",
        "",
        "---",
        "",
        "## 完整转录稿（按 90 秒窗口预打包）",
        "",
    ]
    for i, g in enumerate(groups, 1):
        time_range = f"{format_timestamp(g['start_sec'])}-{format_timestamp(g['end_sec'])}"
        lines.append(f"### 窗口 {i}（{time_range}）")
        lines.append("")
        lines.append(" ".join(g["texts"]))
        lines.append("")
    return "\n".join(lines) + "\n"


def build_boundary_review(transcript: dict, suggested_route: str) -> str:
    """生成 boundary-review_N.md（切分工作表，指导主对话如何切分）。

    按 90 秒窗口预打包设计生成的 boundary-review.md。
    """
    route_info = ROUTE_RULES[suggested_route]
    last_end = float(transcript["segments"][-1]["end"]) if transcript["segments"] else 0
    duration = transcript.get("duration_sec", last_end)

    lines = [
        "# 语义边界切分工作表",
        "",
        f"## 视频信息",
        f"- 标题: {transcript['title']}",
        f"- 时长: {duration:.1f}s ({format_timestamp(duration)})",
        f"- segments 数: {len(transcript['segments'])}",
        "",
        "## 路由建议",
        f"- 路由: `{suggested_route}`（{route_info['name']}）",
        f"- 适用: {route_info['applies_to']}",
        f"- 切分单位: {route_info['unit']}",
        f"- 切分规则: {route_info['rule']}",
        "",
        "## 你的任务",
        "",
        "1. 读 `takes_packed.md` 中的完整转录稿",
        "2. 按上述路由规则，在语义完成处提议边界点",
        "3. **不要按固定时长机械切分**（这是核心原则）",
        "4. **保留完整内容**：推理、例子、数字、限定条件、问答、重复强调都不要删",
        "5. 每个边界点要有明确的 reason（如\"完整论点+清晰停顿\"）",
        "",
        "## 可选路由（如果你想调整）",
        "",
    ]
    for key, info in ROUTE_RULES.items():
        marker = "✅" if key == suggested_route else "  "
        lines.append(f"{marker} `{key}` - {info['name']}：{info['applies_to']}")

    lines.extend([
        "",
        "## 输出格式",
        "",
        "将切分结果写入 `scene-boundaries.json`，格式：",
        "```json",
        "{",
        f'  "video_id": "{transcript["video_id"]}",',
        f'  "title": "{transcript["title"]}",',
        '  "route": "' + suggested_route + '",',
        '  "route_reason": "为什么选这个路由（一句话）",',
        '  "scenes": [',
        '    {',
        '      "id": 1,',
        '      "start_sec": 0.0,',
        '      "end_sec": 45.3,',
        '      "title": "场景标题（简短描述这段内容）",',
        '      "reason": "为什么在这里切（如：完整知识点结束+清晰过渡）"',
        '    }',
        "  ]",
        "}",
        "```",
        "",
        "## 约束",
        "",
        f"- 第一个场景的 start_sec 必须是 0.0",
        f"- 最后一个场景的 end_sec 必须覆盖到 {last_end:.3f}s（视频时长 {duration:.3f}s）",
        "- 场景之间不能有重叠或空隙",
        "- 每个场景的 title 要简短描述这段内容（如\"课程介绍\"、\"例句1解析\"）",
        "- reason 要具体（如\"知识点结束，进入例句解析\"而非\"场景切换\"）",
        "",
        "## Light-plus 原则（必须遵守）",
        "",
        "- **不是摘要**：必须保留推理、例子、数字、限定条件、分歧、问答、重复强调",
        "- **按语义边界切分**：不机械每 60/90 秒切一段",
        "- **保持时间顺序**：不重排内容",
        "",
    ])
    return "\n".join(lines) + "\n"


def process_one(transcript_path: Path, work_dir: Path) -> dict:
    """处理单个 transcript，生成 packed + review。"""
    transcript = read_json(transcript_path)
    idx = transcript["video_id"]
    title = transcript["title"]

    print(f"\n[{idx}] 打包: {title}", flush=True)

    # 预打包
    groups = group_cues(transcript["segments"])
    print(f"   预打包: {len(groups)} 个窗口", flush=True)

    # 路由建议
    suggested_route = route_heuristic(title)
    print(f"   路由建议: {suggested_route}", flush=True)

    # 生成产物
    work_dir.mkdir(parents=True, exist_ok=True)
    packed_path = work_dir / f"takes_packed_{idx}.md"
    review_path = work_dir / f"boundary-review_{idx}.md"

    packed_path.write_text(build_takes_packed(transcript, groups), encoding="utf-8")
    review_path.write_text(build_boundary_review(transcript, suggested_route), encoding="utf-8")

    print(f"   ✅ {packed_path.name}", flush=True)
    print(f"   ✅ {review_path.name}", flush=True)

    return {
        "video_id": idx,
        "title": title,
        "suggested_route": suggested_route,
        "packed_path": str(packed_path),
        "review_path": str(review_path),
        "group_count": len(groups),
        # v4.0: 语言 + 翻译标记
        "language": transcript.get("language", "unknown"),
        "source_type": transcript.get("source_type", "whisper"),
        "needs_translation": _needs_translation(transcript),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="阶段 3：打包转录稿 + 生成切分工作表")
    parser.add_argument("--transcript-dir", type=Path, required=True, help="transcript/ 目录")
    parser.add_argument("--output-dir", type=Path, required=True, help="输出根目录（work/ 子目录）")
    args = parser.parse_args()

    transcript_files = sorted(args.transcript_dir.glob("transcript_*.json"))
    if not transcript_files:
        print(f"❌ 未找到 transcript 文件: {args.transcript_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"📋 待打包: {len(transcript_files)} 个 transcript", flush=True)

    work_dir = args.output_dir / "work"
    results = []
    for tf in transcript_files:
        results.append(process_one(tf, work_dir))

    # 汇总
    summary_path = work_dir / "pack_summary.json"
    write_json(summary_path, {"items": results})
    print(f"\n📊 打包完成: {len(results)} 个，汇总: {summary_path}", flush=True)


if __name__ == "__main__":
    main()
