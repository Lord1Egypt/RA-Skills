#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股收盘小结（合并版）— 六大指数 + 板块行情 + 全市场主力资金 + 行业资金流(Top) + 量化打分 + IF期货基差
依赖: akshare, pandas, requests, hithink-sector-selector
"""
import urllib.request as _ur, json as _json, os, subprocess, sys, socket, re, time
import requests as _req, pandas as pd
from datetime import datetime, date as _date, timezone, timedelta as _td
from datetime import datetime as _dt

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

# ── 问财 API（新版 /v1/query2data）─────────────────────────────────
def _iwencai_query(query: str, timeout: int = 25) -> dict:
    """同花顺问财 OpenAPI v1，返回 {columns:[...], datas:[...]}
    旧接口 /stockpick/search 已废弃（401 not_found_apikey），统一迁至此。"""
    import requests as _req2, secrets as _secrets
    api_key = os.environ.get("IWENCAI_API_KEY", "")
    if not api_key:
        return {}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Claw-Call-Type": "normal",
        "X-Claw-Skill-Id": "hithink-market-query",
        "X-Claw-Skill-Version": "1.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": _secrets.token_hex(32),
    }
    try:
        r = _req2.post(
            "https://openapi.iwencai.com/v1/query2data",
            headers=headers,
            json={"query": query, "page": "1", "limit": "50", "is_cache": "1", "expand_index": "true"},
            timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"  [_iwencai] HTTP {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"  [_iwencai] 查询失败: {e}")
    return {}

def _fmt_wencai_date(trade_date):
    """将 YYYYMMDD 转换为问财查询用日期描述。
    若等于今天则返回'今日'，否则返回'YYYY年MM月DD日'。"""
    today_str = _date.today().strftime("%Y%m%d")
    if trade_date == today_str:
        return "今日"
    d = _dt.strptime(trade_date, "%Y%m%d")
    return f"{d.year}年{d.month}月{d.day}日"

# ── 全市场成交额（问财）────────────────────────────────────
def get_market_total(trade_date):
    """获取指定日期全A股总成交额（元）。问财新版v1兜底腾讯。
    新版 v1 格式: {columns:[...], datas:[{...}]}，字段名含日期后缀如 成交额[20260529]."""
    date_hint = _fmt_wencai_date(trade_date)
    try:
        data = _iwencai_query(f"{date_hint} A股总成交额", timeout=20)
        rows = data.get("datas") or []
        for item in rows:
            for k, v in item.items():
                if "成交额" in k and v not in (None, "", 0, "0", "0.0"):
                    # 问财返回值类型不稳定:有时 str,有时 float;统一强转为 float 再比较 (2026-06-16 修复 v > 0 str/int 比较错误)
                    try:
                        v_num = float(v)
                    except (TypeError, ValueError):
                        continue
                    if v_num > 0:
                        val_yi = v_num / 1e8
                        print(f"  [成交额] 问财全A成交额={val_yi:.0f}亿（{date_hint}，新API）")
                        return v_num   # 返元
    except Exception as e:
        print(f"  [成交额] 问财失败: {e}")
    # 兜底: 腾讯 web.ifzq 分时接口, 4 大指数累计成交额 (2026-06-16 替换旧 qt.gtimg.cn)
    # 旧 fallback 的 if code in ('sh000300','sz399001') 永远不成立(parts[2] 是 '000300' 不带 sh/sz 前缀), 返回 0
    # 新接口每行格式: "0930 价格 累计手数 累计成交额(元)", 取最后一行累加
    try:
        total_yuan = 0.0
        codes = [("sh000300", "沪深300"), ("sz399001", "深证成指"), ("sz399006", "创业板指"), ("sh000001", "上证指数")]
        for code, name in codes:
            url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={code}"
            req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=8) as r:
                raw = r.read().decode("utf-8", "replace")
            obj = _json.loads(raw)
            points = obj.get("data", {}).get(code, {}).get("data", {}).get("data") or []
            if not points:
                print(f"  [成交额] web.ifzq {name} 无数据")
                continue
            last = points[-1].split(" ")
            if len(last) < 4:
                print(f"  [成交额] web.ifzq {name} 字段不足: {last}")
                continue
            amt_yuan = float(last[3])
            total_yuan += amt_yuan
        if total_yuan > 0:
            total_yi = total_yuan / 1e8
            print(f"  [成交额] web.ifzq 4大指数累计={total_yi:.0f}亿（沪深300+深证+创业板+上证）")
            return total_yuan   # 返元
        else:
            print(f"  [成交额] web.ifzq 兜底全部为空")
            return None
    except Exception as e:
        print(f"  [成交额] web.ifzq 兜底失败: {e}"); return None

# ── 全A股流通市值（问财）────────────────────────────────
def get_market_cap(trade_date):
    """获取指定日期全A股（沪深京）流通市值（单位：亿元）
    新版 v1 格式: {columns:[...], datas:[{...}]}，字段名 流通市值[YYYYMMDD]."""
    date_hint = _fmt_wencai_date(trade_date)
    try:
        data = _iwencai_query(f"{date_hint} A股总流通市值", timeout=20)
        rows = data.get("datas") or []
        for item in rows:
            for k, v in item.items():
                if "流通市值" in k and v:
                    val_yuan = float(v)
                    val_yi = val_yuan / 1e8
                    print(f"  [流通市值] 全A流通市值={val_yi:.2f}亿（{val_yuan/1e12:.2f}万亿）（{date_hint}，新API）")
                    return val_yi
    except Exception as e:
        print(f"  [流通市值] ⚠️ 问财失败: {e}")
    return None

# ── 涨跌停数据（同花顺问财）──────────────────────────────
def get_zt_stats(trade_date):
    """用同花顺问财一次性获取涨停/跌停/炸板家数（1次查询）。
    trade_date 为 YYYYMMDD 格式。
    新版 API v1 响应格式: {columns:[...], datas:[{...}]}
    日期后缀字段如 涨停家数[20260529]."""
    date_hint = _fmt_wencai_date(trade_date)
    query = f"{date_hint} 全A股涨停家数 跌停家数 炸板家数"
    try:
        data = _iwencai_query(query, timeout=25)
        rows = data.get("datas") or []
        if not rows:
            print(f'  [涨跌停] ⚠️ 无数据返回')
            return None, None, None

        # 优先：找字段名含"全A股"的行（市场汇总行）
        item = None
        for row in rows:
            for k in row:
                if '全A股' in k:
                    item = row
                    break
            if item:
                break

        # 降级：找不到全A股行时，单行直接用 / 多行按涨停数最大选
        if item is None:
            if len(rows) == 1:
                # 单行无"全A股"前缀但只有 1 行，直接当作全 A 数据
                item = rows[0]
                print(f'  [涨跌停] 单行数据（无"全A股"前缀），直接采纳')
            else:
                # 多行：按涨停家数最大选
                best_zt = -1
                for row in rows:
                    for k in row:
                        if '涨停家数' in k:
                            try:
                                v = int(float(row[k]))
                                if v > best_zt:
                                    best_zt = v
                                    item = row
                            except (ValueError, TypeError):
                                pass
                if item:
                    print(f'  [涨跌停] ⚠️ 多行无"全A股"，降级取涨停数最大行（{best_zt}家）')
                else:
                    print(f'  [涨跌停] ⚠️ 所有行均无法解析')
                    return None, None, None

        # 新版字段带日期后缀
        date_key = trade_date  # "YYYYMMDD"
        zn_key = next((k for k in item if '涨停家数' in k), None)
        dn_key = next((k for k in item if '跌停家数' in k), None)
        # 兼容问财字段名：旧版"炸板家数" / 新版"涨停开板家数"
        zb_key = next((k for k in item if '炸板家数' in k or '涨停开板家数' in k), None)
        zn = int(float(item[zn_key])) if zn_key else None
        dn = int(float(item[dn_key])) if dn_key else None
        zb = int(float(item[zb_key])) if zb_key else None

        if zn is not None and zb is not None:
            exp_rate = round(zb / (zn + zb) * 100, 1) if (zn + zb) > 0 else 0.0
            print(f'  [涨跌停] 涨停={zn} 跌停={dn} 炸板={zb} 炸板率={exp_rate}%（同花顺问财，新API）')
            return zn, dn, exp_rate
        print(f'  [涨跌停] ⚠️ 字段缺失: {item}')
        return None, None, None

    except Exception as e:
        print(f'  [涨跌停] ⚠️ 异常: {e}')
        return None, None, None
_UTC8 = timezone(_td(hours=8))
_LOCK = "/tmp/a_stock_close_summary.lock"
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lock import lock as _smart_lock, unlock as _smart_unlock

def _acquire_lock():
    if not _smart_lock(_LOCK, owner=__file__):
        _sys.exit(0)
def _unlock():
    _smart_unlock(_LOCK)



def _parse_net(item):
    for k, v in item.items():
        if "主力净买入额" in k:
            return float(v) if v else 0.0
    return 0.0

def get_sector_fund_flow(trade_date):
    """用问财查询近5日主力净流入行业板块。
    新版 v1 格式: {columns:[...], datas:[{...}]}，字段名 主力净买入额[20260525-20260529]."""
    try:
        top5_in, top5_out = [], []
        data5 = _iwencai_query("近5日主力净流入前10行业板块", timeout=30)
        if data5.get("datas"):
            for item in data5["datas"]:
                net = _parse_net(item)
                pct = item.get("最新涨跌幅:前复权", 0) or 0
                entry = f"{item.get('指数简称','?')} {net/1e8:+.2f}亿({pct:+.2f}%)"
                if net > 0 and len(top5_in) < 5:
                    top5_in.append(entry)
                elif net < 0 and len(top5_out) < 3:
                    top5_out.append(entry)
        return {"top5_in": top5_in, "top5_out": top5_out}
    except Exception as e:
        print(f"  [行业资金流] ⚠️ {e}"); return None

def get_main_net_flow(trade_date):
    """获取全市场主力净流入。优先 RPT_MARKET_CAPITALFLOW（东方财富全A汇总）。
    精确匹配 trade_date，按 BONDTYPE="A股" 过滤（全市场=AB股=A股+B股，B股体量可忽略）。
    NET_INFLOW 单位为万元，除以 1e4 转为亿元。"""
    try:
        import requests

        params = {
            'reportName': 'RPT_MARKET_CAPITALFLOW',
            'columns': 'ALL',
            'filter': '(INDEX_CODE="800000.EI")(BONDTYPE="A股")',
            'sortColumns': 'TRADE_DATE',
            'sortTypes': '-1',
            'pageSize': '1',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://data.eastmoney.com',
        }
        r = requests.get(
            'https://datacenter-web.eastmoney.com/api/data/v1/get',
            params=params, headers=headers, timeout=10
        )
        r.raise_for_status()
        rows = (r.json().get('result') or {}).get('data') or []

        if not rows:
            print(f"  [主力净流入] ⚠️ 无数据"); return None

        row = rows[0]
        latest_date = row['TRADE_DATE'][:10]
        # trade_date 形如 "20260601"，latest_date 形如 "2026-06-01"，先归一化再比
        trade_date_norm = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:]}" if len(trade_date) == 8 else trade_date
        if latest_date != trade_date_norm:
            print(f"  [主力净流入] ⚠️ 请求 {trade_date_norm}，实际返回 {latest_date}（日期不匹配）")
        net_yi = round(row['NET_INFLOW'] / 1e4, 2)
        print(f"  [主力净流入] {latest_date}  "
              f"主力净流入={net_yi:+.2f}亿（RPT_MARKET_CAPITALFLOW，精确匹配 BONDTYPE=A股）")
        if abs(net_yi) > 500:
            print(f"  ⚠️ 主力净流出{net_yi:.0f}亿，异常大额出逃，注意风险")
        return {
            "net": net_yi,
            "san": None, "zhong": None, "da": None, "chao": None,
        }
    except Exception as e:
        print(f"  [主力净流入] RPT_MARKET_CAPITALFLOW 失败: {e}"); return None


# ── 共用推送库（v3.1.1 抽取）────────────────────────────────────
import sys as _sys_push
_sys_push.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _send_lib import get_webhook_url, wx, notify_failure  # noqa: E402

# ── 微信推送（占位：v3.1.1 起改用 _send_lib）────────────────────
# 原 get_webhook_url / wx 已删除，需要处见上面 import。

# ── 六大指数（腾讯） ─────────────────────────────────────
def get_index_data():
    """获取六大指数实时/收盘数据。
    ⚠️ 腾讯API返回的code key无sh/sz前缀（如"000001"而非"sh000001"），
    解析时需strip[2:]去掉前缀，以匹配后续lookup。"""
    url = "https://qt.gtimg.cn/q=sh000300,sz399001,sz399006,sh000688,sh000001,sh000905"
    req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with _ur.urlopen(req, timeout=8) as r:
            raw = r.read().decode("gbk", "replace")
    except Exception as e:
        print(f"  [六大指数] ⚠️ 腾讯API请求失败: {e}")
        return []
    result = {}
    for line in raw.strip().split("\n"):
        parts = line.lstrip("v_").split("~")
        if len(parts) < 33: continue
        # 关键：去掉sh/sz前缀，统一用6位数字码存储
        raw_code = parts[2].strip()
        num_code = raw_code[2:] if raw_code.startswith(("sh", "sz")) else raw_code
        try:
            result[num_code] = {
                "name":  parts[1].strip(),
                "price": float(parts[3]),
                "pct":   float(parts[32]),
            }
        except (ValueError, IndexError) as e:
            print(f"  [六大指数] ⚠️ 解析{raw_code}失败: {e}")
            continue
    # 用6位数字码（num）做lookup，与result key格式一致
    out = []
    for num, _code, name in [
        ("000001","sh000001","上证指数"),("399001","sz399001","深证成指"),
        ("399006","sz399006","创业板指"),("000688","sh000688","科创50"),
        ("000300","sh000300","沪深300"),("000905","sh000905","中证500"),
    ]:
        d = result.get(num, {})
        out.append({"code": num, "name": name, "price": d.get("price"), "pct": d.get("pct")})
    found = sum(1 for x in out if x["price"] is not None)
    print(f"  [六大指数] 获取成功 {found}/6 条数据")
    return out

# ── IF期货实时价格（新浪 nf_IF0）────────────────────
def get_if_realtime():
    """获取IF主连实时价格（新浪nf接口，字段[3]=当前价，字段[36]=日期）。
    返回 (price: float, date_str: str) 或 (None, None)"""
    try:
        url = "https://hq.sinajs.cn/list=nf_IF0"
        req = _ur.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn",
        })
        with _ur.urlopen(req, timeout=5) as r:
            raw = r.read().decode("gbk", "replace")
        line = raw.strip()
        if "nf_IF0" not in line or "=" not in line:
            print("  [IF期货] ⚠️ 新浪 nf_IF0 返回数据异常")
            return None, None
        content = line.split('"')[1]
        fields = content.split(",")
        if len(fields) < 37:
            print(f"  [IF期货] ⚠️ 新浪 nf_IF0 字段不足: {len(fields)}")
            return None, None
        price = float(fields[3])
        date_str = fields[36]   # YYYY-MM-DD
        print(f"  [IF期货] 实时价格={price:.2f} ({date_str})")
        return price, date_str
    except Exception as e:
        print(f"  [IF期货] ⚠️ 新浪 nf_IF0 请求失败: {e}")
        return None, None

# ── IF期货基差
def get_if_basis(trade_date):
    """IF期货基差：IF期货价格 vs 沪深300现货价格。
    今日优先新浪nf_IF0实时价；失败则降级akshare（不区分日期，取最近收盘）。
    现货：akshare stock_zh_index_daily(symbol='sh000300') 取最近有效收盘日"""
    try:
        import akshare as ak
        today_str = _date.today().strftime("%Y%m%d")
        if trade_date == today_str:
            if_price, _ = get_if_realtime()
            if if_price is None:
                # 降级：akshare 不区分日期，取最近收盘价
                df_if = ak.futures_main_sina(symbol="IF0")
                if df_if is None or df_if.empty:
                    print("  [IF期货] ⚠️ akshare IF 历史也无数据")
                    return None
                if_price = float(df_if.iloc[-1]["收盘价"])
                print(f"  [IF期货] 降级akshare最近价={if_price:.2f}")
        else:
            # 非今日（历史日期）：akshare 不区分日期，取最近收盘
            df_if = ak.futures_main_sina(symbol="IF0")
            if df_if is None or df_if.empty:
                print(f"  [IF期货] ⚠️ akshare IF 无数据")
                return None
            if_price = float(df_if.iloc[-1]["收盘价"])
            print(f"  [IF期货] akshare最近价={if_price:.2f}")
        if if_price is None:
            return None
        df_hs = ak.stock_zh_index_daily(symbol="sh000300")
        if df_hs is None or df_hs.empty:
            print("  [IF期货] ⚠️ akshare stock_zh_index_daily('sh000300') 无数据")
            return None
        spot = float(df_hs.iloc[-1]["close"])
        basis = round(if_price - spot, 2)
        label = "贴水" if basis < 0 else "升水"
        print(f"  [IF期货] IF={if_price:.2f} 现货={spot:.2f} 基差={basis:+.2f}点（{label}）")
        return if_price, basis
    except Exception as e:
        print(f"  [IF期货] ⚠️ {e}"); return None, None

# ── 板块行情（hithink-sector-selector）───────────────────
def get_sector_data(trade_date):
    """获取指定日期行业板块涨跌幅前5/后5。
    新版 v1 格式: 字段名 涨跌幅[YYYYMMDD]，如 涨跌幅[20260529]."""
    date_hint = _fmt_wencai_date(trade_date)
    try:
        d_top = _iwencai_query(f"{date_hint} 行业板块涨幅前10", timeout=30)
        d_bot = _iwencai_query(f"{date_hint} 行业板块跌幅前10", timeout=30)
        top5, bot5 = [], []
        hist_key_base = f"涨跌幅[{trade_date}]"
        if d_top.get("datas"):
            for item in d_top["datas"][:5]:
                pct = item.get(hist_key_base) or item.get("最新涨跌幅:前复权", 0) or 0
                name = item.get("指数简称", "?")
                top5.append(f"{name}{float(pct):+.2f}%")
        if d_bot.get("datas"):
            for item in d_bot["datas"][:5]:
                pct = item.get(hist_key_base) or item.get("最新涨跌幅:前复权", 0) or 0
                name = item.get("指数简称", "?")
                bot5.append(f"{name}{float(pct):+.2f}%")
        if top5 or bot5:
            print(f"  [板块] 涨幅前5={top5} 跌幅前5={bot5}（新API）")
        return top5, bot5
    except Exception as e:
        print(f"  [板块] 问财失败: {e}"); return None, None

# ── 打分辅助 ─────────────────────────────────────────────
def _sc(v, lo, hi):
    if v is None: return None
    return round(max(0.0, min(1.0, (v - lo) / (hi - lo))) * 100)

def get_ratio_score(ratio):
    import math
    if ratio is None or ratio <= 0: return None
    THRESHOLDS = [(1.0, 40), (3.0, 60), (10.0, 80), (30.0, 100)]
    for i in range(len(THRESHOLDS) - 1):
        (r0, s0), (r1, s1) = THRESHOLDS[i], THRESHOLDS[i + 1]
        if ratio <= r0: return s0
        if ratio <= r1:
            lr0, lr1 = math.log10(r0), math.log10(r1)
            lr = math.log10(ratio)
            return round(s0 + (lr - lr0) / (lr1 - lr0) * (s1 - s0))
    return 100

# ── 生成报告 ─────────────────────────────────────────────
def build_report(indices, zn, dn, exp_rate, net_flow, turnover,
                 if_price, basis, market_total,
                 ind_gainers=None, ind_losers=None,
                 date_str="???", net_flow_raw=None, sector_flow=None):
    ind_up   = ind_gainers or []
    ind_down = ind_losers or []
    pct_map  = {i["code"]: i["pct"] for i in indices if i.get("pct") is not None}

    def _f(code, default="-"):
        p = pct_map.get(code)
        if p is None: return default
        arrow = "↑" if p > 0 else "↓" if p < 0 else ""
        return f"{arrow}{abs(p):.2f}%"

    def _idx(code, name):
        p = pct_map.get(code)
        if p is None: return f"{name}：- "
        arrow = "↑" if p > 0 else "↓" if p < 0 else ""
        return f"{name}：{p:.2f}%"

    index_lines = []
    for num, code, name in [
        ("000001","000001","上证指数"),("399001","399001","深证成指"),
        ("399006","399006","创业板指"),("000688","000688","科创50"),
        ("000300","000300","沪深300"),("000905","000905","中证500"),
    ]:
        i = next((x for x in indices if x["code"] == num), None)
        if not i or i.get("price") is None: continue
        p = i["pct"]; arrow = "↑" if p > 0 else "↓" if p < 0 else "→"
        index_lines.append(f"• {name}：{i['price']:.2f}，{arrow}{abs(p):.2f}%")
    index_block = "\n".join(index_lines) + "\n"

    turnover_line = f"{turnover:.2f}%" if turnover else "未获取"

    if net_flow is not None:
        arrow = "🔴" if net_flow < 0 else "🟢"
        net_line = f"  {arrow} 全市场主力资金：{net_flow:+.2f}亿元（{'净流出' if net_flow < 0 else '净流入'}）"
    else:
        net_line = "  全市场主力资金：未获取"

    if net_flow_raw:
        subs = []
        for lbl, key in [("散户", "san"), ("中单", "zhong"), ("大单", "da"), ("超大单", "chao")]:
            v = net_flow_raw.get(key)
            if v is not None:
                subs.append(f"{lbl}={v:+.2f}亿")
        if subs:
            net_line += "  " + "  ".join(subs)

    zn_dn_line = f"涨停{zn}家 / 跌停{dn}家" if zn is not None and dn is not None else "涨停/跌停数据未获取"
    exp_line = f"{exp_rate}%" if exp_rate is not None else "未获取"

    up_block = "  🔺 涨幅前5：\n" + "\n".join(f"    · {x}" for x in ind_up) + "\n" if ind_up else ""
    dn_block = "  🟢 跌幅前5：\n" + "\n".join(f"    · {x}" for x in ind_down) + "\n" if ind_down else ""

    if sector_flow:
        top_in = sector_flow.get("top5_in", [])
        top_out = sector_flow.get("top5_out", [])
        sec_block = ""
        if top_in:
            sec_block += "  近5日净流入板块 TOP5：\n" + "\n".join(f"    · {x}" for x in top_in) + "\n"
        if top_out:
            sec_block += "  近5日净流出板块 TOP3：\n" + "\n".join(f"    · {x}" for x in top_out) + "\n"
    else:
        sec_block = ""

    calc = []
    score_map = []

    if zn is not None:
        zn_s = _sc(float(zn), 10, 100)
        calc.append(f"· 涨停家数 → {zn_s}分（涨停{zn}家，区间10~100家映射）")
        score_map.append(("涨停", zn_s))
    if dn is not None and dn > 0 and zn is not None and zn > 0:
        ratio = float(zn) / dn
        import math
        zb_s = get_ratio_score(ratio)
        calc.append(f"· 涨跌停比 → {zb_s}分（涨停{zn}/跌停{dn}={ratio:.2f}倍，对数插值）")
        score_map.append(("涨跌停比", zb_s))
    if exp_rate is not None:
        exp_s = _sc(exp_rate, 40, 10)
        calc.append(f"· 炸板率 → {exp_s}分（区间40%~10%映射，越低越好）")
        score_map.append(("炸板率", exp_s))
    if net_flow is not None:
        ratio = net_flow / (market_total / 1e8) * 100 if market_total else None
        nf_s = _sc(ratio, -5, 5) if ratio is not None else None
        if ratio is not None:
            calc.append(f"· 主力净流入占比 → {nf_s}分（{ratio:.2f}%，区间-5%~+5%映射）")
        score_map.append(("主力", nf_s))
    if turnover is not None:
        tu_s = _sc(turnover, 1, 4)
        calc.append(f"· 全市场换手率 → {tu_s}分（换手率{turnover:.2f}%，区间1%~4%映射）")
        score_map.append(("换手率", tu_s))
    if basis is not None:
        if_s = _sc(basis, -300, 150)
        calc.append(f"· IF基差 → {if_s}分（基差{basis:+.2f}点，区间-300~+150点映射）")
        score_map.append(("IF基差", if_s))

    scores = [s for _, s in score_map if s is not None]
    total = round(sum(scores) / len(scores), 0) if scores else None

    def _color(t):
        t = int(t)
        if t >= 70: return "🟢做多"
        if t >= 55: return "🟡偏多"
        if t >= 40: return "⚪分歧"
        if t >= 25: return "🟠偏空"
        return "🔴冰点"

    score_block = ""
    if zn is not None or exp_rate is not None:
        score_block += f"📌 涨跌停：{zn_dn_line}  炸板率：{exp_line}\n"
    if calc:
        score_block += "\n".join(calc) + f"\n综合评分：{int(total)}/100  {_color(total)}"

    outlook = "市场震荡调整，风格偏向题材与成长，建议控制仓位、关注轮动节奏。"

    return f"""📊 【A股收盘小结】{date_str}

