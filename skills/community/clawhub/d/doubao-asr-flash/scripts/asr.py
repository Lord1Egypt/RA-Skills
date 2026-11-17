#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doubao-asr — 火山引擎豆包语音识别（录音文件极速版 flash 接口）

把音频/视频文件转成文字：
  - 本地文件（wav/mp3/ogg 直传；m4a/flac/aac/视频等自动用 ffmpeg 转 mp3）
  - 公网 URL（直传，跳过上传）
一次 HTTP POST 返回结果，无需轮询。

鉴权（新版控制台）：
  X-Api-Key           专属 API Key（控制台"语音技术"开通后创建）
  X-Api-Resource-Id   volc.bigasr.auc_turbo
  X-Api-Request-Id    随机 UUID
  X-Api-Sequence      -1

价格：极速版 4.5 元/小时（按音频时长计费）。限制：≤2h、≤100MB。

API Key 获取优先级：--api-key 参数 > 环境变量 DOUBAO_ASR_API_KEY
> 配置文件 ~/.config/doubao-asr/config.json
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Optional

import warnings
warnings.filterwarnings("ignore", message=r"urllib3 v2 only supports OpenSSL.*")

try:
    import requests
except ImportError:
    print("缺少 requests 库，请先安装: pip3 install requests", file=sys.stderr)
    sys.exit(2)

FLASH_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash"
RESOURCE_ID = "volc.bigasr.auc_turbo"
CONFIG_PATH = os.path.expanduser("~/.config/doubao-asr/config.json")

# 限制
MAX_SIZE = 100 * 1024 * 1024   # 100MB
MAX_DURATION = 2 * 3600        # 2 小时（秒）

# flash 支持直接上传的格式；其他格式用 ffmpeg 转 mp3
DIRECT_EXTS = {".wav", ".mp3", ".ogg"}
# 视频/其他音频扩展名 → 需要转码
TRANSCODE_EXTS = {
    ".m4a", ".flac", ".aac", ".amr", ".wma", ".opus", ".mp4", ".mov", ".mkv",
    ".avi", ".webm", ".flv", ".ts", ".m4v", ".3gp", ".caf", ".aiff", ".aif",
}


def get_api_key(args_key: Optional[str]) -> str:
    """按优先级取 API Key。"""
    if args_key:
        return args_key
    env = os.environ.get("DOUBAO_ASR_API_KEY", "").strip()
    if env:
        return env
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            key = (cfg.get("api_key") or "").strip()
            if key:
                return key
        except Exception:
            pass
    print("未找到 API Key。请通过以下任一方式提供：", file=sys.stderr)
    print("  1) 环境变量: export DOUBAO_ASR_API_KEY=<你的Key>", file=sys.stderr)
    print("  2) 命令行参数: --api-key <你的Key>", file=sys.stderr)
    print("  3) 配置文件: ~/.config/doubao-asr/config.json ({\"api_key\": \"...\"})", file=sys.stderr)
    print("获取方法见 SKILL.md 的『配置』一节。", file=sys.stderr)
    sys.exit(1)


def check_ffmpeg() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=10)
        return True
    except Exception:
        return False


def probe_duration(path: str) -> Optional[float]:
    """用 ffprobe 获取音频时长（秒），失败返回 None。"""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=60,
        )
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return None


def transcode_to_mp3(src: str, dst: str) -> None:
    """用 ffmpeg 把任意音频/视频转为 16k 单声道 mp3。"""
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-vn", "-ar", "16000", "-ac", "1", "-b:a", "64k",
        dst,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        print(f"ffmpeg 转码失败:\n{r.stderr[-2000:]}", file=sys.stderr)
        sys.exit(2)


def prepare_audio(input_path: str) -> tuple:
    """返回 (处理后的音频路径, 是否需要清理临时文件)。"""
    ext = os.path.splitext(input_path)[1].lower()
    size = os.path.getsize(input_path)
    dur = probe_duration(input_path)

    if dur is not None and dur > MAX_DURATION:
        print(f"错误: 音频时长 {dur/3600:.1f} 小时超过 flash 极速版上限 2 小时。"
              f"请先截取分段，或改用录音文件识别标准版（submit/query 异步接口）。", file=sys.stderr)
        sys.exit(2)

    if ext in DIRECT_EXTS and size <= MAX_SIZE:
        return input_path, False  # 直接上传

    if size > MAX_SIZE:
        print(f"错误: 文件 {size/1024/1024:.0f}MB 超过 100MB 上限，无法自动压缩，"
              f"请分段处理。", file=sys.stderr)
        sys.exit(2)

    if not check_ffmpeg():
        print("错误: 文件格式需要 ffmpeg 转码，但系统未安装 ffmpeg。"
              "安装: brew install ffmpeg", file=sys.stderr)
        sys.exit(2)

    tmpdir = tempfile.mkdtemp(prefix="doubao-asr-")
    out = os.path.join(tmpdir, "audio.mp3")
    print(f"[prep] 用 ffmpeg 转码为 16k 单声道 mp3 ...", file=sys.stderr)
    transcode_to_mp3(input_path, out)
    if os.path.getsize(out) > MAX_SIZE:
        print(f"错误: 转码后 {os.path.getsize(out)/1024/1024:.0f}MB 仍超 100MB 上限，"
              f"请分段处理。", file=sys.stderr)
        sys.exit(2)
    return out, True


