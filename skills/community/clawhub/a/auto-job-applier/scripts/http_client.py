#!/usr/bin/env python3
"""
http_client.py — Shared HTTP client for the Auto Job Applier skill.

Provides a session-based HTTP client with:
  - requests library (replaces urllib)
  - Automatic retry with exponential backoff
  - Retry-After header support for 429 rate limits
  - Custom exception hierarchy for error categorization
  - Configurable timeouts

Usage:
    from http_client import create_session, ResumeXAPIError, RateLimitError

    session = create_session(api_key)
    data = session.api_get("/api/v1/agent")
    session.api_post("/api/v1/agent/jobs", {"company": "Acme"})
"""

import os
import sys
import json
import time

try:
    import requests
    from requests.exceptions import ConnectionError, Timeout, RequestException
except ImportError:
    print(
        "ERROR: 'requests' library is not installed.\n"
        "Install it with:\n"
        "  pip3 install requests\n"
        "Or:\n"
        "  pip3 install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


# ── Exception Hierarchy ──────────────────────────────────────────────────────

class ResumeXAPIError(Exception):
    """Base exception for all ResumeX API errors."""

    def __init__(self, message: str, status_code: int = None, response_body: str = ""):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class AuthenticationError(ResumeXAPIError):
    """401/403 — API key is missing, invalid, or expired."""
    pass


class NotFoundError(ResumeXAPIError):
    """404 — Resource not found (e.g. no resume, invalid endpoint)."""
    pass


class RateLimitError(ResumeXAPIError):
    """429 — Rate limited. Check retry_after for wait time."""

    def __init__(self, message: str, retry_after: int = 10, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class ServerError(ResumeXAPIError):
    """5xx — Server-side error."""
    pass


class NetworkError(ResumeXAPIError):
    """Connection timeout, DNS failure, or other network issue."""
    pass


# ── Constants ────────────────────────────────────────────────────────────────

API_BASE_URL = "https://resumex.dev"
DEFAULT_TIMEOUT = 15  # seconds
MAX_RETRIES = 3
BASE_BACKOFF_DELAY = 1  # seconds
MAX_BACKOFF_DELAY = 30  # seconds


# ── API Session ──────────────────────────────────────────────────────────────

class ResumeXSession:
    """
    A session-based HTTP client for the ResumeX API.

    Wraps the requests library with automatic retry logic, exponential backoff,
    and structured error handling.
    """

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT,
                 max_retries: int = MAX_RETRIES):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _classify_error(self, response: requests.Response) -> ResumeXAPIError:
        """Classify an HTTP error response into the appropriate exception type."""
        code = response.status_code
        try:
            body = response.text
        except Exception:
            body = ""

        if code == 401:
            return AuthenticationError(
                "401 Unauthorized. Your RESUMEX_API_KEY is invalid or expired.\n"
                "Please generate a new key at resumex.dev → Dashboard → Resumex API.",
                status_code=code,
                response_body=body,
            )
        elif code == 403:
            return AuthenticationError(
                "403 Forbidden. Your API key does not have permission for this action.",
                status_code=code,
                response_body=body,
            )
        elif code == 404:
            return NotFoundError(
                f"404 Not Found. The requested resource does not exist.\n"
                f"Response: {body[:200]}",
                status_code=code,
                response_body=body,
            )
        elif code == 429:
            retry_after = int(response.headers.get("Retry-After", "10"))
            return RateLimitError(
                f"429 Rate Limited. Please wait {retry_after}s before retrying.",
                retry_after=retry_after,
                status_code=code,
                response_body=body,
            )
        elif 500 <= code < 600:
            return ServerError(
                f"Server error {code}: {response.reason}. "
                f"This is a temporary issue on the ResumeX side.",
                status_code=code,
                response_body=body,
            )
        else:
            return ResumeXAPIError(
                f"HTTP {code}: {response.reason}\n{body[:200]}",
                status_code=code,
                response_body=body,
            )

    def _should_retry(self, error: ResumeXAPIError) -> bool:
        """Determine if a request should be retried based on the error type."""
        return isinstance(error, (RateLimitError, ServerError, NetworkError))

    def _get_backoff_delay(self, attempt: int, error: ResumeXAPIError = None) -> float:
        """Calculate exponential backoff delay, respecting Retry-After header for 429s."""
        if isinstance(error, RateLimitError) and error.retry_after:
            return min(error.retry_after, MAX_BACKOFF_DELAY)
        delay = BASE_BACKOFF_DELAY * (2 ** attempt)
        return min(delay, MAX_BACKOFF_DELAY)

    def _request(self, method: str, path: str, json_body: dict = None,
                 raw_url: str = None) -> dict:
        """
        Execute an HTTP request with automatic retry and error handling.

        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            path: API path (e.g. "/api/v1/agent")
            json_body: Optional JSON request body
            raw_url: If set, use this full URL instead of API_BASE_URL + path

        Returns:
            Parsed JSON response dict

        Raises:
            AuthenticationError: On 401/403
            NotFoundError: On 404
            RateLimitError: On 429 (after all retries exhausted)
            ServerError: On 5xx (after all retries exhausted)
            NetworkError: On connection/timeout failure (after all retries exhausted)
        """
        url = raw_url or f"{API_BASE_URL}{path}"
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=json_body,
                    timeout=self.timeout,
                )

                # Success
                if response.ok:
                    if response.text.strip():
                        return response.json()
                    return {"success": True}

                # Classify the error
                error = self._classify_error(response)

                # Non-retryable errors: raise immediately
                if not self._should_retry(error):
                    raise error

                last_error = error

            except (ConnectionError, Timeout) as e:
                last_error = NetworkError(
                    f"Network error: {str(e)}. Check your internet connection.",
                    status_code=None,
                )
            except RequestException as e:
                last_error = NetworkError(
                    f"Request failed: {str(e)}",
                    status_code=None,
                )

            # Retry logic
            if attempt < self.max_retries:
                delay = self._get_backoff_delay(attempt, last_error)
                error_type = type(last_error).__name__
                print(
                    f"⏳ {error_type} — retrying in {delay:.0f}s "
                    f"(attempt {attempt + 1}/{self.max_retries})...",
                    file=sys.stderr,
                )
                time.sleep(delay)

        # All retries exhausted
        raise last_error

    def api_get(self, path: str) -> dict:
        """Send a GET request to the ResumeX API."""
        return self._request("GET", path)

    def api_post(self, path: str, payload: dict) -> dict:
        """Send a POST request to the ResumeX API."""
        return self._request("POST", path, json_body=payload)

    def api_patch(self, path: str, payload: dict) -> dict:
        """Send a PATCH request to the ResumeX API."""
        return self._request("PATCH", path, json_body=payload)

    def api_post_with_fallback(self, paths: list, payload: dict) -> dict:
        """
        Try POST to multiple paths in order, falling back on 404.

        Args:
            paths: List of API paths to try (e.g. ["/api/v1/agent/jobs", "/api/v1/agent/logs"])
            payload: JSON payload to send

        Returns:
            Parsed JSON response from the first successful endpoint

        Raises:
            The last error encountered if all paths fail
        """
        last_error = None
        for i, path in enumerate(paths):
            try:
                return self.api_post(path, payload)
            except NotFoundError as e:
                last_error = e
                if i < len(paths) - 1:
                    print(
                        f"⚠️  Endpoint {path} returned 404, trying next...",
                        file=sys.stderr,
                    )
                continue

        raise last_error

    def close(self):
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ── Factory Function ─────────────────────────────────────────────────────────

def get_api_key() -> str:
    """
    Retrieve the RESUMEX_API_KEY from environment variables.

    Returns:
        The API key string.

    Raises:
        SystemExit: If the key is not set.
    """
    key = os.environ.get("RESUMEX_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: RESUMEX_API_KEY environment variable is not set.\n"
            "Steps to fix:\n"
            "  1. Go to https://resumex.dev → Dashboard → Resumex API\n"
            "  2. Generate a new API key\n"
            "  3. Set RESUMEX_API_KEY in your OpenClaw environment variables",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def create_session(api_key: str = None, timeout: int = DEFAULT_TIMEOUT,
                   max_retries: int = MAX_RETRIES) -> ResumeXSession:
    """
    Create a new ResumeX API session.

    Args:
        api_key: API key. If None, reads from RESUMEX_API_KEY env var.
        timeout: Request timeout in seconds (default: 15).
        max_retries: Max retry attempts for transient errors (default: 3).

    Returns:
        A configured ResumeXSession instance.
    """
    if api_key is None:
        api_key = get_api_key()
    return ResumeXSession(api_key=api_key, timeout=timeout, max_retries=max_retries)
