import os
import sys
from typing import List, Optional
import datetime
import requests
from io import TextIOWrapper
import locale

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (  # noqa: E402
    GTS_AUTHORIZATION,
    SUMMARY_URL,
    FILE_DEFAULT_LIMIT,
    INDUSTRIES_MAP,
    INSTITUTIONS_MAP,
    RESEARCH_AREA_MAP,
    format_response,
    match_best,
    remove_html_tags,
    check_version,
)
from get_file import download_files

SUMMARY_SOURCE_MAP = {
    "会议平台": 1,
    "网络资源": 3,
    "公司公告": 2,
}

SUMMARY_MARKET_CODE_MAP = {
    "A股": "aShares",
    "港股": "hkStocks",
    "美股中概": "usChinaConcept",
    "美股": "usStocks",
}

SUMMARY_PARTICIPANT_ROLE_CODE_MAP = {
    "高管": "management",
    "专家": "expert",
}

SUMMARY_CATEGORY_CODE_MAP = {
    "业绩会": "earningsCall",
    "策略会": "strategyMeeting",
    "基金路演": "fundRoadshow",
    "股东大会": "shareholdersMeeting",
    "并购会议": "maMeeting",
    "特别会议": "specialMeeting",
    "公司分析": "companyAnalysis",
    "行业分析": "industryAnalysis",
    "其他": "other",
}


def _format_time_range(start_date: str = None, end_date: str = None):
    start_timestamp = None
    end_timestamp = None
    if start_date:
        start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
    if end_date:
        end_timestamp = int(
            (datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).timestamp() * 1000
        ) - 1
    return start_timestamp, end_timestamp


def _format_summary_item(summaries: List[dict]) -> List[dict]:
    _results = []
    for summary in summaries:
        summ_time = summary.get("publishTime") or summary.get("summaryTime")
        file_time = ""
        if summ_time and len(str(summ_time)) == 13:
            file_time = datetime.datetime.fromtimestamp(summ_time / 1000).strftime("%Y-%m-%d %H:%M:%S")
        elif summ_time and len(str(summ_time)) == 10:
            file_time = datetime.datetime.fromtimestamp(summ_time).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(summ_time, str) and summ_time:
            file_time = summ_time

        security_items = summary.get("securityList") or summary.get("stock") or []
        stock_display_parts: List[str] = []
        for s in security_items:
            if not isinstance(s, dict):
                continue
            code = s.get("securityCode") or s.get("gtsCode") or ""
            name = s.get("securityName") or s.get("scrAbbr") or ""
            if code:
                display = f"{name}({code})" if name else f"({code})"
                if display not in stock_display_parts:
                    stock_display_parts.append(display)
        stock_display = ", ".join(stock_display_parts)

        institution_items = summary.get("institutionList") or summary.get("initiator") or []
        initiator_display_parts: List[str] = []
        for i in institution_items:
            if not isinstance(i, dict):
                continue
            name = i.get("institutionName") or i.get("cnName") or i.get("partyName") or ""
            if name and name not in initiator_display_parts:
                initiator_display_parts.append(name)
        initiator_display = ", ".join(initiator_display_parts)

        essences = summary.get("essence") or []
        sentiment_map = {
            1: "正面",
            "1": "正面",
            0: "中性",
            "0": "中性",
            -1: "负面",
            "-1": "负面",
        }
        
        if essences:
            essence_display = "; ".join(
                "(" + sentiment_map.get(e.get("sentiment"), "中性") + ")"
                + (e.get("brief", "") or "")
                + ": "
                + (e.get("content", "") or "")
                for e in sorted(essences, key=lambda x: x.get("sort", 0))
                if isinstance(e, dict)
            )
        else:
            essence_display = ""

        category_list = summary.get("categoryList") or []
        category_display = ", ".join([str(x) for x in category_list if x]) if isinstance(category_list, list) else ""

        market_list = summary.get("marketList") or []
        market_display = ", ".join([str(x) for x in market_list if x]) if isinstance(market_list, list) else ""

        participant_role_list = summary.get("participantRoleList") or []
        participant_role_display = (
            ", ".join([str(x) for x in participant_role_list if x]) if isinstance(participant_role_list, list) else ""
        )

        source_display = summary.get("sourceName")
        if not source_display:
            source_display = str(summary.get("source") or "")

        item = {
            "标题": remove_html_tags(summary.get("translatedTitle") or summary.get("title", "")),
            "文件时间": file_time,
            "来源": source_display,
            "分类": category_display or summary.get("category", ""),
            "发起方": initiator_display,
            "嘉宾": summary.get("guest", "") or "",
            "摘要": remove_html_tags((summary.get("translatedBrief") or summary.get("brief", "") or "") + ("..." if (summary.get("translatedBrief") or summary.get("brief")) else "")),
            "关联股票": stock_display,
            "纪要精华": essence_display,
            "市场": market_display,
            "参会人角色": participant_role_display,
            "类型": "会议纪要",
            "类型中ID": str(summary.get("summaryId") or summary.get("id", "")),
        }
        _results.append(item)
    return _results


