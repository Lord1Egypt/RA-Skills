#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易日志系统
功能：记录每笔交易、策略信号、账户快照
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os

# ============ 配置 ============
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 日志文件
TRADE_LOG = LOG_DIR / "trades.csv"
SIGNAL_LOG = LOG_DIR / "signals.jsonl"
DAILY_SNAPSHOT = LOG_DIR / "daily_snapshots.jsonl"

# ============ 交易日志 ============

def init_trade_log():
    """初始化交易日志 CSV"""
    if not TRADE_LOG.exists():
        with open(TRADE_LOG, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "symbol", "name", "side", "quantity", "price",
                "amount", "currency", "strategy", "order_id", "status", "remark"
            ])

def log_trade(order: Dict):
    """记录交易"""
    init_trade_log()
    
    with open(TRADE_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            order.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            order["symbol"],
            order.get("name", ""),
            order["side"],
            order["quantity"],
            order["price"],
            order.get("amount", order["quantity"] * order["price"]),
            order.get("currency", "HKD"),
            order.get("strategy", "manual"),
            order.get("order_id", ""),
            order.get("status", "submitted"),
            order.get("remark", "")
        ])
    
    print(f"📝 交易日志已记录：{order['symbol']} {order['side']} {order['quantity']}股")

def get_trade_history(symbol: Optional[str] = None, limit: int = 50) -> List[Dict]:
    """获取交易历史"""
    if not TRADE_LOG.exists():
        return []
    
    trades = []
    with open(TRADE_LOG, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if symbol and row["symbol"] != symbol:
                continue
            trades.append(row)
    
    return trades[-limit:]

# ============ 策略信号日志 ============

def log_signal(signal: Dict):
    """记录策略信号"""
    record = {
        "timestamp": datetime.now().isoformat(),
        **signal
    }
    
    with open(SIGNAL_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"📝 策略信号已记录：{signal['symbol']} {signal['type']}")

def get_signals(strategy: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """获取策略信号历史"""
    if not SIGNAL_LOG.exists():
        return []
    
    signals = []
    with open(SIGNAL_LOG, "r", encoding="utf-8") as f:
        for line in f:
            signal = json.loads(line)
            if strategy and signal.get("strategy") != strategy:
                continue
            signals.append(signal)
    
    return signals[-limit:]

# ============ 账户快照 ============

def log_daily_snapshot(account_data: Dict):
    """记录每日账户快照"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        **account_data
    }
    
    with open(DAILY_SNAPSHOT, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    
    print(f"📝 账户快照已记录：总资产 {account_data.get('total_value', 0):,.2f}")

def get_performance_stats() -> Dict:
    """获取绩效统计"""
    if not DAILY_SNAPSHOT.exists():
        return {"error": "No data"}
    
    snapshots = []
    with open(DAILY_SNAPSHOT, "r", encoding="utf-8") as f:
        for line in f:
            snapshots.append(json.loads(line))
    
    if len(snapshots) < 2:
        return {"error": "Insufficient data"}
    
    # 计算收益
    first_value = snapshots[0].get("total_value", 0)
    last_value = snapshots[-1].get("total_value", 0)
    total_return = (last_value - first_value) / first_value if first_value > 0 else 0
    
    # 计算最大回撤
    peak = first_value
    max_drawdown = 0
    for snap in snapshots:
        value = snap.get("total_value", 0)
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak > 0 else 0
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return {
        "start_date": snapshots[0]["date"],
        "end_date": snapshots[-1]["date"],
        "initial_value": first_value,
        "current_value": last_value,
        "total_return": total_return,
        "total_return_pct": f"{total_return:.2%}",
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": f"{max_drawdown:.2%}",
        "trading_days": len(snapshots),
        "avg_daily_return": total_return / len(snapshots) if len(snapshots) > 0 else 0
    }

# ============ 策略绩效 ============

def get_strategy_performance(strategy: str) -> Dict:
    """获取单个策略绩效"""
    signals = get_signals(strategy=strategy)
    trades = get_trade_history()
    
    # 筛选该策略的交易
    strategy_trades = [t for t in trades if t.get("strategy") == strategy]
    
    if not strategy_trades:
        return {"error": "No trades for this strategy"}
    
    # 计算胜率
    wins = 0
    total_pnl = 0
    for trade in strategy_trades:
        # 简化计算，实际需要配对买卖
        total_pnl += float(trade.get("pnl", 0))
        if float(trade.get("pnl", 0)) > 0:
            wins += 1
    
    win_rate = wins / len(strategy_trades) if strategy_trades else 0
    
    return {
        "strategy": strategy,
        "total_trades": len(strategy_trades),
        "wins": wins,
        "losses": len(strategy_trades) - wins,
        "win_rate": f"{win_rate:.2%}",
        "total_pnl": total_pnl,
        "avg_pnl": total_pnl / len(strategy_trades) if strategy_trades else 0
    }

# ============ 命令行工具 ============

if __name__ == "__main__":
    import sys
    
    print("📊 交易日志系统")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 logger.py stats          - 查看绩效统计")
        print("  python3 logger.py strategy XXX   - 查看策略绩效")
        print("  python3 logger.py history [SYM]  - 查看交易历史")
        print("  python3 logger.py signals [STR]  - 查看策略信号")
    else:
        cmd = sys.argv[1]
        
        if cmd == "stats":
            stats = get_performance_stats()
            print("\n📈 绩效统计:")
            for k, v in stats.items():
                print(f"  {k}: {v}")
        
        elif cmd == "strategy" and len(sys.argv) > 2:
            strategy = sys.argv[2]
            perf = get_strategy_performance(strategy)
            print(f"\n📈 策略 '{strategy}' 绩效:")
            for k, v in perf.items():
                print(f"  {k}: {v}")
        
        elif cmd == "history":
            symbol = sys.argv[2] if len(sys.argv) > 2 else None
            trades = get_trade_history(symbol=symbol)
            print(f"\n📋 交易历史 ({len(trades)} 条):")
            for t in trades[-10:]:
                print(f"  {t['timestamp']}: {t['side']} {t['symbol']} {t['quantity']}股 @ {t['price']}")
        
        elif cmd == "signals":
            strategy = sys.argv[2] if len(sys.argv) > 2 else None
            signals = get_signals(strategy=strategy)
            print(f"\n📋 策略信号 ({len(signals)} 条):")
            for s in signals[-10:]:
                print(f"  {s['timestamp']}: {s['symbol']} {s['type']} -> {s['action']}")
