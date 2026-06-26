#!/usr/bin/env python3
"""A股模拟炒股引擎 - 基于akshare实时行情"""

import json
import os
import sys
import argparse
from datetime import datetime, date
from pathlib import Path

PORTFOLIO_DIR = Path.home() / ".openclaw" / "paper-trade"
PORTFOLIO_FILE = PORTFOLIO_DIR / "portfolio.json"
INITIAL_CASH = 50_000  # 5万初始资金


def _ensure_dir():
    PORTFOLIO_DIR.mkdir(parents=True, exist_ok=True)


def _load_portfolio() -> dict:
    _ensure_dir()
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "cash": INITIAL_CASH,
        "initial_cash": INITIAL_CASH,
        "positions": {},  # {symbol: {name, qty, cost_price, buy_date}}
        "transactions": [],  # [{date, time, type, symbol, name, price, qty, amount}]
        "created_at": datetime.now().isoformat(),
    }


def _save_portfolio(pf: dict):
    _ensure_dir()
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(pf, f, ensure_ascii=False, indent=2)


def _sina_code(code: str) -> str:
    """6位代码转新浪格式"""
    code = code.replace("SH.", "").replace("SZ.", "").replace("sh.", "").replace("sz.", "")
    if code.startswith("6"):
        return f"sh{code}"
    elif code.startswith(("0", "3")):
        return f"sz{code}"
    elif code.startswith("8") or code.startswith("4"):
        return f"bj{code}"
    return f"sz{code}"


def _clean_code(code: str) -> str:
    """标准化为纯6位代码"""
    return code.replace("SH.", "").replace("SZ.", "").replace("sh.", "").replace("sz.", "")


def _get_realtime_quote(symbol: str) -> dict:
    """获取实时行情，使用新浪HTTP接口（直连稳定）"""
    import requests

    code = _clean_code(symbol)
    sc = _sina_code(code)
    url = f"http://hq.sinajs.cn/list={sc}"
    try:
        r = requests.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=10)
        r.encoding = "gbk"
        text = r.text.strip()
        # var hq_str_sh600519="贵州茅台,1416.000,..."
        if not text or "=" not in text:
            return None
        data_str = text.split('"')[1]
        fields = data_str.split(",")
        if len(fields) < 32:
            return None

        name = fields[0]
        try:
            price = float(fields[3]) if fields[3] else 0
        except ValueError:
            price = 0

        return {
            "symbol": code,
            "name": name,
            "price": price,
            "open": float(fields[1]) if fields[1] else 0,
            "prev_close": float(fields[2]) if fields[2] else 0,
            "high": float(fields[4]) if fields[4] else 0,
            "low": float(fields[5]) if fields[5] else 0,
            "volume": float(fields[8]) if fields[8] else 0,
            "turnover": float(fields[9]) if fields[9] else 0,
            "change": price - float(fields[2]) if fields[2] else 0,
            "change_pct": ((price - float(fields[2])) / float(fields[2]) * 100) if fields[2] and float(fields[2]) > 0 else 0,
        }
    except Exception as e:
        return {"error": str(e)}


def _get_realtime_quotes_batch(symbols: list) -> list:
    """批量获取行情"""
    import requests

    codes = [_clean_code(s) for s in symbols]
    scodes = ",".join(_sina_code(c) for c in codes)
    url = f"http://hq.sinajs.cn/list={scodes}"
    try:
        r = requests.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=10)
        r.encoding = "gbk"
        results = []
        for line in r.text.strip().split("\n"):
            if not line or "=" not in line:
                continue
            code_raw = line.split("_str_")[1].split("=")[0] if "_str_" in line else ""
            code = code_raw[2:]  # 去掉 sh/sz 前缀
            data_str = line.split('"')[1]
            fields = data_str.split(",")
            if len(fields) < 10:
                continue
            try:
                price = float(fields[3]) if fields[3] else 0
                prev = float(fields[2]) if fields[2] else 0
                results.append({
                    "symbol": code,
                    "name": fields[0],
                    "price": price,
                    "open": float(fields[1]) if fields[1] else 0,
                    "prev_close": prev,
                    "high": float(fields[4]) if fields[4] else 0,
                    "low": float(fields[5]) if fields[5] else 0,
                    "volume": float(fields[8]) if fields[8] else 0,
                    "turnover": float(fields[9]) if fields[9] else 0,
                    "change": price - prev,
                    "change_pct": ((price - prev) / prev * 100) if prev > 0 else 0,
                })
            except (ValueError, IndexError):
                continue
        return results
    except Exception as e:
        return [{"error": str(e)}]


