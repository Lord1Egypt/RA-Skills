from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError

from .ark_client import ArkClient
from .config import Settings
from .material import load_material_config
from .placement_schema import (
    PlacementAnalysisDraft,
    PlacementAssessmentDraft,
    build_placement_candidates,
    build_placement_analysis_report,
)
from .schema import StoryboardReport
from .service import extract_json_payload

logger = logging.getLogger(__name__)


class PlacementAnalysisService:
    def __init__(self, settings: Settings, client: ArkClient | None = None) -> None:
        self._settings = settings
        self._client = client or ArkClient(settings)

    def run(
        self,
        *,
        storyboard_path: str | Path,
        material_config_path: str | Path,
        output_dir: str | Path | None = None,
        model: str | None = None,
        retry: int = 1,
    ) -> Path:
        storyboard_file = Path(storyboard_path).expanduser().resolve()
        if not storyboard_file.is_file():
            raise FileNotFoundError(f"Storyboard file not found: {storyboard_file}")
        material_file = Path(material_config_path).expanduser().resolve()
        if not material_file.is_file():
            raise FileNotFoundError(f"Material config file not found: {material_file}")
        if retry < 0:
            raise ValueError("--retry must be greater than or equal to 0.")

        storyboard = StoryboardReport.model_validate_json(
            storyboard_file.read_text(encoding="utf-8")
        )
        material = load_material_config(material_file)
        material_image_path = material.resolve_image_path(material_file)
        if not material_image_path.is_file():
            raise FileNotFoundError(f"Material image file not found: {material_image_path}")

        resolved_model = model or self._settings.default_model
        logger.info("Loaded storyboard: %s", storyboard_file)
        logger.info("Loaded material config: %s", material_file)
        logger.info("Using model: %s", resolved_model)

        try:
            material_upload = self._client.upload_file(material_image_path)
            material_file_id = self._client.extract_file_id(material_upload)
            logger.info("Uploaded material image to Ark.")

            logger.info("Analyzing placement suitability for all segments in one request.")
            response_payload = self._client.create_placement_analysis_response(
                model=resolved_model,
                material_image_file_id=material_file_id,
                material_text=material.to_prompt_block(),
                segment_blocks=[self._format_segment_block(segment) for segment in storyboard.segments],
            )
            raw_text = self._client.extract_text(response_payload)
            analysis = self._validate_or_repair(
                raw_text=raw_text,
                retry=retry,
                model=resolved_model,
            )

            candidates = build_placement_candidates(
                storyboard=storyboard,
                assessments=analysis.assessments,
            )
            report = build_placement_analysis_report(
                storyboard_path=str(storyboard_file),
                material=material,
                material_image_path=str(material_image_path),
                model=resolved_model,
                candidates=candidates,
                best_segment_index=analysis.best_segment_index,
                best_segment_reason=analysis.best_segment_reason,
            )
            target_dir = (
                Path(output_dir).expanduser().resolve()
                if output_dir is not None
                else storyboard_file.parent
            )
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / "placement_analysis.json"
            target_path.write_text(
                json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            logger.info("Placement analysis output saved to %s", target_path)
            return target_path
        finally:
            close = getattr(self._client, "close", None)
            if callable(close):
                close()

    def _validate_or_repair(
        self,
        *,
        raw_text: str,
        retry: int,
        model: str,
    ) -> PlacementAnalysisDraft:
        try:
            return self._build_analysis(raw_text)
        except (JSONDecodeError, ValidationError, ValueError) as initial_error:
            if retry <= 0:
                raise RuntimeError(f"Placement validation failed: {initial_error}") from initial_error

        repaired_payload = self._client.repair_placement_json(model=model, raw_text=raw_text)
        repaired_text = self._client.extract_text(repaired_payload)
        try:
            return self._build_analysis(repaired_text)
        except (JSONDecodeError, ValidationError, ValueError) as repair_error:
            raise RuntimeError(
                "Placement validation failed after one repair attempt. "
                f"Last error: {repair_error}"
            ) from repair_error

    @staticmethod
    def _build_analysis(raw_text: str) -> PlacementAnalysisDraft:
        payload = extract_json_payload(raw_text)
        if not isinstance(payload, dict):
            raise ValueError("Placement analysis payload must be a JSON object.")
        return PlacementAnalysisDraft.model_validate(payload)

    @staticmethod
    def _format_segment_block(segment) -> str:
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
            f"characters: {'、'.join(segment.characters) if segment.characters else '无'}\n"
            f"actions: {'、'.join(segment.actions) if segment.actions else '无'}\n"
            f"camera_motion: {segment.camera_motion}"
        )
