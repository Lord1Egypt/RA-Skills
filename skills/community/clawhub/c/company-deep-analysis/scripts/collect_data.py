#!/usr/bin/env python3
"""
A股公司数据采集脚本（Step0.2 调用）。

用法:
  python3 scripts/collect_data.py <股票代码>             # 全量采集，写系统临时目录/{code}_data.json
  python3 scripts/collect_data.py --quotes <代码,代码>     # 仅批量行情（Step3.2 竞对 PE/PB/市值）
  python3 scripts/collect_data.py --finances <代码,代码>   # 仅批量财务比率（Step4 §6 可比公司：毛利率/净利率/ROE/营收/同比）

例: python3 scripts/collect_data.py 600519
    python3 scripts/collect_data.py --quotes 600519,000858,600809
    python3 scripts/collect_data.py --finances 600519,000858,600809

全量采集数据（A 股 11 项 / 港股按数据源有差异），输出: 系统临时目录/{股票代码}_data.json（macOS/Linux 走 /tmp/，Windows 走 %TEMP%）
- A 股 11 项：finance/f10/lrb/fzb/llb/ebitda/quote/em_info/blocks/reports/ths_forecast
- 港股数据项（与 A 股差异）：
  - 财务三表：lrb/fzb 来自东财港股 datacenter（INCOME/BALANCE）；**llb 为空（港股无现金流量表）**
  - 主要财务指标 finance：来自东财港股 datacenter GMAININDICATOR
  - ebitda：**不计算**（无 llb → 无法反推 D&A），估值自动跳过 EV/EBITDA
  - quote/em_info：腾讯 qt.gtimg.cn(hk{code}) / 东财个股信息
  - blocks：港股无概念板块，改用 profile.industry（恒生行业分类）作行业归类
  - dividend：东财 F10 现金分红（港股 BonusFinancing）
  - 不采集：reports（港股无研报源）、ths_forecast（港股无一致预期数据源）
"""

import sys
import json
import os
import time
import tempfile
import subprocess
import requests
import urllib.request
import pandas as pd
from io import StringIO

# 三表收集：优先走 westock_data.finance()（A股→新浪，港股→东财 datacenter），失败自动降级到新浪
# 控制开关：环境变量 WESTOCK_TRIPLE=0 关闭，强制走新浪
try:
    from westock_data import (
        finance as _westock_finance,
        calc_ebitda as _calc_ebitda,
        profile as _westock_profile,
        shareholder as _westock_shareholder,
        quote as _westock_quote_one_cli,
        dividend as _westock_dividend,
        hk_main_indicator as _westock_hk_main_indicator,
        hk_quote as _westock_hk_quote,
        _safe_float as _f,
        market_prefix,
    )
    _WESTOCK_AVAILABLE = True
except ImportError:
    _WESTOCK_AVAILABLE = False
    def _f(v):  # 降级版：去掉逗号/百分号后转 float
        if v is None or v == "" or v == "--" or v == "-":
            return None
        try:
            if isinstance(v, str):
                v = v.replace(",", "").strip()
                if v.endswith("%"):
                    return float(v[:-1]) / 100
            return float(v)
        except (ValueError, TypeError):
            return None

WESTOCK_TRIPLE_ENABLED = os.environ.get("WESTOCK_TRIPLE", "1") == "1" and _WESTOCK_AVAILABLE

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# ── 通用工具：带自动重试的联网请求 ──────────────────────
# 网络偶尔会抽风，失败时自动再试 2 次，比一次失败就放弃更稳。
def http_get(url, params=None, headers=None, timeout=15, retries=2, want="json"):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout)
            return r.json() if want == "json" else r
        except Exception as e:
            last = e
            if attempt < retries:
                time.sleep(1.0)
    raise last


# ── 通用工具：根据 6 位代码判断交易所前缀（统一在 westock_data.market_prefix） ──


# 东财接口用数字表示市场：上海=1，深圳=0，北交所=0
def em_market(code):
    return 1 if code.startswith(("6", "9")) else 0


# ── 参数校验 ────────────────────────────────────────────
if len(sys.argv) < 2:
    print("用法: python3 scripts/collect_data.py <5位港股或6位A股代码>")
    print("     python3 scripts/collect_data.py --quotes <代码,代码,...>")
    sys.exit(1)

# 批量行情模式（Step3.2 竞对取数）：仅拉行情，打印 JSON，不写文件
QUOTES_MODE = sys.argv[1] == "--quotes"
# 批量财务比率模式（Step4 §6 可比公司）：仅拉财务比率（8 期），打印 JSON，不写文件
FINANCES_MODE = sys.argv[1] == "--finances"
BATCH_MODE = QUOTES_MODE or FINANCES_MODE

