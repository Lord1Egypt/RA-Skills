"""Coding 开放平台 Open API — 团队成员接口。"""

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
    DescribeTeamMembers：拉取全量团队成员，返回 [{'id': int, 'name': str}, ...]。
    返回项中的 id 可用作 describe_issue_list(assignee_ids=[...]) 的过滤条件。

    注意：部分 token 无 DescribeTeamMembers 权限，会抛出 CodingAPIError。
    替代方案：先调 describe_issue_list，再用 extract_members_from_issue_list 从 Assignees 字段反查成员 ID。
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
        logger.error("解析团队成员 Id/Name 失败\n%s", traceback.format_exc())
        raise CodingAPIError("响应中缺少 Data/TeamMembers 或 Id/Name 字段") from e
