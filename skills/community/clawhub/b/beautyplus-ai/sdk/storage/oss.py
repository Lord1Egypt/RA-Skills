"""OSS upload functionality for BeautyPlus AI SDK."""

import os
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, Dict, Any

import alibabacloud_oss_v2 as oss

from sdk.core.config import USER_AGENT


def normalize_oss_endpoint(url: str) -> str:
    """Ensure endpoint is https://host with no path."""
    if not url:
        return url
    u = url.strip()
    if "://" not in u:
        u = "https://" + u
    parsed = urlparse(u)
    if not parsed.netloc:
        return u
    return f"{parsed.scheme or 'https'}://{parsed.netloc}"


def _region_from_oss_endpoint_host(host: str) -> Optional[str]:
    """
    Infer OSS signing region from endpoint hostname.
    Supports path-style (oss-cn-beijing.aliyuncs.com) and virtual-hosted
    (bucket.oss-cn-beijing.aliyuncs.com).
    """
    host = (host or "").lower()
    if ".oss-" in host and "aliyuncs.com" in host:
        tail = host.split(".oss-", 1)[1]
        reg = tail.split(".aliyuncs.com", 1)[0]
        if reg.endswith("-internal"):
            reg = reg[: -len("-internal")]
        if reg:
            return reg
    if host.startswith("oss-") and "aliyuncs.com" in host:
        seg = host.split(".")[0]
        if seg.startswith("oss-"):
            seg = seg[4:]
        if seg.endswith("-internal"):
            seg = seg[: -len("-internal")]
        if seg:
            return seg
    return None


def resolve_oss_region(policy: Dict[str, Any], oss_region_fallback: Optional[str] = None) -> str:
    """
    OSS SDK v2 requires region (e.g. cn-beijing).
    Prefer region parsed from endpoint host (authoritative for bucket);
    token_policy['region'] may be API region (e.g. cn-north-4) and must not
    override when host is clearly OSS virtual-hosted or path-style.
    """
    endpoint = policy.get("url") or ""
    parsed = urlparse(endpoint if "://" in endpoint else "https://" + endpoint)
    host = parsed.hostname or ""
    from_host = _region_from_oss_endpoint_host(host)
    if from_host:
        return from_host
    r = policy.get("region")
    if r:
        return str(r).strip()
    if oss_region_fallback:
        return oss_region_fallback
    raise ValueError(
        "Cannot determine OSS region from policy; set policy['region'] or pass oss_region="
    )


class OssUploader:
    """OSS file upload handler."""

    def __init__(self, policy: Dict[str, Any], oss_region: Optional[str] = None, user_agent: str = USER_AGENT):
        self.policy = policy
        self.oss_region = oss_region
        self.user_agent = user_agent

    def upload(self, file) -> Dict[str, Any]:
        """
        Upload data to OSS.

        :param file: The data to upload. This can either be bytes or a string.
                     When this argument is a string, it is interpreted as a file name.
        :return: The policy data with upload result information.
        """
        creds = self.policy["credentials"]
        credentials_provider = oss.credentials.StaticCredentialsProvider(
            creds["access_key"],
            creds["secret_key"],
            creds.get("session_token"),
        )
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = resolve_oss_region(self.policy, self.oss_region)
        cfg.endpoint = normalize_oss_endpoint(self.policy["url"])

        client = oss.Client(cfg)
        key = self.policy.get("key") or ""

        try:
            if isinstance(file, str):
                result = client.put_object_from_file(
                    oss.PutObjectRequest(
                        bucket=self.policy["bucket"],
                        key=key,
                    ),
                    file,
                )
            else:
                result = client.put_object(
                    oss.PutObjectRequest(
                        bucket=self.policy["bucket"],
                        key=key,
                        body=file,
                    )
                )

            if result.status_code != 200:
                raise RuntimeError(
                    f"OSS put_object failed: status={result.status_code}, "
                    f"request_id={getattr(result, 'request_id', None)}"
                )

            return self.policy.get("data", {})
        finally:
            if not isinstance(file, str) and getattr(file, "close", None):
                file.close()
