"""
Price Monitor — DIY stop-loss and take-profit system
No Bankr Club needed. Direct on-chain price checks.
"""

import json
import sys
import time
from pathlib import Path
from web3 import Web3
from config import TOKENS, UNISWAP
from rpc import get_w3, call_with_retry

ORDERS_FILE = Path(__file__).parent / "active-orders.json"

QUOTER_ABI = [
    {
        "inputs": [{
            "components": [
                {"name": "tokenIn", "type": "address"},
                {"name": "tokenOut", "type": "address"},
                {"name": "amountIn", "type": "uint256"},
                {"name": "fee", "type": "uint24"},
                {"name": "sqrtPriceLimitX96", "type": "uint160"},
            ],
            "name": "params",
            "type": "tuple"
        }],
        "name": "quoteExactInputSingle",
        "outputs": [
            {"name": "amountOut", "type": "uint256"},
            {"name": "sqrtPriceX96After", "type": "uint160"},
            {"name": "initializedTicksCrossed", "type": "uint32"},
            {"name": "gasEstimate", "type": "uint256"},
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
]


class PriceMonitor:
    def __init__(self):
        self.w3 = get_w3()
        self.quoter = self.w3.eth.contract(
            address=Web3.to_checksum_address(UNISWAP["quoter_v2"]),
            abi=QUOTER_ABI
        )
        self.orders = self.load_orders()

    def load_orders(self):
        if ORDERS_FILE.exists():
            with open(ORDERS_FILE) as f:
                return json.load(f)
        return []

    def save_orders(self):
        with open(ORDERS_FILE, "w") as f:
            json.dump(self.orders, f, indent=2)

    def get_price(self, token_address, quote_token="USDC", amount=1.0, fee=3000):
        """Get current price of a token in USDC (or another quote token)."""
        if quote_token.upper() in TOKENS:
            quote_token = TOKENS[quote_token.upper()]
        if token_address.upper() in TOKENS:
            token_address = TOKENS[token_address.upper()]

        # Get decimals
        erc20_abi = [{"constant": True, "inputs": [], "name": "decimals",
                      "outputs": [{"name": "", "type": "uint8"}], "type": "function"}]

        token_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address), abi=erc20_abi)
        quote_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(quote_token), abi=erc20_abi)

        token_decimals = token_contract.functions.decimals().call()
        quote_decimals = quote_contract.functions.decimals().call()

        amount_raw = int(amount * (10 ** token_decimals))

        try:
            result = self.quoter.functions.quoteExactInputSingle({
                "tokenIn": Web3.to_checksum_address(token_address),
                "tokenOut": Web3.to_checksum_address(quote_token),
                "amountIn": amount_raw,
                "fee": fee,
                "sqrtPriceLimitX96": 0,
            }).call()
            price = result[0] / (10 ** quote_decimals)
            return price / amount
        except Exception as e:
            # Try different fee tiers
            for alt_fee in [500, 10000]:
                try:
                    result = self.quoter.functions.quoteExactInputSingle({
                        "tokenIn": Web3.to_checksum_address(token_address),
                        "tokenOut": Web3.to_checksum_address(quote_token),
                        "amountIn": amount_raw,
                        "fee": alt_fee,
                        "sqrtPriceLimitX96": 0,
                    }).call()
                    price = result[0] / (10 ** quote_decimals)
                    return price / amount
                except:
                    continue
            return None

    def add_stop_loss(self, token, entry_price, stop_pct, amount):
        """Add a stop-loss order."""
        stop_price = entry_price * (1 - stop_pct / 100)
        order = {
            "type": "stop_loss",
            "token": token,
            "entry_price": entry_price,
            "trigger_price": stop_price,
            "stop_pct": stop_pct,
            "amount": amount,
            "created_at": time.time(),
            "status": "active"
        }
        self.orders.append(order)
        self.save_orders()
        print(f"🛡️ Stop-loss set: sell {amount} {token} if price drops below ${stop_price:.6f} ({stop_pct}% from ${entry_price:.6f})")

    def add_take_profit(self, token, entry_price, profit_pct, amount):
        """Add a take-profit order."""
        tp_price = entry_price * (1 + profit_pct / 100)
        order = {
            "type": "take_profit",
            "token": token,
            "entry_price": entry_price,
            "trigger_price": tp_price,
            "profit_pct": profit_pct,
            "amount": amount,
            "created_at": time.time(),
            "status": "active"
        }
        self.orders.append(order)
        self.save_orders()
        print(f"🎯 Take-profit set: sell {amount} {token} if price rises above ${tp_price:.6f} ({profit_pct}% from ${entry_price:.6f})")

    def check_orders(self):
        """Check all active orders against current prices."""
        triggered = []

        for order in self.orders:
            if order["status"] != "active":
                continue

            token = order["token"]
            current_price = self.get_price(token)

            if current_price is None:
                print(f"⚠️ Could not get price for {token}")
                continue

            if order["type"] == "stop_loss" and current_price <= order["trigger_price"]:
                print(f"🚨 STOP-LOSS TRIGGERED: {token} at ${current_price:.6f} (trigger: ${order['trigger_price']:.6f})")
                order["status"] = "triggered"
                order["triggered_price"] = current_price
                order["triggered_at"] = time.time()
                triggered.append(order)

            elif order["type"] == "take_profit" and current_price >= order["trigger_price"]:
                print(f"🎉 TAKE-PROFIT TRIGGERED: {token} at ${current_price:.6f} (trigger: ${order['trigger_price']:.6f})")
                order["status"] = "triggered"
                order["triggered_price"] = current_price
                order["triggered_at"] = time.time()
                triggered.append(order)
            else:
                pct_from_trigger = ((current_price - order["trigger_price"]) / order["trigger_price"]) * 100
                direction = "above" if pct_from_trigger > 0 else "below"
                print(f"   {order['type'].upper()} {token}: ${current_price:.6f} ({abs(pct_from_trigger):.1f}% {direction} trigger)")

        self.save_orders()
        return triggered

    def list_orders(self):
        """List all active orders."""
        active = [o for o in self.orders if o["status"] == "active"]
        if not active:
            print("No active orders.")
            return

        print(f"\n📋 Active Orders ({len(active)}):")
        for i, order in enumerate(active):
            print(f"  {i+1}. {order['type'].upper()}: {order['amount']} {order['token']} @ ${order['trigger_price']:.6f}")


if __name__ == "__main__":
    monitor = PriceMonitor()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "price" and len(sys.argv) > 2:
            token = sys.argv[2]
            price = monitor.get_price(token)
            if price:
                print(f"{token}: ${price:.6f}")

        elif cmd == "check":
            triggered = monitor.check_orders()
            if triggered:
                print(f"\n⚡ {len(triggered)} order(s) triggered! Execute swaps manually or via swap.py")

        elif cmd == "list":
            monitor.list_orders()

        elif cmd == "stop" and len(sys.argv) > 5:
            monitor.add_stop_loss(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

        elif cmd == "tp" and len(sys.argv) > 5:
            monitor.add_take_profit(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

        else:
            print("Usage:")
            print("  python3 price_monitor.py price WETH")
            print("  python3 price_monitor.py stop WETH 2000.0 8.0 0.1")
            print("  python3 price_monitor.py tp WETH 2000.0 5.0 0.1")
            print("  python3 price_monitor.py check")
            print("  python3 price_monitor.py list")
    else:
        monitor.check_orders()
