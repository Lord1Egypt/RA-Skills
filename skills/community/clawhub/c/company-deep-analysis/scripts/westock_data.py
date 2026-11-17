#!/usr/bin/env python3
"""
金融数据采集模块（纯 HTTP 接口版）。

零外部依赖：仅使用 Python 标准库（urllib），无任何第三方包，通过公开免费 API 直接采集
全部金融数据（三表 / F10 / 行情 / 股东 / 分红），确保通过严格安全审计。

数据源一览：
  三表（利润表/资产负债表/现金流量表）：新浪财报 API
  公司概况：东财 F10 CompanySurvey
  股东信息：东财 F10 ShareholderResearch
  行情报价：腾讯 qt.gtimg.cn（A 股）/ 新浪实时行情（港股）
  分红送配：东财 F10 现金分红接口

调用方式（与原 westock_data.py 接口兼容）：
  from westock_data import finance, profile, shareholder, quote, dividend, calc_ebitda
"""

import re
import time
import urllib.request
import urllib.error
import json as _json

# ── 工具 ──

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def http_get(url, params=None, timeout=15, encoding="utf-8"):
    """通用 GET 请求，返回解析后的 JSON dict。"""
    if params:
        from urllib.parse import urlencode
        url = url + "?" + urlencode(params) if "?" not in url else url + "&" + urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    resp = urllib.request.urlopen(req, timeout=timeout)
    data = resp.read().decode(encoding)
    return _json.loads(data) if data.strip() else {}


def market_prefix(code):
    """5 位数字 = 港股 (hk)；6 位按首位分 A 股 (sh/sz/bj)。"""
    if len(code) == 5 and code.isdigit():
        return "hk"
    if code.startswith(("6", "9")):
        return "sh"
    if code.startswith(("8", "4")):
        return "bj"
    return "sz"


def em_market(code):
    """东财市场代码：SH/SZ/BJ/HK。"""
    p = market_prefix(code)
    return {"sh": "1", "sz": "0", "bj": "2", "hk": "116"}.get(p, "0")


def _safe_float(v):
    if v is None or v == "" or v == "--" or v == "-":
        return None
    try:
        if isinstance(v, str):
            v = v.replace(",", "").replace("元", "").strip()
            if v.endswith("%"):
                return float(v[:-1]) / 100
        return float(v)
    except (ValueError, TypeError):
        return None


# ══════════════════════════════════════════════
#  1. 三表：利润表 / 资产负债表 / 现金流量表
# ══════════════════════════════════════════════

def finance(code, num=8):
    """
    返回 {"lrb": [...], "fzb": [...], "llb": [...]}。
    每行格式：{"报告期": "YYYY-MM-DD", "字段名": 值, ...}
    数据源：
      - A 股：新浪财经财报 API
      - 港股：东财港股 datacenter（RPT_HKF10_FN_INCOME/BALANCE）
              注：新浪港股三表接口返回空，港股改走东财港股 datacenter（零依赖）。
    """
    if len(code) == 5 and code.isdigit():
        return hk_triple(code, num)   # 港股走东财港股 datacenter
    prefix = market_prefix(code)
    base_url = "https://quotes.sina.cn/cn/api/openapi.php/CompanyFinanceService.getFinanceReport2022"

    out = {"lrb": [], "fzb": [], "llb": []}

    # 报表类型映射：(sina report_type 参数, 输出 key)
    report_types = [
        ("lrb", "lrb"),       # 利润表
        ("zcfz", "fzb"),      # 资产负债表
        ("xjll", "llb"),      # 现金流量表
    ]

    for rtype, out_key in report_types:
        try:
            params = {
                "paperCode": f"{prefix}{code}",
                "source": rtype,
                "type": "0",
                "page": "1",
                "num": str(num),
            }
            j = http_get(base_url, params=params, timeout=15)
            report_list = (j.get("result") or {}).get("data", {}).get("report_list", {}) or {}
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
                        rec[f"{title}_同比"] = tongbi
                rows.append(rec)
            out[out_key] = rows
            time.sleep(0.2)
        except Exception:
            out[out_key] = []

    return out


# ══════════════════════════════════════════════
#  港股专用：东财港股 datacenter（替代原 npm 包，零依赖）
#  说明：原 westock-data npm 包港股三表/指标底层即东财，此处直连东财港股
#        datacenter（RPT_HKF10_FN_*），覆盖更全、无 npm 依赖，通过安全审计。
#        港股免费源无现金流量表（CASHFLOW 报表配置不存在）与主营构成明细。
# ══════════════════════════════════════════════

