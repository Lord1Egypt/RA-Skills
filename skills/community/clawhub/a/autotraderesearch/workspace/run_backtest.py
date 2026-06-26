"""Thin backtesting.py evaluator for the open AutoTradeResearch workspace."""

from __future__ import annotations

import ast
import importlib.util
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


WORKSPACE_DIR = Path(__file__).resolve().parent
AGENT_DIR = WORKSPACE_DIR / "agent"
DATA_PATH = WORKSPACE_DIR / "data" / "prices.csv"
RESULTS_PATH = WORKSPACE_DIR / "results" / "results.tsv"
LEADERBOARD_PATH = WORKSPACE_DIR / "reports" / "leaderboard.md"
PROGRAM_PATH = AGENT_DIR / "program.md"
STRATEGY_PATH = AGENT_DIR / "strategy.py"

DEFAULT_SYMBOL = "SPY"
DEFAULT_START = "2018-01-01"

PROGRAM_METADATA_KEYS = ("map_index", "exploration_mode", "strategy_family", "notes")
RESULT_COLUMNS = [
    "timestamp",
    "data_source",
    "symbol",
    "period_start",
    "period_end",
    "map_index",
    "exploration_mode",
    "strategy_family",
    "notes",
    "return_pct",
    "buy_hold_return_pct",
    "sharpe_ratio",
    "sortino_ratio",
    "calmar_ratio",
    "max_drawdown_pct",
    "win_rate_pct",
    "profit_factor",
    "exposure_time_pct",
    "trades",
    "duration_days",
]


def _column_levels(column: Any) -> tuple[str, ...]:
    if isinstance(column, tuple):
        values = column
    elif isinstance(column, str):
        text = column.strip()
        if text.startswith("(") and text.endswith(")"):
            try:
                parsed = ast.literal_eval(text)
            except (SyntaxError, ValueError):
                parsed = None
            if isinstance(parsed, tuple):
                values = parsed
            else:
                values = (text,)
        else:
            values = (text,)
    else:
        values = (column,)

    levels = [str(value).strip() for value in values if str(value).strip()]
    return tuple(levels)


def _canonical_column_name(column: Any) -> str | None:
    levels = _column_levels(column)
    if not levels:
        return None

    normalized = " ".join(levels[0].replace("_", " ").split()).lower()
    alias_map = {
        "date": "Date",
        "datetime": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "adj close": "Adj Close",
        "adjclose": "Adj Close",
        "volume": "Volume",
    }
    return alias_map.get(normalized)


def parse_frontmatter(path: Path) -> dict[str, str]:
    defaults = {key: "not set yet" for key in PROGRAM_METADATA_KEYS}
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        return defaults

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return defaults

    metadata_block = parts[1]
    for raw_line in metadata_block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in defaults:
            continue
        cleaned = value.strip().strip("'").strip('"')
        defaults[key] = cleaned or "not set yet"

    return defaults


