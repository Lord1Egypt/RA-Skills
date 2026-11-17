"""Coding Open API — iteration-related endpoints."""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import Any

sys.path.insert(0, os.path.dirname(__file__))
from core import (  # noqa: E402
    CodingAPIError,
    DEFAULT_ITERATION_CODE,
    DEFAULT_ITERATION_ENV,
    DEFAULT_TIMEOUT,
    _request,
    _resolve_project_name,
    _resolve_token,
)

logger = logging.getLogger(__name__)


def _resolve_iteration_code(iteration: int | None) -> int:
    """
    Resolve the iteration Code used for the ITERATION condition.
    Priority: explicit argument > CODING_DEFAULT_ITERATION_CODE env var > module constant.
    """
    if iteration is not None:
        return int(iteration)
    env = os.environ.get(DEFAULT_ITERATION_ENV, "").strip()
    if env:
        return int(env)
    if DEFAULT_ITERATION_CODE is not None:
        return int(DEFAULT_ITERATION_CODE)
    raise ValueError(
        f"No iteration Code specified: pass iteration=... (see get_iteration_list_code_and_name for valid values), "
        f"or set the environment variable {DEFAULT_ITERATION_ENV}",
    )


def describe_iteration_list(
    project_name: str | None = None,
    *,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """DescribeIterationList: return the raw iteration list response for a project."""
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    return _request("DescribeIterationList", {"ProjectName": pn}, t, timeout=timeout)


def get_iteration_list_code_and_name(
    project_name: str | None = None,
    *,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    Fetch all iterations for a project, returning [{'code': int, 'name': str}, ...].
    The `code` in each returned item is the iteration Code required by describe_issue_list(iteration=...).
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    merged: list[dict[str, Any]] = []
    page = 1
    total_page = 1
    try:
        while page <= total_page:
            body: dict[str, Any] = {"ProjectName": pn}
            if page > 1:
                body["Page"] = page
            parsed = _request("DescribeIterationList", body, t, timeout=timeout)
            data = parsed["Response"]["Data"]
            total_page = int(data.get("TotalPage") or 1)
            for it in data.get("List") or []:
                merged.append({"code": it["Code"], "name": it["Name"]})
            page += 1
        return merged
    except (KeyError, TypeError) as e:
        logger.error("Failed to parse Code/Name from the iteration list\n%s", traceback.format_exc())
        raise CodingAPIError("Response is missing Data/List or Code/Name fields") from e
