from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .schema import StoryboardReport


COMMON_FFMPEG_PATHS = (
    "/opt/homebrew/bin/ffmpeg",
    "/usr/local/bin/ffmpeg",
    "/opt/local/bin/ffmpeg",
)


class ThumbnailServiceError(RuntimeError):
    """Raised when thumbnail extraction fails."""


def build_thumbnail_filename(index: int) -> str:
    """Build the per-segment preview asset name."""
    return f"shot-{index:04d}.gif"


def midpoint_timestamp(start_sec: float, end_sec: float) -> float:
    """Return the temporal midpoint of a segment."""
    return start_sec + ((end_sec - start_sec) / 2.0)


def calculate_gif_duration(start_sec: float, end_sec: float) -> float:
    """Scale GIF duration to 10% of the segment, clamped to 1-10 seconds."""
    segment_duration = end_sec - start_sec
    scaled_duration = max(1.0, min(segment_duration * 0.1, 10.0))
    return min(segment_duration, scaled_duration)


def select_gif_window(start_sec: float, end_sec: float, target_duration: float) -> tuple[float, float]:
    """Choose a centered GIF window that stays within the segment bounds."""
    segment_duration = end_sec - start_sec
    if target_duration >= segment_duration:
        return (round(start_sec, 3), round(end_sec, 3))
    midpoint = midpoint_timestamp(start_sec, end_sec)
    window_start = midpoint - (target_duration / 2.0)
    window_end = window_start + target_duration
    return (round(window_start, 3), round(window_end, 3))


class FFmpegThumbnailService:
    """Render storyboard preview GIFs for each segment with ffmpeg."""

    def __init__(self, ffmpeg_bin: str = "ffmpeg") -> None:
        self._ffmpeg_bin = ffmpeg_bin

    def render(
        self,
        *,
        video_path: Path,
        report: StoryboardReport,
        thumbnails_dir: Path,
    ) -> StoryboardReport:
        """Render one GIF preview per segment and update thumbnail paths."""
        resolved_ffmpeg = self._resolve_ffmpeg_bin()
        thumbnails_dir.mkdir(parents=True, exist_ok=True)

        updated_segments = []
        for segment in report.segments:
            file_name = build_thumbnail_filename(segment.index)
            output_path = thumbnails_dir / file_name
            gif_duration = calculate_gif_duration(segment.start_sec, segment.end_sec)
            window_start, window_end = select_gif_window(
                segment.start_sec,
                segment.end_sec,
                gif_duration,
            )
            self._extract_gif(
                ffmpeg_bin=resolved_ffmpeg,
                video_path=video_path,
                start_sec=window_start,
                duration_sec=window_end - window_start,
                output_path=output_path,
            )
            updated_segments.append(
                segment.model_copy(
                    update={"thumbnail_path": str(Path("thumbnails") / file_name)}
                )
            )

        return report.model_copy(update={"segments": updated_segments})

    def _resolve_ffmpeg_bin(self) -> str:
        """Resolve the configured ffmpeg binary path."""
        resolved = shutil.which(self._ffmpeg_bin)
        if resolved:
            return resolved
        binary_path = Path(self._ffmpeg_bin)
        if binary_path.is_file():
            return str(binary_path)
        if binary_path.name == self._ffmpeg_bin:
            for candidate in COMMON_FFMPEG_PATHS:
                candidate_path = Path(candidate)
                if candidate_path.is_file():
                    return str(candidate_path)
        raise ThumbnailServiceError(
            f"ffmpeg binary not found: {self._ffmpeg_bin}. Install ffmpeg or set a valid binary path."
        )

    @staticmethod
    def _extract_gif(
        *,
        ffmpeg_bin: str,
        video_path: Path,
        start_sec: float,
        duration_sec: float,
        output_path: Path,
    ) -> None:
        """Run ffmpeg to render a palette-optimized GIF preview."""
        result = subprocess.run(
            [
                ffmpeg_bin,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                f"{start_sec:.3f}",
                "-t",
                f"{duration_sec:.3f}",
                "-i",
                str(video_path),
                "-filter_complex",
                (
                    "fps=8,"
                    "scale=720:-1:flags=lanczos,"
                    "split[s0][s1];"
                    "[s0]palettegen=stats_mode=diff[p];"
                    "[s1][p]paletteuse=dither=bayer:bayer_scale=5"
                ),
                "-an",
                "-loop",
                "0",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ThumbnailServiceError(
                f"ffmpeg failed while rendering {output_path.name}: {result.stderr.strip() or result.stdout.strip()}"
            )
        if not output_path.exists():
            raise ThumbnailServiceError(
                f"ffmpeg reported success but preview GIF was not created: {output_path}"
            )
