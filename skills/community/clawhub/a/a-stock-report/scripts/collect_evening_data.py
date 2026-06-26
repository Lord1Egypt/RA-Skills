#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晚报数据采集脚本
合并了 send_evening_report.py 的两融/市值/成交额/风险溢价函数，
统一采集晚报模板所需的全部结构化数据，输出 JSON + 晚报 Markdown。

用法: python3 collect_evening_data.py [--date YYYY-MM-DD] [--dry-run] [--ai-fill]
"""
from __future__ import annotations
import os, sys, json, re, time, warnings
import urllib.request as _ur
import requests as _req
import pandas as pd
from datetime import datetime, date, timezone, timedelta
from typing import Optional, Tuple

# ── 白名单 .env 加载 ──────────────────────────────────────────
# 多路径回退（v3.2.7 修复）：../.env（skill 自带，可选）→ /workspace/.env（项目级，SKILL.md line70 规定）
_REQUIRED_KEYS = ["WECOM_WEBHOOK_KEY"]
for _p in [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
    "/workspace/.env",
]:
    if os.path.exists(_p):
        for line in open(_p):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            if k.strip() in _REQUIRED_KEYS and k.strip() not in os.environ:
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

OUT_FILE = "/tmp/evening_data.json"
OUT_DIR  = "/workspace/projects/A股报告系统/reports"

# ── 全局常量 ────────────────────────────────────────────────
_TZ     = timezone(timedelta(hours=8))
NOW     = datetime.now(_TZ)
TODAY_DATE = NOW.strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def ts():
    return datetime.now(_TZ).strftime("%H:%M:%S")

def prev_trading_day(n=1):
    """返回上一第 n 个工作日的 YYYYMMDD 字符串"""
    d = date.today()
    count = 0
    while count < n:
        d -= timedelta(days=1)
        if d.weekday() < 5:
            count += 1
    return d.strftime("%Y%m%d")

def _fmt_date(trade_date):
    today_s = date.today().strftime("%Y%m%d")
    if trade_date == today_s:
        return "今日"
    d = datetime.strptime(trade_date, "%Y%m%d")
    return f"{d.year}年{d.month}月{d.day}日"

def _timeout_call(func, args, default, timeout_sec=5):
    """线程超时包装，防止 SZSE/BSE 接口卡死"""
    from concurrent.futures import ThreadPoolExecutor
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(func, *args)
            return future.result(timeout=timeout_sec)
    except Exception:
        return default

def _parse_flow(v):
    """解析流量字段：亿/万/万手"""
    if v is None: return 0.0
    v = str(v).strip()
    if "亿" in v:
        try: return float(re.sub(r"[^\d.]", "", v))
        except: return 0.0
    if "万" in v:
        try: return float(re.sub(r"[^\d.]", "", v)) / 10000
        except: return 0.0
    try: return float(re.sub(r"[^\d.]", "", v))
    except: return 0.0

# ═══════════════════════════════════════════════════════════════
# 1. 六大指数（腾讯 qt.gtimg.cn）
# ═══════════════════════════════════════════════════════════════

def get_index_data():
    """六大指数：上证/深证/创业板/科创50/沪深300/中证500
    返回: [{"name": str, "price": float, "pct": float}, ...]"""
    imap = {
        "上证指数": "sh000001", "深证成指": "sz399001",
        "创业板指": "sz399006", "科创50": "sh000688",
        "沪深300": "sh000300", "中证500": "sh000905"
    }
    try:
        url = f"https://qt.gtimg.cn/q={','.join(imap.values())}"
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=10) as r:
            raw = r.read().decode("gbk", errors="replace")
        result = []
        for line in raw.strip().split("\n"):
            fields = line.lstrip("v_").split("~")
            if len(fields) < 33: continue
            code_num = fields[2].strip()
            pct = float(fields[32]) if fields[32] else 0.0
            for name, c in imap.items():
                if c.replace("sh","").replace("sz","") in code_num:
                    result.append({"name": name,
                                   "price": float(fields[3]) if fields[3] else 0.0,
                                   "pct": pct})
                    break
        print(f"  [六大指数] {len(result)}/6 条")
        return result
    except Exception as e:
        print(f"  [六大指数] ⚠️ {e}")
        return []
    return result

# ═══════════════════════════════════════════════════════════════
# 8. 两融余额（akshare macro_china_market_margin_sh/sz）
# ═══════════════════════════════════════════════════════════════

def get_margin_balance_effective() -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    两融余额（亿元）+ 较前日变化。
    数据源：akshare macro_china_market_margin_sh/sz
    返回: (融资余额_亿, delta_亿, 日期字符串)
    """
    try:
        import akshare as ak
        df_sh = ak.macro_china_market_margin_sh()
        df_sz = ak.macro_china_market_margin_sz()
        total = 0.0
        ed = None
        for df in [df_sh, df_sz]:
            df = df.sort_values('日期')
            row = df.iloc[-1]
            total += float(row['融资余额'])   # 单位：元
            ed = row['日期'].strftime("%Y年%m月%d日")
        # 前一日
        pre_sh = df_sh.sort_values('日期').iloc[-2] if len(df_sh) >= 2 else None
        pre_sz = df_sz.sort_values('日期').iloc[-2] if len(df_sz) >= 2 else None
        pre = (float(pre_sh['融资余额']) + float(pre_sz['融资余额'])
               if pre_sh is not None and pre_sz is not None else None)
        delta = round((total - pre) / 1e8, 0) if pre else None  # 元→亿
        print(f"  [两融余额] {ed}={total/1e8:.0f}亿，较前日{'+' if (delta or 0)>=0 else ''}{delta:.0f}亿")
        return total / 1e8, delta, ed
    except Exception as e:
        print(f"  [两融余额] ⚠️ {e}")
        return None, None, None

