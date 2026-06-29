"""Coding 开放平台 Open API — 迭代相关接口。"""

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
    解析 ITERATION 条件用的迭代 Code。
    优先级：显式参数 > 环境变量 CODING_DEFAULT_ITERATION_CODE > 模块常量。
    """
    if iteration is not None:
        return int(iteration)
    env = os.environ.get(DEFAULT_ITERATION_ENV, "").strip()
    if env:
        return int(env)
    if DEFAULT_ITERATION_CODE is not None:
        return int(DEFAULT_ITERATION_CODE)
    raise ValueError(
        f"未指定迭代 Code：请传 iteration=（取值见 get_iteration_list_code_and_name），"
        f"或设置环境变量 {DEFAULT_ITERATION_ENV}",
    )


def describe_iteration_list(
    project_name: str | None = None,
    *,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """DescribeIterationList：返回项目下的原始迭代列表响应。"""
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
    获取项目下全量迭代，返回 [{'code': int, 'name': str}, ...]。
    返回项中的 code 即 describe_issue_list(iteration=...) 所需的迭代 Code。
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
        logger.error("解析迭代列表 Code/Name 失败\n%s", traceback.format_exc())
        raise CodingAPIError("响应中缺少 Data/List 或 Code/Name 字段") from e