def normalize_price_data(raw: pd.DataFrame) -> pd.DataFrame:
    data = raw.copy()
    recognized_columns: dict[str, Any] = {}

    for column in data.columns:
        canonical = _canonical_column_name(column)
        if canonical is None or canonical in recognized_columns:
            continue
        recognized_columns[canonical] = column

    date_column = recognized_columns.get("Date")
    if date_column is not None:
        data[date_column] = pd.to_datetime(data[date_column], utc=False)
        data = data.set_index(date_column)
    elif not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index, utc=False)

    data.index.name = "Date"
    data = data.sort_index()

    close_column = recognized_columns.get("Close") or recognized_columns.get("Adj Close")
    if close_column is None:
        numeric_columns = []
        for column in data.columns:
            converted = pd.to_numeric(data[column], errors="coerce")
            if converted.notna().any():
                numeric_columns.append(column)
        if len(numeric_columns) == 1:
            close_column = numeric_columns[0]
        else:
            raise SystemExit(
                "workspace/data/prices.csv is not compatible with backtesting.py: expected OHLCV columns or a single price column."
            )

    close = pd.to_numeric(data[close_column], errors="coerce")
    normalized = pd.DataFrame(index=data.index)
    normalized["Close"] = close
    for target in ("Open", "High", "Low"):
        source = recognized_columns.get(target)
        values = close if source is None else pd.to_numeric(data[source], errors="coerce")
        normalized[target] = values.fillna(close)

    volume_source = recognized_columns.get("Volume")
    volume = pd.Series(0, index=data.index) if volume_source is None else data[volume_source]
    normalized["Volume"] = pd.to_numeric(volume, errors="coerce").fillna(0)

    normalized = normalized[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Open", "High", "Low", "Close"])
    return normalized


def download_default_data() -> pd.DataFrame:
    try:
        import yfinance as yf
    except ImportError as exc:
        raise SystemExit(
            "workspace/data/prices.csv is missing and yfinance is not installed, so the evaluator cannot fetch default data."
        ) from exc

    try:
        downloaded = yf.download(DEFAULT_SYMBOL, start=DEFAULT_START, auto_adjust=True, progress=False)
    except Exception as exc:  # pragma: no cover - network/runtime dependent
        raise SystemExit(f"Failed to download default data for {DEFAULT_SYMBOL}: {exc}") from exc

    if downloaded.empty:
        raise SystemExit(f"Downloaded dataset for {DEFAULT_SYMBOL} is empty.")

    normalized = normalize_price_data(downloaded.reset_index())
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(DATA_PATH)
    return normalized


def load_backtest_data() -> tuple[pd.DataFrame, str, str]:
    if DATA_PATH.exists():
        local = pd.read_csv(DATA_PATH)
        return normalize_price_data(local), "csv", DATA_PATH.name

    return download_default_data(), "yfinance", DEFAULT_SYMBOL


def load_strategy_class():
    spec = importlib.util.spec_from_file_location("autotraderesearch_agent_strategy", STRATEGY_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load strategy module from {STRATEGY_PATH}.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    strategy_class = getattr(module, "AutoTradeStrategy", None)
    if strategy_class is None:
        raise SystemExit("agent/strategy.py must define AutoTradeStrategy.")

    return strategy_class


def safe_float(value: Any) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return float(value)


def build_result_row(stats: pd.Series, metadata: dict[str, str], data_source: str, symbol: str) -> dict[str, Any]:
    start = pd.Timestamp(stats["Start"])
    end = pd.Timestamp(stats["End"])

    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "data_source": data_source,
        "symbol": symbol,
        "period_start": start.date().isoformat(),
        "period_end": end.date().isoformat(),
        "map_index": metadata["map_index"],
        "exploration_mode": metadata["exploration_mode"],
        "strategy_family": metadata["strategy_family"],
        "notes": metadata["notes"],
        "return_pct": safe_float(stats["Return [%]"]),
        "buy_hold_return_pct": safe_float(stats["Buy & Hold Return [%]"]),
        "sharpe_ratio": safe_float(stats["Sharpe Ratio"]),
        "sortino_ratio": safe_float(stats["Sortino Ratio"]),
        "calmar_ratio": safe_float(stats["Calmar Ratio"]),
        "max_drawdown_pct": safe_float(stats["Max. Drawdown [%]"]),
        "win_rate_pct": safe_float(stats["Win Rate [%]"]),
        "profit_factor": safe_float(stats["Profit Factor"]),
        "exposure_time_pct": safe_float(stats["Exposure Time [%]"]),
        "trades": int(round(safe_float(stats["# Trades"]))),
        "duration_days": int((end - start).days),
    }


def format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"

    columns = list(frame.columns)
    rows = [[format_value(value) for value in row] for row in frame.to_numpy()]
    widths = []
    for index, column in enumerate(columns):
        max_cell = max(len(row[index]) for row in rows) if rows else 0
        widths.append(max(len(column), max_cell))

    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    divider = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = [
        "| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(columns))) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def select_columns(frame: pd.DataFrame) -> pd.DataFrame:
    wanted = [
        "timestamp",
        "map_index",
        "exploration_mode",
        "strategy_family",
        "symbol",
        "return_pct",
        "sharpe_ratio",
        "calmar_ratio",
        "max_drawdown_pct",
        "trades",
        "notes",
    ]
    return frame[[column for column in wanted if column in frame.columns]]


def write_results(row: dict[str, Any]) -> pd.DataFrame:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if RESULTS_PATH.exists():
        existing = pd.read_csv(RESULTS_PATH, sep="\t")
    else:
        existing = pd.DataFrame(columns=RESULT_COLUMNS)

    updated = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    updated = updated.reindex(columns=RESULT_COLUMNS)
    updated.to_csv(RESULTS_PATH, sep="\t", index=False)
    return updated


def write_leaderboard(results: pd.DataFrame) -> None:
    LEADERBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)

    table_columns = select_columns(results)

    best_sharpe = table_columns.sort_values(["sharpe_ratio", "return_pct"], ascending=[False, False]).head(10)

    acceptable_drawdown = table_columns[table_columns["max_drawdown_pct"] >= -20.0]
    if acceptable_drawdown.empty:
        acceptable_drawdown = table_columns
    best_return_acceptable_dd = acceptable_drawdown.sort_values(
        ["return_pct", "sharpe_ratio"], ascending=[False, False]
    ).head(10)

    low_drawdown_positive = table_columns[table_columns["return_pct"] > 0]
    low_drawdown_positive = low_drawdown_positive.sort_values(
        ["max_drawdown_pct", "return_pct"], ascending=[False, False]
    ).head(10)

    best_calmar = table_columns.sort_values(["calmar_ratio", "return_pct"], ascending=[False, False]).head(10)

    low_trade_candidates = table_columns.sort_values(["trades", "return_pct"], ascending=[True, False]).head(10)

    recent_experiments = table_columns.sort_values("timestamp", ascending=False).head(10)

    main_board = table_columns.sort_values(
        ["sharpe_ratio", "return_pct", "max_drawdown_pct"], ascending=[False, False, False]
    ).head(20)

    lines = [
        "# AutoTradeResearch Leaderboard",
        "",
        "_Generated by `workspace/run_backtest.py`. Coding agents may read this file but should not edit it._",
        "",
        "## Main leaderboard",
        "",
        markdown_table(main_board),
        "",
        "## Best Sharpe",
        "",
        markdown_table(best_sharpe),
        "",
        "## Best return with acceptable drawdown",
        "",
        markdown_table(best_return_acceptable_dd),
        "",
        "## Lowest drawdown with positive return",
        "",
        markdown_table(low_drawdown_positive),
        "",
        "## Best Calmar",
        "",
        markdown_table(best_calmar),
        "",
        "## Low-trade-count candidates",
        "",
        markdown_table(low_trade_candidates),
        "",
        "## Recent experiments",
        "",
        markdown_table(recent_experiments),
        "",
    ]

    LEADERBOARD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    try:
        from backtesting import Backtest
    except ImportError as exc:
        raise SystemExit("backtesting.py is not installed, so the evaluator cannot run.") from exc

    metadata = parse_frontmatter(PROGRAM_PATH)
    data, data_source, symbol = load_backtest_data()
    strategy_class = load_strategy_class()

    backtest = Backtest(data, strategy_class, cash=10_000, commission=0.001, exclusive_orders=True, finalize_trades=True)
    stats = backtest.run()

    row = build_result_row(stats, metadata, data_source, symbol)
    results = write_results(row)
    write_leaderboard(results)

    print("AutoTradeResearch backtest")
    print(f"Strategy: {strategy_class.__name__}")
    print(f"Data: {symbol} ({data_source})")
    print(f"Period: {row['period_start']} -> {row['period_end']}")
    print(f"Return: {row['return_pct']:.2f}%")
    print(f"Sharpe: {row['sharpe_ratio']:.3f}")
    print(f"Max drawdown: {row['max_drawdown_pct']:.2f}%")
    print(f"Trades: {row['trades']}")
    print(f"Results: {RESULTS_PATH}")
    print(f"Leaderboard: {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()
