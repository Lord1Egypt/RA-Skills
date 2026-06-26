"""
基金数据 API 模块 - 东方财富数据源

纯 Python 实现，不依赖 akshare

提供函数：
  - fetch_otc_fund_valuation(code)   → 实时估值（当日涨跌/净值）
  - fetch_otc_fund_history(code, days) → 历史净值列表
  - search_fund(keyword)             → 按名称/代码搜索基金

使用方式：
  python3 fund_api.py              # 测试数据获取
  from fund_api import fetch_otc_fund_valuation  # 作为模块导入
"""
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Optional


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://fund.eastmoney.com/",
}


def fetch_otc_fund_valuation(fund_code: str) -> Optional[dict]:
    """
    获取基金实时/最新净值
    - 场外基金(OTC): 使用 fundgz API 获取估算值
    - LOF/ETF基金: 回退到历史净值（当日收盘后更新）
    """
    # 尝试 OTC 基金估算净值 API
    url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            text = resp.read().decode("utf-8")
        match = re.search(r"jsonpgz\((.+)\)", text)
        if match:
            data = json.loads(match.group(1))
            if data.get("name"):
                return {
                    "code": fund_code,
                    "name": data.get("name", ""),
                    "date": data.get("jzrq", ""),
                    "nav": float(data.get("dwjz", 0)),
                    "est_nav": float(data.get("gsz", 0)),
                    "est_change": float(data.get("gszzl", 0)),
                    "gztime": data.get("gztime", ""),
                }
    except Exception:
        pass

    # 回退：从历史净值取最新数据（适用于 LOF/ETF 基金）
    history = fetch_otc_fund_history(fund_code, days=5)
    if history:
        latest = history[0]
        return {
            "code": fund_code,
            "name": "",
            "date": latest.get("date", ""),
            "nav": latest.get("nav", 0),
            "est_nav": latest.get("nav", 0),
            "est_change": latest.get("change", 0),
            "gztime": latest.get("date", ""),
        }
    return None


def fetch_otc_fund_history(fund_code: str, days: int = 90) -> Optional[list]:
    """
    获取基金历史净值（场外/LOF均适用）
    API: https://api.fund.eastmoney.com/f10/lsjz
    """
    url = "https://api.fund.eastmoney.com/f10/lsjz"
    # 分页获取，总共最多取 pagesize 条
    params = f"?fundCode={fund_code}&pageIndex=1&pageSize={days}&startDate=&endDate="
    full_url = url + params

    req = urllib.request.Request(full_url, headers={
        **HEADERS,
        "Referer": f"https://fundf10.eastmoney.com/f10/F10DataApi.aspx?act=f10lsjz&code={fund_code}"
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        records = data.get("Data", {}).get("LSJZList", []) or []
        result = []
        for r in records:
            result.append({
                "date": r.get("FSRQ", ""),
                "nav": float(r.get("DWJZ", 0)),
                "acc_nav": float(r.get("LJJZ", 0)),
                "change": float(r.get("JZZZL", 0)),
                "buy": r.get("SGZT", ""),
                "sell": r.get("SHZT", ""),
            })
        return result
    except Exception as e:
        print(f"[基金API] 获取 {fund_code} 历史净值失败: {e}")
        return None


def fetch_fund_info(fund_code: str) -> Optional[dict]:
    """
    获取基金基本信息（通过天天基金详情页）
    """
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        # 从页面提取基金名称
        name_match = re.search(r"fS_name\s*=\s*[\"']([^\"']+)[\"']", text)
        if not name_match:
            return None
        return {"code": fund_code, "name": name_match.group(1)}
    except Exception as e:
        print(f"[基金API] 获取 {fund_code} 信息失败: {e}")
        return None


def search_fund(keyword: str) -> list:
    """
    搜索基金（场外）
    API: https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx
    """
    import urllib.parse
    params = urllib.parse.urlencode({
        "m": "1", "key": keyword, "type": "2", "v": "0",
        "pagesize": "20", "pageindex": "0", "uid": ""
    })
    url = f"https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?{params}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = []
        for item in (data.get("Datas", []) or [])[:15]:
            # CATEGORY=700 表示基金，非700是股票
            category = item.get("CATEGORY", 0)
            fund_info = item.get("FundBaseInfo", {})
            if category != 700:
                continue
            name = fund_info.get("SHORTNAME", "") or item.get("NAME", "")
            if not name:
                continue
            results.append({
                "code": item.get("CODE", ""),
                "name": name,
                "type": fund_info.get("FTYPE", ""),
                "nav": fund_info.get("DWJZ", ""),
                "nav_date": fund_info.get("FSRQ", ""),
            })
        return results
    except Exception as e:
        print(f"[基金API] 搜索基金 '{keyword}' 失败: {e}")
        return []


if __name__ == "__main__":
    # 测试
    print("=== 测试基金估值 ===")
    r = fetch_otc_fund_valuation("161226")
    print(r)

    print("\n=== 测试历史净值 ===")
    h = fetch_otc_fund_history("161226", days=5)
    print(h)

    print("\n=== 测试基金搜索 ===")
    s = search_fund("白银")
    print(s)
