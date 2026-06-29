"""Coding 开放平台 Open API — 事项相关接口。"""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import Any, Literal

sys.path.insert(0, os.path.dirname(__file__))
from core import (  # noqa: E402
    CodingAPIError,
    DEFAULT_TIMEOUT,
    _request,
    _resolve_project_name,
    _resolve_token,
)
from iterations import _resolve_iteration_code  # noqa: E402

logger = logging.getLogger(__name__)

_STATUS_TYPE_SET = frozenset({"TODO", "PROCESSING", "COMPLETED"})
_BASE_ISSUE_TYPE_SET = frozenset({"REQUIREMENT", "DEFECT", "MISSION"})


# ── 内部辅助 ──────────────────────────────────────────────────────────────────

def _resolve_issue_status_type_filter(
    status_types: list[str] | None,
) -> frozenset[str] | None:
    """None → 默认仅 TODO、PROCESSING；[] → 不过滤；非空 → 仅保留列出的类型。"""
    if status_types is None:
        return frozenset({"TODO", "PROCESSING"})
    if not status_types:
        return None
    bad = [s for s in status_types if s not in _STATUS_TYPE_SET]
    if bad:
        raise ValueError(f"IssueStatusType 仅允许 TODO/PROCESSING/COMPLETED，无效项: {bad}")
    return frozenset(status_types)


def _filter_response_issue_list_by_issue_status_type(
    parsed: dict[str, Any],
    allowed: frozenset[str] | None,
) -> None:
    """就地缩小 Response.IssueList，仅保留 IssueStatusType 在 allowed 内的事项。"""
    if allowed is None:
        return
    resp = parsed.get("Response")
    if not isinstance(resp, dict):
        return
    issues = resp.get("IssueList")
    if not isinstance(issues, list):
        return
    resp["IssueList"] = [
        item for item in issues
        if isinstance(item, dict) and item.get("IssueStatusType") in allowed
    ]


def _summarize_issue_list_item(raw: dict[str, Any]) -> dict[str, Any]:
    """DescribeIssueList 单条事项精简字段。Assignees 是处理人数组，保留完整。"""
    assignees = [
        {"id": m.get("Id"), "name": str(m.get("Name") or "")}
        for m in (raw.get("Assignees") or [])
        if isinstance(m, dict)
    ]
    iter_info = raw.get("Iteration") or {}
    custom = raw.get("CustomFields") or []
    return {
        "Code": raw.get("Code"),
        "Name": raw.get("Name"),
        "Type": raw.get("Type"),
        "IssueStatusName": raw.get("IssueStatusName"),
        "IssueStatusType": raw.get("IssueStatusType"),
        "Priority": raw.get("Priority"),
        "Assignees": assignees,          # [{"id": int, "name": str}, ...]
        "IterationCode": iter_info.get("Code"),
        "IterationName": iter_info.get("Name"),
        "StartDate": raw.get("StartDate"),
        "DueDate": raw.get("DueDate"),
        "CustomFields": custom,
    }


def _summarize_response_issue_list(parsed: dict[str, Any]) -> None:
    """将 Response.IssueList 替换为精简结构（就地）。"""
    resp = parsed.get("Response")
    if not isinstance(resp, dict):
        return
    issues = resp.get("IssueList")
    if not isinstance(issues, list):
        return
    resp["IssueList"] = [
        _summarize_issue_list_item(item) for item in issues if isinstance(item, dict)
    ]


def _build_issue_list_conditions(
    *,
    assignee_ids: list[int] | None,
    iteration: int | None,
    base_issue_type: str | None,
) -> list[dict[str, Any]]:
    conds: list[dict[str, Any]] = []
    if assignee_ids:
        conds.append({"key": "ASSIGNEE", "value": [int(x) for x in assignee_ids]})
    conds.append({"key": "ITERATION", "value": [_resolve_iteration_code(iteration)]})
    if base_issue_type is not None:
        if base_issue_type not in _BASE_ISSUE_TYPE_SET:
            raise ValueError(
                f"BASE_ISSUE_TYPE 仅允许 REQUIREMENT/DEFECT/MISSION，收到: {base_issue_type!r}"
            )
        conds.append({"key": "BASE_ISSUE_TYPE", "value": base_issue_type})
    return conds


def _issue_detail_person_name(obj: Any) -> str:
    if isinstance(obj, dict):
        return str(obj.get("Name") or "")
    return ""


def _summarize_issue_detail(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "Name": issue.get("Name"),
        "Description": issue.get("Description"),
        "IssueStatusName": issue.get("IssueStatusName"),
        "AssigneeName": _issue_detail_person_name(issue.get("Assignee")),
        "CreatorName": _issue_detail_person_name(issue.get("Creator")),
    }


# ── 公开接口 ──────────────────────────────────────────────────────────────────

