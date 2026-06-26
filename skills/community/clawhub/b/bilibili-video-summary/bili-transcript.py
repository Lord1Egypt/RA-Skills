#!/usr/bin/env python3
"""
Bilibili Video Text Extraction Tool
Supports: subtitle extraction, GPU-accelerated transcription (whisper.cpp + Vulkan),
danmaku download, and comment scraping.

Dependencies: pip install yt-dlp av
Optional: whisper.cpp with Vulkan support for audio transcription
"""

import subprocess
import json
import sys
import argparse
import shutil
import os
from pathlib import Path
import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET
from collections import Counter
import math

# ── Path Configuration ────────────────────────────────

# Script directory (for locating whisper-cpp relative to the repo)
SCRIPT_DIR = Path(__file__).parent.resolve()

# yt-dlp
YT_DLP = shutil.which("yt-dlp")
if not YT_DLP:
    try:
        import yt_dlp
        YT_DLP = [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        YT_DLP = "yt-dlp"

# whisper.cpp paths — configurable via environment variables
WHISPER_CPP_DIR = Path(os.environ.get(
    "WHISPER_CPP_DIR",
    str(SCRIPT_DIR / "whisper-cpp")
))
WHISPER_CLI = WHISPER_CPP_DIR / "whisper-cli.exe"
if sys.platform != "win32":
    # Linux/macOS naming
    WHISPER_CLI = WHISPER_CPP_DIR / "whisper-cli"

WHISPER_MODEL_PATH = Path(os.environ.get(
    "WHISPER_MODEL",
    str(WHISPER_CPP_DIR / "models" / "ggml-large-v3-turbo.bin")
))

# Default output directory (configurable via --output or BILI_OUTPUT_DIR env)
DEFAULT_OUTPUT = Path(os.environ.get(
    "BILI_OUTPUT_DIR",
    str(Path.cwd() / "bili-output")
))

# ── HTTP Utilities ────────────────────────────────────

REQ_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/",
}


