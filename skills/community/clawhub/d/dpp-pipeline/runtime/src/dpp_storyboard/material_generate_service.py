from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError

from .ark_client import ArkClient
from .config import Settings
from .material import MaterialConfig
from .service import extract_json_payload

logger = logging.getLogger(__name__)


class MaterialGenerationService:
    """Generate a single-product material config JSON from a product image via Ark."""

    def __init__(self, settings: Settings, client: ArkClient | None = None) -> None:
        self._settings = settings
        self._client = client or ArkClient(settings)

    def run(
        self,
        *,
        product_image_path: str | Path,
        image_path_for_config: str,
        output_path: str | Path,
        model: str | None = None,
        brand: str | None = None,
        product_name: str | None = None,
        retry: int = 1,
    ) -> Path:
        """Generate and write a material config JSON file.

        Args:
            product_image_path: Local path to the product image file to upload.
            image_path_for_config: The exact `image_path` string to write into the JSON config.
            output_path: Target JSON path to write (will be overwritten).
            model: Optional model/endpoint override.
            brand: Optional brand hint (LLM may infer if omitted).
            product_name: Optional product name hint (LLM may infer if omitted).
            retry: Number of repair retries after validation failure (>= 0).
        """
        if retry < 0:
            raise ValueError("--retry must be greater than or equal to 0.")

        image_file = Path(product_image_path).expanduser().resolve()
        if not image_file.is_file():
            raise FileNotFoundError(f"Product image file not found: {image_file}")

        resolved_model = model or self._settings.default_model
        target_path = Path(output_path).expanduser().resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            uploaded = self._client.upload_file(image_file)
            file_id = self._client.extract_file_id(uploaded)
            response_payload = self._client.create_material_config_response(
                model=resolved_model,
                product_image_file_id=file_id,
                image_path=image_path_for_config,
                brand=brand,
                product_name=product_name,
            )
            raw_text = self._client.extract_text(response_payload)
            material = self._validate_or_repair(
                raw_text=raw_text,
                retry=retry,
                model=resolved_model,
                image_path=image_path_for_config,
            )
            payload = material.model_dump(mode="json")
            target_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            logger.info("Material config written to %s", target_path)
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
        image_path: str,
    ) -> MaterialConfig:
        """Validate LLM output against MaterialConfig and optionally repair."""
        try:
            return self._build_material(raw_text=raw_text)
        except (JSONDecodeError, ValidationError, ValueError, TypeError) as initial_error:
            if retry <= 0:
                raise RuntimeError(f"Material config validation failed: {initial_error}") from initial_error

        logger.info("Validation failed, attempting JSON repair.")
        repaired_payload = self._client.repair_material_config_json(
            model=model,
            raw_text=raw_text,
            image_path=image_path,
        )
        repaired_text = self._client.extract_text(repaired_payload)
        try:
            return self._build_material(raw_text=repaired_text)
        except (JSONDecodeError, ValidationError, ValueError, TypeError) as repair_error:
            raise RuntimeError(
                "Material config validation failed after one repair attempt. "
                f"Last error: {repair_error}"
            ) from repair_error

    @staticmethod
    def _build_material(*, raw_text: str) -> MaterialConfig:
        """Parse and validate raw model output into a MaterialConfig."""
        payload = extract_json_payload(raw_text)
        if not isinstance(payload, dict):
            raise ValueError("Material config payload must be a JSON object.")
        return MaterialConfig.model_validate(payload)

