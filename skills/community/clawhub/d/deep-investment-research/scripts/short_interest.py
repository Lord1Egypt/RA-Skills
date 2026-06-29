"""short_interest.py — 港股沽空持仓（SFC 每周聚合数据）

数据源: SFC Aggregated Reportable Short Positions CSV
URL: https://www.sfc.hk/.../Latest-CSV (每周四/五更新)
输出: hk_short_daily.json (保持与 convergence scanner 的文件名约定一致)
价值: 外资/机构对港股的方向性判断（做空=看跌信号）
"""
import os, json, sys, csv, io
from datetime import date, datetime
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult, DATA_DIR

SFC_CSV_URL = "https://www.sfc.hk/en/Regulatory-functions/Market/Short-position-reporting/Aggregated-reportable-short-positions-of-specified-shares/Latest-CSV"
HISTORY_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "short_interest_prev.json")


class Fetcher(BaseFetcher):
    name = "short_interest"  # Output filename aligns with convergence scanner expectation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.watchlist = self._get_hk_symbols()

    def _get_hk_symbols(self):
        """Get HK stock codes from watchlist (numeric, without leading zeros)."""
        try:
            import yaml
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            with open(wl_path) as f:
                data = yaml.safe_load(f) or {}
            codes = set()
            for section in ["positions", "focus"]:
                for item in data.get(section, []):
                    sym = item["symbol"]
                    if sym.endswith(".HK"):
                        code = sym.split(".")[0].lstrip("0")
                        codes.add(int(code))
            return codes if codes else {700, 1810, 981}
        except Exception:
            return {700, 1810, 981}

    def fetch_raw(self):
        """Download SFC latest CSV."""
        resp = requests.get(SFC_CSV_URL, timeout=30, allow_redirects=True,
                           headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return None
        text = resp.text
        if not text or "Stock Code" not in text:
            return None
        return text

    def parse(self, raw):
        """Parse CSV into records for watchlist symbols."""
        # Load previous data for week-over-week comparison
        prev_data = {}
        try:
            if os.path.exists(HISTORY_PATH):
                with open(HISTORY_PATH) as f:
                    prev_data = {r["symbol"]: r for r in json.load(f)}
        except Exception:
            pass

        records = []
        reader = csv.DictReader(io.StringIO(raw))

        for row in reader:
            try:
                code = int(row.get("Stock Code", 0))
            except (ValueError, TypeError):
                continue

            if code not in self.watchlist:
                continue

            symbol = f"{code:04d}.HK"
            shares = int(row.get("Aggregated Reportable Short Positions (Shares)", 0) or 0)
            value_hkd = int(row.get("Aggregated Reportable Short Positions (HK$)", 0) or 0)
            report_date = row.get("Date", "")

            # Convert date format: DD/MM/YYYY → YYYY-MM-DD
            if "/" in report_date:
                parts = report_date.split("/")
                if len(parts) == 3:
                    report_date = f"{parts[2]}-{parts[1]}-{parts[0]}"

            # Week-over-week change
            prev = prev_data.get(symbol, {})
            prev_shares = prev.get("short_shares", 0)
            wow_change_pct = None
            if prev_shares > 0:
                wow_change_pct = round((shares - prev_shares) / prev_shares * 100, 2)

            records.append({
                "symbol": symbol,
                "stock_name": row.get("Stock Name", "").strip(),
                "short_shares": shares,
                "short_value_hkd": value_hkd,
                "report_date": report_date,
                "wow_change_pct": wow_change_pct,
                "prev_short_shares": prev_shares,
            })

        # Save current as history for next comparison
        if records:
            os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
            with open(HISTORY_PATH, "w") as f:
                json.dump(records, f, ensure_ascii=False)

        return records

    def validate(self, records):
        if not records:
            raise ValueError("No short interest records for watchlist")
        if len(records) > 200:
            raise ValueError(f"Abnormal count: {len(records)}")
        for r in records[:5]:
            if not r.get("symbol") or not r.get("short_shares"):
                raise ValueError(f"Invalid record: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
