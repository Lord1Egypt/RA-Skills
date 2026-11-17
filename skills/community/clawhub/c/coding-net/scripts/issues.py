"""Coding Open API — issue-related endpoints."""

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


# ── Internal helpers ────────────────────────────────────────────────────────

def _resolve_issue_status_type_filter(
    status_types: list[str] | None,
) -> frozenset[str] | None:
    """None → defaults to TODO and PROCESSING only; [] → no filter; non-empty → keep only the listed types."""
    if status_types is None:
        return frozenset({"TODO", "PROCESSING"})
    if not status_types:
        return None
    bad = [s for s in status_types if s not in _STATUS_TYPE_SET]
    if bad:
        raise ValueError(f"IssueStatusType only allows TODO/PROCESSING/COMPLETED, invalid values: {bad}")
    return frozenset(status_types)


def _filter_response_issue_list_by_issue_status_type(
    parsed: dict[str, Any],
    allowed: frozenset[str] | None,
) -> None:
    """Narrow Response.IssueList in place, keeping only issues whose IssueStatusType is in `allowed`."""
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
    """Trim a single DescribeIssueList item down to a summary. Assignees is the array of assignees, kept in full."""
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
    """Replace Response.IssueList with the trimmed-down structure (in place)."""
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
                f"BASE_ISSUE_TYPE only allows REQUIREMENT/DEFECT/MISSION, got: {base_issue_type!r}"
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


# ── Public API ────────────────────────────────────────────────────────────

def describe_defect_types(
    project_name: str | None = None,
    *,
    token: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    DescribeDefectTypes: return the project's list of defect types, [{'id': int, 'name': str}].
    Use issue_type_id= when creating a defect to specify the type.
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    parsed = _request("DescribeDefectTypes", {"ProjectName": pn}, t, timeout=timeout)
    try:
        types = parsed["Response"]["DefectTypes"]
    except (KeyError, TypeError) as e:
        logger.error("DescribeDefectTypes response is missing Response.DefectTypes\n%s", traceback.format_exc())
        raise CodingAPIError("Response is missing Response.DefectTypes") from e
    if not isinstance(types, list):
        raise CodingAPIError("Response.DefectTypes is not a list")
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
    CreateIssue: create a requirement, defect, or task, returning a summary of the newly created issue.

    :param name: issue title (required)
    :param issue_type: REQUIREMENT / DEFECT / MISSION
    :param priority: 0=Low 1=Medium 2=High(default) 3=Urgent
    :param assignee_id: assignee ID; can be looked up from the Assignees field returned by describe_issue_list
    :param iteration: iteration Code; falls back to the environment variable if omitted, and to no iteration if that's also unset
    :param start_date: start date, format 'YYYY-MM-DD' (required in some projects)
    :param due_date: due date, format 'YYYY-MM-DD' (required in some projects)
    :param label_ids: list of label IDs (required in some projects; missing value raises issue_project_label_required)
    :param working_hours: estimated hours (required in some projects; missing value raises working_hour_required)
    :param issue_type_id: issue category ID (e.g. the fixed ID for the defect category), not the defect subtype
    :param defect_type_id: defect subtype ID, from describe_defect_types; only applies when creating a defect
    :param custom_field_values: list of custom fields, format [{"Id": <IssueFieldId>, "Content": "<value>"}]
    :return: {Code, Name, IssueStatusName, AssigneeName, CreatorName}
    """
    t = _resolve_token(token)
    pn = _resolve_project_name(project_name)
    # The API requires Priority/AssigneeId/IterationCode to be passed as strings
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
        logger.error("CreateIssue response is missing Response.Issue\n%s", traceback.format_exc())
        raise CodingAPIError("Response is missing Response.Issue") from e
    if not isinstance(issue, dict):
        raise CodingAPIError("Response.Issue is not an object")
    return _summarize_issue_detail(issue)


def get_custom_fields_from_issues(
    project_name: str | None = None,
    *,
    issue_type: str = "REQUIREMENT",
    sample: int = 10,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """
    Infer the custom fields used by a project by sampling existing issues, returning [{"id": int, "name": str}].

    DescribeIssueCustomFieldsBoundToProject requires an elevated token scope; this function works around that.
    Should be called before creating an issue, so any required custom fields can be passed to
    create_issue(custom_field_values=...).
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
    Extract a deduplicated member list, [{'id': int, 'name': str}], from a describe_issue_list result.

    A fallback for when DescribeTeamMembers is not permitted: fetch the issue list first, then look up
    member IDs from the Assignees field. Compatible with both the summarized format ({"id": int, "name": str})
    and the raw format ({"Id": int, "Name": str}).
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
    Filter an issue list client-side (the IssueList returned by describe_issue_list).

    :param assignee_name: assignee name (fuzzy match, case-insensitive)
    :param assignee_id: assignee ID (exact match)
    :param iteration_code: iteration Code (exact match) — server-side filtering sometimes fails, so a re-filter is recommended
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
    DescribeIssue: look up a single issue by Code, returning a summarized set of fields.

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
        logger.error("DescribeIssue response is missing Response.Issue\n%s", traceback.format_exc())
        raise CodingAPIError("Response is missing Response.Issue") from e
    if not isinstance(issue, dict):
        raise CodingAPIError("Response.Issue is not an object") from None
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
    DescribeIssueList: query the list of issues in a project.

    Sorting is fixed to SortKey=PRIORITY/DESC; STATUS_TYPE is applied via local filtering.
    :param status_types: None → TODO/PROCESSING only; [] → no filter; other → the specified types.
    :return: contains Response.IssueList, each entry trimmed to a summary (see _summarize_issue_list_item).
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
    # Re-filter by iteration client-side (the server-side Conditions[ITERATION] filter sometimes fails)
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
