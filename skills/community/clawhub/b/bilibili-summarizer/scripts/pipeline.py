#!/usr/bin/env python3
"""
pipeline.py - 视频字幕提取一键流程（B站 + 抖音 + YouTube + 小红书 + 本地文件）

用法:
    # 单个视频
    python3 pipeline.py "https://www.bilibili.com/video/BVxxxx"
    python3 pipeline.py "https://v.douyin.com/xxx"
    python3 pipeline.py "https://youtube.com/watch?v=xxx"
    python3 pipeline.py "https://www.xiaohongshu.com/explore/xxx"
    python3 pipeline.py "/path/to/local_video.mp4"

    # 批量处理（空格分隔多个链接）
    python3 pipeline.py "链接1" "链接2" "链接3"

    # B站收藏夹/合集
    python3 pipeline.py --collection "https://space.bilibili.com/xxx/favlist?fid=xxx"

    # 输出选项
    python3 pipeline.py "链接" --output-dir ~/Desktop
    python3 pipeline.py "链接" --format srt          # 导出 SRT 字幕
    python3 pipeline.py "链接" --frames               # 提取关键帧截图
    python3 pipeline.py "链接" --danmaku              # 分析弹幕（仅B站）
    python3 pipeline.py "链接" --diarize              # 说话人分离（仅ASR）
    python3 pipeline.py "链接" --all                  # 全部功能

输出:
    JSON 格式到 stdout，包含完整的处理结果
    字幕文件保存到 cache/output/ 目录
"""

import sys
import os
import json
import re
import shutil
import subprocess
from pathlib import Path

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPTS_DIR, "..", "cache")
OUTPUT_DIR = os.path.join(CACHE_DIR, "output")
FRAMES_DIR = os.path.join(CACHE_DIR, "frames")


# ---------- 工具函数 ----------

def detect_input_type(text):
    """判断输入类型: bilibili / douyin / youtube / xiaohongshu / local_file / unknown"""
    t = text.lower().strip()
    if os.path.isfile(t) or os.path.isfile(os.path.expanduser(t)):
        return "local_file"
    if "bilibili.com" in t or re.search(r"(BV[0-9A-Za-z]{10})", t, re.IGNORECASE):
        return "bilibili"
    if "douyin.com" in t or "tiktok.com" in t:
        return "douyin"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"
    if "xiaohongshu.com" in t or "xhslink.com" in t or "xhs.cn" in t:
        return "xiaohongshu"
    return "unknown"


