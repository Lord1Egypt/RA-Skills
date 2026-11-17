#!/usr/bin/env python3
"""阶段 5：按 scene-boundaries.json 生成结构化 Markdown 输出。

核心功能：
- 读 scene-boundaries_N.json（主对话在阶段 4 写入）
- 读 transcript_N.json（阶段 2 输出的带时间戳 segments）
- 按场景边界切分 segments，生成 ## 标题（时间区间）+ 完整内容
- 输出 share/{标题}.md（每视频独立文件）
"""
from __future__ import annotations
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import read_json, write_json, format_timestamp, apply_error_corrections


def safe_filename(name: str) -> str:
    """生成安全的文件名。"""
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", name.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-.")
    return cleaned[:120] or "video"


def collect_segments_in_range(
    segments: list[dict], start_sec: float, end_sec: float
) -> list[str]:
    """收集时间范围内的 segment 文本。

    一个 segment 属于某场景的条件：segment.start >= scene.start 且 segment.start < scene.end
    """
    texts = []
    for seg in segments:
        seg_start = float(seg["start"])
        if seg_start >= start_sec - 0.1 and seg_start < end_sec - 0.1:
            texts.append(seg["text"])
    return texts


def collect_translations_in_range(
    translations: list[dict], start_sec: float, end_sec: float
) -> list[dict]:
    """v4.0: 收集时间范围内的翻译（译文 + 原文）。

    Returns:
        [{"translation": "中文译文", "source": "English text"}, ...]
    """
    result = []
    for t in translations:
        t_start = float(t.get("start", 0))
        if t_start >= start_sec - 0.1 and t_start < end_sec - 0.1:
            result.append({
                "translation": t.get("translation", ""),
                "source": t.get("source", ""),
            })
    return result


