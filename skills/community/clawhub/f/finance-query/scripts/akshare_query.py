#!/usr/bin/env python3
"""
AKShare 查询封装脚本 v2
用法: python3 akshare_query.py <接口名> [参数...]

Examples:
  python3 akshare_query.py stock_zh_a_spot_em
  python3 akshare_query.py stock_zh_a_hist "000001.SZ" 300
  python3 akshare_query.py index_zh_a_hist "000300.SH" 300
  python3 akshare_query.py search_stock "茅台"
  python3 akshare_query.py macro_china_gdp
"""

import os
# 禁用 tqdm 进度条，避免污染 stdout 输出
os.environ['TQDM_DISABLE'] = '1'
os.environ['AKSHARE_NO_PROGRESS'] = '1'

import sys
import json
from datetime import datetime, timedelta

try:
    import akshare as ak
    import pandas as pd
except ImportError as e:
    print(json.dumps({"error": f"缺少依赖库: {e}，请运行: pip install akshare pandas"}))
    sys.exit(1)


def _date_from_count(count: int, period: str = "daily"):
    """根据数量计算开始日期"""
    end = datetime.now()
    if period == "daily":
        start = end - timedelta(days=count)
    elif period == "weekly":
        start = end - timedelta(weeks=count)
    elif period == "monthly":
        start = end - timedelta(days=count * 30)
    else:
        start = end - timedelta(days=count)
    return start.strftime("%Y%m%d"), end.strftime("%Y%m%d")


def safe_call(func, *args, **kwargs):
    """安全调用函数，捕获异常并返回结构化结果"""
    try:
        df = func(*args, **kwargs)
        if df is None or (isinstance(df, (list, dict)) and len(df) == 0):
            return {"error": "数据为空", "data": None}
        if hasattr(df, 'to_dict'):
            if df.empty:
                return {"error": "数据为空（empty DataFrame）", "data": None}
            try:
                records = df.to_dict(orient='records')
                json.dumps(records[:3])  # 验证可序列化
                return {"data": records, "columns": list(df.columns), "len": len(records)}
            except (ValueError, TypeError):
                # 尝试 squeeze（单行/标量 DataFrame）
                try:
                    record = df.squeeze().to_dict()
                    record = {k: (str(v) if not isinstance(v, (str, int, float, type(None))) else v)
                              for k, v in record.items()}
                    return {"data": [record], "columns": list(df.columns), "len": 1}
                except Exception:
                    pass
                # 最后一搏：全部转字符串
                df_str = df.astype(str)
                records = df_str.to_dict(orient='records')
                return {"data": records, "columns": list(df.columns), "len": len(records),
                        "note": "部分列已转为字符串"}
        return {"data": df}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}


# ========== 股票 ==========

def stock_zh_a_spot_em():
    """A股全市场实时行情"""
    return safe_call(ak.stock_zh_a_spot_em)


def stock_zh_a_hist(symbol: str = "000001.SZ", period: str = "daily",
                     adjust: str = "qfq", count: int = None):
    """
    个股历史K线
    symbol: 股票代码，如 "000001.SZ"
    period: "daily"/"weekly"/"monthly"
    adjust: "qfq"(前复权)/"hfq"(后复权)/""
    count: 最近N个（忽略 start_date/end_date）
    """
    if count:
        start_date, end_date = _date_from_count(count, period)
    else:
        start_date, end_date = "", ""
    return safe_call(ak.stock_zh_a_hist,
                     symbol=symbol, period=period, adjust=adjust,
                     start_date=start_date, end_date=end_date)


def stock_financial_analysis_indicator(symbol: str = "000001.SZ", start_year: str = "2020"):
    """财务指标（ROE、EPS等）"""
    return safe_call(ak.stock_financial_analysis_indicator, symbol=symbol, start_year=start_year)


def stock_profit_forecast(symbol: str = "000001.SZ"):
    """个股盈利预测"""
    return safe_call(ak.stock_profit_forecast, symbol=symbol)


def stock_zh_a_stocks_spot():
    """A股实时行情（单个股票）"""
    return safe_call(ak.stock_zh_a_spot_em)


