from __future__ import annotations

import concurrent.futures
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Callable

import volcenginesdkarkruntime as ark

from .config import Settings
from .prompt import (
    COMPOSITION_PROMPT_INSTRUCTIONS,
    MATERIAL_CONFIG_INSTRUCTIONS,
    PLACEMENT_ANALYSIS_INSTRUCTIONS,
    STORYBOARD_INSTRUCTIONS,
    build_composition_json_repair_prompt,
    build_composition_prompt_request,
    build_json_repair_prompt,
    build_material_config_prompt,
    build_material_json_repair_prompt,
    build_placement_analysis_prompt,
    build_placement_json_repair_prompt,
)

logger = logging.getLogger(__name__)
responses_logger = logging.getLogger("dpp.responses")


def configure_response_logging(log_dir: str | Path = "log") -> Path:
    """配置 Responses API 入参与出参的文件日志。"""
    resolved_log_dir = Path(log_dir).expanduser().resolve()
    resolved_log_dir.mkdir(parents=True, exist_ok=True)
    log_path = resolved_log_dir / "ark_responses.log"
    responses_logger.handlers.clear()
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    responses_logger.addHandler(file_handler)
    responses_logger.setLevel(logging.INFO)
    responses_logger.propagate = False
    return log_path


class ArkAPIError(RuntimeError):
    """Raised when Ark returns a non-success response."""


def _stdout_progress_reporter(event: dict[str, Any]) -> None:
    """Emit Ark request lifecycle updates to CLI stdout."""
    print(json.dumps(event, ensure_ascii=False), flush=True)


