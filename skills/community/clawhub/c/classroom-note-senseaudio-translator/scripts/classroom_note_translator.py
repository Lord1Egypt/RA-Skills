#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import textwrap
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests

SENSEAUDIO_ENDPOINT = "https://api.senseaudio.cn/v1/audio/transcriptions"
DEFAULT_MODEL = "sense-asr-pro"
DEFAULT_SUMMARY_PROVIDER = "local"
DEFAULT_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus"}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "lecture-note"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classroom Note Translator for OpenClaw")
    parser.add_argument("--audio", default="", help="Path to the audio file")
    parser.add_argument("--video", default="", help="Path to the video file; audio will be extracted automatically")
    parser.add_argument("--page-url", default="", help="Web page URL; media URL will be extracted and downloaded first")
    parser.add_argument("--title", default="", help="Lecture title or topic")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=["sense-asr", "sense-asr-pro", "sense-asr-deepthink", "sense-asr-lite"])
    parser.add_argument("--language", default="en", help="Source language code. For English lectures, use en.")
    parser.add_argument("--target-language", default="zh", help="Target translation language code")
    parser.add_argument("--timestamps", default="segment", choices=["none", "segment", "word", "both"])
    parser.add_argument("--speaker-diarization", action="store_true")
    parser.add_argument("--max-speakers", type=int, default=8)
    parser.add_argument("--enable-sentiment", action="store_true")
    parser.add_argument("--enable-punctuation", action="store_true")
    parser.add_argument("--enable-itn", action="store_true", default=True)
    parser.add_argument("--output-dir", required=True, help="User-specified output directory for generated files")
    parser.add_argument("--summary-provider", default=DEFAULT_SUMMARY_PROVIDER, choices=["local", "openai-compatible"])
    parser.add_argument("--openai-model", default="gpt-4o-mini")
    parser.add_argument("--export-notion", action="store_true")
    parser.add_argument("--notion-parent-page-id", default="")
    parser.add_argument("--export-obsidian", action="store_true")
    parser.add_argument("--obsidian-vault", default="")
    parser.add_argument("--obsidian-folder", default="Lecture Notes")
    return parser.parse_args()


def extension_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix.lower()


def content_type_to_extension(content_type: str) -> str:
    ctype = (content_type or "").split(";")[0].strip().lower()
    mapping = {
        "video/mp4": ".mp4",
        "video/webm": ".webm",
        "video/quicktime": ".mov",
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/mp4": ".m4a",
        "audio/aac": ".aac",
        "audio/flac": ".flac",
        "audio/ogg": ".ogg",
        "audio/opus": ".opus",
    }
    return mapping.get(ctype, "")


def infer_is_video(media_url: str, content_type: str = "") -> bool:
    ext = extension_from_url(media_url)
    if ext in VIDEO_EXTENSIONS:
        return True
    if ext in AUDIO_EXTENSIONS:
        return False
    ctype = (content_type or "").lower()
    if ctype.startswith("video/"):
        return True
    if ctype.startswith("audio/"):
        return False
    return True


