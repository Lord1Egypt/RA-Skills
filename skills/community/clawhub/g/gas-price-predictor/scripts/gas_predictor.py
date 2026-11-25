#!/usr/bin/env python3
"""Base L2 Gas Price Predictor - Analyzes gas markets and predicts optimal timing.

Security notes (v1.0.1, v1.0.3):
- No credentials are hardcoded anywhere in this skill. The RPC endpoint
  comes from the BASE_RPC_URL environment variable or --rpc-url, and
  defaults to the public no-key endpoint https://mainnet.base.org.
- Only https:// RPC URLs are accepted, and URLs with embedded
  username/password credentials are rejected.
- RPC failures print a fixed message only ("RPC error: request failed").
  The raw requests exception is never printed: it includes the full
  request URL, and a keyed provider URL carries the key in its path.
  An invalid endpoint likewise prints a fixed message, never the URL.
- Read-only: makes JSON-RPC read calls only. Never signs, sends, or
  executes transactions, and never runs shell commands.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from statistics import mean
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

DEFAULT_RPC_URL = "https://mainnet.base.org"
MAX_HISTORY_BLOCKS = 200


def _validate_rpc_url(url: str) -> str:
    """Accept only https:// RPC URLs with no embedded userinfo credentials.

    The endpoint is operator-supplied (env var or flag), so this rejects
    plaintext http and credential-in-URL forms rather than trusting any
    string as a network destination.
    """
    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("RPC URL must be an https:// URL")
    if parsed.username or parsed.password:
        raise ValueError(
            "RPC URL must not contain embedded username/password credentials"
        )
    return url


class GasPredictor:
    def __init__(self, rpc_url: str = DEFAULT_RPC_URL):
        self.rpc_url = _validate_rpc_url(rpc_url)
        self.blocks: List[Dict] = []

    def _rpc_call(self, method: str, params: list) -> dict:
        """Make JSON-RPC call to Base node."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        try:
            resp = requests.post(self.rpc_url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, dict):
                return {}
            result = data.get("result", {})
            return result if isinstance(result, dict) else {}
        except Exception:
            # Fixed message only. requests exceptions include the full
            # request URL, and a keyed provider URL carries the key in
            # its path — printing the exception would leak it into
            # stderr / logs (v1.0.3 fix; same class as the MEV SDI-4).
            print("RPC error: request failed", file=sys.stderr)
            return {}

    @staticmethod
    def _parse_block(result: dict) -> Dict:
        """Parse an eth_getBlockByNumber result.

        Returns {} on malformed data instead of crashing on a bad hex
        value or unexpected type from the RPC node.
        """
        if not isinstance(result, dict):
            return {}
        try:
            return {
                "number": int(result.get("number", "0x0"), 16),
                "timestamp": int(result.get("timestamp", "0x0"), 16),
                "base_fee": int(result.get("baseFeePerGas", "0x0"), 16) / 1e9,
                "gas_used": int(result.get("gasUsed", "0x0"), 16),
                "gas_limit": int(result.get("gasLimit", "0x0"), 16),
                "tx_count": len(result.get("transactions", []) or []),
            }
        except (TypeError, ValueError):
            return {}

    def get_latest_block(self) -> Dict:
        """Get latest block with full transaction data."""
        return self._parse_block(
            self._rpc_call("eth_getBlockByNumber", ["latest", False])
        )

    def get_block_by_number(self, block_num: int) -> Dict:
        """Get specific block data."""
        hex_num = hex(block_num)
        return self._parse_block(
            self._rpc_call("eth_getBlockByNumber", [hex_num, False])
        )

    def fetch_history(self, blocks: int = 100) -> List[Dict]:
        """Fetch historical gas data (capped at MAX_HISTORY_BLOCKS)."""
        latest = self.get_latest_block()
        if not latest:
            return []

        self.blocks = [latest]
        latest_num = latest["number"]

        for i in range(1, min(blocks, MAX_HISTORY_BLOCKS)):
            block = self.get_block_by_number(latest_num - i)
            if block:
                self.blocks.append(block)

        return sorted(self.blocks, key=lambda x: x["number"])

    def analyze_patterns(self) -> Dict:
        """Window statistics over the fetched blocks.

        Previously this method was called by predict_optimal() and by
        the --analyze path but was never defined, so every run crashed
        with NameError. It now computes the stats inline from
        self.blocks: average/min/max base fee plus 20/50/200-block
        moving averages (None when fewer blocks than the window were
        fetched).
        """
        fees = [
            b["base_fee"]
            for b in self.blocks
            if isinstance(b.get("base_fee"), (int, float))
        ]
        if not fees:
            return {
                "block_count": 0,
                "avg_base_fee": 0.0,
                "min_base_fee": 0.0,
                "max_base_fee": 0.0,
                "ma_20_gwei": None,
                "ma_50_gwei": None,
                "ma_200_gwei": None,
            }

        def _ma(window: int) -> Optional[float]:
            if len(fees) < window:
                return None
            return round(mean(fees[-window:]), 6)

        return {
            "block_count": len(fees),
            "avg_base_fee": round(mean(fees), 6),
            "min_base_fee": round(min(fees), 6),
            "max_base_fee": round(max(fees), 6),
            "ma_20_gwei": _ma(20),
            "ma_50_gwei": _ma(50),
            "ma_200_gwei": _ma(200),
        }

    def predict_optimal(self) -> Dict:
        """Predict optimal gas price and timing."""
        if not self.blocks:
            return {
                "error": "No block data available - check RPC connection",
                "current_base_fee_gwei": 0.05,
                "recommended_priority_gwei": 0.001,
                "total_gas_price_gwei": 0.051,
                "congestion": "unknown",
                "wait_recommended": False,
                "estimated_cost_usd": 0.5,
                "confidence": 50,
                "avg_base_fee_gwei": 0.05,
                "ratio_to_avg": 1.0,
                "block_number": 0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        latest = self.blocks[-1]
        patterns = self.analyze_patterns()

        # Simple heuristic: if current is above 1.5x average, suggest waiting
        current = latest["base_fee"]
        avg = patterns.get("avg_base_fee", current)
        ratio = current / avg if avg > 0 else 1.0

        if ratio > 1.5:
            congestion = "high"
            wait_recommended = True
            confidence = min(95, int(ratio * 30))
        elif ratio > 1.2:
            congestion = "medium"
            wait_recommended = False
            confidence = 60
        else:
            congestion = "low"
            wait_recommended = False
            confidence = 85

        # Recommended priority fee (conservative)
        priority_fee = min(0.001, current * 0.05)

        # Estimate cost for standard transfer (21K gas)
        gas_units = 21000
        total_gas_gwei = current + priority_fee
        cost_eth = (gas_units * total_gas_gwei) / 1e9
        cost_usd = cost_eth * 3000  # Approx ETH price

        return {
            "current_base_fee_gwei": round(current, 6),
            "recommended_priority_gwei": round(priority_fee, 6),
            "total_gas_price_gwei": round(total_gas_gwei, 6),
            "congestion": congestion,
            "wait_recommended": wait_recommended,
            "estimated_cost_usd": round(cost_usd, 4),
            "confidence": confidence,
            "avg_base_fee_gwei": round(avg, 6),
            "ratio_to_avg": round(ratio, 2),
            "block_number": latest["number"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def monitor(self, threshold: float, interval: int = 30):
        """Continuous monitoring mode (polling; prints alerts to stdout)."""
        print(f"Monitoring Base gas prices. Alert threshold: {threshold} gwei", flush=True)
        try:
            while True:
                self.fetch_history(blocks=20)
                pred = self.predict_optimal()

                total = pred.get("total_gas_price_gwei", 999)
                if total < threshold:
                    print(f"\n🟢 ALERT: Gas dropped to {total:.4f} gwei!", flush=True)
                    print(json.dumps(pred, indent=2), flush=True)
                else:
                    print(f"Current: {total:.4f} gwei | Congestion: {pred.get('congestion')} | Confidence: {pred.get('confidence')}%", flush=True)

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Base L2 Gas Price Predictor")
    parser.add_argument(
        "--rpc-url",
        default=os.environ.get("BASE_RPC_URL", DEFAULT_RPC_URL),
        help="Base JSON-RPC endpoint (default: $BASE_RPC_URL or "
             "https://mainnet.base.org). Must be https://. For a keyed "
             "provider, put your full endpoint URL in BASE_RPC_URL.",
    )
    parser.add_argument("--quick", action="store_true", help="Quick current check")
    parser.add_argument("--analyze", action="store_true", help="Full historical analysis")
    parser.add_argument("--blocks", type=int, default=100, help="Number of blocks to analyze (capped at 200)")
    parser.add_argument("--monitor", action="store_true", help="Continuous monitoring")
    parser.add_argument("--threshold", type=float, default=0.1, help="Alert threshold in gwei")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    try:
        predictor = GasPredictor(args.rpc_url)
    except ValueError:
        # Fixed message only — the endpoint URL is never echoed, so a
        # key in its path cannot leak into stderr.
        print("Invalid RPC endpoint", file=sys.stderr)
        sys.exit(2)

    if args.monitor:
        predictor.monitor(args.threshold)
    elif args.analyze:
        predictor.fetch_history(args.blocks)
        pred = predictor.predict_optimal()
        patterns = predictor.analyze_patterns()

        output = {
            "prediction": pred,
            "patterns": patterns,
            "blocks_analyzed": len(predictor.blocks),
        }

        if args.json:
            print(json.dumps(output, indent=2))
        else:
            print(f"\n📊 Gas Analysis ({len(predictor.blocks)} blocks)")
            print(f"Current base fee: {pred['current_base_fee_gwei']:.4f} gwei")
            print(f"Average (last {len(predictor.blocks)}): {pred.get('avg_base_fee_gwei', 0.0):.4f} gwei")
            print(f"Min/Max: {patterns.get('min_base_fee', 0.0):.4f} / {patterns.get('max_base_fee', 0.0):.4f} gwei")
            if patterns.get("ma_20_gwei") is not None:
                print(f"MA-20: {patterns['ma_20_gwei']:.4f} gwei")
            if patterns.get("ma_50_gwei") is not None:
                print(f"MA-50: {patterns['ma_50_gwei']:.4f} gwei")
            print(f"Congestion: {pred['congestion'].upper()}")
            print(f"Wait recommended: {pred['wait_recommended']}")
            print(f"Confidence: {pred['confidence']}%")
            print(f"\nRecommended settings:")
            print(f"  maxFeePerGas: {pred['total_gas_price_gwei']:.4f} gwei")
            print(f"  maxPriorityFeePerGas: {pred['recommended_priority_gwei']:.4f} gwei")
            print(f"\nEstimated transfer cost: ${pred['estimated_cost_usd']:.4f}")
    else:
        # Quick check
        predictor.fetch_history(blocks=20)
        pred = predictor.predict_optimal()

        if args.json:
            print(json.dumps(pred, indent=2))
        else:
            print(f"\n⚡ Quick Gas Check (Block #{pred['block_number']})")
            print(f"Base fee: {pred['current_base_fee_gwei']:.4f} gwei")
            print(f"Total gas: {pred['total_gas_price_gwei']:.4f} gwei")
            print(f"Congestion: {pred['congestion'].upper()}")
            print(f"Confidence: {pred['confidence']}%")
            if pred['wait_recommended']:
                print("💡 Consider waiting for lower gas")

if __name__ == "__main__":
    main()