def stock_info_a_code_name():
    """A股全市场代码与名称列表"""
    return safe_call(ak.stock_info_a_code_name)


def search_stock(keyword: str = ""):
    """按关键词搜索股票（名称或代码）"""
    result = safe_call(ak.stock_info_a_code_name)
    if "error" in result:
        return result
    data = result.get("data", [])
    keyword_lower = keyword.lower()
    matched = [r for r in data
               if keyword_lower in str(r.get("name", "")).lower()
               or keyword_lower in str(r.get("code", "")).lower()]
    return {"data": matched, "columns": result.get("columns", []), "len": len(matched),
            "keyword": keyword}


# ========== 指数 ==========

def stock_zh_index_spot_em():
    """主要指数实时行情（上证、深证、沪深300等）"""
    return safe_call(ak.stock_zh_index_spot_em)


def index_zh_a_hist(symbol: str = "000300.SH", period: str = "daily",
                     start_date: str = "", end_date: str = "", count: int = None):
    """
    A股指数历史K线
    symbol: 指数代码，如 "000300.SH"(沪深300)、"000001.SH"(上证指数)
    period: "daily"/"weekly"/"monthly"
    count: 最近N个（优先于 start_date/end_date）
    """
    if count:
        start_date, end_date = _date_from_count(count, period)
    return safe_call(ak.index_zh_a_hist,
                     symbol=symbol, period=period,
                     start_date=start_date, end_date=end_date)


def stock_zh_index_hist_csindex(symbol: str = "000300.SH",
                                  start_date: str = "", end_date: str = "", count: int = None):
    """中证/申万指数历史K线"""
    if count:
        start_date, end_date = _date_from_count(count, period="daily")
    return safe_call(ak.stock_zh_index_hist_csindex,
                     symbol=symbol, start_date=start_date, end_date=end_date)


# ========== 基金 ==========

def fund_open_fund_info_em(fund: str = "000001", start_date: str = "", end_date: str = ""):
    """公募基金历史净值"""
    if not start_date:
        start_date = "20000101"
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    return safe_call(ak.fund_open_fund_info_em, fund=fund, start_date=start_date, end_date=end_date)


def fund_etf_fund_info_em(fund: str = "510300", start_date: str = "", end_date: str = ""):
    """ETF基金历史净值"""
    if not start_date:
        start_date = "20000101"
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    return safe_call(ak.fund_etf_fund_info_em, fund=fund, start_date=start_date, end_date=end_date)


def fund_fund_spot_em():
    """公募基金实时行情"""
    return safe_call(ak.fund_fund_spot_em)


# ========== 期货/大宗商品 ==========

def futures_goods_index_en():
    """国际商品指数"""
    return safe_call(ak.futures_goods_index_en)


def futures_spot():
    """国内期货现货行情"""
    return safe_call(ak.futures_spot)


def futures_zh_daily(symbol: str = "SI"):
    """国内期货日常行情（贵金属/有色/农产品等）"""
    return safe_call(ak.futures_zh_daily, symbol=symbol)


# ========== 宏观 ==========

def macro_china_gdp():
    """中国GDP数据"""
    return safe_call(ak.macro_china_gdp)


def macro_china_cpi():
    """中国CPI数据（月度）"""
    return safe_call(ak.macro_china_cpi)


def macro_china_ppi():
    """中国PPI数据（月度）"""
    return safe_call(ak.macro_china_ppi)


def macro_china_money_supply():
    """中国货币供应量M0/M1/M2"""
    return safe_call(ak.macro_china_money_supply)


def macro_china_fx():
    """中国外汇储备"""
    return safe_call(ak.macro_china_fx)


def macro_china_sw():
    """申万行业指数"""
    return safe_call(ak.macro_china_sw)


# ========== 外汇/汇率 ==========

def forex_rmb_iist():
    """人民币外汇即期汇率（境内外）"""
    return safe_call(ak.forex_rmb_iist)


def currency_name():
    """货币名称列表"""
    return safe_call(ak.currency_name)


# ========== 债券 ==========

def bond_china_comparison():
    """中国企业债/公司债对比行情"""
    return safe_call(ak.bond_china_comparison)


