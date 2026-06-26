"""
Common utilities for Feishu Bitable Attachment Skill.

Provides:
- Custom exception classes for clear error handling
- Environment variable loading
- HTTP request wrapper with retry logic
- Token management (tenant_access_token caching)
- JSON output helpers
- MIME type detection
- Logging utilities
"""

import os
import json
import time
import hashlib
import mimetypes
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

import requests


# ============================================================================
# Custom Exception Classes
# ============================================================================

class SkillError(Exception):
    """Base exception for Skill errors."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {"error": self.message, **self.details}


class SkillInputError(SkillError):
    """Invalid input parameters."""
    pass


class SkillFileNotFoundError(SkillError):
    """Local file not found."""
    pass


class SkillDownloadError(SkillError):
    """Failed to download file from URL."""
    pass


class FeishuAuthError(SkillError):
    """Authentication/authorization failed."""
    pass


class FeishuAPIError(SkillError):
    """Feishu API request failed."""
    def __init__(self, message: str, status_code: int = 0, response_data: Optional[Dict] = None, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.status_code = status_code
        self.response_data = response_data or {}


class FeishuUploadError(SkillError):
    """File upload to Feishu failed."""
    pass


class BitableResolveError(SkillError):
    """Failed to resolve Bitable target (table/field/record)."""
    pass


class BitableUpdateError(SkillError):
    """Failed to update Bitable record."""
    pass


# ============================================================================
# Environment Variables
# ============================================================================

def get_env(name: str, default: str = "") -> str:
    """Get environment variable with optional default."""
    return os.environ.get(name, default)


def get_env_required(name: str) -> str:
    """
    Get required environment variable, raise if missing.

    Raises:
        SkillInputError: If environment variable is not set
    """
    value = os.environ.get(name)
    if not value:
        raise SkillInputError(
            f"Required environment variable {name} is not set. "
            f"Please set it before running this skill."
        )
    return value


def get_feishu_base_url() -> str:
    """Get Feishu API base URL."""
    return get_env("FEISHU_BASE_URL", "https://open.feishu.cn")


# ============================================================================
# Token Management
# ============================================================================

class TokenCache:
    """Simple in-memory token cache."""

    def __init__(self):
        self._token: Optional[str] = None
        self._expire_at: Optional[datetime] = None

    def get(self) -> Optional[str]:
        """Get cached token if valid."""
        if self._token and self._expire_at and datetime.now() < self._expire_at:
            return self._token
        return None

    def set(self, token: str, expires_in: int):
        """Cache token with expiration."""
        self._token = token
        # Expire 5 minutes early to be safe
        self._expire_at = datetime.now() + timedelta(seconds=expires_in - 300)

    def clear(self):
        """Clear cached token."""
        self._token = None
        self._expire_at = None


# Global token cache
_token_cache = TokenCache()


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """
    Get tenant_access_token using app credentials.

    Uses cache if available. Fetches new token if missing or expired.

    Args:
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        tenant_access_token string

    Raises:
        FeishuAuthError: If token acquisition fails
    """
    # Check cache first
    cached = _token_cache.get()
    if cached:
        return cached

    # Fetch new token
    base_url = get_feishu_base_url()
    url = f"{base_url}/open-apis/auth/v3/tenant_access_token/internal"

    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }

    try:
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code != 200:
            raise FeishuAuthError(
                f"Failed to get tenant_access_token: HTTP {response.status_code}. "
                f"Please check your network connection."
            )

        data = response.json()

        if data.get("code") != 0:
            raise FeishuAuthError(
                f"Failed to get tenant_access_token: {data.get('code')} - {data.get('msg', 'Unknown error')}. "
                f"Please check your FEISHU_APP_ID and FEISHU_APP_SECRET."
            )

        token = data.get("tenant_access_token")
        expires_in = data.get("expire", 7200)

        if not token:
            raise FeishuAuthError("tenant_access_token not returned in response")

        # Cache the token
        _token_cache.set(token, expires_in)

        return token

    except requests.RequestException as e:
        raise FeishuAuthError(f"Failed to get tenant_access_token: Network error - {str(e)}")


# ============================================================================
# Feishu API Constants
# ============================================================================

# Drive Upload API endpoints - Medias upload flow (current API)
API_UPLOAD_MATERIAL = "/open-apis/drive/v1/medias/upload_all"
API_CHUNKED_UPLOAD_PREPARE = "/open-apis/drive/v1/medias/upload_prepare"
API_CHUNKED_UPLOAD = "/open-apis/drive/v1/medias/upload_part"
API_CHUNKED_UPLOAD_FINISH = "/open-apis/drive/v1/medias/upload_finish"

# Bitable API endpoints
API_BITABLE_LIST_TABLES = "/open-apis/bitable/v1/apps/{app_token}/tables"
API_BITABLE_LIST_FIELDS = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
API_BITABLE_GET_RECORD = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
API_BITABLE_UPDATE_RECORD = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
API_BITABLE_CREATE_RECORD = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
API_BITABLE_SEARCH_RECORDS = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"

# Upload thresholds
CHUNKED_UPLOAD_THRESHOLD = 20 * 1024 * 1024  # 20MB
DEFAULT_CHUNK_SIZE = 5 * 1024 * 1024  # 5MB per part

# ============================================================================
# HTTP Request Wrapper
# ============================================================================

def make_request(
    method: str,
    url: str,
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    data: Optional[Any] = None,
    json_body: Optional[Dict] = None,
    files: Optional[Dict] = None,
    timeout: int = 60,
    max_retries: int = 2
) -> Dict[str, Any]:
    """
    Make HTTP request with retry logic.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        headers: Request headers
        params: URL query parameters
        data: Form data
        json_body: JSON body (use json_body instead of json to avoid keyword conflict)
        files: Files for upload
        timeout: Request timeout in seconds
        max_retries: Number of retry attempts

    Returns:
        Response data as dict

    Raises:
        FeishuAPIError: On request failure
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_body,
                files=files,
                timeout=timeout
            )

            # Try to parse as JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"raw": response.text}

            # Check for Feishu API error code
            if isinstance(response_data, dict) and response_data.get("code") != 0:
                raise FeishuAPIError(
                    f"Feishu API error: {response_data.get('code')} - {response_data.get('msg', 'Unknown error')}",
                    status_code=response.status_code,
                    response_data=response_data
                )

            # Check for HTTP error
            if response.status_code >= 400:
                raise FeishuAPIError(
                    f"HTTP error: {response.status_code}",
                    status_code=response.status_code,
                    response_data=response_data
                )

            return response_data

        except requests.RequestException as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(1 * (attempt + 1))  # Progressive backoff
                continue
            raise FeishuAPIError(f"Request failed: {str(e)}")

    raise FeishuAPIError(f"Request failed after {max_retries} retries: {last_error}")


