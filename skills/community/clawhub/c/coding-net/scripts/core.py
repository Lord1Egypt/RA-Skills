"""Coding Open API — infrastructure (HTTP client, token resolution)."""

from __future__ import annotations

import json
import logging
import os
import traceback
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

BASE_URL = "https://e.coding.net/open-api/"
DEFAULT_TIMEOUT = 30
# Set the token via `export CODING_TOKEN=...` — never hardcode secrets in code.
TOKEN_ENV = "CODING_TOKEN"
# Default project name
DEFAULT_PROJECT_NAME_ENV = "CODING_DEFAULT_PROJECT_NAME"
DEFAULT_PROJECT_NAME: str | None = None
# Default source for the iteration Code used in DescribeIssueList's ITERATION condition
DEFAULT_ITERATION_ENV = "CODING_DEFAULT_ITERATION_CODE"
DEFAULT_ITERATION_CODE: int | None = None


class CodingAPIError(Exception):
    """A Coding API call failed (HTTP error, invalid JSON, or malformed response)."""


def _resolve_project_name(project_name: str | None) -> str:
    if project_name is not None and project_name.strip():
        return project_name.strip()
    env = os.environ.get(DEFAULT_PROJECT_NAME_ENV, "").strip()
    if env:
        return env
    if DEFAULT_PROJECT_NAME is not None and DEFAULT_PROJECT_NAME.strip():
        return DEFAULT_PROJECT_NAME.strip()
    raise ValueError(
        f"No project name provided: pass project_name=..., or set the environment variable {DEFAULT_PROJECT_NAME_ENV}",
    )


def _resolve_token(token: str | None) -> str:
    if token is not None and token.strip():
        return token.strip()
    env = os.environ.get(TOKEN_ENV, "").strip()
    if env:
        return env
    raise ValueError(
        f"No token provided: pass token=..., or set the environment variable {TOKEN_ENV}",
    )


def _request(
    action: str,
    body: dict[str, Any],
    token: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Send a POST request to the Coding Open API and return the parsed JSON object."""
    query = urlencode({"Action": action, "action": action})
    url = f"{BASE_URL}?{query}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = Request(
        url,
        data=data,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
    except HTTPError as e:
        try:
            raw = e.read()
        except Exception:
            raw = b""
        logger.error("Coding API HTTP error: %s\n%s", e, traceback.format_exc())
        raise CodingAPIError(f"HTTP {e.code}: {e.reason}") from e
    except URLError as e:
        logger.error("Coding API network error: %s\n%s", e, traceback.format_exc())
        raise CodingAPIError(f"Request failed: {e.reason}") from e
    except Exception:
        logger.error("Coding API request exception\n%s", traceback.format_exc())
        raise

    try:
        text = raw.decode("utf-8")
        parsed: dict[str, Any] = json.loads(text)
    except json.JSONDecodeError:
        logger.error(
            "Coding API response is not valid JSON\n%s\nbody excerpt: %s",
            traceback.format_exc(),
            raw[:500],
        )
        raise CodingAPIError("Response is not valid JSON") from None

    if status and not (200 <= status < 300):
        logger.error("Coding API returned a non-success status: status=%s body=%s", status, parsed)
        raise CodingAPIError(f"Unexpected HTTP status: {status}")

    if "Response" not in parsed:
        err = parsed.get("Error") or parsed.get("error") or parsed
        logger.error("Coding API response is missing Response: %s", err)
        raise CodingAPIError(f"Response is missing the 'Response' field: {err}")

    return parsed


def get_team_info(*, token: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Return basic team info (Name, TeamHost, etc.), used to validate that the token is valid."""
    t = _resolve_token(token)
    parsed = _request("DescribeTeam", {}, t, timeout=timeout)
    return parsed.get("Response", {}).get("Data", {})


def bootstrap(
    project_name: str | None = None,
    *,
    token: str | None = None,
) -> dict[str, Any]:
    """
    Bootstrap: validate the token and (optionally) validate the project, returning the iteration list.

    Returns {"team": {"name": str, "host": str}, "iterations": [...], "error": str | None}

    Usage:
    - bootstrap() — validates only the token, confirming the team
    - bootstrap("biaopin-swiftagent") — also validates the project and returns the iteration list for the user to choose from
    """
    result: dict[str, Any] = {"team": None, "iterations": [], "error": None}
    try:
        t = _resolve_token(token)
    except ValueError as e:
        result["error"] = str(e)
        return result

    try:
        team = get_team_info(token=t)
    except Exception as e:
        result["error"] = f"Token is invalid or team info could not be fetched: {e}"
        return result

    if not team or "Name" not in team:
        result["error"] = "Token is invalid: could not fetch team info"
        return result

    result["team"] = {"name": team.get("Name"), "host": team.get("TeamHost")}

    if project_name:
        pn = project_name.strip()
        try:
            parsed = _request("DescribeIterationList", {"ProjectName": pn}, t)
            err = parsed.get("Response", {}).get("Error")
            if err:
                result["error"] = f"Project '{pn}' does not exist or is not accessible: {err.get('Message')}"
            else:
                items = parsed.get("Response", {}).get("Data", {}).get("List") or []
                result["iterations"] = [{"code": it["Code"], "name": it["Name"]} for it in items]
        except Exception as e:
            result["error"] = f"Failed to query iterations: {e}"

    return result