if BATCH_MODE:
    if len(sys.argv) < 3:
        mode_name = "--quotes" if QUOTES_MODE else "--finances"
        print(f"用法: python3 scripts/collect_data.py {mode_name} <代码,代码,...>")
        sys.exit(1)
    QUOTE_CODES = [c.strip() for c in sys.argv[2].split(",") if c.strip().isdigit()]
    if not QUOTE_CODES:
        print("错误：批量模式后需提供逗号分隔的 5/6 位代码")
        sys.exit(1)
    CODE = QUOTE_CODES[0]
else:
    CODE = sys.argv[1]
    # 验证股票代码格式：5 位港股 或 6 位 A 股
    if not ((len(CODE) == 5 or len(CODE) == 6) and CODE.isdigit()):
        print(f"错误：股票代码必须是 5 位港股或 6 位 A 股代码，当前输入：{CODE}")
        sys.exit(1)

result = {}

# 市场识别：5 位数字 = 港股，6 位 = A 股（决定数据源走东财港股 datacenter 还是新浪）
IS_HK = len(CODE) == 5 and CODE.isdigit()

# ── 港股数据源：东财港股 datacenter（RPT_HKF10_FN_*）+ 东财 push2（secid=116） ──
# 港股三表/指标走东财港股 datacenter（零依赖，比原 npm 包覆盖更全）；
# 行情/股本/市值走东财 push2。研报/一致预期港股无免费源，标无数据。
def _hk_annual_row(mi):
    """从 GMAININDICATOR 列表挑最新年报；无年报则取最新期。"""
    if not mi:
        return {}
    for r in mi:
        if "年报" in (r.get("报告类型") or ""):
            return r
    return mi[0]


def _get_finance_hk(code):
    """港股财务快照：东财港股主要指标（GMAININDICATOR）→ 归一化字段。"""
    try:
        mi = _westock_hk_main_indicator(code)
        if not mi:
            return {"error": "港股主要指标拉取为空"}
        snap = _hk_annual_row(mi)
        p = _westock_profile(code)
        return {
            "报告期": snap.get("报告期", ""),
            "公司全称": p.get("name", ""),
            "所属行业": p.get("industry", ""),
            "董事长": p.get("chairman", ""),
            "上市日期": p.get("listedDate", "") or p.get("list_date", ""),
            "注册地": p.get("regAddress", "") or p.get("reg_capital", ""),
            "网址": p.get("website", ""),
            "电话": p.get("tel", ""),
            "邮箱": p.get("email", ""),
            "公司简介": (p.get("introduction", "") or p.get("company_profile", "") or "").strip()[:600],
            "主营业务": (p.get("business", "") or "").strip()[:600],
            "主营构成": {"产品": [], "行业": [], "地区": [],
                         "_说明": "港股免费数据源无主营构成明细（需付费源）"},
            "财务指标": {
                "基本每股收益": snap.get("基本每股收益"),
                "每股净资产": snap.get("每股净资产"),
                "ROE加权": snap.get("ROE加权"),
                "销售毛利率": snap.get("销售毛利率"),
                "销售净利率": snap.get("销售净利率"),
                "资产负债率": snap.get("资产负债率"),
                "营业总收入": snap.get("营业总收入"),
                "归母净利润": snap.get("归母净利润"),
                "营收同比": snap.get("营收同比"),
                "净利同比": snap.get("净利同比"),
                "总资产收益率": snap.get("总资产收益率"),
                "每股经营现金流": snap.get("每股经营现金流"),
                "每股股息": snap.get("每股股息"),
                "_数据源": "东财港股 GMAININDICATOR（国际会计准则）",
                "_报告期": snap.get("报告期", ""),
            },
        }
    except Exception as e:
        return {"error": str(e)[:80]}

def _get_f10_hk(code):
    """港股 F10：东财 HK CompanySurvey + ShareholderResearch。"""
    out = {}
    try:
        p = _westock_profile(code)
        out["公司概况"] = {
            "公司简介": (p.get("introduction") or p.get("company_profile") or "").strip()[:600],
            "所属东财行业": p.get("industry", ""),
            "所属证监会行业": "",
            "注册资本万元": p.get("reg_capital", ""),
            "董事长": p.get("chairman", ""),
            "省份": p.get("regAddress", ""),
            "_数据源": "东财 HK CompanySurvey",
        }
    except Exception as e:
        out["公司概况"] = {"error": str(e)[:80]}

    # 主营构成：港股免费源无明细
    out["主营构成"] = [{"_说明": "港股免费数据源无主营构成明细"}]

    # 股东研究：东财 HK ShareholderResearch
    try:
        sh_list = _westock_shareholder(code)
        out["股东研究"] = {
            "股东户数": "",
            "十大股东": [{"名称": h.get("name", ""),
                          "持股比例": h.get("pct", ""),
                          "持股数": h.get("shares", "")} for h in sh_list[:10]],
            "_数据源": "东财 HK ShareholderResearch",
        }
    except Exception as e:
        out["股东研究"] = {"error": str(e)[:80]}

    out["财务分析"] = _get_finance_hk(code)
    out["行业分析"] = {
        "所属行业": out.get("公司概况", {}).get("所属东财行业", "") if isinstance(out.get("公司概况"), dict) else "",
        "说明": "港股行业由东财 HK CompanySurvey（EM2016 行业分类）提供",
    }
    return out