# ═══════════════════════════════════════════════════════════════
# 9. 两融交易额（akshare）
# ═══════════════════════════════════════════════════════════════

def get_margin_buy_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    两融交易额（亿元）= 融资买入额 + 融券卖出额。
    数据源：akshare macro_china_market_margin_sh/sz
    akshare 字段单位为元 → ÷1e8 转亿。
    若当日无数据，取 T-2 回退。
    返回: (交易额_亿, 日期字符串)
    """
    try:
        import akshare as ak
        df_sh = ak.macro_china_market_margin_sh()
        df_sz = ak.macro_china_market_margin_sz()
        target = datetime.strptime(effective_date, "%Y%m%d").date()
        total = 0.0
        ed = None
        for df in [df_sh, df_sz]:
            row = df[df['日期'] == target]
            if not row.empty:
                r = row.iloc[0]
                total += float(r['融资买入额'])  # 元→亿
                if ed is None:
                    ed = r['日期'].strftime("%Y年%m月%d日")
        # 回退：T-1 通常 T+1 才出，取 T-2
        if total == 0:
            df_all = df_sh.sort_values('日期')
            fb = df_all.iloc[-2] if len(df_all) >= 2 else df_all.iloc[-1]
            total = float(fb['融资买入额'])
            ed = fb['日期'].strftime("%Y年%m月%d日")
            print(f"  [两融交易额] ⚠️ T-1未出，用T-2回退: {ed}={total/1e8:.1f}亿")
        print(f"  [两融交易额] {ed}={total/1e8:.1f}亿")
        return total / 1e8, ed
    except Exception as e:
        print(f"  [两融交易额] ⚠️ {e}")
        return None, None

# ═══════════════════════════════════════════════════════════════
# 7. A股成交额（沪深北三所合计）
# ═══════════════════════════════════════════════════════════════

def _get_bse_turnover(effective_date: str) -> float:
    """北交所成交额（亿元）。超时返回 0。"""
    def _fetch():
        import akshare as ak
        df = ak.stock_bse_summary(date=effective_date)
        if df is None or df.empty:
            return 0.0
        bj_row = df[df['证券类别'] == '股票'].iloc[0]
        amt = float(bj_row.iloc[1]) / 1e8
        print(f"  [北交所成交额] {amt:.1f}亿")
        return amt
    return _timeout_call(_fetch, (), 0.0, timeout_sec=5)

def get_turnover_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    A股成交额（亿元）。沪深北三所合计。
    当日：腾讯实时（沪+深）；历史：akshare 三所加总。
    返回: (成交额_亿, 日期字符串)
    """
    if effective_date == TODAY_DATE:
        try:
            req = _ur.Request("https://qt.gtimg.cn/q=sh000001,sz399001",
                              headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=8) as r:
                raw = r.read().decode("gbk", errors="replace")
            sh = sz = 0.0
            for line in raw.strip().split("\n"):
                parts = line.split("~")
                if len(parts) < 38: continue
                amt = float(parts[37]) / 1e4  # 万元→亿
                if "000001" in parts[2]: sh = amt
                elif "399001" in parts[2]: sz = amt
            total = round(sh + sz, 0)
            ed = NOW.strftime("%Y年%m月%d日")
            print(f"  [成交额] {ed}（T日实时）=沪{sh:.0f}+深{sz:.0f}={total:.0f}亿")
            return total, ed
        except Exception as e:
            print(f"  [成交额] 腾讯实时失败: {e}")

    try:
        import akshare as ak
        # 沪市：成交金额 单位=亿元，直接使用
        df_sh = ak.stock_sse_deal_daily(date=effective_date)
        sh_row = df_sh[df_sh['单日情况'] == '成交金额']
        sh_turn = float(sh_row.iloc[0].get('股票', 0))  # 亿

        # 深市：元 ÷ 1e8 = 亿元
        df_sz = _timeout_call(ak.stock_szse_summary, (effective_date,), None)
        if df_sz is None: raise RuntimeError('SZSE timeout')
        sz_row = df_sz[df_sz['证券类别'] == '股票']
        sz_turn = float(sz_row.iloc[0].get('成交金额', 0)) / 1e8

        # 北交所：元 ÷ 1e8 = 亿元
        bj_turn = _get_bse_turnover(effective_date)

        total = round(sh_turn + sz_turn + bj_turn, 0)
        ed = (datetime.strptime(effective_date, "%Y%m%d") .replace(tzinfo=_TZ)).strftime("%Y年%m月%d日")
        print(f"  [成交额] {ed}=沪{sh_turn:.0f}+深{sz_turn:.0f}+北交所{bj_turn:.0f}={total:.0f}亿")
        return total, ed
    except Exception as e:
        # Fallback：沪市×1.37 估算深市
        try:
            import akshare as ak
            df_sh = ak.stock_sse_deal_daily(date=effective_date)
            sh_row = df_sh[df_sh['单日情况'] == '成交金额']
            sh_turn = float(sh_row.iloc[0].get('股票', 0))
            est = round(sh_turn * 1.37, 0)
            ed = (datetime.strptime(effective_date, "%Y%m%d") .replace(tzinfo=_TZ)).strftime("%Y年%m月%d日")
            print(f"  [成交额] ⚠️ SZSE超时，估算: {ed}=沪{sh_turn:.0f}×1.37={est:.0f}亿")
            return est, ed
        except Exception:
            print(f"  [成交额] ⚠️ {effective_date}: {e}")
            return None, None

