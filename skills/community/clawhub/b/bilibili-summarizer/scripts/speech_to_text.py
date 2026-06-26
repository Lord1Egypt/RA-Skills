#!/usr/bin/env python3
"""
speech_to_text.py - 语音转文字（支持多引擎 + 说话人分离 + SRT导出）

用法:
    python3 speech_to_text.py <音频文件路径> [--engine auto|funasr|whisper|sensevoice]
    python3 speech_to_text.py <音频文件路径> --format srt     # 导出 SRT 字幕
    python3 speech_to_text.py <音频文件路径> --diarize        # 说话人分离（仅 FunASR）
    python3 speech_to_text.py <音频文件路径> --all            # 全部功能

依赖（按引擎）:
    auto / funasr:     pip install funasr modelscope torch torchaudio
    auto / whisper:    pip install openai-whisper
    auto / sensevoice: pip install funasr modelscope torch torchaudio

引擎选择优先级（auto模式）:
    1. funasr (Paraformer) - 中文最优，离线运行
    2. sensevoice - 阿里新一代，速度快
    3. whisper (openai-whisper) - 通用备选

输出:
    JSON 格式（打印到 stdout），包含带时间戳和纯文本两种字幕
"""

import sys
import os
import json
import time


def check_engine(engine: str) -> str:
    """检查引擎是否可用，不可用则尝试下一个"""
    if engine == "auto":
        for e in ["funasr", "sensevoice", "whisper"]:
            if check_engine(e):
                return e
        return ""

    if engine == "funasr":
        try:
            from funasr import AutoModel
            return "funasr"
        except ImportError:
            return ""

    if engine == "sensevoice":
        try:
            from funasr import AutoModel
            return "sensevoice"
        except ImportError:
            return ""

    if engine == "whisper":
        try:
            import whisper
            return "whisper"
        except ImportError:
            return ""

    return ""


def run_funasr(audio_path: str, diarize: bool = False) -> list:
    """使用 FunASR Paraformer 模型"""
    from funasr import AutoModel

    print("[*] 加载 FunASR Paraformer 模型（首次运行会下载约 1GB）...", file=sys.stderr)

    model_kwargs = {
        "model": "paraformer-zh",
        "vad_model": "fsmn-vad",
        "punc_model": "ct-punc-c",
        "disable_update": True,
    }

    # 说话人分离需要额外加载 SD 模型
    sd_model = None
    if diarize:
        try:
            print("[*] 加载说话人分离模型（SD）...", file=sys.stderr)
            sd_model = AutoModel(
                model="cam++",
                disable_update=True,
            )
            print("[*] 说话人分离模型加载成功", file=sys.stderr)
        except Exception as e:
            print(f"[!] 说话人分离模型加载失败，将使用普通识别: {e}", file=sys.stderr)
            sd_model = None

    model = AutoModel(**model_kwargs)
    print("[*] 开始语音识别...", file=sys.stderr)
    start = time.time()

    if sd_model:
        # 使用说话人分离模式
        res = model.generate(
            input=audio_path,
            batch_size_s=300,
            hotword="",
            sd_model=sd_model,
        )
    else:
        res = model.generate(
            input=audio_path,
            batch_size_s=300,
            hotword="",
        )

    elapsed = time.time() - start
    print(f"[*] 识别完成，耗时 {elapsed:.1f}s", file=sys.stderr)

    segments = []

    if res and res[0].get("sentence_info"):
        for sent in res[0]["sentence_info"]:
            start_ms = sent.get("start", 0)
            end_ms = sent.get("end", 0)
            text_seg = sent.get("text", "").strip()
            speaker = sent.get("spk", "")
            if text_seg:
                seg = {
                    "from": start_ms / 1000,
                    "to": end_ms / 1000,
                    "content": text_seg,
                }
                if speaker:
                    seg["speaker"] = str(speaker)
                segments.append(seg)
    else:
        text = res[0].get("text", "") if res else ""
        total_dur = _get_audio_duration(audio_path)
        if text and total_dur:
            segments = _estimate_timestamps(text, total_dur)

    return segments


def run_sensevoice(audio_path: str) -> list:
    """使用 SenseVoice 模型（速度快）"""
    from funasr import AutoModel

    print("[*] 加载 SenseVoice 模型...", file=sys.stderr)
    model = AutoModel(
        model="iic/SenseVoiceSmall",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        disable_update=True,
    )
    print("[*] 开始语音识别...", file=sys.stderr)
    start = time.time()

    res = model.generate(
        input=audio_path,
        batch_size_s=60,
        language="auto",
        use_itn=True,
    )

    elapsed = time.time() - start
    print(f"[*] 识别完成，耗时 {elapsed:.1f}s", file=sys.stderr)

    segments = []
    total_dur = _get_audio_duration(audio_path)

    if res:
        text = res[0].get("text", "")
        if text:
            segments = _estimate_timestamps(text, total_dur) if total_dur else []

    return segments


def run_whisper(audio_path: str) -> list:
    """使用 OpenAI Whisper 模型"""
    import whisper

    print("[*] 加载 Whisper 模型 (base)（首次运行会下载约 140MB）...", file=sys.stderr)
    model = whisper.load_model("base")
    print("[*] 开始语音识别...", file=sys.stderr)
    start = time.time()

    result = model.transcribe(audio_path, language="zh", verbose=False)

    elapsed = time.time() - start
    print(f"[*] 识别完成，耗时 {elapsed:.1f}s", file=sys.stderr)

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "from": seg["start"],
            "to": seg["end"],
            "content": seg["text"].strip(),
        })

    return segments


