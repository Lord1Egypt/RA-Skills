#!/usr/bin/env python3
"""
YouTube 视频下载 + 音频转录 + 中英对照翻译

功能：
1. 使用 yt-dlp 下载 YouTube 视频（最佳质量）
2. 使用 OpenAI Whisper 将音频转录为文字
3. 如果是英文，使用 AI 翻译成中文（一段英文原文 + 一段中文翻译的对照格式）
4. 输出 Markdown 格式的文字稿

使用方式：
  python3 yt_download_transcribe.py <YouTube URL> --output-dir <输出目录>

依赖：
  pip3 install yt-dlp openai-whisper openai
  brew install ffmpeg
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing = []

    # 检查 yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"],
                       capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("yt-dlp (brew install yt-dlp)")

    # 检查 whisper
    try:
        import whisper  # noqa: F401
    except ImportError:
        missing.append("openai-whisper (pip3 install openai-whisper)")

    # 检查 ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("ffmpeg (brew install ffmpeg)")

    if missing:
        print("❌ 缺少以下依赖：")
        for dep in missing:
            print(f"   - {dep}")
        sys.exit(1)


def get_video_info(url: str, cookies_from_browser: str | None = "chrome") -> dict:
    """获取视频元信息（标题、时长、频道等）"""
    print("📋 获取视频信息...")
    cmd = ["yt-dlp", "--dump-json", "--no-download"]
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # 如果带 cookies 失败，尝试不带 cookies
        if cookies_from_browser:
            print("   ⚠️  使用浏览器 cookies 失败，尝试不带 cookies...")
            cmd_no_cookies = ["yt-dlp", "--dump-json", "--no-download", url]
            result = subprocess.run(cmd_no_cookies, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 获取视频信息失败: {result.stderr}")
            sys.exit(1)

    # 解析 JSON（跳过 stderr 警告行，只取最后一行 JSON）
    stdout_lines = result.stdout.strip().split('\n')
    json_line = stdout_lines[-1] if stdout_lines else ""
    info = json.loads(json_line)
    return {
        "title": info.get("title", "Unknown"),
        "channel": info.get("channel", info.get("uploader", "Unknown")),
        "upload_date": info.get("upload_date", ""),
        "duration": info.get("duration", 0),
        "description": info.get("description", ""),
        "url": url,
        "webpage_url": info.get("webpage_url", url),
        "thumbnail": info.get("thumbnail", ""),
        "view_count": info.get("view_count", 0),
        "like_count": info.get("like_count", 0),
    }


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    # 替换文件名不合法字符
    name = re.sub(r'[/\\:*?"<>|]', '-', name)
    # 去除首尾空格和点
    name = name.strip(' .')
    # 限制长度
    if len(name) > 200:
        name = name[:200]
    return name


def download_video(url: str, output_dir: str, title: str,
                   cookies_from_browser: str | None = "chrome") -> str:
    """下载 YouTube 视频，返回视频文件路径"""
    safe_title = sanitize_filename(title)
    output_template = os.path.join(output_dir, f"{safe_title}.%(ext)s")

    print(f"⬇️  下载视频: {title}")
    print(f"   输出目录: {output_dir}")

    # 优先使用 HLS(m3u8) 格式避免 YouTube DASH 403 错误
    # 95-1: 720p HLS, 94-1: 480p HLS, 93-1: 360p HLS
    # 回退到传统 DASH 格式
    cmd = [
        "yt-dlp",
        "-f", "95-1/94-1/93-1/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--no-playlist",
        "--progress",
        "--newline",
    ]
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    cmd.append(url)

    result = subprocess.run(
        cmd,
        capture_output=False,  # 显示下载进度
        text=True
    )

    if result.returncode != 0:
        print("❌ 视频下载失败")
        sys.exit(1)

    # 找到下载的视频文件
    video_file = os.path.join(output_dir, f"{safe_title}.mp4")
    if not os.path.exists(video_file):
        # 尝试查找其他可能的文件名
        for f in os.listdir(output_dir):
            if f.endswith(('.mp4', '.mkv', '.webm')) and safe_title[:20] in f:
                video_file = os.path.join(output_dir, f)
                break

    if not os.path.exists(video_file):
        print("❌ 找不到下载的视频文件")
        sys.exit(1)

    file_size = os.path.getsize(video_file) / (1024 * 1024)
    print(f"   ✅ 下载完成: {os.path.basename(video_file)} ({file_size:.1f} MB)")
    return video_file


def extract_audio(video_path: str) -> str:
    """从视频中提取音频（WAV 格式，Whisper 推荐）"""
    audio_path = os.path.splitext(video_path)[0] + ".wav"

    if os.path.exists(audio_path):
        print(f"   ⏭️  音频文件已存在，跳过提取")
        return audio_path

    print("🎵 提取音频...")
    result = subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vn",  # 不要视频
            "-acodec", "pcm_s16le",  # WAV 格式
            "-ar", "16000",  # 16kHz 采样率（Whisper 推荐）
            "-ac", "1",  # 单声道
            "-y",  # 覆盖已有文件
            audio_path
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"❌ 音频提取失败: {result.stderr}")
        sys.exit(1)

    print(f"   ✅ 音频提取完成: {os.path.basename(audio_path)}")
    return audio_path


def transcribe_audio(audio_path: str, model_name: str = "base") -> dict:
    """使用 Whisper 转录音频"""
    import whisper

    print(f"🎙️  使用 Whisper ({model_name}) 转录音频...")
    print(f"   这可能需要几分钟，请耐心等待...")

    start_time = time.time()

    model = whisper.load_model(model_name)
    result = model.transcribe(
        audio_path,
        verbose=True,  # 显示转录进度
        language=None,  # 自动检测语言
        task="transcribe",
    )

    elapsed = time.time() - start_time
    print(f"   ✅ 转录完成（耗时 {elapsed:.1f}s）")
    print(f"   检测到语言: {result.get('language', 'unknown')}")

    return result


def format_timestamp(seconds: float) -> str:
    """将秒数转为 HH:MM:SS 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def merge_segments_to_paragraphs(segments: list, max_gap: float = 2.0,
                                  max_duration: float = 60.0) -> list:
    """
    将 Whisper 的细粒度 segments 合并为段落。
    合并规则：
    - 如果两个相邻 segment 之间的间隔 < max_gap 秒，合并
    - 如果合并后的段落时长超过 max_duration 秒，强制断开
    - 遇到句号/问号/感叹号结尾时，倾向断开
    """
    if not segments:
        return []

    paragraphs = []
    current = {
        "start": segments[0]["start"],
        "end": segments[0]["end"],
        "text": segments[0]["text"].strip(),
    }

    for seg in segments[1:]:
        gap = seg["start"] - current["end"]
        duration = seg["end"] - current["start"]
        text = seg["text"].strip()

        # 判断是否需要断开
        ends_with_punct = current["text"].rstrip().endswith(('.', '?', '!', '。', '？', '！'))
        should_break = (
            gap > max_gap or
            duration > max_duration or
            (ends_with_punct and gap > 0.5)
        )

        if should_break:
            paragraphs.append(current)
            current = {
                "start": seg["start"],
                "end": seg["end"],
                "text": text,
            }
        else:
            current["end"] = seg["end"]
            current["text"] += " " + text

    paragraphs.append(current)
    return paragraphs


