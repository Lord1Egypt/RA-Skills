#!/usr/bin/env python3
"""播客音频全流程处理脚本：抓取 Show Notes → 下载 → ASR转录 → 生成Markdown → 上传乐享知识库。

核心设计原则：
- 所有操作固化在脚本中，Agent 只需准备 JSON 配置文件 + 一行命令调用
- 长音频预切片 → 逐片段转录 → 按标点切分 → 章节对齐
- 热词通过 generate(hotword="词1 词2") 传入，提升专有名词准确率
- 大文档通过预签名 URL 上传，不经过 MCP 参数传递

用法：
  # 完整流程（下载 + 转录 + 生成 Markdown）
  python3 podcast_to_lexiang.py "<播客链接>" \\
      --output-dir ./output \\
      --language zh \\
      --metadata-json metadata.json \\
      --chapters-json chapters.json \\
      --hotwords-json hotwords.json \\
      --no-upload

  # 含上传（需要 LEXIANG_TOKEN）
  python3 podcast_to_lexiang.py "<播客链接>" \\
      --output-dir ./output \\
      --space-id <SPACE_ID> --parent-entry-id <日期目录ID>

依赖安装（首次使用）：
  pip install funasr torch torchaudio modelscope yt-dlp opencc-python-reimplemented

环境变量（上传到乐享时需要）：
  LEXIANG_TOKEN  - 乐享 MCP Token（约2小时有效）
  COMPANY_FROM   - 乐享企业ID
  MCP_BASE_URL   - MCP 服务地址（默认 https://mcp.lexiang-app.com）

已知经验和踩坑记录：
  1. FunASR 热词必须通过 generate(hotword="词1 词2") 传入，不能放 AutoModel 构造函数
  2. 长音频（>10分钟）必须预切片再逐片段转录，否则 FunASR 会合并为一整段
  3. 切片大小建议 600s（10分钟），ffmpeg -f segment -segment_time 600
  4. FunASR 返回逐字 timestamp，需按标点符号切分为自然段落
  5. 系统 Python (/usr/bin/python3) 可用，managed Python 的 torch 有 code signing 问题
  6. 脚本执行时间较长（139分钟音频约10分钟），建议 nohup 后台运行
"""
from __future__ import annotations

import argparse
import html as html_module
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


# 节目级 boilerplate，shownotes 中截断点（保留介绍 + 本期剧透，去掉重复 footer）
_SHOWNOTES_CUT_MARKERS = (
    "听友来信", "收听渠道", "新节目指路", "关于我们",
    "展开Show Notes", "打开小宇宙查看更多精彩评论",
)
_SHOWNOTES_SECTION_HEADERS = ("本期剧透", "时间线", "章节", "Shownotes", "Show Notes")


# ============================================================
# 0. 抓取 Show Notes / 元信息
# ============================================================
def _http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_xiaoyuzhou_metadata(url: str) -> dict:
    """从小宇宙 episode 页 __NEXT_DATA__ 提取 shownotes 与元信息。"""
    page = _http_get(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.DOTALL)
    if not m:
        return {}
    data = json.loads(m.group(1))
    ep = data.get("props", {}).get("pageProps", {}).get("episode") or {}
    if not ep:
        return {}

    pod = ep.get("podcast") or {}
    duration_sec = ep.get("duration") or 0
    pub = (ep.get("pubDate") or "")[:10]
    shownotes = (ep.get("description") or "").strip()
    if not shownotes and ep.get("shownotes"):
        shownotes = html_module.unescape(re.sub(r"<[^>]+>", "\n", ep["shownotes"]))
        shownotes = re.sub(r"\n{3,}", "\n\n", shownotes).strip()

    return {
        "title": ep.get("title"),
        "show_name": pod.get("title"),
        "shownotes": shownotes,
        "description": shownotes,
        "date": pub,
        "duration": f"{duration_sec // 60}分钟" if duration_sec else "",
        "platform": "小宇宙FM",
        "url": url,
    }