def recognize(api_key: str, audio: dict, uid: Optional[str] = None) -> dict:
    """调用 flash 接口，返回完整响应 JSON。"""
    headers = {
        "X-Api-Key": api_key,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Request-Id": str(uuid.uuid4()),
        "X-Api-Sequence": "-1",
        "Content-Type": "application/json",
    }
    payload = {
        "user": {"uid": uid or api_key},
        "audio": audio,
        "request": {"model_name": "bigmodel"},
    }
    # 大文件 base64 上传可能较慢；2h 音频 flash 处理一般 1~3 分钟
    r = requests.post(FLASH_URL, json=payload, headers=headers, timeout=900)
    status_code = r.headers.get("X-Api-Status-Code", "")
    message = r.headers.get("X-Api-Message", "")
    logid = r.headers.get("X-Tt-Logid", "")
    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text[:2000]}

    if r.status_code != 200 or status_code not in ("", "20000000"):
        print(f"识别失败: HTTP {r.status_code}  X-Api-Status-Code={status_code}"
              f"  X-Api-Message={message}  logid={logid}", file=sys.stderr)
        if isinstance(body, dict):
            print(json.dumps(body, ensure_ascii=False, indent=2)[:2000], file=sys.stderr)
        sys.exit(1)

    return body


def ms_to_ts(ms: int) -> str:
    """毫秒 → SRT 时间戳 HH:MM:SS,mmm"""
    ms = max(0, int(ms))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(body: dict) -> str:
    """从完整响应体生成 SRT 字幕（utterances 含逐句时间戳）。"""
    utts = (body.get("result") or {}).get("utterances") or []
    if not utts:
        return ""
    lines = []
    for i, u in enumerate(utts, 1):
        text = (u.get("text") or "").strip()
        if not text:
            continue
        lines.append(str(i))
        lines.append(f"{ms_to_ts(u.get('start_time', 0))} --> {ms_to_ts(u.get('end_time', 0))}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="火山引擎豆包语音识别（录音文件极速版）— 音频/视频转文字")
    ap.add_argument("input", help="本地音频/视频文件路径，或公网音频 URL")
    ap.add_argument("--api-key", help="火山引擎语音技术专属 API Key（默认读环境变量 DOUBAO_ASR_API_KEY）")
    ap.add_argument("--uid", help="请求体 user.uid（默认与 api key 相同）")
    ap.add_argument("--out", help="结果保存到文件（可选）")
    ap.add_argument("--json", action="store_true", help="输出完整 JSON（含逐句时间戳）")
    ap.add_argument("--srt", action="store_true", help="额外导出 SRT 字幕（需输出文件 --out，或写 .srt）")
    ap.add_argument("--quiet", action="store_true", help="不打印预处理日志")
    args = ap.parse_args()

    api_key = get_api_key(args.api_key)
    is_url = args.input.startswith(("http://", "https://"))

    if is_url:
        audio = {"url": args.input}
        cleanup = False
        local_path = None
    else:
        if not os.path.exists(args.input):
            print(f"文件不存在: {args.input}", file=sys.stderr)
            sys.exit(2)
        path, cleanup = prepare_audio(args.input)
        local_path = path
        if not args.quiet and path != args.input:
            pass  # 转码日志已在 prepare_audio 里打印
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        audio = {"data": b64}

    t0 = time.time()
    if not args.quiet:
        print(f"[asr] 正在识别 ... (音频时长按量计费，极速版 4.5 元/小时)", file=sys.stderr)
    body = recognize(api_key, audio, uid=args.uid)
    elapsed = time.time() - t0

    result = body.get("result") or {}
    text = (result.get("text") or "").strip()

    if args.json:
        out_str = json.dumps(body, ensure_ascii=False, indent=2)
    else:
        out_str = text or "(未识别到内容，可能为静音)"

    if args.out:
        if args.srt and args.out.endswith(".srt"):
            pass  # 纯字幕文件，下面单独写
        else:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out_str + "\n")
            print(f"已保存到: {args.out}")
    else:
        print(out_str)

    if args.srt:
        srt = to_srt(body)
        if srt:
            srt_path = args.out if args.out and args.out.endswith(".srt") else (
                args.out + ".srt" if args.out else
                os.path.splitext(args.input)[0] + ".srt")
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt + "\n")
            print(f"SRT 字幕已保存到: {srt_path}")

    if cleanup and local_path:
        shutil.rmtree(os.path.dirname(local_path), ignore_errors=True)

    if not args.quiet:
        dur_ms = (body.get("audio_info") or {}).get("duration")
        dur_s = f"{int(dur_ms)/1000:.1f}s" if dur_ms else "?"
        print(f"[asr] 完成，耗时 {elapsed:.1f}s，音频时长 {dur_s}", file=sys.stderr)


if __name__ == "__main__":
    main()