def _get_kline(symbol: str, days: int = 30) -> list:
    """获取日K线"""
    import akshare as ak

    code = symbol.replace("SH.", "").replace("SZ.", "").replace("sh.", "").replace("sz.", "")
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        if df is None or df.empty:
            return []
        records = df.tail(days).to_dict("records")
        result = []
        for r in records:
            result.append({
                "date": str(r["日期"]),
                "open": float(r["开盘"]),
                "high": float(r["最高"]),
                "low": float(r["最低"]),
                "close": float(r["收盘"]),
                "volume": float(r["成交量"]),
                "turnover": float(r["成交额"]),
            })
        return result
    except Exception as e:
        return [{"error": str(e)}]


def cmd_init(args):
    """初始化账户"""
    pf = _load_portfolio()
    if PORTFOLIO_FILE.exists() and not args.reset:
        print(json.dumps({"info": "账户已存在", "cash": pf["cash"], "positions_count": len(pf["positions"])}, ensure_ascii=False, indent=2))
        return
    pf = {
        "cash": INITIAL_CASH,
        "initial_cash": INITIAL_CASH,
        "positions": {},
        "transactions": [],
        "created_at": datetime.now().isoformat(),
    }
    _save_portfolio(pf)
    print(json.dumps({"ok": f"账户初始化完成，初始资金 {INITIAL_CASH:,.0f} 元"}, ensure_ascii=False, indent=2))


def cmd_quote(args):
    """查实时行情"""
    if args.all:
        # 大盘概览
        import akshare as ak
        try:
            indices = ak.stock_zh_index_spot_em()
            for code in ["000001", "399001", "399006"]:
                row = indices[indices["代码"] == code]
                if not row.empty:
                    r = row.iloc[0]
                    print(f"{r['名称']}: {r['最新价']} ({r['涨跌幅']}%)  成交额: {r['成交额']}")
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return

    result = []
    for s in args.symbols:
        q = _get_realtime_quote(s)
        if q:
            result.append(q)
        else:
            result.append({"symbol": s, "error": "未找到该股票"})
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


def cmd_kline(args):
    """查K线"""
    data = _get_kline(args.symbol, args.days)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_buy(args):
    """买入"""
    pf = _load_portfolio()
    q = _get_realtime_quote(args.symbol)
    if not q or "error" in q:
        print(json.dumps({"error": f"无法获取行情: {q}"}, ensure_ascii=False))
        return

    price = args.price or q["price"]
    qty = args.qty
    amount = price * qty * 100  # A股100股一手
    fee = max(amount * 0.0003, 5)  # 佣金万三，最低5元
    total = amount + fee

    if total > pf["cash"]:
        print(json.dumps({"error": f"资金不足，需要 {total:,.2f} 元，可用 {pf['cash']:,.2f} 元"}, ensure_ascii=False))
        return

    if not isinstance(qty, int) or qty <= 0:
        print(json.dumps({"error": "数量必须是正整数（手数，1手=100股）"}, ensure_ascii=False))
        return

    now = datetime.now()
    symbol = q["symbol"]

    # 更新持仓
    if symbol in pf["positions"]:
        pos = pf["positions"][symbol]
        old_total_cost = pos["cost_price"] * pos["qty"]
        new_total_cost = price * qty * 100
        pos["qty"] += qty * 100
        pos["cost_price"] = (old_total_cost + new_total_cost) / pos["qty"]
    else:
        pf["positions"][symbol] = {
            "name": q["name"],
            "qty": qty * 100,
            "cost_price": price,
            "buy_date": now.strftime("%Y-%m-%d"),
        }

    pf["cash"] -= total
    pf["transactions"].append({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "type": "buy",
        "symbol": symbol,
        "name": q["name"],
        "price": price,
        "qty": qty * 100,
        "amount": amount,
        "fee": round(fee, 2),
        "total": round(total, 2),
    })

    _save_portfolio(pf)
    print(json.dumps({
        "ok": f"买入 {q['name']}({symbol}) {qty}手 x {price} 元",
        "amount": round(amount, 2),
        "fee": round(fee, 2),
        "cash_remaining": round(pf["cash"], 2),
    }, ensure_ascii=False, indent=2))