def build_markdown(
    transcript: dict,
    boundaries: dict,
    route_descriptions: dict | None = None,
    translation: dict | None = None,  # v4.0: 翻译数据
) -> str:
    """生成最终的 Markdown 文档。

    v4.0: 如果 translation 不为 None，输出双语对比格式。
    """
    title = transcript.get("title", "未知标题")
    author = transcript.get("author", "未知作者")
    source_url = transcript.get("source_url", "")
    duration = transcript.get("duration_sec", 0)
    segments = transcript.get("segments", [])
    today = datetime.now().strftime("%Y-%m-%d")

    route = boundaries.get("route", "explainer")
    route_reason = boundaries.get("route_reason", "")
    scenes = boundaries.get("scenes", [])

    # v4.0: 语言和翻译状态
    language = transcript.get("language", "unknown")
    source_type = transcript.get("source_type", "whisper")
    model_name = transcript.get("model", "whisper-small")
    is_bilingual = translation is not None and translation.get("translations")

    # v3.0: 根据 source_url 判断平台（支持四平台 + v4.0 全平台）
    if "bilibili.com" in source_url:
        source_label = "B站"
    elif "douyin.com" in source_url:
        source_label = "抖音"
    elif "xiaoyuzhoufm.com" in source_url:
        source_label = "小宇宙"
    elif "youtube.com" in source_url or "youtu.be" in source_url:
        source_label = "YouTube"
    elif "vimeo.com" in source_url:
        source_label = "Vimeo"
    elif "tiktok.com" in source_url:
        source_label = "TikTok"
    else:
        source_label = "未知平台"

    # 路由说明
    route_names = {
        "lesson": "教学课",
        "explainer": "科普解读",
        "conversation": "访谈对话",
        "demo": "操作演示",
        "narrative": "叙事讲述",
        "bulletin": "资讯速览",
    }
    route_label = f"{route}（{route_names.get(route, route)}）"

    # v4.0: 转录工具标注
    if source_type == "subtitle":
        transcribe_tool = f"平台字幕 ({model_name})"
    else:
        transcribe_tool = "faster-whisper (small) + opencc"

    # v4.0: 语言标注
    if is_bilingual:
        lang_label = f"{language} → 中文（双语对比）"
    elif language != "unknown" and language != "zh":
        lang_label = f"{language}（未翻译）"
    else:
        lang_label = "中文"

    # 文档头
    lines = [
        f"# {title}",
        "",
        f"> 作者: {author}",
        f"> 来源: {source_label}",
        f"> 原始链接: {source_url}",
        f"> 转录工具: {transcribe_tool}",
        f"> 转录日期: {today}",
        f"> 路由: {route_label}",
        f"> 路由原因: {route_reason}",
        f"> 时长: {format_timestamp(duration)}",
        f"> 场景数: {len(scenes)}",
        f"> 语言: {lang_label}",
        "",
        "---",
        "",
    ]

    # 场景目录
    if scenes:
        lines.append("## 目录")
        lines.append("")
        for scene in scenes:
            time_range = f"{format_timestamp(scene['start_sec'])}-{format_timestamp(scene['end_sec'])}"
            lines.append(f"{scene['id']}. [{scene['title']}](#{scene['id']:02d}-{safe_filename(scene['title']).lower()})")
        lines.append("")
        lines.append("---")
        lines.append("")

    # 翻译列表（v4.0: 双语模式时用）
    translations_list = (
        translation.get("translations", []) if is_bilingual else []
    )

    # 每个场景
    for scene in scenes:
        scene_id = int(scene["id"])
        scene_title = scene.get("title", f"场景 {scene_id}")
        start = float(scene["start_sec"])
        end = float(scene["end_sec"])
        reason = scene.get("reason", "")
        time_range = f"{format_timestamp(start)}-{format_timestamp(end)}"

        # 场景标题
        lines.append(f"## {scene_id:02d}. {scene_title}（{time_range}）")
        lines.append("")

        if is_bilingual and translations_list:
            # v4.0: 双语对比模式
            # 收集场景范围内的翻译单元
            scene_translations = collect_translations_in_range(
                translations_list, start, end
            )

            if not scene_translations:
                lines.append("（此场景无转录内容）")
                lines.append("")
            else:
                # 合并译文为一段（中文在前）
                translated_text = " ".join(
                    t["translation"] for t in scene_translations
                    if t.get("translation", "").strip()
                ).strip()
                # 合并原文为一段（英文紧跟其后 blockquote）
                source_text = " ".join(
                    t["source"] for t in scene_translations
                    if t.get("source", "").strip()
                ).strip()

                if translated_text:
                    lines.append(translated_text)
                    lines.append("")
                if source_text:
                    lines.append(f"> **原文**：{source_text}")
                    lines.append("")
        else:
            # 单语模式（原有逻辑）
            texts = collect_segments_in_range(segments, start, end)
            content = " ".join(texts).strip()
            # 应用错字修正（faster-whisper 在中文上的常见同音错字）
            content = apply_error_corrections(content)

            if not content:
                content = f"（此场景无转录内容）"

            lines.append(content)
            lines.append("")

        if reason:
            lines.append(f"<details><summary>切分原因</summary>{reason}</details>")
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def process_one(
    transcript_path: Path,
    boundaries_path: Path,
    share_dir: Path,
    translation_path: Path | None = None,  # v4.0: 翻译文件
) -> dict:
    """处理单个视频的输出。

    v4.0: 如果 translation_path 不为 None 且文件存在，输出双语对比格式。
    """
    transcript = read_json(transcript_path)
    if not boundaries_path.is_file():
        return {
            "video_id": transcript.get("video_id"),
            "title": transcript.get("title"),
            "success": False,
            "error": f"scene-boundaries 文件不存在: {boundaries_path}",
        }

    boundaries = read_json(boundaries_path)
    title = transcript.get("title", f"video_{transcript.get('video_id')}")

    # v4.0: 加载翻译（如果存在）
    translation = None
    is_bilingual = False
    if translation_path is not None and translation_path.is_file():
        translation = read_json(translation_path)
        # 确认 translations 列表非空且已完成
        if translation.get("translations") and translation.get("completed", True):
            is_bilingual = True

    print(f"\n[{transcript.get('video_id')}] 输出: {title}", flush=True)
    print(f"   路由: {boundaries.get('route')}", flush=True)
    print(f"   场景: {len(boundaries.get('scenes', []))}", flush=True)
    if is_bilingual:
        src_lang = translation.get("source_language", "unknown")
        tgt_lang = translation.get("target_language", "zh-CN")
        unit_count = len(translation.get("translations", []))
        print(f"   双语: {src_lang} → {tgt_lang} ({unit_count} units)", flush=True)

    md_content = build_markdown(
        transcript, boundaries, translation=translation
    )
    share_dir.mkdir(parents=True, exist_ok=True)
    out_path = share_dir / f"{safe_filename(title)}.md"
    out_path.write_text(md_content, encoding="utf-8")

    word_count = len(md_content)
    print(f"   ✅ {out_path.name} ({word_count} 字符)", flush=True)

    result = {
        "video_id": transcript.get("video_id"),
        "title": title,
        "success": True,
        "output_path": str(out_path),
        "scene_count": len(boundaries.get("scenes", [])),
        "word_count": word_count,
        "is_bilingual": is_bilingual,  # v4.0
    }
    if is_bilingual:
        result["source_language"] = translation.get("source_language")
        result["target_language"] = translation.get("target_language")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="阶段 5：按场景边界生成结构化 Markdown")
    parser.add_argument("--transcript-dir", type=Path, required=True, help="transcript/ 目录")
    parser.add_argument("--boundaries-dir", type=Path, required=True, help="scene-boundaries 所在目录（通常是 work/）")
    parser.add_argument("--output-dir", type=Path, required=True, help="输出根目录（share/ 子目录）")
    parser.add_argument(
        "--translation-dir",
        type=Path,
        default=None,
        help="v4.0: translation_N.json 所在目录（通常是 work/）。若未提供则自动在 boundaries-dir 同目录查找",
    )
    args = parser.parse_args()

    transcript_files = sorted(args.transcript_dir.glob("transcript_*.json"))
    if not transcript_files:
        print(f"❌ 未找到 transcript 文件: {args.transcript_dir}", file=sys.stderr)
        sys.exit(1)

    # v4.0: 翻译文件目录（默认在 boundaries-dir 同目录）
    translation_dir = args.translation_dir or args.boundaries_dir

    share_dir = args.output_dir / "share"
    results = []
    bilingual_count = 0
    for tf in transcript_files:
        idx = tf.stem.split("_")[1]
        boundaries_path = args.boundaries_dir / f"scene-boundaries_{idx}.json"
        # v4.0: 查找对应的 translation_N.json（可能不存在）
        translation_path = translation_dir / f"translation_{idx}.json"
        result = process_one(tf, boundaries_path, share_dir, translation_path)
        results.append(result)
        if result.get("is_bilingual"):
            bilingual_count += 1

    success = sum(1 for r in results if r.get("success"))
    failed = [r for r in results if not r.get("success")]
    print(f"\n📊 输出完成: {success}/{len(results)}", flush=True)
    if bilingual_count:
        print(f"   其中双语对比: {bilingual_count} 个", flush=True)
    if failed:
        print(f"⚠️ 失败 {len(failed)} 个（缺少 scene-boundaries）:", flush=True)
        for f in failed:
            print(f"   - {f['title']}: {f.get('error')}", flush=True)


if __name__ == "__main__":
    main()
