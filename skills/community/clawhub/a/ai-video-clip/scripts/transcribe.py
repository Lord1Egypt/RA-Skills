#!/usr/bin/env python3
"""Transcribe — 高精度语音转录，输出结构化 packed transcript。

支持:
  - 本地 Whisper（openai-whisper / faster-whisper）
  - FunClip / Alibaba Damo ASR
  - 词级时间戳 + confidence + 说话人分离
  - 输出 packed transcript JSON，供 LLM 分析

使用:
  python3 transcribe.py --input video.mp4 --engine whisper --output transcript.json
  python3 transcribe.py --input video.mp4 --engine whisper --language zh --diarize
"""

import argparse
import json
import os
import subprocess
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional


@dataclass
class Phrase:
    start: float
    end: float
    text: str
    speaker: str = "S0"
    confidence: float = 0.0
    words: list = field(default_factory=list)  # [{word, start, end, confidence}]


@dataclass
class Transcript:
    source: str
    duration: float
    language: str = "unknown"
    engine: str = "whisper"
    phrases: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def get_video_duration(video_path: str) -> float:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    return 0.0


def extract_audio(video_path: str, audio_path: str) -> bool:
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
           "-ar", "16000", "-ac", "1", audio_path]
    return subprocess.run(cmd, capture_output=True).returncode == 0


def transcribe_whisper(audio_path: str, language: Optional[str] = None,
                        model: str = "medium") -> Transcript:
    try:
        import whisper
    except ImportError:
        print("警告: openai-whisper 未安装，尝试 faster-whisper...", file=sys.stderr)
        return _transcribe_faster_whisper(audio_path, language, model)

    model_instance = whisper.load_model(model)
    transcribe_opts = {
        "word_timestamps": True,
        "verbose": False,
    }
    if language:
        transcribe_opts["language"] = language

    result = model_instance.transcribe(audio_path, **transcribe_opts)

    language = result.get("language", "unknown")
    phrases = []

    for segment in result.get("segments", []):
        words = []
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": round(w["start"], 2),
                "end": round(w["end"], 2),
                "confidence": round(w.get("confidence", 0), 2),
            })

        phrases.append(Phrase(
            start=round(segment["start"], 2),
            end=round(segment["end"], 2),
            text=segment["text"].strip(),
            confidence=round(segment.get("confidence", 0), 2),
            words=words,
        ))

    return Transcript(
        source=os.path.basename(audio_path),
        duration=result.get("duration", 0),
        language=language,
        engine="whisper",
        phrases=phrases,
    )


def _transcribe_faster_whisper(audio_path: str, language: Optional[str] = None,
                                 model: str = "medium") -> Transcript:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("错误: 未找到任何 Whisper 引擎。安装 openai-whisper 或 faster-whisper",
              file=sys.stderr)
        sys.exit(1)

    model_size = model.replace("-", "_") if "-" in model else model
    model_instance = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model_instance.transcribe(
        audio_path,
        language=language,
        word_timestamps=True,
        beam_size=5,
    )

    phrases = []
    for segment in segments:
        words = []
        if segment.words:
            for w in segment.words:
                words.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 2),
                    "end": round(w.end, 2),
                    "confidence": round(w.probability, 2),
                })

        phrases.append(Phrase(
            start=round(segment.start, 2),
            end=round(segment.end, 2),
            text=segment.text.strip(),
            confidence=round(segment.avg_logprob, 2) if segment.avg_logprob else 0,
            words=words,
        ))

    return Transcript(
        source=os.path.basename(audio_path),
        duration=info.duration,
        language=info.language,
        engine="faster-whisper",
        phrases=phrases,
    )


def transcribe_funclip(video_path: str) -> Transcript:
    try:
        import funasr
        from funasr import AutoModel
    except ImportError:
        print("错误: funasr 未安装。安装: pip install funasr funclip", file=sys.stderr)
        sys.exit(1)

    # FunClip 使用 Alibaba DAMO 模型，中文效果好
    try:
        model = AutoModel(
            model="iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
            vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
            punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        )
    except Exception as e:
        print(f"错误: 无法加载 FunASR 模型: {e}", file=sys.stderr)
        sys.exit(1)

    result = model.generate(input=video_path)

    phrases = []
    if result and len(result) > 0:
        res = result[0]
        text = res.get("text", "")
        timestamps = res.get("timestamp", [])

        # FunASR returns sentences with timestamps
        if timestamps:
            for sent in timestamps:
                if len(sent) >= 3:
                    start = float(sent[0]) / 1000.0
                    end = float(sent[1]) / 1000.0
                    txt = sent[2] if isinstance(sent[2], str) else ""
                    if txt.strip():
                        phrases.append(Phrase(
                            start=round(start, 2),
                            end=round(end, 2),
                            text=txt.strip(),
                        ))
        else:
            # Fallback: single phrase
            phrases.append(Phrase(
                start=0,
                end=0,
                text=text.strip(),
            ))

    return Transcript(
        source=os.path.basename(video_path),
        duration=get_video_duration(video_path),
        language="zh",
        engine="funclip",
        phrases=phrases,
    )


