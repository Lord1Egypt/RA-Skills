#!/usr/bin/env python3
"""AkShare Stock Data Helper - 股票数据获取脚本

用法: python3 stock_data.py <command> [args...]

命令 (无参数):
  spot            沪深A股实时行情
  spot-sh         沪A股实时行情
  spot-sz         深A股实时行情
  spot-bj         京A股实时行情
  spot-cy         创业板实时行情
  spot-kc         科创板实时行情
  spot-us         美股实时行情
  spot-hk         港股实时行情
  fund-flow-rank  资金流向排名
  board-concept   概念板块列表
  board-concept-spot  概念板块行情
  board-industry  行业板块列表
  board-industry-spot 行业板块行情
  zt-pool         涨停股池
  margin-sse      上交所融资融券
  margin-szse     深交所融资融券
  hot-rank        股票热度排名

命令 (1个参数: symbol 或 name):
  info <symbol>              个股基本信息(东财)
  info-xq <symbol>           个股基本信息(雪球, 如 SH600519)
  intraday <symbol>          日内分时数据
  bid-ask <symbol>           行情报价
  financial-indicator <symbol>  财务主要指标
  top10 <symbol>             十大股东
  top10-free <symbol>        十大流通股东
  fund-flow <symbol>         个股资金流向
  board-concept-cons <name>  概念板块成份股
  board-industry-cons <name> 行业板块成份股
  dividend <symbol>          历史分红
  tick <symbol>              历史分笔
  lhbcg <date>               龙虎榜(YYYYMMDD)

命令 (多参数):
  hist <symbol> <start> <end> [daily|weekly|monthly] [""|qfq|hfq]
  hist-min <symbol> <1|5|15|30|60> <start_date> <end_date> [""|qfq|hfq]
  financial <symbol> [balance|profit|cashflow] [report|yearly|quarterly]
"""
import sys
import akshare as ak
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 30)


def to_csv(df):
    return df.to_csv(index=False)


def cmd_spot():
    print(to_csv(ak.stock_zh_a_spot_em()))


def cmd_spot_sh():
    print(to_csv(ak.stock_sh_a_spot_em()))


def cmd_spot_sz():
    print(to_csv(ak.stock_sz_a_spot_em()))


def cmd_spot_bj():
    print(to_csv(ak.stock_bj_a_spot_em()))


def cmd_spot_cy():
    print(to_csv(ak.stock_cy_a_spot_em()))


def cmd_spot_kc():
    print(to_csv(ak.stock_kc_a_spot_em()))


def cmd_spot_us():
    print(to_csv(ak.stock_us_spot_em()))


def cmd_spot_hk():
    print(to_csv(ak.stock_hk_spot_em()))


def cmd_hist(symbol, start, end, period="daily", adjust="qfq"):
    print(to_csv(ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start, end_date=end, adjust=adjust)))


def cmd_hist_min(symbol, period, start_date, end_date, adjust="qfq"):
    print(to_csv(ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)))


def cmd_intraday(symbol):
    print(to_csv(ak.stock_intraday_em(symbol=symbol)))


def cmd_info(symbol):
    print(to_csv(ak.stock_individual_info_em(symbol=symbol)))


def cmd_info_xq(symbol):
    print(to_csv(ak.stock_individual_basic_info_xq(symbol=symbol)))


def cmd_bid_ask(symbol):
    print(to_csv(ak.stock_bid_ask_em(symbol=symbol)))


def cmd_financial(symbol, report_type="balance", period_type="report"):
    if report_type == "balance":
        if period_type == "yearly":
            df = ak.stock_balance_sheet_by_yearly_em(symbol=symbol)
        else:
            df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
    elif report_type == "profit":
        if period_type == "yearly":
            df = ak.stock_profit_sheet_by_yearly_em(symbol=symbol)
        elif period_type == "quarterly":
            df = ak.stock_profit_sheet_by_quarterly_em(symbol=symbol)
        else:
            df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
    elif report_type == "cashflow":
        if period_type == "yearly":
            df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=symbol)
        elif period_type == "quarterly":
            df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=symbol)
        else:
            df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
    else:
        print(f"Unknown report_type: {report_type}")
        return
    print(to_csv(df))


def cmd_financial_indicator(symbol):
    print(to_csv(ak.stock_financial_analysis_indicator_em(symbol=symbol)))


def cmd_top10(symbol):
    print(to_csv(ak.stock_gdfx_top_10_em(symbol=symbol)))


def cmd_top10_free(symbol):
    print(to_csv(ak.stock_gdfx_free_top_10_em(symbol=symbol)))


def cmd_fund_flow(symbol):
    print(to_csv(ak.stock_individual_fund_flow(symbol=symbol)))


def cmd_fund_flow_rank():
    print(to_csv(ak.stock_individual_fund_flow_rank()))


def cmd_board_concept():
    print(to_csv(ak.stock_board_concept_name_em()))