_HK_CACHE = {}  # 进程内缓存，避免同一次采集重复拉取


def _em_hk_datacenter(report, code="00700", num=8, columns="ALL"):
    """东财港股 datacenter 通用取数，返回 result.data 列表（带缓存）。"""
    cache_key = f"{report}|{code}|{num}|{columns}"
    if cache_key in _HK_CACHE:
        return _HK_CACHE[cache_key]
    params = {
        "reportName": report, "columns": columns,
        "filter": f'(SECUCODE="{code}.HK")',
        "pageSize": str(num), "sortColumns": "REPORT_DATE",
        "sortTypes": "-1", "source": "HSF10", "client": "PC",
    }
    data = []
    try:
        d = http_get(
            "https://datacenter.eastmoney.com/securities/api/data/v1/get",
            params=params, timeout=15)
        data = (d.get("result") or {}).get("data") or []
    except Exception:
        data = []
    _HK_CACHE[cache_key] = data
    return data


def hk_main_indicator(code, num=12):
    """
    东财港股主要指标（RPT_HKF10_FN_GMAININDICATOR）→ 归一化列表（每期一份）。
    含中文标签：基本每股收益/每股净资产/ROE加权/销售毛利率/销售净利率/
    资产负债率/营业总收入/归母净利润/营收同比/净利同比/每股经营现金流/每股股息/总资产收益率。
    用于 finance['财务指标'] 快照与估值（PE/PB）。
    """
    cache_key = f"mi|{code}"
    if cache_key not in _HK_CACHE:
        rows = _em_hk_datacenter("RPT_HKF10_FN_GMAININDICATOR", code, 12)
        parsed = []
        for r in rows:
            parsed.append({
                "报告期": str(r.get("REPORT_DATE", ""))[:10],
                "报告类型": str(r.get("DATE_TYPE", "")),
                "基本每股收益": _safe_float(r.get("BASIC_EPS")),
                "每股净资产": _safe_float(r.get("BPS")),
                "ROE加权": _safe_float(r.get("ROE")),
                "销售毛利率": _safe_float(r.get("GROSS_PROFIT_RATIO")),
                "销售净利率": _safe_float(r.get("NET_PROFIT_RATIO")),
                "资产负债率": _safe_float(r.get("DEBT_ASSET_RATIO")),
                "营业总收入": _safe_float(r.get("OPERATE_INCOME")),
                "归母净利润": _safe_float(r.get("HOLDER_PROFIT")),
                "营收同比": _safe_float(r.get("OPERATE_INCOME_YOY")),
                "净利同比": _safe_float(r.get("HOLDER_PROFIT_YOY")),
                "总资产收益率": _safe_float(r.get("ROA")),
                "每股经营现金流": _safe_float(r.get("PER_NETCASH_OPERATE")),
                "每股股息": _safe_float(r.get("DPS_HKD")),
            })
        _HK_CACHE[cache_key] = parsed
    return _HK_CACHE[cache_key][:num]


