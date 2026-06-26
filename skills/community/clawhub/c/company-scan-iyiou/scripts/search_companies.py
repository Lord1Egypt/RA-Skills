#!/usr/bin/env python3
"""
search_companies.py — 亿欧企业搜索脚本

Usage:
    python search_companies.py [options]

Options:
    --concepts          概念关键词，逗号分隔，如 "生物医药,医疗器械"
    --keyword           企业名称关键词（精确/模糊）
    --min-invest-round  最低融资轮次，如 "B轮"
    --max-invest-round  最高融资轮次，如 "Pre-B轮"
    --min-invest-amount-wan  最低融资金额（万元），如 10000
    --latest-invest-after   最近融资起始日期，如 "2024-01-01"
    --provinces         省份列表，逗号分隔，如 "上海,江苏,浙江"
    --cities            城市列表，逗号分隔，如 "合肥,杭州"
    --country           国家 (0=不限, 44=中国大陆)，默认44
    --established-after  成立日期起始
    --established-before 成立日期截止
    --max-results       最多返回企业数量，默认50
    --page-size         每次API请求条数，默认10，最大100
    --output-format     输出格式：markdown（默认）或 json
"""

import argparse
import json
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_ENDPOINT = "https://api-open-data.iyiou.com/llm/company/search"
IYIOU_LIST_URL = "https://data.iyiou.com/company/comlist"

# Ordered round labels for range validation reference (informational only)
ROUND_ORDER = [
    "种子轮", "天使轮", "Pre-A轮", "A轮", "A+轮",
    "Pre-B轮", "B轮", "B+轮", "Pre-C轮", "C轮", "C+轮",
    "D轮", "E轮", "F轮", "G轮", "H轮", "I轮", "J轮", "K轮",
    "战略投资", "Pre-IPO", "已上市", "并购", "未融资", "无需融资", "已退市",
]


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class APIError(Exception):
    """Raised when the API returns a non-200 code."""
    pass


# ---------------------------------------------------------------------------
# Parameter builder
# ---------------------------------------------------------------------------

def build_params(
    concepts: list[str] | None = None,
    keyword: str | None = None,
    min_invest_round: str | None = None,
    max_invest_round: str | None = None,
    min_invest_amount_wan: int | None = None,
    latest_invest_after: str | None = None,
    provinces: list[str] | None = None,
    cities: list[str] | None = None,
    country: int = 44,
    established_after: str | None = None,
    established_before: str | None = None,
    page_no: int = 1,
    page_size: int = 10,
) -> dict[str, Any]:
    """Build the API request payload, omitting None values."""
    params: dict[str, Any] = {
        "country": country,
        "pageNo": page_no,
        "pageSize": page_size,
    }

    if concepts:
        params["concepts"] = concepts
    if keyword:
        params["keyword"] = keyword
    if min_invest_round is not None:
        params["minInvestRound"] = min_invest_round
    if max_invest_round is not None:
        params["maxInvestRound"] = max_invest_round
    if min_invest_amount_wan is not None:
        params["minInvestAmountWan"] = min_invest_amount_wan
    if latest_invest_after is not None:
        params["latestInvestAfter"] = latest_invest_after
    if provinces:
        params["provinces"] = provinces
    if cities:
        params["cities"] = cities
    if established_after is not None:
        params["establishedAfter"] = established_after
    if established_before is not None:
        params["establishedBefore"] = established_before

    return params


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_api(params: dict[str, Any]) -> dict[str, Any]:
    """POST params to the search endpoint and return parsed JSON."""
    payload = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise APIError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise APIError(f"Network error: {e.reason}") from e


# ---------------------------------------------------------------------------
# Pagination engine
# ---------------------------------------------------------------------------

def fetch_all(
    base_params: dict[str, Any],
    max_results: int = 50,
    page_size: int = 10,
) -> tuple[list[dict[str, Any]], int]:
    """
    Paginate through the API until we have `max_results` items or exhaust
    the result set.

    Returns:
        (companies, api_total) — fetched list and the total count from the API.

    Raises APIError if any page returns a non-200 response code.
    """
    collected: list[dict[str, Any]] = []
    api_total: int = 0
    page_no = 1

    while len(collected) < max_results:
        params = {**base_params, "pageNo": page_no, "pageSize": page_size}
        response = call_api(params)

        # Error handling
        if response.get("code") != 200:
            raise APIError(
                f"API error (code={response.get('code')}): "
                f"{response.get('message', 'unknown error')}"
            )

        data = response.get("data") or {}
        items: list[dict] = data.get("records") or []
        api_total = data.get("total", 0)

        if not items:
            break

        collected.extend(items)

        # Stop if we've seen all available results
        if len(collected) >= api_total:
            break

        page_no += 1

    return collected[:max_results], api_total


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def _fmt_valuation(val) -> str:
    if val is None:
        return "—"
    try:
        v = int(val)
        if v >= 10000:
            return f"{v // 10000}亿"
        return f"{v}万"
    except (ValueError, TypeError):
        return str(val)


