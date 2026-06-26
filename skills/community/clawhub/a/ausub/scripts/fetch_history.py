import csv
import os
import re
from datetime import datetime

try:
    import tushare as ts
except ImportError:  # pragma: no cover
    ts = None


def get_tushare_client():
    token = os.getenv("TUSHARE_TOKEN")
    if not token:
        raise RuntimeError("Missing TUSHARE_TOKEN environment variable.")
    if ts is None:
        raise RuntimeError("tushare is not installed. Run `pip install tushare` first.")
    ts.set_token(token)
    return ts.pro_api()


def sanitize_symbol(symbol: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", symbol):
        raise RuntimeError("OPENCLAW_SYMBOL contains invalid characters.")
    return symbol


def ensure_data_dir() -> str:
    data_dir = os.path.join(os.path.dirname(__file__), "..", "references", "history")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def main() -> None:
    symbol = sanitize_symbol(os.getenv("OPENCLAW_SYMBOL", "518880.SH"))
    start_date = os.getenv("OPENCLAW_START_DATE", "20160101")
    end_date = os.getenv("OPENCLAW_END_DATE", datetime.now().strftime("%Y%m%d"))

    pro = get_tushare_client()
    df = pro.fund_daily(ts_code=symbol, start_date=start_date, end_date=end_date)
    if df is None or df.empty:
        df = pro.daily(ts_code=symbol, start_date=start_date, end_date=end_date)
    if df is None or df.empty:
        raise RuntimeError(f"No historical data returned for symbol {symbol}.")

    df = df.sort_values("trade_date")
    data_dir = ensure_data_dir()
    output_path = os.path.join(data_dir, f"{symbol.replace('.', '_')}.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["trade_date", "close"])
        for _, row in df.iterrows():
            writer.writerow([row["trade_date"], row["close"]])

    print(f"Saved historical data to: {output_path}")


if __name__ == "__main__":
    main()
