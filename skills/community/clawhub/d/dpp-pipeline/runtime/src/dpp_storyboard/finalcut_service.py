from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .composition_schema import CompositionResultReport
from .finalcut_schema import build_finalcut_result
from .schema import StoryboardReport
from .thumbnailer import COMMON_FFMPEG_PATHS

logger = logging.getLogger(__name__)
COMMON_FFPROBE_PATHS = tuple(
    str(Path(candidate).with_name("ffprobe")) for candidate in COMMON_FFMPEG_PATHS
)


@dataclass(frozen=True)
class VideoStreamProfile:
    width: int
    height: int
    sample_aspect_ratio: str
    avg_frame_rate: str


class FinalCutService:
    """将 compose-best 生成的视频片段替换回原视频对应分镜位置，输出最终合成视频。"""

    def __init__(self, ffmpeg_bin: str = "ffmpeg", ffprobe_bin: str = "ffprobe") -> None:
        self._ffmpeg_bin = ffmpeg_bin
        self._ffprobe_bin = ffprobe_bin

    def run(
        self,
        *,
        composition_result_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> Path:
        """执行最终剪辑合成，返回 finalcut_result.json 的路径。"""

        composition_file = Path(composition_result_path).expanduser().resolve()
        if not composition_file.is_file():
            raise FileNotFoundError(f"Composition result file not found: {composition_file}")

        composition = CompositionResultReport.model_validate_json(
            composition_file.read_text(encoding="utf-8")
        )

        if composition.generation.status != "succeeded":
            raise RuntimeError(
                f"Composition generation status is '{composition.generation.status}', "
                "final cut requires a succeeded generation."
            )
        if not composition.generation.downloaded_video_path:
            raise RuntimeError("Composition result does not contain a downloaded_video_path.")

        generated_video = Path(composition.generation.downloaded_video_path).expanduser().resolve()
        if not generated_video.is_file():
            raise FileNotFoundError(f"Generated video not found: {generated_video}")

        storyboard_file = Path(composition.storyboard_path).expanduser().resolve()
        if not storyboard_file.is_file():
            raise FileNotFoundError(f"Storyboard file not found: {storyboard_file}")

        storyboard = StoryboardReport.model_validate_json(
            storyboard_file.read_text(encoding="utf-8")
        )

        source_video = self._resolve_source_video_path(
            source_video=storyboard.source_video,
            storyboard_file=storyboard_file,
        )
        if not source_video.is_file():
            raise FileNotFoundError(f"Source video not found: {source_video}")

        start_sec = composition.best_segment.start_sec
        end_sec = composition.best_segment.end_sec

        target_dir = (
            Path(output_dir).expanduser().resolve()
            if output_dir is not None
            else composition_file.parent / "finalCut"
        )
        target_dir.mkdir(parents=True, exist_ok=True)

        output_video = target_dir / "final_cut.mp4"

        logger.info(
            "Assembling final cut: replacing segment %d [%.3fs - %.3fs] in source video.",
            composition.best_segment.segment_index,
            start_sec,
            end_sec,
        )

        self._assemble(
            source_video=source_video,
            generated_video=generated_video,
            start_sec=start_sec,
            end_sec=end_sec,
            output_path=output_video,
        )

        logger.info("Final cut video saved to %s", output_video)

        result = build_finalcut_result(
            composition_result_path=str(composition_file),
            source_video_path=str(source_video),
            generated_video_path=str(generated_video),
            best_segment_index=composition.best_segment.segment_index,
            replace_start_sec=start_sec,
            replace_end_sec=end_sec,
            output_video_path=str(output_video),
        )
        result_path = target_dir / "finalcut_result.json"
        result_path.write_text(
            json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        logger.info("Final cut result saved to %s", result_path)
        return result_path

    def _assemble(
        self,
        *,
        source_video: Path,
        generated_video: Path,
        start_sec: float,
        end_sec: float,
        output_path: Path,
    ) -> None:
        """使用 FFmpeg concat filter 将原视频前段 + generated 视频 + 原视频后段拼接输出。"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ffmpeg = self._resolve_ffmpeg_bin()
        source_profile = self._probe_video_stream(source_video)
        generated_profile = self._probe_video_stream(generated_video)
        source_video_prefix = (
            f"fps={source_profile.avg_frame_rate},"
            f"setsar={self._normalize_sar(source_profile.sample_aspect_ratio)}"
        )

        generated_video_filter = "[1:v]setpts=PTS-STARTPTS[v1]"
        if generated_profile != source_profile:
            generated_video_filter = (
                "[1:v]"
                f"scale={source_profile.width}:{source_profile.height}:force_original_aspect_ratio=decrease,"
                f"pad={source_profile.width}:{source_profile.height}:(ow-iw)/2:(oh-ih)/2,"
                f"fps={source_profile.avg_frame_rate},"
                f"setsar={self._normalize_sar(source_profile.sample_aspect_ratio)},"
                "setpts=PTS-STARTPTS[v1]"
            )

        filter_complex = (
            f"[0:v]trim=0:{start_sec:.3f},setpts=PTS-STARTPTS,{source_video_prefix}[v0];"
            f"[0:a]atrim=0:{start_sec:.3f},asetpts=PTS-STARTPTS[a0];"
            f"{generated_video_filter};"
            f"[1:a]asetpts=PTS-STARTPTS[a1];"
            f"[0:v]trim={end_sec:.3f},setpts=PTS-STARTPTS,{source_video_prefix}[v2];"
            f"[0:a]atrim={end_sec:.3f},asetpts=PTS-STARTPTS[a2];"
            f"[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[outv][outa]"
        )

        command = [
            resolved_ffmpeg,
            "-y",
            "-i", str(source_video),
            "-i", str(generated_video),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-c:a", "aac",
            "-b:a", "128k",
            str(output_path),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("ffmpeg is required for final cut assembly.") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise RuntimeError(f"ffmpeg final cut assembly failed: {stderr or exc}") from exc

    @staticmethod
    def _resolve_source_video_path(*, source_video: str, storyboard_file: Path) -> Path:
        """解析原视频路径，支持绝对路径、相对于 storyboard 目录、DPP_WORKDIR 和 cwd 的路径。"""

        raw = (source_video or "").strip()
        if not raw:
            raise ValueError("Storyboard source_video cannot be empty.")

        candidate = Path(raw).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()

        storyboard_relative = (storyboard_file.parent / candidate).resolve()
        if storyboard_relative.is_file():
            return storyboard_relative

        workdir_raw = (os.getenv("DPP_WORKDIR") or "").strip()
        if workdir_raw:
            workdir_relative = (Path(workdir_raw).expanduser().resolve() / candidate).resolve()
            if workdir_relative.is_file():
                return workdir_relative

        cwd_relative = (Path.cwd() / candidate).resolve()
        if cwd_relative.is_file():
            return cwd_relative

        return storyboard_relative

    def _resolve_ffmpeg_bin(self) -> str:
        """解析 ffmpeg 可执行文件路径。"""

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
        raise RuntimeError("ffmpeg is required for final cut assembly.")

    def _resolve_ffprobe_bin(self) -> str:
        resolved = shutil.which(self._ffprobe_bin)
        if resolved:
            return resolved
        binary_path = Path(self._ffprobe_bin)
        if binary_path.is_file():
            return str(binary_path)
        if binary_path.name == self._ffprobe_bin:
            for candidate in COMMON_FFPROBE_PATHS:
                candidate_path = Path(candidate)
                if candidate_path.is_file():
                    return str(candidate_path)
        raise RuntimeError("ffprobe is required for final cut assembly.")

    def _probe_video_stream(self, video_path: Path) -> VideoStreamProfile:
        resolved_ffprobe = self._resolve_ffprobe_bin()
        command = [
            resolved_ffprobe,
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,width,height,sample_aspect_ratio,avg_frame_rate",
            "-of",
            "json",
            str(video_path),
        ]
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("ffprobe is required for final cut assembly.") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise RuntimeError(f"ffprobe stream probing failed: {stderr or exc}") from exc

        try:
            payload = json.loads(completed.stdout or "{}")
        except json.JSONDecodeError as exc:
            raise RuntimeError("ffprobe returned invalid JSON for stream probing.") from exc

        for stream in payload.get("streams", []):
            if stream.get("codec_type") != "video":
                continue
            width = int(stream.get("width") or 0)
            height = int(stream.get("height") or 0)
            sample_aspect_ratio = str(stream.get("sample_aspect_ratio") or "1:1")
            avg_frame_rate = str(stream.get("avg_frame_rate") or "30/1")
            if width <= 0 or height <= 0:
                break
            return VideoStreamProfile(
                width=width,
                height=height,
                sample_aspect_ratio=sample_aspect_ratio,
                avg_frame_rate=avg_frame_rate,
            )

        raise RuntimeError(f"ffprobe did not return a valid video stream profile: {video_path}")

    @staticmethod
    def _normalize_sar(sample_aspect_ratio: str) -> str:
        raw = (sample_aspect_ratio or "").strip()
        if not raw or raw == "N/A":
            return "1/1"
        return raw.replace(":", "/")