━━━ 一，主要股指表现 ━━━
{index_block}全市场成交额：{market_total/1e8:.0f}亿
IF期货信号：IF={if_price}，基差{'+' if (basis or 0) > 0 else ''}{basis}点（{'升水' if (basis or 0) > 0 else '贴水'}）

━━━ 二，板块行情 ━━━
{up_block}{dn_block}
━━━ 三，全市场主力资金 ━━━
{net_line}

━━━ 四，行业主力资金流 ━━━
{sec_block}
━━━ 五，量化情绪打分 ━━━
{score_block}

━━━ 六，后市展望 ━━━
{outlook}

━━━ 数据来源：腾讯财经·东方财富·同花顺 ━━━
⚠️ 仅供参考，不构成投资建议。股市有风险，投资需谨慎。
"""

# ── 主程序 ─────────────────────────────────────────────
if __name__ == "__main__":
    import signal, chinese_calendar as cc, argparse as _argparse
    from datetime import date as _date
    _parser = _argparse.ArgumentParser()
    _parser.add_argument('--date', default=None)
    _args = _parser.parse_args()
    def _sig_handler(signum, frame): _unlock(); sys.exit(0)
    signal.signal(signal.SIGALRM, _sig_handler)
    signal.alarm(100)
    _acquire_lock()
    _exit_code = 0  # v3.1.2 修复：单一变量，失败路径必须设非 0（v3.1.0 模板同形）
    try:
        now_local = datetime.now(timezone.utc).astimezone(_UTC8)
        print(f"[{now_local.strftime('%H:%M:%S')}] 开始...")

        today = _date.today()
        if not _args.date and not cc.is_workday(today):
            print(f"[{now_local.strftime('%H:%M:%S')}] 今日({today})非交易日（节假日/周末），退出。")
            _exit_code = 0
            # 直接走 finally 释放锁并退出

        if _args.date:
            trade_date = _args.date.replace('-', '')
            print(f"  [日期] 使用指定日期：{trade_date}")
        else:
            trade_date = None
            for d in range(8):
                td = (now_local - _td(days=d)).strftime("%Y%m%d")
                wd = (now_local - _td(days=d)).weekday()
                if wd < 5: trade_date = td; break
            if not trade_date:
                print("⚠️ 未找到最近交易日")
                _exit_code = 1
                # 直接走 finally 释放锁并退出
            print(f"  [日期] 数据交易日：{trade_date}（周{['','一','二','三','四','五','六'][wd]}）")

        indices      = get_index_data()
        market_total = get_market_total(trade_date)
        circ_wan     = get_market_cap(trade_date)
        # 换手率 = 成交额(亿元) / 流通市值(亿元) * 100%
        turnover     = round(market_total / 1e8 / (circ_wan) * 100, 2) if circ_wan and market_total else None
        print(f"  [换手率] {turnover:.2f}%" if turnover else "  [换手率] ⚠️")
        if_price, basis = get_if_basis(trade_date)
        ind_gainers, ind_losers = get_sector_data(trade_date)
        zn, dt_n, exp_rate = get_zt_stats(trade_date)
        net_flow_raw  = get_main_net_flow(trade_date)
        net_flow_val  = net_flow_raw.get("net") if net_flow_raw else None
        sector_flow   = get_sector_fund_flow(trade_date)

        date_str = datetime.strptime(trade_date, "%Y%m%d").strftime("%Y年%m月%d日")

        report = build_report(indices, 
            zn=zn, dn=dt_n, exp_rate=exp_rate,
            net_flow=net_flow_val,
            turnover=turnover,
            if_price=if_price, basis=basis,
            market_total=market_total,
            ind_gainers=ind_gainers,
            ind_losers=ind_losers,
            date_str=date_str,
            net_flow_raw=net_flow_raw,
            sector_flow=sector_flow,
        )

        print("\n" + "=" * 50)
        print(report)
        print("=" * 50)

        print("\n[TS] 保存...")
        _dir = "/workspace/projects/A股报告系统/reports"
        os.makedirs(_dir, exist_ok=True)
        fname = f"收盘小结_{trade_date}.md"
        _path = os.path.join(_dir, fname)
        with open(_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  已保存: {_path}")

        print("[TS] 推送...")
        err = wx(report)
        if err == 0:
            print(f"\n✅ 推送成功")
        else:
            print(f"\n❌ 推送失败 (errcode={err})")
            _exit_code = 1  # v3.1.2 修复：业务失败必须让监控看到非 0 退出码
            # notify_failure 自身 try/except 包裹（v3.1.0 教训），不会阻断主流程
            try:
                from _send_lib import notify_failure
                notify_failure("收盘小结", f"webhook 返回错误: err={err}")
            except Exception as _ne:
                print(f"  [notify_failure 调用失败] {_ne}")
    except Exception as e:
        print(f"  ❌ 执行异常（收盘小结崩溃）: {e}")
        import traceback; traceback.print_exc()
        _exit_code = 1
        try:
            from _send_lib import notify_failure
            notify_failure("收盘小结", f"脚本执行异常: {e}")
        except Exception as _ne:
            print(f"  [notify_failure 调用失败] {_ne}")
    finally:
        _unlock()
        sys.exit(_exit_code)
