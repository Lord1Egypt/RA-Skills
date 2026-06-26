from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(ValueError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    api_key: str
    base_url: str
    default_model: str
    default_video_generation_model: str
    default_reference_video_url: str | None
    default_video_path: str
    default_file_id: str | None
    timeout_seconds: float
    file_purpose: str
    input_file_type: str
    video_generation_duration_seconds: int
    video_generation_ratio: str
    video_generation_resolution: str
    video_generation_poll_interval_seconds: float
    video_generation_wait_timeout_seconds: float
    video_generation_reference_video_role: str
    video_generation_reference_image_role: str
    tos_bucket: str | None = None
    tos_access_key: str | None = None
    tos_secret_key: str | None = None
    tos_endpoint: str | None = None
    tos_region: str | None = None
    tos_object_prefix: str = "demo/dpp"
    tos_enable_https: bool = True
    tos_force_endpoint: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv(dotenv_path=os.getenv("DPP_DOTENV_PATH"))

        api_key = os.getenv("ARK_API_KEY", "").strip()
        if not api_key:
            raise ConfigError("ARK_API_KEY is required.")

        base_url = os.getenv(
            "ARK_BASE_URL",
            "https://ark.cn-beijing.volces.com/api/v3",
        ).strip()
        if not base_url:
            raise ConfigError("ARK_BASE_URL cannot be empty.")

        default_model = os.getenv(
            "DOUBAO_SEED_ENDPOINT_ID",
            "doubao-seed-2-0-pro-260215",
        ).strip()
        if not default_model:
            raise ConfigError("DOUBAO_SEED_ENDPOINT_ID cannot be empty.")

        default_video_generation_model = os.getenv(
            "DPP_VIDEO_GENERATION_MODEL",
            "doubao-seedance-2-0-260128",
        ).strip()
        if not default_video_generation_model:
            raise ConfigError("DPP_VIDEO_GENERATION_MODEL cannot be empty.")

        default_reference_video_url = os.getenv("DPP_REFERENCE_VIDEO_URL", "").strip() or None

        default_video_path = os.getenv(
            "DPP_DEFAULT_VIDEO_PATH",
            "video/demo.mp4",
        ).strip()
        if not default_video_path:
            raise ConfigError("DPP_DEFAULT_VIDEO_PATH cannot be empty.")

        default_file_id = os.getenv("ARK_FILE_ID", "").strip() or None

        timeout_raw = os.getenv("ARK_TIMEOUT_SECONDS", "120").strip()
        try:
            timeout_seconds = float(timeout_raw)
        except ValueError as exc:
            raise ConfigError("ARK_TIMEOUT_SECONDS must be a number.") from exc
        if timeout_seconds <= 0:
            raise ConfigError("ARK_TIMEOUT_SECONDS must be greater than 0.")

        file_purpose = os.getenv("ARK_FILE_PURPOSE", "user_data").strip() or "user_data"
        input_file_type = os.getenv("ARK_INPUT_FILE_TYPE", "input_video").strip() or "input_video"

        generation_duration_raw = os.getenv("DPP_VIDEO_DURATION_SECONDS", "5").strip()
        try:
            video_generation_duration_seconds = int(generation_duration_raw)
        except ValueError as exc:
            raise ConfigError("DPP_VIDEO_DURATION_SECONDS must be an integer.") from exc
        if not 2 <= video_generation_duration_seconds <= 12:
            raise ConfigError("DPP_VIDEO_DURATION_SECONDS must be between 2 and 12.")

        video_generation_ratio = os.getenv("DPP_VIDEO_RATIO", "adaptive").strip() or "adaptive"
        video_generation_resolution = os.getenv("DPP_VIDEO_RESOLUTION", "720p").strip() or "720p"

        generation_poll_interval_raw = os.getenv("DPP_VIDEO_POLL_INTERVAL_SECONDS", "5").strip()
        try:
            video_generation_poll_interval_seconds = float(generation_poll_interval_raw)
        except ValueError as exc:
            raise ConfigError("DPP_VIDEO_POLL_INTERVAL_SECONDS must be a number.") from exc
        if video_generation_poll_interval_seconds <= 0:
            raise ConfigError("DPP_VIDEO_POLL_INTERVAL_SECONDS must be greater than 0.")

        generation_wait_timeout_raw = os.getenv("DPP_VIDEO_WAIT_TIMEOUT_SECONDS", "900").strip()
        try:
            video_generation_wait_timeout_seconds = float(generation_wait_timeout_raw)
        except ValueError as exc:
            raise ConfigError("DPP_VIDEO_WAIT_TIMEOUT_SECONDS must be a number.") from exc
        if video_generation_wait_timeout_seconds <= 0:
            raise ConfigError("DPP_VIDEO_WAIT_TIMEOUT_SECONDS must be greater than 0.")

        video_generation_reference_video_role = (
            os.getenv("DPP_VIDEO_REFERENCE_VIDEO_ROLE", "reference_video").strip()
            or "reference_video"
        )
        video_generation_reference_image_role = (
            os.getenv("DPP_VIDEO_REFERENCE_IMAGE_ROLE", "reference_image").strip()
            or "reference_image"
        )
        tos_bucket = os.getenv("TOS_BUCKET", "dpp").strip() or None
        tos_access_key = os.getenv("TOS_AK", "").strip() or None
        tos_secret_key = os.getenv("TOS_SK", "").strip() or None
        tos_endpoint = os.getenv("TOS_ENDPOINT", "tos-cn-beijing.volces.com").strip() or None
        tos_region = os.getenv("TOS_REGION", "cn-beijing").strip() or None
        tos_object_prefix = os.getenv("TOS_OBJECT_PREFIX", "demo/dpp").strip()
        tos_object_prefix = tos_object_prefix.strip("/") or "demo/dpp"
        tos_enable_https = os.getenv("TOS_ENABLE_HTTPS", "true").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        tos_force_endpoint = os.getenv("TOS_FORCE_ENDPOINT", "false").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

        return cls(
            api_key=api_key,
            base_url=base_url.rstrip("/"),
            default_model=default_model,
            default_video_generation_model=default_video_generation_model,
            default_reference_video_url=default_reference_video_url,
            default_video_path=default_video_path,
            default_file_id=default_file_id,
            timeout_seconds=timeout_seconds,
            file_purpose=file_purpose,
            input_file_type=input_file_type,
            video_generation_duration_seconds=video_generation_duration_seconds,
            video_generation_ratio=video_generation_ratio,
            video_generation_resolution=video_generation_resolution,
            video_generation_poll_interval_seconds=video_generation_poll_interval_seconds,
            video_generation_wait_timeout_seconds=video_generation_wait_timeout_seconds,
            video_generation_reference_video_role=video_generation_reference_video_role,
            video_generation_reference_image_role=video_generation_reference_image_role,
            tos_bucket=tos_bucket,
            tos_access_key=tos_access_key,
            tos_secret_key=tos_secret_key,
            tos_endpoint=tos_endpoint,
            tos_region=tos_region,
            tos_object_prefix=tos_object_prefix,
            tos_enable_https=tos_enable_https,
            tos_force_endpoint=tos_force_endpoint,
        )