def describe_defect_types(
    project_name: str | None = None,
    *,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    DescribeDefectTypes：返回项目下缺陷类型列表 [{'id': int, 'name': str}]。
    创建缺陷时可通过 issue_type_id= 指定类型。
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    parsed = _request("DescribeDefectTypes", {"ProjectName": pn}, t, timeout=timeout)
    try:
        types = parsed["Response"]["DefectTypes"]
    except (KeyError, TypeError) as e:
        logger.error("DescribeDefectTypes 响应缺少 Response.DefectTypes\n%s", traceback.format_exc())
        raise CodingAPIError("响应中缺少 Response.DefectTypes") from e
    if not isinstance(types, list):
        raise CodingAPIError("Response.DefectTypes 不是列表")
    return [{"id": item.get("Id"), "name": item.get("Name")} for item in types if isinstance(item, dict)]


def create_issue(
    project_name: str | None = None,
    *,
    name: str,
    issue_type: Literal["REQUIREMENT", "DEFECT", "MISSION"] = "REQUIREMENT",
    description: str = "",
    priority: int = 2,
    assignee_id: int | None = None,
    iteration: int | None = None,
    start_date: str | None = None,
    due_date: str | None = None,
    label_ids: list[int] | None = None,
    working_hours: float | None = None,
    issue_type_id: int | None = None,
    defect_type_id: int | None = None,
    custom_field_values: list[dict] | None = None,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    CreateIssue：创建需求、缺陷或任务，返回新建事项的精简信息。

    :param name: 事项标题（必填）
    :param issue_type: REQUIREMENT / DEFECT / MISSION
    :param priority: 0=低 1=中 2=高(默认) 3=紧急
    :param assignee_id: 处理人 ID，可从 describe_issue_list 返回的 Assignees 字段反查
    :param iteration: 迭代 Code；省略时读环境变量，仍无则不关联迭代
    :param start_date: 开始日期，格式 'YYYY-MM-DD'（部分项目必填）
    :param due_date: 截止日期，格式 'YYYY-MM-DD'（部分项目必填）
    :param label_ids: 标签 ID 列表（部分项目必填，缺失报 issue_project_label_required）
    :param working_hours: 预估工时，单位小时（部分项目必填，缺失报 working_hour_required）
    :param issue_type_id: 事项大类 ID（如缺陷大类固定 ID），非缺陷子类型
    :param defect_type_id: 缺陷子类型 ID，来自 describe_defect_types；仅创建缺陷时有效
    :param custom_field_values: 自定义字段列表，格式 [{"Id": <IssueFieldId>, "Content": "<值>"}]
    :return: {Code, Name, IssueStatusName, AssigneeName, CreatorName}
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    # API 要求 Priority/AssigneeId/IterationCode 传字符串类型
    body: dict[str, Any] = {
        "ProjectName": pn,
        "Name": name,
        "Type": issue_type,
        "Priority": str(priority),
    }
    if description:
        body["Description"] = description
    if assignee_id is not None:
        body["AssigneeId"] = str(assignee_id)
    try:
        body["IterationCode"] = str(_resolve_iteration_code(iteration))
    except ValueError:
        pass  # iteration is optional when creating
    if start_date is not None:
        body["StartDate"] = start_date
    if due_date is not None:
        body["DueDate"] = due_date
    if label_ids:
        body["LabelIds"] = [int(x) for x in label_ids]
    if working_hours is not None:
        body["WorkingHours"] = float(working_hours)
    if issue_type_id is not None:
        body["IssueTypeId"] = int(issue_type_id)
    if defect_type_id is not None:
        body["DefectTypeId"] = int(defect_type_id)
    if custom_field_values:
        body["CustomFieldValues"] = custom_field_values

    parsed = _request("CreateIssue", body, t, timeout=timeout)
    try:
        issue = parsed["Response"]["Issue"]
    except (KeyError, TypeError) as e:
        logger.error("CreateIssue 响应缺少 Response.Issue\n%s", traceback.format_exc())
        raise CodingAPIError("响应中缺少 Response.Issue") from e
    if not isinstance(issue, dict):
        raise CodingAPIError("Response.Issue 不是对象")
    return _summarize_issue_detail(issue)


def get_custom_fields_from_issues(
    project_name: str | None = None,
    *,
    issue_type: str = "REQUIREMENT",
    sample: int = 10,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """
    通过采样现有事项推断项目中使用的自定义字段，返回 [{"id": int, "name": str}]。

    DescribeIssueCustomFieldsBoundToProject 需要更高 token scope，此函数绕开该限制。
    创建事项前应先调用，以便将必填自定义字段一并传入 create_issue(custom_field_values=...)。
    """
    result = describe_issue_list(
        project_name, issue_type=issue_type, limit=str(sample),
        status_types=[], token=token,
    )
    seen: dict[int, str] = {}
    for it in (result.get("Response") or {}).get("IssueList") or []:
        for cf in (it.get("CustomFields") or []):
            fid = cf.get("Id")
            if fid is not None and fid not in seen:
                seen[fid] = cf.get("Name", "")
    return [{"id": fid, "name": name} for fid, name in seen.items()]


def extract_members_from_issue_list(issues_result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    从 describe_issue_list 返回结果中提取去重成员列表 [{'id': int, 'name': str}]。

    用于 DescribeTeamMembers 无权限时的替代方案：先拉取事项列表，再从 Assignees 字段反查成员 ID。
    兼容摘要格式（{"id": int, "name": str}）和原始格式（{"Id": int, "Name": str}）。
    """
    seen: dict[int, str] = {}
    issues = (issues_result.get("Response") or {}).get("IssueList") or []
    for issue in issues:
        for a in (issue.get("Assignees") or []):
            if not isinstance(a, dict):
                continue
            uid = a.get("id") if "id" in a else a.get("Id")
            name = a.get("name") or a.get("Name") or ""
            if uid is not None:
                seen[int(uid)] = name
    return sorted([{"id": uid, "name": name} for uid, name in seen.items()], key=lambda x: x["name"])


def filter_issues(
    items: list[dict[str, Any]],
    *,
    assignee_name: str | None = None,
    assignee_id: int | None = None,
    iteration_code: int | None = None,
) -> list[dict[str, Any]]:
    """
    客户端过滤事项列表（describe_issue_list 返回的 IssueList）。

    :param assignee_name: 处理人姓名（模糊匹配，不区分大小写）
    :param assignee_id: 处理人 ID（精确匹配）
    :param iteration_code: 迭代 Code（精确匹配）——API 侧过滤有时失效，建议二次过滤
    """
    result = []
    for it in items:
        if iteration_code is not None and it.get("IterationCode") != iteration_code:
            continue
        if assignee_id is not None or assignee_name is not None:
            matched = False
            for a in (it.get("Assignees") or []):
                if assignee_id is not None and a.get("id") == assignee_id:
                    matched = True; break
                if assignee_name is not None and assignee_name.lower() in (a.get("name") or "").lower():
                    matched = True; break
            if not matched:
                continue
        result.append(it)
    return result


def describe_issue(
    project_name: str | None = None,
    issue_code: int = 0,
    *,
    show_image_out_url: bool = True,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    DescribeIssue：按事项 Code 查询单条事项详情，返回精简字段。

    :return: {Name, Description, IssueStatusName, AssigneeName, CreatorName}
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    parsed = _request(
        "DescribeIssue",
        {"ProjectName": pn, "IssueCode": int(issue_code), "ShowImageOutUrl": show_image_out_url},
        t,
        timeout=timeout,
    )
    try:
        issue = parsed["Response"]["Issue"]
    except (KeyError, TypeError) as e:
        logger.error("DescribeIssue 响应缺少 Response.Issue\n%s", traceback.format_exc())
        raise CodingAPIError("响应中缺少 Response.Issue") from e
    if not isinstance(issue, dict):
        raise CodingAPIError("Response.Issue 不是对象") from None
    return _summarize_issue_detail(issue)


def describe_issue_list(
    project_name: str | None = None,
    *,
    issue_type: str = "ALL",
    limit: str = "2000",
    assignee_ids: list[int] | None = None,
    iteration: int | None = None,
    status_types: list[str] | None = None,
    base_issue_type: Literal["REQUIREMENT", "DEFECT", "MISSION"] | None = None,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    DescribeIssueList：查询项目下事项列表。

    排序固定为 SortKey=PRIORITY/DESC；STATUS_TYPE 由本地过滤实现。
    :param status_types: None → 仅 TODO/PROCESSING；[] → 不过滤；其他 → 指定类型。
    :return: 含 Response.IssueList，每条仅含精简字段（见 _summarize_issue_list_item）。
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    allowed_status = _resolve_issue_status_type_filter(status_types)
    conditions = _build_issue_list_conditions(
        assignee_ids=assignee_ids, iteration=iteration, base_issue_type=base_issue_type,
    )
    body: dict[str, Any] = {
        "ProjectName": pn,
        "IssueType": issue_type,
        "Limit": limit,
        "Conditions": conditions,
        "SortKey": "PRIORITY",
        "SortValue": "DESC",
        "ShowImageOutUrl": False,
    }
    parsed = _request("DescribeIssueList", body, t, timeout=timeout)
    _filter_response_issue_list_by_issue_status_type(parsed, allowed_status)
    # 客户端二次过滤迭代（API 侧 Conditions[ITERATION] 有时失效）
    if iteration is not None:
        iter_code = _resolve_iteration_code(iteration)
        resp = parsed.get("Response", {})
        raw_list = resp.get("IssueList") or []
        resp["IssueList"] = [
            it for it in raw_list
            if (it.get("Iteration") or {}).get("Code") == iter_code
        ]
    _summarize_response_issue_list(parsed)
    return parsed
