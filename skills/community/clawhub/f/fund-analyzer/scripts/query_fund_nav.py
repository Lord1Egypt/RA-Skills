#!/usr/bin/env python3
"""
基金净值查询脚本
查询基金的最新净值、日涨跌幅、历史收益等信息
数据来源：天天基金网 (fund.eastmoney.com)
"""

import sys
import json
import time
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote

# 配置
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def fetch_fund_data(fund_code: str) -> dict:
    """
    获取基金数据
    使用天天基金网的API接口
    """
    # 基金概况API
    url = f"https://fund.eastmoney.com/pingzhong.html?ft=type&fdm=0&fs=n&lcf=zqjj&fd=&rt={fund_code}"

    try:
        req = Request(url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            return parse_fund_html(html, fund_code)
    except HTTPError as e:
        return {"error": f"HTTP错误: {e.code}", "message": "请检查基金代码是否正确"}
    except URLError as e:
        return {"error": "网络错误", "message": str(e)}
    except Exception as e:
        return {"error": "解析错误", "message": str(e)}


def parse_fund_html(html: str, fund_code: str) -> dict:
    """解析HTML页面获取基金数据"""
    result = {
        "fund_code": fund_code,
        "fund_name": "",
        "net_value": "",
        "daily_growth": "",
        "history_returns": {},
        "fund_type": "",
        "fund_scale": "",
        "fund_manager": "",
    }

    try:
        # 提取基金名称
        if 'fundName' in html:
            import re
            name_match = re.search(r"fundName\s*[=：]\s*['\"]([^'\"]+)['\"]", html)
            if name_match:
                result["fund_name"] = name_match.group(1)

        # 尝试从JSON数据中提取
        if 'fsrq' in html:
            import re
            # 提取各项数据
            patterns = {
                'fund_name': r"fundName\s*[=：]\s*['\"]([^'\"]+)['\"]",
                'net_value': r"['\"]?dwjz['\"]?\s*[=：]\s*['\"]?([\d.]+)['\"]?",
                'daily_growth': r"['\"]?zzf['\"]?\s*[=：]\s*['\"]?([-+]?[\d.]+%)?['\"]?",
                'fund_type': r"['\"]?fundType['\"]?\s*[=：]\s*['\"]?([^'\"]+)['\"]?",
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, html)
                if match:
                    result[key] = match.group(1).strip()

        # 解析历史收益率（从页面中的表格数据）
        if 'jzzz' in html:
            import re
            # 提取收益率数据
            return_patterns = {
                '近1周': r'近1周\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近1月': r'近1月\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近3月': r'近3月\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近6月': r'近6月\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近1年': r'近1年\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近2年': r'近2年\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '近3年': r'近3年\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '今年来': r'今年来\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
                '成立来': r'成立来\s*</td>\s*<td[^>]*>([-+]?[\d.]+%)',
            }

            for period, pattern in return_patterns.items():
                match = re.search(pattern, html)
                if match:
                    result["history_returns"][period] = match.group(1)

    except Exception as e:
        result["parse_warning"] = f"部分数据解析失败: {str(e)}"

    return result


def format_output(data: dict) -> str:
    """格式化输出结果"""
    if "error" in data:
        return f"❌ 错误: {data['error']}\n   {data.get('message', '')}"

    output = []
    output.append(f"📊 基金基本信息")
    output.append(f"代码: {data.get('fund_code', 'N/A')}")
    output.append(f"名称: {data.get('fund_name', 'N/A')}")
    output.append(f"类型: {data.get('fund_type', 'N/A')}")
    output.append("")

    if data.get('net_value'):
        output.append(f"📈 净值信息")
        output.append(f"单位净值: {data.get('net_value', 'N/A')}")
        output.append(f"日涨跌幅: {data.get('daily_growth', 'N/A')}")
        output.append("")

    if data.get('history_returns'):
        output.append(f"📉 历史收益率")
        for period, value in data['history_returns'].items():
            output.append(f"  {period}: {value}")
        output.append("")

    if data.get('fund_scale'):
        output.append(f"💰 基金规模: {data['fund_scale']}")

    if data.get('fund_manager'):
        output.append(f"👤 基金经理: {data['fund_manager']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='查询基金净值信息')
    parser.add_argument('fund_code', help='基金代码（6位数字）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')

    args = parser.parse_args()

    # 验证基金代码
    fund_code = args.fund_code.strip()
    if not fund_code.isdigit() or len(fund_code) != 6:
        print("❌ 错误: 基金代码应为6位数字")
        sys.exit(1)

    print(f"🔍 正在查询基金 {fund_code}...")
    data = fetch_fund_data(fund_code)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))


if __name__ == "__main__":
    main()
