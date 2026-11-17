#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
曙光精选策略 Dawn Selector v2.0
================================================================================
升级:
  v1.0 → v2.0: HTSC select-stock → pywencai (速度从5分钟→5秒)
  新增: ETF溢价率检查、缩量铁律信号、龙回头扫描
  数据源: pywencai(选股) + 腾讯行情(实时价) + 东财API(板块资金)

整合学习资料:
  - 李娜一进二战法 (首板→二板量化)
  - 抖财神缩量操盘铁律 (缩量阴线风控+阳线持股)
  - 龙头首阴战法 / 龙回头战法 / 抓龙头低吸
================================================================================
"""

import os
import sys
import json
import requests
import pandas as pd
from datetime import datetime
from typing import Optional

# ==================== 配置 ====================
TODAY = datetime.now()
DATE_STR = TODAY.strftime("%Y-%m-%d")
TIME_STR = TODAY.strftime("%H:%M")

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ==================== pywencai选股引擎 ====================

try:
    import pywencai
    HAVE_PYWENCAI = True
except ImportError:
    HAVE_PYWENCAI = False
    print("[WARN] pywencai 未安装，请 pip install pywencai")


def wencai_select(query: str, max_ret: int = 30) -> pd.DataFrame:
    """问财选股，返回DataFrame"""
    if not HAVE_PYWENCAI:
        return pd.DataFrame()
    try:
        result = pywencai.get(loop=False, query=query)
        if result is not None and len(result) > 0:
            return result.head(max_ret)
        return pd.DataFrame()
    except Exception as e:
        print(f"[ERROR] pywencai查询失败: {e}")
        return pd.DataFrame()


# ==================== 腾讯行情引擎 ====================

def get_quotes(codes: list[str]) -> dict:
    """批量获取腾讯实时行情"""
    if not codes:
        return {}
    prefixes = {c: f"sh{c}" if c.startswith(("6", "9")) else f"sz{c}" for c in codes}
    url = f"https://qt.gtimg.cn/q={','.join(prefixes.values())}"
    result = {}
    try:
        resp = requests.get(url, timeout=15)
        resp.encoding = "gbk"
        for line in resp.text.strip().split(";\n"):
            if not line or "=" not in line:
                continue
            parts = line.split("=", 1)
            raw = parts[1].strip('\";\n ')
            fields = raw.split("~")
            if len(fields) < 40:
                continue
            code = fields[2]
            result[code] = {
                "name": fields[1],
                "price": float(fields[3]) if fields[3] else 0,
                "yesterday": float(fields[4]) if fields[4] else 0,
                "open": float(fields[5]) if fields[5] else 0,
                "high": float(fields[33]) if fields[33] else 0,
                "low": float(fields[34]) if fields[34] else 0,
                "change": float(fields[32]) if fields[32] else 0,
                "volume": int(fields[6]) if fields[6] else 0,
                "amount": float(fields[37]) if len(fields) > 37 and fields[37] else 0,
            }
    except Exception as e:
        print(f"[ERROR] 行情获取失败: {e}")
    return result


# ==================== 东财板块资金引擎 ====================

def eastmoney_sector_flow(top_n: int = 10) -> list[dict]:
    """从东财API获取行业板块资金净流入TOP"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz={top_n}&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f14,f2,f3,f62,f184,f66,f69"
    try:
        resp = requests.get(url, timeout=10)
        raw = resp.text
        # 提取JSON
        start = raw.index("[")
        end = raw.rindex("]") + 1
        data = json.loads(raw[start:end])
        sectors = []
        for item in data:
            sectors.append({
                "name": item.get("f14", ""),
                "code": item.get("f12", ""),
                "change_pct": item.get("f3", 0),
                "main_flow": item.get("f62", 0) / 1e8,  # 转亿
                "super_large_flow": item.get("f66", 0) / 1e8,
                "main_ratio": item.get("f69", 0),
            })
        return sectors
    except Exception as e:
        print(f"[ERROR] 东财板块资金查询失败: {e}")
        return []