def hk_triple(code, num=8):
    """
    港股三表：东财 HK INCOME/BALANCE（CASHFLOW 港股无免费源）→ Sina 风格中文标题。
    返回 {lrb, fzb, llb}；港股免费源无现金流量表，llb 恒为空，EBITDA 由估值层优雅降级。
    字段命名对齐 calc_ebitda() 与 _calc_pe_pb_hk() 的读取约定。
    """
    out = {"lrb": [], "fzb": [], "llb": []}

    # 利润表（长格式：ITEM_NAME + AMOUNT），按报告期分组
    inc_rows = _em_hk_datacenter("RPT_HKF10_FN_INCOME", code, num * 40)
    inc_by_period = {}
    for r in inc_rows:
        p = str(r.get("REPORT_DATE", ""))[:10]
        inc_by_period.setdefault(p, {})[str(r.get("ITEM_NAME", ""))] = _safe_float(r.get("AMOUNT"))
    for p, items in inc_by_period.items():
        out["lrb"].append({
            "报告期": p,
            "营业总收入": items.get("营业额") or items.get("营运收入"),
            "利润总额": items.get("除税前溢利"),
            "财务费用": items.get("融资成本"),
            "归属于母公司股东的净利润": items.get("持续经营业务税后利润") or items.get("股东应占溢利"),
            "净利润": items.get("持续经营业务税后利润") or items.get("股东应占溢利"),
            "毛利": items.get("毛利"),
            "销售费用": items.get("销售及分销费用"),
            "管理费用": items.get("行政开支"),
            "所得税": items.get("税项"),
            "利息收入": items.get("利息收入"),
        })

    # 资产负债表
    bal_rows = _em_hk_datacenter("RPT_HKF10_FN_BALANCE", code, num * 40)
    bal_by_period = {}
    for r in bal_rows:
        p = str(r.get("REPORT_DATE", ""))[:10]
        bal_by_period.setdefault(p, {})[str(r.get("ITEM_NAME", ""))] = _safe_float(r.get("AMOUNT"))
    for p, items in bal_by_period.items():
        out["fzb"].append({
            "报告期": p,
            "资产总计": items.get("总资产"),
            "负债合计": items.get("总负债"),
            "归属于母公司股东权益合计": items.get("股东权益"),
            "所有者权益合计": items.get("总权益"),
            "流动资产合计": items.get("流动资产合计"),
            "非流动资产合计": items.get("非流动资产合计"),
            "流动负债合计": items.get("流动负债合计"),
            "非流动负债合计": items.get("非流动负债合计"),
            "货币资金": items.get("现金及等价物"),
        })

    # 现金流量表：港股东财无 CASHFLOW 报表（接口返回"报表配置不存在"），
    # 免费源无法取得 OCF，llb 留空；EBITDA 由估值层优雅降级（跳过 EV/EBITDA 变体）。

    for k in ("lrb", "fzb"):
        out[k].sort(key=lambda x: x.get("报告期", ""), reverse=True)
    return out


def hk_quote(code):
    """
    港股行情报价：腾讯 qt.gtimg.cn（q=hk{code}），可靠且无 push2 依赖。
    返回 {price, total_shares(股), mcap(港元), name, mcap_yi, pb(推算)}。
    PE 由估值层用 price/eps 计算；PB 用 mcap/归母股东权益（与 valuation 一致）。
    """
    cache_key = f"quote|{code}"
    if cache_key in _HK_CACHE:
        return _HK_CACHE[cache_key]
    result = {"error": "港股行情获取失败"}
    try:
        req = urllib.request.Request(f"https://qt.gtimg.cn/q=hk{code}")
        req.add_header("User-Agent", UA)
        raw = urllib.request.urlopen(req, timeout=10).read().decode("gbk")
        if "=" in raw and '"' in raw:
            vals = raw.split('"')[1].split("~")
            if len(vals) > 47:
                name = vals[1]
                price = _safe_float(vals[3])
                mcap_yi = _safe_float(vals[44])   # 总市值（亿港元）
                mcap = (mcap_yi * 1e8) if mcap_yi else None
                shares = (mcap / price) if (mcap and price) else None
                # 归母股东权益（PB 分母）：东财 BALANCE 最新期
                equity = None
                triple = hk_triple(code, 1)
                if triple.get("fzb"):
                    equity = triple["fzb"][0].get("归属于母公司股东权益合计")
                pb = (mcap / equity) if (mcap and equity) else None
                result = {
                    "code": code,
                    "name": name,
                    "industry": "",
                    "price": price,
                    "total_shares": shares,
                    "float_shares": shares,
                    "mcap": mcap,
                    "mcap_yi": mcap_yi,
                    "list_date": "",
                    "pb": round(pb, 3) if pb else None,
                    "_数据源": "腾讯 qt.gtimg.cn（港股 hk{code}）",
                }
    except Exception as e:
        result = {"error": str(e)[:80]}
    _HK_CACHE[cache_key] = result
    return result


# ══════════════════════════════════════════════
#  2. 公司简况（profile）
# ══════════════════════════════════════════════

