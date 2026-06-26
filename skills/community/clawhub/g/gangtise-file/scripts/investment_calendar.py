import os
import sys
from typing import Any, Dict, List, Optional

import datetime
import requests
from io import TextIOWrapper

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (  # noqa: E402
    GTS_AUTHORIZATION,
    ROADSHOW_LIST_URL,
    SITE_VISIT_LIST_URL,
    STRATEGY_MEETING_LIST_URL,
    FORUM_LIST_URL,
    FILE_DEFAULT_LIMIT,
    RESEARCH_AREA_MAP,
    INSTITUTIONS_MAP,
    format_response,
    match_best,
    remove_html_tags,
    check_version,
)

KIND_URL: Dict[str, str] = {
    "roadshow": ROADSHOW_LIST_URL,
    "site_visit": SITE_VISIT_LIST_URL,
    "strategy_meeting": STRATEGY_MEETING_LIST_URL,
    "forum": FORUM_LIST_URL,
}

KIND_TYPE_LABEL = {
    "roadshow": "路演",
    "site_visit": "调研",
    "strategy_meeting": "线下策略会",
    "forum": "论坛",
}


def _format_time_range(start_date: Optional[str] = None, end_date: Optional[str] = None):
    start_timestamp = None
    end_timestamp = None
    if start_date:
        start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
    if end_date:
        end_timestamp = int(
            (datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).timestamp() * 1000
        ) - 1
    return start_timestamp, end_timestamp


def _ts_str(ts: Any) -> str:
    if isinstance(ts, (int, float)) and ts and len(str(ts)) == 13:
        return datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(ts, (int, float)) and ts and len(str(ts)) == 10:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(ts, str) and ts:
        return ts
    return ts or ""


def _time_window_display(start_ms: Any, end_ms: Any) -> str:
    s = _ts_str(start_ms)
    e = _ts_str(end_ms)
    if s and e:
        return f"{s} ~ {e}"
    return s or e or ""


def _join_securities(sec_list: Any) -> str:
    parts: List[str] = []
    for s in sec_list or []:
        if not isinstance(s, dict):
            continue
        c = (s.get("securityCode") or "").strip()
        n = (s.get("securityName") or "").strip()
        if c and n:
            parts.append(f"{n}({c})")
        elif c:
            parts.append(c)
        elif n:
            parts.append(n)
    return "、".join(parts)


def _join_institutions(objs: Any) -> str:
    parts: List[str] = []
    for x in objs or []:
        if not isinstance(x, dict):
            continue
        iid = (x.get("institutionId") or "").strip()
        name = (x.get("institutionName") or "").strip()
        if name and iid:
            parts.append(f"{name}({iid})")
        elif name:
            parts.append(name)
        elif iid:
            parts.append(iid)
    return "、".join(parts)


def _join_ra_concept(objs: Any, id_key: str, name_key: str) -> str:
    parts: List[str] = []
    for x in objs or []:
        if not isinstance(x, dict):
            continue
        rid = (x.get(id_key) or "").strip()
        name = (x.get(name_key) or "").strip()
        if name and rid:
            parts.append(f"{name}({rid})")
        elif name:
            parts.append(name)
        elif rid:
            parts.append(rid)
    return "、".join(parts)


def _perm_label(p: Any) -> str:
    if p == 1:
        return "公开"
    if p == 2:
        return "私密"
    if p is None:
        return ""
    return str(p)


def _format_participant_company(pcs: Any) -> str:
    if not isinstance(pcs, list):
        return ""
    lines: List[str] = []
    for g in pcs:
        if not isinstance(g, dict):
            continue
        grp = (g.get("participantGroup") or "").strip()
        for d in g.get("participantDetail") or []:
            if not isinstance(d, dict):
                continue
            name = (d.get("participantName") or "").strip()
            remark = (d.get("participantRemark") or "").strip()
            if not name and not remark:
                continue
            piece = f"{grp}/{name}" if grp else name
            if remark:
                piece += f"({remark})"
            lines.append(piece)
    return "；".join(lines)