def extract_media_url_from_page(page_url: str) -> str:
    resp = requests.get(page_url, headers=DEFAULT_HTTP_HEADERS, timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(f"Failed to fetch page {page_url}: {resp.status_code}")

    html = resp.text
    candidates: List[Tuple[int, str]] = []

    video_meta_patterns = [
        r'<meta[^>]+property=["\']og:video(?::url)?["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+name=["\']twitter:player:stream["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    audio_meta_patterns = [
        r'<meta[^>]+property=["\']og:audio(?::url)?["\'][^>]+content=["\']([^"\']+)["\']',
    ]

    for pattern in video_meta_patterns:
        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            candidates.append((100, urljoin(page_url, match.strip())))
    for pattern in audio_meta_patterns:
        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            candidates.append((90, urljoin(page_url, match.strip())))

    for tag_name, src in re.findall(
        r"<(video|audio|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>",
        html,
        flags=re.IGNORECASE,
    ):
        tag = tag_name.lower()
        score = 80 if tag == "video" else 70 if tag == "audio" else 60
        candidates.append((score, urljoin(page_url, src.strip())))

    if not candidates:
        raise RuntimeError("No downloadable video/audio source found in page HTML")

    def candidate_rank(item: Tuple[int, str]) -> Tuple[int, int]:
        score, url = item
        ext = extension_from_url(url)
        known_ext = 1 if (ext in VIDEO_EXTENSIONS or ext in AUDIO_EXTENSIONS) else 0
        return (score, known_ext)

    candidates.sort(key=candidate_rank, reverse=True)
    return candidates[0][1]


def download_media_file(media_url: str, temp_dir: Path) -> Tuple[Path, bool]:
    resp = requests.get(media_url, headers=DEFAULT_HTTP_HEADERS, stream=True, timeout=180)
    if resp.status_code >= 400:
        raise RuntimeError(f"Failed to download media {media_url}: {resp.status_code}")

    content_type = resp.headers.get("Content-Type", "")
    ext = extension_from_url(media_url) or content_type_to_extension(content_type)
    if not ext:
        ext = ".mp4" if infer_is_video(media_url, content_type) else ".mp3"

    file_path = temp_dir / f"page_media{ext}"
    with file_path.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return file_path, infer_is_video(str(file_path), content_type)


def resolve_media_input(args: argparse.Namespace) -> Tuple[Path, bool, Optional[tempfile.TemporaryDirectory[str]], Optional[str]]:
    audio = args.audio.strip()
    video = args.video.strip()
    page_url = args.page_url.strip()
    provided = [bool(audio), bool(video), bool(page_url)]
    if sum(provided) == 0:
        raise ValueError("Provide one input source: --audio, --video, or --page-url")
    if sum(provided) > 1:
        raise ValueError("Provide only one input source: --audio, --video, or --page-url")

    if audio:
        path = Path(audio).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        return path, False, None, None

    if video:
        path = Path(video).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        return path, True, None, None

    temp_dir_obj = tempfile.TemporaryDirectory(prefix="classroom_note_translator_page_")
    temp_dir = Path(temp_dir_obj.name)
    media_url = extract_media_url_from_page(page_url)
    media_path, is_video = download_media_file(media_url, temp_dir)
    return media_path, is_video, temp_dir_obj, media_url


def extract_audio_from_video(video_path: Path, temp_dir: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for --video input but was not found in PATH")

    output_path = temp_dir / f"{video_path.stem}_extracted_audio.mp3"
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-b:a",
        "64k",
        str(output_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed to extract audio: {proc.stderr.strip()}")
    return output_path


def build_timestamp_params(mode: str) -> List[Tuple[str, str]]:
    if mode == "none":
        return []
    if mode == "segment":
        return [("timestamp_granularities[]", "segment")]
    if mode == "word":
        return [("timestamp_granularities[]", "word")]
    return [("timestamp_granularities[]", "segment"), ("timestamp_granularities[]", "word")]


def call_senseaudio(args: argparse.Namespace, audio_path: Path) -> Dict[str, Any]:
    api_key = os.getenv("SENSEAUDIO_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SENSEAUDIO_API_KEY")

    headers = {"Authorization": f"Bearer {api_key}"}
    data: List[Tuple[str, str]] = [("model", args.model), ("response_format", "verbose_json")]

    if args.model != "sense-asr-deepthink":
        data.append(("language", args.language))
    if args.model != "sense-asr-lite":
        data.append(("target_language", args.target_language))
    if args.enable_itn and args.model != "sense-asr-deepthink":
        data.append(("enable_itn", "true"))
    if args.enable_punctuation and args.model in {"sense-asr", "sense-asr-pro"}:
        data.append(("enable_punctuation", "true"))
    if args.speaker_diarization and args.model in {"sense-asr", "sense-asr-pro"}:
        data.append(("enable_speaker_diarization", "true"))
    if args.model == "sense-asr-pro" and args.speaker_diarization:
        data.append(("max_speakers", str(args.max_speakers)))
    if args.enable_sentiment and args.model in {"sense-asr", "sense-asr-pro"}:
        data.append(("enable_sentiment", "true"))
    data.extend(build_timestamp_params(args.timestamps))

    with audio_path.open("rb") as f:
        files = {"file": (audio_path.name, f)}
        resp = requests.post(SENSEAUDIO_ENDPOINT, headers=headers, data=data, files=files, timeout=300)
    if resp.status_code >= 400:
        raise RuntimeError(f"SenseAudio API error {resp.status_code}: {resp.text}")
    return resp.json()


def extract_bilingual_segments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = payload.get("segments") or []
    if segments:
        out = []
        for seg in segments:
            out.append(
                {
                    "start": seg.get("start"),
                    "end": seg.get("end"),
                    "speaker": seg.get("speaker"),
                    "sentiment": seg.get("sentiment"),
                    "text": (seg.get("text") or "").strip(),
                    "translation": (seg.get("translation") or "").strip(),
                }
            )
        return out

    return [{"start": None, "end": None, "speaker": None, "sentiment": None, "text": (payload.get("text") or "").strip(), "translation": ""}]


def format_ts(v: Optional[float]) -> str:
    if v is None:
        return "--:--"
    total = int(round(v))
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def local_markdown_summary(title: str, segments: List[Dict[str, Any]], payload: Dict[str, Any]) -> str:
    merged_text = "\n".join(seg["text"] for seg in segments if seg["text"])
    merged_zh = "\n".join(seg["translation"] for seg in segments if seg.get("translation"))
    speakers = sorted({seg["speaker"] for seg in segments if seg.get("speaker")})

    # very lightweight heuristic extraction
    lines = [s.strip() for s in re.split(r"(?<=[.!?。！？])\s+", merged_zh or merged_text) if s.strip()]
    key_points = lines[:6]

    vocab_candidates = re.findall(r"\b[A-Za-z][A-Za-z\-]{3,}\b", merged_text)
    freq: Dict[str, int] = {}
    for word in vocab_candidates:
        w = word.lower()
        if w in {"that", "this", "with", "from", "have", "there", "their", "about", "which", "would", "could", "should", "because"}:
            continue
        freq[w] = freq.get(w, 0) + 1
    glossary = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:12]

    timeline = []
    for seg in segments[:20]:
        zh = seg.get("translation") or seg.get("text")
        zh = zh.replace("\n", " ").strip()
        if zh:
            timeline.append(f"- **{format_ts(seg.get('start'))}–{format_ts(seg.get('end'))}** {zh}")

    review_questions = []
    if key_points:
        review_questions.append(f"这节内容的核心主题是什么？")
    if len(key_points) > 1:
        review_questions.append(f"老师重点解释了哪些概念，它们之间的关系是什么？")
    if glossary:
        review_questions.append(f"术语 {glossary[0][0]} 和 {glossary[min(1, len(glossary)-1)][0]} 在课堂中的含义分别是什么？")

    summary_text = "\n".join(f"- {p}" for p in key_points) if key_points else "- 暂未提取到明确重点，请查看下方时间轴与原文。"
    glossary_text = "\n".join(f"- `{term}`：课堂中高频出现，建议结合上下文补充中文释义" for term, _ in glossary) or "- 暂无"
    timeline_text = "\n".join(timeline) or "- 暂无分段信息"
    review_text = "\n".join(f"- {q}" for q in review_questions) or "- 请用自己的话复述本节课的三个重点。"

    meta = [
        f"- 生成时间：{dt.datetime.now().isoformat(timespec='seconds')}",
        f"- 识别模型：{payload.get('model', 'unknown')}",
        f"- 说话人数：{len(speakers) if speakers else '未启用'}",
        f"- 音频时长：{payload.get('duration', 'unknown')}",
    ]

    excerpt_blocks = []
    for seg in segments[:12]:
        en = seg.get("text", "").strip()
        zh = seg.get("translation", "").strip()
        if not en:
            continue
        prefix = f"**{format_ts(seg.get('start'))}–{format_ts(seg.get('end'))}**"
        if seg.get("speaker"):
            prefix += f" [{seg['speaker']}]"
        excerpt = f"- {prefix}\n  - EN: {en}"
        if zh:
            excerpt += f"\n  - ZH: {zh}"
        excerpt_blocks.append(excerpt)

    return textwrap.dedent(f"""
    # {title}

    ## 元信息
    {chr(10).join(meta)}

    ## 中文摘要
    {summary_text}

    ## 关键要点
    {summary_text}

    ## 术语表
    {glossary_text}

    ## 时间轴梳理
    {timeline_text}

    ## 复习问题
    {review_text}

    ## 英文原文摘录
    {chr(10).join(excerpt_blocks) or '- 暂无'}

    ## 全文文本
    ### 英文原文
    ```text
    {merged_text[:12000]}
    ```

    ### 中文整理文本
    ```text
    {(merged_zh or '无直出翻译，可改用 openai-compatible 进一步翻译。')[:12000]}
    ```
    """).strip() + "\n"


def openai_chat(messages: List[Dict[str, str]], model: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY for openai-compatible summarization")

    resp = requests.post(
        base_url.rstrip("/") + "/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": 0.2},
        timeout=180,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenAI-compatible API error {resp.status_code}: {resp.text}")
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def llm_markdown_summary(title: str, segments: List[Dict[str, Any]], model: str) -> str:
    transcript = []
    for seg in segments:
        prefix = f"[{format_ts(seg.get('start'))}-{format_ts(seg.get('end'))}]"
        speaker = f" {seg['speaker']}" if seg.get("speaker") else ""
        line = f"{prefix}{speaker} EN: {seg.get('text','')}"
        if seg.get("translation"):
            line += f"\n{prefix}{speaker} ZH: {seg.get('translation','')}"
        transcript.append(line)

    prompt = f"""请把下面的课堂转录整理成高质量中文 Markdown 学习笔记。
要求：
1. 保留标题：{title}
2. 输出结构必须包含：
   - 元信息
   - 中文摘要
   - 关键要点
   - 术语表
   - 时间轴梳理
   - 复习问题
   - 英文原文摘录
3. 内容面向留学生复习使用，强调可读性与学习价值。
4. 如果原文中出现定义、公式、例子、老师提醒、作业要求，要尽量分出来。
5. 不要输出 JSON，只输出 Markdown。

课堂转录如下：
{chr(10).join(transcript)[:40000]}
"""
    return openai_chat([
        {"role": "system", "content": "你是一个擅长课堂笔记整理、双语学习总结和知识结构化的助手。"},
        {"role": "user", "content": prompt},
    ], model)


def export_to_notion(markdown_text: str, title: str, parent_page_id: str) -> Dict[str, Any]:
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise RuntimeError("Missing NOTION_TOKEN")
    if not parent_page_id:
        raise RuntimeError("Missing notion parent page id")

    paragraphs = [p.strip() for p in markdown_text.split("\n\n") if p.strip()]
    children = []
    for para in paragraphs[:80]:
        block_type = "heading_1" if para.startswith("# ") else "heading_2" if para.startswith("## ") else "bulleted_list_item" if para.startswith("- ") else "paragraph"
        text = para
        text = re.sub(r"^#+\s*", "", text)
        text = re.sub(r"^-\s*", "", text)
        children.append(
            {
                "object": "block",
                "type": block_type,
                block_type: {"rich_text": [{"type": "text", "text": {"content": text[:1900]}}]},
            }
        )

    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": title[:200]}}]}},
        "children": children,
    }

    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
        json=payload,
        timeout=60,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Notion API error {resp.status_code}: {resp.text}")
    return resp.json()


def export_to_obsidian(markdown_text: str, title: str, vault: Path, folder: str) -> Path:
    if not vault:
        raise RuntimeError("Missing Obsidian vault path")
    target_dir = vault / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    note_path = target_dir / f"{slugify(title)}.md"
    note_path.write_text(markdown_text, encoding="utf-8")
    return note_path


def main() -> None:
    args = parse_args()
    media_path, is_video, source_temp_dir_obj, source_media_url = resolve_media_input(args)
    temp_dirs: List[tempfile.TemporaryDirectory[str]] = []
    if source_temp_dir_obj is not None:
        temp_dirs.append(source_temp_dir_obj)
    audio_path = media_path
    if is_video:
        extract_temp_dir_obj = tempfile.TemporaryDirectory(prefix="classroom_note_translator_")
        temp_dirs.append(extract_temp_dir_obj)
        audio_path = extract_audio_from_video(media_path, Path(extract_temp_dir_obj.name))

    try:
        title = args.title.strip() or media_path.stem.replace("_", " ").replace("-", " ").title()
        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        payload = call_senseaudio(args, audio_path)
        payload["model"] = args.model
        segments = extract_bilingual_segments(payload)

        stem = slugify(title)
        raw_json_path = output_dir / f"{stem}_transcript.json"
        bilingual_path = output_dir / f"{stem}_bilingual.txt"
        markdown_path = output_dir / f"{stem}_summary.md"

        write_json(raw_json_path, payload)
        bilingual_text = "\n\n".join(
            f"[{format_ts(seg.get('start'))}-{format_ts(seg.get('end'))}]\nEN: {seg.get('text','')}\nZH: {seg.get('translation','')}" for seg in segments
        )
        bilingual_path.write_text(bilingual_text, encoding="utf-8")

        if args.summary_provider == "openai-compatible":
            markdown_text = llm_markdown_summary(title, segments, args.openai_model)
        else:
            markdown_text = local_markdown_summary(title, segments, payload)
        markdown_path.write_text(markdown_text, encoding="utf-8")

        notion_result = None
        if args.export_notion:
            notion_result = export_to_notion(markdown_text, title, args.notion_parent_page_id)

        obsidian_result = None
        if args.export_obsidian:
            vault_path = Path(args.obsidian_vault).expanduser().resolve()
            obsidian_result = export_to_obsidian(markdown_text, title, vault_path, args.obsidian_folder)

        result = {
            "title": title,
            "input_media": str(media_path),
            "input_page_url": args.page_url.strip() or None,
            "extracted_media_url": source_media_url,
            "audio": str(audio_path),
            "markdown": str(markdown_path),
            "raw_json": str(raw_json_path),
            "bilingual_text": str(bilingual_path),
            "notion_page_url": notion_result.get("url") if notion_result else None,
            "obsidian_note": str(obsidian_result) if obsidian_result else None,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        for temp_dir_obj in temp_dirs:
            temp_dir_obj.cleanup()


if __name__ == "__main__":
    main()
