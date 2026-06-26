#!/usr/bin/env python3
"""
基金持仓分析脚本
查询基金的前十大持仓股票、行业分布、持仓变化等信息
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
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://fund.eastmoney.com/',
}


def fetch_fund_holding(fund_code: str) -> dict:
    """
    获取基金持仓信息
    """
    # 基金持仓API - 使用股票持仓接口
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js"

    try:
        req = Request(url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=15) as response:
            js_content = response.read().decode('utf-8')
            return parse_holding_js(js_content, fund_code)
    except HTTPError as e:
        if e.code == 404:
            return {"error": "基金不存在", "message": f"代码 {fund_code} 的基金未找到"}
        return {"error": f"HTTP错误: {e.code}", "message": "获取持仓失败"}
    except URLError as e:
        return {"error": "网络错误", "message": str(e)}
    except Exception as e:
        return {"error": "获取数据失败", "message": str(e)}


def parse_holding_js(js_content: str, fund_code: str) -> dict:
    """解析JS文件获取持仓数据"""
    result = {
        "fund_code": fund_code,
        "top_holdings": [],
        "industry_distribution": [],
        "quarter": "",
        "stock_position_ratio": 0,
    }

    try:
        # 提取前十大持仓
        # 格式: var data_gg = [[股票代码, 股票名称, 持仓占比, ...], ...]
        patterns = [
            (r'var\s+data_gg\s*=\s*(\[.*?\]);', 'stock'),
            (r'var\s+Data_gg\s*=\s*(\[.*?\]);', 'stock'),
            (r'["\']?data_gg["\']?\s*:\s*(\[.*?\])', 'stock'),
        ]

        holdings_found = False
        for pattern, data_type in patterns:
            match = re.search(pattern, js_content, re.DOTALL)
            if match:
                try:
                    raw_data = match.group(1)
                    raw_data = raw_data.replace("'", '"')

                    # 解析JSON
                    data_list = json.loads(raw_data)

                    for i, item in enumerate(data_list[:10]):
                        if isinstance(item, list) and len(item) >= 3:
                            result["top_holdings"].append({
                                "rank": i + 1,
                                "stock_code": str(item[0]),
                                "stock_name": item[1] if len(item) > 1 else "",
                                "holding_ratio": item[2] if len(item) > 2 else 0,
                            })
                    holdings_found = True
                    break
                except:
                    continue

        if not holdings_found:
            result["note"] = "持仓数据需要从基金详情页获取"

        # 提取股票持仓占比
        stock_ratio_patterns = [
            r'["\']?stock_zb["\']?\s*[:=]\s*["\']?([\d.]+)',
            r'股票持仓\s*[:\s]*([\d.]+)%',
        ]

        for pattern in stock_ratio_patterns:
            match = re.search(pattern, js_content)
            if match:
                result["stock_position_ratio"] = float(match.group(1))
                break

        # 尝试提取行业分布
        # 格式: var data_hy = [[行业, 占比], ...]
        hy_pattern = r'var\s+data_hy\s*=\s*(\[.*?\]);'
        hy_match = re.search(hy_pattern, js_content, re.DOTALL)
        if hy_match:
            try:
                hy_data = json.loads(hy_match.group(1).replace("'", '"'))
                for item in hy_data[:10]:
                    if isinstance(item, list) and len(item) >= 2:
                        result["industry_distribution"].append({
                            "industry": item[0],
                            "ratio": item[1]
                        })
            except:
                pass

        # 提取季度信息
        quarter_pattern = r'["\']?report_date["\']?\s*[:=]\s*["\']?(\d{4}-\d{2}-\d{2})'
        quarter_match = re.search(quarter_pattern, js_content)
        if quarter_match:
            result["quarter"] = quarter_match.group(1)[:7]  # 只取年月

    except Exception as e:
        result["parse_warning"] = f"部分数据解析失败: {str(e)}"

    return result


def format_output(data: dict) -> str:
    """格式化输出结果"""
    if "error" in data:
        return f"❌ 错误: {data['error']}\n   {data.get('message', '')}"

    output = []
    output.append(f"📊 基金持仓分析 - {data.get('fund_code', '')}")

    if data.get('quarter'):
        output.append(f"数据季度: {data['quarter']}")

    if data.get('stock_position_ratio'):
        output.append(f"股票持仓占比: {data['stock_position_ratio']:.2f}%")

    output.append("")

    # 前十大持仓
    if data.get('top_holdings'):
        output.append(f"🏢 前十大持仓股票")
        output.append(f"{'排名':<4} {'代码':<8} {'名称':<12} {'持仓占比'}")
        output.append("-" * 40)

        for stock in data['top_holdings']:
            output.append(
                f"{stock['rank']:<4} "
                f"{stock['stock_code']:<8} "
                f"{stock['stock_name'][:10]:<12} "
                f"{stock['holding_ratio']:.2f}%"
            )
        output.append("")

    # 行业分布
    if data.get('industry_distribution'):
        output.append(f"📈 行业分布")
        for industry in data['industry_distribution']:
            ratio = industry['ratio']
            bar = "█" * int(ratio / 2)
            output.append(f"  {industry['industry']:<12} {industry['ratio']:.1f}% {bar}")

    if data.get('note'):
        output.append("")
        output.append(f"ℹ️ {data['note']}")

    if data.get('parse_warning'):
        output.append(f"⚠️ {data['parse_warning']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='查询基金持仓信息')
    parser.add_argument('fund_code', help='基金代码（6位数字）')

    args = parser.parse_args()

    # 验证基金代码
    fund_code = args.fund_code.strip()
    if not fund_code.isdigit() or len(fund_code) != 6:
        print("❌ 错误: 基金代码应为6位数字")
        sys.exit(1)

    print(f"🔍 正在查询基金 {fund_code} 持仓信息...")
    data = fetch_fund_holding(fund_code)
    print(format_output(data))


if __name__ == "__main__":
    main()
