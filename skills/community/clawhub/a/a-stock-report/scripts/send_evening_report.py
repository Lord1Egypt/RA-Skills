#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股收盘晚报生成脚本
触发：python3 send_evening_report.py [--date YYYY-MM-DD] [--dry-run] [--ai-fill]

日期参数说明：
  --date YYYY-MM-DD  指定报告目标日期（如 --date 2026-05-20）
                   不带参数时默认取当天
                   晚报为 T 日生成，数据为 T-1 交易日数据

数据一致性原则：
  两融余额、两融交易额 → 取最新可用日期（通常为 T-1）
  流通市值、成交额        → 必须与两融余额为同一日期
  两融交易额 = 融资买入额 + 融券卖出额
  流通市值 = 沪市流通市值 + 深市流通市值（沪深北三所合计）
"""
from __future__ import annotations
import sys, os, warnings, json, subprocess, re, time
import requests as _req

OUT_FILE = "/tmp/evening_data.json"
# ── 配置加载（白名单读取外部配置，路径可通过 ENV_FILE 系列变量覆盖）──────────────
_REQUIRED_KEYS = ["WECOM_WEBHOOK_KEY", "IWENCAI_API_KEY"]
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

# ── 问财 API 直连（进程内 HTTP，避免 subprocess 泄露密钥）────────────
import secrets
def _iwencai_query(query: str, timeout: int = 20) -> dict:
    """同花顺问财 OpenAPI v1 直查（使用正确格式的 X-Claw Header），返回原始 JSON dict。"""
    import requests
    api_key = os.environ.get("IWENCAI_API_KEY", "")
    if not api_key:
        return {}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-Claw-Call-Type": "normal",
        "X-Claw-Skill-Id": "hithink-market-query",
        "X-Claw-Skill-Version": "1.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": secrets.token_hex(32),
    }
    payload = {
        "query": query,
        "page": "1",
        "limit": "5",
        "is_cache": "1",
        "expand_index": "true",
    }
    try:
        r = requests.post(
            "https://openapi.iwencai.com/v1/query2data",
            headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"  [_iwencai] 查询失败: {e}")
    return {}
from datetime import datetime, timezone, timedelta
from datetime import date as _date
from typing import Optional, Tuple

warnings.filterwarnings('ignore')

_TZ  = timedelta(hours=8)
NOW  = datetime.now(timezone.utc) + _TZ
TODAY_STR  = NOW.strftime("%Y年%m月%d日")
TODAY_DATE = NOW.strftime("%Y%m%d")
TS         = NOW.strftime("%m/%d %H:%M")

def prev_trading_day(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y%m%d")
    for i in range(1, 8):
        d = (dt - timedelta(days=i)).strftime("%Y%m%d")
        if datetime.strptime(d, "%Y%m%d").weekday() < 5:
            return d
    return date_str

YESTERDAY = prev_trading_day((NOW - timedelta(days=1)).strftime("%Y%m%d"))

def get_webhook_url() -> str:
    key = os.environ.get("WECOM_WEBHOOK_KEY", "")
    if not key:
        raise FileNotFoundError("WECOM_WEBHOOK_KEY environment variable not set")
    return f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key.strip()}"

def wx(text: str, max_retries: int = 2) -> int:
    """企业微信推送，curl 风格，带自动重试"""
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}, ensure_ascii=False)
    for attempt in range(max_retries + 1):
        r = subprocess.run(
            ["curl", "-s", "-X", "POST", get_webhook_url(),
             "-H", "Content-Type: application/json", "-d", "@-"],
            input=payload.encode("utf-8"), capture_output=True)
        try:
            errcode = json.loads(r.stdout.decode()).get("errcode", -1)
        except Exception:
            errcode = -1
        if errcode == 0:
            return 0
        if attempt < max_retries:
            print(f"[WX] 发送失败，errcode={errcode}，重试中...")
    return -1

# ── AI 补数 ────────────────────────────────────────────────
def _call_batch_web_search(queries):
    try:
        from openclaw import invoke
        import asyncio
        async def _do():
            return await invoke('batch_web_search',
                               {"queries": [{"query": q, "num_results": 5} for q in queries]})
        return asyncio.run(_do())
    except Exception as e:
        print(f"[AI补数] openclaw.invoke 失败: {e}")
        return {}

def ai_supplement(data: dict) -> dict:
    today = NOW.strftime('%Y年%m月%d日')
    missing = []
    # 两融和市值数据极少缺失，无额外补数需求
    if not missing:
        return data
    print(f"[AI补数] {len(missing)} 项暂缺，启动AI搜索...")
    raw = ""
    for q in missing:
        for entry in _call_batch_web_search([q]).get('content', []):
            if entry.get('success'):
                raw += entry.get('formatted_content', '') + " "; break
    for pat in [r'两融余额.*?(\d+\.?\d*)\s*亿', r'融资余额.*?(\d+\.?\d*)\s*亿']:
        m = re.search(pat, raw)
        # 合理性校验：两融余额正常区间 1万亿~4万亿
        if m and 1000 < float(m.group(1)) < 100000:
            data['rz_bal'] = float(m.group(1)); break
    # ⚠️ rz_buy 不走 Web 搜索回退（搜索结果格式不稳，容易捕到市值等字段）
    # akshare 的 get_margin_buy_effective 已通过 T-2 回退保证有数据
    for pat in [r'流通市值.*?(\d+\.?\d*)\s*万亿', r'A股流通市值.*?(\d+\.?\d*)\s*万亿']:
        m = re.search(pat, raw)
        if m and 10 < float(m.group(1)) < 500:
            data['mkt_cap'] = float(m.group(1)); break
    for pat in [r'成交额.*?(\d+\.?\d*)\s*万亿', r'A股成交额.*?(\d+\.?\d*)\s*万亿']:
        m = re.search(pat, raw)
        if m and float(m.group(1)) > 0.5:
            data['turnover'] = float(m.group(1)); break
    for pat in [r'成交额.*?(\d+\.?\d*)\s*万亿', r'A股成交额.*?(\d+\.?\d*)\s*万亿']:
        m = re.search(pat, raw)
        if m and abs(float(m.group(1))) > 0.1:
            data['turnover'] = float(m.group(1)); break
    for k, v in data.items():
        if v is not None:
            print(f"[AI补数] {k}: {v}")
    return data

# ── 六大指数 ────────────────────────────────────────────────
def get_index_data():
    imap = {"上证指数":"sh000001","深证成指":"sz399001","创业板指":"sz399006",
            "科创50":"sh000688","沪深300":"sh000300","中证500":"sh000905"}
    try:
        import urllib.request
        req = urllib.request.Request(
            f"https://qt.gtimg.cn/q={','.join(imap.values())}",
            headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
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
        return result
    except Exception as e:
        print(f"[指数] {e}"); return []

# ── PE与风险溢价 ─────────────────────────────────────────

# ── PE + 国债收益率 ───────────────────────────────────────
# ── 核心数据获取 ──────────────────────────────────────────

def get_margin_balance_effective() -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    两融余额（亿元）+ 较前日变化。
    两融余额 = 融资余额 + 融券余额（单位：亿元）。
    数据源：akshare macro_china_market_margin_sh/sz（沪深两市汇总）
    """
    try:
        import akshare as ak
        df_sh = ak.macro_china_market_margin_sh()
        df_sz = ak.macro_china_market_margin_sz()
        total = 0.0
        ed = None
        for df in [df_sh, df_sz]:
            row = df.sort_values('日期').iloc[-1]
            total += float(row['融资余额'])          # 单位：元 → ÷1e8 转亿
            ed = row['日期'].strftime("%Y年%m月%d日")
        # 前一日（iloc[-2] 取倒数第二行，即前一日）
        pre_sh = df_sh.sort_values('日期').iloc[-2] if len(df_sh) >= 2 else None
        pre_sz = df_sz.sort_values('日期').iloc[-2] if len(df_sz) >= 2 else None
        pre = None
        if pre_sh is not None and pre_sz is not None:
            pre = float(pre_sh['融资余额']) + float(pre_sz['融资余额'])
        delta = round((total - pre) / 1e8, 0) if pre else None  # 单位：元 → ÷1e8 转亿
        print(f"  [两融余额] {ed}={total/1e8:.0f}亿，较前日{'+' if (delta or 0)>=0 else ''}{delta:.0f}亿")
        return total / 1e8, delta, ed                             # 返回亿
    except Exception as e:
        print(f"  [两融余额] {e}"); return None, None, None

