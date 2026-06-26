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
    COMPANY_ANNOUNCEMENT_URL,
    FILE_DEFAULT_LIMIT,
    format_response,
    match_best,
    remove_html_tags,
    ANNOUNCEMENT_CATEGORY_MAP,
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


def _format_announcement_item(announcements: List[dict]) -> List[dict]:
    _results = []
    for ann in announcements:
        publish_time = ann.get("publishTime")
        ann_date = ann.get("announcementDate")
        file_time = ""
        if isinstance(publish_time, (int, float)) and publish_time and len(str(publish_time)) == 13:
            file_time = datetime.datetime.fromtimestamp(publish_time / 1000).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(publish_time, (int, float)) and publish_time and len(str(publish_time)) == 10:
            file_time = datetime.datetime.fromtimestamp(publish_time).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(publish_time, str) and publish_time:
            file_time = publish_time
        elif isinstance(ann_date, (int, float)) and ann_date and len(str(ann_date)) == 13:
            file_time = datetime.datetime.fromtimestamp(ann_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(ann_date, (int, float)) and ann_date and len(str(ann_date)) == 10:
            file_time = datetime.datetime.fromtimestamp(ann_date).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(ann_date, str) and ann_date:
            file_time = ann_date

        primary = ann.get("primaryCategory") or {}
        secondary = ann.get("secondaryCategory") or {}
        primary_name = (primary.get("categoryName") or "").strip() if isinstance(primary, dict) else ""
        secondary_name = (secondary.get("categoryName") or "").strip() if isinstance(secondary, dict) else ""
        category_display = " / ".join([x for x in [primary_name, secondary_name] if x])

        sec_code = (ann.get("securityCode") or "").strip()
        sec_name = (ann.get("securityName") or "").strip()
        sec_display = ""
        if sec_code and sec_name:
            sec_display = f"{sec_name}({sec_code})"
        else:
            sec_display = sec_code or sec_name

        item = {
            "标题": remove_html_tags(ann.get("title", "")),
            "文件时间": file_time,
            "所属证券": sec_display,
            "公告类型": category_display,
            "来源": ann.get("sourceName", "") or "",
            "摘要": "",
            "类型": "公司公告",
            "类型中ID": str(ann.get("announcementId", "") or ""),
        }
        _results.append(item)
    return _results


def _clean_keyword(keyword: str, securities=None) -> str:
    if not keyword:
        return ""
    keyword = (
        keyword.replace("[", "").replace("]", "")
        .replace("、", " ").replace("，", " ")
        .replace(", ", " ").replace(",", " ")
    )
    keyword = (
        keyword.replace("的公告", "").replace("的公司公告", "")
        .replace("公司公告", "").replace("公告", "")
    )
    if securities:
        for item in securities:
            keyword = keyword.replace(item, "")
    return keyword.strip()


def _fetch_announcements(headers, payload_base, keyword, search_type, rank_type, limit):
    """分页获取公告，返回格式化后的结果列表"""
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
        response = requests.post(COMPANY_ANNOUNCEMENT_URL, headers=headers, json=data)
        if response.status_code != 200:
            if all_results:
                return all_results, response.text.replace("\n", " ").replace("\r", " ").strip()
            return None, response.text.replace("\n", " ").replace("\r", " ").strip()
        result = response.json()

        if result.get("code") not in [200, "000000"] and result.get("status") is not True:
            return None, result.get("msg", "请求失败").replace("\n", " ").replace("\r", " ").strip()

        ann_data = result.get("data", {})
        announcements = ann_data.get("list", [])
        if not announcements:
            break

        all_results.extend(_format_announcement_item(announcements))

        if len(announcements) < page_size:
            break

        offset += page_size
        remaining -= len(announcements)

    return all_results, None


def _resolve_announcement_categories(categories: Optional[List[str]]) -> List[str]:
    if not categories:
        return []
    results: List[str] = []
    for c in categories:
        if not c:
            continue
        c = str(c).strip()
        if not c:
            continue
        # 纯 ID（数字/字母混合）直接透传
        if c.isdigit() or c.startswith("ANN") or c.startswith("10"):
            if c not in results:
                results.append(c)
            continue
        if ANNOUNCEMENT_CATEGORY_MAP:
            matched = match_best(c, ANNOUNCEMENT_CATEGORY_MAP.keys())
            if matched:
                cid = str(ANNOUNCEMENT_CATEGORY_MAP[matched])
                if cid and cid not in results:
                    results.append(cid)
    return results


def announcement_finder(
    keyword: str = "",
    securities: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category_list: Optional[List[str]] = None,
    search_type: int = 1,
    rank_type: int = 1,
    limit: int = FILE_DEFAULT_LIMIT["announcement"],
    download: bool = False,
    output_dir: Optional[str] = None,
    download_types: Optional[List[str]] = None,
):
    try:
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }

        if securities:
            securities = [security.upper() for security in securities]

        start_timestamp, end_timestamp = _format_time_range(start_date, end_date)

        keyword_str = _clean_keyword(keyword, securities)

        payload_base = {}
        if start_timestamp:
            payload_base["startTime"] = start_timestamp
        if end_timestamp:
            payload_base["endTime"] = end_timestamp
        if securities:
            payload_base["securityList"] = securities
        category_ids = _resolve_announcement_categories(category_list)
        if category_ids:
            payload_base["categoryList"] = category_ids

        part_error_message = ""
        all_results, err = _fetch_announcements(headers, payload_base, keyword_str, search_type, rank_type, limit)
        if err and not all_results:
            return format_response({"state": "error", "message": err}, "announcement")
        elif err and all_results:
            part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results and keyword_str:
            all_results, err = _fetch_announcements(headers, payload_base, keyword_str, 2, rank_type, limit)
            if err and not all_results:
                return format_response({"state": "error", "message": err}, "announcement")
            elif err and all_results:
                part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results:
            return format_response(
                {"state": "error", "message": "未找到相关公告，建议修改查询条件", "data": []},
                "announcement",
            )

        all_results = all_results[:limit]

        additional_message = None
        if download:
            additional_message = download_files(all_results, "announcement", output_dir, download_types=download_types) + ("\n\n" + part_error_message if part_error_message else "")

        response_data = {
            "state": "success",
            "message": "已找到相关公告",
            "data": [{"data": all_results, "module": "announcement", "type": "files"}],
        }
        return format_response(response_data, "announcement", additional_message=additional_message)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "announcement",
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
        description="公告检索命令行：根据关键词、证券代码等条件查找公司公告。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-k", "--keyword", default="", help="检索查询关键词，可为空")
    parser.add_argument("-sd", "--start_date", default="", help="开始日期，格式YYYY-MM-DD")
    parser.add_argument("-ed", "--end_date", default="", help="结束日期，格式YYYY-MM-DD")
    parser.add_argument(
        "-l",
        "--limit",
        default=FILE_DEFAULT_LIMIT["announcement"],
        type=int,
        help="返回文件数量上限",
    )
    parser.add_argument(
        "--securities",
        default="",
        help="证券代码列表，逗号分隔，必须为标准证券代码，如 000001.SZ",
    )
    parser.add_argument(
        "--category_list",
        default="",
        help="公告分类列表，逗号分隔（可直接传 categoryId；或传分类名称并在 utils.ANNOUNCEMENT_CATEGORY_MAP 中配置映射）",
    )
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
        help="是否在检索后自动下载对应公司公告文件，默认不下载",
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
    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")

    args = parser.parse_args()
    keyword = args.keyword or ""
    securities = _parse_str_list(args.securities)
    category_list = _parse_str_list(args.category_list)
    start_date = args.start_date or None
    end_date = args.end_date or None
    limit = int(args.limit)
    search_type = int(args.search_type or 1)
    rank_type = int(args.rank_type or 1)
    download = args.download or False
    output_dir = args.output_dir or None
    if not download and output_dir:
        print(f"[WARNING] 参数 -od/--output_dir 仅在下载文件时有效，已忽略\n")
        output_dir = None
    download_types = _parse_str_list(args.download_types)
    out = announcement_finder(
        keyword=keyword,
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        category_list=category_list,
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
