"""Coding Open API — team member endpoints."""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import Any

sys.path.insert(0, os.path.dirname(__file__))
from core import (  # noqa: E402
    CodingAPIError,
    DEFAULT_TIMEOUT,
    _request,
    _resolve_token,
)

logger = logging.getLogger(__name__)


def get_team_members_id_and_name(
    *,
    page_size: int = 500,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    DescribeTeamMembers: fetch all team members, returning [{'id': int, 'name': str}, ...].
    The `id` in each returned item can be used as a filter for describe_issue_list(assignee_ids=[...]).

    Note: some tokens lack the DescribeTeamMembers permission, which raises CodingAPIError.
    Fallback: call describe_issue_list first, then use extract_members_from_issue_list to look up
    member IDs from the Assignees field.
    """
    t = _resolve_token(token)
    merged: list[dict[str, Any]] = []
    page = 1
    total_count: int | None = None
    try:
        while True:
            parsed = _request(
                "DescribeTeamMembers",
                {"PageNumber": page, "PageSize": page_size},
                t,
                timeout=timeout,
            )
            data = parsed["Response"]["Data"]
            if total_count is None:
                total_count = int(data.get("TotalCount") or 0)
            for m in data.get("TeamMembers") or []:
                merged.append({"id": m["Id"], "name": m["Name"]})
            if total_count == 0 or len(merged) >= total_count:
                break
            if not data.get("TeamMembers"):
                break
            page += 1
        return merged
    except (KeyError, TypeError) as e:
        logger.error("Failed to parse Id/Name from team members\n%s", traceback.format_exc())
        raise CodingAPIError("Response is missing Data/TeamMembers or Id/Name fields") from e