def add_speakers(transcript: Transcript) -> Transcript:
    """尝试用 pyannote-audio 进行说话人分离。"""
    try:
        from pyannote.audio import Pipeline
    except ImportError:
        print("警告: pyannote-audio 未安装，跳过说话人分离", file=sys.stderr)
        return transcript

    print("  正在执行说话人分离 (pyannote-audio)...")
    # pyannote 需要 HuggingFace token
    hf_token = os.environ.get("HF_TOKEN", "")
    if not hf_token:
        print("警告: 未设置 HF_TOKEN，跳过说话人分离", file=sys.stderr)
        return transcript

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.0",
        use_auth_token=hf_token,
    )

    # 需要音频文件路径
    audio_file = getattr(transcript, '_audio_path', None)
    if not audio_file:
        return transcript

    from pyannote.core import Segment
    diarization = pipeline(audio_file)

    for phrase in transcript.phrases:
        mid = (phrase.start + phrase.end) / 2
        segment = Segment(mid, mid + 0.01)
        try:
            for track, speaker in diarization.itertracks(yield_label=True):
                if track.start <= mid <= track.end:
                    phrase.speaker = speaker
                    break
        except Exception:
            pass

    return transcript


def format_packed(transcript: Transcript) -> str:
    """将 transcript 格式化为紧凑的可读文本（供 LLM 阅读）。"""
    lines = []
    for i, phrase in enumerate(transcript.phrases):
        start = phrase.start
        end = phrase.end
        duration = end - start
        speaker = phrase.speaker
        text = phrase.text

        # 格式: [002.52-005.36] S0 Ninety percent of what a web agent does...
        lines.append(
            f"  [{start:07.2f}-{end:07.2f}] {speaker} {text}"
        )
        if phrase.words:
            word_tokens = []
            for w in phrase.words:
                word_tokens.append(f"{w['word']}@{w['start']:.2f}")
            lines.append(f"    words: {' | '.join(word_tokens)}")

    header = (
        f"## {os.path.basename(transcript.source)}  "
        f"(duration: {transcript.duration:.1f}s, "
        f"lang: {transcript.language}, engine: {transcript.engine}, "
        f"{len(transcript.phrases)} phrases)\n"
    )
    return header + "\n".join(lines)


def to_dict(transcript: Transcript) -> dict:
    """转换为 JSON 可序列化的字典。"""
    data = asdict(transcript)
    data["created_at"] = datetime.now().isoformat()
    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="语音转录工具")
    p.add_argument("--input", required=True, help="输入视频/音频文件")
    p.add_argument("--engine", default="whisper",
                   choices=["whisper", "faster-whisper", "funclip"],
                   help="转录引擎 (默认: whisper)")
    p.add_argument("--language", help="语言代码 (zh/en/auto)")
    p.add_argument("--model", default="medium",
                   help="Whisper 模型大小 (tiny/base/small/medium/large)")
    p.add_argument("--diarize", action="store_true", help="说话人分离")
    p.add_argument("--output", default="transcript.json", help="输出文件")
    p.add_argument("--format", default="json",
                   choices=["json", "packed"], help="输出格式")
    p.add_argument("--keep-audio", action="store_true", help="保留提取的音频文件")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    audio_path = args.input
    is_video = args.input.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'))

    if is_video:
        print(f"提取音频: {os.path.basename(args.input)}")
        tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio_path = tmp_audio.name
        if not extract_audio(args.input, audio_path):
            print("错误: 音频提取失败", file=sys.stderr)
            sys.exit(1)

    print(f"转录引擎: {args.engine}, 模型: {args.model}")
    if args.engine in ("whisper", "faster-whisper"):
        transcript = transcribe_whisper(audio_path, args.language, args.model)
    elif args.engine == "funclip":
        transcript = transcribe_funclip(args.input)

    # 说话人分离
    if args.diarize:
        transcript._audio_path = audio_path
        transcript = add_speakers(transcript)

    # 输出
    if args.format == "packed":
        packed_text = format_packed(transcript)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(packed_text)
        print(f"\n转录完成: {args.output}")
        print(f"  {len(transcript.phrases)} phrases, {transcript.duration:.1f}s")
        print(f"  packed text: {len(packed_text)} bytes")
    else:
        data = to_dict(transcript)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n转录完成: {args.output}")
        print(f"  语言: {transcript.language}")
        print(f"  时长: {transcript.duration:.1f}s")
        print(f"  phrases: {len(transcript.phrases)}")
        total_words = sum(len(p.words) for p in transcript.phrases)
        print(f"  词级标注: {total_words} words")

    # 清理
    if is_video and not args.keep_audio and audio_path != args.input:
        os.unlink(audio_path)