def profile(code):
    """
    返回公司基本信息的 dict：
    {"code": ..., "name": ..., "industry": ..., "chairman": ...,
     "reg_capital": ..., "province": ..., "list_date": ..., "price": ...}
    """
    result = {}
    is_hk = len(code) == 5 and code.isdigit()

    if not is_hk:
        # A 股：东财 F10 CompanySurvey + 东财 push2 个股信息
        em = f"{market_prefix(code).upper()}{code}"
        try:
            d = http_get(
                f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?code={em}",
                timeout=15,
            )
            jbzl = (d.get("jbzl") or [{}])[0]
            result.update({
                "code": code,
                "name": jbzl.get("SHORTNAME", "") or jbzl.get("SECURITY_NAME_ABBR", ""),
                "industry": jbzl.get("EM2016", ""),
                "chairman": jbzl.get("CHAIRMAN", ""),
                "reg_capital": jbzl.get("REG_CAPITAL", ""),
                "province": jbzl.get("PROVINCE", ""),
                "company_profile": (jbzl.get("ORG_PROFILE") or "").strip()[:400],
            })
        except Exception:
            pass

        # 补充行情价格和上市日期
        try:
            mkt = em_market(code)
            d2 = http_get(
                "https://push2.eastmoney.com/api/qt/stock/get",
                params={
                    "fltt": "2", "invt": "2",
                    "fields": "f57,f58,f84,f85,f127,f189,f43",
                    "secid": f"{mkt}.{code}",
                },
                timeout=10,
            )
            dd = d2.get("data") or {}
            if not result.get("name"):
                result["name"] = dd.get("f58", "")
            result["price"] = str(dd.get("f43", 0))
            result["list_date"] = str(dd.get("f189", ""))
            if not result.get("industry"):
                result["industry"] = dd.get("f127", "")
        except Exception:
            pass
    else:
        # 港股：新浪实时行情拿基本信息 + 东方财富国际版
        prefix = market_prefix(code)
        try:
            # 新浪港股实时行情
            hk_url = f"https://hq.sinajs.cn/list={prefix}{code}"
            req = urllib.request.Request(hk_url)
            req.add_header("Referer", "https://finance.sina.com.cn/")
            req.add_header("User-Agent", UA)
            resp = urllib.request.urlopen(req, timeout=10)
            raw = resp.read().decode("gbk").strip()
            if "=" in raw and '"' in raw:
                vals = raw.split('"')[1].split(",")
                result.update({
                    "code": code,
                    "name": vals[0].strip() if vals else "",
                    "price": vals[6] if len(vals) > 6 else "",
                    "industry": "",  # 新浪不返回行业
                })
        except Exception:
            pass

        # 补充行业等信息（东方财富国际港股 F10）
        try:
            d3 = http_get(
                f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?code=HK.{code}",
                timeout=15,
            )
            jbzl = (d3.get("jbzl") or [{}])[0]
            result.setdefault("name", jbzl.get("SHORTNAME", ""))
            result["industry"] = jbzl.get("EM2016", "") or ""
            result.setdefault("chairman", jbzl.get("CHAIRMAN", ""))
            result.setdefault("reg_capital", jbzl.get("REG_CAPITAL", ""))
            result.setdefault("introduction", (jbzl.get("ORG_PROFILE") or "").strip())
            result.setdefault("listedDate", str(jbzl.get("LISTING_DATE", "") or jbzl.get("APPLY_DATE", "") or ""))
            result.setdefault("website", jbzl.get("WEB_ADDRESS", "") or jbzl.get("ORG_WEB", ""))
            result.setdefault("regAddress", jbzl.get("REG_ADDRESS", "") or jbzl.get("PROVINCE", ""))
            result.setdefault("business", (jbzl.get("MAIN_BUSINESS", "") or jbzl.get("BUSINESS_SCOPE", "") or "").strip())
        except Exception:
            pass

    return result


# ══════════════════════════════════════════════
#  3. 股东信息（shareholder）
# ══════════════════════════════════════════════

def shareholder(code):
    """
    返回 list[dict]，每项含股东名称、持股比例、持股数、性质等。
    数据源：东财 F10 ShareholderResearch。
    """
    is_hk = len(code) == 5 and code.isdigit()
    results = []

    try:
        if is_hk:
            em = f"HK.{code}"
        else:
            em = f"{market_prefix(code).upper()}{code}"

        d = http_get(
            f"https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/PageAjax?code={em}",
            timeout=15,
        )

        sdgd = d.get("sdgd") or []
        for r in sdgd[:10]:
            entry = {
                "name": r.get("HOLDER_NAME", ""),
                "shares": r.get("HOLD_NUM", ""),
                "pct": r.get("HOLD_RATIO", ""),
                "type": r.get("HOLDER_TYPE", ""),
                "change": r.get("HOLD_CHANGE", ""),  # 持股变动
            }
            # 过滤空行
            if entry.get("name"):
                results.append(entry)

        # 补充股东户数
        gdrs = d.get("gdrs")
        if gdrs is not None:
            results.insert(0, {"_meta": "股东人数", "total_shareholders": str(gdrs)})

    except Exception as e:
        results = [{"error": str(e)}]

    return results


# ══════════════════════════════════════════════
#  4. 行情报价（quote）
# ══════════════════════════════════════════════