def _calc_pe_pb_hk(code):
    """
    港股 PE/PB/总市值 自算：price×shares 得市值，再除净利/权益。
    - 净利用最新年报归母净利润（GMAININDICATOR），避免用单季利润算错 PE。
    - 权益用最新期归母股东权益（东财 BALANCE）。
    """
    try:
        q = _westock_hk_quote(code)
        if "error" in q:
            return q
        price = q.get("price")
        shares = q.get("total_shares")  # 股
        mcap = q.get("mcap")            # 港元（元）
        if not (price and shares and mcap):
            return {"error": "现价/股本/市值缺失"}
        # 净利/权益/eps/bvps：东财 GMAININDICATOR（取最新年报）
        mi = _westock_hk_main_indicator(code, 12)
        snap = _hk_annual_row(mi)
        np_parent = snap.get("归母净利润")
        bvps = snap.get("每股净资产")
        eps = snap.get("基本每股收益")
        # 归母股东权益（PB 分母）：东财 BALANCE 最新期
        equity = None
        triple = _westock_finance(code, 1)   # 港股走 hk_triple
        if triple.get("fzb"):
            equity = triple["fzb"][0].get("归属于母公司股东权益合计")
        mcap_yi = mcap / 1e8  # 亿港元
        pe_ttm = (mcap / np_parent) if np_parent else None
        pb = (mcap / equity) if equity else None
        return {
            "现价": round(price, 2) if price else None,
            "总股本亿股": round(shares / 1e8, 2) if shares else None,
            "总市值亿港元": round(mcap_yi, 2) if mcap else None,
            "PE_TTM": round(pe_ttm, 2) if pe_ttm else None,
            "PB": round(pb, 3) if pb else None,
            "BVPS": round(bvps, 2) if bvps else None,
            "EPS_TTM": round(eps, 2) if eps else None,
            "归母净利润亿元": round(np_parent / 1e8, 2) if np_parent else None,
            "_报告期": snap.get("报告期", ""),
            "_数据源": "东财 push2 现价/股本 + GMAININDICATOR 净利 + BALANCE 权益",
        }
    except Exception as e:
        return {"error": str(e)[:80]}


def _westock_quote_one(code):
    """单只港股 quote：东财 push2（secid=116）→ em_info 兼容结构。"""
    try:
        q = _westock_hk_quote(code)
        if "error" in q:
            return q
        return {
            "code": code,
            "name": q.get("name", ""),
            "industry": q.get("industry", ""),
            "total_shares_yi": (q.get("total_shares") or 0) / 1e8,
            "float_shares": q.get("float_shares", 0),
            "mcap_yi": q.get("mcap_yi", 0),
            "list_date": q.get("list_date", ""),
            "price": q.get("price", 0),
            "pe_ttm": "",   # 由 valuation 用 price/eps 计算
            "pb": q.get("pb", ""),
            "_open": "", "_high": "", "_low": "", "_volume": "", "_amount": "",
            "_数据源": "东财 push2（港股）",
        }
    except Exception as e:
        return {"error": str(e)[:80]}

def _westock_quote_batch(codes):
    """港股批量行情：腾讯 qt.gtimg.cn/hk{code}（hk_quote）→ 与 tencent_quote 一致的结构。"""
    out = {}
    for c in codes:
        try:
            q = _westock_hk_quote(c)
            out[c] = {
                "name": q.get("name", ""),
                "price": q.get("price", ""),
                "pe_ttm": "",
                "pb": q.get("pb", ""),
                "mcap_yi": q.get("mcap_yi", ""),
                "float_mcap_yi": "",
                "open": "", "high": "", "low": "", "volume": "",
            }
        except Exception as e:
            out[c] = {"error": str(e)[:80]}
    return out


