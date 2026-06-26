"""
A股核心企业篮子
贵州茅台 / 宁德时代 / 比亚迪 / 招商银行 / 工商银行 / 美的集团 / 中芯国际 / 立讯精密
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from stock_quote import fetch_stock_quotes, format_stock_quote


CORE_COMPANIES = {
    "sh600519": "贵州茅台",
    "sz300750": "宁德时代",
    "sz002594": "比亚迪",
    "sh600036": "招商银行",
    "sh601398": "工商银行",
    "sz000333": "美的集团",
    "sh688981": "中芯国际",
    "sz002475": "立讯精密",
}


if __name__ == "__main__":
    print("\n=== 🏭 A股核心企业 ===")
    quotes = fetch_stock_quotes(list(CORE_COMPANIES.keys()))
    for item in quotes:
        print(format_stock_quote(item))