def fetch_ytdlp_metadata(url: str) -> dict:
    """yt-dlp JSON 作为通用 fallback（description 常为节目级简介，信息量有限）。"""
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    try:
        info = json.loads(result.stdout.strip().split("\n")[0])
    except (json.JSONDecodeError, IndexError):
        return {}

    desc = (info.get("description") or "").strip()
    upload_date = info.get("upload_date") or ""
    if len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    duration = info.get("duration") or 0
    return {
        "title": info.get("title") or info.get("fulltitle"),
        "show_name": info.get("uploader") or info.get("channel"),
        "shownotes": desc,
        "description": desc,
        "date": upload_date,
        "duration": f"{duration // 60}分钟" if duration else "",
        "platform": info.get("extractor_key", ""),
        "url": info.get("webpage_url") or url,
    }


def fetch_episode_metadata(url: str) -> dict:
    """按平台抓取 episode 元信息与 shownotes。"""
    if "xiaoyuzhoufm.com" in url:
        meta = fetch_xiaoyuzhou_metadata(url)
        if meta.get("shownotes"):
            return meta
    return fetch_ytdlp_metadata(url)


def merge_metadata(base: dict, fetched: dict) -> dict:
    """页面抓取结果填空白；metadata.json / Agent 手工字段优先。"""
    merged = dict(fetched)
    merged.update({k: v for k, v in base.items() if v not in (None, "", [], {})})
    if not merged.get("shownotes") and base.get("description"):
        merged["shownotes"] = base["description"]
    elif not merged.get("shownotes") and fetched.get("description"):
        merged["shownotes"] = fetched["description"]
    return merged


def trim_shownotes_boilerplate(text: str) -> str:
    """去掉节目级 footer（听友来信、关于我们等），保留介绍与本期剧透。"""
    if not text:
        return ""
    cut_at = len(text)
    for marker in _SHOWNOTES_CUT_MARKERS:
        idx = text.find(marker)
        if 0 < idx < cut_at:
            cut_at = idx
    return text[:cut_at].strip()


def parse_time_to_seconds(time_str: str) -> int:
    parts = time_str.strip().split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0


def extract_chapters_from_shownotes(text: str) -> list[tuple[int, str]]:
    """从 shownotes 时间线提取章节，如「1、09:36 标题」。"""
    chapters: list[tuple[int, str]] = []
    for line in text.split("\n"):
        line = line.strip()
        m = re.match(
            r"^\d+[、.]?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$",
            line,
        )
        if m:
            chapters.append((parse_time_to_seconds(m.group(1)), m.group(2).strip()))
    return chapters


def format_shownotes_markdown(shownotes: str) -> str:
    """将 shownotes 格式化为「节目介绍」区块（位于逐字稿之前）。"""
    text = trim_shownotes_boilerplate(shownotes)
    if not text:
        return ""

    lines = ["## 节目介绍", ""]
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        if para in _SHOWNOTES_SECTION_HEADERS:
            lines.extend(["", f"### {para}", ""])
        else:
            lines.extend([para, ""])

    return "\n".join(lines).strip()