# ── 1. 东财主要财务指标：ROE/毛利率/净利率/资产负债率等现成值 ──
# 东财主要财务指标快照。datacenter 直接给算好的比率（ROE/毛利率/净利率/资产负债率），省去自己算。
# 港股走 westock 替代（_get_finance_hk）。
def get_finance(code):
    if len(code) == 5 and code.isdigit():
        return _get_finance_hk(code)
    secucode = f"{code}.{market_prefix(code).upper()}"
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {"reportName": "RPT_F10_FINANCE_MAINFINADATA",
              "columns": "ALL", "filter": f'(SECUCODE="{secucode}")',
              "pageSize": "8", "sortColumns": "REPORT_DATE",
              "sortTypes": "-1", "source": "HSF10", "client": "PC"}
    d = http_get(url, params=params, timeout=15)
    rows = (d.get("result") or {}).get("data") or []
    if not rows:
        return {}
    # 取最近一期的关键指标 + 保留近8期供趋势参考
    pick = {"EPSJB": "每股收益", "BPS": "每股净资产", "ROEJQ": "ROE加权",
            "ROEKCJQ": "ROE扣非加权", "XSMLL": "销售毛利率", "XSJLL": "销售净利率",
            "ZCFZL": "资产负债率", "TOTALOPERATEREVE": "营业总收入",
            "PARENTNETPROFIT": "归母净利润", "MGJYXJJE": "每股经营现金流",
            "TOTALOPERATEREVETZ": "营收同比", "PARENTNETPROFITTZ": "净利同比"}
    latest = rows[0]
    snapshot = {"报告期": str(latest.get("REPORT_DATE", ""))[:10]}
    for k, label in pick.items():
        v = latest.get(k)
        if v is not None:
            snapshot[label] = str(v)
    snapshot["_近8期报告期"] = [str(r.get("REPORT_DATE", ""))[:10] for r in rows]
    return snapshot


# ── 2. 东财 F10 五大类：公司概况/财务分析/股东研究/股本结构/行业分析 ──
# 东财 F10 五大类。逐类调用东财 PC 端 F10 接口，组装成结构化字典。
# 港股走 westock 替代（_get_f10_hk）。
def get_f10(code):
    if len(code) == 5 and code.isdigit():
        return _get_f10_hk(code)
    em = f"{market_prefix(code).upper()}{code}"
    base = "https://emweb.securities.eastmoney.com/PC_HSF10"
    out = {}

    # (1) 公司概况：简介/所属行业/注册资本/董事长/省份
    try:
        d = http_get(f"{base}/CompanySurvey/PageAjax?code={em}", timeout=15)
        jbzl = (d.get("jbzl") or [{}])[0]
        out["公司概况"] = {
            "公司简介": (jbzl.get("ORG_PROFILE") or "").strip()[:600],
            "所属东财行业": jbzl.get("EM2016", ""),
            "所属证监会行业": jbzl.get("INDUSTRYCSRC1", ""),
            "注册资本万元": jbzl.get("REG_CAPITAL", ""),
            "董事长": jbzl.get("CHAIRMAN", ""),
            "省份": jbzl.get("PROVINCE", ""),
        }
    except Exception as e:
        out["公司概况"] = {"error": str(e)}
    time.sleep(0.3)

    # (2) 主营构成（按产品/地区拆分收入）
    try:
        d = http_get(f"{base}/BusinessAnalysis/PageAjax?code={em}", timeout=15)
        zygc = d.get("zygcfx") or []
        out["主营构成"] = [
            {"类型": r.get("MAINOP_TYPE", ""), "项目": r.get("ITEM_NAME", ""),
             "收入": r.get("MAIN_BUSINESS_INCOME", ""),
             "收入占比": r.get("MBI_RATIO", ""), "毛利率": r.get("GROSS_RPOFIT_RATIO", "")}
            for r in zygc[:20]
        ]
    except Exception as e:
        out["主营构成"] = {"error": str(e)}
    time.sleep(0.3)

    # (3) 股东研究：十大股东 + 股东户数
    try:
        d = http_get(f"{base}/ShareholderResearch/PageAjax?code={em}", timeout=15)
        sdgd = d.get("sdgd") or []
        out["股东研究"] = {
            "股东户数": d.get("gdrs", ""),
            "十大股东": [{"名称": r.get("HOLDER_NAME", ""),
                          "持股比例": r.get("HOLD_RATIO", ""),
                          "持股数": r.get("HOLD_NUM", ""),
                          "性质": r.get("HOLDER_TYPE", "")} for r in sdgd[:10]],
        }
    except Exception as e:
        out["股东研究"] = {"error": str(e)}
    time.sleep(0.3)

    # (4) 财务分析：直接复用主要指标（行业排名由 Step2 用 WebSearch 获取）
    try:
        out["财务分析"] = get_finance(code)
    except Exception as e:
        out["财务分析"] = {"error": str(e)}

    # (5) 行业分析：东财行业分类（详细竞争格局由 Step2 用 WebSearch 获取）
    out["行业分析"] = {
        "所属行业": out.get("公司概况", {}).get("所属东财行业", "")
        if isinstance(out.get("公司概况"), dict) else "",
        "说明": "行业竞争格局/排名以 Step2 联网搜索为主要数据源",
    }
    return out


