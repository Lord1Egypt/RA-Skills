#!/usr/bin/env python3
"""
Crypto K线数据采集器 - Binance API版
支持采集BTC、ETH等主流加密货币的K线数据
"""

import argparse
import sqlite3
import requests
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys


def get_default_db_path(symbol, interval):
    """获取默认数据库路径"""
    data_dir = Path.home() / ".openclaw" / "workspace" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    symbol_lower = symbol.lower().replace("USDT", "").replace("-", "")
    return data_dir / f"{symbol_lower}_{interval}_kline.db"


def init_db(db_path, table_name):
    """初始化数据库"""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            open_time TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            quote_volume REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cur.execute(f'CREATE INDEX IF NOT EXISTS idx_timestamp ON {table_name}(timestamp)')

    conn.commit()
    return conn


def fetch_klines(symbol, interval, start_date, end_date, proxy=None, limit=1000):
    """从Binance API获取K线数据"""
    url = "https://api.binance.com/api/v3/klines"

    # 转换日期为时间戳
    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000) + 86400000  # 加一天

    all_data = []
    current_start = start_ts

    proxies = {"http": proxy, "https": proxy} if proxy else None

    while current_start < end_ts:
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit,
            "startTime": current_start,
            "endTime": end_ts
        }

        try:
            resp = requests.get(url, params=params, proxies=proxies, timeout=30)
            data = resp.json()

            if not data or len(data) == 0:
                break

            all_data.extend(data)

            earliest = data[0]
            latest = data[-1]
            print(f"  获取 {len(data)}条, {datetime.fromtimestamp(earliest[0]/1000).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(latest[0]/1000).strftime('%Y-%m-%d')}")

            if len(data) < limit:
                break

            # 更新起始时间为最后一条的下一根K线
            current_start = data[-1][0] + 1
            time.sleep(0.3)

        except Exception as e:
            print(f"  ❌ 获取失败: {e}")
            break

    # 去重
    unique = {}
    for k in all_data:
        unique[k[0]] = k

    return sorted(unique.values(), key=lambda x: x[0])


def save_to_db(db_path, table_name, klines):
    """保存数据到数据库"""
    if not klines:
        return 0

    conn = init_db(db_path, table_name)
    cur = conn.cursor()

    count = 0
    for k in klines:
        ts = k[0]
        dt = datetime.fromtimestamp(ts / 1000)
        cur.execute(f'''
            INSERT OR REPLACE INTO {table_name}
            (timestamp, open_time, open, high, low, close, volume, quote_volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ts, dt.strftime("%Y-%m-%d %H:%M:%S"), k[1], k[2], k[3], k[4], k[5], k[7]))
        count += 1

    conn.commit()
    conn.close()
    return count


def main():
    parser = argparse.ArgumentParser(description="Crypto K线数据采集器 - Binance API")
    parser.add_argument("--symbol", "-s", default="BTCUSDT", help="交易对 (如 BTCUSDT, ETHUSDT)")
    parser.add_argument("--interval", "-i", default="1h", help="K线周期 (1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d, 1w)")
    parser.add_argument("--start-date", default="2024-01-01", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", default=None, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--db-path", "-d", default=None, help="数据库路径")
    parser.add_argument("--proxy", "-p", default="http://192.168.10.188:7897", help="HTTP代理")

    args = parser.parse_args()

    # 设置结束日期
    if args.end_date is None:
        args.end_date = datetime.now().strftime("%Y-%m-%d")

    # 获取数据库路径
    if args.db_path:
        db_path = Path(args.db_path)
    else:
        db_path = get_default_db_path(args.symbol, args.interval)

    # 创建表名
    table_name = f"{args.symbol.lower()}_{args.interval}_kline"

    print(f"📊 采集 {args.symbol} {args.interval} K线数据...")
    print(f"   日期: {args.start_date} ~ {args.end_date}")
    print(f"   数据库: {db_path}")

    # 获取数据
    klines = fetch_klines(
        args.symbol,
        args.interval,
        args.start_date,
        args.end_date,
        args.proxy
    )

    if not klines:
        print("❌ 未获取到数据")
        return

    print(f"\n获取到 {len(klines)} 条数据")

    # 保存到数据库
    count = save_to_db(db_path, table_name, klines)

    # 验证
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*), MIN(open_time), MAX(open_time) FROM {table_name}")
    r = cur.fetchone()
    print(f"\n✅ 保存完成!")
    print(f"   总记录: {r[0]}条")
    print(f"   范围: {r[1]} ~ {r[2]}")
    conn.close()


if __name__ == "__main__":
    main()