def translate_paragraphs(paragraphs: list, source_lang: str) -> list:
    """
    使用 OpenAI API 将段落翻译为中文。
    分批翻译以避免 token 限制。
    返回翻译后的段落列表（与输入对应）。
    """
    if source_lang == "zh" or source_lang == "Chinese":
        print("   ℹ️  源语言为中文，跳过翻译")
        return [p["text"] for p in paragraphs]

    print(f"🌐 翻译段落（{source_lang} → 中文）...")

    # 检查 OpenAI API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("   ⚠️  未设置 OPENAI_API_KEY，跳过翻译")
        return [None] * len(paragraphs)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except ImportError:
        print("   ⚠️  未安装 openai 库，跳过翻译")
        return [None] * len(paragraphs)

    translations = []
    batch_size = 10  # 每批翻译 10 个段落

    for i in range(0, len(paragraphs), batch_size):
        batch = paragraphs[i:i + batch_size]
        batch_texts = []
        for j, p in enumerate(batch):
            batch_texts.append(f"[{j + 1}] {p['text']}")

        prompt = (
            "将以下编号的段落翻译为中文。保持编号格式，每段翻译独立一行。\n"
            "翻译要求：自然流畅的中文表达，专业术语保留英文并附中文注释。\n\n"
            + "\n".join(batch_texts)
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个专业的翻译员，擅长将英文技术内容翻译为准确、自然的中文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
            reply = response.choices[0].message.content.strip()

            # 解析翻译结果
            batch_translations = []
            lines = reply.split('\n')
            current_trans = ""
            for line in lines:
                # 匹配 [N] 开头的行
                match = re.match(r'^\[(\d+)\]\s*(.+)', line.strip())
                if match:
                    if current_trans:
                        batch_translations.append(current_trans.strip())
                    current_trans = match.group(2)
                elif line.strip():
                    current_trans += " " + line.strip()
            if current_trans:
                batch_translations.append(current_trans.strip())

            # 确保数量匹配
            while len(batch_translations) < len(batch):
                batch_translations.append(None)

            translations.extend(batch_translations[:len(batch)])

        except Exception as e:
            print(f"   ⚠️  翻译批次 {i // batch_size + 1} 失败: {e}")
            translations.extend([None] * len(batch))

        # 显示进度
        done = min(i + batch_size, len(paragraphs))
        print(f"   翻译进度: {done}/{len(paragraphs)} 段")

    return translations


def generate_markdown(video_info: dict, paragraphs: list,
                      translations: list | None,
                      detected_language: str) -> str:
    """
    生成 Markdown 格式的文字稿。
    如果有翻译，采用一段英文原文 + 一段中文翻译的对照格式。
    """
    lines = []

    # 标题
    title = video_info["title"]
    lines.append(f"# {title}")
    lines.append("")

    # 元信息
    lines.append(f"**频道**: {video_info['channel']}")
    if video_info.get("upload_date"):
        date_str = video_info["upload_date"]
        if len(date_str) == 8:
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        lines.append(f"**发布日期**: {date_str}")
    if video_info.get("duration"):
        lines.append(f"**时长**: {format_timestamp(video_info['duration'])}")
    lines.append(f"**原始链接**: {video_info['webpage_url']}")
    lines.append(f"**转录语言**: {detected_language}")
    lines.append("")
    lines.append("---")
    lines.append("")

    description = (video_info.get("description") or "").strip()
    if description:
        lines.append("## 视频介绍")
        lines.append("")
        for para in description.split("\n"):
            para = para.strip()
            if para:
                lines.append(para)
                lines.append("")
        lines.append("---")
        lines.append("")

    # 正文
    is_bilingual = translations and any(t is not None for t in translations)

    if is_bilingual:
        lines.append("## 逐字稿（中英对照）")
        lines.append("")
        lines.append("> 以下内容采用「英文原文 + 中文翻译」对照排列。")
        lines.append("")

        for i, para in enumerate(paragraphs):
            timestamp = format_timestamp(para["start"])
            # 英文原文
            lines.append(f"**[{timestamp}]**")
            lines.append("")
            lines.append(para["text"])
            lines.append("")
            # 中文翻译
            if i < len(translations) and translations[i]:
                lines.append(f"🇨🇳 {translations[i]}")
                lines.append("")
            lines.append("---")
            lines.append("")
    else:
        lines.append("## 逐字稿")
        lines.append("")

        for para in paragraphs:
            timestamp = format_timestamp(para["start"])
            lines.append(f"**[{timestamp}]** {para['text']}")
            lines.append("")

    return "\n".join(lines)


def save_meta_json(video_info: dict, output_path: str,
                   detected_language: str, paragraph_count: int,
                   video_file: str | None = None):
    """保存元信息 JSON"""
    meta = {
        "url": video_info["webpage_url"],
        "title": video_info["title"],
        "channel": video_info["channel"],
        "upload_date": video_info.get("upload_date", ""),
        "duration": video_info.get("duration", 0),
        "description": video_info.get("description", "")[:500],
        "thumbnail": video_info.get("thumbnail", ""),
        "view_count": video_info.get("view_count", 0),
        "like_count": video_info.get("like_count", 0),
        "detected_language": detected_language,
        "paragraph_count": paragraph_count,
        "video_file": video_file,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="下载 YouTube 视频 + 转录 + 翻译"
    )
    parser.add_argument("url", help="YouTube 视频 URL")
    parser.add_argument(
        "--output-dir", "-o", default=".",
        help="输出目录（默认当前目录）"
    )
    parser.add_argument(
        "--whisper-model", "-m", default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper 模型大小（默认 base，越大越准但越慢）"
    )
    parser.add_argument(
        "--skip-download", action="store_true",
        help="跳过视频下载（使用已下载的视频）"
    )
    parser.add_argument(
        "--skip-translate", action="store_true",
        help="跳过翻译步骤"
    )
    parser.add_argument(
        "--keep-audio", action="store_true",
        help="保留提取的音频文件（默认删除）"
    )
    parser.add_argument(
        "--cookies-from-browser", default="chrome",
        help="从哪个浏览器获取 cookies（默认 chrome，设为空字符串禁用）"
    )

    args = parser.parse_args()

    # 处理 cookies 参数
    cookies_browser = args.cookies_from_browser if args.cookies_from_browser else None

    # 检查依赖
    check_dependencies()

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)

    # Step 1: 获取视频信息
    video_info = get_video_info(args.url, cookies_browser)
    safe_title = sanitize_filename(video_info["title"])
    print(f"   标题: {video_info['title']}")
    print(f"   频道: {video_info['channel']}")
    print(f"   时长: {format_timestamp(video_info.get('duration', 0))}")
    print()

    # Step 2: 下载视频
    if args.skip_download:
        # 查找已有的视频文件
        video_file = None
        for f in os.listdir(args.output_dir):
            if f.endswith(('.mp4', '.mkv', '.webm')) and safe_title[:20] in f:
                video_file = os.path.join(args.output_dir, f)
                break
        if not video_file:
            print("❌ 未找到已下载的视频文件")
            sys.exit(1)
        print(f"⏭️  使用已下载的视频: {os.path.basename(video_file)}")
    else:
        video_file = download_video(args.url, args.output_dir, video_info["title"], cookies_browser)

    print()

    # Step 3: 提取音频
    audio_file = extract_audio(video_file)
    print()

    # Step 4: 转录
    result = transcribe_audio(audio_file, args.whisper_model)
    detected_language = result.get("language", "unknown")
    segments = result.get("segments", [])
    print()

    # Step 5: 合并为段落
    paragraphs = merge_segments_to_paragraphs(segments)
    print(f"📝 合并为 {len(paragraphs)} 个段落")
    print()

    # Step 6: 翻译（如果不是中文）
    translations = None
    if not args.skip_translate and detected_language not in ("zh", "Chinese"):
        translations = translate_paragraphs(paragraphs, detected_language)
    print()

    # Step 7: 生成 Markdown
    md_content = generate_markdown(
        video_info, paragraphs, translations, detected_language
    )
    md_path = os.path.join(args.output_dir, f"{safe_title}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"📄 文字稿已保存: {md_path}")

    # Step 8: 保存元信息
    meta_path = os.path.join(args.output_dir, f"{safe_title}_meta.json")
    save_meta_json(
        video_info, meta_path, detected_language,
        len(paragraphs), video_file
    )
    print(f"📋 元信息已保存: {meta_path}")

    # 清理音频文件
    if not args.keep_audio and os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"🗑️  已清理音频文件: {os.path.basename(audio_file)}")

    print()
    print("=" * 60)
    print(f"✅ 处理完成！")
    print(f"   视频文件: {video_file}")
    print(f"   文字稿:   {md_path}")
    print(f"   元信息:   {meta_path}")
    print(f"   段落数:   {len(paragraphs)}")
    print(f"   语言:     {detected_language}")
    if translations and any(t is not None for t in translations):
        print(f"   翻译:     ✅ 已翻译为中文（中英对照）")
    print("=" * 60)

    # 返回关键路径供后续脚本使用
    return {
        "video_file": video_file,
        "md_path": md_path,
        "meta_path": meta_path,
        "title": video_info["title"],
        "safe_title": safe_title,
    }


if __name__ == "__main__":
    main()
