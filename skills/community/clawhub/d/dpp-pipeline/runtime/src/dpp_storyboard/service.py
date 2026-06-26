from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .ark_client import ArkClient
from .config import Settings
from .prompt import build_storyboard_user_prompt
from .schema import StoryboardDraft, StoryboardReport, build_storyboard_report
from .thumbnailer import FFmpegThumbnailService

logger = logging.getLogger(__name__)


class StoryboardService:
    def __init__(
        self,
        settings: Settings,
        client: ArkClient | None = None,
        thumbnailer: FFmpegThumbnailService | None = None,
    ) -> None:
        self._settings = settings
        self._client = client or ArkClient(settings)
        self._thumbnailer = thumbnailer or FFmpegThumbnailService()

    def run(
        self,
        *,
        video_path: str | Path,
        output_dir: str | Path,
        model: str | None = None,
        file_id: str | None = None,
        retry: int = 1,
    ) -> Path:
        # Preserve the original user input (absolute or relative) in storyboard.json,
        # while still resolving to an absolute path for local file IO.
        video_source = str(video_path).strip()
        if not video_source:
            raise ValueError("video_path cannot be empty.")

        video = Path(video_source).expanduser().resolve()
        if not video.is_file():
            raise FileNotFoundError(f"Video file not found: {video}")
        if video.suffix.lower() not in {".mp4", ".mov"}:
            raise ValueError("Only .mp4 and .mov files are supported in v1.")
        if retry < 0:
            raise ValueError("--retry must be greater than or equal to 0.")

        resolved_model = model or self._settings.default_model
        logger.info("Using video: %s", video)
        logger.info("Output root: %s", Path(output_dir).expanduser().resolve())
        logger.info("Using model: %s", resolved_model)
        try:
            resolved_file_id = file_id.strip() if isinstance(file_id, str) else ""
            if resolved_file_id:
                logger.info("Using existing Ark file id: %s", resolved_file_id)
            else:
                uploaded = self._client.upload_file(video)
                resolved_file_id = self._client.extract_file_id(uploaded)
                logger.info("Uploaded file is ready for inference.")
            response_payload = self._client.create_storyboard_response(
                model=resolved_model,
                file_id=resolved_file_id,
                user_prompt=build_storyboard_user_prompt(),
            )
            raw_text = self._client.extract_text(response_payload)
            logger.info("Received storyboard response from Ark.")
            report = self._validate_or_repair(
                raw_text=raw_text,
                source_video=video_source,
                model=resolved_model,
                retry=retry,
            )

            target_dir = Path(output_dir).expanduser().resolve() / video.stem
            target_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Generating %s thumbnails.", len(report.segments))
            report = self._thumbnailer.render(
                video_path=video,
                report=report,
                thumbnails_dir=target_dir / "thumbnails",
            )
            target_path = target_dir / "storyboard.json"
            logger.info("Writing storyboard output to %s", target_path)
            target_path.write_text(
                json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            logger.info("Storyboard output saved.")
            return target_path
        finally:
            close = getattr(self._client, "close", None)
            if callable(close):
                close()

    def _validate_or_repair(
        self,
        *,
        raw_text: str,
        source_video: str,
        model: str,
        retry: int,
    ) -> StoryboardReport:
        try:
            logger.info("Validating storyboard payload.")
            return self._build_report(raw_text=raw_text, source_video=source_video, model=model)
        except (JSONDecodeError, ValidationError, ValueError) as initial_error:
            if retry <= 0:
                raise RuntimeError(f"Storyboard validation failed: {initial_error}") from initial_error

        logger.info("Validation failed, attempting JSON repair.")
        repaired_payload = self._client.repair_storyboard_json(model=model, raw_text=raw_text)
        repaired_text = self._client.extract_text(repaired_payload)
        try:
            logger.info("Validating repaired storyboard payload.")
            return self._build_report(
                raw_text=repaired_text,
                source_video=source_video,
                model=model,
            )
        except (JSONDecodeError, ValidationError, ValueError) as repair_error:
            raise RuntimeError(
                "Storyboard validation failed after one repair attempt. "
                f"Last error: {repair_error}"
            ) from repair_error

    def _build_report(self, *, raw_text: str, source_video: str, model: str) -> StoryboardReport:
        payload = extract_json_payload(raw_text)
        if isinstance(payload, list):
            payload = {"language": "zh-CN", "segments": payload}
        if not isinstance(payload, dict):
            raise ValueError("Storyboard payload must be a JSON object or a list of segments.")
        draft = StoryboardDraft.model_validate(payload)
        return build_storyboard_report(
            source_video=source_video,
            model=model,
            draft=draft,
        )


def extract_json_payload(raw_text: str) -> Any:
    normalized = _strip_code_fences(raw_text).strip()
    if not normalized:
        raise JSONDecodeError("Empty model output.", raw_text, 0)

    try:
        return json.loads(normalized)
    except JSONDecodeError:
        decoder = json.JSONDecoder()
        for start_char in ("{", "["):
            start_index = normalized.find(start_char)
            while start_index != -1:
                try:
                    payload, _ = decoder.raw_decode(normalized[start_index:])
                    return payload
                except JSONDecodeError:
                    start_index = normalized.find(start_char, start_index + 1)
        raise


def _strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if not lines:
        return stripped

    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)