# ============================================================
# 1. 下载音频
# ============================================================
def download_audio(url: str, output_dir: Path) -> Path:
    """使用 yt-dlp 下载播客音频。已存在则跳过。"""
    print(f"\n{'='*60}")
    print(f"[1/5] 下载音频: {url}")
    print(f"{'='*60}", flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)

    # 检查已有文件（避免重复下载）
    existing = list(output_dir.glob("*.m4a")) + list(output_dir.glob("*.mp3")) + list(output_dir.glob("*.opus"))
    if existing:
        audio_path = max(existing, key=lambda f: f.stat().st_mtime)
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        print(f"📌 已存在音频文件，跳过下载: {audio_path.name} ({size_mb:.1f} MB)")
        return audio_path

    cmd = ["yt-dlp", "--no-playlist", "-o", str(output_dir / "%(title)s.%(ext)s"), url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 下载失败: {result.stderr[-500:]}")
        sys.exit(1)

    audio_files = list(output_dir.glob("*.m4a")) + list(output_dir.glob("*.mp3")) + list(output_dir.glob("*.opus"))
    if not audio_files:
        print("❌ 未找到下载的音频文件")
        sys.exit(1)

    audio_path = max(audio_files, key=lambda f: f.stat().st_mtime)
    size_mb = audio_path.stat().st_size / (1024 * 1024)
    print(f"✅ 下载完成: {audio_path.name} ({size_mb:.1f} MB)")
    return audio_path


# ============================================================
# 2. 音频预处理（转WAV + 切片）
# ============================================================
def prepare_audio(audio_path: Path, output_dir: Path, chunk_seconds: int = 600) -> tuple[Path, list[Path]]:
    """转换为 WAV 16kHz 单声道，并切成固定时长的片段。"""
    print(f"\n{'='*60}")
    print(f"[2/5] 音频预处理: WAV转换 + 切片({chunk_seconds}s/片)")
    print(f"{'='*60}", flush=True)

    wav_path = output_dir / "audio_16k.wav"
    chunks_dir = output_dir / "chunks"

    # 转 WAV（如已存在则跳过）
    if not wav_path.exists():
        cmd = ["ffmpeg", "-i", str(audio_path), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-y", str(wav_path)]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"✅ WAV 转换完成: {wav_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print(f"📌 WAV 已存在，跳过转换")

    # 切片（如已存在则跳过）
    if not chunks_dir.exists() or not list(chunks_dir.glob("*.wav")):
        chunks_dir.mkdir(exist_ok=True)
        cmd = ["ffmpeg", "-i", str(wav_path), "-f", "segment", "-segment_time", str(chunk_seconds), "-c", "copy", str(chunks_dir / "chunk_%03d.wav")]
        subprocess.run(cmd, capture_output=True, check=True)

    chunk_files = sorted(chunks_dir.glob("chunk_*.wav"))
    print(f"✅ 切片完成: {len(chunk_files)} 个片段 (每片 {chunk_seconds}s)")
    return wav_path, chunk_files


# ============================================================
# 3. ASR 转录（FunASR 分片 + 热词 + 标点切分）
# ============================================================
def transcribe(chunk_files: list[Path], hotwords: str = "", chunk_seconds: int = 600) -> list[dict]:
    """逐片段转录，带热词增强和标点切分。

    关键经验：
    - 热词通过 generate(hotword="词1 词2") 传入（空格分隔）
    - 不能放在 AutoModel(hotword=file) 构造函数中（那是 contextual 模型专用）
    - merge_vad=True + merge_length_s=15 避免段落过碎
    """
    print(f"\n{'='*60}")
    print(f"[3/5] ASR 转录 (FunASR Paraformer + CT-Punc + 热词)")
    print(f"{'='*60}", flush=True)

    from funasr import AutoModel

    model = AutoModel(
        model="paraformer-zh",
        model_revision="v2.0.4",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        punc_model="ct-punc",
        device="cpu",
        disable_update=True,
    )

    if hotwords:
        print(f"📌 热词: {hotwords[:80]}...")

    all_segments = []
    total_offset = 0.0
    start_time = time.time()

    for i, chunk_file in enumerate(chunk_files):
        print(f"[{i+1}/{len(chunk_files)}] {chunk_file.name}...", end=" ", flush=True)
        t0 = time.time()

        gen_kwargs = {
            "input": str(chunk_file),
            "cache": {},
            "language": "auto",
            "use_itn": True,
            "batch_size_s": 300,
            "merge_vad": True,
            "merge_length_s": 15,
        }
        if hotwords:
            gen_kwargs["hotword"] = hotwords

        res = model.generate(**gen_kwargs)

        chunk_segs = []
        for item in res:
            text = item.get("text", "")
            timestamps = item.get("timestamp", [])
            if not text.strip():
                continue
            if timestamps:
                chunk_segs.extend(split_by_punctuation(text, timestamps))
            else:
                chunk_segs.append({"text": text, "start": 0, "end": 0})

        # 加时间偏移
        for seg in chunk_segs:
            seg["start"] += total_offset
            seg["end"] += total_offset

        all_segments.extend(chunk_segs)
        total_offset += chunk_seconds
        print(f"{len(chunk_segs)} 段, {time.time()-t0:.1f}s", flush=True)

    elapsed = time.time() - start_time
    print(f"\n✅ 转录完成: {len(all_segments)} 段, 总用时 {elapsed:.0f}s")
    return all_segments


def split_by_punctuation(text: str, timestamps: list[list[int]]) -> list[dict]:
    """将 FunASR 的整段 text + 逐字 timestamp 按句末标点切分为自然段落。

    切分策略：
    - 遇到句号/问号/感叹号 → 断句
    - 累计超过 200 字 → 在最近的逗号处断句
    - 超过 300 字无论如何断
    - 最终每段 30-200 字，带起止时间戳
    """
    if not text or not timestamps:
        return [{"text": text, "start": 0, "end": 0}]

    sentence_ends = set("。！？!?")
    soft_breaks = set("，,；;：:")

    segments = []
    chars = list(text)

    # 建立字符到时间戳映射
    ts_idx = 0
    char_ts_map = []
    for ch in chars:
        if ts_idx < len(timestamps):
            char_ts_map.append((ch, timestamps[ts_idx][0], timestamps[ts_idx][1]))
            if ch not in sentence_ends and ch not in soft_breaks and ch not in "，,。！？!?；;：:、\"\"''""（）()【】《》":
                ts_idx += 1
        else:
            last_end = timestamps[-1][1] if timestamps else 0
            char_ts_map.append((ch, last_end, last_end))

    cur_text = ""
    cur_start = char_ts_map[0][1] if char_ts_map else 0
    cur_end = 0
    last_soft_break_pos = -1

    for i, (ch, start_ms, end_ms) in enumerate(char_ts_map):
        cur_text += ch
        cur_end = end_ms

        if ch in soft_breaks:
            last_soft_break_pos = len(cur_text)

        should_break = False
        if ch in sentence_ends:
            should_break = True
        elif len(cur_text) > 200 and last_soft_break_pos > 50:
            overflow = cur_text[last_soft_break_pos:]
            cur_text = cur_text[:last_soft_break_pos]
            segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})
            cur_text = overflow
            cur_start = start_ms
            last_soft_break_pos = -1
            continue
        elif len(cur_text) > 300:
            should_break = True

        if should_break and ch in sentence_ends:
            segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})
            cur_text = ""
            cur_start = end_ms
            last_soft_break_pos = -1

    if cur_text.strip():
        segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})

    return segments