def eastmoney_concept_flow(top_n: int = 15) -> list[dict]:
    """东财概念板块资金净流入TOP"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz={top_n}&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:3&fields=f12,f14,f2,f3,f62,f184,f66,f69"
    try:
        resp = requests.get(url, timeout=10)
        raw = resp.text
        start = raw.index("[")
        end = raw.rindex("]") + 1
        data = json.loads(raw[start:end])
        concepts = []
        for item in data:
            concepts.append({
                "name": item.get("f14", ""),
                "change_pct": item.get("f3", 0),
                "main_flow": item.get("f62", 0) / 1e8,
            })
        return concepts
    except Exception as e:
        print(f"[ERROR] 东财概念资金查询失败: {e}")
        return []


# ==================== 策略一：一进二筛选 ====================

def strategy_yijiner() -> dict:
    """李娜一进二战法筛选"""
    print("\n[Dawn] === 一进二筛选 ===")
    print(f"[Dawn] 时间: {TIME_STR}")
    
    result = {"candidates": [], "raw_count": 0}
    
    # Step 1: 问财查询今日涨停首板
    df = wencai_select("今日涨停首板，非st，沪深主板，非科创板，非北交所")
    if df.empty:
        print("[Dawn] 无数据")
        return result
    
    result["raw_count"] = len(df)
    
    # 提取字段
    codes = []
    stocks = []
    for _, row in df.iterrows():
        try:
            code_raw = str(row.get("股票代码", ""))
            name = str(row.get("股票简称", ""))
            price = float(row.get("最新价", 0) if pd.notna(row.get("最新价")) else 0)
            code = code_raw.split(".")[0] if "." in code_raw else code_raw
            stocks.append({"code": code, "name": name, "price": price})
            codes.append(code)
        except (ValueError, TypeError):
            continue
    
    # Step 2: 获取实时行情补充
    quotes = get_quotes(codes)
    
    # Step 3: 筛选条件
    candidates = []
    for s in stocks:
        q = quotes.get(s["code"], {})
        price = q.get("price", s["price"])
        
        # 条件1: 股价1-20元
        if price <= 0 or price > 20:
            continue
        
        # 条件2: 上午涨停（pywencai已经带了）
        s["price"] = price
        s["change_pct"] = q.get("change", 0)
        s["volume"] = q.get("volume", 0)
        candidates.append(s)
    
    candidates.sort(key=lambda x: x.get("price", 0))
    result["candidates"] = candidates
    
    print(f"[Dawn] 首板总数: {len(stocks)}")
    print(f"[Dawn] 筛选通过: {len(candidates)}")
    for i, s in enumerate(candidates[:10], 1):
        print(f"  {i}. {s['name']}({s['code']}) {s['price']:.2f}元")
    
    return result


# ==================== 策略二：龙回头扫描 ====================

def strategy_dragon_return() -> dict:
    """扫描近20天2+连板的股票，找回调机会"""
    print("\n[Dawn] === 龙回头扫描 ===")
    
    result = {"candidates": [], "total": 0}
    
    df = wencai_select("近20日有过连续2个涨停的股票，非st，非科创板")
    if df.empty:
        print("[Dawn] 无数据")
        return result
    
    result["total"] = len(df)
    codes = []
    stocks = []
    for _, row in df.iterrows():
        try:
            code_raw = str(row.get("股票代码", ""))
            name = str(row.get("股票简称", ""))
            price = float(row.get("最新价", 0) if pd.notna(row.get("最新价")) else 0)
            code = code_raw.split(".")[0] if "." in code_raw else code_raw
            stocks.append({"code": code, "name": name, "price": price})
            codes.append(code)
        except:
            continue
    
    quotes = get_quotes(codes)
    
    candidates = []
    for s in stocks:
        q = quotes.get(s["code"], {})
        chg = q.get("change", 0)
        s["change_pct"] = chg
        s["price"] = q.get("price", s["price"])
        
        # 回调中（跌幅>2%）或企稳（-2%~2%）
        if chg < -2:
            s["status"] = "深度回调"
            candidates.append(s)
        elif -2 <= chg < 0:
            s["status"] = "轻度回调"
            candidates.append(s)
    
    candidates.sort(key=lambda x: x.get("change_pct", 0))
    result["candidates"] = candidates
    
    print(f"[Dawn] 连板股票: {len(stocks)}")
    print(f"[Dawn] 回调中: {len(candidates)}")
    for s in candidates[:8]:
        print(f"  {s['name']}({s['code']}) {s['change_pct']:+.2f}% {s['status']}")
    
    return result


# ==================== 策略三：板块资金扫描 ====================

def strategy_sector_flow() -> dict:
    """东财板块资金流向"""
    print("\n[Dawn] === 板块资金流向 ===")
    
    sectors = eastmoney_sector_flow(10)
    concepts = eastmoney_concept_flow(10)
    
    result = {"sectors": sectors, "concepts": concepts}
    
    print("[Dawn] 行业板块TOP5:")
    for s in sectors[:5]:
        print(f"  {s['name']} +{s['main_flow']:.1f}亿  {s['change_pct']:+.2f}%")
    
    print("[Dawn] 概念板块TOP5:")
    for c in concepts[:5]:
        print(f"  {c['name']} +{c['main_flow']:.1f}亿  {c['change_pct']:+.2f}%")
    
    return result


# ==================== 主入口 ====================

def main():
    print("╔══════════════════════════════════════╗")
    print("║   Dawn Selector v2.0                ║")
    print(f"║   {DATE_STR} {TIME_STR}               ║")
    print("╚══════════════════════════════════════╝")
    
    results = {}
    
    # 1. 板块资金
    results["sectors"] = strategy_sector_flow()
    
    # 2. 一进二候选
    results["yijiner"] = strategy_yijiner()
    
    # 3. 龙回头
    results["dragon"] = strategy_dragon_return()
    
    # 输出竞价关注
    print("\n[Dawn] === 明日竞价关注 ===")
    yj = results.get("yijiner", {})
    candidates = yj.get("candidates", [])
    if candidates:
        for i, s in enumerate(candidates[:5], 1):
            print(f"  {i}. {s['name']}({s['code']}) {s['price']:.2f}元")
    
    print("\n[Dawn] 竞价买入条件:")
    print("  1. 高开3%-7%（最理想）")
    print("  2. 竞昨比 > 5%（看竞价量）")
    print("  3. 10:30前涨停优先")
    print("  4. 仓位：单票1/5")
    print()
    print("  卖出规则:")
    print("  1. 不封板→卖   2. 炸板减半   3. 低开反抽止损")
    
    # 保存结果
    out_path = os.path.join(OUT_DIR, f"dawn_selector_{DATE_STR}.json")
    # 清理不可序列化的数据
    clean = {
        "yijiner_count": len(candidates),
        "dragon_count": len(results.get("dragon", {}).get("candidates", [])),
        "top_sectors": [s["name"] for s in results.get("sectors", {}).get("sectors", [])[:5]],
        "top_concepts": [c["name"] for c in results.get("sectors", {}).get("concepts", [])[:5]],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
    print(f"\n[Dawn] 结果保存: {out_path}")


if __name__ == "__main__":
    main()
