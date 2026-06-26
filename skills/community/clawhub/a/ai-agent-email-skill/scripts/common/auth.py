import os
import json
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Any

from .errors import SkillError


def _get_password_from_env() -> str | None:
    """Read password from environment variables."""
    return os.environ.get("EMAIL_PASSWORD")


def _get_username_from_env() -> str | None:
    """Read username from environment variable."""
    return os.environ.get("EMAIL_USERNAME")


def _detect_auth_type() -> str | None:
    """Detect authentication type from environment variables."""
    has_oauth2 = all([
        os.environ.get("EMAIL_OAUTH2_CLIENT_ID"),
        os.environ.get("EMAIL_OAUTH2_CLIENT_SECRET"),
        os.environ.get("EMAIL_OAUTH2_REFRESH_TOKEN"),
        os.environ.get("EMAIL_OAUTH2_TOKEN_URL"),
    ])
    if has_oauth2:
        return "oauth2"
    has_password = os.environ.get("EMAIL_PASSWORD")
    if has_password:
        return "password"
    return None


def _get_oauth2_from_env(oauth_cfg: dict[str, Any]) -> dict[str, Any]:
    """Read OAuth2 config from environment variables."""
    result = oauth_cfg.copy() if oauth_cfg else {}
    result["client_id"] = os.environ.get("EMAIL_OAUTH2_CLIENT_ID", oauth_cfg.get("client_id", "") if oauth_cfg else "")
    result["client_secret"] = os.environ.get("EMAIL_OAUTH2_CLIENT_SECRET", oauth_cfg.get("client_secret", "") if oauth_cfg else "")
    result["refresh_token"] = os.environ.get("EMAIL_OAUTH2_REFRESH_TOKEN", oauth_cfg.get("refresh_token", "") if oauth_cfg else "")
    result["token_url"] = os.environ.get("EMAIL_OAUTH2_TOKEN_URL", oauth_cfg.get("token_url", "") if oauth_cfg else "")
    return result


def get_oauth2_token(oauth_cfg: dict[str, Any]) -> str:
    """Fetches a new OAuth2 access token using the refresh token with retry logic."""
    token_url = oauth_cfg.get("token_url")
    refresh_token = oauth_cfg.get("refresh_token")
    client_id = oauth_cfg.get("client_id")
    client_secret = oauth_cfg.get("client_secret")

    if not all([token_url, refresh_token, client_id, client_secret]):
        raise SkillError("CONFIG_ERROR", "Missing one or more required OAuth2 fields for token refresh in account configuration.")

    if not isinstance(token_url, str):
        raise SkillError("CONFIG_ERROR", "OAuth2 token_url must be a string")

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")

    max_retries = 3
    base_delay = 1.0

    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    if response.status in (400, 401, 403):
                        raise SkillError("OAUTH_ERROR", f"OAuth2 token refresh failed (auth error): {response.status}", {"status": response.status})
                    raise SkillError("OAUTH_ERROR", f"Failed to refresh OAuth2 token, status: {response.status}", {"status": response.status})

                token_data = json.loads(response.read().decode("utf-8"))
                access_token = token_data.get("access_token")
                if not access_token:
                    raise SkillError("OAUTH_ERROR", "No access_token in OAuth2 response", {"response": token_data})
                return access_token
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403):
                raise SkillError("OAUTH_ERROR", f"OAuth2 token refresh failed (auth error): {e.code}", {"status": e.code}) from e
            if attempt == max_retries:
                raise SkillError("OAUTH_ERROR", f"Failed to refresh OAuth2 token after {max_retries} attempts: {e.reason}") from e
        except urllib.error.URLError as e:
            if attempt == max_retries:
                raise SkillError("NETWORK_ERROR", f"Failed to connect to OAuth2 token URL after {max_retries} attempts: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise SkillError("OAUTH_ERROR", "Failed to parse OAuth2 token response as JSON") from e

        if attempt < max_retries:
            delay = base_delay * (2 ** (attempt - 1))
            time.sleep(delay)

    raise SkillError("NETWORK_ERROR", f"Failed to refresh OAuth2 token after {max_retries} attempts")
