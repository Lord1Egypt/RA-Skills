"""analyst_revision.py — 分析师估值修正动量追踪

策略：每日对比 analyst_consensus.json 与历史数据，计算修正方向和速度。
- 连续上调 target_mean + 股价未充分反映 = 正面预期差信号
- 连续下调 = 预警信号
- 评级变化（buy/sell 比例变化）= 重要信号

输出: analyst_revision.json
依赖: analyst_consensus.py 的输出 analyst_consensus.json (同日已生成)
"""
import os, json, sys, shutil
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult, DATA_DIR

# Store historical snapshots for comparison
HISTORY_DIR = os.path.join(os.path.dirname(__file__), "..", "state", "analyst_history")


class Fetcher(BaseFetcher):
    name = "analyst_revision"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def fetch_raw(self):
        """Read today's analyst_consensus.json (already produced by analyst_consensus)."""
        today_consensus = os.path.join(self.daily_dir, "analyst_consensus.json")
        if not os.path.exists(today_consensus):
            return None
        with open(today_consensus) as f:
            return f.read()

    def parse(self, raw):
        """Compare today vs prior snapshots to compute revision scores."""
        today_data = json.loads(raw)
        if not isinstance(today_data, list):
            raise ValueError(f"Expected list, got {type(today_data).__name__}")

        today_by_sym = {r["symbol"]: r for r in today_data}

        # Load historical snapshots (up to 30 days back)
        history = self._load_history(lookback_days=30)

        records = []
        for symbol, current in today_by_sym.items():
            revision = self._compute_revision(symbol, current, history)
            if revision:
                records.append(revision)

        # Sort by absolute revision score (strongest signals first)
        records.sort(key=lambda r: abs(r.get("revision_score", 0)), reverse=True)

        # Archive today's data for future comparisons
        self._archive_today(today_data)

        return records

    def _load_history(self, lookback_days=30):
        """Load archived analyst snapshots from past N days."""
        history = {}  # date_str -> {symbol: record}
        today_dt = date.fromisoformat(self.today)

        for i in range(1, lookback_days + 1):
            d = (today_dt - timedelta(days=i)).isoformat()
            path = os.path.join(HISTORY_DIR, f"{d}.json")
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        data = json.load(f)
                    history[d] = {r["symbol"]: r for r in data}
                except Exception:
                    continue
        return history

    def _archive_today(self, today_data):
        """Save today's snapshot for future revision tracking."""
        path = os.path.join(HISTORY_DIR, f"{self.today}.json")
        with open(path, "w") as f:
            json.dump(today_data, f, ensure_ascii=False)

        # Cleanup: keep only last 60 days
        self._cleanup_history(keep_days=60)

    def _cleanup_history(self, keep_days=60):
        """Remove snapshots older than keep_days."""
        cutoff = (date.fromisoformat(self.today) - timedelta(days=keep_days)).isoformat()
        for fname in os.listdir(HISTORY_DIR):
            if fname.endswith(".json") and fname[:10] < cutoff:
                try:
                    os.remove(os.path.join(HISTORY_DIR, fname))
                except OSError:
                    pass

    def _compute_revision(self, symbol, current, history):
        """Compute revision metrics for a single symbol."""
        target_mean = current.get("target_mean")
        price = current.get("price_current")
        buy = current.get("buy", 0)
        hold = current.get("hold", 0)
        sell = current.get("sell", 0)

        # Find most recent prior data point
        prior = None
        prior_date = None
        sorted_dates = sorted(history.keys(), reverse=True)
        for d in sorted_dates:
            if symbol in history[d]:
                prior = history[d][symbol]
                prior_date = d
                break

        # Find data from ~7 days ago for weekly comparison
        week_ago = None
        week_ago_date = None
        today_dt = date.fromisoformat(self.today)
        for d in sorted_dates:
            d_dt = date.fromisoformat(d)
            if (today_dt - d_dt).days >= 5:
                if symbol in history[d]:
                    week_ago = history[d][symbol]
                    week_ago_date = d
                break

        # Build revision record
        record = {
            "symbol": symbol,
            "target_mean": target_mean,
            "price_current": price,
            "buy": buy,
            "hold": hold,
            "sell": sell,
        }

        # Compute upside (target vs current price)
        if target_mean and price and price > 0:
            record["upside_pct"] = round((target_mean - price) / price * 100, 1)
        else:
            record["upside_pct"] = None

        # Compute revision vs prior
        if prior:
            prev_target = prior.get("target_mean")
            prev_buy = prior.get("buy", 0)
            prev_sell = prior.get("sell", 0)

            if prev_target and target_mean and prev_target > 0:
                record["target_change_pct"] = round(
                    (target_mean - prev_target) / prev_target * 100, 2
                )
            else:
                record["target_change_pct"] = 0

            record["buy_change"] = buy - prev_buy
            record["sell_change"] = sell - (prior.get("sell", 0))
            record["prior_date"] = prior_date
        else:
            record["target_change_pct"] = 0
            record["buy_change"] = 0
            record["sell_change"] = 0
            record["prior_date"] = None

        # Compute weekly revision (more meaningful for detection)
        if week_ago:
            prev_target_w = week_ago.get("target_mean")
            if prev_target_w and target_mean and prev_target_w > 0:
                record["target_change_7d_pct"] = round(
                    (target_mean - prev_target_w) / prev_target_w * 100, 2
                )
            else:
                record["target_change_7d_pct"] = 0
            record["buy_change_7d"] = buy - week_ago.get("buy", 0)
            record["sell_change_7d"] = sell - week_ago.get("sell", 0)
        else:
            record["target_change_7d_pct"] = 0
            record["buy_change_7d"] = 0
            record["sell_change_7d"] = 0

        # Composite revision score (-100 to +100)
        # Factors: target price change, rating shifts, upside gap
        score = 0

        # Target price revision component (weight: 40%)
        target_chg = record.get("target_change_pct", 0) or 0
        score += min(max(target_chg * 10, -40), 40)

        # Rating shift component (weight: 30%)
        buy_chg = record.get("buy_change", 0) or 0
        sell_chg = record.get("sell_change", 0) or 0
        rating_signal = buy_chg * 5 - sell_chg * 10
        score += min(max(rating_signal, -30), 30)

        # Upside gap component (weight: 30%) — large upside = potential undervaluation
        upside = record.get("upside_pct") or 0
        if upside > 0:
            score += min(upside * 0.6, 30)
        else:
            score += max(upside * 0.6, -30)

        record["revision_score"] = round(score, 1)

        # Classification
        if score >= 20:
            record["signal"] = "positive_revision"
        elif score <= -20:
            record["signal"] = "negative_revision"
        else:
            record["signal"] = "neutral"

        return record

    def validate(self, records):
        if len(records) > 500:
            raise ValueError(f"Abnormal count: {len(records)}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
