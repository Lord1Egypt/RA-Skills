import os
import sys
from typing import List, Optional
import datetime
import requests
from io import TextIOWrapper

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (  # noqa: E402
    GTS_AUTHORIZATION,
    OPINION_URL,
    FILE_DEFAULT_LIMIT,
    RESEARCH_AREA_MAP,
    INSTITUTIONS_MAP,
    format_response,
    match_best,
    remove_html_tags,
    check_version,
)

OPINION_LLM_TAG_MAP = {
    "强烈推荐": "strongRcmd",
    "业绩点评": "earningsReview",
    "头部券商": "topBroker",
    "新财富团队": "newFortune",
}

OPINION_SOURCE_MAP = {
    "实时": "realTime",
    "开放来源": "openSource",
}

OPINION_LLM_CODES = frozenset(OPINION_LLM_TAG_MAP.values())
OPINION_SOURCE_CODES = frozenset(OPINION_SOURCE_MAP.values())


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


def _format_opinion_item(items: List[dict]) -> List[dict]:
    _results = []
    for row in items:
        content_list = row.get("contentList") or {}
        title = remove_html_tags(content_list.get("title") or "")
        content = remove_html_tags(content_list.get("content") or "")

        author = row.get("author") or {}
        chief_name = author.get("chiefName") or ""
        chief_id = author.get("chiefId") or ""
        chief_display = f"{chief_name}({chief_id})" if chief_id else chief_name

        research_areas = author.get("researchAreaList") or []
        ra_display = ", ".join([str(x) for x in research_areas if x]) if isinstance(research_areas, list) else ""

        broker_name = author.get("brokerName") or ""
        broker_id = author.get("brokerID") or ""
        broker_display = f"{broker_name}({broker_id})" if broker_id else broker_name

        security_items = row.get("securityList") or []
        stock_parts: List[str] = []
        for s in security_items:
            if not isinstance(s, dict):
                continue
            code = s.get("securityCode") or ""
            name = s.get("securityName") or ""
            if code:
                part = f"{name}({code})" if name else f"({code})"
                if part not in stock_parts:
                    stock_parts.append(part)
        stock_display = ", ".join(stock_parts)

        industry_items = row.get("industryList") or []
        ind_parts: List[str] = []
        for i in industry_items:
            if not isinstance(i, dict):
                continue
            ic = i.get("industryCode") or ""
            iname = i.get("industryName") or ""
            if ic or iname:
                part = f"{iname}({ic})" if ic else iname
                if part not in ind_parts:
                    ind_parts.append(part)
        industry_display = ", ".join(ind_parts)

        concept_items = row.get("conceptList") or []
        con_parts: List[str] = []
        for c in concept_items:
            if not isinstance(c, dict):
                continue
            cid = c.get("conceptId") or ""
            cname = c.get("conceptName") or ""
            if cid or cname:
                part = f"{cname}({cid})" if cid else cname
                if part not in con_parts:
                    con_parts.append(part)
        concept_display = ", ".join(con_parts)

        llm_tags = row.get("llmTagList") or []
        tag_display = ", ".join([str(x) for x in llm_tags if x]) if isinstance(llm_tags, list) else ""

        item = {
            "标题": title,
            "文件时间": "",
            "摘要": content + ("..." if content else ""),
            "首席": chief_display,
            "券商": broker_display,
            "研究方向": ra_display,
            "关联股票": stock_display,
            "关联行业": industry_display,
            "概念": concept_display,
            "标签": tag_display,
            "类型": "首席观点",
            "类型中ID": str(row.get("chiefOpinionId") or ""),
        }
        _results.append(item)
    return _results


def _resolve_research_areas(industries: Optional[List[str]]) -> List[str]:
    """CLI 参数 industries → API researchAreaList（仅研究方向 ID，不含行业 industryList）。"""
    if not industries:
        return []
    id_set = {str(v) for v in RESEARCH_AREA_MAP.values()}
    results = []
    for raw in industries:
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
    results = []
    for institution in institutions:
        result = match_best(institution, INSTITUTIONS_MAP.keys())
        if result and result not in results:
            results.append(str(INSTITUTIONS_MAP[result]))
    return results


