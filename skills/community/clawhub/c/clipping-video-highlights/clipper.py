#!/usr/bin/env python3
"""
clipping-video-highlights — 自主方案重制版

长视频（YouTube/本地）→ N个短高光片段 + 字幕 + AI封面
全流程免费方案（无Clawvard付费调用）

步骤：
1. yt-dlp 下载视频/提取字幕 → 免费
2. ffmpeg 提取音频 → 免费
3. MiniMax LLM 提取高光时间点 → 已有配额
4. MiniMax 图片生成封面 → 已有配额
5. ffmpeg 剪辑 + 烧字幕 → 免费
6. 腾讯COS存储 → 已有方案
"""

import os, sys, json, subprocess, tempfile, shutil
from pathlib import Path
from datetime import datetime

# ── 依赖检查 ──────────────────────────────────────
def check_deps():
    for cmd in ["ffmpeg", "ffprobe", "yt-dlp"]:
        if subprocess.run(["which", cmd], capture_output=True).returncode != 0:
            raise RuntimeError(f"缺少命令: {cmd}")
    return True

# ── Step 1: 下载视频 + 提取字幕（YouTube）──────────────────────
def fetch_youtube(video_url: str, output_dir: str) -> dict:
    """下载YouTube视频，自动提取字幕（免费）"""
    os.chdir(output_dir)
    
    # 提取字幕（优先en，中文源则zh-Hans）
    cmd = [
        "yt-dlp", "--write-auto-subs",
        "--write-subs", "--skip-download",
        "--sub-lang", "en,zh-Hans,zh-Hant",
        "--convert-subs", "srt",
        "-o", "%(title)s.%(ext)s",
        video_url
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"yt-dlp失败: {r.stderr[:200]}")
    
    # 找字幕文件
    subs = list(Path(output_dir).glob("*.srt"))
    if not subs:
        raise RuntimeError("未找到字幕文件")
    
    return {
        "video_file": None,  # 没下载视频，只用了字幕
        "subtitle_file": str(subs[0]),
        "title": Path(output_dir).glob("*.srt")[0].stem.replace(".en", "").replace(".zh-Hans", "").replace(".zh-Hant", ""),
        "subs_available": True
    }

# ── Step 2: 用MiniMax LLM从字幕选高光 ──────────────────────────
import subprocess, json

def _mmx_chat(prompt: str, max_tokens: int = 2000) -> str:
    """用mmx CLI调用MiniMax文本API（兼容所有模型）
    
    重要：max_tokens必须足够大（≥2000），否则thinking过程占用所有token导致content为空
    """
    r = subprocess.run(
        ["mmx", "text", "chat", "--message", prompt,
         "--model", "MiniMax-M2.7", "--max-tokens", str(max_tokens),
         "--output", "json"],
        capture_output=True, text=True, timeout=120
    )
    try:
        d = json.loads(r.stdout)
        # mmx返回 content:[{text:...}] 或 [{thinking:..., text:...}] 格式
        blocks = d.get("content", [])
        if isinstance(blocks, list):
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "text":
                    txt = b.get("text", "").strip()
                    if txt:
                        return txt
            # Fallback: collect all text from thinking-type blocks too
            texts = [b.get("text", "").strip() for b in blocks if isinstance(b, dict)]
            return "\n".join(texts)
        return str(blocks)
    except:
        return r.stdout[:500]

def pick_highlights(subtitle_file: str, n_clips: int = 5) -> list:
    """让MiniMax LLM从字幕文本选高光时间点"""
    with open(subtitle_file, "r", encoding="utf-8") as f:
        sub_text = f.read()[:8000]  # 限制字数


    prompt = f"""你是一个短视频高光提取专家。从以下字幕文本中精确选出{n_clips}个最有价值的高光片段。

要求（必须严格遵守）：
1. 只输出片段列表，每行一个片段，不要任何解释、编号说明或思考过程
2. 格式：起始时间-结束时间 | 片段核心内容（10字内）
3. 时间格式：MM:SS（如 01:23）
4. 优先选：观点金句、关键结论、情感高潮、知识点密集段落

字幕（按时间顺序）：
{sub_text}

输出示例（严格按此格式）：
00:15-00:45 | 核心观点
05:30-06:10 | 关键结论
08:20-09:05 | 精彩分析"""

    content = _mmx_chat(prompt, max_tokens=512)

    # 解析时间点
    clips = []
    for line in content.split("\n"):
        if not line.strip() or not line[0].isdigit():
            continue
        try:
            # 解析 "1. 00:15-01:02 | 内容"
            time_part = line.split("|")[0].split(".")[-1].strip()
            if "-" in time_part:
                start, end = time_part.split("-")
                clips.append({"start": start.strip(), "end": end.strip()})
        except:
            continue

    return clips[:n_clips]

