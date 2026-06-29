"""
数据采集 — 从公共 Web API 获取股票数据（全16维）
不依赖任何 MCP 服务，全部 HTTP 直连
数据源：新浪/腾讯/东方财富DataCenter/同花顺
"""
import json, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta
from typing import Optional


def _market(code: str) -> str:
    """市场前缀：6/9开头=上海，其余=深圳"""
    c = code.strip()
    return "sh" if c.startswith(("6","9")) else "sz"


def _call_eastmoney(code: str, report_name: str, sort_col: str = "REPORTDATE",
                    page_size: int = 5, filter_field: str = "SECURITY_CODE",
                    extra_filters: str = "") -> list:
    """通用东方财富 DataCenter API 调用
    
    参数:
        code: 股票代码（纯6位数字）
        report_name: 报告名
        sort_col: 排序列名
        page_size: 返回条数
        filter_field: 过滤字段名，默认SECURITY_CODE
        extra_filters: 额外过滤条件，如 '(NUMBERNEW="1")'
    """
    filter_str = extra_filters + f'({filter_field}="{code}")' if filter_field else f'(SECURITY_CODE="{code}")'
    if not filter_field:
        filter_str = extra_filters
    params = {
        "sortColumns": sort_col,
        "sortTypes": "-1",
        "pageSize": page_size,
        "pageNumber": 1,
        "columns": "ALL",
        "reportName": report_name,
        "source": "WEB",
        "client": "WEB",
        "filter": filter_str,
    }
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("success") and data.get("result") and data["result"].get("data"):
            return data["result"]["data"]
        return []
    except Exception as e:
        print(f"[eastmoney] {report_name}: {e}")
        return []


# ========== 1. 实时行情（双源交叉） ==========

