"""Stock Skill v3.2 - CLI 入口"""
from __future__ import annotations
import json, logging, sys
from .config import get_config
from .tools.tools import StockTools
from .semantic import execute_query

def _setup_logging():
    cfg = get_config()
    logging.basicConfig(level=getattr(logging,cfg.log_level,logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("stock_skill.log",encoding="utf-8")])

def main():
    _setup_logging()
    cfg = get_config()
    issues = cfg.validate()
    if issues:
        for i in issues: print(f"⚠ {i}")
        if len(sys.argv)<=1: sys.exit(1)
    tools = StockTools()
    args = sys.argv[1:]
    if not args:
        result = tools.full_review()
        print(result.get("summary",result.get("error",""))); return
    cmd = args[0]
    if cmd=="--review": r=tools.full_review(); print(r.get("summary",r.get("error","")))
    elif cmd=="--analyze" and len(args)>1: print(json.dumps(tools.analyze_stock(args[1]),ensure_ascii=False,indent=2))
    elif cmd=="--market": print(json.dumps(tools.analyze_market(),ensure_ascii=False,indent=2))
    elif cmd=="--quote" and len(args)>1: print(json.dumps(tools.get_quote(args[1]),ensure_ascii=False,indent=2))
    elif cmd=="--flow" and len(args)>1: print(json.dumps(tools.get_money_flow(args[1]),ensure_ascii=False,indent=2))
    elif cmd=="--breadth": print(json.dumps(tools.get_market_breadth(),ensure_ascii=False,indent=2))
    elif cmd=="--correlation" and len(args)>1: print(json.dumps(tools.check_correlation(args[1:]),ensure_ascii=False,indent=2))
    elif cmd=="--breaker": print(json.dumps(tools.circuit_breaker_check(),ensure_ascii=False,indent=2))
    elif cmd=="--positions": print(json.dumps(tools.get_positions(),ensure_ascii=False,indent=2))
    elif cmd=="--history": print(json.dumps(tools.get_signal_history(args[1] if len(args)>1 else None),ensure_ascii=False,indent=2))
    elif cmd=="--perf": print(json.dumps(tools.evaluate_signal_performance(),ensure_ascii=False,indent=2))
    elif cmd=="--attribution": print(json.dumps(tools.strategy_attribution(days=int(args[1]) if len(args)>1 else 30),ensure_ascii=False,indent=2))
    elif cmd=="--backtest-bt":
        # Backtrader 回测命令
        if len(args) < 2:
            print("用法: python -m stock_skill --backtest-bt <股票代码> [--strategy <策略名>] [--start <日期>] [--end <日期>] [--cash <资金>]")
            print("示例: python -m stock_skill --backtest-bt 600036.SH --strategy MAStrategy --start 2023-01-01 --end 2026-04-30")
            return
        code = args[1]
        strategy_name = 'MAStrategy'
        start_date = ''
        end_date = ''
        cash = 100000.0
        # 解析可选参数
        i = 2
        while i < len(args):
            if args[i] == '--strategy' and i + 1 < len(args):
                strategy_name = args[i + 1]; i += 2
            elif args[i] == '--start' and i + 1 < len(args):
                start_date = args[i + 1]; i += 2
            elif args[i] == '--end' and i + 1 < len(args):
                end_date = args[i + 1]; i += 2
            elif args[i] == '--cash' and i + 1 < len(args):
                cash = float(args[i + 1]); i += 2
            else:
                i += 1
        result = tools.backtest_bt(code, strategy_name, start_date, end_date, cash)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd=="--list-bt-strategies":
        # 列出可用的 Backtrader 策略
        from .strategies.backtrader_adapters import list_bt_strategies
        strategies = list_bt_strategies()
        print("可用的 Backtrader 策略:")
        for s in strategies:
            print(f"  - {s}")
    elif cmd=="--monitor":
        from .monitor import PollMonitor
        m=PollMonitor(tools); m.on_alert(lambda e,d: print(d.get("message",str(d)))); m.start(int(args[1]) if len(args)>1 else None)
    elif cmd=="--help": print(__doc__)
    else:
        result = execute_query(" ".join(args), tools)
        print(result.get("summary",json.dumps(result,ensure_ascii=False,indent=2)))

if __name__=="__main__": main()