def _resolve_llm_tags(tags: Optional[List[str]]) -> List[str]:
    if not tags:
        return []
    out: List[str] = []
    for t in tags:
        if not t:
            continue
        s = t.strip()
        if s in OPINION_LLM_CODES:
            if s not in out:
                out.append(s)
            continue
        if s in OPINION_LLM_TAG_MAP:
            c = OPINION_LLM_TAG_MAP[s]
            if c not in out:
                out.append(c)
            continue
        if s not in out:
            out.append(s)
    return out


def _resolve_opinion_sources(source_types: Optional[List[str]]) -> List[str]:
    if not source_types:
        return []
    out: List[str] = []
    for t in source_types:
        if not t:
            continue
        s = t.strip()
        if s in OPINION_SOURCE_CODES:
            if s not in out:
                out.append(s)
            continue
        if s in OPINION_SOURCE_MAP:
            c = OPINION_SOURCE_MAP[s]
            if c not in out:
                out.append(c)
            continue
        if s not in out:
            out.append(s)
    return out


def _clean_keyword(
    keyword: str,
    securities=None,
    institutions=None,
    industries=None,
    chiefs=None,
    concepts=None,
    llm_tags=None,
    source_types=None,
):
    if not keyword:
        return ""
    keyword = (
        keyword.replace("[", "").replace("]", "")
        .replace("、", " ").replace("，", " ")
        .replace(", ", " ").replace(",", " ")
    )
    for items in [securities, institutions, industries, chiefs, concepts, llm_tags, source_types]:
        if items:
            for item in items:
                keyword = keyword.replace(item, "")
    return keyword.strip()


def _fetch_opinions(headers, payload_base, keyword, limit):
    max_page_size = 50
    all_results = []
    offset = 0
    remaining = limit

    while remaining > 0:
        page_size = min(remaining, max_page_size)
        data = {**payload_base, "from": offset, "size": page_size}
        if keyword:
            data["keyword"] = keyword

        response = requests.post(OPINION_URL, headers=headers, json=data)
        if response.status_code != 200:
            if all_results:
                return all_results, response.text.replace("\n", " ").replace("\r", " ").strip()
            return None, response.text.replace("\n", " ").replace("\r", " ").strip()
        result = response.json()

        if result.get("code") not in [200, "000000"] and result.get("status") is not True:
            return None, result.get("msg", "请求失败").replace("\n", " ").replace("\r", " ").strip()

        block = result.get("data") or {}
        rows = block.get("list") or []
        if not rows:
            break

        all_results.extend(_format_opinion_item(rows))

        if len(rows) < page_size:
            break

        offset += page_size
        remaining -= len(rows)

    return all_results, None


