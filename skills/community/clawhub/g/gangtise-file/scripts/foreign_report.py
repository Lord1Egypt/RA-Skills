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
    FOREIGN_REPORT_URL,
    FILE_DEFAULT_LIMIT,
    INDUSTRIES_MAP,
    INSTITUTIONS_MAP,
    REGIONS_MAP,
    format_response,
    match_best,
    remove_html_tags,
    check_version,
)
from get_file import download_files


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


def _format_report_item(reports: List[dict]) -> List[dict]:
    _results = []
    for report in reports:
        publisher = report.get("publisher") or {}
        broker_name = (publisher.get("brokerName") or "").strip()
        author_display = (publisher.get("author") or "").strip()

        publish_time = report.get("publishTime")
        report_date = report.get("reportDate")
        file_time = ""
        if isinstance(publish_time, (int, float)) and publish_time and len(str(publish_time)) == 13:
            file_time = datetime.datetime.fromtimestamp(publish_time / 1000).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(publish_time, (int, float)) and publish_time and len(str(publish_time)) == 10:
            file_time = datetime.datetime.fromtimestamp(publish_time).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(publish_time, str) and publish_time:
            file_time = publish_time
        elif isinstance(report_date, (int, float)) and report_date and len(str(report_date)) == 13:
            file_time = datetime.datetime.fromtimestamp(report_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(report_date, (int, float)) and report_date and len(str(report_date)) == 10:
            file_time = datetime.datetime.fromtimestamp(report_date).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(report_date, str) and report_date:
            file_time = report_date

        securities = report.get("securityList") or []
        security_display = []
        if isinstance(securities, list):
            for s in securities:
                if not isinstance(s, dict):
                    continue
                code = (s.get("securityCode") or "").strip()
                name = (s.get("securityName") or "").strip()
                if code and name:
                    security_display.append(f"{name}({code})")
                elif code:
                    security_display.append(code)
                elif name:
                    security_display.append(name)

        industries = report.get("industryList") or []
        industry_display = []
        if isinstance(industries, list):
            for ind in industries:
                if not isinstance(ind, dict):
                    continue
                name = (ind.get("industryName") or "").strip()
                if name:
                    industry_display.append(name)

        llm_tags = report.get("llmTagList") or []
        llm_tags_display = "、".join([str(x) for x in llm_tags if x]) if isinstance(llm_tags, list) else ""

        region_obj = report.get("region") if isinstance(report.get("region"), dict) else {}
        region_name = (region_obj.get("regionName") or "").strip()
        region_code = (region_obj.get("regionCode") or "").strip()
        region_display = ""
        if region_name and region_code:
            region_display = f"{region_name}({region_code})"
        elif region_name:
            region_display = region_name
        elif region_code:
            region_display = region_code

        title_tr = remove_html_tags(report.get("titleTranslate", "") or "")
        brief_tr = remove_html_tags(report.get("briefTranslate", "") or "")
        print(f"titleTranslate: {report.get('titleTranslate')}")

        item = {
            "标题": remove_html_tags(report.get("title", "")),
            "中文标题": title_tr,
            "文件时间": file_time,
            "作者": author_display,
            "来源机构": broker_name,
            "所属区域": region_display,
            "所属证券": "、".join(security_display),
            "所属板块": "、".join(industry_display),
            "研报类别": report.get("category", "") or "",
            "语义标签": llm_tags_display,
            "页数": report.get("pageNumber", None),
            "有翻译": report.get("hasTranslate"),
            "摘要": remove_html_tags(report.get("brief", "") or ""),
            "中文摘要": brief_tr,
            "类型": "外资研报",
            "类型中ID": str(report.get("reportId", "") or ""),
        }
        _results.append(item)
    return _results


def _resolve_industries(industries: List[str]) -> List[str]:
    if not industries:
        return []
    all_industries = {}
    for key, value in INDUSTRIES_MAP.items():
        all_industries.update(value.copy())
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


def _resolve_regions(regions: List[str]) -> List[str]:
    if not regions:
        return []
    valid_ids = set(REGIONS_MAP.values())
    results = []
    for raw in regions:
        r = str(raw).strip()
        if not r:
            continue
        if r in valid_ids:
            if r not in results:
                results.append(r)
            continue
        result = match_best(r, REGIONS_MAP.keys())
        if result and REGIONS_MAP.get(result) not in results:
            results.append(str(REGIONS_MAP[result]))
    return results


def _clean_keyword(keyword: str, securities=None, institutions=None, industries=None) -> str:
    if not keyword:
        return ""
    keyword = (
        keyword.replace("[", "").replace("]", "")
        .replace("、", " ").replace("，", " ")
        .replace(", ", " ").replace(",", " ")
    )
    keyword = (
        keyword.replace("的研报", "").replace("的研究报告", "").replace("的外资研报", "")
        .replace("的报告", "").replace("研报", "").replace("外资研报", "")
        .replace("研究报告", "").replace("报告", "").replace("外资研报", "")
    )
    for items in [securities, institutions, industries]:
        if items:
            for item in items:
                keyword = keyword.replace(item, "")
    return keyword.strip()


def _fetch_reports(headers, payload_base, keyword, search_type, rank_type, limit):
    """分页获取研报，返回格式化后的结果列表"""
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
        if rank_type:
            data["rankType"] = rank_type

        response = requests.post(FOREIGN_REPORT_URL, headers=headers, json=data)
        if response.status_code != 200:
            if all_results:
                return all_results, response.text.replace("\n", " ").replace("\r", " ").strip()
            return None, response.text.replace("\n", " ").replace("\r", " ").strip()
        result = response.json()

        if result.get("code") not in [200, "000000"] and result.get("status") is not True:
            return None, result.get("msg", "请求失败").replace("\n", " ").replace("\r", " ").strip()

        report_data = result.get("data", {})
        reports = report_data.get("list", [])
        if not reports:
            break

        all_results.extend(_format_report_item(reports))

        if len(reports) < page_size:
            break

        offset += page_size
        remaining -= len(reports)

    return all_results, None


def report_finder(
    keyword: str = "",
    securities: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    institutions: Optional[List[str]] = None,
    industries: Optional[List[str]] = None,
    region_list: Optional[List[str]] = None,
    category_list: Optional[List[str]] = None,
    llm_tag_list: Optional[List[str]] = None,
    rating_list: Optional[List[str]] = None,
    rating_change_list: Optional[List[str]] = None,
    min_report_pages: Optional[int] = None,
    max_report_pages: Optional[int] = None,
    search_type: int = 1,
    rank_type: int = 1,
    limit: int = FILE_DEFAULT_LIMIT["foreign_report"],
    download: bool = False,
    download_types: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
):
    try:
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }

        industry_ids = _resolve_industries(industries) if industries else []
        org_ids = _resolve_institutions(institutions) if institutions else []
        region_ids = _resolve_regions(region_list) if region_list else []

        if securities:
            securities = [security.upper() for security in securities]

        if securities and industries:
            industry_ids = []

        start_timestamp, end_timestamp = _format_time_range(start_date, end_date)

        keyword_str = _clean_keyword(keyword, securities, institutions, industries)

        payload_base = {}
        if start_timestamp:
            payload_base["startTime"] = start_timestamp
        if end_timestamp:
            payload_base["endTime"] = end_timestamp
        if securities:
            payload_base["securityList"] = securities
        if industry_ids:
            payload_base["industryList"] = industry_ids
        if org_ids:
            payload_base["brokerList"] = org_ids
        if region_ids:
            payload_base["regionList"] = region_ids
        if category_list:
            payload_base["categoryList"] = category_list
        if llm_tag_list:
            payload_base["llmTagList"] = llm_tag_list
        if rating_list:
            payload_base["ratingList"] = rating_list
        if rating_change_list:
            payload_base["ratingChangeList"] = rating_change_list
        if min_report_pages is not None:
            payload_base["minReportPages"] = int(min_report_pages)
        if max_report_pages is not None:
            payload_base["maxReportPages"] = int(max_report_pages)

        part_error_message = ""
        all_results, err = _fetch_reports(headers, payload_base, keyword_str, search_type, rank_type, limit)
        if err and not all_results:
            return format_response({"state": "error", "message": err}, "foreign_report")
        elif err and all_results:
            part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results and keyword_str:
            all_results, err = _fetch_reports(headers, payload_base, keyword_str, 2, rank_type, limit)
            if err and not all_results:
                return format_response({"state": "error", "message": err}, "foreign_report")
            elif err and all_results:
                part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results:
            return format_response(
                {"state": "error", "message": "未找到相关研报，建议修改查询条件", "data": []},
                "foreign_report",
            )

        all_results = all_results[:limit]

        additional_message = None
        if download:
            additional_message = download_files(all_results, "foreign_report", output_dir, download_types=download_types) + ("\n\n" + part_error_message if part_error_message else "")

        response_data = {
            "state": "success",
            "message": "已找到相关研报",
            "data": [{"data": all_results, "module": "foreign_report", "type": "files"}],
        }
        return format_response(response_data, "foreign_report", additional_message=additional_message)
    except Exception as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "foreign_report",
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
        description="外资研报检索命令行：根据关键词、证券、机构等条件查找外资研报。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-k", "--keyword", default="", help="检索查询关键词，可为空")
    parser.add_argument("-sd", "--start_date", default="", help="开始日期，格式YYYY-MM-DD")
    parser.add_argument("-ed", "--end_date", default="", help="结束日期，格式YYYY-MM-DD")
    parser.add_argument(
        "-l",
        "--limit",
        default=FILE_DEFAULT_LIMIT["foreign_report"],
        type=int,
        help="返回文件数量上限",
    )
    parser.add_argument(
        "--securities",
        default="",
        help="证券代码列表，逗号分隔；境外格式如 UBER.N",
    )
    parser.add_argument(
        "--institutions",
        default="",
        help="券商列表，逗号分隔（会智能匹配到 brokerId）",
    )
    parser.add_argument(
        "--industries",
        default="",
        help="行业列表，逗号分隔",
    )
    parser.add_argument(
        "--region_list",
        default="",
        help="区域列表，逗号分隔；可为区域 ID（如 us）或中文名（见 get_regions.py）",
    )
    parser.add_argument(
        "--category_list",
        default="",
        help="研报类别列表，逗号分隔（macro/strategy/industry/company/bond/quant/morningNotes/fund/forex/futures/options/warrants/market/wealthManagement/other）",
    )
    parser.add_argument(
        "--llm_tag_list",
        default="",
        help="语义标签列表，逗号分隔（inDepth/earningsReview/industryStrategy）",
    )
    parser.add_argument(
        "--rating_list",
        default="",
        help="研报评级列表，逗号分隔（buy/overweight/neutral/underweight/sell）",
    )
    parser.add_argument(
        "--rating_change_list",
        default="",
        help="评级变动列表，逗号分隔（upgrade/maintain/downgrade/initiate）",
    )
    parser.add_argument("--min_report_pages", default=None, type=int, help="研报最小页数")
    parser.add_argument("--max_report_pages", default=None, type=int, help="研报最大页数")
    parser.add_argument(
        "--search_type",
        default=1,
        type=int,
        help="搜索类型：1-标题搜索 2-全文搜索",
    )
    parser.add_argument(
        "--rank_type",
        default=1,
        type=int,
        help="排序方式：1-综合排序 2-时间倒序",
    )
    parser.add_argument(
        "-d",
        "--download",
        default=False,
        type=bool,
        help="是否在检索后自动下载对应研究报告文件，默认不下载",
    )
    parser.add_argument(
        "-od",
        "--output_dir",
        default=None,
        help="下载文件保存路径，建议使用绝对路径",
    )
    parser.add_argument(
        "-dt",
        "--download-types",
        default="pdf",
        help="下载的文件类型，逗号分隔，可选值：pdf, markdown",
    )

    args = parser.parse_args()

    keyword = args.keyword or ""
    securities = _parse_str_list(args.securities)
    institutions = _parse_str_list(args.institutions)
    industries = _parse_str_list(args.industries)
    region_list = _parse_str_list(args.region_list)
    category_list = _parse_str_list(args.category_list)
    llm_tag_list = _parse_str_list(args.llm_tag_list)
    rating_list = _parse_str_list(args.rating_list)
    rating_change_list = _parse_str_list(args.rating_change_list)
    start_date = args.start_date or None
    end_date = args.end_date or None
    limit = int(args.limit)
    search_type = int(args.search_type or 1)
    rank_type = int(args.rank_type or 1)
    download = args.download or False
    output_dir = args.output_dir or None
    download_types = _parse_str_list(args.download_types)
    if not download and output_dir:
        print(f"[WARNING] 参数 -od/--output_dir 仅在下载文件时有效，已忽略\n")
        output_dir = None

    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")

    out = report_finder(
        keyword=keyword,
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        institutions=institutions,
        industries=industries,
        region_list=region_list,
        category_list=category_list,
        llm_tag_list=llm_tag_list,
        rating_list=rating_list,
        rating_change_list=rating_change_list,
        min_report_pages=args.min_report_pages,
        max_report_pages=args.max_report_pages,
        search_type=search_type,
        rank_type=rank_type,
        limit=limit,
        download=download,
        output_dir=output_dir,
        download_types=download_types,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()
