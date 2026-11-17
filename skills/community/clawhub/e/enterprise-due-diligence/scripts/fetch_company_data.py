#!/usr/bin/env python3
"""
企业尽调 - 数据采集模块
从企查查等公开数据源获取企业工商信息。

使用方式:
    python fetch_company_data.py "企业名称"
    python fetch_company_data.py "企业名称" --output data.json
"""

import json
import sys
import os
import argparse
from datetime import datetime


# ============================================================
# 企查查公开接口（需要注册获取 Token）
# ============================================================
QICHACHA_API_URL = "https://open.api.qichacha.com"
QICHACHA_TOKEN = os.environ.get("QICHACHA_TOKEN", "")


def qcc_search_company(company_name: str) -> dict:
    """
    通过企查查开放 API 查询企业信息。
    需要先在 https://open.api.qichacha.com 注册并获取 Token，
    然后设置环境变量 QICHACHA_TOKEN。
    """
    if not QICHACHA_TOKEN:
        return {"error": "QICHACHA_TOKEN not configured", "available": False}

    try:
        import requests
        headers = {"Token": QICHACHA_TOKEN}
        params = {"key": company_name}
        resp = requests.get(
            f"{QICHACHA_API_URL}/Company/Search",
            headers=headers,
            params=params,
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"API error: {resp.status_code}", "available": False}
    except ImportError:
        return {"error": "requests library not installed", "available": False}
    except Exception as e:
        return {"error": str(e), "available": False}


def empty_data(company_name: str) -> dict:
    """
    当所有数据源都不可用时，返回空数据结构。
    """
    return {
        "company_name": company_name,
        "data_available": False,
        "data_note": "所有公开数据源不可用。请通过用户提供的文档补充信息。",
        "data_sources": [],
        "basic_info": {
            "name": company_name,
            "credit_code": None,
            "legal_person": None,
            "reg_capital": None,
            "reg_capital_unit": "万元",
            "established_date": None,
            "address": None,
            "business_scope": None,
            "company_type": None,
            "status": None,
            "source": "未获取"
        },
        "equity": [],
        "lawsuits": [],
        "ip": {
            "patents": [],
            "trademarks": [],
            "copyrights": [],
            "patent_count": 0,
            "trademark_count": 0,
            "copyright_count": 0
        },
        "management": [],
        "financing": [],
        "penalties": [],
        "branch_offices": [],
        "change_records": [],
        "forged_person": None
    }


def search_company(company_name: str) -> dict:
    """
    主入口：依次尝试各数据源，合并结果。
    """
    result = empty_data(company_name)

    # 尝试企查查
    qcc_data = qcc_search_company(company_name)
    if qcc_data.get("available", True) and "error" not in qcc_data:
        # 解析企查查数据并填充到 result
        # 根据实际 API 响应格式调整
        result["data_sources"].append("qichacha")
        result["data_available"] = True
        # 这里需要根据企查查 API 实际返回格式做映射
        # 目前留空，后续接入
        pass

    return result


def main():
    parser = argparse.ArgumentParser(description="企业尽调 - 数据采集")
    parser.add_argument("company_name", help="要查询的企业名称")
    parser.add_argument("--output", "-o", help="输出到文件（默认输出到 stdout）")
    args = parser.parse_args()

    data = search_company(args.company_name)

    output = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"数据已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