def make_authenticated_request(
    method: str,
    url: str,
    app_id: str,
    app_secret: str,
    **kwargs
) -> Dict[str, Any]:
    """
    Make authenticated request to Feishu API.

    Automatically adds tenant_access_token to headers.

    Args:
        method: HTTP method
        url: Request URL
        app_id: Feishu app ID
        app_secret: Feishu app secret
        **kwargs: Additional arguments for make_request

    Returns:
        Response data as dict

    Raises:
        FeishuAuthError: If token acquisition fails
        FeishuAPIError: If request fails
    """
    token = get_tenant_access_token(app_id, app_secret)

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"

    return make_request(method, url, headers=headers, **kwargs)


# ============================================================================
# File Utilities
# ============================================================================

def detect_mime_type(file_path: str) -> str:
    """Detect MIME type from file extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)


def generate_file_hash(file_path: str) -> str:
    """Generate SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# ============================================================================
# Output Helpers
# ============================================================================

def output_success(data: Dict[str, Any]) -> str:
    """Format success output as JSON."""
    result = {"ok": True, **data}
    return json.dumps(result, indent=2, ensure_ascii=False)


def output_error(message: str, details: Optional[Dict] = None) -> str:
    """Format error output as JSON."""
    result = {"ok": False, "error": message}
    if details:
        result["details"] = details
    return json.dumps(result, indent=2, ensure_ascii=False)


def print_json(data: Dict[str, Any]):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================================
# Logging
# ============================================================================

class Logger:
    """Simple logger with timestamp."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def _log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix_str = f"[{self.prefix}] " if self.prefix else ""
        print(f"[{timestamp}] {prefix_str}{level}: {message}")

    def info(self, message: str):
        self._log("INFO", message)

    def warning(self, message: str):
        self._log("WARN", message)

    def error(self, message: str):
        self._log("ERROR", message)

    def debug(self, message: str):
        self._log("DEBUG", message)


# Global logger
log = Logger("feishu-bitable")


# ============================================================================
# Validation Helpers
# ============================================================================

def validate_required_fields(data: Dict, fields: List[str], context: str = "Input") -> None:
    """
    Validate that required fields are present.

    Raises:
        SkillInputError: If required fields are missing
    """
    missing = [f for f in fields if f not in data or not data[f]]
    if missing:
        raise SkillInputError(f"{context} missing required fields: {', '.join(missing)}")


def validate_one_of_fields(data: Dict, fields: List[str], context: str = "Input") -> None:
    """
    Validate that at least one of the specified fields is present.

    Raises:
        SkillInputError: If none of the fields are present
    """
    present = [f for f in fields if f in data and data[f]]
    if not present:
        raise SkillInputError(f"{context} requires at least one of: {', '.join(fields)}")
