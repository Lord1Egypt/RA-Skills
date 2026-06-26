from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class OssUploadResult:
    object_key: str
    public_url: str


class OssUploader:
    """
    Upload local files to Alibaba Cloud OSS and return public URLs.

    This uploader is intentionally optional at runtime:
    - If required env vars are missing, treat OSS as disabled.
    - If OSS is enabled but `oss2` is missing, fail with a clear message.
    """

    def __init__(
        self,
        endpoint: str,
        bucket: str,
        access_key_id: str,
        access_key_secret: str,
        prefix: str = "",
        public_base_url: str | None = None,
    ) -> None:
        endpoint = endpoint.strip()
        if endpoint and not endpoint.startswith(("http://", "https://")):
            endpoint = "https://" + endpoint
        self.endpoint = endpoint
        self.endpoint_host = endpoint.removeprefix("https://").removeprefix("http://")
        self.bucket = bucket
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.prefix = prefix.strip("/")
        self.public_base_url = (public_base_url or "").rstrip("/")

    @staticmethod
    def from_env() -> Optional["OssUploader"]:
        endpoint = os.getenv("OSS_ENDPOINT", "").strip()
        bucket = os.getenv("OSS_BUCKET", "").strip()
        access_key_id = os.getenv("OSS_ACCESS_KEY_ID", "").strip()
        access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET", "").strip()
        prefix = os.getenv("OSS_PREFIX", "bbt-skills/competitive-analysis").strip()
        public_base_url = os.getenv("OSS_PUBLIC_BASE_URL", "").strip() or None

        required = [endpoint, bucket, access_key_id, access_key_secret]
        if not all(required):
            return None
        return OssUploader(
            endpoint=endpoint,
            bucket=bucket,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            prefix=prefix,
            public_base_url=public_base_url,
        )

    def upload_file(self, local_path: Path, object_key: str) -> OssUploadResult:
        try:
            import oss2  # type: ignore
        except ImportError as exc:
            raise RuntimeError("已配置 OSS_* 环境变量，但缺少依赖 oss2。请安装：python3 -m pip install oss2") from exc

        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket)
        bucket.put_object_from_file(object_key, str(local_path))
        return OssUploadResult(object_key=object_key, public_url=self._public_url(object_key))

    def key_for(self, relative_path: str) -> str:
        cleaned = relative_path.lstrip("/")
        if self.prefix:
            return f"{self.prefix}/{cleaned}"
        return cleaned

    def _public_url(self, object_key: str) -> str:
        if self.public_base_url:
            return f"{self.public_base_url}/{object_key}"

        # Derive a public URL (works for public-read buckets or public endpoints).
        # Example endpoint: oss-cn-hangzhou.aliyuncs.com
        # Public URL: https://{bucket}.{endpoint}/{object_key}
        return f"https://{self.bucket}.{self.endpoint_host}/{object_key}"