# ── 3. 新浪财报三表：利润表/资产负债表/现金流量表 ──────
def sina_report(code, report_type, num=8):
    prefix = market_prefix(code)
    url = "https://quotes.sina.cn/cn/api/openapi.php/CompanyFinanceService.getFinanceReport2022"
    params = {"paperCode": f"{prefix}{code}", "source": report_type,
              "type": "0", "page": "1", "num": str(num)}
    j = http_get(url, params=params, timeout=15)
    report_list = j.get("result", {}).get("data", {}).get("report_list", {}) or {}
    rows = []
    for period in sorted(report_list.keys(), reverse=True)[:num]:
        obj = report_list[period]
        rec = {"报告期": f"{period[:4]}-{period[4:6]}-{period[6:8]}"}
        for it in obj.get("data", []) or []:
            title = it.get("item_title", "")
            if not title or it.get("item_value") is None:
                continue
            rec[title] = it.get("item_value")
            tongbi = it.get("item_tongbi")
            if tongbi not in (None, ""):
                rec[title + "_同比"] = tongbi
        rows.append(rec)
    return rows

# ── 4. 腾讯行情：PE/PB/市值 批量（港股走 Tencent qt.gtimg.cn hk{code}） ──────────────────────
def tencent_quote(codes):
    """
    批量行情：逐只判断市场
    - 5 位数字 → 港股，走 _westock_quote_batch
    - 6 位数字 → A 股，走 qt.gtimg.cn

    注意：港股 qt.gtimg.cn 字段位置跟 A 股不同（mcap 后面跟的是英文 code 如 TENCENT），
    所以港股强制走 westock 路径，不要在 qt.gtimg.cn 里解析港股
    """
    out = {}
    hk_codes = [c for c in codes if len(c) == 5 and c.isdigit()]
    a_codes = [c for c in codes if len(c) == 6 and c.isdigit()]
    # 港股走 westock
    if hk_codes:
        out.update(_westock_quote_batch(hk_codes))
    # A 股走 qt.gtimg.cn
    if a_codes:
        prefixed = [market_prefix(c) + c for c in a_codes]
        url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
        req = urllib.request.Request(url)
        req.add_header("User-Agent", UA)
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("gbk")
        for line in data.strip().split(";"):
            if not line.strip() or "=" not in line or '"' not in line:
                continue
            key = line.split("=")[0].split("_")[-1]
            vals = line.split('"')[1].split("~")
            if len(vals) < 53:
                continue
            c = key[2:]
            out[c] = {"name": vals[1], "price": vals[3], "pe_ttm": vals[39],
                      "pb": vals[46], "mcap_yi": vals[44], "float_mcap_yi": vals[45]}
    return out

# ── 5. 东财个股信息（港股走 Tencent qt.gtimg.cn）──────────────────────
def eastmoney_info(code):
    if len(code) == 5 and code.isdigit():
        return _westock_quote_one(code)
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {"fltt": "2", "invt": "2",
              "fields": "f57,f58,f84,f85,f127,f116,f117,f189,f43",
              "secid": f"{em_market(code)}.{code}"}
    j = http_get(url, params=params, timeout=10)
    d = j.get("data", {}) or {}
    return {"code": d.get("f57",""), "name": d.get("f58",""),
            "industry": d.get("f127",""), "total_shares": d.get("f84",0),
            "float_shares": d.get("f85",0), "mcap": d.get("f116",0),
            "list_date": str(d.get("f189","")), "price": d.get("f43",0)}

# ── 6. 百度概念板块（港股无概念板块数据，改用 westock profile 拿 HSI 行业） ─────
def baidu_blocks(code):
    if len(code) == 5 and code.isdigit():
        # 港股无概念板块数据（散户题材），但有恒生行业分类（westock profile 字段）
        # 模板读 blocks.industry 时显示 HSI 行业而非"无数据"
        try:
            p = _westock_profile(code)
            industry = p.get("industry", "")
            return {
                "industry": [{"name": industry, "change_pct": "", "_数据源": "westock profile（HSI 行业）"}] if industry else [],
                "concept": [],  # 港股无概念板块
                "region": [],
                "_说明": "港股无概念板块（散户题材），行业分类按 HSI（恒生）口径",
            }
        except Exception as e:
            return {"industry": [], "concept": [], "region": [], "_说明": f"港股 HSI 行业拉取失败: {str(e)[:60]}"}
    url = f"https://finance.pae.baidu.com/api/getrelatedblock?code={code}&market=ab&typeCode=all&finClientType=pc"
    headers = {"Accept": "application/vnd.finance-web.v1+json",
               "Origin": "https://gushitong.baidu.com",
               "Referer": "https://gushitong.baidu.com/"}
    d = http_get(url, headers=headers, timeout=10)
    out = {"industry": [], "concept": [], "region": []}
    for block in d.get("Result", []):
        bt = block.get("type", "")
        for item in block.get("list", []):
            entry = {"name": item.get("name",""), "change_pct": item.get("increase","")}
            if "行业" in bt: out["industry"].append(entry)
            elif "概念" in bt: out["concept"].append(entry)
            elif "地域" in bt: out["region"].append(entry)
    return out

