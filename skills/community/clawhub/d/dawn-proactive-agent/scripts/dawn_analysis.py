# -*- coding: utf-8 -*-
"""
曙光 多维分析引擎 v1.0 (ai-berkshire/FinRobot Inspired)

四维加权：技术面 + 新闻情绪 + 资金流向 + 量价关系
================================================================
"""
import json, os, urllib.request, time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def log(m): print(f"[ANALYSIS] {m}")

def fetch(url, timeout=10, retries=3):
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        except Exception as e:
            last = e
            if a < retries - 1:
                time.sleep(1)
    raise last


def get_fund_flow(sector_keyword: str) -> float:
    """获取板块资金流向评分 (-30 to +30)
    从东方财富板块资金流API获取主力净流入
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=30&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f14,f62,f184,f66"
    try:
        data = fetch(url)
        items = data.get("data", {}).get("diff", [])
        for item in items:
            name = (item.get("f14") or "").lower()
            if sector_keyword.lower() in name:
                flow = item.get("f62", 0) or 0
                if isinstance(flow, (int, float)):
                    return max(-30, min(30, flow))
        return 0
    except:
        return 0


def get_volume_ratio(quote: Dict) -> float:
    """量比：当前成交量/5日均量"""
    vol = quote.get("volume", 0) or quote.get("f47", 0) or 0
    avg_vol = quote.get("avg_volume", 0) or quote.get("f670", 0) or vol
    if avg_vol <= 0:
        return 1.0
    ratio = vol / avg_vol
    return round(ratio, 2)


def score_by_volume(ratio: float) -> float:
    """量价评分"""
    if ratio > 2.0:
        return 15  # 放量突破
    elif ratio > 1.5:
        return 8
    elif ratio > 1.0:
        return 3
    elif ratio > 0.7:
        return 0
    elif ratio > 0.5:
        return -5  # 缩量
    else:
        return -10  # 严重缩量


def score_by_fund_flow(net_inflow: float) -> float:
    """资金流评分"""
    if net_inflow > 500000000:
        return 15  # &gt;5亿净流入
    elif net_inflow > 100000000:
        return 10  # &gt;1亿
    elif net_inflow > 0:
        return 5
    elif net_inflow > -100000000:
        return -5
    elif net_inflow > -500000000:
        return -10
    else:
        return -15


def multi_dimension_score(
    price_chg: float,
    news_score: float,
    volume_ratio: float,
    fund_flow: float,
    momentum_days: int = 5,
) -> Dict:
    """
    四维综合评分
    
    权重分配:
    - 技术面 (price_chg): 30%
    - 新闻情绪 (news): 25%
    - 资金流 (fund_flow): 25%
    - 量价关系 (volume): 20%
    """
    tech = max(-30, min(30, price_chg * 2.5))  # 30%
    news = max(-30, min(30, news_score))       # 25%
    vol_score = score_by_volume(volume_ratio)   # 20%
    fund = score_by_fund_flow(fund_flow)        # 25%
    
    total = round(tech * 0.30 + news * 0.25 + vol_score * 0.20 + fund * 0.25, 1)
    
    return {
        "total": total,
        "dimensions": {
            "technical": round(tech, 1),
            "news_sentiment": round(news, 1),
            "volume_price": round(vol_score, 1),
            "fund_flow": round(fund, 1),
        },
        "weights": {"technical": 0.30, "news": 0.25, "volume": 0.20, "fund": 0.25},
        "volume_ratio": volume_ratio,
        "raw_fund_flow": fund_flow,
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--sector", type=str, default="", help="查询指定板块资金流")
    args = ap.parse_args()
    
    if args.sector:
        flow = get_fund_flow(args.sector)
        print(f"{args.sector} sector fund flow score: {flow}")
    else:
        # 演示
        demo = multi_dimension_score(2.5, 10, 1.8, 200000000)
        print(json.dumps(demo, ensure_ascii=False, indent=2))