# ============================================================
# 4. 生成 Markdown 文字稿
# ============================================================
def generate_markdown(segments: list[dict], title: str, metadata: dict,
                      chapters: list[tuple[int, str]] | None = None, language: str = "zh") -> str:
    """将分段结果生成带 shownotes、章节和时间戳的 Markdown。"""
    print(f"\n{'='*60}")
    print(f"[4/5] 生成 Markdown 文字稿")
    print(f"{'='*60}", flush=True)

    # 繁简转换
    if language in ("zh", "auto"):
        try:
            import opencc
            converter = opencc.OpenCC("t2s")
            for seg in segments:
                seg["text"] = converter.convert(seg["text"])
            print("📌 已完成繁简转换")
        except ImportError:
            pass

    def fmt_time(seconds: float) -> str:
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m:02d}:{s:02d}"

    lines = []
    lines.append(f"# {title}\n")
    if metadata.get("show_name"):
        lines.append(f"> 播客：{metadata['show_name']} | 平台：{metadata.get('platform', '小宇宙FM')}")
    if metadata.get("guest"):
        lines.append(f"> 嘉宾：{metadata['guest']} | 主播：{metadata.get('host', '')}")
    if metadata.get("date"):
        lines.append(f"> 发布日期：{metadata['date']} | 时长：{metadata.get('duration', '')}")
    if metadata.get("url"):
        lines.append(f"> 原始链接：{metadata['url']}")
    lines.append(f"> 转录工具：FunASR (Paraformer + CT-Punc) | 标点自动恢复\n")
    lines.append("---\n")

    shownotes = metadata.get("shownotes") or metadata.get("description") or ""
    shownotes_md = format_shownotes_markdown(shownotes)
    if shownotes_md:
        lines.append(shownotes_md)
        lines.append("\n---\n")
        print(f"📌 已插入节目介绍 ({len(trim_shownotes_boilerplate(shownotes))} 字符)")

    lines.append("## 逐字稿\n")

    # 插入章节标题
    if chapters:
        chapter_idx = 0
        inserted = set()
        for seg in segments:
            while chapter_idx < len(chapters):
                ch_time, ch_title = chapters[chapter_idx]
                if seg["start"] >= ch_time and chapter_idx not in inserted:
                    lines.append(f"\n## {ch_title}\n")
                    inserted.add(chapter_idx)
                    chapter_idx += 1
                else:
                    break
            lines.append(f"**[{fmt_time(seg['start'])}]** {seg['text']}\n")
    else:
        for seg in segments:
            lines.append(f"**[{fmt_time(seg['start'])}]** {seg['text']}\n")

    content = "\n".join(lines)
    print(f"✅ Markdown 生成完成: {len(segments)} 段, {len(content)} 字符")
    return content