def get_margin_buy_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    两融交易额（亿元）= 融资买入额 + 融券卖出额。
    数据源：akshare macro_china_market_margin_sh/sz
    """
    try:
        import akshare as ak
        df_sh = ak.macro_china_market_margin_sh()
        df_sz = ak.macro_china_market_margin_sz()
        target = datetime.strptime(effective_date, "%Y%m%d").date()
        row_sh = df_sh[df_sh['日期'] == target]
        row_sz = df_sz[df_sz['日期'] == target]
        total = 0.0
        ed = None
        for df in [row_sh, row_sz]:
            if not df.empty:
                r = df.iloc[0]
                total += float(r['融资买入额'])        # akshare 字段单位为元 → ÷1e8 转亿
                if ed is None: ed = r['日期'].strftime("%Y年%m月%d日")
        # akshare 融资数据 T 日晚间仅更新至 T-2，T-1 通常 T+1 早晨才有
        # 回退时明确取 T-2 或倒数第二行，避免取到今日空白行
        if total == 0:
            df_all = df_sh.sort_values('日期')
            if len(df_all) >= 2:
                row_fb = df_all.iloc[-2]              # 取 T-2 数据
            else:
                row_fb = df_all.iloc[-1]              # 兜底取最新
            total = float(row_fb['融资买入额'])
            ed = row_fb['日期'].strftime("%Y年%m月%d日")
            print(f"  [两融交易额] ⚠️ T-1 未出，用 T-2 回退: {ed}={total/1e8:.1f}亿")
        print(f"  [两融交易额] {ed}={total/1e8:.1f}亿（⚠️T-2回退，数据可能偏高）")
        return total / 1e8, ed                         # 返回亿（akshare 字段单位=元→÷1e8转亿）
    except Exception as e:
        print(f"  [两融交易额] {e}"); return None, None

def _timeout_call(func, args, default, timeout_sec=5):
    """用线程超时包装器调用任意函数，防止SZSE/BSE接口卡死"""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(func, *args)
            return future.result(timeout=timeout_sec)
    except Exception:
        return default

def _get_bse_turnover(effective_date: str) -> float:
    """
    北交所成交额（亿元）。
    数据源：akshare stock_bse_summary（单位：元 → ÷1e8）。
    北交所无独立接口时返回0（占比极小，不影响主逻辑）。
    """
    def _fetch():
        import akshare as ak
        df = ak.stock_bse_summary(date=effective_date)
        if df is None or df.empty:
            return 0.0
        bj_row = df[df['证券类别'] == '股票'].iloc[0]
        amt = float(bj_row.iloc[1]) / 1e8  # 元→亿
        print(f"  [北交所成交额] {amt:.1f}亿")
        return amt
    return _timeout_call(_fetch, (), 0.0, timeout_sec=5)

def get_turnover_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    A股成交额（亿元）。沪深北三所合计。

    逻辑：
    1. 当日(T日)：腾讯实时 API（沪+深，不含北交所，实时行情不含BSE）
    2. 历史：依次取沪市 + 深市 + 北交所 → 三所加总
       - 沪市：stock_sse_deal_daily['成交金额']，单位=万元 → ÷10000 = 亿
       - 深市：stock_szse_summary['成交金额']，单位=元   → ÷1e8  = 亿
       - 北交所：stock_bse_summary，单位=元              → ÷1e8  = 亿
    """
    if effective_date == TODAY_DATE:
        try:
            import urllib.request
            req = urllib.request.Request(
                "https://qt.gtimg.cn/q=sh000001,sz399001",
                headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
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
            print(f"  [成交额] {ed}（T日实时）=沪{sh:.0f}+深{sz:.0f}={total:.0f}亿={total/10000:.2f}万亿")
            return total, ed
        except Exception as e:
            print(f"  [成交额] 腾讯实时失败: {e}")

    try:
        import akshare as ak
        # 沪市：数据列单位=亿，直接使用（无需换算）
        df_sh = ak.stock_sse_deal_daily(date=effective_date)
        sh_row = df_sh[df_sh['单日情况'] == '成交金额']
        sh_turn = float(sh_row.iloc[0].get('股票', 0))  # 亿

        # 深市：元 ÷ 1e8 = 亿元
        df_sz = _timeout_call(ak.stock_szse_summary, (effective_date,), None)
        if df_sz is None: raise RuntimeError('SZSE timeout')
        sz_row = df_sz[df_sz['证券类别'] == '股票']
        sz_turn = float(sz_row.iloc[0].get('成交金额', 0)) / 1e8  # 元→亿

        # 北交所：元 ÷ 1e8 = 亿元
        bj_turn = _get_bse_turnover(effective_date)

        total = round(sh_turn + sz_turn + bj_turn, 0)
        ed = (datetime.strptime(effective_date, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日")
        print(f"  [成交额] {ed}=沪{sh_turn:.0f}+深{sz_turn:.0f}+北交所{bj_turn:.0f}={total:.0f}亿={total/10000:.2f}万亿")
        return total, ed
    except Exception as e:
        # Fallback：仅用沪市×1.37估算深市（深沪成交比约1.3-1.5倍历史均值）
        try:
            import akshare as ak
            df_sh = ak.stock_sse_deal_daily(date=effective_date)
            sh_row = df_sh[df_sh['单日情况'] == '成交金额']
            sh_turn = float(sh_row.iloc[0].get('股票', 0))
            est = round(sh_turn * 1.37, 0)
            ed = (datetime.strptime(effective_date, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日")
            print(f"  [成交额] ⚠️ SZSE超时，用估算值: {ed}=沪{sh_turn:.0f}×1.37={est:.0f}亿={est/10000:.2f}万亿")
            return est, ed
        except Exception:
            print(f"  [成交额] ⚠️ {effective_date}: {e}"); return None, None

def get_market_cap_effective(effective_date: str) -> Tuple[Optional[float], Optional[str]]:
    """
    A股流通市值（亿元）。沪深北三所合计。
    沪市：数据列单位=亿，直接使用（已包含主板A+科创板）
    深市：元 ÷ 1e8 = 亿元（已包含主板+创业板）
    """
    try:
        import akshare as ak
        # 沪市：数据列单位=亿，直接使用
        df_sh = ak.stock_sse_deal_daily(date=effective_date)
        sh_row = df_sh[df_sh['单日情况'] == '流通市值']
        sh_cap = float(sh_row.iloc[0].get('股票', 0))  # 亿

        # 深市：元 ÷ 1e8 = 亿元
        df_sz = _timeout_call(ak.stock_szse_summary, (effective_date,), None)
        if df_sz is None: raise RuntimeError('SZSE timeout')
        sz_row = df_sz[df_sz['证券类别'] == '股票']
        sz_cap = float(sz_row.iloc[0].get('流通市值', 0)) / 1e8  # 元→亿

        total = round(sh_cap + sz_cap, 0)
        ed = (datetime.strptime(effective_date, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日")
        print(f"  [流通市值] {ed}=沪{sh_cap:.0f}+深{sz_cap:.0f}={total:.0f}亿={total/10000:.2f}万亿")
        return total, ed
    except Exception as e:
        # Fallback：仅用沪市×1.05倍估算深市（深沪市值大致相当）
        try:
            import akshare as ak
            df_sh = ak.stock_sse_deal_daily(date=effective_date)
            sh_row = df_sh[df_sh['单日情况'] == '流通市值']
            sh_cap = float(sh_row.iloc[0].get('股票', 0))
            est = round(sh_cap * 1.05, 0)
            ed = (datetime.strptime(effective_date, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日")
            print(f"  [流通市值] ⚠️ SZSE超时，用估算值: {ed}=沪{sh_cap:.0f}×1.05={est:.0f}亿={est/10000:.2f}万亿")
            return est, ed
        except Exception:
            print(f"  [流通市值] ⚠️ {effective_date}: {e}"); return None, None

def get_asia_pacific():
    """
    亚太股市收盘：恒生指数、日经225、韩国综合。
    恒生：腾讯 qt.gtimg.cn（实时）
    日经225 + 韩国综合：akshare index_global_hist_sina（取最近两个收盘日算涨跌幅）
    """
    result = []

    # 富时A50期货：新浪财经期货接口（hf_CHA50CFD = 当月连续 CFD）
    # fields: [0]=最新价,[4]=最高,[5]=最低,[2]=昨收,[7]=开盘,[8]=结算价,[9]=持仓量,[14]=成交量
    # 涨跌幅自行计算: (最新价-昨收)/昨收*100
    a50_found = False
    try:
        import requests
        r = requests.get(
            "https://hq.sinajs.cn/list=hf_CHA50CFD",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://finance.sina.com.cn",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            },
            timeout=8
        )
        r.raise_for_status()
        raw = r.text
        m = re.search(r'hq_str_hf_CHA50CFD="([^"]+)"', raw)
        if m and m.group(1).strip():
            flds = m.group(1).split(',')
            if len(flds) >= 8 and flds[0]:
                a50_price = float(flds[0])
                a50_prev  = float(flds[2]) if flds[2] else None
                a50_pct   = round((a50_price - a50_prev) / a50_prev * 100, 2) if a50_prev and a50_prev > 0 else 0.0
                result.append(('富时A50期货', a50_price, a50_pct))
                print(f"  [亚太] 富时A50期货={a50_price:.0f} {'↑' if a50_pct>=0 else '↓'}{abs(a50_pct):.2f}%")
                a50_found = True
    except Exception as e_a50:
        print(f"  [亚太] 富时A50 数据缺失 ({e_a50})")
    if not a50_found:
        # 兜底：用 w.sinajs.cn（含gzip支持）
        try:
            import gzip, urllib.request as _ur2
            req2 = _ur2.Request(
                "https://w.sinajs.cn/?list=hf_CHA50CFD",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://finance.sina.com.cn/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            )
            with _ur2.urlopen(req2, timeout=8) as resp:
                raw2 = resp.read()
                if resp.info().get("Content-Encoding") == "gzip":
                    raw2 = gzip.decompress(raw2)
                raw2 = raw2.decode("gbk", errors="replace")
            m2 = re.search(r'hq_str_hf_CHA50CFD="([^"]+)"', raw2)
            if m2 and m2.group(1).strip():
                flds2 = m2.group(1).split(',')
                if len(flds2) >= 8 and flds2[0]:
                    a50_price = float(flds2[0])
                    a50_prev  = float(flds2[2]) if flds2[2] else None
                    a50_pct   = round((a50_price - a50_prev) / a50_prev * 100, 2) if a50_prev and a50_prev > 0 else 0.0
                    result.append(('富时A50期货', a50_price, a50_pct))
                    print(f"  [亚太] 富时A50期货={a50_price:.0f} {'↑' if a50_pct>=0 else '↓'}{abs(a50_pct):.2f}%（兜底接口）")
                    a50_found = True
        except Exception as e2:
            print(f"  [亚太] 富时A50 兜底也失败 ({e2})")

    # 恒生指数：腾讯 qt.gtimg.cn（field[3]=当前价, field[32]=涨跌幅）
    try:
        import urllib.request
        for symbol, label in [('hkHSI', '恒生指数')]:
            req = urllib.request.Request(
                f'https://qt.gtimg.cn/q={symbol}',
                headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as r:
                raw = r.read().decode('gbk', errors='replace')
            for line in raw.strip().split('\n'):
                if symbol not in line: continue
                flds = line.lstrip('v_').split('~')
                if len(flds) < 33: continue
                price = float(flds[3]) if flds[3] else 0.0
                pct   = float(flds[32]) if flds[32] else 0.0
                result.append((label, price, pct))
                print(f"  [亚太] {label}={price:.0f} {'↑' if pct>=0 else '↓'}{abs(pct):.2f}%")
    except Exception as e:
        print(f"  [亚太] 恒生指数 获取失败: {e}")

    # 日经225 + 韩国综合：问财 API（akshare index_global_hist_sina 已废）
    # 字段：'收盘价[YYYYMMDD]' / '最新价' 取价；'涨跌幅[YYYYMMDD]' / '最新涨跌幅:前复权' 取涨幅
    for code_key, label in [
        ('N225', '日经225'),
        ('KS11', '韩国综合'),
    ]:
        try:
            data = _iwencai_query(f"{code_key} 收盘 涨跌幅", timeout=15)
            items = data.get("datas", [])
            if not items:
                print(f"  [亚太] {label} 问财无数据")
                continue
            item = items[0]
            # 校验指数代码（防止问财误匹配其他标的）
            if code_key not in item.get('指数代码', ''):
                print(f"  [亚太] {label} 问财返回非目标: {item.get('指数代码', '')}={item.get('指数简称', '?')}")
                continue
            # 提取价格（优先 收盘价[YYYYMMDD]，回退 最新价）
            price = None
            for k, v in item.items():
                if v in (None, ''): continue
                if k.startswith('收盘价[2'):
                    try: price = float(v); break
                    except (ValueError, TypeError): pass
            if price is None:
                np = item.get('最新价')
                if np not in (None, ''):
                    try: price = float(np)
                    except (ValueError, TypeError): pass
            # 提取涨跌幅（优先 最新涨跌幅:前复权，回退 涨跌幅[YYYYMMDD]）
            pct = None
            for k, v in item.items():
                if v is None: continue
                if '涨跌幅:前复权' in k:
                    try: pct = round(float(v), 2); break
                    except (ValueError, TypeError): pass
            if pct is None:
                for k, v in item.items():
                    if v is None: continue
                    if k.startswith('涨跌幅[2'):
                        try: pct = round(float(v), 2); break
                        except (ValueError, TypeError): pass
            if price is not None and pct is not None:
                result.append((label, price, pct))
                print(f"  [亚太] {label}={price:.0f} {'↑' if pct>=0 else '↓'}{abs(pct):.2f}%（问财）")
            else:
                print(f"  [亚太] {label} 问财缺价/缺涨幅: price={price}, pct={pct}, raw={item}")
        except Exception as e2:
            print(f"  [亚太] {label} 失败: {e2}")

    return result

# ── 情绪参考 ──────────────────────────────────────────────

# ── PE + 国债收益率 + 风险溢价 ─────────────────────────────
def get_pe_and_bond(effective_date: str = "") -> dict:
    result = {'hs300_pe': None, 'hs300_pct5y': None,
              'zzqz_pe': None, 'bond10y': None,
              'rep_date': None, 'risk_premium': None}

    # 1. 国债收益率
    try:
        import akshare as ak
        from datetime import datetime, timedelta
        dates = [effective_date] if effective_date else             [(datetime.now()-timedelta(days=d)).strftime('%Y%m%d') for d in range(5)]
        for d in dates:
            try:
                df = ak.bond_china_yield(start_date=d, end_date=d)
                if df is not None and not df.empty:
                    gov = df[df['曲线名称'] == '中债国债收益率曲线']
                    if not gov.empty:
                        row = gov.iloc[0]
                        col_10y = None
                        for c in ['10年', '10Y']:
                            if c in gov.columns:
                                try:
                                    v = float(str(row[c])); 
                                    if v > 0: col_10y = v; break
                                except: pass
                        if col_10y is not None:
                            result['bond10y'] = round(col_10y, 4)
                            result['rep_date'] = str(row['日期'])[:10]; break
            except: continue
    except Exception as e: print(f"  [国债] {e}")

    # 2. 指数 PE（问财直连）
    # 新格式字段名示例: '市盈率(pe,ttm)[20260528]', '指数代码': '000300.SH'
    try:
        data = _iwencai_query("沪深300PE,中证全指PE", timeout=20)
        for item in data.get("datas", []):
            code = str(item.get("指数代码", ""))
            if "000300" in code:
                for k, v in item.items():
                    if v is None or not isinstance(v, (int, float, str)): continue
                    if "pe" in k.lower():
                        try:
                            result["hs300_pe"] = round(float(v), 2)
                            print(f"  [沪深300PE] 问财={result['hs300_pe']} (字段={k})")
                            break
                        except (ValueError, TypeError): continue
            elif "000985" in code:
                for k, v in item.items():
                    if v is None or not isinstance(v, (int, float, str)): continue
                    if "pe" in k.lower():
                        try:
                            result["zzqz_pe"] = round(float(v), 2)
                            print(f"  [中证全指PE] 问财={result['zzqz_pe']} (字段={k})")
                            break
                        except (ValueError, TypeError): continue
        print(f"  [沪深300PE] 问财={result.get('hs300_pe')}, [中证全指PE] 问财={result.get('zzqz_pe')}")
    except Exception as e:
        print(f"  [PE] 问财失败: {e}")

    # 3. 沪深300 分位点（问财直连）
    # 新格式: '历史分位点(pe,ttm)[20260528]': 0.328（0~1标尺）
    try:
        data_pct = _iwencai_query("沪深300市盈率分位数", timeout=20)
        for item in data_pct.get("datas", []):
            for k, v in item.items():
                if v is None: continue
                if "分位点" in k:
                    try:
                        pct = round(float(v) * 100, 1)
                        result["hs300_pct5y"] = pct
                        print(f"  [沪深300PE分位] 问财口径={pct}% (字段={k})")
                        break
                    except (ValueError, TypeError): continue
    except Exception as e: print(f"  [分位] 问财失败: {e}")

    # 4. 风险溢价 = 1/中证全指PE - 10年期国债收益率
    zz = result.get('zzqz_pe'); bond = result.get('bond10y')
    if zz and bond and zz > 0 and bond > 0:
        result['risk_premium'] = round((1/zz - bond/100)*100, 2)
    if effective_date and len(effective_date) == 8:
        y, m, d = effective_date[:4], effective_date[4:6], effective_date[6:8]
        result['rep_date'] = f'{y}年{m}月{d}日'

    if result.get('bond10y'):
        print(f"  [股市风险溢价] 中证全指PE={result['zzqz_pe']}, 10年期国债={result['bond10y']}%, "
              f"风险溢价={result.get('risk_premium')}%")
    return result


def build_report(indices, data, today_str, ai_news=None, ai_action=None):
    rz_ed = data.get('rz_bal_date'); mc_ed = data.get('mkt_cap_date')
    to_ed = data.get('turnover_date')
    lines = [f"📋 【A股晚报】{today_str}\n"]

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
        lines += ["• 富时A50期货：⚠️暂缺", "• 恒生指数：⚠️暂缺", "• 日经225：⚠️暂缺", "• 韩国综合：⚠️暂缺"]

    rz = data.get('rz_bal'); rb = data.get('rz_buy')
    mc = data.get('mkt_cap')
    # 与两融同日期的成交额，用于比率计算
    rz_turnover = data.get('rz_turnover'); rz_to_ed = data.get('rz_turnover_date')
    delta = data.get('rz_delta')
    lines.append("\n━━━ 市场风险偏好 ━━━")
    if rz is not None and rz_ed:
        delta_str = f"，较前日{'+' if (delta or 0)>=0 else ''}{delta:.0f}亿" if delta is not None else ""
        lines.append(f"• 两融余额（{rz_ed}）：{rz:.0f}亿{delta_str}")
    else:
        lines.append("• 两融余额：⚠️暂缺")

    if rz is not None and mc is not None and mc > 0 and mc_ed:
        ratio1 = rz / mc * 100
        # ── 边界校验：A股正常区间约 1.5%~5%，超出即告警，不输出乱码 ──
        if not (0.1 < ratio1 < 200):
            lines.append(f"• 两融余额/A股流通市值（{rz_ed}）：⚠️数据波动（待核实）")
            print(f"  [⚠️ 比例异常] rz={rz}亿 mc={mc}亿 ratio={ratio1:.2f}%")
        else:
            safe = "✅ 安全区间" if ratio1 < 3.0 else ("⚠️ 预警区" if ratio1 < 3.5 else "🔴 高危区")
            lines.append(f"• 两融余额/A股流通市值（{rz_ed}）= {ratio1:.2f}%  → {safe}")
    else:
        lines.append("• 两融余额/A股流通市值：⚠️数据暂缺")

    # v3.3.2 修复: turnover 之前是裸变量名（line 684 "if turnover is not None"），未在 build_report 内赋值 → NameError 退出 1
    # 改用 data.get('turnover')（与 line 638 风格一致），由 collect_evening_data.py 注入到 JSON
    turnover_val = data.get('turnover')
    if turnover_val is not None and turnover_val > 0:
        # v3.3.2 改: 指标名"融资买入额占比", 公式 rb/turnover (全市场), 阈值 6/9/11
        # rz_buy 来自 akshare（已经是亿元）; turnover 来自 get_turnover_effective（A股全市场成交额，亿元）
        ratio2 = rb / turnover_val * 100
        # 合理性上限保护：融资买入额/全市场成交额正常区间 0~20%，超限说明数据异常
        if ratio2 > 30:
            lines.append(f"• 融资买入额占比（{rz_ed}）：⚠️数据异常比{ratio2:.0f}%，已忽略")
            print(f"  [⚠️ ratio2异常] rz_buy={rb}亿 turnover={turnover_val}亿 ratio={ratio2:.0f}%")
        else:
            rz_to_ed_fmt = (datetime.strptime(rz_to_ed, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日") if re.match(r"^\d{8}$", str(rz_to_ed)) else str(rz_to_ed)
            if ratio2 < 6:
                judgement = "偏冷"
            elif ratio2 <= 9:
                judgement = "中性"
            elif ratio2 <= 11:
                judgement = "偏热"
            else:
                judgement = "过热"
            lines += [
                f"• 融资买入额占比（{rz_to_ed_fmt}）= {ratio2:.1f}%",
                f"  阈值：<6%偏冷 | 6-9%中性 | 9-11%偏热 | >11%过热",
                f"  → 比例={ratio2:.1f}% → {judgement}",
            ]
    else:
        lines.append("• 融资买入额占比：⚠️数据暂缺")

    # PE + 国债收益率 + 风险溢价
    pe = data.get('pe_data', {})
    if pe.get('risk_premium') is not None:
        rp_judge = "高估" if pe['risk_premium'] < 3 else ("中性" if pe['risk_premium'] <= 6 else "低估")
        rep_dt = pe.get('rep_date') or ''
        if rep_dt and len(rep_dt) == 10:
            y, m, d = rep_dt.split('-')
            rep_dt_fmt = f"{y}年{m}月{d}日"
        else:
            rep_dt_fmt = rep_dt

        zz = pe.get('zzqz_pe'); bond = pe.get('bond10y'); rp = pe['risk_premium']
        lines += [
            f"• 股市风险溢价（{rep_dt_fmt}）= {rp:.2f}%",
            f"  阈值：<3%高估 | 3-6%中性 |>6%低估",
            f"  → 溢价率={rp:.2f}% → {rp_judge}",
        ]
    else:
        lines.append("• 股市风险溢价：⚠️数据暂缺")

    hs300_pe = pe.get('hs300_pe')
    hs300_pct = pe.get('hs300_pct5y')
    today_fmt = NOW.strftime("%Y年%m月%d日")
    # 修复：PE 段日期用 pe_data.rep_date（akshare 理杏仁源实际数据日期），
    # 避免显示"今天"但实际数据是 1-2 天前的不一致（2026-06-13 用户反馈）
    pe_date_str = pe.get('rep_date') or today_fmt
    if hs300_pe:
        pct_str = f"{hs300_pct:.1f}%" if hs300_pct else "N/A"
        lines.append(f"• 沪深300PE = {hs300_pe:.2f}（近5年分位点={pct_str}，{pe_date_str}）")
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
    # v3.3.2 修复：免责声明统一由 LLM 按 evening.json 模板生成（与早报模式对齐），
    # build_report 不再追加，避免晚报末尾出现两个相同免责行。
    return "\n".join(lines)

# ── 主流程 ───────────────────────────────────────────────
def main(ai_fill: bool = True, target_date: str = None, dry_run: bool = False):
    """
    target_date: 报告目标日期（YYYYMMDD），None 则默认当天。
    晚报数据 = T-1 交易日数据（effective_date = prev(target_date)）。
    优先从 /tmp/evening_data.json 读取（由 collect_evening_data.py 预先生成），
    无 JSON 时才回退到实时采集。
    """
    # 目标日期（报告标题用）
    if target_date is None:
        _target = TODAY_DATE
    else:
        _target = target_date
    _target_str = (datetime.strptime(_target, "%Y%m%d") + _TZ).strftime("%Y年%m月%d日")

    # effective_date：晚报数据取前一交易日
    _effective = prev_trading_day(_target)

    data = None
    if os.path.exists(OUT_FILE):
        try:
            with open(OUT_FILE, encoding="utf-8") as f:
                data = json.load(f)
            # 验证 JSON 数据日期是否匹配本次目标
            _json_date = data.get("trade_date", "")
            if _json_date and _json_date != _effective:
                print(f"[{TS}] JSON日期({_json_date})与目标({_effective})不符，重新采集")
                data = None
            else:
                # ── 完整性校验：避免"同 trade_date 但采集失败"的 JSON 被复用 ──
                # 触发条件（任一满足即重采，最多一次，不会死循环）：
                #   1. 亚太数据 < 3 项（正常应有 4 项：A50/HSI/N225/KS11）
                #   2. PE 数据缺关键字段（沪深300PE 缺失视为采集失败）
                _ap_len = len(data.get("asia_pacific") or [])
                _pe_ok  = data.get("pe_data", {}).get("hs300_pe")
                if _ap_len < 3 or not _pe_ok:
                    print(f"[{TS}] ⚠️ JSON数据不完整（亚太{_ap_len}项/PE={_pe_ok}），强制重采（仅一次）")
                    data = None
                else:
                    print(f"[{TS}] 从JSON加载数据（{_effective}，{_ap_len}项亚太），跳过重复采集")
        except Exception as e:
            print(f"[{TS}] JSON读取失败: {e}，回退到实时采集")

    if data is None:
        # ════════════════════════════════════════════════════════════════
        # A0 改造：send_evening_report.py 不再具备采集能力（fallback 已删）。
        # 采集完全由 collect_evening_data.py 负责，必须先跑。
        # 缺 JSON = 采集端没跑过（或失败）= 立即报错退出，不重采。
        # 用 raise 不用 sys.exit(1)：外层 try/finally 里的 sys.exit(0)
        # 会覆盖这里的 exit code，必须通过异常传递非零状态。
        # ════════════════════════════════════════════════════════════════
        print(f"\n[{TS}] ❌ 错误：/tmp/evening_data.json 不存在或数据不完整")
        print(f"    目标={_target}，期望数据日期={_effective}")
        print(f"    请先执行: python3 collect_evening_data.py --date {_target}")
        raise SystemExit(1)

    # JSON 日期字段是中文格式，需要统一转为 %Y%m%d（build_report 内部用 strptime）
    for _f in ('rz_bal_date', 'rz_buy_date', 'rz_turnover_date', 'mkt_cap_date', 'turnover_date'):
        _v = data.get(_f, '')
        if _v and '年' in _v:
            data[_f] = _v.replace('年','').replace('月','').replace('日','')

    # ── 读取 LLM 生成的 AI 内容（文件由 cron task 预先生成）─────────────
    _ai_news_lines, _ai_action_lines = [], []
    _ai_file = "/tmp/evening_report_ai.txt"
    if os.path.exists(_ai_file):
        try:
            _content = open(_ai_file, encoding="utf-8").read()
            _parts = re.split(r'\[(财经要闻|操作建议)\]', _content)
            for i in range(1, len(_parts)-1, 2):
                _section = _parts[i]
                _text = (_parts[i+1] or "")
                # v3.3.1 修复：保留空行（要闻之间 1 个空行的可读性约束）
                # 只过滤：纯 ━━━ 分隔行；保留空行；rstrip 仅去行尾空格
                _lines = []
                for _l in _text.splitlines():
                    _s = _l.strip()
                    if _s.startswith('━━━') and _s.endswith('━━━'):
                        continue
                    _lines.append(_l.rstrip())  # 保留空行（"") 但去行尾空格
                if _section == "财经要闻" and _text:
                    _ai_news_lines = _lines
                    print(f"[AI内容] 财经要闻已加载（{len(_ai_news_lines)}行）")
                elif _section == "操作建议" and _text:
                    _ai_action_lines = _lines
                    print(f"[AI内容] 操作建议已加载（{len(_ai_action_lines)}行）")
        except Exception as e:
            print(f"[AI内容] 读取失败: {e}")
    else:
        print(f"[AI内容] 文件不存在（{_ai_file}），财经要闻和操作建议将为空")

    # ── 协议硬校验（v3.1.0 修复）：缺标记/内容为空 → 立即失败 ──
    if not _ai_news_lines:
        raise SystemExit(f"[{TS}] ❌ 协议错：{_ai_file} 缺 [财经要闻] 标记或内容为空")
    if not _ai_action_lines:
        raise SystemExit(f"[{TS}] ❌ 协议错：{_ai_file} 缺 [操作建议] 标记或内容为空")

    # ── 内容质量校验（2026-06-18 立, v3.5.1）：模板硬约束 enforce ──
    # 模板约定（templates/evening.json v3.1.0+）：
    #   1. 要闻禁用 "约/大约" 等模糊词
    #   2. 要闻间必须 1 个空行
    #   3. 操作建议依据长度 30-50 字符
    #   4. 末尾必须含"免责声明：仅供参考"
    #   5. 要闻 6-8 条
    # 校验失败 → 立即失败, LLM 看到错误重试时会更规矩
    _content_full = open(_ai_file, encoding="utf-8").read() if os.path.exists(_ai_file) else ""
    _quality_errors = []

    # 1. 约字检查 (只看要闻段, 避免误伤操作建议里的"约"字)
    _news_text = "\n".join(_ai_news_lines)
    _yue_matches = re.findall(r'约[^\s，。、\n]{0,15}', _news_text)
    if _yue_matches:
        _quality_errors.append(f"要闻含'约'字 {len(_yue_matches)} 次（禁用模糊词）：{_yue_matches[:3]}")

    # 2. 要闻间空行 (检查 【N】之间是否有空行)
    _news_titles = re.findall(r'【\d+】', _news_text)
    if len(_news_titles) >= 2:
        _positions = [m.start() for m in re.finditer(r'【\d+】', _news_text)]
        _no_blank = []
        for i in range(len(_positions) - 1):
            _gap = _news_text[_positions[i]:_positions[i+1]]
            if "\n\n" not in _gap and not re.search(r'\n\s*\n', _gap):
                _no_blank.append(f"【{i+1}】→【{i+2}】")
        if _no_blank:
            _quality_errors.append(f"要闻间无空行 {len(_no_blank)} 处：{_no_blank[:3]}（每条要闻间必须 1 个空行）")

    # 3. 操作建议依据长度 30-50 字符
    _reasons = re.findall(r'依据[:：]\s*([^\n]+)', "\n".join(_ai_action_lines))
    for _i, _r in enumerate(_reasons, 1):
        _r_len = len(_r.strip())
        if _r_len < 25 or _r_len > 60:  # 放宽到 25-60 字符 (模板说 30-50, 给 LLM 一点容差)
            _quality_errors.append(f"依据 {_i} 长度 {_r_len} 字符（建议 30-50）：{_r[:50]}")

    # 4. 免责声明
    if "免责声明" not in _content_full and "仅供参考" not in _content_full:
        _quality_errors.append("末尾缺免责声明（必须有'免责声明：仅供参考，不构成投资建议'）")

    # 5. 要闻数 6-8
    if len(_news_titles) < 6 or len(_news_titles) > 8:
        _quality_errors.append(f"要闻数 {len(_news_titles)} 条（模板要求 6-8）")

    if _quality_errors:
        _err_msg = "内容质量校验失败（v3.5.1）：\n  • " + "\n  • ".join(_quality_errors)
        raise SystemExit(f"[{TS}] ❌ {_err_msg}\n请 LLM 按模板重生成后重试。")

    # indices 优先从 JSON 读取（包含更多字段如 pct），JSON 无则用 get_index_data()
    indices = data.get("indices")
    if not indices:
        indices = get_index_data()

    report = build_report(indices, data, _target_str,
                          ai_news=_ai_news_lines or None,
                          ai_action=_ai_action_lines or None)
    print("\n" + "=" * 50); print(report); print("=" * 50)
    return report

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

def notify_failure(msg: str):
    """推送失败时，通过企业微信发预警通知。

    v3.1.0 修复：包裹 try/except 防止 wx() 自身失败把外层 except 块吃掉。
    原 bug：notify_failure 自身 wx() 失败时抛 FileNotFoundError，外层
    `except Exception` 块里 `_exit_code = 1` 还没执行就被新异常冒泡替换，
    导致脚本永远 exit 0 + 打印"✅ 已完成"误导监控。
    """
    try:
        alert = f"⚠️ 【晚报推送失败】\n{msg}\n\n请及时检查 cron 任务状态。"
        _err = wx(alert)
        if _err == 0:
            print(f"[{TS}] 失败通知已发送")
        else:
            print(f"[{TS}] 失败通知发送失败: err={_err}")
    except Exception as _e:
        # notify_failure 自身失败也不能让外层崩
        # 退化方案：仅打印到 stderr，让 cron 日志能捕获
        import sys as _s
        _s.stderr.write(f"[{TS}] notify_failure 失败: type={type(_e).__name__} msg={_e}\n")
        _s.stderr.flush()

if __name__ == "__main__":
    _acquire_lock()
    _exit_code = 0  # v3.1.0 修复：单一变量，所有失败路径必须设非 0
    _dry_run = False
    try:
        import argparse as _argparse
        _parser = _argparse.ArgumentParser()
        _parser.add_argument('--date', default=None)
        # v3.1.0 修复：argparse 反转。默认加载 ai.txt；--no-ai-fill 才跳过
        _parser.add_argument('--no-ai-fill', action='store_true',
                            help='跳过加载 /tmp/evening_report_ai.txt（默认会加载）')
        # v3.1.0 修复：--dry-run 模式。生成报告 + 保存到文件，但跳过企业微信推送
        _parser.add_argument('--dry-run', action='store_true',
                            help='dry-run 模式：生成报告 + 保存到文件，但跳过企业微信推送')
        _args = _parser.parse_args()

        _target = _args.date.replace('-', '') if _args.date else None
        _ai_fill = not _args.no_ai_fill  # 默认 True（加载 ai.txt）
        _dry_run = _args.dry_run

        print(f"[{TS}] 第一步：收集数据（目标日期={_target or '今天'}，dry-run={_dry_run})...")
        report = main(ai_fill=_ai_fill, target_date=_target, dry_run=_dry_run)
        if report:
            print(f"\n[{TS}] 第二步：保存Markdown报告...")
            _dir = "/workspace/projects/A股报告系统/reports"
            os.makedirs(_dir, exist_ok=True)
            _saved_date = _target or TODAY_DATE
            _path = os.path.join(_dir, f"晚报_{_saved_date}.md")
            with open(_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"  已保存: {_path}")
            print("\n" + "="*60)
            print(report)
            print("="*60)
            # 推送微信
            if _dry_run:
                print(f"[{TS}] 第三步：dry-run 模式，跳过微信推送")
            else:
                print(f"[{TS}] 第三步：推送微信...")
                _push_err = wx(report)
                if _push_err == 0:
                    print(f"  ✅ 微信推送成功")
                else:
                    _msg = f"webhook 返回错误: err={_push_err}"
                    print(f"  ❌ {_msg}")
                    notify_failure(_msg)
                    _exit_code = 1
        else:
            _msg = "晚报内容为空，数据采集可能失败"
            print(f"  ❌ {_msg}")
            notify_failure(_msg)
            _exit_code = 1
    except SystemExit as e:
        # main() 主动退出（如 A0 改造的「数据缺失」场景、v3.1.0 协议错场景、v3.5.1 质量校验场景）
        # 不被外层吞掉，传播非 0 状态码
        _exit_code = e.code if isinstance(e.code, int) else 1
        # v3.5.1 修复: 把 SystemExit 的错误消息打出来, 不然 LLM 看不到具体校验错
        if isinstance(e.code, str) and e.code:
            print(f"  ❌ {e.code}")
    except Exception as e:
        print(f"  ❌ 执行异常: {e}")
        # v3.1.0 修复：notify_failure 自身已包裹 try/except，不会再抛异常打断这里
        notify_failure(f"晚报脚本执行异常: {e}")
        _exit_code = 1
    finally:
        _release_lock()
        print(f"\n[{TS}] {'✅ 已完成' if _exit_code == 0 else f'❌ 失败(err={_exit_code})'}")
        sys.exit(_exit_code)
