"""ASR 响应后处理"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TranscriptionResult:
    text: str
    language: str | None = None
    duration: float | None = None
    segments: list[dict] | None = None  # verbose_json 时有值


class Postprocessor:
    """将 funasr-server 原始响应转换为 TranscriptionResult"""

    def process(self, raw: dict | str, response_format: str) -> TranscriptionResult:
        """
        - json: raw = {"text": "..."} → TranscriptionResult(text=...)
        - text: raw = "..." → TranscriptionResult(text=raw)
        - verbose_json: raw = {"text": "...", "segments": [...], "language": "...", "duration": ...} → 完整结果
        """
        if response_format == "text":
            return TranscriptionResult(text=str(raw))

        if not isinstance(raw, dict):
            return TranscriptionResult(text=str(raw))

        text = raw.get("text", "")
        if response_format == "verbose_json":
            return TranscriptionResult(
                text=text,
                language=raw.get("language"),
                duration=raw.get("duration"),
                segments=raw.get("segments"),
            )

        # json
        return TranscriptionResult(text=text)

    # ─── 字幕格式化 ──────────────────────────

    @staticmethod
    def _format_timestamp(seconds: float, vtt: bool = False) -> str:
        """秒 → HH:MM:SS,mmm（SRT）或 HH:MM:SS.mmm（VTT）"""
        total_ms = max(0, int(round(float(seconds) * 1000)))
        hours, total_ms = divmod(total_ms, 3_600_000)
        minutes, total_ms = divmod(total_ms, 60_000)
        secs, ms = divmod(total_ms, 1000)
        sep = "." if vtt else ","
        return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{ms:03d}"

    @staticmethod
    def _cue_text(seg: dict) -> str:
        """segment 文本，带 speaker 时加 [SPKx] 前缀"""
        text = seg.get("text", "")
        speaker = seg.get("speaker")
        return f"[{speaker}] {text}" if speaker else text

    @staticmethod
    def to_srt(segments: list[dict]) -> str:
        """
        将 segments 转为 SRT 格式字符串。
        每个 segment: {"start": float(秒), "end": float(秒), "text": str, "speaker": str|None}

        SRT 格式：
        1
        00:00:01,234 --> 00:00:05,678
        你好世界

        2
        00:00:06,000 --> 00:00:10,500
        [SPK1] 我是第二个人
        """
        blocks = []
        for idx, seg in enumerate(segments, start=1):
            start = Postprocessor._format_timestamp(seg.get("start", 0.0))
            end = Postprocessor._format_timestamp(seg.get("end", 0.0))
            blocks.append(f"{idx}\n{start} --> {end}\n{Postprocessor._cue_text(seg)}")
        return "\n\n".join(blocks)

    @staticmethod
    def to_vtt(segments: list[dict]) -> str:
        """
        将 segments 转为 VTT 格式字符串。

        VTT 格式：
        WEBVTT

        00:00:01.234 --> 00:00:05.678
        你好世界

        注意：VTT 时间戳用 . 而非 , 分隔毫秒
        """
        blocks = []
        for seg in segments:
            start = Postprocessor._format_timestamp(seg.get("start", 0.0), vtt=True)
            end = Postprocessor._format_timestamp(seg.get("end", 0.0), vtt=True)
            blocks.append(f"{start} --> {end}\n{Postprocessor._cue_text(seg)}")
        return "WEBVTT\n\n" + "\n\n".join(blocks)