def quote(code):
    """
    返回最近一期行情 dict：
    {"date": ..., "open": ..., "last"(现价): ..., "high": ..., "low": ..., "volume": ..., "amount": ...}
    A 股用腾讯 qt.gtimg.cn。
    港股行情请走 hk_quote()（腾讯 qt.gtimg.cn/hk{code}）；本函数港股分支仅作兼容保留，实际采集不调用。
    """
    is_hk = len(code) == 5 and code.isdigit()

    if is_hk:
        # 港股：新浪实时行情
        prefix = market_prefix(code)
        try:
            url = f"https://hq.sinajs.cn/list={prefix}{code}"
            req = urllib.request.Request(url)
            req.add_header("Referer", "https://finance.sina.com.cn/")
            req.add_header("User-Agent", UA)
            resp = urllib.request.urlopen(req, timeout=10)
            raw = resp.read().decode("gbk").strip()
            if "=" in raw and '"' in raw:
                vals = raw.split('"')[1].split(",")
                if len(vals) >= 10:
                    return {
                        "date": vals[17] if len(vals) > 17 else vals[3][:10] if len(vals) > 3 else "",
                        "open": vals[2],
                        "last": vals[6],           # 现价
                        "high": vals[4],
                        "low": vals[5],
                        "volume": vals[8],         # 成交量（手）
                        "amount": vals[9],          # 成交额
                        "prev_close": vals[3],
                    }
        except Exception:
            pass
        return {"error": "港股行情获取失败"}

    else:
        # A 股：腾讯 qt.gtimg.cn
        prefixed = f"{market_prefix(code)}{code}"
        try:
            url = f"https://qt.gtimg.cn/q={prefixed}"
            req = urllib.request.Request(url)
            req.add_header("User-Agent", UA)
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read().decode("gbk")
            for line in data.strip().split(";"):
                if not line.strip() or "=" not in line or '"' not in line:
                    continue
                vals = line.split('"')[1].split("~")
                if len(vals) >= 53:
                    return {
                        "date": vals[30][:10] if len(vals) > 30 else "",
                        "open": vals[5],
                        "last": vals[3],              # 现价
                        "high": vals[33],
                        "low": vals[34],
                        "volume": vals[36],            # 成交量（手）
                        "amount": vals[37],             # 成交额（万）
                        "prev_close": vals[4],
                        "pe_ttm": vals[39],
                        "pb": vals[46],
                        "mcap_yi": vals[44],            # 总市值（亿）
                        "float_mcap_yi": vals[45],      # 流通市值（亿）
                    }
        except Exception:
            pass
        return {"error": "A 股行情获取失败"}


# ══════════════════════════════════════════════
#  5. 分红数据（dividend）
# ══════════════════════════════════════════════

def dividend(code):
    """
    返回 list[dict]，每项包含报告期末、除权日、每股现金红利等。
    数据源：东财 F10 现金分红接口。
    """
    is_hk = len(code) == 5 and code.isdigit()
    results = []

    try:
        if is_hk:
            em = f"HK.{code}"
        else:
            em = f"{market_prefix(code).upper()}{code}"

        d = http_get(
            f"https://emweb.securities.eastmoney.com/PC_HSF10/BonusFinancing/PageAjax?code={em}&type=0",
            timeout=15,
        )

        items = d.get("xjfhlist") or []
        for item in items[:20]:
            entry = {
                "reportEndDate": item.get("REPORT_DATE_NAME", ""),
                "exDiviDate": item.get("EX_DIVIDEND_DATE_NAME", ""),
                "cashPayDate": item.get("PAY_DATE_NAME", ""),
                "cashDivPerShare": item.get("DIVIDEND_PER_SHARE_PRE_TAX", ""),   # 每股税前
                "totalCashDivi": item.get("TOTAL_DIVIDEND", ""),                  # 分红总额
                "dividendPlan": item.get("PLAN_DESC", ""),                       # 方案描述
            }
            if entry.get("reportEndDate"):
                results.append(entry)

    except Exception as e:
        results = [{"error": str(e)}]

    return results


# ══════════════════════════════════════════════
#  6. EBITDA 计算（纯数学，无外部依赖）
# ══════════════════════════════════════════════