# ── 7. 东财研报：含三年EPS预测（港股：westock 无 report 命令，标 N/A） ────────────────────
def eastmoney_reports(code, max_pages=2):
    if len(code) == 5 and code.isdigit():
        return [{"_说明": "无数据"}]  # westock-data 无 report 命令，港股无研报
    all_records = []
    for page in range(1, max_pages + 1):
        params = {"industryCode": "*", "pageSize": "100", "industry": "*",
                  "rating": "*", "ratingChange": "*",
                  "beginTime": "2000-01-01", "endTime": "2030-01-01",
                  "pageNo": str(page), "fields": "", "qType": "0",
                  "code": code, "rcode": "", "p": str(page),
                  "pageNum": str(page), "pageNumber": str(page)}
        d = http_get("https://reportapi.eastmoney.com/report/list",
                     params=params,
                     headers={"Referer": "https://data.eastmoney.com/"},
                     timeout=30)
        rows = d.get("data") or []
        if not rows: break
        all_records.extend(rows)
        if page >= (d.get("TotalPage", 1) or 1): break
        time.sleep(1.2)
    return [{"date": r.get("publishDate","")[:10], "org": r.get("orgSName",""),
             "title": r.get("title","")[:80], "rating": r.get("emRatingName",""),
             "eps_this": r.get("predictThisYearEps",""),
             "eps_next": r.get("predictNextYearEps",""),
             "eps_next2": r.get("predictNextTwoYearEps",""),
             "industry": r.get("indvInduName","")}
            for r in all_records[:30]]

# ── 8. 同花顺一致预期EPS（港股：westock 无 consensus 命令，标 N/A） ──────────────────────
def ths_forecast(code):
    if len(code) == 5 and code.isdigit():
        return [{"_说明": "无数据"}]  # westock-data 无 consensus 命令，港股无一致预期
    url = f"https://basic.10jqka.com.cn/new/{code}/worth.html"
    headers = {"Referer": "https://basic.10jqka.com.cn/"}
    r = http_get(url, headers=headers, timeout=15, want="raw")
    r.encoding = "gbk"
    # 优先 lxml，失败再退 html5lib，避免不同环境解析器差异导致整项失败
    try:
        dfs = pd.read_html(StringIO(r.text), flavor="lxml")
    except Exception:
        dfs = pd.read_html(StringIO(r.text), flavor="html5lib")
    for df in dfs:
        cols = [str(c) for c in df.columns]
        if any("每股收益" in c or "均值" in c for c in cols):
            return df.to_dict(orient="records")
    return []

