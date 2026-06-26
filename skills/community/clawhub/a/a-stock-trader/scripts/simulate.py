#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟交易脚本 / Paper Trading Script

功能 / Function:
    - 模拟买入卖出 / Simulate buy/sell
    - 持仓管理 / Position management
    - 盈亏计算 / PnL calculation
    - 账户管理 / Account management
"""

import sqlite3
import os
from datetime import datetime

# 数据库路径 / Database path
DB_PATH = os.path.expanduser("~/.openclaw/workspace/a-stock/data.db")

def init_trading_db():
    """
    初始化交易数据库 / Initialize trading database
    创建持仓表、交易记录表、账户表 / Create positions, trades, account tables
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 持仓表 / Positions table
    c.execute('''CREATE TABLE IF NOT EXISTS positions (
        code TEXT PRIMARY KEY, name TEXT, shares INTEGER, 
        cost REAL, buy_date TEXT
    )''')
    
    # 交易记录表 / Trades table
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, code TEXT, name TEXT, type TEXT,
        price REAL, shares INTEGER, pnl REAL
    )''')
    
    # 账户表 / Account table
    c.execute('''CREATE TABLE IF NOT EXISTS account (
        id INTEGER PRIMARY KEY, cash REAL, total_value REAL, updated TEXT
    )''')
    
    # 初始化账户（100万模拟金）/ Initialize account (1M simulated)
    c.execute("SELECT * FROM account WHERE id=1")
    if not c.fetchone():
        c.execute("INSERT INTO account (id, cash, total_value) VALUES (1, 1000000, 1000000)")
    
    conn.commit()
    return conn

def get_account(conn):
    """
    获取账户信息 / Get account info
    返回现金和持仓 / Return cash and positions
    """
    c = conn.cursor()
    c.execute("SELECT cash FROM account WHERE id=1")
    cash = c.fetchone()[0]
    
    c.execute("SELECT code, name, shares, cost FROM positions")
    positions = c.fetchall()
    
    return {"cash": cash, "positions": positions}

def buy(conn, code, name, price, shares):
    """
    买入 / Buy stocks
    参数 / Parameters:
        conn: 数据库连接 (database connection)
        code: 股票代码 (stock code)
        name: 股票名称 (stock name)
        price: 买入价格 (buy price)
        shares: 股数 (number of shares)
    """
    c = conn.cursor()
    cost = price * shares
    
    c.execute("SELECT cash FROM account WHERE id=1")
    cash = c.fetchone()[0]
    
    if cash < cost:
        print(f"资金不足! 需要 {cost:.2f}, 当前 {cash:.2f} / Insufficient funds! Need {cost:.2f}, have {cash:.2f}")
        return False
    
    # 扣款 / Deduct cash
    c.execute("UPDATE account SET cash = cash - ? WHERE id=1", (cost,))
    
    # 更新持仓 / Update position
    c.execute("SELECT * FROM positions WHERE code=?", (code,))
    pos = c.fetchone()
    
    if pos:
        # 追加持仓 / Add to position
        old_shares, old_cost = pos[2], pos[3]
        new_shares = old_shares + shares
        new_cost = (old_shares * old_cost + cost) / new_shares
        c.execute("UPDATE positions SET shares=?, cost=? WHERE code=?", 
                 (new_shares, new_cost, code))
    else:
        # 新建持仓 / New position
        c.execute("INSERT INTO positions (code, name, shares, cost, buy_date) VALUES (?, ?, ?, ?, ?)",
                  (code, name, shares, price, datetime.now().strftime("%Y-%m-%d")))
    
    # 记录交易 / Record trade
    c.execute("INSERT INTO trades (date, code, name, type, price, shares) VALUES (?, ?, ?, 'BUY', ?, ?)",
              (datetime.now().strftime("%Y-%m-%d"), code, name, price, shares))
    
    conn.commit()
    print(f"买入 / Bought {code} {name} {shares}股 @ ¥{price:.2f}")
    return True

def sell(conn, code, price, shares):
    """
    卖出 / Sell stocks
    参数 / Parameters:
        conn: 数据库连接 (database connection)
        code: 股票代码 (stock code)
        price: 卖出价格 (sell price)
        shares: 股数 (number of shares)
    """
    c = conn.cursor()
    
    c.execute("SELECT shares, cost, name FROM positions WHERE code=?", (code,))
    pos = c.fetchone()
    
    if not pos or pos[0] < shares:
        print(f"持仓不足! / Insufficient position!")
        return False
    
    # 更新持仓 / Update position
    new_shares = pos[0] - shares
    if new_shares == 0:
        c.execute("DELETE FROM positions WHERE code=?", (code,))
    else:
        c.execute("UPDATE positions SET shares=? WHERE code=?", (new_shares, code))
    
    # 收款 / Add revenue
    revenue = price * shares
    c.execute("UPDATE account SET cash = cash + ? WHERE id=1", (revenue,))
    
    # 计算盈亏 / Calculate PnL
    pnl = (price - pos[1]) * shares
    
    # 记录交易 / Record trade
    c.execute("INSERT INTO trades (date, code, name, type, price, shares, pnl) VALUES (?, ?, ?, 'SELL', ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d"), code, pos[2], price, shares, pnl))
    
    conn.commit()
    print(f"卖出 / Sold {code} {pos[2]} {shares}股 @ ¥{price:.2f}, 盈亏 / PnL: ¥{pnl:.2f}")
    return True

def show_portfolio(conn):
    """
    显示持仓 / Display portfolio
    打印账户现金、持仓详情、总资产 / Print cash, positions, total assets
    """
    c = conn.cursor()
    c.execute("SELECT cash FROM account WHERE id=1")
    cash = c.fetchone()[0]
    
    c.execute("SELECT code, name, shares, cost FROM positions")
    positions = c.fetchall()
    
    print(f"\n{'='*50}")
    print(f"账户现金 / Cash: ¥{cash:,.2f}")
    print(f"{'='*50}")
    print(f"{'代码':<8} {'名称':<10} {'股数':<8} {'成本':<10} {'现价':<10}")
    print(f"{'-'*50}")
    
    total_value = cash
    for p in positions:
        code, name, shares, cost = p
        # 模拟现价 = 成本 * 1.05 (实际应该实时获取) / Simulated price (should fetch real price)
        current_price = cost * 1.05
        value = shares * current_price
        total_value += value
        print(f"{code:<8} {name:<10} {shares:<8} {cost:<10.2f} {current_price:<10.2f}")
    
    print(f"{'-'*50}")
    print(f"总资产 / Total: ¥{total_value:,.2f}")
    print(f"{'='*50}")

def main():
    """
    主函数 / Main function
    命令行入口 / CLI entry point
    """
    import argparse
    parser = argparse.ArgumentParser(description='模拟交易 / Paper Trading')
    parser.add_argument("--strategy", default="ma", help="策略 / Strategy")
    parser.add_argument("--stock", help="股票代码 / Stock code")
    parser.add_argument("--buy", action="store_true", help="买入 / Buy")
    parser.add_argument("--sell", action="store_true", help="卖出 / Sell")
    parser.add_argument("--shares", type=int, help="股数 / Shares")
    parser.add_argument("--price", type=float, help="价格 / Price")
    parser.add_argument("--show", action="store_true", help="显示持仓 / Show portfolio")
    args = parser.parse_args()
    
    conn = init_trading_db()
    
    if args.show:
        show_portfolio(conn)
    elif args.buy and args.stock and args.shares and args.price:
        buy(conn, args.stock, args.stock, args.price, args.shares)
    elif args.sell and args.stock and args.shares and args.price:
        sell(conn, args.stock, args.price, args.shares)
    else:
        print("用法 / Usage:")
        print("  python simulate.py --show                    # 显示持仓 / Show portfolio")
        print("  python simulate.py --buy --stock 600519 --shares 1000 --price 50.0  # 买入 / Buy")

if __name__ == "__main__":
    main()