def fetch_realtime(code: str) -> dict:
    """
    双源实时行情（新浪主 + 腾讯补换手率/PE/PB）
    返回 {code, name, price, open, close, high, low, volume, amount,
          change_pct, turnover_rate, pe, pb, circ_market, total_market, amplitude}
    """
    mk = _market(code)
    result = {"code": code}
    try:
        url = f"http://hq.sinajs.cn/list={mk}{code}"
        req = urllib.request.Request(url, headers={"Referer":"https://finance.sina.com.cn","User-Agent":"Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        text = resp.read().decode("gbk")
        if '"' in text:
            parts = text.split('"')[1].split(",")
            if len(parts) >= 32:
                result.update(name=parts[0], open=float(parts[1]), close=float(parts[2]),
                              price=float(parts[3]), high=float(parts[4]), low=float(parts[5]),
                              volume=float(parts[8]), amount=float(parts[9]))
                if result.get("close",0): result["change_pct"]=(result["price"]-result["close"])/result["close"]*100
    except: pass
    try:
        resp2 = urllib.request.urlopen(f"http://qt.gtimg.cn/q={mk}{code}", timeout=10)
        p = resp2.read().decode("gbk").split("~")
        if len(p) > 46:
            if not result.get("price"): result["price"]=float(p[3]) if p[3] else 0
            result["name"]=p[1]; result["turnover_rate"]=float(p[38]); result["pe"]=float(p[39])
            result["amplitude"]=float(p[43]); result["circ_market"]=float(p[44])
            result["total_market"]=float(p[45]); result["pb"]=float(p[46])
            if not result.get("close") and p[4]: result["close"]=float(p[4])
            if not result.get("high") and p[33]: result["high"]=float(p[33])
            if not result.get("low") and p[34]: result["low"]=float(p[34])
    except: pass
    return result


# ========== 2. K线数据（腾讯财经） ==========

def fetch_kline(code: str, days: int = 365) -> Optional[list]:
    """腾讯财经日K线（复权）
    参数格式: secid,day,start_date,end_date,count,qfq
    返回 [{date,open,close,high,low,volume,amount}]
    """
    mk = _market(code)
    secid = f"{mk}{code}"
    end = datetime.now()
    start = end - timedelta(days=days + 30)
    param = f"{secid},day,{start.strftime('%Y-%m-%d')},{end.strftime('%Y-%m-%d')},{days+30},qfq"
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={urllib.parse.quote(param)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        dd = data.get("data")
        day_data = []
        if isinstance(dd, dict):
            stock_data = dd.get(secid, {})
            if isinstance(stock_data, dict):
                day_data = stock_data.get("qfqday") or stock_data.get("day") or stock_data.get("data") or []
        elif isinstance(dd, list):
            day_data = dd
        if not day_data:
            return None
        result = []
        for item in day_data:
            if len(item) < 6: continue
            try: result.append({"date":str(item[0]),"open":float(item[1]),"close":float(item[2]),
                                "high":float(item[3]),"low":float(item[4]),"volume":float(item[5]),
                                "amount":float(item[6]) if len(item)>6 else 0})
            except: continue
        result.sort(key=lambda x:x["date"]); return result
    except Exception as e:
        print(f"[kline] {code}: {e}")
        return None


# ========== 3. 今日分时数据 ==========

def fetch_today_tick(code: str) -> Optional[list]:
    """腾讯今日分钟数据，返回 [{time,price,volume}]"""
    try:
        resp = urllib.request.urlopen(f"http://qt.gtimg.cn/q={_market(code)}{code}", timeout=10)
        p = resp.read().decode("gbk").split("~")
        if len(p) > 29:
            raw = p[29].split("|") if len(p[29])>10 else []
            items = []; last_vol = 0
            for part in raw:
                segs = part.strip().split("/")
                if len(segs) >= 3:
                    try:
                        t, pr, cv = segs[0], float(segs[1]), float(segs[2])
                        vol = cv - last_vol if cv >= last_vol else cv
                        last_vol = cv
                        items.append({"time":t,"price":pr,"volume":vol})
                    except: continue
            return items if items else None
    except: pass
    return None


# ========== 4. 资金流向 ==========

def fetch_money_flow(code: str, days: int = 10) -> list:
    """东方财富 push2his 资金流向（日级）
    返回 [{date, main_net, small_net, medium_net, large_net, super_net}]
    """
    market = "1." if code.startswith(("6","9")) else "0."
    url = (f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
           f"?lmt={days}&klt=101&fields1=f1,f2,f3,f7"
           f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
           f"&secid={market}{code}")
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent":"Mozilla/5.0","Referer":"https://data.eastmoney.com/"
        })
        resp = urllib.request.urlopen(req, timeout=15)
        d = json.loads(resp.read())
        klines = d.get("data",{}).get("klines",[])
        result = []
        for k in klines:
            parts = k.split(",")
            if len(parts) >= 13:
                result.append({
                    "date": parts[0],
                    "main_net": float(parts[1]) if parts[1] else 0,        # f52 主力净流入
                    "small_net": float(parts[2]) if parts[2] else 0,       # f53 小单净流入
                    "medium_net": float(parts[3]) if parts[3] else 0,      # f54 中单净流入
                    "large_net": float(parts[4]) if parts[4] else 0,       # f55 大单净流入
                    "super_net": float(parts[5]) if parts[5] else 0,       # f56 超大单净流入
                    "main_pct": float(parts[6]) if len(parts) > 6 and parts[6] else 0,  # f57 主力占比
                    "close": float(parts[11]) if len(parts) > 11 and parts[11] else 0,  # f62 收盘价
                    "change_pct": float(parts[12]) if len(parts) > 12 and parts[12] else 0,  # f63 涨跌幅
                })
        return result
    except Exception as e:
        print(f"[money_flow] {code}: {e}")
        return []


# ========== 5-8. 财务数据 ==========

def fetch_financial(code: str, top: int = 5) -> list:
    """业绩报表（RPT_LICO_FN_CPD）"""
    items = _call_eastmoney(code, "RPT_LICO_FN_CPD", sort_col="REPORTDATE", page_size=top)
    return [{"date":i.get("REPORTDATE","")[:10],"revenue":i.get("TOTAL_OPERATE_INCOME",0),
             "revenue_growth":i.get("YSTZ",0),"net_profit":i.get("PARENT_NETPROFIT",0),
             "profit_growth":i.get("SJLTZ",0),"eps":i.get("BASIC_EPS",0),
             "roe":i.get("WEIGHTAVG_ROE",0),"gross_margin":i.get("XSMLL",0),
             "bps":i.get("BPS",0)} for i in items]

def fetch_balance_sheet(code: str, top: int = 5) -> list:
    """资产负债表（RPT_DMSK_FN_BALANCE）"""
    items = _call_eastmoney(code, "RPT_DMSK_FN_BALANCE", sort_col="REPORT_DATE", page_size=top)
    return [{"date":i.get("REPORT_DATE","")[:10],"total_assets":i.get("TOTAL_ASSETS",0),
             "total_liab":i.get("TOTAL_LIABILITIES",0),"equity":i.get("TOTAL_EQUITY",0),
             "cash":i.get("MONETARY_FUNDS",0),"debt_ratio":i.get("DEBT_ASSET_RATIO",0),
             "current_ratio":i.get("CURRENT_RATIO",0)} for i in items]

def fetch_income_statement(code: str, top: int = 5) -> list:
    """利润表（RPT_DMSK_FN_INCOME）"""
    items = _call_eastmoney(code, "RPT_DMSK_FN_INCOME", sort_col="REPORT_DATE", page_size=top)
    return [{"date":i.get("REPORT_DATE","")[:10],"revenue":i.get("TOTAL_OPERATE_INCOME",0),
             "cost":i.get("TOTAL_OPERATE_COST",0),"gross_profit":i.get("OPERATE_PROFIT",0),
             "net_profit":i.get("NET_PROFIT_ATSOPC",0)} for i in items]

def fetch_cashflow(code: str, top: int = 5) -> list:
    """现金流量表（RPT_DMSK_FN_CASHFLOW）"""
    items = _call_eastmoney(code, "RPT_DMSK_FN_CASHFLOW", sort_col="REPORT_DATE", page_size=top)
    return [{"date":i.get("REPORT_DATE","")[:10],"operate_net":i.get("NET_OPERATE_CASHFLOW",0),
             "invest_net":i.get("NET_INVEST_CASHFLOW",0),"finance_net":i.get("NET_FINANCE_CASHFLOW",0),
             "cash_equity":i.get("CASH_EQUITY",0)} for i in items]


# ========== 9. 融资融券 ==========

def fetch_margin_trading(code: str, days: int = 10) -> list:
    """融资融券（RPTA_WEB_RZRQ_GGMX，filter用SCODE）"""
    items = _call_eastmoney(code, "RPTA_WEB_RZRQ_GGMX", sort_col="DATE",
                            page_size=days, filter_field="SCODE")
    return [{"date":i.get("DATE",""),"balance":i.get("RZYE",0),
             "rz_net":i.get("RZJME",0)} for i in items]


# ========== 10. 机构持仓 ==========

def fetch_main_holdings(code: str) -> dict:
    """主力持仓（RPT_MAIN_ORGHOLD）
    返回 {date, total_holders, fund_sum, insurance_sum, securities_sum, qfii_sum}
    """
    items = _call_eastmoney(code, "RPT_MAIN_ORGHOLD", sort_col="HOLD_VALUE",
                            page_size=10, filter_field="SECURITY_CODE")
    if not items:
        return {}
    # ORG_TYPE: 00=汇总 01=基金 02=QFII 03=社保 04=券商 05=保险 06=信托
    result = {"date": items[0].get("REPORT_DATE","")[:10],
              "total_holders": 0, "fund_sum": 0, "insurance_sum": 0,
              "securities_sum": 0, "qfii_sum": 0}
    for i in items:
        ot = i.get("ORG_TYPE","")
        hv = float(i.get("HOLD_VALUE",0) or 0)
        hv_ratio = float(i.get("HOLD_VALUE_RATIO",0) or 0)
        if ot == "00" or not ot:
            result["total_holders"] = hv_ratio  # 占总股本比例
        elif ot == "01":
            result["fund_sum"] = hv_ratio
        elif ot == "05":
            result["insurance_sum"] = hv_ratio
        elif ot == "04":
            result["securities_sum"] = hv_ratio
        elif ot == "02":
            result["qfii_sum"] = hv_ratio
    return result


# ========== 11. 股东增减持 ==========

def fetch_shareholder_trade(code: str, top: int = 50) -> list:
    """股东增减持（RPT_SHARE_HOLDER_INCREASE）"""
    items = _call_eastmoney(code, "RPT_SHARE_HOLDER_INCREASE", sort_col="END_DATE",
                            page_size=top, filter_field="SECURITY_CODE")
    return [{"date":i.get("END_DATE","")[:10],
             "name":i.get("HOLDER_NAME",""),"type":i.get("DIRECTION",""),
             "volume":i.get("CHANGE_NUM",0),"ratio":i.get("CHANGE_RATE",0),
             "after_hold":i.get("AFTER_HOLDER_NUM",0)} for i in items]


# ========== 12. 高管持股变动 ==========

def fetch_executive_change(code: str, top: int = 30) -> list:
    """高管持股变动（RPT_EXECUTIVE_HOLD_DETAILS）"""
    items = _call_eastmoney(code, "RPT_EXECUTIVE_HOLD_DETAILS",
                            sort_col="CHANGE_DATE,SECURITY_CODE,PERSON_NAME",
                            page_size=top, filter_field="SECURITY_CODE")
    return [{"date":i.get("CHANGE_DATE","")[:10],"name":i.get("PERSON_NAME",""),
             "position":i.get("POSITION_NAME",""),"volume":i.get("CHANGE_VOLUME",0),
             "price":i.get("CHANGE_PRICE",0)} for i in items]


# ========== 13. 分红历史 ==========

def fetch_dividend(code: str, top: int = 10) -> list:
    """分红配股（RPT_SHAREBONUS_DET）"""
    items = _call_eastmoney(code, "RPT_SHAREBONUS_DET", sort_col="PLAN_NOTICE_DATE",
                            page_size=top, filter_field="SECURITY_CODE")
    return [{"date":i.get("PLAN_NOTICE_DATE","")[:10],
             "plan":i.get("SHARE_BONUS_IMPLICIT",0),
             "bonus":i.get("CASH_DIVIDENT",0),
             "transfer":i.get("CONVERT_OF_CAPITAL_RESERVE",0),
             "dividend":i.get("CASH_DIVIDENT_PER_SHARE",0)} for i in items]


# ========== 14. 券商研报（POST API） ==========

def fetch_research_report(code: str, top: int = 10) -> list:
    """券商研报（POST reportapi.eastmoney.com）
    注意：beginTime/endTime 不可为空，否则返回500
    """
    payload = json.dumps({
        "beginTime": "2025-06-01", "endTime": "2026-06-22", "industryCode": "*",
        "rating": "*", "ratingChange": "*", "orgCode": "*",
        "code": code, "rcode": "", "pageSize": top, "pageNo": 1,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            "https://reportapi.eastmoney.com/report/list2",
            data=payload,
            headers={"Content-Type":"application/json; charset=UTF-8","User-Agent":"Mozilla/5.0"}
        )
        resp = urllib.request.urlopen(req, timeout=20)
        result = json.loads(resp.read())
        items = result.get("data", [])
        return [{"date":i.get("publishDate","")[:10],"org":i.get("orgSName","") or i.get("orgName",""),
                 "author":i.get("researcher","") or i.get("author",""),
                 "rating":i.get("emRatingName","") or i.get("sRatingName",""),
                 "title":i.get("title","")} for i in items]
    except Exception as e:
        print(f"[research] {code}: {e}")
        return []


# ========== 15. 机构调研 ==========

def fetch_institutional_survey(code: str, top: int = 10) -> list:
    """机构调研（RPT_ORG_SURVEY）"""
    items = _call_eastmoney(code, "RPT_ORG_SURVEY", sort_col="NOTICE_DATE",
                            page_size=top, filter_field="SECURITY_CODE",
                            extra_filters='(NUMBERNEW="1")(IS_SOURCE="1")')
    return [{"date":i.get("NOTICE_DATE","")[:10],"org_list":i.get("INVESTIGATORS",""),
             "content":i.get("CONTENT","")[:200] if i.get("CONTENT") else "",
             "num":i.get("SUM",0)} for i in items]


# ========== 16. 限售解禁 ==========

def fetch_unlock_data(code: str, top: int = 10) -> list:
    """限售股解禁（RPT_LIFT_GD - 个股明细）"""
    items = _call_eastmoney(code, "RPT_LIFT_GD", sort_col="FREE_DATE",
                            page_size=top, filter_field="SECURITY_CODE")
    return [{"date":i.get("FREE_DATE","")[:10],"quantity":i.get("CURRENT_FREE_SHARES",0),
             "ratio":i.get("FREE_RATIO",0),"holder":i.get("HOLDER_NAME","")} for i in items]


# ========== 17. 公司行业信息 ==========

def fetch_industry_info(code: str) -> dict:
    """公司行业（RPT_F10_ORG_BASICINFO）"""
    items = _call_eastmoney(code, "RPT_F10_ORG_BASICINFO", sort_col="",
                            page_size=1, filter_field="SECURITY_CODE")
    if items:
        i = items[0]
        # 行业分级字段名：BOARD_NAME_1LEVEL / BOARD_NAME_2LEVEL / BOARD_NAME_3LEVEL / CSRC_INDUSTRY_NAME
        ind1 = i.get("BOARD_NAME_1LEVEL","") or i.get("BOARD_NAME","")
        ind2 = i.get("BOARD_NAME_2LEVEL","")
        ind3 = i.get("BOARD_NAME_3LEVEL","")
        csrc = i.get("CSRC_INDUSTRY_NAME","")
        return {"industry": f"{ind1}-{ind2}-{ind3}" if ind2 else ind1,
                "area": i.get("AREA_BOARD_NAME",""),
                "concept": i.get("BLGAINIAN",""),
                "main_business": i.get("MAIN_BUSINESS",""),
                "stock_name": i.get("SECURITY_NAME_ABBR",""),
                "csrc_industry": csrc}
    return {}


# ========== 18. 公司基本信息（腾讯） ==========

def get_company_info(code: str) -> dict:
    """腾讯行情获取公司基本信息"""
    try:
        resp = urllib.request.urlopen(f"http://qt.gtimg.cn/q={_market(code)}{code}", timeout=10)
        p = resp.read().decode("gbk").split("~")
        if len(p) > 46:
            return {"name":p[1],"code":code,"price":float(p[3]),"pe":float(p[39]),
                    "amplitude":float(p[43]),"circ_market":float(p[44]),"total_market":float(p[45]),
                    "pb":float(p[46]),"turnover_rate":float(p[38]),"high":float(p[33]),
                    "low":float(p[34]),"open":float(p[5]),"close_yest":float(p[4]),
                    "volume":float(p[6]),"amount":float(p[37])}
    except: pass
    return {}