# ═══════════════════════════════════════════════════════════════
# 8. A股流通市值（沪深北三所合计）
# ═══════════════════════════════════════════════════════════════

def get_market_cap_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    A股流通市值（亿元）。沪深北三所合计。
    沪市：数据列单位=亿，直接使用。
    深市：元 ÷ 1e8 = 亿元。
    返回: (市值_亿, 日期字符串)
    """
    try:
        import akshare as ak
        # 沪市：单位=亿
        df_sh = ak.stock_sse_deal_daily(date=effective_date)
        sh_row = df_sh[df_sh['单日情况'] == '流通市值']
        sh_cap = float(sh_row.iloc[0].get('股票', 0))  # 亿

        # 深市：元 ÷ 1e8 = 亿元
        df_sz = _timeout_call(ak.stock_szse_summary, (effective_date,), None)
        if df_sz is None: raise RuntimeError('SZSE timeout')
        sz_row = df_sz[df_sz['证券类别'] == '股票']
        sz_cap = float(sz_row.iloc[0].get('流通市值', 0)) / 1e8

        total = round(sh_cap + sz_cap, 0)
        ed = (datetime.strptime(effective_date, "%Y%m%d") .replace(tzinfo=_TZ)).strftime("%Y年%m月%d日")
        print(f"  [流通市值] {ed}=沪{sh_cap:.0f}+深{sz_cap:.0f}={total:.0f}亿={total/10000:.2f}万亿")
        return total, ed
    except Exception as e:
        # Fallback：沪市×1.05 估算深市
        try:
            import akshare as ak
            df_sh = ak.stock_sse_deal_daily(date=effective_date)
            sh_row = df_sh[df_sh['单日情况'] == '流通市值']
            sh_cap = float(sh_row.iloc[0].get('股票', 0))
            est = round(sh_cap * 1.05, 0)
            ed = (datetime.strptime(effective_date, "%Y%m%d") .replace(tzinfo=_TZ)).strftime("%Y年%m月%d日")
            print(f"  [流通市值] ⚠️ SZSE超时，估算: {ed}=沪{sh_cap:.0f}×1.05={est:.0f}亿")
            return est, ed
        except Exception:
            print(f"  [流通市值] ⚠️ {effective_date}: {e}")
            return None, None

# ═══════════════════════════════════════════════════════════════
# 9. PE + 国债 + 风险溢价
# ═══════════════════════════════════════════════════════════════

def get_pe_and_bond(effective_date: str = "") -> dict:
    """
    PE 及风险溢价。整合以下数据源：
    - 沪深300 PE：akshare stock_index_pe_lg（理杏仁数据源）
    - 沪深300 PE分位数：akshare stock_index_pe_lg（5年历史分位）
    - 中证全指 PE：akshare stock_zh_index_value_csindex（数据略有滞后，用作风险溢价代理）
    - 10年国债：akshare bond_china_yield
    - 风险溢价 = 1/中证全指PE - 10年国债收益率
    返回: {hs300_pe, hs300_pct5y, zzqz_pe, bond10y, rep_date, risk_premium}
    """
    result = {'hs300_pe': None, 'hs300_pct5y': None,
              'zzqz_pe': None, 'bond10y': None,
              'rep_date': None, 'risk_premium': None}

    # 10年国债（akshare）
    try:
        import akshare as ak
        for d in ([effective_date] if effective_date else
                  [(datetime.now(_TZ)-timedelta(days=i)).strftime('%Y%m%d') for i in range(5)]):
            try:
                df = ak.bond_china_yield(start_date=d, end_date=d)
                if df is not None and not df.empty:
                    gov = df[df['曲线名称'] == '中债国债收益率曲线']
                    if not gov.empty:
                        row = gov.iloc[0]
                        for c in ['10年', '10Y']:
                            if c in gov.columns:
                                try:
                                    v = float(str(row[c]))
                                    if v > 0:
                                        result['bond10y'] = round(v, 4)
                                        result['rep_date'] = str(row['日期'])[:10]
                                        break
                                except: pass
                        if result['bond10y'] is not None:
                            break
            except: continue
        if result['bond10y']:
            print(f"  [10年国债] {result['bond10y']}%（{result['rep_date']}）")
    except Exception as e:
        print(f"  [10年国债] ⚠️ {e}")

    # 指数 PE（akshare stock_index_pe_lg，理杏仁数据源）
    try:
        import pandas as _pd
        # 沪深300 PE TTM
        df_pe = ak.stock_index_pe_lg(symbol='沪深300')
        df_pe['日期'] = _pd.to_datetime(df_pe['日期'])
        latest_pe = df_pe.iloc[-1]
        result['hs300_pe'] = round(float(latest_pe['滚动市盈率']), 2)
        print(f"  [PE] 沪深300 TTM={result['hs300_pe']}（{latest_pe['日期'].date()}）")

        # 沪深300 PE 5年分位
        # 修复：akshare 返回的'日期'是 datetime64[s]，与带 tz 的 _pd.Timestamp
        # 比较会报「Invalid comparison」；用 naive datetime（去掉 tz）即可
        five_years_ago = (datetime.now(_TZ) - timedelta(days=5*365+30)).replace(tzinfo=None)
        df_5y = df_pe[df_pe['日期'] >= _pd.Timestamp(five_years_ago)]
        if not df_5y.empty:
            pe_series = df_5y['滚动市盈率'].dropna()
            cur_val = df_5y.iloc[-1]['滚动市盈率']
            pct = float((pe_series < cur_val).sum() / len(pe_series) * 100)
            result['hs300_pct5y'] = round(pct, 1)
            print(f"  [沪深300PE分位] 5年分位={result['hs300_pct5y']}%（{pe_series.min():.2f}~{pe_series.max():.2f}）")
    except Exception as e:
        print(f"  [PE] akshare失败: {e}")

    # 中证全指 PE：用 stock_zh_index_value_csindex（数据略有滞后，用作风险溢价代理）
    try:
        df_zz = ak.stock_zh_index_value_csindex(symbol='000985')
        if df_zz is not None and not df_zz.empty:
            _pe_cols = ['市盈率1', '市盈率2']
            for _c in _pe_cols:
                if _c in df_zz.columns:
                    try:
                        _val = float(df_zz[_c].dropna().iloc[0])
                        if _val > 0:
                            result['zzqz_pe'] = round(_val, 2)
                            print(f"  [PE] 中证全指={result['zzqz_pe']}（{_c}，数据滞后约{(datetime.now(_TZ)-df_zz['日期'].max()).days}天）")
                            break
                    except: pass
    except Exception as e:
        print(f"  [PE] 中证全指: {e}")

    # 风险溢价 = 1/中证全指PE - 10年国债
    zz = result.get('zzqz_pe'); bond = result.get('bond10y')
    if zz and bond and zz > 0 and bond > 0:
        result['risk_premium'] = round((1/zz - bond/100)*100, 2)
    if effective_date and len(effective_date) == 8:
        y, m, d = effective_date[:4], effective_date[4:6], effective_date[6:8]
        result['rep_date'] = f'{y}年{m}月{d}日'
    if result.get('bond10y'):
        print(f"  [风险溢价] 中证全指PE={result['zzqz_pe']}, "
              f"国债={result['bond10y']}%, 溢价={result.get('risk_premium')}%")
    return result

# ═══════════════════════════════════════════════════════════════
# 10. 亚太股市（富时A50 + 腾讯恒生/日经/韩综）
# ═══════════════════════════════════════════════════════════════

def get_asia_pacific():
    """亚太股市：富时A50期货、恒生指数、日经225、韩国综合
    返回: [(名称, 现价, 涨跌幅%), ...]

    数据源（按可用性优先级）：
    - 富时A50期货：Sina w.sinajs.cn hf_CHA50CFD（主力连续合约）
    - 恒生/日经/韩综：Sina hq.sinajs.cn b_xxx 系列
      ⚠️ 腾讯 qt.gtimg.cn 早期用 hkHSI/hkJPN225/hkKOR200，
      但日经/韩综 2026-01 后从腾讯下线；改用 sina b_NKY/b_KOSPI/b_HSI。
      批量请求 b_xxx 易被限频，故每个代码单独请求。
    """
    result = []

    # 富时A50期货：Sina w.sinajs.cn hf_CHA50CFD（主力连续合约）
    # ⚠️ w.sinajs.cn 与 hq.sinajs.cn 是 sina 不同子域，但同样有频率限制，
    # 失败时重试 1 次（sleep 3 秒）。
    _got_a50 = False
    for attempt in (1, 2):
        try:
            if attempt == 2:
                time.sleep(3)
            req = _ur.Request("https://w.sinajs.cn/?list=hf_CHA50CFD",
                              headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                       "Referer": "https://finance.sina.com.cn/",
                                       "Accept-Encoding": "gzip, deflate",
                                       "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
            with _ur.urlopen(req, timeout=8) as r:
                raw = r.read()
                if r.info().get("Content-Encoding") == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                raw = raw.decode("gbk", errors="replace")
            for line in raw.strip().split("\n"):
                if "hf_CHA50CFD" not in line:
                    continue
                content = line.split('"')[1] if '"' in line else ""
                if not content:
                    continue
                parts = content.split(",")
                if len(parts) < 14:
                    continue
                price = float(parts[0]) if parts[0] else None
                prev_close = float(parts[7]) if parts[7] else None
                pct = round((price - prev_close) / prev_close * 100, 2) if price and prev_close and prev_close > 0 else None
                result.append(("富时A50期货", price, pct))
                print(f"  [亚太] 富时A50期货={price}, {'↑' if (pct or 0)>=0 else '↓'}{abs(pct or 0):.2f}%")
                _got_a50 = True
                break
        except Exception as e:
            print(f"  [亚太] 富时A50 attempt {attempt}: {e}")
        if _got_a50:
            break
    if not _got_a50:
        print(f"  [亚太] 富时A50: 获取失败")

    # 恒生/日经/韩综：Sina b_xxx（每个代码单独请求，避免被限频）
    # 字段格式: "b_NKY": "日经225指数,66734.02,-200.31,-0.30,..."
    # 索引: 0=名称, 1=现价, 2=涨跌点数, 3=涨跌幅%
    # ⚠️ 同一 session 连续请求 b_xxx 会在第 2 次被 403（sina 反爬），
    # 修复：每请求一次 sleep 3-5 秒，失败时最多重试 1 次
    sina_codes = [
        ("恒生指数", "b_HSI"),
        ("日经225",  "b_NKY"),
        ("韩国综合", "b_KOSPI"),
    ]
    for i, (name, code) in enumerate(sina_codes):
        # 第二次起的请求加间隔，避开 sina hq 接口的频率限制
        if i > 0:
            time.sleep(4)
        price, pct = None, None
        for attempt in (1, 2):
            try:
                url = f"https://hq.sinajs.cn/list={code}"
                req = _ur.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://finance.sina.com.cn/"
                })
                with _ur.urlopen(req, timeout=8) as r:
                    raw = r.read().decode("gbk", errors="replace")
                for line in raw.strip().split("\n"):
                    if code not in line or '""' in line:
                        continue
                    content = line.split('"')[1] if '"' in line else ""
                    if not content:
                        continue
                    parts = content.split(",")
                    if len(parts) < 4:
                        continue
                    price = float(parts[1]) if parts[1] else None
                    pct = float(parts[3]) if parts[3] else None
                    break
                if price is not None:
                    break
            except Exception as e:
                print(f"  [亚太] {name}({code}) attempt {attempt}: {e}")
                if attempt == 1:
                    time.sleep(3)
        if price is not None:
            result.append((name, price, pct))
            print(f"  [亚太] {name}={price}, {'↑' if (pct or 0)>=0 else '↓'}{abs(pct or 0):.2f}%")
        else:
            print(f"  [亚太] {name}({code}): 全部重试失败")
    return result

# ═══════════════════════════════════════════════════════════════
# 11. 构建晚报文本
# ═══════════════════════════════════════════════════════════════

def build_report(indices, data, today_str, ai_news=None, ai_action=None):
    """将数据渲染为晚报 Markdown 文本。逻辑与 send_evening_report.py 完全一致。"""
    rz_ed  = data.get('rz_bal_date')
    mc_ed  = data.get('mkt_cap_date')
    lines  = [f"📋 【A股晚报】{today_str}\n"]

    if indices:
        lines.append("━━━ A股收盘 ━━━")
        for x in indices:
            p = x.get('pct', 0)
            lines.append(f"• {x['name']}：{x['price']:.1f}，{'↑' if p>=0 else '↓'}{abs(p):.2f}%")
        if data.get('turnover'):
            lines.append(f"• 成交额：{data['turnover']/10000:.2f}万亿元")

    lines.append("\n━━━ 亚太股市 ━━━")
    ap = data.get('asia_pacific', [])
    if ap:
        ap_map = {name: (price, pct) for name, price, pct in ap}
        for name, label in [
            ('富时A50期货', '富时A50期货'),
            ('恒生指数', '恒生指数'),
            ('日经225', '日经225'),
            ('韩国综合', '韩国综合'),
        ]:
            if name in ap_map:
                price, pct = ap_map[name]
                extra = '【预判A股明日开盘】' if name == '富时A50期货' else ''
                lines.append(f"• {label}：{price:.0f}，{'↑' if pct>=0 else '↓'}{abs(pct):.2f}% {extra}".rstrip())
            else:
                lines.append(f"• {label}：⚠️暂缺")
    else:
        lines += ["• 富时A50期货：⚠️暂缺","• 恒生指数：⚠️暂缺",
                  "• 日经225：⚠️暂缺","• 韩国综合：⚠️暂缺"]

    rz         = data.get('rz_bal')
    rb         = data.get('rz_buy')
    mc         = data.get('mkt_cap')
    rz_turnover = data.get('rz_turnover')
    rz_to_ed  = data.get('rz_turnover_date')
    delta      = data.get('rz_delta')

    lines.append("\n━━━ 市场风险偏好 ━━━")
    if rz is not None and rz_ed:
        delta_str = f"，较前日{'+' if (delta or 0)>=0 else ''}{delta:.0f}亿" if delta is not None else ""
        lines.append(f"• 两融余额（{rz_ed}）：{rz:.0f}亿{delta_str}")
    else:
        lines.append("• 两融余额：⚠️暂缺")

    if rz is not None and mc is not None and mc > 0 and mc_ed:
        ratio1 = rz / mc * 100
        if not (0.1 < ratio1 < 200):
            lines.append(f"• 两融余额/A股流通市值（{rz_ed}）：⚠️数据波动（待核实）")
            print(f"  [⚠️ 比例异常] rz={rz}亿 mc={mc}亿 ratio={ratio1:.2f}%")
        else:
            safe = "✅ 安全区间" if ratio1 < 3.0 else ("⚠️ 预警区" if ratio1 < 3.5 else "🔴 高危区")
            lines.append(f"• 两融余额/A股流通市值（{rz_ed}）= {ratio1:.2f}%  → {safe}")
    else:
        lines.append("• 两融余额/A股流通市值：⚠️数据暂缺")

    if rz_turnover is not None and rz_turnover > 0:
        ratio2 = rb / rz_turnover * 100
        if ratio2 > 30:
            lines.append(f"• 两融交易额/A股成交额（{rz_ed}）：⚠️数据异常比{ratio2:.0f}%，已忽略")
            print(f"  [⚠️ ratio2异常] rz_buy={rb} rz_turnover={rz_turnover} ratio={ratio2:.0f}%")
        else:
            # rz_to_ed 可能是 YYYYMMDD 或 YYYY年MM月DD日
            if rz_to_ed and "年" in str(rz_to_ed):
                rz_to_ed_fmt = rz_to_ed
            else:
                rz_to_ed_fmt = (datetime.strptime(rz_to_ed, "%Y%m%d").replace(tzinfo=_TZ)).strftime("%Y年%m月%d日") if rz_to_ed else ""
            judgement = "保守" if ratio2 < 7 else ("中性" if ratio2 <= 11 else "过热")
            lines += [
                f"• 两融交易额/A股成交额（{rz_to_ed_fmt}）= {ratio2:.1f}%",
                f"  阈值：<7%保守 | 7-11%中性 | >11%过热",
                f"  → 比例={ratio2:.1f}% → {judgement}",
            ]
    else:
        lines.append("• 两融交易额/A股成交额：⚠️数据暂缺")

    pe = data.get('pe_data', {})
    if pe.get('risk_premium') is not None:
        rp_judge = "高估" if pe['risk_premium'] < 3 else ("中性" if pe['risk_premium'] <= 6 else "低估")
        rep_dt = pe.get('rep_date') or ''
        if rep_dt and len(rep_dt) == 10:
            y, m, d = rep_dt.split('-')
            rep_dt_fmt = f"{y}年{m}月{d}日"
        else:
            rep_dt_fmt = rep_dt
        lines += [
            f"• 股市风险溢价（{rep_dt_fmt}）= {pe['risk_premium']:.2f}%",
            f"  阈值：<3%高估 | 3-6%中性 |>6%低估",
            f"  → 溢价率={pe['risk_premium']:.2f}% → {rp_judge}",
        ]
    else:
        lines.append("• 股市风险溢价：⚠️数据暂缺")

    hs300_pe = pe.get('hs300_pe'); hs300_pct = pe.get('hs300_pct5y')
    today_fmt = NOW.strftime("%Y年%m月%d日")
    if hs300_pe:
        pct_str = f"{hs300_pct:.1f}%" if hs300_pct else "N/A"
        lines.append(f"• 沪深300PE = {hs300_pe:.2f}（近5年分位点={pct_str}，{today_fmt}）")
    else:
        lines.append("• 沪深300PE：⚠️数据暂缺")

    if ai_news:
        lines.append("\n━━━ 财经要闻 ━━━"); lines.extend(ai_news)
    else:
        lines += ["\n━━━ 财经要闻 ━━━", "⚠️暂缺"]
    if ai_action:
        lines.append("\n━━━ 明日操作建议 ━━━"); lines.extend(ai_action)
    else:
        lines += ["\n━━━ 明日操作建议 ━━━",
                  "① 顺势而为：⚠️暂缺","② 超跌博弈：⚠️暂缺","③ 控制仓位：⚠️暂缺"]
    lines.append("\n⚠️ 免责声明：仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

def main(ai_fill: bool = False, target_date: str = None):
    """
    晚报数据采集主流程。
    target_date: 报告目标日期（YYYYMMDD），None 则默认当天。
    数据日期 = T-1 交易日（effective_date）。
    """
    if target_date is None:
        _target = TODAY_DATE
    else:
        _target = target_date.replace("-", "")
    _target_str = (datetime.strptime(_target, "%Y%m%d") .replace(tzinfo=_TZ)).strftime("%Y年%m月%d日")

    # effective_date：晚报数据取前一交易日
    _effective = prev_trading_day(1)
    print(f"\n[{ts()}] 晚报数据采集（目标={_target}，数据={_effective}）...")

    data = {}

    # 六大指数
    print(f"\n[{ts()}] 采集六大指数...")
    data["indices"] = get_index_data()

    

    

    

    # ── 两融/市值/成交额（来自 send_evening_report.py 原有逻辑）────────
    print(f"\n[{ts()}] 采集两融余额...")
    rz_bal, rz_delta, rz_bal_date = get_margin_balance_effective()
    data["rz_bal"]     = rz_bal
    data["rz_delta"]   = rz_delta
    data["rz_bal_date"] = rz_bal_date

    # 若两融余额日期比 effective 更旧，重新取
    if rz_bal_date:
        _rz_date = rz_bal_date.replace('年','').replace('月','').replace('日','')
        if _rz_date < _effective:
            rz_bal_date = None
    if not rz_bal_date:
        rz_bal, rz_delta, rz_bal_date = get_margin_balance_effective()
        data["rz_bal"]       = rz_bal
        data["rz_delta"]     = rz_delta
        data["rz_bal_date"]  = rz_bal_date

    effective_date = (rz_bal_date.replace('年','').replace('月','').replace('日','')
                     if rz_bal_date else _effective)

    print(f"\n[{ts()}] 采集两融交易额...")
    rz_buy, rz_buy_date = get_margin_buy_effective(effective_date)
    data["rz_buy"]      = rz_buy
    data["rz_buy_date"] = rz_buy_date

    print(f"\n[{ts()}] 采集全市场成交额（今日实时）...")
    turnover, to_date = get_turnover_effective(TODAY_DATE)
    data["turnover"]       = turnover
    data["turnover_date"]  = to_date

    print(f"\n[{ts()}] 采集全市场成交额（与两融同日期）...")
    rz_turnover, rz_to_ed = get_turnover_effective(effective_date)
    data["rz_turnover"]       = rz_turnover
    data["rz_turnover_date"]  = rz_to_ed

    print(f"\n[{ts()}] 采集流通市值...")
    mkt_cap, mc_date = get_market_cap_effective(effective_date)
    data["mkt_cap"]       = mkt_cap
    data["mkt_cap_date"]  = mc_date

    # PE + 国债 + 风险溢价
    print(f"\n[{ts()}] 采集PE与风险溢价...")
    data["pe_data"] = get_pe_and_bond(effective_date)

    # 亚太多空
    print(f"\n[{ts()}] 采集亚太股市...")
    data["asia_pacific"] = get_asia_pacific()

    # AI 补数
    _needs_fill = any(v is None for k, v in data.items()
                  if k not in ('indices','market_stats','asia_pacific'))
    if (ai_fill and _needs_fill) or (data.get('rz_buy') or 0) == 0:
        data = ai_supplement(data)

    # 打印摘要
    print(f"\n[{ts()}] 数据汇总:")
    for k, v in [('两融余额', data['rz_bal']), ('两融交易额', data['rz_buy']),
                 ('流通市值', data['mkt_cap']), ('成交额', data['turnover'])]:
        print(f"  {k}：{v}")

    # ── 读取 LLM 生成的 AI 内容（文件由 cron task 预先生成）──────────
    _ai_news_lines, _ai_action_lines = [], []
    _ai_file = "/tmp/evening_report_ai.txt"
    if os.path.exists(_ai_file):
        try:
            _content = open(_ai_file, encoding="utf-8").read()
            _parts = re.split(r'\[(财经要闻|操作建议)\]', _content)
            for i in range(1, len(_parts)-1, 2):
                _section = _parts[i]
                _text = (_parts[i+1] or "").strip()
                _lines = [_l.rstrip() for _l in _text.splitlines() if _l.strip()
                      and not (_l.strip().startswith('━━━') and _l.strip().endswith('━━━'))]
                if _section == "财经要闻" and _text:
                    _ai_news_lines = _lines
                elif _section == "操作建议" and _text:
                    _ai_action_lines = _lines
        except Exception as e:
            print(f"  [AI内容] 读取失败: {e}")
    else:
        print(f"  [AI内容] 文件不存在（{_ai_file}）")

    # 输出 JSON
    data["trade_date"]      = _effective
    data["trade_date_fmt"]  = _fmt_date(_effective)
    data["collected_at"]    = datetime.now(_TZ).isoformat()

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[{ts()}] ✅ JSON 已保存: {OUT_FILE}")

    # 构建并输出晚报
    report = build_report(data["indices"], data, _target_str,
                         ai_news=_ai_news_lines or None,
                         ai_action=_ai_action_lines or None)
    print("\n" + "="*50 + "\n" + report + "\n" + "="*50)
    return report, data

# ── 防重复运行锁（PID + TTL 智能锁）──────────────────
_LOCK_FILE = "/tmp/a_stock_evening.lock"
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lock import lock as _smart_lock, unlock as _smart_unlock

def _acquire_lock():
    if not _smart_lock(_LOCK_FILE, owner=__file__):
        _sys.exit(0)

def _release_lock():
    _smart_unlock(_LOCK_FILE)

# ── 企业微信推送 ──────────────────────────────────────────────
def wx(text: str, max_retries: int = 2) -> int:
    key = os.environ.get("WECOM_WEBHOOK_KEY", "")
    if not key:
        print("  [WX] WECOM_WEBHOOK_KEY 未设置，跳过推送")
        return -1
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key.strip()}"
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}, ensure_ascii=False)
    for attempt in range(max_retries + 1):
        r = _req.post(url, headers={"Content-Type": "application/json"},
                      data=payload.encode("utf-8"), timeout=10)
        try:
            errcode = r.json().get("errcode", -1)
        except Exception:
            errcode = -1
        if errcode == 0:
            return 0
        if attempt < max_retries:
            print(f"  [WX] 发送失败，errcode={errcode}，重试中...")
    return -1

if __name__ == "__main__":
    _acquire_lock()
    _exit_code = 0  # v3.1.2 修复：单一变量，失败路径必须设非 0（v3.1.0 模板同形）
    try:
        import argparse
        _parser = argparse.ArgumentParser()
        _parser.add_argument('--date', default=None)
        _parser.add_argument('--ai-fill', action='store_true')
        _parser.add_argument('--dry-run', action='store_true')
        _args = _parser.parse_args()

        _target = _args.date.replace('-', '') if _args.date else None
        print(f"\n[{ts()}] 第一步：收集数据（目标日期={_target or '今天'}）...")

        report, data = main(ai_fill=_args.ai_fill, target_date=_target)

        if _args.dry_run:
            print(f"\n[{ts()}] dry-run 模式，仅打印报告")
            _exit_code = 0
        else:
            # 保存 Markdown（推送由 send_evening_report.py 统一处理）
            print(f"\n[{ts()}] 第二步：保存 Markdown 报告...")
            os.makedirs(OUT_DIR, exist_ok=True)
            _saved_date = _target or TODAY_DATE
            _path = os.path.join(OUT_DIR, f"晚报_{_saved_date}.md")
            with open(_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"  已保存: {_path}")
    except Exception as e:
        print(f"  ❌ 执行异常（采集崩溃）: {e}")
        import traceback; traceback.print_exc()
        # v3.1.2 修复：采集失败必须让监控看到非 0 退出码
        # notify_failure 自身 try/except 包裹（v3.1.0 教训），不会阻断主流程
        try:
            from _send_lib import notify_failure
            notify_failure("晚报采集", f"脚本执行异常: {e}")
        except Exception as _ne:
            print(f"  [notify_failure 调用失败] {_ne}")
        _exit_code = 1
    finally:
        _release_lock()
        print(f"\n[{ts()}] {'✅ 已完成' if _exit_code == 0 else f'❌ 失败(err={_exit_code})'}")
        sys.exit(_exit_code)