def run_script(script_name, args, timeout=600):
    """运行 scripts 目录下的脚本，返回 parsed JSON"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        return {"error": f"脚本不存在: {script_name}"}
    cmd = [sys.executable, script_path] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            return {"error": stderr or f"脚本 {script_name} 返回非零状态码"}
        stdout = result.stdout.strip()
        if not stdout:
            return {"error": f"脚本 {script_name} 无输出"}
        # 尝试解析 JSON
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            # 可能是纯文本输出（如 export），直接返回
            return {"raw_output": stdout}
    except subprocess.TimeoutExpired:
        return {"error": f"脚本 {script_name} 执行超时（{timeout}s）"}
    except Exception as e:
        return {"error": str(e)}


def extract_audio_from_local(video_path, output_dir):
    """从本地视频文件提取音频"""
    os.makedirs(output_dir, exist_ok=True)
    basename = Path(video_path).stem
    audio_path = os.path.join(output_dir, f"local_{basename}.m4a")

    if os.path.exists(audio_path):
        print(f"[*] 音频已存在: {audio_path}", file=sys.stderr)
        return {"audio_path": audio_path, "video_id": f"local_{basename}"}

    print(f"[*] 从本地视频提取音频...", file=sys.stderr)
    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if not ffmpeg or not os.path.exists(ffmpeg):
        return {"error": "ffmpeg 未安装。请运行: brew install ffmpeg"}

    cmd = [ffmpeg, "-i", video_path, "-vn", "-acodec", "copy", "-y", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        # 尝试重新编码
        cmd = [ffmpeg, "-i", video_path, "-vn", "-acodec", "aac", "-b:a", "128k", "-y", audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"error": f"提取音频失败: {result.stderr[-300:]}"}

    info = {"audio_path": audio_path, "video_id": f"local_{basename}"}
    if os.path.exists(audio_path):
        info["file_size_mb"] = round(os.path.getsize(audio_path) / (1024 * 1024), 2)
    return info


def fetch_youtube_info(url):
    """获取 YouTube 视频信息（通过 yt-dlp）"""
    ytdlp = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
    if not ytdlp:
        return {"error": "yt-dlp 未安装"}

    cmd = [ytdlp, "--no-playlist", "--dump-json", "--skip-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return {"error": f"获取YouTube信息失败: {result.stderr[-300:]}"}

    try:
        data = json.loads(result.stdout)
        return {
            "platform": "youtube",
            "video_id": data.get("id", ""),
            "title": data.get("title", ""),
            "desc": data.get("description", "")[:500],
            "owner": data.get("uploader", ""),
            "duration_sec": data.get("duration", 0),
            "view": data.get("view_count", 0),
            "like": data.get("like_count", 0),
            "tags": data.get("tags", [])[:20],
            "pic": data.get("thumbnail", ""),
            "extra": {"url": url},
        }
    except json.JSONDecodeError:
        return {"error": "解析YouTube信息失败"}


def fetch_collection_videos(url):
    """获取B站收藏夹/合集中的所有视频链接"""
    print(f"[*] 获取收藏夹/合集视频列表...", file=sys.stderr)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
    }

    # 判断是收藏夹还是合集
    import urllib.request
    import urllib.parse

    if "favlist" in url:
        # 收藏夹
        fid_match = re.search(r'fid=(\d+)', url)
        if not fid_match:
            return []
        fid = fid_match.group(1)
        videos = []
        page = 1
        while True:
            api_url = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={fid}&pn={page}&ps=20"
            try:
                req = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if data.get("code") != 0:
                    break
                medias = data.get("data", {}).get("medias", [])
                if not medias:
                    break
                for m in medias:
                    bvid = m.get("bvid", "")
                    if bvid:
                        videos.append(f"https://www.bilibili.com/video/{bvid}")
                if not data.get("data", {}).get("has_more", False):
                    break
                page += 1
            except Exception as e:
                print(f"[!] 获取收藏夹第{page}页失败: {e}", file=sys.stderr)
                break
        return videos
    elif "series" in url or "season" in url:
        # 合集/视频系列
        # 从URL提取 mid 和 series_id
        mid_match = re.search(r'space\.bilibili\.com/(\d+)', url)
        series_match = re.search(r'series=(\d+)', url)
        if not mid_match or not series_match:
            return []
        mid = mid_match.group(1)
        sid = series_match.group(1)
        videos = []
        page = 1
        while True:
            api_url = f"https://api.bilibili.com/x/series/archives?mid={mid}&series_id={sid}&pn={page}&ps=30"
            try:
                req = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if data.get("code") != 0:
                    break
                archives = data.get("data", {}).get("archives", [])
                if not archives:
                    break
                for a in archives:
                    bvid = a.get("bvid", "")
                    if bvid:
                        videos.append(f"https://www.bilibili.com/video/{bvid}")
                if not data.get("data", {}).get("page", {}).get("has_more", False):
                    break
                page += 1
            except Exception as e:
                print(f"[!] 获取合集第{page}页失败: {e}", file=sys.stderr)
                break
        return videos
    return []


def save_output(video_id, result_data, output_dir, format_type="txt"):
    """保存输出文件"""
    os.makedirs(output_dir, exist_ok=True)

    info = result_data.get("info", {})
    subtitle = result_data.get("subtitle", {})

    # 保存带时间戳字幕
    timed = subtitle.get("timed_text", "")
    if timed:
        if format_type == "srt":
            srt_content = _timed_to_srt(subtitle.get("segments", []))
            ext = "srt"
            content = srt_content
        else:
            ext = "txt"
            content = timed
        filepath = os.path.join(output_dir, f"{video_id}_subtitle.{ext}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # 保存完整 JSON
    json_path = os.path.join(output_dir, f"{video_id}_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    return json_path


def _timed_to_srt(segments):
    """将 segments 转为 SRT 格式"""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = _seconds_to_srt_time(seg.get("from", 0))
        end = _seconds_to_srt_time(seg.get("to", seg.get("from", 0) + 1))
        text = seg.get("content", "").strip()
        if text:
            lines.append(f"{i}")
            lines.append(f"{start} --> {end}")
            lines.append(text)
            lines.append("")
    return "\n".join(lines)


def _seconds_to_srt_time(seconds):
    """将秒数转为 SRT 时间格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ---------- 单视频处理 ----------