def _resolve_industries(industries: List[str]) -> List[str]:
    if not industries:
        return []
    all_industries = {}
    for key, value in INDUSTRIES_MAP.items():
        all_industries.update(value.copy())
    all_industries.update(RESEARCH_AREA_MAP.copy())
    results = []
    for industry in industries:
        result = match_best(industry, all_industries.keys())
        if result and result not in results:
            results.append(str(all_industries[result]))
    return results


def _resolve_institutions(institutions: List[str]) -> List[str]:
    if not institutions:
        return []
    results = []
    for institution in institutions:
        result = match_best(institution, INSTITUTIONS_MAP.keys())
        if result and result not in results:
            results.append(str(INSTITUTIONS_MAP[result]))
    return results


def _resolve_sources(source_types: List[str]) -> List[int]:
    if not source_types:
        return []
    return [SUMMARY_SOURCE_MAP[name] for name in source_types if name in SUMMARY_SOURCE_MAP]


def _resolve_code_list(
    raw_items: Optional[List[str]],
    label_to_code_map: dict,
) -> List[str]:
    if not raw_items:
        return []

    resolved_codes: List[str] = []
    for raw_item in raw_items:
        if not raw_item:
            continue

        item = raw_item.strip()
        if not item:
            continue

        if item in label_to_code_map:
            resolved_code = label_to_code_map[item]
            if resolved_code not in resolved_codes:
                resolved_codes.append(resolved_code)
            continue

        if item not in resolved_codes:
            resolved_codes.append(item)

    return resolved_codes


def _resolve_market_list(market_list: Optional[List[str]]) -> List[str]:
    return _resolve_code_list(market_list, SUMMARY_MARKET_CODE_MAP)


def _resolve_participant_role_list(participant_role_list: Optional[List[str]]) -> List[str]:
    return _resolve_code_list(participant_role_list, SUMMARY_PARTICIPANT_ROLE_CODE_MAP)


def _resolve_category_list(category_list: Optional[List[str]]) -> List[str]:
    return _resolve_code_list(category_list, SUMMARY_CATEGORY_CODE_MAP)


def _clean_keyword(
    keyword: str,
    securities=None,
    source_types=None,
    institutions=None,
    industries=None,
    market_list=None,
    participant_role_list=None,
    category_list=None,
    columns=None,
) -> str:
    if not keyword:
        return ""
    keyword = (
        keyword.replace("[", "").replace("]", "")
        .replace("、", " ").replace("，", " ")
        .replace(", ", " ").replace(",", " ")
    )
    keyword = (
        keyword.replace("的纪要", "").replace("的会议纪要", "")
        .replace("的调研纪要", "").replace("纪要", "")
        .replace("会议纪要", "").replace("调研纪要", "")
    )
    for items in [
        securities,
        source_types,
        institutions,
        industries,
        market_list,
        participant_role_list,
        category_list,
        columns,
    ]:
        if items:
            for item in items:
                keyword = keyword.replace(item, "")
    return keyword.strip()