def _format_row(kind: str, row: dict) -> dict:
    start_ms = row.get("startTime")
    end_ms = row.get("endTime")
    file_time = _time_window_display(start_ms, end_ms)
    type_label = KIND_TYPE_LABEL[kind]

    if kind == "roadshow":
        rid = str(row.get("roadshowId") or "")
        item = {
            "标题": remove_html_tags(row.get("title") or ""),
            "文件时间": file_time,
            "简介": remove_html_tags(row.get("abstractInfo") or ""),
            "路演类型": row.get("category") or "",
            "关联证券": _join_securities(row.get("securityList")),
            "牵头机构": _join_institutions(row.get("institutionList")),
            "联系方式": row.get("contact") or "",
            "研究方向": _join_ra_concept(row.get("researchAreaList"), "researchAreaId", "researchAreaName"),
            "概念": _join_ra_concept(row.get("conceptList"), "conceptId", "conceptName"),
            "参会人员": row.get("participant") or "",
            "参会角色": "、".join(row.get("participantRoleList") or []) if isinstance(row.get("participantRoleList"), list) else "",
            "地点": row.get("location") or "",
            "行程": (row.get("schedulePlan") or "").replace("\n", " / "),
            "权限": _perm_label(row.get("permission")),
            "类型": type_label,
            "类型中ID": rid,
        }
        return item

    if kind == "site_visit":
        rid = str(row.get("siteVisitId") or "")
        item = {
            "标题": remove_html_tags(row.get("title") or ""),
            "文件时间": file_time,
            "简介": remove_html_tags(row.get("abstractInfo") or ""),
            "调研类型": row.get("object") or "",
            "调研形式": row.get("category") or "",
            "关联证券": _join_securities(row.get("securityList")),
            "牵头机构": _join_institutions(row.get("institutionList")),
            "联系方式": row.get("contact") or "",
            "研究方向": _join_ra_concept(row.get("researchAreaList"), "researchAreaId", "researchAreaName"),
            "概念": _join_ra_concept(row.get("conceptList"), "conceptId", "conceptName"),
            "参会人员": row.get("participant") or "",
            "地点": row.get("location") or "",
            "行程": (row.get("schedulePlan") or "").replace("\n", " / "),
            "权限": _perm_label(row.get("permission")),
            "类型": type_label,
            "类型中ID": rid,
        }
        return item

    if kind == "strategy_meeting":
        rid = str(row.get("strategyMeetingId") or "")
        item = {
            "标题": remove_html_tags(row.get("title") or ""),
            "文件时间": file_time,
            "牵头机构": _join_institutions(row.get("institutionList")),
            "参会公司": _format_participant_company(row.get("participantCompany")),
            "报名链接": row.get("registrationUrl") or "",
            "地点": row.get("location") or "",
            "类型": type_label,
            "类型中ID": rid,
        }
        return item

    # forum
    rid = str(row.get("forumId") or "")
    item = {
        "标题": remove_html_tags(row.get("title") or ""),
        "文件时间": file_time,
        "研究方向": _join_ra_concept(row.get("researchAreaList"), "researchAreaId", "researchAreaName"),
        "地点": row.get("location") or "",
        "类型": type_label,
        "类型中ID": rid,
    }
    return item


def _resolve_research_areas(raw_list: Optional[List[str]]) -> List[str]:
    if not raw_list:
        return []
    id_set = {str(v) for v in RESEARCH_AREA_MAP.values()}
    results: List[str] = []
    for raw in raw_list:
        if not raw:
            continue
        s = raw.strip()
        if s in id_set:
            if s not in results:
                results.append(s)
            continue
        m = match_best(s, list(RESEARCH_AREA_MAP.keys()))
        if m:
            sid = str(RESEARCH_AREA_MAP[m])
            if sid not in results:
                results.append(sid)
    return results


def _resolve_institutions(institutions: Optional[List[str]]) -> List[str]:
    if not institutions:
        return []
    results: List[str] = []
    for institution in institutions:
        result = match_best(institution, INSTITUTIONS_MAP.keys())
        if result and result not in results:
            results.append(str(INSTITUTIONS_MAP[result]))
    return results


