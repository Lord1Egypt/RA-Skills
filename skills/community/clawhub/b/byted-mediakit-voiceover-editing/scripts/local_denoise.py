"""
Local 人声降噪：使用 ffmpeg 内置滤镜。
"""
from __future__ import annotations

from pathlib import Path

from ffmpeg_utils import denoise_audio


def denoise_voice(
    input_audio: Path,
    output_audio: Path,
    method: str = "afftdn",
) -> Path:
    """
    本地人声降噪。

    method:
      - afftdn: FFT 降噪（推荐，稳态噪声效果好）
      - anlmdn: 非局部均值降噪（保真度更高）
      - combined: highpass+lowpass+afftdn（最强降噪，可能有失真）
    """
    return denoise_audio(input_audio, output_audio, method=method)
