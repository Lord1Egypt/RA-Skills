#!/usr/bin/env python3
"""A股每日简报生成器 - 使用免费公开数据源"""

import json
import sys
import os
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")

def fetch_json(url, retries=2):
    """带SSL降级的JSON获取"""
    for attempt in range(retries + 1):
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (ssl.SSLError, urllib.error.URLError) as e:
            if attempt < retries and "SSL" in str(e):
                ctx = ssl.create_default_context()
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                        return json.loads(resp.read().decode("utf-8"))
                except Exception:
                    continue
            return None
        except Exception:
            return None
    return None

def get_market_indices():
    """获取主要指数数据"""
    indices = []
    codes = {
        "000001": "上证指数",
        "399001": "深证成指",
        "399006": "创业板指",
        "000688": "科创50",
    }
    for code, name in codes.items():
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=1.{code}&fields=f43,f44,f45,f46,f47,f170&ut=fa5fd1943c7b386f172d6893dbfba10b"
        data = fetch_json(url)
        if data and data.get("data"):
            d = data["data"]
            price = d.get("f43", 0) / 100
            change_pct = d.get("f170", 0) / 100
            change_amt = d.get("f169", 0) / 100
            vol = d.get("f47", 0)
            amt = d.get("f48", 0)
            indices.append({
                "name": name,
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "change_amt": round(change_amt, 2),
                "volume": vol,
            })
    return indices

def get_top_gainers(limit=10):
    """获取涨幅排行"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz={limit}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f2,f3,f12,f14"
    data = fetch_json(url)
    results = []
    if data and data.get("data") and data["data"].get("diff"):
        for item in data["data"]["diff"][:limit]:
            results.append({
                "code": item.get("f12", ""),
                "name": item.get("f14", ""),
                "price": item.get("f2", 0),
                "change_pct": item.get("f3", 0),
            })
    return results

def get_top_losers(limit=10):
    """获取跌幅排行"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz={limit}&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f2,f3,f12,f14"
    data = fetch_json(url)
    results = []
    if data and data.get("data") and data["data"].get("diff"):
        for item in data["data"]["diff"][:limit]:
            results.append({
                "code": item.get("f12", ""),
                "name": item.get("f14", ""),
                "price": item.get("f2", 0),
                "change_pct": item.get("f3", 0),
            })
    return results

def get_sector_performance():
    """获取板块涨跌"""
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f14"
    data = fetch_json(url)
    results = []
    if data and data.get("data") and data["data"].get("diff"):
        for item in data["data"]["diff"][:20]:
            results.append({
                "name": item.get("f14", ""),
                "change_pct": item.get("f3", 0),
            })
    return results

def format_brief(indices, gainers, losers, sectors):
    """格式化简报"""
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]
    
    lines = [f"📊 A股每日简报 | {today} {weekday}", "=" * 40]
    
    # 指数
    lines.append("\n📈 大盘指数")
    for idx in indices:
        arrow = "🟢" if idx["change_pct"] >= 0 else "🔴"
        sign = "+" if idx["change_pct"] >= 0 else ""
        lines.append(f"  {arrow} {idx['name']}: {idx['price']:.2f} ({sign}{idx['change_pct']:.2f}%)")
    
    # 板块
    if sectors:
        lines.append("\n🏭 板块涨跌 TOP10")
        for i, s in enumerate(sectors[:10], 1):
            sign = "+" if s["change_pct"] >= 0 else ""
            lines.append(f"  {i}. {s['name']}: {sign}{s['change_pct']:.2f}%")
    
    # 涨幅榜
    if gainers:
        lines.append("\n🚀 涨幅榜 TOP10")
        for i, g in enumerate(gainers[:10], 1):
            lines.append(f"  {i}. {g['name']}({g['code']}): {g['price']:.2f} +{g['change_pct']:.2f}%")
    
    # 跌幅榜
    if losers:
        lines.append("\n📉 跌幅榜 TOP10")
        for i, l in enumerate(losers[:10], 1):
            lines.append(f"  {i}. {l['name']}({l['code']}): {l['price']:.2f} {l['change_pct']:.2f}%")
    
    lines.append("\n" + "=" * 40)
    lines.append("数据来源：东方财富 | 仅供参考，不构成投资建议")
    
    return "\n".join(lines)

def main():
    args = sys.argv[1:]
    mode = "brief"  # default
    
    if "--json" in args:
        mode = "json"
    elif "--indices" in args:
        mode = "indices"
    elif "--sectors" in args:
        mode = "sectors"
    
    print("🔍 正在获取A股数据...")
    
    indices = get_market_indices()
    if mode == "indices":
        print(json.dumps(indices, ensure_ascii=False, indent=2))
        return
    
    if mode == "sectors":
        sectors = get_sector_performance()
        print(json.dumps(sectors, ensure_ascii=False, indent=2))
        return
    
    gainers = get_top_gainers(10)
    losers = get_top_losers(10)
    sectors = get_sector_performance()
    
    if mode == "json":
        result = {"indices": indices, "gainers": gainers, "losers": losers, "sectors": sectors}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 默认：格式化简报
    print(format_brief(indices, gainers, losers, sectors))

if __name__ == "__main__":
    main()