def _fetch_list(url: str, headers: dict, payload_base: dict, keyword: str, limit: int, kind: str) -> tuple:
    max_page_size = 50
    all_results: List[dict] = []
    offset = 0
    remaining = limit

    while remaining > 0:
        page_size = min(remaining, max_page_size)
        data = {**payload_base, "from": offset, "size": page_size}
        if keyword:
            data["keyword"] = keyword
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            if all_results:
                return all_results, response.text.replace("\n", " ").replace("\r", " ").strip()
            return None, response.text.replace("\n", " ").replace("\r", " ").strip()
        result = response.json()
        # TODO 目前有bug，临时组装一下
        result = {
            "data": result
        }

        if result.get("code", 200) not in [200, "000000"] and result.get("status", True) is not True:
            return None, result.get("msg", "请求失败").replace("\n", " ").replace("\r", " ").strip()

        report_data = result.get("data") or {}
        rows = report_data.get("list") or []
        if not rows:
            break

        for row in rows:
            all_results.append(_format_row(kind, row))

        if len(rows) < page_size:
            break

        offset += page_size
        remaining -= len(rows)

    return all_results, None


def _build_payload(
    kind: str,
    start_timestamp: Optional[int],
    end_timestamp: Optional[int],
    securities: Optional[List[str]],
    institution_ids: Optional[List[str]],
    research_area_ids: Optional[List[str]],
    category_list: Optional[List[str]],
    market_list: Optional[List[str]],
    participant_role_list: Optional[List[str]],
    broker_type_list: Optional[List[str]],
    permission_list: Optional[List[int]],
    object_list: Optional[List[str]],
) -> dict:
    payload: dict = {}
    if start_timestamp is not None:
        payload["startTime"] = start_timestamp
    if end_timestamp is not None:
        payload["endTime"] = end_timestamp

    if kind == "roadshow":
        if institution_ids:
            payload["institutionList"] = institution_ids
        if research_area_ids:
            payload["researchAreaList"] = research_area_ids
        if securities:
            payload["securityList"] = [s.upper() for s in securities]
        if category_list:
            payload["categoryList"] = [str(x).strip() for x in category_list if str(x).strip()]
        if market_list:
            payload["marketList"] = [str(x).strip() for x in market_list if str(x).strip()]
        if participant_role_list:
            payload["participantRoleList"] = [str(x).strip() for x in participant_role_list if str(x).strip()]
        if broker_type_list:
            payload["brokerTypeList"] = [str(x).strip() for x in broker_type_list if str(x).strip()]
        if permission_list:
            payload["permission"] = permission_list
        return payload

    if kind == "site_visit":
        if institution_ids:
            payload["institutionList"] = institution_ids
        if research_area_ids:
            payload["researchAreaList"] = research_area_ids
        if securities:
            payload["securityList"] = [s.upper() for s in securities]
        if object_list:
            payload["objectList"] = [str(x).strip() for x in object_list if str(x).strip()]
        if category_list:
            payload["categoryList"] = [str(x).strip() for x in category_list if str(x).strip()]
        if market_list:
            payload["marketList"] = [str(x).strip() for x in market_list if str(x).strip()]
        if permission_list:
            payload["permission"] = permission_list
        return payload

    if kind == "strategy_meeting":
        if institution_ids:
            payload["institutionList"] = institution_ids
        return payload

    # forum
    if securities:
        payload["securityList"] = [s.upper() for s in securities]
    if research_area_ids:
        payload["researchAreaList"] = research_area_ids
    return payload


def calendar_finder(
    kind: str,
    keyword: str = "",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = FILE_DEFAULT_LIMIT["calendar"],
    securities: Optional[List[str]] = None,
    institutions: Optional[List[str]] = None,
    research_areas: Optional[List[str]] = None,
    category_list: Optional[List[str]] = None,
    market_list: Optional[List[str]] = None,
    participant_role_list: Optional[List[str]] = None,
    broker_type_list: Optional[List[str]] = None,
    permission_list: Optional[List[int]] = None,
    object_list: Optional[List[str]] = None,
):
    try:
        kind = (kind or "").strip().lower().replace("-", "_")
        if kind not in KIND_URL:
            return format_response(
                {"state": "error", "message": f"不支持的日程类型：{kind}，可选：roadshow, site_visit, strategy_meeting, forum", "data": []},
                "calendar",
            )

        url = KIND_URL[kind]
        headers = {"Authorization": GTS_AUTHORIZATION}

        research_area_ids = _resolve_research_areas(research_areas) if research_areas else []
        institution_ids = _resolve_institutions(institutions) if institutions else []

        start_timestamp, end_timestamp = _format_time_range(start_date, end_date)

        payload_base = _build_payload(
            kind,
            start_timestamp,
            end_timestamp,
            securities,
            institution_ids,
            research_area_ids,
            category_list,
            market_list,
            participant_role_list,
            broker_type_list,
            permission_list,
            object_list,
        )

        keyword_str = (keyword or "").strip()

        all_results, err = _fetch_list(url, headers, payload_base, keyword_str, limit, kind)
        part_error_message = ""
        if err and not all_results:
            return format_response({"state": "error", "message": err}, "calendar")
        if err and all_results:
            part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results:
            return format_response(
                {"state": "error", "message": "未找到相关日程，建议修改查询条件", "data": []},
                "calendar",
            )

        all_results = all_results[:limit]

        response_data = {
            "state": "success",
            "message": "已找到相关日程",
            "data": [{"data": all_results, "module": "calendar", "type": "files"}],
        }
        return format_response(response_data, "calendar", additional_message=part_error_message or "")
    except Exception as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "calendar",
        )