# ── Step 3: 生成AI封面 ───────────────────────────────────────
def generate_cover(title: str, topic: str = "视频剪辑") -> str:
    """用MiniMax图片生成封面"""
    prompt = f"{topic}短视频封面，高清，16:9，文字：「{title[:10]}」，专业感，抖音风格"
    
    r = subprocess.run(
        ["mmx", "image", "generate",
         "--prompt", prompt,
         "--aspect-ratio", "16:9",
         "--n", "1",
         "--out-dir", "/tmp",
         "--out-prefix", f"cover_{datetime.now().strftime('%H%M%S')}",
         "--quiet"],
        capture_output=True, text=True, timeout=30
    )
    import glob
    files = glob.glob(f"/tmp/cover_*.png") + glob.glob(f"/tmp/cover_*.jpg")
    if files:
        latest = sorted(files, key=lambda x: os.path.getmtime(x))[-1]
        out = f"/tmp/cover_{datetime.now().strftime('%H%M%S')}.jpg"
        shutil.copy(latest, out)
        return out
    return None

# ── Step 4: 剪辑片段 + 烧字幕 ────────────────────────────────
def cut_clip(video_url: str, clip_info: dict, subtitle_file: str, 
             output_path: str, video_downloaded: str = None) -> str:
    """用ffmpeg裁剪片段并烧入字幕"""
    start = clip_info["start"]
    end = clip_info["end"]
    
    # 将字幕SRT转换为ASS格式（支持样式）
    ass_file = output_path.replace(".mp4", ".ass")
    cmd = ["ffmpeg", "-y", "-i", subtitle_file, ass_file]
    subprocess.run(cmd, capture_output=True)
    
    # 如果视频存在，直接裁剪；否则需要先下载
    if video_downloaded and Path(video_downloaded).exists():
        input_video = video_downloaded
    else:
        # 临时下载视频片段（只下裁剪部分，节省时间）
        temp_dir = tempfile.mkdtemp()
        dl_cmd = [
            "yt-dlp", "-f", "best[height<=720]",
            "--download-sections", f"*{start}-{end}",
            "-o", f"{temp_dir}/clip.mp4",
            video_url
        ]
        r = subprocess.run(dl_cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"下载片段失败: {r.stderr[:100]}")
        input_video = f"{temp_dir}/clip.mp4"
    
    # ffmpeg裁剪 + 烧字幕
    cut_cmd = [
        "ffmpeg", "-y",
        "-ss", start, "-to", end,
        "-i", input_video,
        "-vf", f"ass={ass_file}",
        "-c:a", "copy",
        "-threads", "2",
        output_path
    ]
    r = subprocess.run(cut_cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # 字幕烧录失败，但视频已裁剪，输出无字幕版本
        cut_cmd_no_sub = [
            "ffmpeg", "-y",
            "-ss", start, "-to", end,
            "-i", input_video,
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(cut_cmd_no_sub, capture_output=True)
    
    return output_path

# ── 主流程 ────────────────────────────────────────────────
def main():
    if len(sys.argv) < 3:
        print("用法: python3 clipper.py <YouTube_URL> <输出目录> [片段数量]")
        sys.exit(1)
    
    video_url = sys.argv[1]
    output_dir = sys.argv[2]
    n_clips = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    os.makedirs(output_dir, exist_ok=True)
    check_deps()
    
    print(f"[1/4] 提取字幕...")
    info = fetch_youtube(video_url, output_dir)
    title = info["title"]
    
    print(f"[2/4] AI选{n_clips}个高光片段...")
    clips = pick_highlights(info["subtitle_file"], n_clips)
    if not clips:
        print("警告：无高光片段，改用字幕均分采样")
        clips = [
            {"start": "00:00", "end": "01:00"},
            {"start": "01:00", "end": "02:00"},
            {"start": "02:00", "end": "03:00"},
        ][:n_clips]
    print(f"   高光: {clips}")
    
    print(f"[3/4] 生成封面...")
    cover = generate_cover(title)
    if cover:
        shutil.copy(cover, f"{output_dir}/cover.jpg")
        print(f"   封面: {output_dir}/cover.jpg")
    
    print(f"[4/4] 剪辑{n_clips}个片段...")
    for i, clip in enumerate(clips):
        out = f"{output_dir}/clip_{i+1:02d}.mp4"
        cut_clip(video_url, clip, info["subtitle_file"], out)
        print(f"   [{i+1}/{len(clips)}] {out}")
    
    print(f"\n✅ 完成！输出目录: {output_dir}")
    return output_dir

if __name__ == "__main__":
    main()