def _fetch_summaries(headers, payload_base, keyword, search_type, limit):
    max_page_size = 50
    all_results = []
    offset = 0
    remaining = limit

    while remaining > 0:
        page_size = min(remaining, max_page_size)
        data = {**payload_base, "from": offset, "size": page_size}
        if keyword:
            data["keyword"] = keyword
            data["searchType"] = search_type

        response = requests.post(SUMMARY_URL, headers=headers, json=data)
        if response.status_code != 200:
            if all_results:
                return all_results, response.text.replace("\n", " ").replace("\r", " ").strip()
            return None, response.text.replace("\n", " ").replace("\r", " ").strip()
        result = response.json()

        if result.get("code") not in [200, "000000"] and result.get("status") is not True:
            return None, result.get("msg", "请求失败").replace("\n", " ").replace("\r", " ").strip()

        summary_data = result.get("data", {})
        summaries = summary_data.get("summList") or summary_data.get("list") or []
        if not summaries:
            break

        all_results.extend(_format_summary_item(summaries))

        if len(summaries) < page_size:
            break

        offset += page_size
        remaining -= len(summaries)

    return all_results, None


def summary_finder(
    keyword: str = "",
    securities: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    institutions: Optional[List[str]] = None,
    industries: Optional[List[str]] = None,
    source_types: Optional[List[str]] = None,
    market_list: Optional[List[str]] = None,
    participant_role_list: Optional[List[str]] = None,
    category_list: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    limit: int = FILE_DEFAULT_LIMIT["summary"],
    download: bool = False,
    output_dir: Optional[str] = None,
):
    try:
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }

        industry_ids = _resolve_industries(industries) if industries else []
        broker_ids = _resolve_institutions(institutions) if institutions else []
        source_ids = _resolve_sources(source_types) if source_types else []
        resolved_market_list = _resolve_market_list(market_list)
        resolved_participant_role_list = _resolve_participant_role_list(participant_role_list)
        resolved_category_list = _resolve_category_list(category_list)

        if columns:
            resolved_market_list = list(
                dict.fromkeys(resolved_market_list + _resolve_market_list(columns)).keys()
            )
            resolved_participant_role_list = list(
                dict.fromkeys(resolved_participant_role_list + _resolve_participant_role_list(columns)).keys()
            )
            resolved_category_list = list(
                dict.fromkeys(resolved_category_list + _resolve_category_list(columns)).keys()
            )

        if securities:
            securities = [security.upper() for security in securities]

        if securities and industries:
            industry_ids = []

        start_timestamp, end_timestamp = _format_time_range(start_date, end_date)

        keyword_str = _clean_keyword(
            keyword=keyword,
            securities=securities,
            source_types=source_types,
            institutions=institutions,
            industries=industries,
            market_list=resolved_market_list,
            participant_role_list=resolved_participant_role_list,
            category_list=resolved_category_list,
            columns=columns,
        )

        payload_base = {}
        if start_timestamp:
            payload_base["startTime"] = start_timestamp
        if end_timestamp:
            payload_base["endTime"] = end_timestamp
        if source_ids:
            payload_base["sourceList"] = source_ids
        if securities:
            payload_base["securityList"] = securities
        if industry_ids:
            payload_base["researchAreaList"] = industry_ids
        if broker_ids:
            payload_base["institutionList"] = broker_ids
        if resolved_category_list:
            payload_base["categoryList"] = resolved_category_list
        if resolved_market_list:
            payload_base["marketList"] = resolved_market_list
        if resolved_participant_role_list:
            payload_base["participantRoleList"] = resolved_participant_role_list

        part_error_message = ""
        all_results, err = _fetch_summaries(headers, payload_base, keyword_str, 1, limit)
        if err and not all_results:
            return format_response({"state": "error", "message": err}, "summary")
        elif err and all_results:
            part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results and keyword_str:
            all_results, err = _fetch_summaries(headers, payload_base, keyword_str, 2, limit)
            if err and not all_results:
                return format_response({"state": "error", "message": err}, "summary")
            elif err and all_results:
                part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results:
            return format_response(
                {"state": "error", "message": "未找到相关纪要，建议修改查询条件", "data": []},
                "summary",
            )

        all_results = all_results[:limit]

        additional_message = None
        if download:
            additional_message = download_files(all_results, "summary", output_dir) + ("\n\n" + part_error_message if part_error_message else "")

        response_data = {
            "state": "success",
            "message": "已找到相关纪要",
            "data": [{"data": all_results, "module": "summary", "type": "files"}],
        }
        return format_response(response_data, "summary", additional_message=additional_message)
    except Exception as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "summary",
        )