def bond_spot():
    """沪深债券实时行情"""
    return safe_call(ak.bond_spot)


# ========== 数字货币 ==========

def coin_bitget(symbol: str = "BTC", market: str = "USDT"):
    """主流加密货币行情（Bitget）"""
    return safe_call(ak.coin_bitget, symbol=symbol, market=market)


def coin_global():
    """全球加密货币行情"""
    return safe_call(ak.coin_global)


# ========== 期权 ==========

def option_sse():
    """上交所期权行情"""
    return safe_call(ak.option_sse)


# ========== 港股/美股 ==========

def stock_hk_spot():
    """港股实时行情"""
    return safe_call(ak.stock_hk_spot)


def stock_us_spot():
    """美股（中概股等）实时行情"""
    return safe_call(ak.stock_us_spot)


# ========== 财务/公告 ==========

def stock_balance_sheet_em(symbol: str = "000001.SZ"):
    """资产负债表"""
    return safe_call(ak.stock_balance_sheet_by_report_em, symbol=symbol)


def stock_profit_sheet_em(symbol: str = "000001.SZ"):
    """利润表"""
    return safe_call(ak.stock_profit_sheet_by_report_em, symbol=symbol)


def stock_cash_flow_em(symbol: str = "000001.SZ"):
    """现金流量表"""
    return safe_call(ak.stock_cash_flow_by_report_em, symbol=symbol)


# ========== 主营构成 ==========

def stock_operation_board_name_em(symbol: str = "000001.SZ"):
    """主营构成"""
    return safe_call(ak.stock_operation_board_name_em, symbol=symbol)


# ========== 股东/股本 ==========

def stock_hold_num_em(symbol: str = "000001.SZ"):
    """股东人数变化"""
    return safe_call(ak.stock_hold_num_em, symbol=symbol)


def stock_float_hist_em(symbol: str = "000001.SZ"):
    """流通股本变动"""
    return safe_call(ak.stock_float_hist_em, symbol=symbol)


# ========== 龙虎榜/大宗交易 ==========

def stock_lhb_detail_em(symbol: str = "000001.SZ"):
    """龙虎榜明细"""
    return safe_call(ak.stock_lhb_detail_em, symbol=symbol)


def stock_bb_detail_em():
    """大宗交易明细"""
    return safe_call(ak.stock_bb_detail_em)


# ========== 概念板块 ==========

def stock_board_concept_name_em():
    """概念板块名称列表"""
    return safe_call(ak.stock_board_concept_name_em)


def stock_board_concept_hist_em(symbol: str = "BK0001"):
    """概念板块历史K线"""
    return safe_call(ak.stock_board_concept_hist_em, symbol=symbol, period="daily",
                     adjust="qfq", count=100)


# ========== 行业板块 ==========

def stock_board_industry_name_em():
    """行业板块名称列表"""
    return safe_call(ak.stock_board_industry_name_em)


def stock_board_industry_hist_em(symbol: str = "881001"):
    """行业板块历史K线"""
    return safe_call(ak.stock_board_industry_hist_em, symbol=symbol, period="daily",
                     adjust="qfq", count=100)


# ========== 主入口 ==========

