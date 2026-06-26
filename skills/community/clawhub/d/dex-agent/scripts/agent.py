#!/usr/bin/env python3
"""
DEX Agent — Autonomous DeFi Trading CLI
Bankr competitor. Direct DEX swaps on Base. Zero middleman.

Usage:
  python3 agent.py swap USDC WETH 5.0          # Swap 5 USDC for WETH
  python3 agent.py swap ETH USDC 0.01           # Swap 0.01 ETH for USDC
  python3 agent.py quote USDC WETH 10.0          # Get quote only
  python3 agent.py price WETH                    # Current price
  python3 agent.py price BRETT                   # Any token price
  python3 agent.py balances                      # Portfolio balances
  python3 agent.py stop WETH 2000 8.0 0.1        # Stop-loss: 8% below $2000
  python3 agent.py tp WETH 2000 5.0 0.1          # Take-profit: 5% above $2000
  python3 agent.py monitor                       # Check all orders
  python3 agent.py wallet                        # Show wallet info
  python3 agent.py wallet generate               # Generate new wallet
"""

import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd == "swap":
        from swap import DexSwapper
        if len(sys.argv) < 5:
            print("Usage: agent.py swap <token_in> <token_out> <amount> [slippage_bps] [fee]")
            return
        swapper = DexSwapper()
        token_in = sys.argv[2]
        token_out = sys.argv[3]
        amount = float(sys.argv[4])
        slippage = int(sys.argv[5]) if len(sys.argv) > 5 else 100
        fee = int(sys.argv[6]) if len(sys.argv) > 6 else 3000

        if token_in.upper() == "ETH":
            result = swapper.swap_eth_for_token(token_out, amount, slippage, fee)
        else:
            result = swapper.swap(token_in, token_out, amount, slippage, fee)

        if result and result["status"] == "success":
            print(f"\n🏆 Trade complete! basescan.org/tx/{result['tx_hash']}")

    elif cmd == "quote":
        from swap import DexSwapper
        if len(sys.argv) < 5:
            print("Usage: agent.py quote <token_in> <token_out> <amount>")
            return
        swapper = DexSwapper()
        from config import TOKENS
        token_in = sys.argv[2]
        token_out = sys.argv[3]
        amount = float(sys.argv[4])

        if token_in.upper() in TOKENS:
            token_in_addr = TOKENS[token_in.upper()]
        else:
            token_in_addr = token_in

        if token_out.upper() in TOKENS:
            token_out_addr = TOKENS[token_out.upper()]
        else:
            token_out_addr = token_out

        in_info = swapper.get_token_info(token_in_addr)
        out_info = swapper.get_token_info(token_out_addr)
        amount_raw = int(amount * (10 ** in_info["decimals"]))

        for fee in [500, 3000, 10000]:
            quote = swapper.get_quote(token_in_addr, token_out_addr, amount_raw, fee)
            if quote:
                out_human = quote / (10 ** out_info["decimals"])
                print(f"  Fee {fee/10000:.2%}: {amount} {in_info['symbol']} → {out_human:.6f} {out_info['symbol']}")

    elif cmd == "price":
        from price_monitor import PriceMonitor
        if len(sys.argv) < 3:
            print("Usage: agent.py price <token>")
            return
        monitor = PriceMonitor()
        token = sys.argv[2]
        price = monitor.get_price(token)
        if price:
            print(f"💰 {token.upper()}: ${price:.6f}")
        else:
            print(f"❌ Could not get price for {token}")

    elif cmd == "balances":
        from wallet import load_wallet, get_balances
        addr, _ = load_wallet()
        if addr:
            get_balances(addr)

    elif cmd == "stop":
        from price_monitor import PriceMonitor
        if len(sys.argv) < 6:
            print("Usage: agent.py stop <token> <entry_price> <stop_pct> <amount>")
            return
        monitor = PriceMonitor()
        monitor.add_stop_loss(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

    elif cmd == "tp":
        from price_monitor import PriceMonitor
        if len(sys.argv) < 6:
            print("Usage: agent.py tp <token> <entry_price> <profit_pct> <amount>")
            return
        monitor = PriceMonitor()
        monitor.add_take_profit(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

    elif cmd == "monitor":
        from price_monitor import PriceMonitor
        monitor = PriceMonitor()
        triggered = monitor.check_orders()
        if triggered:
            # Auto-execute triggered orders
            from swap import DexSwapper
            swapper = DexSwapper()
            for order in triggered:
                print(f"\n⚡ Executing {order['type']}: selling {order['amount']} {order['token']}")
                result = swapper.swap(order['token'], "USDC", order['amount'])
                if result and result["status"] == "success":
                    print(f"   ✅ Sold! Tx: {result['tx_hash']}")

    elif cmd == "wallet":
        if len(sys.argv) > 2 and sys.argv[2] == "generate":
            from wallet import generate_wallet
            generate_wallet()
        else:
            from wallet import load_wallet, get_balances
            addr, _ = load_wallet()
            if addr:
                print(f"🔑 Wallet: {addr}")
                get_balances(addr)

    elif cmd == "scan":
        # Integration with existing momentum scanner
        print("🔍 Running momentum scan + auto-trade via DEX Agent...")
        from price_monitor import PriceMonitor
        monitor = PriceMonitor()

        # Get prices for all tracked tokens
        from config import TOKENS
        print("\n📊 Current Prices:")
        for name, addr in TOKENS.items():
            if name in ["WETH", "USDC", "USDbC"]:
                continue
            price = monitor.get_price(addr)
            if price:
                print(f"   {name}: ${price:.6f}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
