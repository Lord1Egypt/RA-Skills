#!/usr/bin/env python3
"""
基金对比脚本
同时查询多只基金的信息进行对比分析
数据来源：天天基金网 (fund.eastmoney.com)
"""

import sys
import json
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# 配置
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}


def fetch_single_fund(fund_code: str) -> dict:
    """获取单个基金数据"""
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js?v={int(time.time())}"

    try:
        req = Request(url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=10) as response:
            js_content = response.read().decode('utf-8')
            return parse_fund_simple(js_content, fund_code)
    except Exception as e:
        return {
            "fund_code": fund_code,
            "error": str(e)
        }


def parse_fund_simple(js_content: str, fund_code: str) -> dict:
    """简单解析基金数据"""
    import re

    result = {
        "fund_code": fund_code,
    }

    try:
        # 基金名称
        name_patterns = [
            r'["\']?fundName["\']?\s*[:=]\s*["\']?([^"\']+)',
            r'fundName\s*=\s*["\']?([^"\']+)',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, js_content)
            if match:
                result["name"] = match.group(1).strip()
                break

        # 单位净值
        nav_patterns = [
            r'["\']?dwjz["\']?\s*[:=]\s*["\']?([\d.]+)',
            r'["\']?NAV["\']?\s*[:=]\s*["\']?([\d.]+)',
        ]
        for pattern in nav_patterns:
            match = re.search(pattern, js_content)
            if match:
                result["nav"] = match.group(1)
                break

        # 日涨跌幅
        growth_patterns = [
            r'["\']?zzf["\']?\s*[:=]\s*["\']?([-+]?[\d.]+%)',
            r'["\']?dailyGrowth["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)',
        ]
        for pattern in growth_patterns:
            match = re.search(pattern, js_content)
            if match:
                result["daily_growth"] = match.group(1)
                break

        # 各周期收益率
        return_keys = ['sy_1w', 'sy_1m', 'sy_3m', 'sy_6m', 'sy_1y', 'sy_3m', 'sy_3y']
        return_labels = ['近1周', '近1月', '近3月', '近6月', '近1年', '近3年']

        for key, label in zip(return_keys[:len(return_labels)], return_labels):
            pattern = rf'["\']?{key}["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)'
            match = re.search(pattern, js_content)
            if match:
                result[label] = match.group(1) + "%"

        # 基金类型
        type_pattern = r'["\']?fundType["\']?\s*[:=]\s*["\']?([^"\']+)'
        match = re.search(type_pattern, js_content)
        if match:
            result["type"] = match.group(1)

    except Exception as e:
        result["parse_error"] = str(e)

    return result


def compare_funds(fund_codes: list) -> dict:
    """对比多只基金"""
    results = []

    # 并行获取数据
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_single_fund, code): code for code in fund_codes}

        for future in as_completed(futures):
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                results.append({"error": str(e)})

    # 按输入顺序排序
    code_order = {code: i for i, code in enumerate(fund_codes)}
    results.sort(key=lambda x: code_order.get(x.get('fund_code', ''), 999))

    return {
        "funds": results,
        "count": len(results)
    }


def format_output(data: dict) -> str:
    """格式化输出结果"""
    funds = data.get('funds', [])

    if not funds:
        return "未获取到任何基金数据"

    output = []
    output.append("📊 基金对比分析")
    output.append("")

    # 基本信息表格
    output.append(f"{'基金代码':<8} {'基金名称':<15} {'净值':<8} {'日涨跌':<8} {'基金类型'}")
    output.append("-" * 65)

    for fund in funds:
        if "error" in fund:
            output.append(f"{fund.get('fund_code', ''):<8} 数据获取失败")
            continue

        output.append(
            f"{fund.get('fund_code', ''):<8} "
            f"{fund.get('name', 'N/A')[:13]:<15} "
            f"{fund.get('nav', 'N/A'):<8} "
            f"{fund.get('daily_growth', 'N/A'):<8} "
            f"{fund.get('type', 'N/A')}"
        )

    output.append("")

    # 收益率对比
    output.append("📈 收益率对比")
    output.append(f"{'基金代码':<8} {'近1周':<8} {'近1月':<8} {'近3月':<8} {'近6月':<8} {'近1年':<8}")
    output.append("-" * 60)

    for fund in funds:
        if "error" in fund:
            continue
        output.append(
            f"{fund.get('fund_code', ''):<8} "
            f"{fund.get('近1周', '-'):<8} "
            f"{fund.get('近1月', '-'):<8} "
            f"{fund.get('近3月', '-'):<8} "
            f"{fund.get('近6月', '-'):<8} "
            f"{fund.get('近1年', '-'):<8}"
        )

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='对比多只基金')
    parser.add_argument('fund_codes', nargs='+', help='基金代码列表（多个代码用空格分隔）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')

    args = parser.parse_args()

    # 验证基金代码
    valid_codes = []
    for code in args.fund_codes:
        code = code.strip()
        if code.isdigit() and len(code) == 6:
            valid_codes.append(code)
        else:
            print(f"⚠️ 跳过无效代码: {code}")

    if not valid_codes:
        print("❌ 错误: 请提供有效的6位基金代码")
        sys.exit(1)

    print(f"🔍 正在对比 {len(valid_codes)} 只基金...")
    data = compare_funds(valid_codes)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))


if __name__ == "__main__":
    main()
