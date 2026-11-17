"""Price tracker for model API pricing."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Default cached prices (yuan per 1M tokens) — fallback when scraping fails
DEFAULT_PRICES: Dict[str, Dict[str, float]] = {
    "deepseek": {"input": 1.0, "output": 2.0},
    "tongyi": {"input": 2.0, "output": 6.0},
    "zhipu": {"input": 5.0, "output": 15.0},
    "kimi": {"input": 12.0, "output": 12.0},
    "hunyuan": {"input": 10.0, "output": 10.0},
    "doubao": {"input": 3.0, "output": 9.0},
    "minimax": {"input": 0.5, "output": 1.0},
    "lingyi": {"input": 2.0, "output": 2.0},
    "baichuan": {"input": 0.5, "output": 0.5},
    "stepfun": {"input": 5.0, "output": 15.0},
}

# Price scrape URLs (simplified — actual implementation may vary)
PRICE_URLS: Dict[str, str] = {
    "deepseek": "https://api.deepseek.com/pricing",
    "tongyi": "https://dashscope.aliyuncs.com/pricing",
    "zhipu": "https://open.bigmodel.cn/pricing",
    "kimi": "https://api.moonshot.cn/pricing",
    "hunyuan": "https://cloud.tencent.com/document/product/1759/97788",
    "doubao": "https://www.volcengine.com/product/doubao",
    "minimax": "https://api.minimax.chat/pricing",
    "lingyi": "https://api.lingyi.cn/pricing",
    "baichuan": "https://api.baichuan-ai.com/pricing",
    "stepfun": "https://api.stepfun.com/pricing",
}


class PriceTracker:
    """Tracks model API pricing with fallback to cached prices."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".cn-model-gateway" / "price.db")
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            # Enable WAL mode for concurrent multi-process access (v1.4.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    provider TEXT,
                    input_price REAL,
                    output_price REAL,
                    source TEXT DEFAULT 'cache'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS price_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    provider TEXT,
                    old_input REAL,
                    new_input REAL,
                    old_output REAL,
                    new_output REAL,
                    notified INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def fetch_prices(self, provider: str) -> Optional[Dict[str, float]]:
        """Fetch latest prices for a provider.

        Args:
            provider: Provider name

        Returns:
            Dict with 'input' and 'output' prices, or None if fetch fails
        """
        url = PRICE_URLS.get(provider)
        if not url:
            return None

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode("utf-8", errors="replace")
                # Simple heuristic parsing — may need adjustment per provider
                prices = self._parse_price_content(content)
                if prices:
                    self._save_price(provider, prices, source="scrape")
                    return prices
        except (urllib.error.URLError, OSError):
            pass

        # Fallback to cached prices
        cached = DEFAULT_PRICES.get(provider)
        if cached:
            self._save_price(provider, cached, source="cache")
            return cached
        return None

    def fetch_all_prices(self) -> Dict[str, Dict[str, float]]:
        """Fetch prices for all providers.

        Returns:
            Dict mapping provider name to price dict
        """
        results = {}
        for provider in DEFAULT_PRICES:
            prices = self.fetch_prices(provider)
            if prices:
                results[provider] = prices
        return results

    def _parse_price_content(self, content: str) -> Optional[Dict[str, float]]:
        """Parse price information from webpage content.

        This is a simplified parser. Real implementation would need
        provider-specific parsing logic.
        """
        # Look for patterns like "¥0.001" or "$0.001" per 1K/1M tokens
        input_match = re.search(r'input[:\s]*[¥$]\s*(\d+\.?\d*)', content, re.IGNORECASE)
        output_match = re.search(r'output[:\s]*[¥$]\s*(\d+\.?\d*)', content, re.IGNORECASE)

        if input_match and output_match:
            return {
                "input": float(input_match.group(1)),
                "output": float(output_match.group(1)),
            }
        return None

    def _save_price(self, provider: str, prices: Dict[str, float], source: str = "cache") -> None:
        """Save price to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO price_history (timestamp, provider, input_price, output_price, source) "
                "VALUES (?, ?, ?, ?, ?)",
                (time.time(), provider, prices.get("input", 0), prices.get("output", 0), source),
            )
            conn.commit()

    def detect_changes(self, provider: str, new_prices: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """Detect price changes for a provider.

        Args:
            provider: Provider name
            new_prices: New price dict

        Returns:
            Change info dict if changed, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM price_history WHERE provider = ? ORDER BY timestamp DESC LIMIT 1",
                (provider,)
            ).fetchone()

        if not row:
            return None

        old_input = row["input_price"]
        old_output = row["output_price"]

        if old_input != new_prices.get("input") or old_output != new_prices.get("output"):
            change = {
                "provider": provider,
                "old_input": old_input,
                "new_input": new_prices.get("input"),
                "old_output": old_output,
                "new_output": new_prices.get("output"),
                "timestamp": time.time(),
            }
            # Save alert
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO price_alerts (timestamp, provider, old_input, new_input, old_output, new_output) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (time.time(), provider, old_input, new_prices.get("input"),
                     old_output, new_prices.get("output")),
                )
                conn.commit()
            return change
        return None

    def get_current_prices(self) -> Dict[str, Dict[str, float]]:
        """Get current prices for all providers (from cache).

        Returns:
            Dict mapping provider name to price dict
        """
        return DEFAULT_PRICES.copy()

    def get_price_history(self, provider: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Get price history for a provider.

        Args:
            provider: Provider name
            limit: Maximum number of records

        Returns:
            List of price history records
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM price_history WHERE provider = ? ORDER BY timestamp DESC LIMIT ?",
                (provider, limit)
            ).fetchall()
        return [dict(r) for r in rows]

    def predict_cost(self, monthly_usage: Dict[str, int]) -> Dict[str, Any]:
        """Predict monthly cost based on usage.

        Args:
            monthly_usage: Dict mapping provider to monthly token count (input + output combined)

        Returns:
            Cost prediction dict
        """
        prices = self.get_current_prices()
        predictions = {}
        total_cost = 0.0

        for provider, tokens in monthly_usage.items():
            price = prices.get(provider, {"input": 0, "output": 0})
            # Assume 60% input, 40% output split
            input_tokens = int(tokens * 0.6)
            output_tokens = int(tokens * 0.4)
            cost = (input_tokens / 1_000_000 * price["input"] +
                    output_tokens / 1_000_000 * price["output"])
            predictions[provider] = {
                "tokens": tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost": round(cost, 2),
            }
            total_cost += cost

        return {
            "predictions": predictions,
            "total_estimated_cost": round(total_cost, 2),
            "note": "基于当前价格估算，实际费用可能因价格调整而变化",
        }

    def generate_price_table(self) -> str:
        """Generate a text-based price comparison table.

        Returns:
            Formatted price table string
        """
        prices = self.get_current_prices()
        lines = ["💰 当前模型价格（元 / 1M tokens）\n"]
        lines.append(f"{'Provider':<15}{'Input':<12}{'Output':<12}{'备注'}")
        lines.append("-" * 50)

        for provider, price in prices.items():
            note = ""
            if price["input"] < 1:
                note = "🟢 低价"
            elif price["input"] < 5:
                note = "🟡 中价"
            else:
                note = "🔴 高价"
            lines.append(f"{provider:<15}{price['input']:<12}{price['output']:<12}{note}")

        lines.append("\n数据来源: 各厂商官网（缓存）| 建议以官网最新定价为准")
        return "\n".join(lines)

    def generate_trend_chart(self, provider: str) -> str:
        """Generate ASCII price trend chart.

        Args:
            provider: Provider name

        Returns:
            ASCII trend chart string
        """
        history = self.get_price_history(provider, limit=10)
        if not history:
            return f"暂无 {provider} 的价格历史数据"

        lines = [f"📈 {provider} 价格趋势\n"]
        lines.append(f"{'日期':<20}{'Input':<12}{'Output':<12}{'来源'}")
        lines.append("-" * 55)

        for row in reversed(history):
            date = time.strftime("%Y-%m-%d", time.localtime(row["timestamp"]))
            lines.append(f"{date:<20}{row['input_price']:<12}{row['output_price']:<12}{row['source']}")

        return "\n".join(lines)
