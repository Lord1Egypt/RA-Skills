#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晨报数据采集脚本
采集隔夜全球市场数据，写入 /tmp/morning_data.json，供后续 LLM 生成晨报内容。
用法：
  python3 collect_morning_data.py              # 采集所有数据
  python3 collect_morning_data.py --test      # 测试模式，打印数据不写文件
  python3 collect_morning_data.py --date 20260528  # 指定前一交易日（YYYYMMDD格式）
"""
from __future__ import annotations
import sys, os, warnings, json, re, time
from datetime import datetime, timezone, timedelta, date as _date
from typing import Optional, Tuple

warnings.filterwarnings('ignore')

# ── 配置加载（白名单读取外部配置，路径可通过 ENV_FILE 系列变量覆盖）──────────────
_REQUIRED_KEYS = ["IWENCAI_API_KEY"]
for _p in (
    os.environ.get("ENV_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")),
    os.environ.get("ENV_FILE_FALLBACK", "/workspace/.env"),
):
    if not os.path.exists(_p):
        continue
    try:
        for _line in open(_p):
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            if _k in _REQUIRED_KEYS and _k not in os.environ:
                os.environ[_k] = _v.strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        continue

_TZ  = timedelta(hours=8)
NOW  = datetime.now(timezone.utc) + _TZ
TODAY_DATE = NOW.strftime("%Y%m%d")
TODAY_STR  = NOW.strftime("%Y年%m月%d日")
WEEKDAY_CN = ["一","二","三","四","五","六","日"][NOW.weekday()]

def prev_trading_day(date_str: str) -> str:
    """返回前一交易日 YYYYMMDD（跳过周末）"""
    dt = datetime.strptime(date_str, "%Y%m%d")
    for i in range(1, 8):
        d = (dt - timedelta(days=i)).strftime("%Y%m%d")
        if datetime.strptime(d, "%Y%m%d").weekday() < 5:
            return d
    return date_str

DEFAULT_TRADE_DATE = prev_trading_day(TODAY_DATE)
TRADE_STR = datetime.strptime(DEFAULT_TRADE_DATE, "%Y%m%d").strftime("%Y年%m月%d日")

# ── 问财 API 调用（进程内直连，替代 subprocess 外部调用）───────
def _iwencai_query(query: str, limit: str = "1", api_key: str = "") -> dict:
    """
    进程内直连问财 OpenAPI，不启动子进程，不泄露环境变量。
    返回 {"datas": [...], "code_count": N} 或 {"datas": []}（失败时）。
    """
    key = api_key or os.environ.get("IWENCAI_API_KEY", "")
    if not key:
        raise RuntimeError("IWENCAI_API_KEY 环境变量未设置，请联系管理员配置。")
    import secrets, urllib.request, urllib.error
    url = "https://openapi.iwencai.com/v1/query2data"
    trace_id = secrets.token_hex(32)
    payload = json.dumps({
        "query": query, "page": "1", "limit": limit,
        "is_cache": "1", "expand_index": "true"
    }).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "X-Claw-Call-Type": "normal",
        "X-Claw-Skill-Id": "hithink-sector-selector",
        "X-Claw-Skill-Version": "1.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": trace_id,
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ════════════════════════════════════════════════════════════
# 1. 美股数据：腾讯行情 usDJI/usINX/usIXIC
# ════════════════════════════════════════════════════════════
def get_us_indices() -> dict:
    """道琼斯、标普500、纳斯达克"""
    result = {}
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://qt.gtimg.cn/q=usDJI,usINX,usIXIC",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("gbk", errors="replace")
        for line in raw.strip().split("\n"):
            f = line.lstrip("v_").split("~")
            if len(f) < 33: continue
            code = f[2].strip()
            price = float(f[3]) if f[3] else None
            pct   = float(f[32]) if f[32] else None
            if "DJI"   in code and price: result["道琼斯"]   = {"price": round(price, 2), "pct": round(pct, 2)}
            elif "IXIC" in code and price: result["纳斯达克"]  = {"price": round(price, 2), "pct": round(pct, 2)}
            elif "INX"  in code and price: result["标普500"]  = {"price": round(price, 2), "pct": round(pct, 2)}
        for k, v in result.items():
            print(f"  [美股] {k}: {v['price']:,.2f} {v['pct']:+.2f}%")
    except Exception as e:
        print(f"  [美股] ❌ {e}")
    return result

# ════════════════════════════════════════════════════════════
# 2. VIX 恐慌指数
# ════════════════════════════════════════════════════════════
def get_vix() -> dict:
    """CBOE美股恐慌指数（新浪 znb_VIX，CBOE VIX 指数本身）

    (2026-06-17 改) 使用 _sina_fetcher 公共函数, 多 UA 轮换 + 5s 退避 + 3 次重试
    """
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        from _sina_fetcher import sina_get_vix
        result = sina_get_vix()
        if result.get("value") is not None:
            print(f"  [VIX] 新浪znb_VIX={result['value']:.2f} 涨跌{result['pct']:.2f}% [{result['level']}]")
        return result
    except Exception as exc_sina:
        print(f"  [VIX] 新浪znb_VIX失败: {exc_sina}")
        return {"value": None, "pct": None, "source": None}

# ════════════════════════════════════════════════════════════
# 3. 港股 + A50期货
# ════════════════════════════════════════════════════════════
def get_hk_a50() -> dict:
    """恒生指数 + 富时中国A50期货"""
    result = {}
    import urllib.request

    # 富时中国A50期货（CHA50CFD）：双数据源模式
    # ────────────────────────────────────────────────
    # 数据源 1（首选）：新浪海外期货 hq.sinajs.cn/list=hf_CHA50CFD
    #   字段（实测）：现价,昨收(空),今开,字段3,字段4,字段5,时间,字段7,字段8,成交量,字段10,字段11,日期,名称,字段14
    #   关键：现价在 14000-16000 区间 → 真实期货指数；昨收空（凌晨非交易时段）→ 用"今开"作前值参考
    # 数据源 2（备份）：东方财富 push2his.eastmoney.com（secid=104.CN00Y，SGX 期货连续合约）
    # 严禁用华夏A50ETF(sh512550)作 fallback —— 与富时A50期货指数是完全不同标的！
    # 严禁用 1.x 范围价格填空 —— 期货指数价格量级 14000+
    # ────────────────────────────────────────────────

    a50_futures_ok = False

    # 数据源 1：新浪 hf_CHA50CFD
    try:
        req1 = urllib.request.Request(
            "https://hq.sinajs.cn/list=hf_CHA50CFD",
            headers={"User-Agent": "Mozilla/5.0",
                     "Referer": "https://finance.sina.com.cn/"})
        with urllib.request.urlopen(req1, timeout=8) as r1:
            raw1 = r1.read().decode("gbk", errors="replace")
        m1 = re.search(r'hq_str_hf_CHA50CFD="(.+?)"', raw1)
        if m1:
            vals = m1.group(1).split(",")
            if len(vals) >= 6:
                price = float(vals[0])  # 现价
                prev  = float(vals[1]) if vals[1] else 0  # 昨收（凌晨非交易时段为空）
                open_ = float(vals[2]) if len(vals) > 2 and vals[2] else 0  # 今开
                # 范围校验：真实期货指数价 14000-16000
                if 10000 < price < 20000:
                    # 优先用昨收，昨收空时用今开作前值（亚盘开市≈前日结算）
                    ref_price = prev if prev else (open_ if open_ else price)
                    pct = round((price - ref_price) / ref_price * 100, 2) if ref_price else 0.0
                    result["富时A50期货"] = {
                        "price": round(price, 2),
                        "pct": pct,
                        "prev": round(ref_price, 2) if ref_price else None,
                        "source": "Sina-hf-CHA50CFD",
                        "note": "" if prev else "亚盘早盘，前值为今开参考"
                    }
                    a50_futures_ok = True
                    print(f"  [A50] 富时中国A50期货(Sina): {price:,.2f} {pct:+.2f}% (前值 {ref_price:,.2f})")
                else:
                    print(f"  [A50] Sina hf_CHA50CFD 价格 {price} 超出期货指数量级(14000-16000)，疑似错源")
    except Exception as e1:
        print(f"  [A50] Sina-hf-CHA50CFD 失败: {e1}")

    # 数据源 2：东方财富 push2his（secid=104.CN00Y，仅在数据源 1 失败时启用）
    if not a50_futures_ok:
        try:
            import gzip
            url_em = "https://push2his.eastmoney.com/api/qt/stock/get?secid=104.CN00Y&fields=f43,f44,f45,f46,f60,f169,f170"
            req2 = urllib.request.Request(
                url_em,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://quote.eastmoney.com/globalfuture/CN00Y.html",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                })
            with urllib.request.urlopen(req2, timeout=10) as r2:
                raw2 = r2.read()
                if r2.headers.get('Content-Encoding', '') == 'gzip':
                    raw2 = gzip.decompress(raw2)
            j2 = json.loads(raw2.decode("utf-8", errors="ignore"))
            d2 = j2.get("data")
            if d2 and d2.get("f43"):
                # f43=现价(×100)，f60=昨收(×100)，f169=涨跌额(×100)，f170=涨跌幅(×100)
                price = d2["f43"] / 100
                prev  = d2["f60"] / 100
                pct   = d2["f170"] / 100
                if 10000 < price < 20000:
                    result["富时A50期货"] = {
                        "price": round(price, 2),
                        "pct": round(pct, 2),
                        "prev": round(prev, 2),
                        "source": "EM-push2-104.CN00Y",
                        "note": ""
                    }
                    a50_futures_ok = True
                    print(f"  [A50] 富时中国A50期货(EM): {price:,.2f} {pct:+.2f}% (昨收 {prev:,.2f})")
        except Exception as e2:
            print(f"  [A50] EM-push2-104.CN00Y 失败: {e2}")

    # 数据源 3：东方财富 push2（无 his，secid=104.CN00Y，仅在 1+2 都失败时启用）
    if not a50_futures_ok:
        try:
            url_em2 = "https://push2.eastmoney.com/api/qt/stock/get?secid=104.CN00Y&fields=f43,f44,f45,f46,f60,f169,f170"
            req3 = urllib.request.Request(
                url_em2,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://quote.eastmoney.com/",
                    "Accept": "*/*",
                })
            with urllib.request.urlopen(req3, timeout=10) as r3:
                raw3 = r3.read()
                if r3.headers.get('Content-Encoding', '') == 'gzip':
                    raw3 = gzip.decompress(raw3)
            j3 = json.loads(raw3.decode("utf-8", errors="ignore"))
            d3 = j3.get("data")
            if d3 and d3.get("f43"):
                price = d3["f43"] / 100
                prev  = d3["f60"] / 100
                pct   = d3["f170"] / 100
                if 10000 < price < 20000:
                    result["富时A50期货"] = {
                        "price": round(price, 2),
                        "pct": round(pct, 2),
                        "prev": round(prev, 2),
                        "source": "EM-push2his-104.CN00Y",
                        "note": ""
                    }
                    print(f"  [A50] 富时中国A50期货(EM-fallback): {price:,.2f} {pct:+.2f}% (昨收 {prev:,.2f})")
        except Exception as e3:
            print(f"  [A50] EM-push2his 失败: {e3}")

    # 恒生指数：腾讯 qt.gtimg.cn hkHSI
    try:
        req = urllib.request.Request(
            "https://qt.gtimg.cn/q=hkHSI",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("gbk", errors="replace")
        f = raw.strip().split("~")
        if len(f) >= 6:
            price = float(f[3]) if f[3] else None
            pct   = float(f[32]) if f[32] else None
            if price:
                result["恒生指数"] = {"price": round(price, 2), "pct": round(pct, 2)}
                print(f"  [港股] 恒生指数: {price:,.0f} {pct:+.2f}%")
    except Exception as e3:
        print(f"  [港股] 腾讯接口失败: {e3}")

    return result

# ════════════════════════════════════════════════════════════
# 4. 大宗商品
# ════════════════════════════════════════════════════════════
def get_commodities(trade_date: str = "") -> dict:
    """
    WTI原油 + 现货黄金（akshare futures_hf_em 全球期货现货报价）。
    数据源：akshare.futures.futures_hf_em.futures_global_spot_em()
      - GC00Y = COMEX黄金（主力连续合约，USD/金衡盎司）
      - CL00Y = NYMEX WTI原油（主力连续合约，USD/桶）
    """
    result = {}

    try:
        import akshare as ak
        from akshare.futures import futures_hf_em
        df = futures_hf_em.futures_global_spot_em()

        gc = df[df["代码"] == "GC00Y"]
        if not gc.empty:
            row = gc.iloc[0]
            price = float(row["最新价"])
            pct   = float(row["涨跌幅"]) if row["涨跌幅"] is not None else 0.0
            result["现货黄金"] = {"price": round(price, 2), "pct": round(pct, 2), "unit": "美元/盎司", "source": "COMEX/akshare"}
            print(f"  [商品] 现货黄金(COMEX): ${price:.2f} {pct:+.2f}%")

        cl = df[df["代码"] == "CL00Y"]
        if not cl.empty:
            row = cl.iloc[0]
            price = float(row["最新价"])
            pct   = float(row["涨跌幅"]) if row["涨跌幅"] is not None else 0.0
            result["WTI原油"] = {"price": round(price, 2), "pct": round(pct, 2), "unit": "美元/桶", "source": "NYMEX/akshare"}
            print(f"  [商品] WTI原油(NYMEX): ${price:.2f} {pct:+.2f}%")
    except Exception as exc:
        print(f"  [商品] akshare失败: {exc}")

    return result


# ════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════
# 主函数
# ════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(description="晨报数据采集")
    parser.add_argument("--test", action="store_true", help="测试模式（打印不写文件）")
    parser.add_argument("--date", default="", help="前一交易日 YYYYMMDD")
    args = parser.parse_args()

    trade_date = args.date or DEFAULT_TRADE_DATE

    print(f"[晨报数据采集] 报告日期={TODAY_STR}（{WEEKDAY_CN}），数据取自={TRADE_STR}")
    print("=" * 60)

    us = get_us_indices()
    vix = get_vix()
    hk_a50 = get_hk_a50()
    commodities = get_commodities(trade_date)

    print("=" * 60)
    print(f"数据采集完成")
    print(f"  报告日期：{TODAY_STR}（{WEEKDAY_CN}）")
    print(f"  数据日期：{TRADE_STR}")
    print(f"  美股数据：{len(us)} 项")
    print(f"  VIX：{vix.get('value')} [{vix.get('level', 'N/A')}]")
    print(f"  港股/A50：{len(hk_a50)} 项")
    print(f"  大宗商品：{len(commodities)} 项")
    print("=" * 60)

    output = {
        "report_date": TODAY_STR,
        "report_weekday": WEEKDAY_CN,
        "trade_date": TRADE_STR,
        "us_indices": us,
        "vix": vix,
        "hk_a50": hk_a50,
        "commodities": commodities,
    }

    print("\n[完整数据 JSON]")
    print(json.dumps(output, ensure_ascii=False, indent=2))

    if not args.test:
        out_path = "/tmp/morning_data.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\n[已写入] {out_path}")

if __name__ == "__main__":
    main()