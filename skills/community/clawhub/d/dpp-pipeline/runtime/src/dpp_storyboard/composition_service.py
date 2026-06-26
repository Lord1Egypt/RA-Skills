from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
import urllib.request
from json import JSONDecodeError
from pathlib import Path
from urllib.parse import urlparse
from typing import Callable

from pydantic import ValidationError

from .ark_client import ArkClient
from .cdn_upload import CDNUploadError, CDNUploader
from .composition_schema import (
    CompositionPromptDraft,
    VideoGenerationResult,
    build_best_segment_reference,
    build_composition_result_report,
)
from .config import Settings
from .material import load_material_config
from .placement_schema import PlacementAnalysisReport, PlacementCandidate
from .schema import StoryboardReport, StoryboardSegment
from .service import extract_json_payload
from .thumbnailer import COMMON_FFMPEG_PATHS

logger = logging.getLogger(__name__)
COMMON_FFPROBE_PATHS = tuple(
    str(Path(candidate).with_name("ffprobe")) for candidate in COMMON_FFMPEG_PATHS
)

class FFmpegClipService:
    def __init__(self, ffmpeg_bin: str = "ffmpeg", ffprobe_bin: str = "ffprobe") -> None:
        self._ffmpeg_bin = ffmpeg_bin
        self._ffprobe_bin = ffprobe_bin

    def render(
        self,
        *,
        video_path: Path,
        start_sec: float,
        end_sec: float,
        output_path: Path,
    ) -> Path:
        duration = end_sec - start_sec
        if duration <= 0:
            raise ValueError("Reference clip duration must be greater than 0.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ffmpeg = self._resolve_ffmpeg_bin()
        command = [
            resolved_ffmpeg,
            "-y",
            "-i",
            str(video_path),
            "-ss",
            f"{start_sec:.3f}",
            "-t",
            f"{duration:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
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
            raise RuntimeError("ffmpeg is required for best-segment clip extraction.") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise RuntimeError(f"ffmpeg clip extraction failed: {stderr or exc}") from exc
        return output_path

    def probe_duration(self, video_path: Path) -> float:
        resolved_ffprobe = self._resolve_ffprobe_bin()
        command = [
            resolved_ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
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
            raise RuntimeError("ffprobe is required for reference clip duration probing.") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise RuntimeError(f"ffprobe duration probing failed: {stderr or exc}") from exc

        raw_duration = (completed.stdout or "").strip()
        try:
            duration = float(raw_duration)
        except ValueError as exc:
            raise RuntimeError(f"ffprobe returned an invalid duration: {raw_duration!r}") from exc
        if duration <= 0:
            raise RuntimeError(f"ffprobe returned a non-positive duration: {duration}")
        return duration

    def _resolve_ffmpeg_bin(self) -> str:
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
        raise RuntimeError("ffmpeg is required for best-segment clip extraction.")

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
        raise RuntimeError("ffprobe is required for reference clip duration probing.")


class GeneratedAssetDownloader:
    def download_video(self, *, url: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=120) as response, output_path.open("wb") as destination:
            shutil.copyfileobj(response, destination)
        return output_path


class BestSegmentCompositionService:
    def __init__(
        self,
        settings: Settings,
        client: ArkClient | None = None,
        clipper: FFmpegClipService | None = None,
        uploader: CDNUploader | None = None,
        downloader: GeneratedAssetDownloader | None = None,
        sleeper: Callable[[float], None] | None = None,
    ) -> None:
        self._settings = settings
        self._client = client or ArkClient(settings)
        self._clipper = clipper or FFmpegClipService()
        self._uploader = uploader or CDNUploader(settings)
        self._downloader = downloader or GeneratedAssetDownloader()
        self._sleeper = sleeper or time.sleep

    def run(
        self,
        *,
        storyboard_path: str | Path,
        placement_analysis_path: str | Path,
        material_config_path: str | Path,
        output_dir: str | Path | None = None,
        prompt_model: str | None = None,
        generation_model: str | None = None,
        reference_video_url: str | None = None,
        duration: int | None = None,
        retry: int = 1,
        generate_audio: bool = True,
        prompt_only: bool = False,
    ) -> Path:
        storyboard_file = Path(storyboard_path).expanduser().resolve()
        placement_file = Path(placement_analysis_path).expanduser().resolve()
        material_file = Path(material_config_path).expanduser().resolve()
        if not storyboard_file.is_file():
            raise FileNotFoundError(f"Storyboard file not found: {storyboard_file}")
        if not placement_file.is_file():
            raise FileNotFoundError(f"Placement analysis file not found: {placement_file}")
        if not material_file.is_file():
            raise FileNotFoundError(f"Material config file not found: {material_file}")
        if retry < 0:
            raise ValueError("--retry must be greater than or equal to 0.")

        storyboard = StoryboardReport.model_validate_json(storyboard_file.read_text(encoding="utf-8"))
        placement_analysis = PlacementAnalysisReport.model_validate_json(
            placement_file.read_text(encoding="utf-8")
        )
        material = load_material_config(material_file)
        material_image_path = material.resolve_image_path(material_file)
        if not material_image_path.is_file():
            raise FileNotFoundError(f"Material image file not found: {material_image_path}")

        source_video = self._resolve_storyboard_source_video_path(
            source_video=storyboard.source_video,
            storyboard_file=storyboard_file,
        )
        if not source_video.is_file():
            raise FileNotFoundError(f"Source video referenced by storyboard not found: {source_video}")

        best_segment = self._find_segment(storyboard, placement_analysis.best_segment_index)
        best_candidate = self._find_candidate(placement_analysis, placement_analysis.best_segment_index)
        thumbnail_path = self._resolve_thumbnail_path(storyboard_file=storyboard_file, segment=best_segment)
        if not thumbnail_path.is_file():
            raise FileNotFoundError(f"Best-segment thumbnail file not found: {thumbnail_path}")

        prompt_model_name = prompt_model or self._settings.default_model
        generation_model_name = generation_model or self._settings.default_video_generation_model
        normalized_duration = self._normalize_requested_duration(duration)

        target_dir = (
            Path(output_dir).expanduser().resolve()
            if output_dir is not None
            else placement_file.parent
        )
        target_dir.mkdir(parents=True, exist_ok=True)

        reference_window_duration = self._resolve_reference_window_duration(
            requested_duration=normalized_duration,
            segment_duration_sec=best_segment.duration_sec,
        )
        reference_start_sec, reference_end_sec = self._select_reference_window(
            segment=best_segment,
            target_duration=reference_window_duration,
        )
        reference_clip_path = self._clipper.render(
            video_path=source_video,
            start_sec=reference_start_sec,
            end_sec=reference_end_sec,
            output_path=target_dir
            / "reference_clips"
            / f"segment-{best_segment.index:04d}.mp4",
        )
        reference_clip_duration_sec = self._clipper.probe_duration(reference_clip_path)
        generation_duration = self._resolve_generation_duration(
            requested_duration=normalized_duration,
            reference_clip_duration_sec=reference_clip_duration_sec,
        )

        logger.info("Loaded best segment %s for compositing.", best_segment.index)
        logger.info("Using prompt model: %s", prompt_model_name)
        logger.info("Using generation model: %s", generation_model_name)
        logger.info("Reference clip window: %.3fs - %.3fs", reference_start_sec, reference_end_sec)
        logger.info("Reference clip duration: %.3fs", reference_clip_duration_sec)

        best_segment_reference = build_best_segment_reference(
            storyboard=storyboard,
            placement_analysis=placement_analysis,
            thumbnail_path=str(thumbnail_path),
            reference_video_path=str(reference_clip_path),
            reference_start_sec=reference_start_sec,
            reference_end_sec=reference_end_sec,
        )

        try:
            resolved_reference_video_url = self._resolve_reference_video_url(
                reference_video_url=reference_video_url,
                reference_clip_path=reference_clip_path,
            )
            resolved_reference_image_url = self._resolve_reference_image_url(material_image_path)

            if not resolved_reference_video_url or not resolved_reference_image_url:
                generation_result = VideoGenerationResult(
                    task_id="pending",
                    status="pending_reference_video_url",
                    video_url=None,
                    last_frame_url=None,
                    file_url=None,
                    error_code="MissingReferenceVideoURL",
                    error_message=(
                        "Compose-best requires a usable reference_video_url. Configure TOS upload "
                        "via TOS_BUCKET, TOS_AK, TOS_SK, TOS_ENDPOINT, and TOS_REGION, or rerun with "
                        "--reference-video-url / DPP_REFERENCE_VIDEO_URL."
                    ),
                )
                return self._write_report(
                    target_dir=target_dir,
                    storyboard_file=storyboard_file,
                    placement_file=placement_file,
                    material=material,
                    material_image_path=material_image_path,
                    prompt_model_name=prompt_model_name,
                    generation_model_name=generation_model_name,
                    best_segment_reference=best_segment_reference,
                    prompt_plan=CompositionPromptDraft(
                        segment_index=best_segment.index,
                        scene_context="待补充",
                        product_feature_specs="待补充",
                        product_integration="待补充",
                        lighting="待补充",
                        motion="待补充",
                        mood="待补充",
                        negative_prompts=["缺少可用的视频参考 URL，尚未生成正式合成提示词"],
                        generation_prompt="待补充",
                    ),
                    generation_result=generation_result,
                )

            response_payload = self._client.create_composition_prompt_response(
                model=prompt_model_name,
                material_image_url=resolved_reference_image_url,
                reference_video_url=resolved_reference_video_url,
                material_text=material.to_prompt_block(),
                segment_block=self._format_segment_block(best_segment),
                candidate_block=self._format_candidate_block(best_candidate, placement_analysis.best_segment_reason),
            )
            raw_text = self._client.extract_text(response_payload)
            prompt_plan = self._validate_or_repair_prompt(
                raw_text=raw_text,
                retry=retry,
                model=prompt_model_name,
            )

            if prompt_only:
                generation_result = VideoGenerationResult(
                    task_id="prompt_only",
                    status="prompt_only",
                    video_url=None,
                    last_frame_url=None,
                    file_url=None,
                    error_code=None,
                    error_message=None,
                )
                return self._write_report(
                    target_dir=target_dir,
                    storyboard_file=storyboard_file,
                    placement_file=placement_file,
                    material=material,
                    material_image_path=material_image_path,
                    prompt_model_name=prompt_model_name,
                    generation_model_name=generation_model_name,
                    best_segment_reference=best_segment_reference,
                    prompt_plan=prompt_plan,
                    generation_result=generation_result,
                )

            task_payload = self._client.create_video_generation_task(
                model=generation_model_name,
                prompt=prompt_plan.generation_prompt,
                reference_image_url=resolved_reference_image_url,
                reference_video_url=resolved_reference_video_url,
                ratio=self._settings.video_generation_ratio,
                duration=generation_duration,
                resolution=self._settings.video_generation_resolution,
                generate_audio=generate_audio,
                watermark=False,
                reference_image_role=self._settings.video_generation_reference_image_role,
                reference_video_role=self._settings.video_generation_reference_video_role,
            )
            task_id = self._client.extract_task_id(task_payload)
            final_task = self._wait_for_generation_task(task_id=task_id)
            generation_status = self._client.extract_task_status(final_task)
            generation_payload = self._client.extract_generation_result(final_task)
            downloaded_video_path = self._download_generated_video(
                video_url=generation_payload["video_url"],
                target_dir=target_dir,
                task_id=task_id,
            )
            generation_result = VideoGenerationResult(
                task_id=task_id,
                status=generation_status,
                video_url=generation_payload["video_url"],
                downloaded_video_path=downloaded_video_path,
                last_frame_url=generation_payload["last_frame_url"],
                file_url=generation_payload["file_url"],
                error_code=generation_payload["error_code"],
                error_message=generation_payload["error_message"],
            )

            return self._write_report(
                target_dir=target_dir,
                storyboard_file=storyboard_file,
                placement_file=placement_file,
                material=material,
                material_image_path=material_image_path,
                prompt_model_name=prompt_model_name,
                generation_model_name=generation_model_name,
                best_segment_reference=best_segment_reference,
                prompt_plan=prompt_plan,
                generation_result=generation_result,
            )
        finally:
            close = getattr(self._client, "close", None)
            if callable(close):
                close()

    def _wait_for_generation_task(self, *, task_id: str) -> object:
        final_statuses = {"succeeded", "failed", "cancelled"}
        deadline = time.monotonic() + self._settings.video_generation_wait_timeout_seconds
        while True:
            task_payload = self._client.get_video_generation_task(task_id=task_id)
            status = self._client.extract_task_status(task_payload)
            if status in final_statuses:
                return task_payload
            if time.monotonic() >= deadline:
                raise RuntimeError(
                    "Timed out while waiting for content generation task to finish. "
                    f"task_id={task_id}"
                )
            self._sleeper(self._settings.video_generation_poll_interval_seconds)

    def _validate_or_repair_prompt(
        self,
        *,
        raw_text: str,
        retry: int,
        model: str,
    ) -> CompositionPromptDraft:
        try:
            return self._build_prompt_plan(raw_text)
        except (JSONDecodeError, ValidationError, ValueError) as initial_error:
            if retry <= 0:
                raise RuntimeError(f"Composition prompt validation failed: {initial_error}") from initial_error

        repaired_payload = self._client.repair_composition_json(model=model, raw_text=raw_text)
        repaired_text = self._client.extract_text(repaired_payload)
        try:
            return self._build_prompt_plan(repaired_text)
        except (JSONDecodeError, ValidationError, ValueError) as repair_error:
            raise RuntimeError(
                "Composition prompt validation failed after one repair attempt. "
                f"Last error: {repair_error}"
            ) from repair_error

    @staticmethod
    def _build_prompt_plan(raw_text: str) -> CompositionPromptDraft:
        payload = extract_json_payload(raw_text)
        if not isinstance(payload, dict):
            raise ValueError("Composition prompt payload must be a JSON object.")
        return CompositionPromptDraft.model_validate(payload)

    @staticmethod
    def _resolve_storyboard_source_video_path(*, source_video: str, storyboard_file: Path) -> Path:
        """Resolve storyboard `source_video` to an absolute local path.

        - If `source_video` is absolute, resolve it as-is.
        - If `source_video` is relative, try in order:
          - relative to the storyboard.json directory (backwards compatible)
          - relative to `DPP_WORKDIR` when set (skill workspace layout)
          - relative to the current working directory (workspace layout when running from repo root)
        - Always expands `~` before resolution.
        """
        raw = (source_video or "").strip()
        if not raw:
            raise ValueError("Storyboard source_video cannot be empty.")

        candidate = Path(raw).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()

        # 1) storyboard.json directory (legacy behavior)
        storyboard_relative = (storyboard_file.parent / candidate).resolve()
        if storyboard_relative.is_file():
            return storyboard_relative

        # 2) workspace directory hinted by the skill scripts
        workdir_raw = (os.getenv("DPP_WORKDIR") or "").strip()
        if workdir_raw:
            workdir_relative = (Path(workdir_raw).expanduser().resolve() / candidate).resolve()
            if workdir_relative.is_file():
                return workdir_relative

        # 3) current working directory (common when running from workspace root)
        cwd_relative = (Path.cwd() / candidate).resolve()
        if cwd_relative.is_file():
            return cwd_relative

        # Fall back to the legacy resolution for a stable error message.
        return storyboard_relative

    @staticmethod
    def _find_segment(storyboard: StoryboardReport, segment_index: int) -> StoryboardSegment:
        for segment in storyboard.segments:
            if segment.index == segment_index:
                return segment
        raise ValueError(f"Segment index not found in storyboard: {segment_index}")

    @staticmethod
    def _find_candidate(
        placement_analysis: PlacementAnalysisReport,
        segment_index: int,
    ) -> PlacementCandidate:
        for candidate in placement_analysis.candidates:
            if candidate.segment_index == segment_index:
                return candidate
        raise ValueError(f"Segment index not found in placement analysis candidates: {segment_index}")

    @staticmethod
    def _resolve_thumbnail_path(*, storyboard_file: Path, segment: StoryboardSegment) -> Path:
        if not segment.thumbnail_path:
            raise ValueError(f"Segment {segment.index} does not include thumbnail_path.")
        thumbnail_path = Path(segment.thumbnail_path)
        if thumbnail_path.is_absolute():
            return thumbnail_path.resolve()
        return (storyboard_file.parent / thumbnail_path).resolve()

    @staticmethod
    def _select_reference_window(
        *,
        segment: StoryboardSegment,
        target_duration: int | None,
    ) -> tuple[float, float]:
        if target_duration is None:
            return (round(segment.start_sec, 3), round(segment.end_sec, 3))
        reference_duration = min(segment.duration_sec, float(target_duration))
        if reference_duration >= segment.duration_sec:
            return (round(segment.start_sec, 3), round(segment.end_sec, 3))
        offset = (segment.duration_sec - reference_duration) / 2
        start_sec = segment.start_sec + offset
        end_sec = start_sec + reference_duration
        return (round(start_sec, 3), round(end_sec, 3))

    @staticmethod
    def _normalize_requested_duration(requested_duration: int | None) -> int | None:
        if requested_duration == -1:
            return -1
        if requested_duration is not None and not 2 <= requested_duration <= 12:
            raise ValueError("--duration must be -1 or between 2 and 12 seconds.")
        return requested_duration

    @staticmethod
    def _normalize_reference_window_duration(requested_duration: int | None) -> int | None:
        # Backwards compatible wrapper used by older tests and code paths.
        if requested_duration == -1:
            return None
        return requested_duration

    @staticmethod
    def _resolve_generation_duration(
        *,
        requested_duration: int | None,
        reference_clip_duration_sec: float,
    ) -> int | None:
        """Resolve the duration passed to Seedance so it matches the reference clip window.

        - `--duration=-1` means "let the model decide" and results in omitting the duration field.
        - Otherwise we pass the actual rendered reference clip duration (integer seconds).
        """
        if requested_duration == -1:
            return None

        duration_int = int(round(reference_clip_duration_sec))
        if not 2 <= duration_int <= 12:
            raise ValueError(
                "Computed generation duration must be between 2 and 12 seconds. "
                "Rerun with --duration (2-12) or --duration -1 to let the model decide."
            )
        return duration_int

    @staticmethod
    def _resolve_reference_window_duration(*, requested_duration: int | None, segment_duration_sec: float) -> int | None:
        """Resolve the target reference window duration.

        - If user specifies `--duration`, use it directly.
        - If `--duration` is omitted, use the best segment duration (rounded to integer seconds).
        - If `--duration=-1`, keep the full segment as the reference window.
        """
        if requested_duration == -1:
            return None
        if requested_duration is not None:
            return requested_duration

        derived = int(round(segment_duration_sec))
        if not 2 <= derived <= 12:
            raise ValueError(
                "Best segment duration is outside Seedance supported range (2-12s). "
                "Pass --duration (2-12) or --duration -1 to let the model decide."
            )
        return derived

    def _resolve_reference_image_url(self, material_image_path: Path) -> str | None:
        try:
            return self._uploader.upload(material_image_path)
        except CDNUploadError:
            return None

    def _download_generated_video(
        self,
        *,
        video_url: str | None,
        target_dir: Path,
        task_id: str,
    ) -> str | None:
        if not video_url:
            return None
        suffix = Path(urlparse(video_url).path).suffix or ".mp4"
        output_path = target_dir / "generated" / f"{task_id}{suffix}"
        try:
            downloaded = self._downloader.download_video(url=video_url, output_path=output_path)
        except Exception as exc:
            logger.warning("Failed to download generated video for task %s: %s", task_id, exc)
            return None
        return str(downloaded.resolve())

    def _resolve_reference_video_url(
        self,
        *,
        reference_video_url: str | None,
        reference_clip_path: Path,
    ) -> str | None:
        if reference_video_url:
            return reference_video_url
        if self._settings.default_reference_video_url:
            return self._settings.default_reference_video_url
        try:
            return self._uploader.upload(reference_clip_path)
        except CDNUploadError:
            return None

    @staticmethod
    def _format_segment_block(segment: StoryboardSegment) -> str:
        return (
            f"segment_index: {segment.index}\n"
            f"start_sec: {segment.start_sec}\n"
            f"end_sec: {segment.end_sec}\n"
            f"duration_sec: {segment.duration_sec}\n"
            f"scene_summary: {segment.scene_summary}\n"
            f"background_summary: {segment.background_summary or '未提供'}\n"
            f"spatial_layout: {segment.spatial_layout or '未提供'}\n"
            f"lighting: {segment.lighting or '未提供'}\n"
            f"placement_space_hint: {segment.placement_space_hint or '未提供'}\n"
            f"camera_motion: {segment.camera_motion}\n"
            f"thumbnail_path: {segment.thumbnail_path or '未提供'}"
        )

    @staticmethod
    def _format_candidate_block(
        candidate: PlacementCandidate,
        best_segment_reason: str,
    ) -> str:
        concerns = "、".join(candidate.concerns) if candidate.concerns else "无明显风险"
        return (
            f"best_segment_reason: {best_segment_reason}\n"
            f"suitability_score: {candidate.suitability_score}\n"
            f"decision: {candidate.decision}\n"
            f"rationale: {candidate.rationale}\n"
            f"suggested_placement: {candidate.suggested_placement}\n"
            f"concerns: {concerns}"
        )

    @staticmethod
    def _write_report(
        *,
        target_dir: Path,
        storyboard_file: Path,
        placement_file: Path,
        material,
        material_image_path: Path,
        prompt_model_name: str,
        generation_model_name: str,
        best_segment_reference,
        prompt_plan: CompositionPromptDraft,
        generation_result: VideoGenerationResult,
    ) -> Path:
        report = build_composition_result_report(
            storyboard_path=str(storyboard_file),
            placement_analysis_path=str(placement_file),
            material=material,
            material_image_path=str(material_image_path),
            prompt_model=prompt_model_name,
            generation_model=generation_model_name,
            best_segment=best_segment_reference,
            prompt_plan=prompt_plan,
            generation=generation_result,
        )
        target_path = target_dir / "composition_result.json"
        target_path.write_text(
            json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        logger.info("Best-segment composition output saved to %s", target_path)
        return target_path