class ArkClient:
    def __init__(
        self,
        settings: Settings,
        *,
        progress_reporter: Callable[[dict[str, Any]], None] | None = None,
        response_wait_heartbeat_seconds: float = 2.0,
    ) -> None:
        self._settings = settings
        self._client = ark.Ark(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout_seconds,
        )
        self._progress_reporter = progress_reporter or _stdout_progress_reporter
        self._response_wait_heartbeat_seconds = response_wait_heartbeat_seconds

    def upload_file(self, file_path: Path) -> Any:
        try:
            logger.info("Uploading file to Ark: %s", file_path.name)
            uploaded = self._client.files.create(
                file=file_path,
                purpose=self._settings.file_purpose,
            )
            logger.info("Waiting for Ark to process uploaded file.")
            processed = self._client.files.wait_for_processing(id=uploaded.id)
        except Exception as exc:
            raise ArkAPIError(f"Ark file upload failed: {exc}") from exc

        status = getattr(processed, "status", None)
        if status != "active":
            error = getattr(processed, "error", None)
            raise ArkAPIError(
                f"Ark file processing did not become active. status={status!r}, error={error!r}"
            )
        return processed

    def create_storyboard_response(
        self,
        *,
        model: str,
        file_id: str,
        user_prompt: str,
    ) -> Any:
        request_payload = {
            "model": model,
            "instructions": STORYBOARD_INSTRUCTIONS,
            "temperature": 0.2,
            "text": {"format": {"type": "json_object"}},
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_prompt},
                        {"type": self._settings.input_file_type, "file_id": file_id},
                    ],
                }
            ],
        }
        try:
            logger.info("Requesting storyboard generation from Ark.")
            return self._create_response(operation="storyboard_generation", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark storyboard generation failed: {exc}") from exc

    def repair_storyboard_json(self, *, model: str, raw_text: str) -> Any:
        request_payload = {
            "model": model,
            "text": {"format": {"type": "json_object"}},
            "input": build_json_repair_prompt(raw_text),
        }
        try:
            logger.info("Requesting Ark to repair invalid JSON output.")
            return self._create_response(operation="storyboard_json_repair", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark JSON repair failed: {exc}") from exc

    def create_placement_analysis_response(
        self,
        *,
        model: str,
        material_image_file_id: str,
        material_text: str,
        segment_blocks: list[str],
    ) -> Any:
        request_payload = {
            "model": model,
            "instructions": PLACEMENT_ANALYSIS_INSTRUCTIONS,
            "text": {"format": {"type": "json_object"}},
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": build_placement_analysis_prompt(
                                material_text=material_text,
                                segment_blocks=segment_blocks,
                            ),
                        },
                        {
                            "type": "input_image",
                            "detail": "high",
                            "file_id": material_image_file_id,
                        },
                    ],
                }
            ],
        }
        try:
            logger.info("Requesting placement analysis from Ark.")
            return self._create_response(operation="placement_analysis", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark placement analysis failed: {exc}") from exc

    def repair_placement_json(self, *, model: str, raw_text: str) -> Any:
        request_payload = {
            "model": model,
            "text": {"format": {"type": "json_object"}},
            "input": build_placement_json_repair_prompt(raw_text),
        }
        try:
            logger.info("Requesting Ark to repair invalid placement JSON output.")
            return self._create_response(operation="placement_json_repair", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark placement JSON repair failed: {exc}") from exc

    def create_composition_prompt_response(
        self,
        *,
        model: str,
        material_image_url: str,
        reference_video_url: str,
        material_text: str,
        segment_block: str,
        candidate_block: str,
    ) -> Any:
        request_payload = {
            "model": model,
            "instructions": COMPOSITION_PROMPT_INSTRUCTIONS,
            "text": {"format": {"type": "json_object"}},
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": build_composition_prompt_request(
                                material_text=material_text,
                                segment_block=segment_block,
                                candidate_block=candidate_block,
                            ),
                        },
                        {
                            "type": "input_image",
                            "detail": "high",
                            "image_url": material_image_url,
                        },
                        {
                            "type": self._settings.input_file_type,
                            "video_url": reference_video_url,
                        },
                    ],
                }
            ],
        }
        try:
            logger.info("Requesting composition prompt generation from Ark.")
            return self._create_response(operation="composition_prompt_generation", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark composition prompt generation failed: {exc}") from exc

    def repair_composition_json(self, *, model: str, raw_text: str) -> Any:
        request_payload = {
            "model": model,
            "text": {"format": {"type": "json_object"}},
            "input": build_composition_json_repair_prompt(raw_text),
        }
        try:
            logger.info("Requesting Ark to repair invalid composition JSON output.")
            return self._create_response(operation="composition_json_repair", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark composition JSON repair failed: {exc}") from exc

    def create_material_config_response(
        self,
        *,
        model: str,
        product_image_file_id: str,
        image_path: str,
        brand: str | None = None,
        product_name: str | None = None,
    ) -> Any:
        """Generate a single-product material config JSON from a product image."""
        request_payload = {
            "model": model,
            "instructions": MATERIAL_CONFIG_INSTRUCTIONS,
            "text": {"format": {"type": "json_object"}},
            "temperature": 0.2,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": build_material_config_prompt(
                                image_path=image_path,
                                brand=brand,
                                product_name=product_name,
                            ),
                        },
                        {
                            "type": "input_image",
                            "detail": "high",
                            "file_id": product_image_file_id,
                        },
                    ],
                }
            ],
        }
        try:
            logger.info("Requesting material config generation from Ark.")
            return self._create_response(operation="material_config_generation", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark material config generation failed: {exc}") from exc

    def repair_material_config_json(self, *, model: str, raw_text: str, image_path: str) -> Any:
        """Repair invalid material config JSON output."""
        request_payload = {
            "model": model,
            "text": {"format": {"type": "json_object"}},
            "input": build_material_json_repair_prompt(raw_text, image_path=image_path),
        }
        try:
            logger.info("Requesting Ark to repair invalid material config JSON output.")
            return self._create_response(operation="material_config_json_repair", request_payload=request_payload)
        except Exception as exc:
            raise ArkAPIError(f"Ark material config JSON repair failed: {exc}") from exc

    def create_video_generation_task(
        self,
        *,
        model: str,
        prompt: str,
        reference_image_url: str,
        reference_video_url: str,
        ratio: str,
        duration: int | None,
        resolution: str,
        generate_audio: bool,
        watermark: bool,
        reference_image_role: str,
        reference_video_role: str,
    ) -> Any:
        request_payload = {
            "model": model,
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "role": reference_image_role,
                    "image_url": {"url": reference_image_url},
                },
                {
                    "type": "video_url",
                    "role": reference_video_role,
                    "video_url": {"url": reference_video_url},
                },
            ],
            "generate_audio": generate_audio,
            "ratio": ratio,
            "resolution": resolution,
            "watermark": watermark,
        }
        if duration is not None:
            request_payload["duration"] = duration
        self._log_api_event(
            phase="request",
            operation="content_generation_create_task",
            endpoint="/contents/generations/tasks",
            payload=request_payload,
        )
        try:
            response = self._client.content_generation.tasks.create(**request_payload)
        except Exception as exc:
            self._log_api_event(
                phase="error",
                operation="content_generation_create_task",
                endpoint="/contents/generations/tasks",
                payload={
                    "request": request_payload,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise ArkAPIError(f"Ark content generation task creation failed: {exc}") from exc
        self._log_api_event(
            phase="response",
            operation="content_generation_create_task",
            endpoint="/contents/generations/tasks",
            payload=response,
        )
        return response

    def get_video_generation_task(self, *, task_id: str) -> Any:
        endpoint = f"/contents/generations/tasks/{task_id}"
        self._log_api_event(
            phase="request",
            operation="content_generation_get_task",
            endpoint=endpoint,
            payload={"task_id": task_id},
        )
        try:
            response = self._client.content_generation.tasks.get(task_id=task_id)
        except Exception as exc:
            self._log_api_event(
                phase="error",
                operation="content_generation_get_task",
                endpoint=endpoint,
                payload={"task_id": task_id, "error_type": type(exc).__name__, "error_message": str(exc)},
            )
            raise ArkAPIError(f"Ark content generation task retrieval failed: {exc}") from exc
        self._log_api_event(
            phase="response",
            operation="content_generation_get_task",
            endpoint=endpoint,
            payload=response,
        )
        return response

    def _create_response(self, *, operation: str, request_payload: dict[str, Any]) -> Any:
        """调用 Responses API 并记录请求与响应日志。"""
        request_run_id = f"{operation}-{uuid.uuid4().hex[:8]}"
        self._log_api_event(
            phase="request",
            operation=operation,
            endpoint="/responses",
            payload=request_payload,
            request_run_id=request_run_id,
        )
        start_time = time.monotonic()
        self._emit_progress(
            {
                "type": "ark_status",
                "request_run_id": request_run_id,
                "operation": operation,
                "state": "request_sent",
            }
        )
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._client.responses.create, **request_payload)
                while True:
                    try:
                        response = future.result(timeout=self._response_wait_heartbeat_seconds)
                        break
                    except concurrent.futures.TimeoutError:
                        self._emit_progress(
                            {
                                "type": "ark_status",
                                "request_run_id": request_run_id,
                                "operation": operation,
                                "state": "waiting",
                                "elapsed_sec": round(time.monotonic() - start_time, 1),
                            }
                        )
        except Exception as exc:
            self._log_api_event(
                phase="error",
                operation=operation,
                endpoint="/responses",
                payload={
                    "request": request_payload,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
                request_run_id=request_run_id,
            )
            self._emit_progress(
                {
                    "type": "ark_status",
                    "request_run_id": request_run_id,
                    "operation": operation,
                    "state": "response_failed",
                    "elapsed_sec": round(time.monotonic() - start_time, 1),
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
            )
            raise
        self._log_api_event(
            phase="response",
            operation=operation,
            endpoint="/responses",
            payload=response,
            request_run_id=request_run_id,
        )
        self._emit_progress(
            {
                "type": "ark_status",
                "request_run_id": request_run_id,
                "operation": operation,
                "state": "response_finished",
                "elapsed_sec": round(time.monotonic() - start_time, 1),
                "response_id": self._extract_response_id(response),
            }
        )
        return response

    @staticmethod
    def _log_api_event(
        *,
        phase: str,
        operation: str,
        endpoint: str,
        payload: Any,
        request_run_id: str | None = None,
    ) -> None:
        """将 Ark API 的请求或响应写入文件日志。"""
        record = {
            "phase": phase,
            "endpoint": endpoint,
            "operation": operation,
            "payload": _serialize_for_log(payload),
        }
        if request_run_id:
            record["request_run_id"] = request_run_id
        responses_logger.info(json.dumps(record, ensure_ascii=False))

    def _emit_progress(self, event: dict[str, Any]) -> None:
        """Emit best-effort CLI progress without breaking the request flow."""
        try:
            self._progress_reporter(event)
        except Exception:  # pragma: no cover - progress reporting must not break API requests
            logger.debug("Ignoring progress reporter failure.", exc_info=True)

    @staticmethod
    def _extract_response_id(payload: Any) -> str | None:
        if isinstance(payload, dict):
            value = payload.get("id")
            return str(value) if value else None
        value = getattr(payload, "id", None)
        return str(value) if value else None

    @staticmethod
    def extract_file_id(payload: Any) -> str:
        candidates = [
            getattr(payload, "id", None),
            getattr(payload, "file_id", None),
        ]
        if isinstance(payload, dict):
            candidates.extend(
                [
                    payload.get("id"),
                    payload.get("file_id"),
                    payload.get("data", {}).get("id")
                    if isinstance(payload.get("data"), dict)
                    else None,
                ]
            )
        for candidate in candidates:
            if isinstance(candidate, str) and candidate.strip():
                return candidate
        raise ArkAPIError(f"Ark file upload response did not include a file id: {payload}")

    @staticmethod
    def extract_text(payload: Any) -> str:
        direct_text = getattr(payload, "output_text", None)
        if isinstance(direct_text, str) and direct_text.strip():
            return direct_text.strip()
        if isinstance(payload, dict):
            output_text = payload.get("output_text")
            if isinstance(output_text, str) and output_text.strip():
                return output_text.strip()

        texts: list[str] = []

        output = getattr(payload, "output", None)
        if output is None and isinstance(payload, dict):
            output = payload.get("output")
        if isinstance(output, list):
            for item in output:
                texts.extend(_extract_texts_from_item(item))

        choices = payload.get("choices") if isinstance(payload, dict) else None
        if isinstance(choices, list):
            for choice in choices:
                if not isinstance(choice, dict):
                    continue
                message = choice.get("message")
                if message is not None:
                    texts.extend(_extract_texts_from_item(message))

        merged = "\n".join(part.strip() for part in texts if part.strip()).strip()
        if merged:
            return merged

        raise ArkAPIError(f"Ark response did not contain readable text output: {payload}")

    @staticmethod
    def extract_task_id(payload: Any) -> str:
        candidates = [getattr(payload, "id", None)]
        if isinstance(payload, dict):
            candidates.append(payload.get("id"))
        for candidate in candidates:
            if isinstance(candidate, str) and candidate.strip():
                return candidate
        raise ArkAPIError(f"Ark content generation task response did not include a task id: {payload}")

    @staticmethod
    def extract_task_status(payload: Any) -> str:
        candidates = [getattr(payload, "status", None)]
        if isinstance(payload, dict):
            candidates.append(payload.get("status"))
        for candidate in candidates:
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        raise ArkAPIError(f"Ark content generation task did not include a status: {payload}")

    @staticmethod
    def extract_generation_result(payload: Any) -> dict[str, str | None]:
        content = getattr(payload, "content", None)
        error = getattr(payload, "error", None)
        if isinstance(payload, dict):
            content = payload.get("content", content)
            error = payload.get("error", error)

        def _extract_nested(source: Any, name: str) -> str | None:
            if source is None:
                return None
            value = getattr(source, name, None)
            if value is None and isinstance(source, dict):
                value = source.get(name)
            if isinstance(value, str) and value.strip():
                return value.strip()
            return None

        return {
            "video_url": _extract_nested(content, "video_url"),
            "last_frame_url": _extract_nested(content, "last_frame_url"),
            "file_url": _extract_nested(content, "file_url"),
            "error_code": _extract_nested(error, "code"),
            "error_message": _extract_nested(error, "message"),
        }

    def close(self) -> None:
        self._client.close()


def _extract_texts_from_item(item: Any) -> list[str]:
    if item is None:
        return []

    item_type = getattr(item, "type", None)
    if item_type is None and isinstance(item, dict):
        item_type = item.get("type")

    item_text = getattr(item, "text", None)
    if item_text is None and isinstance(item, dict):
        item_text = item.get("text")

    texts: list[str] = []
    if item_type in {"output_text", "text"} and isinstance(item_text, str) and item_text.strip():
        texts.append(item_text)

    content = getattr(item, "content", None)
    if content is None and isinstance(item, dict):
        content = item.get("content")

    if isinstance(content, str) and content.strip():
        texts.append(content)
    elif isinstance(content, list):
        for block in content:
            texts.extend(_extract_texts_from_item(block))

    return texts


def _serialize_for_log(value: Any) -> Any:
    """将任意响应对象转换为可写入 JSON 日志的结构。"""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _serialize_for_log(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_for_log(item) for item in value]
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return _serialize_for_log(model_dump(mode="json"))
        except TypeError:
            return _serialize_for_log(model_dump())
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return _serialize_for_log(to_dict())
    if hasattr(value, "__dict__"):
        return {
            key: _serialize_for_log(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return repr(value)