def render_markdown(
    companies: list[dict[str, Any]],
    total_found: int,
    query_summary: str,
) -> str:
    """Render company list as a Markdown table with footer prompt."""
    lines: list[str] = []

    if not companies:
        lines.append(f"## 企业扫描结果\n")
        lines.append(f"**查询条件：** {query_summary}\n")
        lines.append("⚠️ 未找到符合条件的企业，请尝试放宽筛选条件。")
        return "\n".join(lines)

    # Header
    lines.append(f"## 企业扫描结果\n")
    lines.append(f"**查询条件：** {query_summary}")
    showing = len(companies)
    if total_found > showing:
        lines.append(
            f"**共找到 {total_found} 家企业，展示前 {showing} 家**\n"
        )
    else:
        lines.append(f"**共找到 {total_found} 家企业**\n")

    # Table
    headers = [
        "企业简称", "企业全称", "一句话简介", "行业",
        "最新融资轮次", "最新投资方", "融资时间",
        "估值(万元)", "省份", "链接",
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for c in companies:
        valuation_str = _fmt_valuation(c.get("marketValuationRmb"))
        url = c.get("url", "")
        link = f"[详情]({url})" if url else "—"
        row = [
            c.get("briefName") or "—",
            c.get("fullName") or "—",
            c.get("briefIntro") or "—",
            c.get("industryName") or "—",
            c.get("latestInvestRoundStr") or "—",
            c.get("latestInvestorStr") or "—",
            c.get("latestInvestTime") or "—",
            valuation_str,
            c.get("province") or "—",
            link,
        ]
        # Escape pipe characters in cell values
        row = [str(v).replace("|", "｜") for v in row]
        lines.append("| " + " | ".join(row) + " |")

    # Footer
    lines.append(f"\n---")
    lines.append(
        f"> 💡 如需查看更多企业请访问亿欧数据：[{IYIOU_LIST_URL}]({IYIOU_LIST_URL})"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI argument parser
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="亿欧企业搜索 — 企业扫描 skill 执行脚本"
    )
    parser.add_argument("--concepts", type=str, default=None,
                        help="概念关键词，逗号分隔")
    parser.add_argument("--keyword", type=str, default=None)
    parser.add_argument("--min-invest-round", type=str, default=None)
    parser.add_argument("--max-invest-round", type=str, default=None)
    parser.add_argument("--min-invest-amount-wan", type=int, default=None)
    parser.add_argument("--latest-invest-after", type=str, default=None)
    parser.add_argument("--provinces", type=str, default=None,
                        help="省份列表，逗号分隔")
    parser.add_argument("--cities", type=str, default=None,
                        help="城市列表，逗号分隔")
    parser.add_argument("--country", type=int, default=44)
    parser.add_argument("--established-after", type=str, default=None)
    parser.add_argument("--established-before", type=str, default=None)
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--output-format", choices=["markdown", "json"],
                        default="markdown")
    parser.add_argument("--output-file", type=str, default=None,
                        help="将结果写入指定文件路径（避免终端截断）")
    parser.add_argument("--output-temp", action="store_true",
                        help="将结果写入系统临时目录（跨平台），并将路径打印到 stdout")

    ns = parser.parse_args(argv)

    # Post-process comma-separated strings into lists
    if ns.concepts:
        ns.concepts = [c.strip() for c in ns.concepts.split(",") if c.strip()]
    if ns.provinces:
        ns.provinces = [p.strip() for p in ns.provinces.split(",") if p.strip()]
    if ns.cities:
        ns.cities = [c.strip() for c in ns.cities.split(",") if c.strip()]

    return ns


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    base_params = build_params(
        concepts=args.concepts,
        keyword=args.keyword,
        min_invest_round=args.min_invest_round,
        max_invest_round=args.max_invest_round,
        min_invest_amount_wan=args.min_invest_amount_wan,
        latest_invest_after=args.latest_invest_after,
        provinces=args.provinces,
        cities=args.cities,
        country=args.country,
        established_after=args.established_after,
        established_before=args.established_before,
        page_no=1,
        page_size=args.page_size,
    )

    try:
        companies, total_found = fetch_all(
            base_params=base_params,
            max_results=args.max_results,
            page_size=args.page_size,
        )
    except APIError as e:
        print(f"❌ API 调用失败: {e}", file=sys.stderr)
        sys.exit(1)

    # Build query summary for display
    parts = []
    if args.concepts:
        parts.append(" / ".join(args.concepts))
    if args.min_invest_round:
        parts.append(f"{args.min_invest_round}以上")
    if args.max_invest_round:
        parts.append(f"最高{args.max_invest_round}")
    if args.provinces:
        parts.append(" / ".join(args.provinces))
    if args.cities:
        parts.append(" / ".join(args.cities))
    if args.keyword:
        parts.append(f"关键词:{args.keyword}")
    query_summary = " | ".join(parts) if parts else "（无筛选条件）"

    if args.output_format == "json":
        output = json.dumps(companies, ensure_ascii=False, indent=2)
    else:
        output = render_markdown(companies, total_found=total_found,
                                 query_summary=query_summary)

    if args.output_temp:
        tmp = Path(tempfile.gettempdir()) / "company_scan_result.md"
        tmp.write_text(output, encoding="utf-8")
        print(f"✅ 结果已写入：{tmp}（共 {len(companies)} 家企业）")
    elif args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 结果已写入：{args.output_file}（共 {len(companies)} 家企业）")
    else:
        print(output)


if __name__ == "__main__":
    main()
