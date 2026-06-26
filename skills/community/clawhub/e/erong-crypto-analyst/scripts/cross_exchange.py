#!/usr/bin/env python3
"""
Cross-Exchange Price Comparison
Compares prices between OKX and Binance to find arbitrage opportunities.
"""

import sys
import requests
import re
import argparse
import os

# ─── OKX ticker ───

def get_okx_price(symbol: str) -> float | None:
    """Get current price from OKX public API (no auth needed)"""
    instId = symbol.upper().replace('-', '-')
    url = f"https://www.okx.com/api/v5/market/ticker?instId={instId}-USDT"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get('data'):
            return float(data['data'][0]['last'])
    except Exception as e:
        print(f"OKX error: {e}", file=sys.stderr)
    return None

# ─── Binance ticker ───

def get_binance_price(symbol: str) -> float | None:
    """Get current price from Binance US (Binance main is blocked in China)"""
    symbol = symbol.upper().replace('-', '') + 'USD'
    # Try Binance US first, then OKX as fallback reference
    for base_url in [
        f"https://api.binance.us/api/v3/ticker/price?symbol={symbol}",
    ]:
        try:
            r = requests.get(base_url, timeout=10)
            data = r.json()
            if 'price' in data:
                return float(data['price'])
        except Exception:
            pass
    # Fallback: use Binance klines summary via alternative.me or OKX spot reference
    return None

# ─── Main ───

def main():
    parser = argparse.ArgumentParser(description='跨交易所价格对比')
    parser.add_argument('symbol', nargs='?', default='BTC', help='交易对，如 BTC、ETH')
    args = parser.parse_args()

    symbol = args.symbol.upper().replace('-', '')

    okx_price = get_okx_price(symbol)
    binance_price = get_binance_price(symbol)

    print(f'╔══════════════════════════════════════╗')
    print(f'║     跨交易所价格对比 [{symbol}]        ║')
    print(f'╠══════════════════════════════════════╣')

    if okx_price:
        print(f'║  OKX:     ${okx_price:,.2f}              ║')
    else:
        print(f'║  OKX:     获取失败                    ║')

    if binance_price:
        print(f'║  Binance: ${binance_price:,.2f}              ║')
    else:
        print(f'║  Binance: 获取失败                   ║')

    print(f'╚══════════════════════════════════════╝')

    if okx_price and binance_price:
        diff = abs(okx_price - binance_price)
        diff_pct = diff / max(okx_price, binance_price) * 100
        winner = 'OKX 更高' if okx_price > binance_price else 'Binance 更高'
        gap = '✅ 正常价差' if diff_pct < 0.1 else '⚠️ 存在价差'
        if diff_pct >= 0.1:
            gap += f' → 可套利!'

        print(f'\n价差: ${diff:.2f} ({diff_pct:.3f}%)')
        print(f'结论: {winner} | {gap}')

if __name__ == '__main__':
    main()
