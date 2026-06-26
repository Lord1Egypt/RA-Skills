from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import quote

from .bytedtos_upload_demo import (
    BytedTosDemoError,
    BytedTosDependencyError,
    TosUploadDemoConfig,
    build_object_key,
    create_client,
)
from .config import Settings

logger = logging.getLogger(__name__)


class CDNUploadError(RuntimeError):
    """Raised when TOS upload is unavailable or fails."""


class CDNUploader:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def is_configured(self) -> bool:
        return bool(
            self._settings.tos_bucket
            and self._settings.tos_access_key
            and self._settings.tos_secret_key
            and self._settings.tos_endpoint
            and self._settings.tos_region
        )

    def upload(self, file_path: str | Path) -> str:
        path = Path(file_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"CDN upload file not found: {path}")
        if not self.is_configured():
            raise CDNUploadError(
                "TOS upload is not configured. Set TOS_BUCKET, TOS_AK, TOS_SK, TOS_ENDPOINT, and TOS_REGION."
            )

        config = self._build_tos_config()
        object_key = build_object_key(config.object_prefix, path.name)
        logger.info("Uploading file via TOS: %s", path.name)
        try:
            client = create_client(config)
            with path.open("rb") as file_obj:
                client.put_object(
                    bucket=config.bucket,
                    key=object_key,
                    content=file_obj,
                )
        except (BytedTosDemoError, BytedTosDependencyError) as exc:
            raise CDNUploadError(str(exc)) from exc
        except Exception as exc:
            raise CDNUploadError(f"TOS upload failed: {exc}") from exc

        return _build_tos_object_url(config=config, object_key=object_key)

    def _build_tos_config(self) -> TosUploadDemoConfig:
        bucket = self._settings.tos_bucket
        access_key = self._settings.tos_access_key
        secret_key = self._settings.tos_secret_key
        endpoint = self._settings.tos_endpoint
        region = self._settings.tos_region
        if not bucket or not access_key or not secret_key or not endpoint or not region:
            raise CDNUploadError(
                "TOS upload is not configured. Set TOS_BUCKET, TOS_AK, TOS_SK, TOS_ENDPOINT, and TOS_REGION."
            )
        return TosUploadDemoConfig(
            bucket=bucket,
            access_key=access_key,
            secret_key=secret_key,
            endpoint=endpoint,
            region=region,
            object_prefix=self._settings.tos_object_prefix,
            enable_https=self._settings.tos_enable_https,
            force_endpoint=self._settings.tos_force_endpoint,
            timeout_seconds=self._settings.timeout_seconds,
            connect_timeout_seconds=min(self._settings.timeout_seconds, 5.0),
        )


def _build_tos_object_url(*, config: TosUploadDemoConfig, object_key: str) -> str:
    scheme = "https" if config.enable_https else "http"
    return f"{scheme}://{config.bucket}.{config.endpoint}/{quote(object_key, safe='/')}"
