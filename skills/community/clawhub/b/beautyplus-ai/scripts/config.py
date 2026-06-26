import os

# BeautyPlus WAPI gateway endpoint.
# This is the required API host for the BeautyPlus paid image-processing service.
# Credentials (BP_AK / BP_SK) are passed via HMAC-signed Authorization headers,
# never as query parameters or in the request body.
WAPI_ENDPOINT = "https://webapi-beautyplus.pixocial.com"

# GID cache (persistent on disk, no TTL in this skill)
GID_CACHE_FILE = "~/.cache/beautyplus/gid_cache.json"

VERSION = "v1.0.1"
USER_AGENT = "beautyplus-web-skill-v1.0.1"

# HTTP(S) input download (run-task --input URL and resolve-input --url); overridable via env.
URL_DOWNLOAD_MAX_BYTES_DEFAULT = 100 * 1024 * 1024
URL_DOWNLOAD_CONNECT_TIMEOUT_DEFAULT = 15
URL_DOWNLOAD_READ_TIMEOUT_DEFAULT = 120


def url_download_max_bytes() -> int:
    raw = os.environ.get("MT_AI_URL_MAX_BYTES", "").strip()
    if raw:
        try:
            return max(1, int(raw))
        except ValueError:
            pass
    return URL_DOWNLOAD_MAX_BYTES_DEFAULT


def url_download_connect_timeout() -> int:
    raw = os.environ.get("MT_AI_URL_CONNECT_TIMEOUT", "").strip()
    if raw:
        try:
            return max(1, min(int(raw), 300))
        except ValueError:
            pass
    return URL_DOWNLOAD_CONNECT_TIMEOUT_DEFAULT


def url_download_read_timeout() -> int:
    raw = os.environ.get("MT_AI_URL_READ_TIMEOUT", "").strip()
    if raw:
        try:
            return max(1, min(int(raw), 3600))
        except ValueError:
            pass
    return URL_DOWNLOAD_READ_TIMEOUT_DEFAULT


def url_download_timeout_tuple() -> tuple[int, int]:
    return (url_download_connect_timeout(), url_download_read_timeout())

# Region map (overwritten by server config when fetched)
REGIONS = {
}

# Optional app parameter for /ai/token_policy, can be overridden by /skill/config.json.
TOKEN_POLICY_APP = None