def cmd_board_concept_spot():
    print(to_csv(ak.stock_board_concept_spot_em()))


def cmd_board_concept_cons(name):
    print(to_csv(ak.stock_board_concept_cons_em(symbol=name)))


def cmd_board_industry():
    print(to_csv(ak.stock_board_industry_name_em()))


def cmd_board_industry_spot():
    print(to_csv(ak.stock_board_industry_spot_em()))


def cmd_board_industry_cons(name):
    print(to_csv(ak.stock_board_industry_cons_em(symbol=name)))


def cmd_zt_pool():
    print(to_csv(ak.stock_zt_pool_em(date=None)))


def cmd_lhbcg(date):
    print(to_csv(ak.stock_lhb_detail_em(date=date)))


def cmd_margin_sse():
    print(to_csv(ak.stock_margin_sse()))


def cmd_margin_szse():
    print(to_csv(ak.stock_margin_szse()))


def cmd_hot_rank():
    print(to_csv(ak.stock_hot_rank_em()))


def cmd_dividend(symbol):
    print(to_csv(ak.stock_history_dividend(symbol=symbol)))


def cmd_tick(symbol):
    print(to_csv(ak.stock_zh_a_tick_tx(symbol=symbol)))


# Dispatch table: command -> (function, arg_count)
DISPATCH = {
    "spot": (cmd_spot, 0),
    "spot-sh": (cmd_spot_sh, 0),
    "spot-sz": (cmd_spot_sz, 0),
    "spot-bj": (cmd_spot_bj, 0),
    "spot-cy": (cmd_spot_cy, 0),
    "spot-kc": (cmd_spot_kc, 0),
    "spot-us": (cmd_spot_us, 0),
    "spot-hk": (cmd_spot_hk, 0),
    "fund-flow-rank": (cmd_fund_flow_rank, 0),
    "board-concept": (cmd_board_concept, 0),
    "board-concept-spot": (cmd_board_concept_spot, 0),
    "board-industry": (cmd_board_industry, 0),
    "board-industry-spot": (cmd_board_industry_spot, 0),
    "zt-pool": (cmd_zt_pool, 0),
    "margin-sse": (cmd_margin_sse, 0),
    "margin-szse": (cmd_margin_szse, 0),
    "hot-rank": (cmd_hot_rank, 0),
    "info": (cmd_info, 1),
    "info-xq": (cmd_info_xq, 1),
    "intraday": (cmd_intraday, 1),
    "bid-ask": (cmd_bid_ask, 1),
    "financial-indicator": (cmd_financial_indicator, 1),
    "top10": (cmd_top10, 1),
    "top10-free": (cmd_top10_free, 1),
    "fund-flow": (cmd_fund_flow, 1),
    "board-concept-cons": (cmd_board_concept_cons, 1),
    "board-industry-cons": (cmd_board_industry_cons, 1),
    "dividend": (cmd_dividend, 1),
    "tick": (cmd_tick, 1),
    "lhbcg": (cmd_lhbcg, 1),
}


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        print("\n可用命令:")
        for cmd in sorted(DISPATCH.keys()):
            print(f"  {cmd}")
        return

    cmd = args[0]

    if cmd == "hist":
        if len(args) < 4:
            print("用法: hist <symbol> <start> <end> [period] [adjust]")
            print("  period: daily|weekly|monthly  默认: daily")
            print("  adjust: ''|qfq|hfq            默认: qfq")
            return
        p = args[4] if len(args) > 4 else "daily"
        a = args[5] if len(args) > 5 else "qfq"
        cmd_hist(args[1], args[2], args[3], p, a)
        return

    if cmd == "hist-min":
        if len(args) < 5:
            print("用法: hist-min <symbol> <period_min> <start_date> <end_date> [adjust]")
            print("  period_min: 1|5|15|30|60")
            print("  adjust: ''|qfq|hfq  默认: qfq")
            return
        a = args[5] if len(args) > 5 else "qfq"
        cmd_hist_min(args[1], args[2], args[3], args[4], a)
        return

    if cmd == "financial":
        if len(args) < 2:
            print("用法: financial <symbol> [report_type] [period_type]")
            print("  report_type: balance|profit|cashflow  默认: balance")
            print("  period_type: report|yearly|quarterly   默认: report")
            return
        rt = args[2] if len(args) > 2 else "balance"
        pt = args[3] if len(args) > 3 else "report"
        cmd_financial(args[1], rt, pt)
        return

    if cmd in DISPATCH:
        func, argc = DISPATCH[cmd]
        if len(args) - 1 < argc:
            print(f"命令 {cmd} 需要 {argc} 个参数")
            return
        if argc == 0:
            func()
        else:
            func(args[1])
    else:
        print(f"未知命令: {cmd}")
        print(f"可用命令: {', '.join(sorted(DISPATCH.keys()))}")


if __name__ == "__main__":
    main()
