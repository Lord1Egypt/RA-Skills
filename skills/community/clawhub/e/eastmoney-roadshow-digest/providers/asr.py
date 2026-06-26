from __future__ import annotations

import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path
from typing import Any, Dict, List


class ASRError(Exception):
    pass


class ASRUnavailable(ASRError):
    pass


def extract_audio(media_url: str, out_dir: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise ASRUnavailable("ffmpeg is not installed")
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_path = out_dir / "audio.mp3"
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        media_url,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(audio_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise ASRError(f"ffmpeg extract failed: {proc.stderr[-600:]}")
    return audio_path


def split_audio(audio_path: Path, out_dir: Path, segment_seconds: int = 30) -> List[Path]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise ASRUnavailable("ffmpeg is not installed")
    chunks_dir = out_dir / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    pattern = chunks_dir / "chunk_%03d.wav"
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(audio_path),
        "-f",
        "segment",
        "-segment_time",
        str(segment_seconds),
        "-c",
        "copy",
        str(pattern),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise ASRError(f"ffmpeg split failed: {proc.stderr[-600:]}")
    chunks = sorted(chunks_dir.glob("chunk_*.wav"))
    if not chunks:
        raise ASRError("audio split produced no chunks")
    return chunks


def _transcribe_chunk(model: Any, chunk_path: Path) -> List[Dict[str, Any]]:
    segments, _info = model.transcribe(str(chunk_path), vad_filter=True, beam_size=1, language="zh")
    out: List[Dict[str, Any]] = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            out.append({
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": text,
            })
    return out


def transcribe_audio(
    audio_path: Path,
    model_size: str = "small",
    segment_seconds: int = 45,
    total_timeout_seconds: int = 7200,
) -> Dict[str, Any]:
    try:
        from faster_whisper import WhisperModel
    except Exception as e:
        raise ASRUnavailable(f"faster-whisper unavailable: {e}")

    start_ts = time.time()
    chunks = split_audio(audio_path, audio_path.parent, segment_seconds=segment_seconds)
    try:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    except Exception as e:
        raise ASRError(f"model init failed: {e}")

    all_segments: List[Dict[str, Any]] = []
    texts: List[str] = []
    status = "ASR_complete"
    timeout_hit = False

    for idx, chunk in enumerate(chunks):
        elapsed = time.time() - start_ts
        remaining = total_timeout_seconds - elapsed
        if remaining <= 0:
            timeout_hit = True
            status = "ASR_partial"
            break
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                fut = pool.submit(_transcribe_chunk, model, chunk)
                chunk_segments = fut.result(timeout=max(10, min(remaining, 90)))
        except FuturesTimeoutError:
            timeout_hit = True
            status = "ASR_partial"
            break
        except Exception as e:
            raise ASRError(f"chunk {idx} transcription failed: {e}")

        offset = idx * segment_seconds
        for seg in chunk_segments:
            seg = {
                "start": round(seg["start"] + offset, 3),
                "end": round(seg["end"] + offset, 3),
                "text": seg["text"],
            }
            all_segments.append(seg)
            texts.append(seg["text"])

    if not all_segments and timeout_hit:
        raise ASRError("ASR timeout before any segment was completed")
    if not all_segments:
        raise ASRError("transcription produced no usable text")

    return {
        "engine": "faster-whisper",
        "model_size": model_size,
        "segment_seconds": segment_seconds,
        "status": status,
        "timeout_seconds": total_timeout_seconds,
        "timed_out": timeout_hit,
        "text": "\n".join(texts),
        "segments": all_segments,
        "completed_chunks": len({int(seg['start'] // segment_seconds) for seg in all_segments}),
        "total_chunks": len(chunks),
    }