def cmd_sell(args):
    """卖出"""
    pf = _load_portfolio()
    q = _get_realtime_quote(args.symbol)
    if not q or "error" in q:
        print(json.dumps({"error": f"无法获取行情: {q}"}, ensure_ascii=False))
        return

    symbol = q["symbol"]
    if symbol not in pf["positions"]:
        print(json.dumps({"error": f"未持有 {q['name']}({symbol})"}, ensure_ascii=False))
        return

    pos = pf["positions"][symbol]
    qty = args.qty * 100

    if qty > pos["qty"]:
        print(json.dumps({"error": f"持仓不足，当前持有 {pos['qty']} 股，想卖 {qty} 股"}, ensure_ascii=False))
        return

    if not isinstance(args.qty, int) or args.qty <= 0:
        print(json.dumps({"error": "数量必须是正整数（手数）"}, ensure_ascii=False))
        return

    price = args.price or q["price"]
    amount = price * qty
    fee = max(amount * 0.0003, 5)
    stamp_tax = amount * 0.001  # 印花税千一（卖出）
    total_fee = fee + stamp_tax
    received = amount - total_fee

    now = datetime.now()
    cost_basis = pos["cost_price"] * qty
    profit = received - cost_basis
    profit_pct = (profit / cost_basis) * 100 if cost_basis > 0 else 0

    pf["cash"] += received
    pos["qty"] -= qty
    if pos["qty"] == 0:
        del pf["positions"][symbol]

    pf["transactions"].append({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "type": "sell",
        "symbol": symbol,
        "name": q["name"],
        "price": price,
        "qty": qty,
        "amount": amount,
        "fee": round(fee, 2),
        "stamp_tax": round(stamp_tax, 2),
        "total_fee": round(total_fee, 2),
        "received": round(received, 2),
        "profit": round(profit, 2),
        "profit_pct": round(profit_pct, 2),
    })

    _save_portfolio(pf)
    print(json.dumps({
        "ok": f"卖出 {q['name']}({symbol}) {args.qty}手 x {price} 元",
        "profit": round(profit, 2),
        "profit_pct": round(profit_pct, 2),
        "cash": round(pf["cash"], 2),
    }, ensure_ascii=False, indent=2))


def cmd_positions(args):
    """查看持仓"""
    pf = _load_portfolio()
    if not pf["positions"]:
        print(json.dumps({"info": "暂无持仓", "cash": round(pf["cash"], 2)}, ensure_ascii=False, indent=2))
        return

    total_market = 0
    total_cost = 0
    result = []
    for symbol, pos in pf["positions"].items():
        q = _get_realtime_quote(symbol)
        if q and "error" not in q:
            market_val = q["price"] * pos["qty"]
            cost_val = pos["cost_price"] * pos["qty"]
            pnl = market_val - cost_val
            pnl_pct = (pnl / cost_val) * 100 if cost_val > 0 else 0
            total_market += market_val
            total_cost += cost_val
            result.append({
                "symbol": symbol,
                "name": pos["name"],
                "qty": pos["qty"],
                "cost_price": round(pos["cost_price"], 3),
                "current_price": q["price"],
                "market_value": round(market_val, 2),
                "cost_value": round(cost_val, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 2),
                "change_pct": q["change_pct"],
            })
        else:
            cost_val = pos["cost_price"] * pos["qty"]
            total_cost += cost_val
            result.append({
                "symbol": symbol,
                "name": pos["name"],
                "qty": pos["qty"],
                "cost_price": round(pos["cost_price"], 3),
                "market_value": "N/A (行情获取失败)",
                "pnl": "N/A",
            })

    total_pnl = total_market - total_cost if total_market > 0 else "N/A"
    print(json.dumps({
        "positions": result,
        "total_market_value": round(total_market, 2) if total_market > 0 else "N/A",
        "total_cost": round(total_cost, 2),
        "total_pnl": round(total_pnl, 2) if isinstance(total_pnl, float) else total_pnl,
        "cash": round(pf["cash"], 2),
        "total_assets": round(total_market + pf["cash"], 2) if total_market > 0 else "N/A",
        "initial_cash": pf["initial_cash"],
    }, ensure_ascii=False, indent=2, default=str))


