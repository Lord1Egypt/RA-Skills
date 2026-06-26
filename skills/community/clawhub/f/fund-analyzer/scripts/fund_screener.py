#!/usr/bin/env python3
"""
基金筛选器脚本
根据条件筛选基金排行，支持按收益率、基金类型、规模等筛选
数据来源：天天基金网 (fund.eastmoney.com)
"""

import sys
import json
import argparse
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# 配置
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://fund.eastmoney.com/',
}


# 基金类型映射
FUND_TYPE_MAP = {
    '股票型': 'gp',
    '混合型': 'hh',
    '债券型': 'zq',
    '指数型': 'zs',
    'QDII': 'qdii',
    '货币型': 'hb',
    'LOF': 'lof',
    'FOF': 'fof',
}

# 时间周期映射
RANK_PERIOD_MAP = {
    '近1周': '1w',
    '近1月': '1m',
    '近3月': '3m',
    '近6月': '6m',
    '近1年': '1y',
    '近2年': '2y',
    '近3年': '3y',
    '近5年': '5y',
    '今年来': 'ytd',
    '成立来': 'all',
}


def fetch_fund_ranking(rank_period: str = '1y', fund_type: str = '', top_n: int = 10) -> dict:
    """
    获取基金排行榜
    """
    # 基金排行页面
    url = "https://fund.eastmoney.com/data/fundranking.html"

    # 如果需要特定类型，构建对应URL
    if fund_type:
        type_code = FUND_TYPE_MAP.get(fund_type, '')
        if type_code:
            url = f"https://fund.eastmoney.com/data/fundranking_{type_code}.html"

    try:
        req = Request(url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            return parse_ranking_html(html, rank_period, top_n)
    except HTTPError as e:
        return {"error": f"HTTP错误: {e.code}", "message": "获取排行榜失败"}
    except URLError as e:
        return {"error": "网络错误", "message": str(e)}
    except Exception as e:
        return {"error": "解析错误", "message": str(e)}


def parse_ranking_html(html: str, rank_period: str, top_n: int) -> dict:
    """解析排行榜页面"""
    result = {
        "rank_period": rank_period,
        "funds": [],
    }

    try:
        # 提取基金数据
        # 格式: var rankList = ["代码|名称|类型|...收益率...", ...]
        pattern = r'var\s+rankList\s*=\s*(\[.*?\]);'
        match = re.search(pattern, html, re.DOTALL)

        if not match:
            result["error"] = "未找到排行数据"
            return result

        # 解析数据
        raw_data = match.group(1)
        # 清理数据
        raw_data = raw_data.replace('\\"', '"').replace("\\'", "'")

        # 提取基金列表
        fund_pattern = r'"([^"|]+)\|([^"|]+)\|([^"|]+)\|([^"|]+)"'
        matches = re.findall(fund_pattern, raw_data)

        period_abbr = RANK_PERIOD_MAP.get(rank_period, '1y')
        # 收益率字段位置（根据页面结构调整）
        return_idx = 5  # 默认收益率位置

        for i, m in enumerate(matches[:top_n]):
            if len(m) >= 6:
                result["funds"].append({
                    "rank": i + 1,
                    "code": m[0],
                    "name": m[1],
                    "type": m[2],
                    "return_1y": m[4] if len(m) > 4 else "",
                })

    except Exception as e:
        result["parse_error"] = str(e)

    return result


def format_output(data: dict) -> str:
    """格式化输出结果"""
    if "error" in data:
        return f"❌ 错误: {data['error']}\n   {data.get('message', '')}"

    if not data.get('funds'):
        return "未找到符合条件的基金"

    output = []
    output.append(f"🏆 基金排行榜 - {data.get('rank_period', '近1年')}")
    output.append(f"共 {len(data['funds'])} 只基金")
    output.append("")
    output.append(f"{'排名':<4} {'代码':<8} {'名称':<15} {'类型':<8} {'近1年收益'}")
    output.append("-" * 60)

    for fund in data['funds']:
        output.append(
            f"{fund['rank']:<4} "
            f"{fund['code']:<8} "
            f"{fund['name'][:12]:<15} "
            f"{fund['type'][:6]:<8} "
            f"{fund.get('return_1y', 'N/A')}"
        )

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='基金筛选排行')
    parser.add_argument('--rank', '-r', default='近1年',
                        choices=['近1周', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '近5年', '今年来', '成立来'],
                        help='排行周期 (默认: 近1年)')
    parser.add_argument('--type', '-t', default='',
                        choices=['', '股票型', '混合型', '债券型', '指数型', 'QDII', '货币型', 'LOF', 'FOF'],
                        help='基金类型')
    parser.add_argument('--top', '-n', type=int, default=10,
                        help='显示数量 (默认: 10)')

    args = parser.parse_args()

    print(f"🔍 正在查询{args.type}{args.rank}基金排行前{args.top}名...")
    data = fetch_fund_ranking(args.rank, args.type, args.top)
    print(format_output(data))


if __name__ == "__main__":
    main()