def opinion_finder(
    keyword: str = "",
    securities: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    institutions: Optional[List[str]] = None,
    industries: Optional[List[str]] = None,
    chiefs: Optional[List[str]] = None,
    concepts: Optional[List[str]] = None,
    llm_tags: Optional[List[str]] = None,
    source_types: Optional[List[str]] = None,
    rank_type: int = 1,
    limit: int = FILE_DEFAULT_LIMIT["opinion"],
):
    try:
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }

        research_area_ids = _resolve_research_areas(industries) if industries else []
        broker_ids = _resolve_institutions(institutions) if institutions else []
        llm_resolved = _resolve_llm_tags(llm_tags) if llm_tags else []
        source_resolved = _resolve_opinion_sources(source_types) if source_types else []

        if securities:
            securities = [s.upper() for s in securities]

        chief_list: List[str] = []
        if chiefs:
            chief_list = [c.strip() for c in chiefs if c and c.strip()]

        concept_list: List[str] = []
        if concepts:
            concept_list = [c.strip() for c in concepts if c and c.strip()]

        start_timestamp, end_timestamp = _format_time_range(start_date, end_date)

        keyword_str = _clean_keyword(
            keyword=keyword,
            securities=securities,
            institutions=institutions,
            industries=industries,
            chiefs=chiefs,
            concepts=concepts,
            llm_tags=llm_tags,
            source_types=source_types,
        )

        payload_base: dict = {
            "rankType": rank_type,
        }
        if start_timestamp is not None:
            payload_base["startTime"] = start_timestamp
        if end_timestamp is not None:
            payload_base["endTime"] = end_timestamp
        if research_area_ids:
            payload_base["researchAreaList"] = research_area_ids
        if broker_ids:
            payload_base["brokerList"] = broker_ids
        if securities:
            payload_base["securityList"] = securities
        if chief_list:
            payload_base["chiefList"] = chief_list
        if concept_list:
            payload_base["conceptList"] = concept_list
        if llm_resolved:
            payload_base["llmTagList"] = llm_resolved
        if source_resolved:
            payload_base["sourceList"] = source_resolved

        all_results, err = _fetch_opinions(headers, payload_base, keyword_str, limit)
        if err and not all_results:
            return format_response({"state": "error", "message": err}, "opinion")
        part_error_message = ""
        if err and all_results:
            part_error_message = f"未完整获取全部结果，错误信息：{err}"

        if not all_results:
            return format_response(
                {"state": "error", "message": "未找到相关观点，建议修改查询条件", "data": []},
                "opinion",
            )

        all_results = all_results[:limit]

        response_data = {
            "state": "success",
            "message": "已找到相关观点",
            "data": [{"data": all_results, "module": "opinion", "type": "files"}],
        }
        return format_response(response_data, "opinion", additional_message=part_error_message or "")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "opinion",
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
        description="首席观点检索：按关键词、证券、券商、研究方向、首席、概念、标签等查询观点列表。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-k", "--keyword", default="", help="搜索关键词，可为空")
    parser.add_argument("-sd", "--start_date", default="", help="开始日期，格式 YYYY-MM-DD")
    parser.add_argument("-ed", "--end_date", default="", help="结束日期，格式 YYYY-MM-DD")
    parser.add_argument(
        "-l",
        "--limit",
        default=FILE_DEFAULT_LIMIT["opinion"],
        type=int,
        help="返回条数上限",
    )
    parser.add_argument(
        "--rank_type",
        default=1,
        type=int,
        choices=[1, 2],
        help="排序：1 综合排序，2 时间倒序",
    )
    parser.add_argument(
        "--securities",
        default="",
        help="证券代码列表，逗号分隔，如 000001.SZ",
    )
    parser.add_argument(
        "--industries",
        default="",
        help="研究方向列表（映射为 researchAreaList），逗号分隔：宏观/策略/固收/金工/海外 等",
    )
    parser.add_argument(
        "--institutions",
        default="",
        help="发布机构（券商）列表，逗号分隔",
    )
    parser.add_argument(
        "--chiefs",
        default="",
        help="首席分析师 ID 列表，逗号分隔",
    )
    parser.add_argument(
        "--concepts",
        default="",
        help="概念 ID 列表，逗号分隔",
    )
    parser.add_argument(
        "--llm_tags",
        default="",
        help="投研标签，逗号分隔：strongRcmd/earningsReview/topBroker/newFortune 或中文",
    )
    parser.add_argument(
        "--source_types",
        default="",
        help="来源，逗号分隔：realTime/openSource 或 实时/开放来源",
    )

    args = parser.parse_args()

    keyword = args.keyword or ""
    securities = _parse_str_list(args.securities)
    institutions = _parse_str_list(args.institutions)
    industries = _parse_str_list(args.industries)
    chiefs = _parse_str_list(args.chiefs)
    concepts = _parse_str_list(args.concepts)
    llm_tags = _parse_str_list(args.llm_tags)
    source_types = _parse_str_list(args.source_types)
    start_date = args.start_date or None
    end_date = args.end_date or None
    limit = int(args.limit)
    rank_type = int(args.rank_type)

    try:
        if not check_version():
            print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
    except Exception:
        print(f"[WARNING] 检查 Gangtise skills 版本失败\n")

    out = opinion_finder(
        keyword=keyword,
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        institutions=institutions,
        industries=industries,
        chiefs=chiefs,
        concepts=concepts,
        llm_tags=llm_tags,
        source_types=source_types,
        rank_type=rank_type,
        limit=limit,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()