def _get_audio_duration(audio_path: str) -> float:
    """用 ffprobe 获取音频时长"""
    import subprocess
    import shutil
    ffprobe = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
    if not ffprobe or not os.path.exists(ffprobe):
        return 0
    try:
        cmd = [ffprobe, "-v", "quiet", "-show_entries", "format=duration",
               "-of", "csv=p=0", audio_path]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(out.stdout.strip())
    except Exception:
        return 0


def _estimate_timestamps(text, total_dur):
    """无精确时间戳时，按字符数比例估算"""
    segments = []
    sentences = []
    current = ""
    for ch in text:
        current += ch
        if ch in "，。！？；\n" or len(current) >= 40:
            s = current.strip()
            if s:
                sentences.append(s)
            current = ""
    if current.strip():
        sentences.append(current.strip())

    total_chars = sum(len(s) for s in sentences)
    if total_chars == 0:
        return segments

    cursor = 0
    for sent in sentences:
        ratio = len(sent) / total_chars
        dur = ratio * total_dur
        segments.append({
            "from": round(cursor, 2),
            "to": round(cursor + dur, 2),
            "content": sent,
        })
        cursor += dur

    return segments


# ---------- 格式转换 ----------

def segments_to_timed_text(segments, show_speaker=False):
    """转为 [MM:SS] 内容 格式，可选显示说话人"""
    lines = []
    for seg in segments:
        t = seg["from"]
        mm = int(t // 60)
        ss = int(t % 60)
        speaker = seg.get("speaker", "")
        prefix = f"[{mm:02d}:{ss:02d}]"
        if speaker and show_speaker:
            prefix = f"[{mm:02d}:{ss:02d}][说话人{speaker}]"
        lines.append(f"{prefix} {seg['content']}")
    return "\n".join(lines)


def segments_to_plain(segments):
    """纯文本"""
    return " ".join(seg["content"].strip() for seg in segments if seg.get("content", "").strip())


def segments_to_srt(segments):
    """转为标准 SRT 字幕格式"""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = _seconds_to_srt_time(seg.get("from", 0))
        end = _seconds_to_srt_time(seg.get("to", seg.get("from", 0) + 1))
        text = seg.get("content", "").strip()
        speaker = seg.get("speaker", "")

        if text:
            if speaker:
                text = f"[说话人{speaker}] {text}"
            lines.append(str(i))
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


# ---------- 主流程 ----------

def run(audio_path: str, engine: str = "auto", output_format: str = "json", diarize: bool = False):
    if not os.path.exists(audio_path):
        print(json.dumps({"error": f"音频文件不存在: {audio_path}"}))
        sys.exit(1)

    actual_engine = check_engine(engine)
    if not actual_engine:
        print(json.dumps({
            "error": "无可用 ASR 引擎。请安装: pip install funasr modelscope torch torchaudio",
            "hint": "推荐安装 FunASR（中文效果最佳）: pip install funasr modelscope torch torchaudio",
        }))
        sys.exit(1)

    print(f"[*] 使用引擎: {actual_engine}", file=sys.stderr)

    if actual_engine == "funasr":
        segments = run_funasr(audio_path, diarize=diarize)
    elif actual_engine == "sensevoice":
        segments = run_sensevoice(audio_path)
    elif actual_engine == "whisper":
        segments = run_whisper(audio_path)
    else:
        segments = []

    has_speakers = any(seg.get("speaker") for seg in segments)
    timed_text = segments_to_timed_text(segments, show_speaker=has_speakers)
    plain_text = segments_to_plain(segments)
    srt_text = segments_to_srt(segments)

    # 说话人统计
    speaker_stats = {}
    if has_speakers:
        for seg in segments:
            spk = seg.get("speaker", "unknown")
            speaker_stats[spk] = speaker_stats.get(spk, 0) + 1

    result = {
        "engine": actual_engine,
        "audio_path": audio_path,
        "diarize": diarize and has_speakers,
        "subtitle": {
            "timed_text": timed_text,
            "plain_text": plain_text,
            "srt_text": srt_text,
            "char_count": len(plain_text),
            "segment_count": len(segments),
            "segments": segments,
        },
    }

    if has_speakers:
        result["speaker_stats"] = speaker_stats
        result["subtitle"]["speaker_count"] = len(speaker_stats)

    # 如果只需要 SRT 格式输出
    if output_format == "srt":
        print(srt_text)
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 speech_to_text.py 音频文件 [--engine auto|funasr|whisper|sensevoice]", file=sys.stderr)
        print("      python3 speech_to_text.py 音频文件 --format srt    # 导出 SRT 字幕", file=sys.stderr)
        print("      python3 speech_to_text.py 音频文件 --diarize       # 说话人分离", file=sys.stderr)
        sys.exit(1)

    audio_file = sys.argv[1]
    engine = "auto"
    output_format = "json"
    diarize = False

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--engine" and i + 1 < len(sys.argv):
            engine = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--diarize":
            diarize = True
            i += 1
        else:
            i += 1

    run(audio_file, engine, output_format, diarize)