def calc_ebitda(triple):
    """
    从三表数据反推 EBITDA。
    输入：finance() 返回的 {"lrb": [...], "fzb": [...], "llb": [...]}
    输出：{EBIT, EBITDA, 税前利润, 财务费用, 折旧摊销, 报告期, 缺失字段, ...}
    算法不变（与原版一致）：
      EBIT = 利润总额 + 财务费用
      D&A ≈ OCF 净额 - 净利润（粗估）
      EBITDA = EBIT + D&A
    """
    lrb = triple.get("lrb") or []
    llb = triple.get("llb") or []

    if not lrb:
        return {"error": "lrb 缺失", "EBITDA": None}

    latest_lrb = lrb[0]
    latest_llb = llb[0] if llb else {}
    missing = []

    ebt = _safe_float(latest_lrb.get("利润总额"))
    if ebt is None:
        missing.append("利润总额")

    interest = _safe_float(latest_lrb.get("财务费用"))
    if interest is None:
        interest = 0.0
        missing.append("财务费用")

    if ebt is None:
        return {
            "error": "关键字段缺失",
            "EBITDA": None,
            "缺失字段": missing,
            "报告期": latest_lrb.get("报告期", ""),
        }

    ocf = _safe_float(latest_llb.get("经营活动产生的现金流量净额"))
    net_profit = _safe_float(latest_lrb.get("净利润"))
    if net_profit is None:
        net_profit = _safe_float(latest_lrb.get("归属于母公司股东的净利润"))

    da = 0.0
    da_method = "未计算"
    da_note = ""

    if ocf is not None and net_profit is not None:
        da_raw = ocf - net_profit
        if da_raw > 0:
            da = da_raw
            da_method = "OCF 净额 - 净利润（粗估）"
        else:
            da = 0.0
            da_method = "OCF ≤ 净利时反推失效，按 0 处理"
            da_note = f"OCF={ocf / 1e8:.1f}亿 ≤ 净利润={net_profit / 1e8:.1f}亿"
    else:
        missing.append("OCF 或净利润缺失")
        da_method = "OCF/净利缺失"

    ebit = ebt + interest
    ebitda_val = ebit + da

    return {
        "EBIT": round(ebit, 2),
        "EBITDA": round(ebitda_val, 2),
        "税前利润": round(ebt, 2),
        "财务费用": round(interest, 2),
        "折旧摊销": round(da, 2),
        "折旧摊销算法": da_method,
        "折旧摊销备注": da_note,
        "OCF_净额": round(ocf, 2) if ocf is not None else None,
        "净利润_参考": round(net_profit, 2) if net_profit is not None else None,
        "报告期": latest_lrb.get("报告期", ""),
        "数据来源": "公开 API（新浪三表 + 东财 F10）",
        "缺失字段": missing,
    }


# ══════════════════════════════════════════════
#  自测
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Test 1: A股 600519 财务三表")
    print("=" * 60)
    try:
        triple = finance("600519", num=2)
        for t in ("lrb", "fzb", "llb"):
            print(f"\n  [{t}] 共 {len(triple[t])} 行")
            if triple[t]:
                print(f"  最新期: {triple[t][0].get('报告期')}")
                keys = list(triple[t][0].keys())[:6]
                print(f"  字段示例: {keys}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 2: 港股 00700 财务三表")
    print("=" * 60)
    try:
        triple = finance("00700", num=2)
        for t in ("lrb", "fzb", "llb"):
            print(f"\n  [{t}] 共 {len(triple[t])} 行")
            if triple[t]:
                print(f"  最新期: {triple[t][0].get('报告期')}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 3: A股 600519 profile")
    print("=" * 60)
    try:
        p = profile("600519")
        for k, v in list(p.items())[:10]:
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 4: 港股 00700 profile")
    print("=" * 60)
    try:
        p = profile("00700")
        for k, v in list(p.items())[:10]:
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 5: A股 600519 quote")
    print("=" * 60)
    try:
        q = quote("600519")
        for k, v in q.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 6: 港股 00700 quote")
    print("=" * 60)
    try:
        q = quote("00700")
        for k, v in q.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 7: calc_ebitda")
    print("=" * 60)
    try:
        triple = finance("00700", num=1)
        result = calc_ebitda(triple)
        for k, v in result.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 8: dividend")
    print("=" * 60)
    try:
        dv = dividend("600519")
        print(f"  共 {len(dv)} 条")
        if dv:
            print(f"  最新: {dv[0]}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Test 9: shareholder")
    print("=" * 60)
    try:
        sh = shareholder("600519")
        print(f"  共 {len(sh)} 条")
        if sh:
            print(f"  Top1: {sh[0]}")
    except Exception as e:
        print(f"  FAIL: {e}")