# ============================================================
# 5. 上传到乐享（可选）
# ============================================================
def upload_to_lexiang(md_content: str, md_path: Path, audio_path: Path,
                      title: str, space_id: str, parent_entry_id: str):
    """上传文字稿和音频到乐享知识库。"""
    print(f"\n{'='*60}")
    print(f"[5/5] 上传到乐享知识库")
    print(f"{'='*60}", flush=True)

    token = os.environ.get("LEXIANG_TOKEN", "")
    company_from = os.environ.get("COMPANY_FROM", "")
    base_url = os.environ.get("MCP_BASE_URL", "https://mcp.lexiang-app.com")

    if not token or not company_from:
        print("⚠️ 未设置 LEXIANG_TOKEN 或 COMPANY_FROM")
        print(f"📌 文字稿已保存本地: {md_path}")
        print(f"📌 音频文件: {audio_path}")
        print("📌 请通过 Agent MCP connector 执行 3 步预签名上传")
        return {"status": "local_only", "md_path": str(md_path), "audio_path": str(audio_path)}

    import requests

    def call_mcp(tool_name, arguments):
        url = f"{base_url}/mcp?company_from={company_from}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool_name, "arguments": arguments}}
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        if resp.status_code == 401:
            return {"error": "token_expired"}
        for line in resp.text.strip().split("\n"):
            line = line.strip()
            if line.startswith("data:"): line = line[5:].strip()
            if not line or line == "[DONE]": continue
            try:
                data = json.loads(line)
                if "result" in data:
                    for c in data["result"].get("content", []):
                        if c.get("type") == "text":
                            return json.loads(c["text"])
            except (json.JSONDecodeError, KeyError):
                continue
        return {"error": "no_response"}

    # 上传文字稿（直接传 content，HTTP 无大小限制）
    print(f"📤 上传文字稿...")
    result = call_mcp("entry_import_content", {
        "name": title, "content": md_content, "content_type": "markdown",
        "parent_id": parent_entry_id, "space_id": space_id,
    })
    entry_id = result.get("data", {}).get("entry", {}).get("id", "")
    if entry_id:
        print(f"✅ 文字稿: entry_id={entry_id}")

    # 上传音频（VOD 路径）
    print(f"📤 上传音频...")
    script_dir = Path(__file__).parent
    upload_script = script_dir / "upload_video_via_openapi.py"
    if upload_script.exists():
        cmd = [sys.executable, str(upload_script), str(audio_path),
               "--space-id", space_id, "--parent-entry-id", parent_entry_id, "--media-type", "audio"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            print(f"✅ 音频已上传")
        else:
            print(f"⚠️ 音频上传失败，请手动上传")

    return {"status": "uploaded", "entry_id": entry_id}


# ============================================================
# 热词构建
# ============================================================
def build_hotwords(args, metadata: dict, chapters: list | None) -> str:
    """从多个来源构建热词列表（空格分隔的词列表）。"""
    # 来源1: --hotwords 直接指定
    if hasattr(args, 'hotwords') and args.hotwords:
        if os.path.isfile(args.hotwords):
            with open(args.hotwords) as f:
                return " ".join(line.split()[0] for line in f if line.strip())
        return args.hotwords

    # 来源2: --hotwords-json
    if hasattr(args, 'hotwords_json') and args.hotwords_json and Path(args.hotwords_json).exists():
        with open(args.hotwords_json) as f:
            hw_list = json.load(f)
        words = []
        for item in hw_list:
            words.append(item["word"] if isinstance(item, dict) else item)
        return " ".join(words)

    # 来源3: 自动从 metadata + chapters 提取
    words = set()
    if metadata.get("guest"):
        name = re.split(r'[（(]', metadata["guest"])[0].strip()
        words.add(name)
        if 2 <= len(name) <= 4:
            words.add(name[1:])
    if metadata.get("host"):
        name = re.split(r'[（(]', metadata["host"])[0].strip()
        words.add(name)
    if chapters:
        for _, ch_title in chapters:
            for term in re.findall(r'\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\b', ch_title):
                if len(term) > 2:
                    words.add(term)

    return " ".join(words) if words else ""


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="播客全流程：下载→转录→Markdown→上传")
    parser.add_argument("url", help="播客链接")
    parser.add_argument("--output-dir", "-o", default="./podcast_output", help="输出目录")
    parser.add_argument("--language", "-l", default="auto", choices=["zh", "en", "auto"])
    parser.add_argument("--space-id", help="乐享 space_id")
    parser.add_argument("--parent-entry-id", help="乐享目标目录 entry_id")
    parser.add_argument("--no-upload", action="store_true", help="仅转录不上传")
    parser.add_argument("--title", help="自定义标题")
    parser.add_argument("--metadata-json", help="元信息 JSON")
    parser.add_argument("--chapters-json", help="章节时间线 JSON")
    parser.add_argument("--hotwords", help="热词文件或字符串")
    parser.add_argument("--hotwords-json", help="热词 JSON")
    parser.add_argument("--shownotes-json", help="Show Notes JSON（含 shownotes 字段）或纯文本 .md")
    parser.add_argument("--skip-shownotes-fetch", action="store_true", help="跳过自动抓取 shownotes")
    parser.add_argument("--chunk-seconds", type=int, default=600, help="切片时长(秒)")

    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载配置
    metadata = {}
    if args.metadata_json and Path(args.metadata_json).exists():
        with open(args.metadata_json) as f:
            metadata = json.load(f)

    if args.shownotes_json and Path(args.shownotes_json).exists():
        p = Path(args.shownotes_json)
        if p.suffix == ".json":
            with open(p) as f:
                sn = json.load(f)
            metadata["shownotes"] = sn.get("shownotes") or sn.get("description") or ""
        else:
            metadata["shownotes"] = p.read_text(encoding="utf-8")

    # 自动抓取 shownotes（小宇宙等平台信息量远高于 yt-dlp description）
    if not args.skip_shownotes_fetch and not metadata.get("shownotes"):
        print(f"\n{'='*60}")
        print(f"[0/5] 抓取 Show Notes")
        print(f"{'='*60}", flush=True)
        fetched = fetch_episode_metadata(args.url)
        metadata = merge_metadata(metadata, fetched)
        if metadata.get("shownotes"):
            print(f"✅ Show Notes: {len(metadata['shownotes'])} 字符")
        else:
            print("⚠️ 未获取到 Show Notes，将仅输出逐字稿")

    chapters = None
    if args.chapters_json and Path(args.chapters_json).exists():
        with open(args.chapters_json) as f:
            chapters = [(c["time"], c["title"]) for c in json.load(f)]
    elif metadata.get("shownotes"):
        chapters = extract_chapters_from_shownotes(metadata["shownotes"])
        if chapters:
            print(f"📌 从 Show Notes 提取 {len(chapters)} 个章节时间点")

    title = args.title or metadata.get("title", "播客转录")
    hotwords = build_hotwords(args, metadata, chapters)

    # Step 1: 下载
    audio_path = download_audio(args.url, output_dir)

    # Step 2: WAV + 切片
    wav_path, chunk_files = prepare_audio(audio_path, output_dir, args.chunk_seconds)

    # Step 3: 转录
    segments = transcribe(chunk_files, hotwords, args.chunk_seconds)

    # 保存 segments
    segments_path = output_dir / "segments.json"
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # Step 4: 生成 Markdown
    md_content = generate_markdown(segments, title, metadata, chapters, args.language)
    md_path = output_dir / f"{title[:80]}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Step 5: 上传（可选）
    if not args.no_upload and args.space_id and args.parent_entry_id:
        upload_to_lexiang(md_content, md_path, audio_path, title, args.space_id, args.parent_entry_id)
    else:
        print(f"\n{'='*60}")
        print(f"🎉 转录完成!")
        print(f"{'='*60}")
        print(f"  音频: {audio_path}")
        print(f"  文字稿: {md_path}")
        print(f"  segments: {segments_path}")

    # 输出 result.json
    result = {"status": "success", "segments_count": len(segments), "content_length": len(md_content),
              "md_path": str(md_path), "audio_path": str(audio_path), "title": title}
    with open(output_dir / "result.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