def process_single(input_text, options):
    """处理单个视频输入，返回完整结果"""
    input_type = detect_input_type(input_text)
    print(f"[*] 输入类型: {input_type}", file=sys.stderr)

    result = {
        "input": input_text,
        "input_type": input_type,
        "info": {},
        "subtitle": {},
        "extras": {},
    }

    # === 第一步：获取视频信息 ===
    if input_type == "local_file":
        expanded = os.path.expanduser(input_text)
        video_id = f"local_{Path(expanded).stem}"
        result["info"] = {
            "platform": "local",
            "video_id": video_id,
            "title": Path(expanded).name,
            "duration_sec": 0,
        }
        # 获取本地视频时长
        ffprobe = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
        if ffprobe and os.path.exists(ffprobe):
            try:
                cmd = [ffprobe, "-v", "quiet", "-show_entries", "format=duration",
                       "-of", "csv=p=0", expanded]
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                result["info"]["duration_sec"] = round(float(out.stdout.strip()))
            except Exception:
                pass

    elif input_type == "youtube":
        print("[*] 获取 YouTube 视频信息...", file=sys.stderr)
        yt_info = fetch_youtube_info(input_text)
        if "error" in yt_info:
            result["error"] = yt_info["error"]
            return result
        result["info"] = yt_info
        video_id = yt_info.get("video_id", "")

    elif input_type in ("bilibili", "douyin", "xiaohongshu"):
        print("[*] 获取视频信息...", file=sys.stderr)
        fetch_result = run_script("video_fetcher.py", [input_text])
        if "error" in fetch_result:
            result["error"] = fetch_result["error"]
            return result

        info = fetch_result.get("info", {})
        subtitle_data = fetch_result.get("subtitle", {})
        result["info"] = info
        video_id = info.get("video_id", "")

        # B站有API字幕则直接用
        if subtitle_data.get("status") == "已提取" and subtitle_data.get("plain_text"):
            print("[*] 使用 API 字幕", file=sys.stderr)
            result["subtitle"] = subtitle_data
            # 保存输出
            output_dir = options.get("output_dir", OUTPUT_DIR)
            save_output(video_id, result, output_dir, options.get("format", "txt"))
            return result

    else:
        result["error"] = f"无法识别输入类型: {input_text}"
        return result

    # === 第二步：下载/提取音频 ===
    print("[*] 提取音频...", file=sys.stderr)
    audio_dir = os.path.join(CACHE_DIR, "audio")

    if input_type == "local_file":
        audio_result = extract_audio_from_local(os.path.expanduser(input_text), audio_dir)
    else:
        audio_result = run_script("video_audio.py", [input_text, audio_dir])

    if "error" in audio_result:
        result["error"] = audio_result["error"]
        return result

    audio_path = audio_result.get("audio_path", "")
    if not audio_path or not os.path.exists(audio_path):
        result["error"] = "音频文件获取失败"
        return result

    # === 第三步：ASR 语音识别 ===
    print("[*] 语音识别中...", file=sys.stderr)
    asr_args = [audio_path, "--engine", "auto"]
    if options.get("diarize"):
        asr_args.append("--diarize")

    asr_result = run_script("speech_to_text.py", asr_args, timeout=1200)

    if "error" in asr_result:
        result["error"] = f"ASR 失败: {asr_result['error']}"
        return result

    subtitle_data = asr_result.get("subtitle", {})
    subtitle_data["source"] = f"asr_{asr_result.get('engine', 'unknown')}"
    subtitle_data["status"] = "已提取"
    result["subtitle"] = subtitle_data
    result["engine"] = asr_result.get("engine", "")

    # === 第四步：可选功能 ===
    # 弹幕分析（仅B站）
    if options.get("danmaku") and input_type == "bilibili":
        print("[*] 分析弹幕...", file=sys.stderr)
        danmaku_result = run_script("danmaku_analyzer.py", [input_text])
        if "error" not in danmaku_result:
            result["extras"]["danmaku"] = danmaku_result

    # 关键帧截图
    if options.get("frames"):
        print("[*] 提取关键帧...", file=sys.stderr)
        if input_type == "local_file":
            frame_args = [os.path.expanduser(input_text)]
        else:
            frame_args = [input_text]
        frames_dir = os.path.join(FRAMES_DIR, video_id)
        frame_args.extend(["--output-dir", frames_dir])
        frame_result = run_script("frame_extractor.py", frame_args)
        if "error" not in frame_result:
            result["extras"]["frames"] = frame_result

    # === 第五步：保存输出 ===
    output_dir = options.get("output_dir", OUTPUT_DIR)
    json_path = save_output(video_id, result, output_dir, options.get("format", "txt"))
    result["output_file"] = json_path

    # 如果有字幕 segments，也保存 SRT
    segments = subtitle_data.get("segments", [])
    if segments and options.get("format") == "srt":
        srt_path = json_path.replace("_result.json", "_subtitle.srt")
        srt_content = _timed_to_srt(segments)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        result["srt_file"] = srt_path

    return result