# ── 批量行情模式：仅输出竞对行情 JSON ────────────────────
if QUOTES_MODE:
    try:
        q = tencent_quote(QUOTE_CODES)
        print(json.dumps(q, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
    sys.exit(0)

# ── 批量财务比率模式：仅输出多公司财务比率（8 期）────────────
# 给 Step4 §6 可比公司财务对比表用：东财数据中心直采，精度=原始数据。
# 失败时不影响其他公司——单家错误只标 FAIL，不阻断整体输出。
# 输出：进度走 stderr，JSON 走 stdout（方便 `> file.json` 直接落盘）。
if FINANCES_MODE:
    out = {"_meta": {"模式": "finances", "公司数": len(QUOTE_CODES),
                     "数据源": "东财 datacenter RPT_F10_FINANCE_MAINFINADATA",
                     "字段": ["营业总收入","营收同比","归母净利润","净利同比",
                              "销售毛利率","销售净利率","ROE加权","ROE扣非加权",
                              "资产负债率","每股净资产","基本每股收益"],
                     "说明": "每家公司返回最近一期快照 + 近 8 期报告期列表"}}
    for c in QUOTE_CODES:
        try:
            fin = get_finance(c)
            if not fin or "error" in fin:
                out[c] = {"error": fin.get("error", "无数据") if isinstance(fin, dict) else "无数据"}
                print(f"  ✗ {c} {out[c]['error'][:60]}", file=sys.stderr)
            else:
                out[c] = fin
                print(f"  ✓ {c} 财务比率", file=sys.stderr)
        except Exception as e:
            out[c] = {"error": str(e)[:80]}
            print(f"  ✗ {c}: {str(e)[:80]}", file=sys.stderr)
        time.sleep(0.3)  # 东财接口限速，避免触发风控
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0)

# ── 执行采集 ──────────────────────────────────────────
print(f"开始采集 {CODE} 的数据...")

try:
    result["finance"] = get_finance(CODE)
    print("  ✓ finance (财务快照)")
except Exception as e:
    result["finance"] = {"error": str(e)}
    print(f"  ✗ finance: {e}")

try:
    result["f10"] = get_f10(CODE)
    print("  ✓ f10 (公司概况/财务分析/股东研究/股本结构/行业分析)")
except Exception as e:
    result["f10"] = {"error": str(e)}
    print(f"  ✗ f10: {e}")

triple_ok = False
if WESTOCK_TRIPLE_ENABLED:
    try:
        triple = _westock_finance(CODE, num=8)
        # 港股无现金流量表（东财无 CASHFLOW 报表），llb 允许为空；
        # 只要利润表 + 资产负债表齐全即视为可用（EBITDA 缺 OCF 时优雅降级）。
        if triple.get("lrb") and triple.get("fzb"):
            for name in ("lrb", "fzb", "llb"):
                result[name] = triple.get(name, [])
            triple_ok = True
            src = "东财港股 datacenter" if IS_HK else "财务三表接口"
            print(f"  ✓ lrb/fzb/llb ({src})")
        else:
            print("  ⚠ 财务三表不齐，降级到新浪")
    except Exception as e:
        print(f"  ⚠ 三表采集失败，降级到新浪: {str(e)[:80]}")

if not triple_ok:
    if IS_HK:
        # 港股无新浪降级路径（sina.cn 不支持港股代码），标缺失
        for name in ("lrb", "fzb", "llb"):
            result.setdefault(name, [{"error": "港股三表采集失败且无新浪降级"}])
        print("  ⚠ 港股三表采集失败，无新浪降级路径")
    else:
        for name, rt in [("lrb", "lrb"), ("fzb", "fzb"), ("llb", "llb")]:
            try:
                result[name] = sina_report(CODE, rt)
                print(f"  ✓ {name} (新浪财报)")
            except Exception as e:
                result[name] = [{"error": str(e)}]
                print(f"  ✗ {name}: {e}")

# 三表拆解 EBITDA（直连新浪或东财港股 datacenter 路径都能用）
try:
    if all(isinstance(result.get(k), list) and result.get(k)
           and not (isinstance(result[k][0], dict) and "error" in result[k][0])
           for k in ("lrb", "llb")):
        result["ebitda"] = _calc_ebitda({"lrb": result["lrb"], "fzb": result.get("fzb", []), "llb": result["llb"]})
        eb = result["ebitda"]
        if eb.get("EBITDA") is not None:
            print(f"  ✓ ebitda (拆解完成): {eb['EBITDA']:.2f} 元 @ {eb.get('报告期','')}")
        else:
            print(f"  ⚠ ebitda 拆解部分缺失: {eb.get('缺失字段', [])}")
    else:
        result["ebitda"] = {"error": "lrb/llb 缺失，无法拆解"}
except Exception as e:
    result["ebitda"] = {"error": str(e)}
    print(f"  ✗ ebitda 拆解失败: {e}")

try:
    result["quote"] = tencent_quote([CODE])
    quote_src = "腾讯行情 (hk{code})" if IS_HK else "腾讯行情"
    print(f"  ✓ quote ({quote_src})")
except Exception as e:
    result["quote"] = {"error": str(e)}
    print(f"  ✗ quote: {e}")

try:
    result["em_info"] = eastmoney_info(CODE)
    em_src = "东财个股信息"
    print(f"  ✓ em_info ({em_src})")
except Exception as e:
    # 备胎：em_info 接口连不上时，用已拿到的 quote + f10 拼出等价信息，避免硬失败
    q = (result.get("quote") or {}).get(CODE, {}) if isinstance(result.get("quote"), dict) else {}
    f10c = (result.get("f10") or {}).get("公司概况", {}) if isinstance(result.get("f10"), dict) else {}
    if q or f10c:
        # 兜底字典补 total_shares_yi：从 mcap_yi / price 反推（em_info 失败时估值必需）
        shares_yi = 0
        try:
            mc = q.get("mcap_yi", 0) or 0
            px = q.get("price", 0) or 0
            if mc and px:
                shares_yi = round(float(mc) * 1e8 / float(px) / 1e8, 4)  # 还原成"亿股"
        except Exception:
            pass
        result["em_info"] = {
            "code": CODE, "name": q.get("name", ""),
            "industry": f10c.get("所属东财行业", "") if isinstance(f10c, dict) else "",
            "mcap_yi": q.get("mcap_yi", ""), "price": q.get("price", ""),
            "total_shares_yi": shares_yi,  # 反推（顶层字段拉平用）
            "_note": f"em_info接口不可用，已由quote+f10兜底。原因: {str(e)[:60]}"}
        print("  ⚠ em_info 接口失败，已用 quote+f10 兜底")
    else:
        result["em_info"] = {"error": str(e)}
        print(f"  ✗ em_info: {e}")

try:
    result["blocks"] = baidu_blocks(CODE)
    if not IS_HK:
        print("  ✓ blocks (百度概念板块)")
    else:
        print("  ✓ blocks (港股 HSI 行业，无概念板块)")
except Exception as e:
    result["blocks"] = {"error": str(e)}
    print(f"  ✗ blocks: {e}")

try:
    result["reports"] = eastmoney_reports(CODE)
    rep_src = "无数据" if IS_HK else "东财研报"
    print(f"  ✓ reports ({rep_src})")
except Exception as e:
    result["reports"] = [{"error": str(e)}]
    print(f"  ✗ reports: {e}")

try:
    result["ths_forecast"] = ths_forecast(CODE)
    fc_src = "无数据" if IS_HK else "同花顺一致预期"
    print(f"  ✓ ths_forecast ({fc_src})")
except Exception as e:
    result["ths_forecast"] = [{"error": str(e)}]
    print(f"  ✗ ths_forecast: {e}")

# 港股额外采集：分红数据（westock dividend 现成命令，A 股暂未启用）
if IS_HK:
    try:
        result["dividend"] = _westock_dividend(CODE)
        print(f"  ✓ dividend (东财分红，{len(result['dividend'])} 条)")
    except Exception as e:
        result["dividend"] = [{"error": str(e)[:80]}]
        print(f"  ⚠ dividend 拉取失败: {str(e)[:60]}")

# 在 result 顶层加 market 标识，方便下游模板识别
result["_market"] = "港股" if IS_HK else "A股"

# ── 顶层拉平估值必需字段（让 valuation.py 能直接读 data["price"] 等） ──
# 港股/A 股共用：em_info 已含 price/total_shares_yi/pe_ttm/pb/mcap_yi，finance 含 eps/bvps
# 历史原因：collect_data 嵌套结构 + valuation.py 平铺读取不匹配；此处加适配层
try:
    em = result.get("em_info") if isinstance(result.get("em_info"), dict) else {}
    q = (result.get("quote") or {}).get(CODE, {}) if isinstance(result.get("quote"), dict) else {}
    fin = result.get("finance") if isinstance(result.get("finance"), dict) else {}
    # 行情字段：em_info 优先（已含自算 PE/PB），quote 兜底
    result["price"] = em.get("price") or q.get("price") or ""
    # total_shares 给 valuation.py 用，要"股"为单位
    # 兼容两种来源：em_info.total_shares（股，东财原始字段）/ total_shares_yi（亿股，港股自算）
    shares_yi = em.get("total_shares_yi", 0) or 0
    raw_shares = em.get("total_shares", 0) or 0
    if raw_shares:
        result["total_shares"] = float(raw_shares)  # 已是"股"
    elif shares_yi:
        result["total_shares"] = float(shares_yi) * 1e8  # 亿股 → 股
    result["mcap_yi"] = em.get("mcap_yi", 0)  # 亿元（A 股）/ 亿港元（港股）
    result["pe_ttm"] = em.get("pe_ttm", 0)
    result["pb"] = em.get("pb", 0)
    result["name"] = em.get("name", "")
    result["code"] = CODE
    # 财务字段：finance["财务指标"]（港股嵌套）已含 EPS/BVPS；A 股 finance 是平铺结构
    if "财务指标" in fin and isinstance(fin["财务指标"], dict):
        ratios = fin["财务指标"]
        result["eps_ttm"] = ratios.get("基本每股收益", 0)
        result["bvps"] = ratios.get("每股净资产", 0)
    elif "每股收益" in fin or "每股净资产" in fin:
        # A 股平铺结构：每股收益 / 每股净资产 / 归母净利润 直接在 finance 顶层
        result["eps_ttm"] = fin.get("每股收益", 0) or result.get("eps_ttm", 0)
        result["bvps"] = fin.get("每股净资产", 0) or result.get("bvps", 0)
    # 兼容 BPS / EPSJB 旧字段
    if "BPS" in fin:
        result["bvps"] = result.get("bvps") or fin.get("BPS", 0)
    if "EPSJB" in fin:
        result["eps_ttm"] = result.get("eps_ttm") or fin.get("EPSJB", 0)
except Exception as e:
    print(f"  ⚠ 顶层字段拉平部分失败: {str(e)[:60]}")

# ── 写入文件，只输出摘要 ──────────────────────────────
# 跨平台：macOS/Linux 走 /tmp/（保持向后兼容），Windows 走 %TEMP%
if sys.platform == "win32":
    _tmpdir = tempfile.gettempdir()
else:
    _tmpdir = "/tmp"
outfile = os.path.join(_tmpdir, f"{CODE}_data.json")
with open(outfile, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 摘要：各模块状态和数据量
summary = {}
for k, v in result.items():
    if isinstance(v, dict) and "error" in v:
        summary[k] = f"FAIL: {v['error'][:50]}"
    elif isinstance(v, list) and v and isinstance(v[0], dict) and "error" in v[0]:
        summary[k] = f"FAIL: {v[0]['error'][:50]}"
    elif isinstance(v, list):
        summary[k] = f"OK: {len(v)} records"
    elif isinstance(v, dict):
        summary[k] = f"OK: {len(v)} fields"
    else:
        summary[k] = "OK"
summary["output_file"] = outfile
print("\n" + "="*50)
print(json.dumps(summary, ensure_ascii=False, indent=2))
print("="*50)
print(f"\n数据已写入: {outfile}")