def _parse_str_list(raw: str) -> Optional[List[str]]:
    if not raw:
        return None
    items = [x.strip() for x in raw.replace("，", ",").split(",") if x.strip()]
    return items or None


def _parse_int_list(raw: str) -> Optional[List[int]]:
    if not raw:
        return None
    out: List[int] = []
    for x in raw.replace("，", ",").split(","):
        x = x.strip()
        if not x:
            continue
        try:
            out.append(int(x))
        except ValueError:
            continue
    return out or None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="投研日程检索：路演、调研、线下策略会、论坛（四合一，通过 -t/--type 指定）。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--type",
        required=True,
        choices=["roadshow", "site_visit", "strategy_meeting", "forum"],
        dest="schedule_type",
        help="日程类型：roadshow 路演；site_visit 调研；strategy_meeting 线下策略会；forum 论坛",
    )
    parser.add_argument("-k", "--keyword", default="", help="搜索关键词，可为空")
    parser.add_argument("-sd", "--start_date", default="", help="开始日期 YYYY-MM-DD")
    parser.add_argument("-ed", "--end_date", default="", help="结束日期 YYYY-MM-DD")
    parser.add_argument("-l", "--limit", default=FILE_DEFAULT_LIMIT["calendar"], type=int, help="返回条数上限")
    parser.add_argument("--securities", default="", help="证券代码，逗号分隔（forum / roadshow / site_visit）")
    parser.add_argument("--institutions", default="", help="牵头机构名称，逗号分隔（roadshow / site_visit / strategy_meeting）")
    parser.add_argument(
        "--research_areas",
        default="",
        help="研究方向：宏观/策略/固收/金工/海外 或研究方向 ID，逗号分隔（roadshow / site_visit / forum）",
    )
    parser.add_argument(
        "--category_list",
        default="",
        help="roadshow：路演类型 earningsCall 等；site_visit：调研形式 single/series",
    )
    parser.add_argument(
        "--object_list",
        default="",
        help="仅 site_visit：调研类型 company / industry",
    )
    parser.add_argument(
        "--market_list",
        default="",
        help="roadshow / site_visit：市场 aShares,hkStocks,usChinaConcept,usStocks",
    )
    parser.add_argument(
        "--participant_role_list",
        default="",
        help="仅 roadshow：参会人标识 management / expert",
    )
    parser.add_argument(
        "--broker_type_list",
        default="",
        help="仅 roadshow：卖方类型 cnBroker / otherBroker",
    )
    parser.add_argument(
        "--permission",
        default="",
        help="roadshow / site_visit：权限 1 公开 2 私密，逗号分隔，如 1 或 1,2",
    )

    args = parser.parse_args()

    securities = _parse_str_list(args.securities)
    institutions = _parse_str_list(args.institutions)
    research_areas = _parse_str_list(args.research_areas)
    category_list = _parse_str_list(args.category_list)
    object_list = _parse_str_list(args.object_list)
    market_list = _parse_str_list(args.market_list)
    participant_role_list = _parse_str_list(args.participant_role_list)
    broker_type_list = _parse_str_list(args.broker_type_list)
    permission_list = _parse_int_list(args.permission)

    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")

    out = calendar_finder(
        kind=args.schedule_type,
        keyword=args.keyword or "",
        start_date=args.start_date or None,
        end_date=args.end_date or None,
        limit=int(args.limit),
        securities=securities,
        institutions=institutions,
        research_areas=research_areas,
        category_list=category_list,
        market_list=market_list,
        participant_role_list=participant_role_list,
        broker_type_list=broker_type_list,
        permission_list=permission_list,
        object_list=object_list,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