# ---------- 主入口 ----------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="视频字幕提取一键流程")
    parser.add_argument("inputs", nargs="*", help="视频链接或本地文件路径（支持多个）")
    parser.add_argument("--collection", help="B站收藏夹/合集URL，自动提取所有视频")
    parser.add_argument("--output-dir", help="输出目录（默认: cache/output/）")
    parser.add_argument("--format", choices=["txt", "srt"], default="txt", help="字幕格式（默认: txt）")
    parser.add_argument("--frames", action="store_true", help="提取关键帧截图")
    parser.add_argument("--danmaku", action="store_true", help="分析弹幕（仅B站）")
    parser.add_argument("--diarize", action="store_true", help="说话人分离（ASR）")
    parser.add_argument("--all", action="store_true", help="启用所有可选功能")

    args = parser.parse_args()

    if args.all:
        args.frames = True
        args.danmaku = True
        args.diarize = True

    options = {
        "output_dir": args.output_dir or OUTPUT_DIR,
        "format": args.format,
        "frames": args.frames,
        "danmaku": args.danmaku,
        "diarize": args.diarize,
    }

    # 收集所有要处理的链接
    urls = list(args.inputs)

    if args.collection:
        print(f"[*] 处理收藏夹/合集: {args.collection}", file=sys.stderr)
        collection_urls = fetch_collection_videos(args.collection)
        if not collection_urls:
            print(json.dumps({"error": "无法获取收藏夹/合集视频列表"}))
            sys.exit(1)
        urls.extend(collection_urls)
        print(f"[*] 共 {len(collection_urls)} 个视频", file=sys.stderr)

    if not urls:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    print(f"[*] 共 {len(urls)} 个视频待处理", file=sys.stderr)

    # 批量处理
    results = []
    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"[*] [{i}/{len(urls)}] 处理: {url[:80]}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        result = process_single(url, options)
        results.append(result)

        if "error" in result:
            fail_count += 1
            print(f"[!] 处理失败: {result['error']}", file=sys.stderr)
        else:
            success_count += 1
            print(f"[✓] 处理成功: {result.get('info', {}).get('title', '')[:50]}", file=sys.stderr)

    # 输出汇总
    summary = {
        "total": len(urls),
        "success": success_count,
        "failed": fail_count,
        "results": results,
    }

    print(f"\n[*] 处理完成: {success_count} 成功, {fail_count} 失败", file=sys.stderr)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