def http_get(url: str, timeout: int = 15) -> bytes:
    """GET request with auto gzip decompression"""
    import gzip
    req = urllib.request.Request(url, headers={
        **REQ_HEADERS,
        "Accept-Encoding": "gzip",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            content = gzip.decompress(content)
        return content


def http_get_json(url: str, timeout: int = 15) -> dict:
    """GET request returning parsed JSON"""
    return json.loads(http_get(url, timeout).decode("utf-8"))


def fmt_time(seconds: float) -> str:
    """Convert seconds to mm:ss format"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def save_json(obj: dict, path: Path):
    """Save JSON file with unicode support"""
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Bilibili Video Info ───────────────────────────────

def get_aid_cid(url: str) -> tuple:
    """Extract aid and cid from a Bilibili video URL"""
    try:
        html = http_get(url, timeout=10).decode("utf-8")

        match = re.search(r'window\.__INITIAL_STATE__=(.*?);\(function', html)
        if match:
            data = json.loads(match.group(1))
            video_data = data.get("videoData", {})
            return video_data.get("aid"), video_data.get("cid")

        cmd = [*([YT_DLP] if isinstance(YT_DLP, str) else YT_DLP),
               "--dump-json", "--no-download", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return info.get("aid"), info.get("cid")

        return None, None
    except Exception:
        return None, None


def get_video_info(url: str) -> dict:
    """Get video metadata (title, uploader, duration, description)"""
    cmd = [*([YT_DLP] if isinstance(YT_DLP, str) else YT_DLP),
           "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}

    data = json.loads(result.stdout)
    return {
        "title": data.get("title", ""),
        "bvid": data.get("id", ""),
        "duration": data.get("duration", 0),
        "uploader": data.get("uploader", ""),
        "description": data.get("description", "")[:500],
    }


# ── Bilibili CC Subtitles ─────────────────────────────

def get_subtitle_url(aid: int, cid: int) -> str:
    """Get subtitle URL from Bilibili API"""
    try:
        data = http_get_json(
            f"https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}"
        )
        subtitles = data.get("data", {}).get("subtitle", {}).get("subtitles", [])
        if subtitles:
            subtitle_url = subtitles[0].get("subtitle_url", "")
            if subtitle_url:
                return "https:" + subtitle_url if subtitle_url.startswith("//") else subtitle_url
        return ""
    except Exception:
        return ""


def parse_subtitle(subtitle_url: str) -> str:
    """Parse Bilibili subtitle JSON into plain text"""
    try:
        data = http_get_json(subtitle_url)
        body = data.get("body", [])

        result = []
        for item in body:
            content = item.get("content", "").strip()
            if content:
                result.append(content)

        return "\n".join(result)
    except Exception:
        return ""


# ── Danmaku (Scrolling Comments) ──────────────────────

def fetch_danmaku(url: str, output_dir: Path) -> str:
    """Download danmaku subtitles via yt-dlp, returns xml file path"""
    output_template = str(output_dir / "danmaku")
    cmd = [
        *([YT_DLP] if isinstance(YT_DLP, str) else YT_DLP),
        "--write-subs",
        "--sub-langs", "danmaku",
        "--skip-download",
        "-o", output_template,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    xml_path = output_dir / "danmaku.danmaku.xml"
    if xml_path.exists():
        return str(xml_path)

    for f in output_dir.iterdir():
        if "danmaku" in f.name and f.suffix == ".xml":
            return str(f)

    return ""


def parse_danmaku(xml_path: str) -> dict:
    """Parse danmaku XML into structured data"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    danmaku_list = []
    for d in root.findall(".//d"):
        p_attr = (d.get("p") or "").split(",")
        ts = float(p_attr[0]) if len(p_attr) > 0 and p_attr[0] else 0
        text = (d.text or "").strip()
        if text:
            danmaku_list.append({
                "time": ts,
                "time_str": fmt_time(ts),
                "text": text,
            })

    text_counts = Counter(d["text"] for d in danmaku_list)
    frequent = [{"text": t, "count": c} for t, c in text_counts.most_common(20)]

    return {
        "total_count": len(danmaku_list),
        "unique_count": len(text_counts),
        "frequent": frequent,
        "sample": danmaku_list[:50],
    }


# ── Comments ──────────────────────────────────────────

def fetch_comments(aid: int, max_pages: int = 3, per_page: int = 20) -> dict:
    """Fetch Bilibili video comments (hot sorted)"""
    all_replies = []
    total_count = 0
    has_more = True
    next_offset = 0

    for page in range(max_pages):
        if not has_more:
            break

        url = (
            f"https://api.bilibili.com/x/v2/reply/main"
            f"?oid={aid}&type=1&mode=3&ps={per_page}"
        )
        if next_offset:
            url += f"&offset={next_offset}"

        try:
            data = http_get_json(url, timeout=10)
        except Exception as e:
            break

        d = data.get("data", {})
        if page == 0:
            total_count = d.get("cursor", {}).get("all_count", 0)

        replies = d.get("replies", [])
        if not replies:
            break

        for r in replies:
            reply_item = {
                "user": r.get("member", {}).get("uname", ""),
                "message": r.get("content", {}).get("message", ""),
                "like": r.get("like", 0),
                "ctime": r.get("ctime", 0),
                "rcount": r.get("rcount", 0),
                "sub_replies": [],
            }
            for sr in (r.get("replies") or [])[:3]:
                reply_item["sub_replies"].append({
                    "user": sr.get("member", {}).get("uname", ""),
                    "message": sr.get("content", {}).get("message", ""),
                    "like": sr.get("like", 0),
                })
            all_replies.append(reply_item)

        cursor = d.get("cursor", {})
        has_more = cursor.get("is_end", True) == False
        if has_more:
            next_offset = cursor.get("pagination_str") or cursor.get("next") or 0

        if not next_offset:
            last_rpid = replies[-1].get("rpid", 0)
            if last_rpid:
                next_offset = last_rpid
            else:
                break

    # Deduplicate by message content, keep highest-liked
    seen = set()
    deduped = []
    for r in sorted(all_replies, key=lambda x: x["like"], reverse=True):
        msg_key = r["message"][:80]
        if msg_key not in seen:
            seen.add(msg_key)
            deduped.append(r)

    return {
        "total_count": total_count,
        "fetched_count": len(all_replies),
        "top_liked": deduped[:10],
        "recent": all_replies[:20],
    }


# ── Audio Download & Conversion ──────────────────────

def download_audio(url: str, output_dir: str) -> str:
    """Download audio as m4a via yt-dlp"""
    output_path = Path(output_dir) / "audio.m4a"
    cmd = [
        *([YT_DLP] if isinstance(YT_DLP, str) else YT_DLP),
        "-f", "bestaudio[ext=m4a]/bestaudio",
        "-o", str(output_path),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return str(output_path)


def convert_to_wav(m4a_path: str, output_dir: str) -> str:
    """Convert m4a to 16kHz mono wav using PyAV (whisper.cpp doesn't support m4a)"""
    import av

    wav_path = str(Path(output_dir) / "audio.wav")

    input_container = av.open(m4a_path)
    input_stream = input_container.streams.audio[0]

    output_container = av.open(wav_path, "w", format="wav")
    output_stream = output_container.add_stream("pcm_s16le", rate=16000, layout="mono")

    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)

    for frame in input_container.decode(audio=0):
        resampled_frames = resampler.resample(frame)
        for resampled in resampled_frames:
            for packet in output_stream.encode(resampled):
                output_container.mux(packet)

    for packet in output_stream.encode(None):
        output_container.mux(packet)

    output_container.close()
    input_container.close()

    return wav_path


# ── whisper.cpp GPU Transcription ─────────────────----

def transcribe_with_whisper_cpp(wav_path: str, output_dir: str) -> str:
    """Transcribe audio using whisper.cpp with Vulkan GPU acceleration"""

    if not WHISPER_CLI.exists():
        return f"Error: whisper-cli not found at {WHISPER_CLI}"
    if not WHISPER_MODEL_PATH.exists():
        return f"Error: model not found at {WHISPER_MODEL_PATH}"

    cmd = [
        str(WHISPER_CLI),
        "-m", str(WHISPER_MODEL_PATH),
        "-f", str(Path(wav_path).resolve()),
        "-l", "zh",
        "--no-timestamps",
        "-otxt",
    ]

    print(f"🎤 Transcribing with whisper.cpp...", file=sys.stderr)

    result = subprocess.run(cmd, capture_output=True, text=False)

    txt_output = str(Path(wav_path).with_suffix(".wav.txt"))

    if Path(txt_output).exists():
        text = Path(txt_output).read_text(encoding="utf-8").strip()
        Path(txt_output).unlink(missing_ok=True)
        return text

    if result.returncode != 0:
        try:
            err = result.stderr.decode("utf-8", errors="replace")[-500:]
        except:
            err = str(result.stderr)[-500:]
        return f"Transcription failed: {err}"

    return ""


# ── Main Extraction Flow ──────────────────────────────

def extract_text(url: str, output_dir: str) -> dict:
    """
    Extract video text content.
    Strategy: Bilibili CC subtitles → whisper.cpp GPU transcription
    """
    info = get_video_info(url)
    if "error" in info:
        return {"error": info["error"]}

    print(f"📺 Video: {info.get('title', '')}", file=sys.stderr)
    print(f"👤 Uploader: {info.get('uploader', '')}", file=sys.stderr)

    aid, cid = get_aid_cid(url)
    subtitle_text = ""
    source = ""

    if aid and cid:
        subtitle_url = get_subtitle_url(aid, cid)
        if subtitle_url:
            subtitle_text = parse_subtitle(subtitle_url)
            if subtitle_text:
                source = "subtitle"
                print(f"✅ Bilibili CC subtitles found ({len(subtitle_text)} chars)", file=sys.stderr)

    if not subtitle_text:
        print("⚠️ No CC subtitles, starting GPU transcription...", file=sys.stderr)
        print("📥 Downloading audio...", file=sys.stderr)
        audio_path = download_audio(url, str(output_dir))
        if audio_path.startswith("Error"):
            return {"error": audio_path}

        print("🔄 Converting to wav (m4a → 16kHz mono wav)...", file=sys.stderr)
        try:
            wav_path = convert_to_wav(audio_path, str(output_dir))
            print(f"   wav: {wav_path}", file=sys.stderr)
        except Exception as e:
            return {"error": f"Audio conversion failed: {str(e)}"}

        subtitle_text = transcribe_with_whisper_cpp(wav_path, str(output_dir))
        source = "whisper_gpu"

        if subtitle_text.startswith("Transcription failed") or subtitle_text.startswith("Error"):
            return {"error": subtitle_text}

        print(f"✅ Transcription complete ({len(subtitle_text)} chars)", file=sys.stderr)

        try:
            Path(audio_path).unlink(missing_ok=True)
            Path(wav_path).unlink(missing_ok=True)
        except:
            pass

    return {
        "source": source,
        "text": subtitle_text,
        "video_info": info,
        "aid": aid,
        "cid": cid,
    }


# ── CLI ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bilibili video text extraction tool (whisper.cpp GPU)"
    )
    parser.add_argument("url", help="Bilibili video URL")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output directory")
    parser.add_argument(
        "--action",
        choices=["info", "subtitle", "transcribe", "danmaku", "comments", "text"],
        default="text",
        help="Action to perform",
    )
    parser.add_argument(
        "--whisper-dir",
        default=None,
        help="Override whisper.cpp directory",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override whisper model path",
    )

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Allow CLI override of whisper paths
    if args.whisper_dir:
        global WHISPER_CPP_DIR, WHISPER_CLI
        WHISPER_CPP_DIR = Path(args.whisper_dir)
        WHISPER_CLI = WHISPER_CPP_DIR / "whisper-cli.exe"
        if sys.platform != "win32":
            WHISPER_CLI = WHISPER_CPP_DIR / "whisper-cli"
    if args.model:
        global WHISPER_MODEL_PATH
        WHISPER_MODEL_PATH = Path(args.model)

    url = args.url

    # ── info ──
    if args.action == "info":
        info = get_video_info(url)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    # ── subtitle ──
    if args.action == "subtitle":
        aid, cid = get_aid_cid(url)
        if not aid or not cid:
            print("Error: unable to get video info")
            return
        subtitle_url = get_subtitle_url(aid, cid)
        if not subtitle_url:
            print("Error: no subtitles available for this video")
            return
        text = parse_subtitle(subtitle_url)
        if text:
            out_path = output_dir / "subtitle.txt"
            out_path.write_text(text, encoding="utf-8")
            print(f"Subtitles saved: {out_path}")
            print(f"Characters: {len(text)}")
            print("\n--- Subtitle Content ---")
            print(text)
        else:
            print("Error: unable to parse subtitles")
        return

    # ── transcribe ──
    if args.action == "transcribe":
        print("📥 Downloading audio...", file=sys.stderr)
        audio_path = download_audio(url, str(output_dir))
        if audio_path.startswith("Error"):
            print(audio_path)
            return

        print("🔄 Converting audio...", file=sys.stderr)
        wav_path = convert_to_wav(audio_path, str(output_dir))

        text = transcribe_with_whisper_cpp(wav_path, str(output_dir))

        out_path = output_dir / "transcript.txt"
        out_path.write_text(text, encoding="utf-8")

        print(f"Transcript saved: {out_path}", file=sys.stderr)
        print(f"Characters: {len(text)}", file=sys.stderr)
        print(text)

        try:
            Path(audio_path).unlink(missing_ok=True)
            Path(wav_path).unlink(missing_ok=True)
        except:
            pass
        return

    # ── danmaku ──
    if args.action == "danmaku":
        print("📥 Downloading danmaku...", file=sys.stderr)
        xml_path = fetch_danmaku(url, output_dir)
        if not xml_path:
            print("Error: danmaku download failed (may need login)")
            return

        danmaku_data = parse_danmaku(xml_path)

        out_path = output_dir / "danmaku.json"
        save_json(danmaku_data, out_path)

        print(f"Danmaku saved: {out_path}", file=sys.stderr)
        print(f"Total danmaku: {danmaku_data['total_count']}", file=sys.stderr)
        print(f"Unique: {danmaku_data['unique_count']}", file=sys.stderr)
        print(json.dumps({
            "total_count": danmaku_data["total_count"],
            "unique_count": danmaku_data["unique_count"],
            "frequent": danmaku_data["frequent"][:10],
            "danmaku_file": str(out_path),
        }, ensure_ascii=False, indent=2))
        return

    # ── comments ──
    if args.action == "comments":
        aid, cid = get_aid_cid(url)
        if not aid:
            print("Error: unable to get video info")
            return

        print("💬 Fetching comments...", file=sys.stderr)
        comments_data = fetch_comments(aid, max_pages=3)

        out_path = output_dir / "comments.json"
        save_json(comments_data, out_path)

        print(f"Comments saved: {out_path}", file=sys.stderr)
        print(f"Total comments: {comments_data['total_count']}", file=sys.stderr)
        print(f"Fetched: {comments_data['fetched_count']}", file=sys.stderr)

        output = {
            "total_count": comments_data["total_count"],
            "fetched_count": comments_data["fetched_count"],
            "comments_file": str(out_path),
            "top_liked": [
                {"user": c["user"], "message": c["message"][:200], "like": c["like"]}
                for c in comments_data["top_liked"]
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # ── text (default): transcript + danmaku + comments ──
    result = extract_text(url, str(output_dir))

    if "error" in result:
        print(f"❌ Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    info = result["video_info"]
    text = result["text"]
    source = result["source"]
    aid = result.get("aid")
    cid = result.get("cid")

    text_path = output_dir / "transcript.txt"
    text_path.write_text(text, encoding="utf-8")

    # Danmaku
    danmaku_info = {"available": False, "count": 0, "frequent": []}
    print("\n📥 Downloading danmaku...", file=sys.stderr)
    xml_path = fetch_danmaku(url, output_dir)
    if xml_path:
        danmaku_data = parse_danmaku(xml_path)
        danmaku_info = {
            "available": True,
            "count": danmaku_data["total_count"],
            "unique_count": danmaku_data["unique_count"],
            "frequent": danmaku_data["frequent"][:15],
            "file": str(output_dir / "danmaku.json"),
        }
        save_json(danmaku_data, output_dir / "danmaku.json")
        print(f"  → {danmaku_data['total_count']} danmaku items", file=sys.stderr)

    # Comments
    comments_info = {"available": False, "count": 0, "top_liked": []}
    if aid:
        print("💬 Fetching comments...", file=sys.stderr)
        comments_data = fetch_comments(aid, max_pages=3)
        comments_info = {
            "available": True,
            "count": comments_data["total_count"],
            "fetched": comments_data["fetched_count"],
            "top_liked": [
                {"user": c["user"], "message": c["message"][:300], "like": c["like"]}
                for c in comments_data["top_liked"][:8]
            ],
            "file": str(output_dir / "comments.json"),
        }
        save_json(comments_data, output_dir / "comments.json")
        print(f"  → {comments_data['total_count']} comments (fetched {comments_data['fetched_count']})", file=sys.stderr)

    output = {
        "title": info.get("title", ""),
        "uploader": info.get("uploader", ""),
        "duration": info.get("duration", 0),
        "description": info.get("description", ""),
        "source": source,
        "char_count": len(text),
        "text_file": str(text_path),
        "text_preview": text[:2000],
        "danmaku": danmaku_info,
        "comments": comments_info,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
