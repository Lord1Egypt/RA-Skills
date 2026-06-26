#!/usr/bin/env python3
"""
基金历史走势查询脚本
查询基金的历史净值数据、不同时间段的收益率走势
数据来源：天天基金网 (fund.eastmoney.com)
"""

import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

# 配置
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://fund.eastmoney.com/',
}


def get_period_days(period: str) -> int:
    """获取时间段对应的天数"""
    period_map = {
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        '2y': 730,
        '3y': 1095,
        '5y': 1825,
    }
    return period_map.get(period, 365)


def fetch_fund_history(fund_code: str, period: str = '1y') -> dict:
    """
    获取基金历史净值数据
    """
    # 使用天天基金网的净值API
    from datetime import datetime, timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=get_period_days(period))

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    # 基金净值API
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js?v={end_date.strftime('%Y%m%d%H%M%S')}"

    try:
        req = Request(url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=15) as response:
            js_content = response.read().decode('utf-8')
            return parse_history_js(js_content, fund_code, period)
    except HTTPError as e:
        if e.code == 404:
            return {"error": "基金不存在", "message": f"代码 {fund_code} 的基金未找到"}
        return {"error": f"HTTP错误: {e.code}", "message": "请稍后重试"}
    except URLError as e:
        return {"error": "网络错误", "message": str(e)}
    except Exception as e:
        return {"error": "获取数据失败", "message": str(e)}


def parse_history_js(js_content: str, fund_code: str, period: str) -> dict:
    """解析JS文件获取历史数据"""
    import re
    import json as json_lib

    result = {
        "fund_code": fund_code,
        "period": period,
        "data_points": [],
        "statistics": {},
    }

    try:
        # 提取净值数据
        # 格式: var data_net = [[日期, 净值], ...]
        patterns = [
            r'var\s+data_net\s*=\s*(\[.*?\]);',
            r'var\s+Data_net\s*=\s*(\[.*?\]);',
            r'"Data_net"\s*:\s*(\[.*?\])',
        ]

        data_found = False
        for pattern in patterns:
            match = re.search(pattern, js_content, re.DOTALL)
            if match:
                try:
                    # 尝试解析为JSON
                    raw_data = match.group(1)
                    # 处理JavaScript数组格式
                    raw_data = raw_data.replace("'", '"')
                    data_list = json_lib.loads(raw_data)

                    # 转换格式
                    for item in data_list[:100]:  # 限制数据点数量
                        if isinstance(item, list) and len(item) >= 2:
                            result["data_points"].append({
                                "date": str(item[0])[:10] if len(str(item[0])) > 10 else str(item[0]),
                                "nav": item[1] if len(item) > 1 else None
                            })
                    data_found = True
                    break
                except:
                    continue

        if not data_found:
            # 尝试提取其他数据格式
            result["note"] = "净值曲线数据需要进一步解析，请访问基金详情页查看"

        # 提取收益率统计
        return_patterns = {
            '近1周': [r'["\']?sy_1y["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近1周'],
            '近1月': [r'["\']?sy_1m["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近1月'],
            '近3月': [r'["\']?sy_3m["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近3月'],
            '近6月': [r'["\']?sy_6m["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近6月'],
            '近1年': [r'["\']?sy_1y["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近1年'],
            '近3年': [r'["\']?sy_3y["\']?\s*[:=]\s*["\']?([-+]?[\d.]+)', '近3年'],
        }

        for key, (pattern, label) in return_patterns.items():
            match = re.search(pattern, js_content)
            if match:
                result["statistics"][key] = match.group(1) + "%"

    except Exception as e:
        result["parse_warning"] = f"部分数据解析失败: {str(e)}"

    return result


def format_output(data: dict) -> str:
    """格式化输出结果"""
    if "error" in data:
        return f"❌ 错误: {data['error']}\n   {data.get('message', '')}"

    output = []
    output.append(f"📈 基金历史走势 - {data.get('fund_code', '')}")
    output.append(f"查询周期: {data.get('period', '1年')}")
    output.append("")

    if data.get('statistics'):
        output.append(f"📊 各周期收益率")
        for period, value in data['statistics'].items():
            output.append(f"  {period}: {value}")
        output.append("")

    if data.get('data_points'):
        output.append(f"📉 近期净值数据（共 {len(data['data_points'])} 条）")
        for point in data['data_points'][-5:]:
            output.append(f"  {point['date']}: {point.get('nav', 'N/A')}")
        output.append("")

    if data.get('note'):
        output.append(f"ℹ️ {data['note']}")

    if data.get('parse_warning'):
        output.append(f"⚠️ {data['parse_warning']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='查询基金历史走势')
    parser.add_argument('fund_code', help='基金代码（6位数字）')
    parser.add_argument('--period', '-p', default='1y',
                        choices=['1m', '3m', '6m', '1y', '2y', '3y', '5y'],
                        help='查询时间段 (默认: 1y)')

    args = parser.parse_args()

    # 验证基金代码
    fund_code = args.fund_code.strip()
    if not fund_code.isdigit() or len(fund_code) != 6:
        print("❌ 错误: 基金代码应为6位数字")
        sys.exit(1)

    print(f"🔍 正在查询基金 {fund_code} 历史数据...")
    data = fetch_fund_history(fund_code, args.period)
    print(format_output(data))


if __name__ == "__main__":
    main()
