#!/usr/bin/env python3
"""Fetch live DRT signals (premium — x402 pay-per-call).

⚠️ PAID API call: each run costs money (x402, USDC on Ethereum) and sends
your API key to the API. Run only when you consciously want live signals.
"""
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
from x402_client import call

print("⚠️ Executing PAID x402 call (/v1/signals) — charged to your key.")
symbol = sys.argv[1] if len(sys.argv) > 1 else None
data = call("/v1/signals", {"symbol": symbol, "limit": 10} if symbol else {"limit": 10})
print(json.dumps(data, indent=2, ensure_ascii=False))