INTERFACE_MAP = {
    # 股票行情
    "stock_zh_a_spot_em":         lambda args: stock_zh_a_spot_em(),
    "stock_zh_a_hist":           lambda args: stock_zh_a_hist(
                                     symbol=args[0] if len(args) > 0 else "000001.SZ",
                                     period=args[1] if len(args) > 1 else "daily",
                                     adjust=args[2] if len(args) > 2 else "qfq",
                                     count=int(args[3]) if len(args) > 3 and args[3].isdigit() else None),
    "stock_info_a_code_name":     lambda args: stock_info_a_code_name(),
    "search_stock":               lambda args: search_stock(args[0] if args else ""),
    # 股票财务
    "stock_financial_analysis_indicator": lambda args: stock_financial_analysis_indicator(
                                     symbol=args[0] if args else "000001.SZ",
                                     start_year=args[1] if len(args) > 1 else "2020"),
    "stock_profit_forecast":     lambda args: stock_profit_forecast(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_balance_sheet_em":     lambda args: stock_balance_sheet_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_profit_sheet_em":      lambda args: stock_profit_sheet_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_cash_flow_em":         lambda args: stock_cash_flow_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_operation_board_name_em": lambda args: stock_operation_board_name_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_hold_num_em":          lambda args: stock_hold_num_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_float_hist_em":        lambda args: stock_float_hist_em(
                                     symbol=args[0] if args else "000001.SZ"),
    # 指数
    "stock_zh_index_spot_em":     lambda args: stock_zh_index_spot_em(),
    "index_zh_a_hist":            lambda args: index_zh_a_hist(
                                     symbol=args[0] if args else "000300.SH",
                                     period=args[1] if len(args) > 1 else "daily",
                                     count=int(args[2]) if len(args) > 2 and args[2].isdigit() else None),
    "stock_zh_index_hist_csindex": lambda args: stock_zh_index_hist_csindex(
                                     symbol=args[0] if args else "000300.SH",
                                     count=int(args[1]) if len(args) > 1 and args[1].isdigit() else None),
    # 概念/行业板块
    "stock_board_concept_name_em": lambda args: stock_board_concept_name_em(),
    "stock_board_concept_hist_em": lambda args: stock_board_concept_hist_em(
                                     symbol=args[0] if args else "BK0001"),
    "stock_board_industry_name_em": lambda args: stock_board_industry_name_em(),
    "stock_board_industry_hist_em": lambda args: stock_board_industry_hist_em(
                                     symbol=args[0] if args else "881001"),
    # 龙虎榜/大宗
    "stock_lhb_detail_em":         lambda args: stock_lhb_detail_em(
                                     symbol=args[0] if args else "000001.SZ"),
    "stock_bb_detail_em":          lambda args: stock_bb_detail_em(),
    # 基金
    "fund_open_fund_info_em":     lambda args: fund_open_fund_info_em(
                                     fund=args[0] if args else "000001"),
    "fund_etf_fund_info_em":      lambda args: fund_etf_fund_info_em(
                                     fund=args[0] if args else "510300"),
    "fund_fund_spot_em":          lambda args: fund_fund_spot_em(),
    # 期货
    "futures_goods_index_en":     lambda args: futures_goods_index_en(),
    "futures_spot":               lambda args: futures_spot(),
    "futures_zh_daily":           lambda args: futures_zh_daily(
                                     symbol=args[0] if args else "SI"),
    # 宏观
    "macro_china_gdp":            lambda args: macro_china_gdp(),
    "macro_china_cpi":            lambda args: macro_china_cpi(),
    "macro_china_ppi":            lambda args: macro_china_ppi(),
    "macro_china_money_supply":   lambda args: macro_china_money_supply(),
    "macro_china_fx":             lambda args: macro_china_fx(),
    "macro_china_sw":             lambda args: macro_china_sw(),
    # 外汇
    "forex_rmb_iist":             lambda args: forex_rmb_iist(),
    "currency_name":              lambda args: currency_name(),
    # 债券
    "bond_china_comparison":      lambda args: bond_china_comparison(),
    "bond_spot":                  lambda args: bond_spot(),
    # 数字货币
    "coin_bitget":                lambda args: coin_bitget(
                                     symbol=args[0] if args else "BTC",
                                     market=args[1] if len(args) > 1 else "USDT"),
    "coin_global":                lambda args: coin_global(),
    # 期权
    "option_sse":                 lambda args: option_sse(),
    # 港美股
    "stock_hk_spot":              lambda args: stock_hk_spot(),
    "stock_us_spot":              lambda args: stock_us_spot(),
}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "用法: python3 akshare_query.py <接口名> [参数...]",
            "supported": sorted(INTERFACE_MAP.keys())
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    interface = sys.argv[1]
    args = sys.argv[2:]

    if interface not in INTERFACE_MAP:
        print(json.dumps({
            "error": f"未知接口: {interface}",
            "supported": sorted(INTERFACE_MAP.keys())
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = INTERFACE_MAP[interface](args)

    output = {
        "interface": interface,
        "args": args,
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