def _parse_str_list(raw: str) -> Optional[List[str]]:
    if not raw:
        return None
    items = [
        x.strip()
        for x in raw.replace("，", ",").split(",")
        if x.strip()
    ]
    return items or None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="纪要检索命令行：根据关键词、证券、行业、机构等条件查找会议纪要。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-k", "--keyword", default="", help="检索查询关键词，可为空")
    parser.add_argument("-sd", "--start_date", default="", help="开始日期，格式YYYY-MM-DD")
    parser.add_argument("-ed", "--end_date", default="", help="结束日期，格式YYYY-MM-DD")
    parser.add_argument(
        "-l",
        "--limit",
        default=FILE_DEFAULT_LIMIT["summary"],
        type=int,
        help="返回文件数量上限",
    )
    parser.add_argument(
        "--securities",
        default="",
        help="证券代码列表，逗号分隔，必须为标准证券代码，如 000001.SZ",
    )
    parser.add_argument(
        "--institutions",
        default="",
        help="机构列表，逗号分隔",
    )
    parser.add_argument(
        "--industries",
        default="",
        help="行业列表，逗号分隔",
    )
    parser.add_argument(
        "--source_types",
        default="",
        help="来源类型列表，逗号分隔（会议平台/网络资源/公司公告）",
    )
    parser.add_argument(
        "--category_list",
        default="",
        help="会议类别列表，逗号分隔（earningsCall/strategyMeeting/fundRoadshow/shareholdersMeeting/maMeeting/specialMeeting/companyAnalysis/industryAnalysis/other），也可传中文（业绩会/策略会/基金路演/股东大会/并购会议/特别会议/公司分析/行业分析/其他）",
    )
    parser.add_argument(
        "--market_list",
        default="",
        help="纪要所属市场类别列表，逗号分隔（aShares/hkStocks/usChinaConcept/usStocks），也可传中文（A股/港股/美股中概/美股）",
    )
    parser.add_argument(
        "--participant_role_list",
        default="",
        help="特殊参会人标识列表，逗号分隔（management/expert），也可传中文（高管/专家）",
    )
    parser.add_argument(
        "--columns",
        default="",
        help="【兼容参数】旧版栏目列表，逗号分隔（A股/港股/美股中概/美股/高管/专家/业绩会/策略会/公司分析/行业分析/基金路演）。该参数将被映射到 categoryList/marketList/participantRoleList，不再发送 columnIdList。",
    )
    parser.add_argument(
        "-d",
        "--download",
        default=False,
        type=bool,
        help="是否在检索后自动下载对应会议纪要文件，默认不下载",
    )
    parser.add_argument(
        "-od",
        "--output_dir",
        default=None,
        help="下载文件保存路径，建议使用绝对路径",
    )

    args = parser.parse_args()

    keyword = args.keyword or ""
    securities = _parse_str_list(args.securities)
    institutions = _parse_str_list(args.institutions)
    industries = _parse_str_list(args.industries)
    source_types = _parse_str_list(args.source_types)
    columns = _parse_str_list(args.columns)
    category_list = _parse_str_list(args.category_list)
    market_list = _parse_str_list(args.market_list)
    participant_role_list = _parse_str_list(args.participant_role_list)
    start_date = args.start_date or None
    end_date = args.end_date or None
    limit = int(args.limit)
    download = args.download or False
    output_dir = args.output_dir or None
    if not download and output_dir:
        print(f"[WARNING] 参数 -od/--output_dir 仅在下载文件时有效，已忽略\n")
        output_dir = None

    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")

    out = summary_finder(
        keyword=keyword,
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        institutions=institutions,
        industries=industries,
        source_types=source_types,
        category_list=category_list,
        market_list=market_list,
        participant_role_list=participant_role_list,
        columns=columns,
        limit=limit,
        download=download,
        output_dir=output_dir,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()