def cmd_balance(args):
    """查看账户"""
    pf = _load_portfolio()
    total_market = 0
    for symbol, pos in pf["positions"].items():
        q = _get_realtime_quote(symbol)
        if q and "error" not in q:
            total_market += q["price"] * pos["qty"]
        else:
            total_market += pos["cost_price"] * pos["qty"]

    total_assets = total_market + pf["cash"]
    total_pnl = total_assets - pf["initial_cash"]
    total_pnl_pct = (total_pnl / pf["initial_cash"]) * 100

    print(json.dumps({
        "initial_cash": pf["initial_cash"],
        "cash": round(pf["cash"], 2),
        "market_value": round(total_market, 2),
        "total_assets": round(total_assets, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
        "positions_count": len(pf["positions"]),
        "transactions_count": len(pf["transactions"]),
    }, ensure_ascii=False, indent=2))


def cmd_history(args):
    """查看交易记录"""
    pf = _load_portfolio()
    txs = pf["transactions"]
    if args.limit:
        txs = txs[-args.limit:]
    print(json.dumps({
        "total": len(pf["transactions"]),
        "showing": len(txs),
        "transactions": txs,
    }, ensure_ascii=False, indent=2))


def cmd_rank(args):
    """涨幅/跌幅排行"""
    import akshare as ak
    try:
        df = ak.stock_zh_a_spot_em()
        df = df.sort_values("涨跌幅", ascending=args.bottom)
        cols = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交量", "成交额"]
        result = df[cols].head(args.top).to_dict("records")
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def cmd_search(args):
    """搜索股票"""
    import akshare as ak
    try:
        df = ak.stock_zh_a_spot_em()
        mask = df["代码"].str.contains(args.keyword) | df["名称"].str.contains(args.keyword)
        matched = df[mask][["代码", "名称", "最新价", "涨跌幅"]].head(args.top).to_dict("records")
        print(json.dumps(matched, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="A股模拟炒股")
    sub = parser.add_subparsers(dest="command")

    # init
    p = sub.add_parser("init", help="初始化账户")
    p.add_argument("--reset", action="store_true", help="重置账户")

    # quote
    p = sub.add_parser("quote", help="实时行情")
    p.add_argument("symbols", nargs="*", help="股票代码(6位)")
    p.add_argument("--all", action="store_true", help="大盘概览")

    # kline
    p = sub.add_parser("kline", help="日K线")
    p.add_argument("symbol", help="股票代码")
    p.add_argument("--days", type=int, default=30, help="天数")

    # buy
    p = sub.add_parser("buy", help="买入")
    p.add_argument("symbol", help="股票代码")
    p.add_argument("qty", type=int, help="买入数量(手)")
    p.add_argument("--price", type=float, default=None, help="指定价格(默认市价)")

    # sell
    p = sub.add_parser("sell", help="卖出")
    p.add_argument("symbol", help="股票代码")
    p.add_argument("qty", type=int, help="卖出数量(手)")
    p.add_argument("--price", type=float, default=None, help="指定价格(默认市价)")

    # positions
    sub.add_parser("positions", help="查看持仓")

    # balance
    sub.add_parser("balance", help="账户总览")

    # history
    p = sub.add_parser("history", help="交易记录")
    p.add_argument("--limit", type=int, default=None, help="最近N条")

    # rank
    p = sub.add_parser("rank", help="涨跌幅排行")
    p.add_argument("--top", type=int, default=10, help="前N名")
    p.add_argument("--bottom", action="store_true", help="跌幅排行")

    # search
    p = sub.add_parser("search", help="搜索股票")
    p.add_argument("keyword", help="代码或名称关键词")
    p.add_argument("--top", type=int, default=10, help="最多返回条数")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmd_map = {
        "init": cmd_init, "quote": cmd_quote, "kline": cmd_kline,
        "buy": cmd_buy, "sell": cmd_sell, "positions": cmd_positions,
        "balance": cmd_balance, "history": cmd_history,
        "rank": cmd_rank, "search": cmd_search,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
