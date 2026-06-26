#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频内容审核 Skill 脚本
输入音频/视频 → SenseAudio ASR 识别 → 敏感词检测 → 结构化报告

深度语义审核由 Claude 直接完成，本脚本不调用外部 LLM。
"""

import os
import re
import json
import argparse
import subprocess
import requests
import time
import glob
import sys

# ============== 配置 ==============
SENSEAUDIO_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
ASR_API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

ASR_MODELS = {
    "lite": "sense-asr-lite",
    "standard": "sense-asr",
    "pro": "sense-asr-pro",
}

# ============== 内置敏感词库 ==============
BUILTIN_SENSITIVE_WORDS = {
    "政治敏感": [
        "颠覆政权", "分裂国家", "恐怖主义", "极端主义",
        "邪教", "反华", "反动",
    ],
    "暴力相关": [
        "杀人", "砍人", "捅死", "炸弹", "枪击", "暗杀",
        "血腥", "虐待", "施暴", "殴打致死",
    ],
    "色情低俗": [
        "色情", "淫秽", "裸体", "性交易", "卖淫", "嫖娼",
        "约炮",
    ],
    "赌博诈骗": [
        "赌博", "赌场", "网赌", "诈骗", "杀猪盘", "传销",
        "非法集资", "洗钱", "黑彩",
    ],
    "毒品相关": [
        "吸毒", "贩毒", "冰毒", "大麻", "海洛因", "摇头丸",
        "制毒",
    ],
    "违禁广告": [
        "包治百病", "祖传秘方", "一夜暴富", "稳赚不赔",
        "免费领取", "内部消息", "保证收益",
    ],
}

AUDIO_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".aac", ".m4a"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".ts"}


def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def extract_audio(video_path: str, output_path: str):
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 提取音频失败:\n{result.stderr}")


def split_audio(audio_path: str, output_dir: str, chunk_duration: int = 55) -> list:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    duration = float(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip())

    if os.path.getsize(audio_path) <= MAX_FILE_SIZE:
        return [(audio_path, 0.0, duration)]

    chunks = []
    start = 0.0
    idx = 0
    while start < duration:
        chunk_path = os.path.join(output_dir, f"audit_chunk_{idx:04d}.wav")
        cmd = ["ffmpeg", "-y", "-i", audio_path,
               "-ss", str(start), "-t", str(chunk_duration),
               "-c", "copy", chunk_path]
        subprocess.run(cmd, capture_output=True, text=True)
        chunk_end = min(start + chunk_duration, duration)
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append((chunk_path, start, chunk_end))
        start += chunk_duration
        idx += 1

    return chunks


def asr_recognize(audio_path: str, api_key: str, model: str = "sense-asr",
                  language: str = None, enable_speaker: bool = False,
                  enable_sentiment: bool = False) -> dict:
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": model,
        "response_format": "verbose_json",
        "enable_punctuation": "true",
    }

    timestamp_granularities = []
    if model in ("sense-asr", "sense-asr-pro"):
        timestamp_granularities = [("timestamp_granularities[]", "segment")]
        if enable_speaker:
            data["enable_speaker_diarization"] = "true"
        if enable_sentiment:
            data["enable_sentiment"] = "true"

    if language and model != "sense-asr-deepthink":
        data["language"] = language

    data_tuples = [(k, v) for k, v in data.items()]
    data_tuples.extend(timestamp_granularities)

    with open(audio_path, "rb") as f:
        files = {"file": (os.path.basename(audio_path), f)}
        for retry in range(3):
            try:
                resp = requests.post(ASR_API_URL, headers=headers, files=files,
                                     data=data_tuples, timeout=120)
                if resp.status_code == 429:
                    wait = 10 * (retry + 1)
                    print(f"    速率限制，等待 {wait}s...")
                    time.sleep(wait)
                    f.seek(0)
                    continue
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                print(f"    ASR 重试 {retry+1}/3: {e}")
                time.sleep(5 * (retry + 1))
                f.seek(0)
        raise RuntimeError(f"ASR 识别失败: {audio_path}")


def keyword_scan(text: str, segments: list, custom_keywords: list = None,
                 offset: float = 0.0) -> list:
    """敏感词扫描"""
    hits = []
    all_keywords = {}
    for category, words in BUILTIN_SENSITIVE_WORDS.items():
        all_keywords[category] = list(words)
    if custom_keywords:
        all_keywords["自定义敏感词"] = custom_keywords

    if segments:
        for seg in segments:
            seg_text = seg.get("text", "")
            seg_start = seg.get("start", 0) + offset
            seg_end = seg.get("end", 0) + offset
            speaker = seg.get("speaker", "")

            for category, words in all_keywords.items():
                for word in words:
                    if word in seg_text:
                        idx = seg_text.index(word)
                        ctx_start = max(0, idx - 20)
                        ctx_end = min(len(seg_text), idx + len(word) + 20)
                        context = seg_text[ctx_start:ctx_end]
                        hits.append({
                            "category": category,
                            "keyword": word,
                            "context": f"...{context}...",
                            "time_start": format_time(seg_start),
                            "time_end": format_time(seg_end),
                            "seconds_start": round(seg_start, 2),
                            "seconds_end": round(seg_end, 2),
                            "speaker": speaker,
                            "severity": "high" if category in ("政治敏感", "暴力相关", "毒品相关") else "medium",
                        })
    else:
        for category, words in all_keywords.items():
            for word in words:
                if word in text:
                    idx = text.index(word)
                    ctx_start = max(0, idx - 30)
                    ctx_end = min(len(text), idx + len(word) + 30)
                    hits.append({
                        "category": category,
                        "keyword": word,
                        "context": f"...{text[ctx_start:ctx_end]}...",
                        "time_start": None,
                        "time_end": None,
                        "severity": "high" if category in ("政治敏感", "暴力相关", "毒品相关") else "medium",
                    })

    return hits


def determine_risk_level(keyword_hits: list) -> str:
    """根据关键词命中确定风险等级"""
    if not keyword_hits:
        return "safe"
    severity_order = {"low": 1, "medium": 2, "high": 3}
    max_severity = 0
    for hit in keyword_hits:
        s = severity_order.get(hit.get("severity", "medium"), 2)
        max_severity = max(max_severity, s)
    level_map = {0: "safe", 1: "low", 2: "medium", 3: "high"}
    return level_map.get(max_severity, "medium")


def generate_report(file_path: str, full_text: str, segments: list,
                    keyword_hits: list, risk_level: str, duration: float) -> dict:
    """生成结构化审核报告"""
    report = {
        "file": os.path.basename(file_path),
        "file_path": file_path,
        "duration": round(duration, 2),
        "duration_formatted": format_time(duration),
        "risk_level": risk_level,
        "total_issues": len(keyword_hits),
        "keyword_scan": {
            "total_hits": len(keyword_hits),
            "hits": keyword_hits,
            "categories_summary": {},
        },
        "transcript_length": len(full_text),
        "transcript_preview": full_text[:500] + ("..." if len(full_text) > 500 else ""),
    }

    cat_summary = {}
    for hit in keyword_hits:
        cat = hit["category"]
        cat_summary[cat] = cat_summary.get(cat, 0) + 1
    report["keyword_scan"]["categories_summary"] = cat_summary

    return report


def write_readable_report(report: dict, output_path: str):
    """生成人类可读的文本审核报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("           音频内容审核报告")
    lines.append("=" * 60)
    lines.append(f"文件: {report['file']}")
    lines.append(f"时长: {report['duration_formatted']}")
    lines.append(f"风险等级: {report['risk_level'].upper()}")
    lines.append(f"总问题数: {report['total_issues']}")
    lines.append("-" * 60)

    kw = report["keyword_scan"]
    lines.append(f"\n[关键词扫描] 命中 {kw['total_hits']} 处")
    if kw["categories_summary"]:
        for cat, count in kw["categories_summary"].items():
            lines.append(f"  - {cat}: {count} 处")
    if kw["hits"]:
        lines.append("")
        for i, hit in enumerate(kw["hits"], 1):
            time_info = f" [{hit['time_start']}~{hit['time_end']}]" if hit.get("time_start") else ""
            speaker_info = f" ({hit['speaker']})" if hit.get("speaker") else ""
            lines.append(f"  {i}. [{hit['severity'].upper()}] {hit['category']} — \"{hit['keyword']}\"{time_info}{speaker_info}")
            lines.append(f"     上下文: {hit['context']}")

    lines.append("\n" + "-" * 60)
    lines.append(f"转写文本预览: {report['transcript_preview']}")
    lines.append("=" * 60)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def audit_single_file(input_path: str, output_dir: str, api_key: str,
                      model: str = "standard", language: str = None,
                      enable_speaker: bool = False, enable_sentiment: bool = False,
                      custom_keywords: list = None) -> dict:
    """审核单个音频/视频文件"""
    basename = os.path.splitext(os.path.basename(input_path))[0]
    ext = os.path.splitext(input_path)[1].lower()
    is_video = ext in VIDEO_EXTENSIONS
    asr_model = ASR_MODELS.get(model, model)

    print(f"\n{'='*50}")
    print(f"审核文件: {input_path}")
    print(f"{'='*50}")

    # Step 1: 提取音频
    audio_path = input_path
    if is_video:
        print("[1] 从视频提取音频...")
        audio_path = os.path.join(output_dir, f"{basename}_audio.wav")
        extract_audio(input_path, audio_path)
        print(f"    完成: {audio_path}")
    else:
        print("[1] 音频文件，跳过提取")

    # Step 2: 切片 + ASR
    print("[2] ASR 语音识别...")
    chunks = split_audio(audio_path, output_dir)
    all_segments = []
    full_text_parts = []
    total_duration = 0.0

    for i, (chunk_path, offset, chunk_end) in enumerate(chunks):
        print(f"    ({i+1}/{len(chunks)}) 识别中... [偏移: {offset:.1f}s]")
        result = asr_recognize(
            chunk_path, api_key, model=asr_model,
            language=language, enable_speaker=enable_speaker,
            enable_sentiment=enable_sentiment,
        )
        segments = result.get("segments") or []
        text = result.get("text", "")
        total_duration = max(total_duration, chunk_end)

        for seg in segments:
            seg["start"] = seg.get("start", 0) + offset
            seg["end"] = seg.get("end", 0) + offset
            all_segments.append(seg)

        if text:
            full_text_parts.append(text)
            print(f"    文本: {text[:80]}...")

    full_text = "\n".join(full_text_parts)

    if not full_text.strip():
        print("    警告: 未识别到任何语音内容")
        return {"file": input_path, "risk_level": "safe", "total_issues": 0,
                "note": "未识别到语音内容"}

    # 保存转写文本
    transcript_path = os.path.join(output_dir, f"{basename}_transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"    转写文本: {transcript_path}")

    # Step 3: 敏感词扫描
    print("[3] 敏感词扫描...")
    keyword_hits = keyword_scan(full_text, all_segments, custom_keywords)
    print(f"    命中 {len(keyword_hits)} 处敏感词")

    # 情感分析结果
    if enable_sentiment:
        sentiment_alerts = [s for s in all_segments
                            if s.get("sentiment") and s["sentiment"] not in ("Neutral", "Happy")]
        if sentiment_alerts:
            print(f"    情感异常片段: {len(sentiment_alerts)} 处")
            for sa in sentiment_alerts[:5]:
                print(f"      [{format_time(sa['start'])}] {sa['sentiment']}: {sa['text'][:40]}...")

    # Step 4: 生成报告
    print("[4] 生成审核报告...")
    risk_level = determine_risk_level(keyword_hits)
    report = generate_report(input_path, full_text, all_segments,
                             keyword_hits, risk_level, total_duration)

    json_path = os.path.join(output_dir, f"{basename}_audit.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"    JSON: {json_path}")

    txt_path = os.path.join(output_dir, f"{basename}_audit.txt")
    write_readable_report(report, txt_path)
    print(f"    TXT:  {txt_path}")

    risk_emoji = {"safe": "OK", "low": "LOW", "medium": "MED", "high": "HIGH"}
    print(f"\n[{risk_emoji.get(risk_level, '?')}] 风险等级: {risk_level.upper()}")
    print(f"    总问题数: {report['total_issues']}")

    # 清理临时音频
    if is_video and os.path.exists(audio_path):
        os.remove(audio_path)
    for chunk_path, _, _ in chunks:
        if chunk_path != input_path and chunk_path != audio_path and os.path.exists(chunk_path):
            os.remove(chunk_path)

    return report


def interactive_select_output_dir(input_path: str, default_subdir: str = "output") -> str:
    """交互式选择输出目录"""
    if os.path.isdir(input_path):
        input_dir = os.path.abspath(input_path)
    else:
        input_dir = os.path.dirname(os.path.abspath(input_path))

    candidates = []
    # 1. 输入文件所在目录下的默认子目录
    candidates.append(os.path.join(input_dir, default_subdir))
    # 2. 当前工作目录下的默认子目录
    cwd_output = os.path.join(os.getcwd(), default_subdir)
    if os.path.abspath(cwd_output) != os.path.abspath(candidates[0]):
        candidates.append(cwd_output)
    # 3. 桌面
    desktop = os.path.join(os.path.expanduser("~"), "Desktop", default_subdir)
    candidates.append(desktop)
    # 4. 输入文件所在目录（直接输出，不创建子目录）
    candidates.append(input_dir)

    # 去重并保持顺序
    seen = set()
    unique = []
    for c in candidates:
        norm = os.path.normpath(c)
        if norm not in seen:
            seen.add(norm)
            unique.append(c)

    print("\n请选择输出目录:")
    for i, path in enumerate(unique, 1):
        exists_tag = " (已存在)" if os.path.isdir(path) else ""
        print(f"  [{i}] {path}{exists_tag}")
    print(f"  [{len(unique) + 1}] 手动输入路径")

    while True:
        try:
            choice = input(f"\n请输入编号 [1-{len(unique) + 1}]，直接回车选 [1]: ").strip()
            if not choice:
                return unique[0]
            idx = int(choice)
            if 1 <= idx <= len(unique):
                return unique[idx - 1]
            elif idx == len(unique) + 1:
                custom = input("请输入自定义输出路径: ").strip()
                if custom:
                    return os.path.abspath(custom)
                print("路径不能为空，请重新选择。")
            else:
                print(f"请输入 1-{len(unique) + 1} 之间的数字。")
        except ValueError:
            print("请输入有效数字。")
        except (EOFError, KeyboardInterrupt):
            print("\n使用默认路径。")
            return unique[0]


def main():
    parser = argparse.ArgumentParser(
        description="音频/视频内容审核工具 — 基于 SenseAudio ASR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python audio_audit.py audio.mp3
  python audio_audit.py video.mp4 --speaker --sentiment
  python audio_audit.py audio.mp3 --keywords "内幕,操盘,割韭菜"
  python audio_audit.py /path/to/media/ --output ./audit_results/
        """,
    )
    parser.add_argument("input", type=str, help="输入音频/视频文件或目录")
    parser.add_argument("--output", type=str, default=None, help="输出目录")
    parser.add_argument("--model", type=str, default="standard",
                        choices=["lite", "standard", "pro"],
                        help="ASR 模型 (默认: standard)")
    parser.add_argument("--language", type=str, default=None,
                        help="音频语言代码 (如 zh/en/ja)")
    parser.add_argument("--speaker", action="store_true", default=False,
                        help="启用说话人分离 (仅 standard/pro)")
    parser.add_argument("--sentiment", action="store_true", default=False,
                        help="启用情感分析 (仅 standard/pro)")
    parser.add_argument("--keywords", type=str, default=None,
                        help="自定义敏感词（逗号分隔）")
    parser.add_argument("--senseaudio-api-key", type=str, default=None,
                        help="SenseAudio API 密钥")

    args = parser.parse_args()

    api_key = args.senseaudio_api_key or SENSEAUDIO_API_KEY
    if not api_key:
        api_key = input("未检测到 SENSEAUDIO_API_KEY，请输入 SenseAudio API 密钥（https://senseaudio.cn 注册获取）: ").strip()
        if not api_key:
            print("错误: 未提供 API 密钥，无法继续。")
            return

    custom_keywords = None
    if args.keywords:
        custom_keywords = [w.strip() for w in args.keywords.split(",") if w.strip()]

    output_dir = args.output
    if output_dir is None:
        output_dir = interactive_select_output_dir(
            args.input, default_subdir="audit_output"
        )
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isdir(args.input):
        media_files = []
        for ext_set in (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS):
            for ext in ext_set:
                media_files.extend(glob.glob(os.path.join(args.input, f"*{ext}")))
        media_files.sort()

        if not media_files:
            print(f"错误: 目录 {args.input} 中未找到音视频文件")
            return

        print(f"批量审核模式: 共 {len(media_files)} 个文件")
        all_reports = []
        for fpath in media_files:
            report = audit_single_file(
                fpath, output_dir, api_key,
                model=args.model, language=args.language,
                enable_speaker=args.speaker, enable_sentiment=args.sentiment,
                custom_keywords=custom_keywords,
            )
            all_reports.append(report)

        summary_path = os.path.join(output_dir, "batch_summary.json")
        batch_summary = {
            "total_files": len(all_reports),
            "risk_distribution": {},
            "files": [],
        }
        for r in all_reports:
            level = r.get("risk_level", "unknown")
            batch_summary["risk_distribution"][level] = batch_summary["risk_distribution"].get(level, 0) + 1
            batch_summary["files"].append({
                "file": r.get("file", ""),
                "risk_level": level,
                "total_issues": r.get("total_issues", 0),
            })
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(batch_summary, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*50}")
        print(f"批量审核完成: {len(all_reports)} 个文件")
        print(f"风险分布: {batch_summary['risk_distribution']}")
        print(f"汇总报告: {summary_path}")

    elif os.path.isfile(args.input):
        audit_single_file(
            args.input, output_dir, api_key,
            model=args.model, language=args.language,
            enable_speaker=args.speaker, enable_sentiment=args.sentiment,
            custom_keywords=custom_keywords,
        )
    else:
        print(f"错误: 文件或目录不存在: {args.input}")


if __name__ == "__main__":
    main()
