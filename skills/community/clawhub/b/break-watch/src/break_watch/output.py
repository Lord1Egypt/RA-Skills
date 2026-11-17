from __future__ import annotations

import csv
import html
import logging
from datetime import date, datetime
from pathlib import Path

from .config import OutputConfig
from .models import Signal, Stock


logger = logging.getLogger(__name__)


def ensure_output_dirs(config: OutputConfig) -> None:
    config.log_dir.mkdir(parents=True, exist_ok=True)
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.result_dir.mkdir(parents=True, exist_ok=True)


def setup_logging(config: OutputConfig, today: date | None = None) -> Path:
    ensure_output_dirs(config)
    today = today or date.today()
    log_path = config.log_dir / f"break_watch_{today:%Y%m%d}.log"

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for handler in list(root.handlers):
        root.removeHandler(handler)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    root.addHandler(file_handler)
    return log_path


class ResultWriter:
    def __init__(self, config: OutputConfig, today: date | None = None):
        ensure_output_dirs(config)
        self.config = config
        self.today = today or date.today()
        self.csv_path = config.result_dir / f"signals_{self.today:%Y%m%d}.sel"
        self.html_path = config.result_dir / f"signals_{self.today:%Y%m%d}.html"
        self.ths_path = config.result_dir / f"ths_codes_{self.today:%Y%m%d}.txt"
        self._rows: list[dict[str, str]] = self._load_existing_csv_rows()
        self._ths_codes: set[str] = self._load_existing_ths_codes()

    def emit(self, signals: list[Signal]) -> None:
        if not signals:
            return

        rows = [self._row(signal) for signal in signals]
        self._rows.extend(rows)

        if self.config.console_enabled:
            self._write_console(signals)
        if self.config.csv_enabled:
            self._append_csv(rows)
        if self.config.ths_txt_enabled:
            self._write_ths_txt(signals)
        if self.config.html_enabled:
            self._write_html()

        logger.info("Wrote %s signals.", len(signals))

    def _write_console(self, signals: list[Signal]) -> None:
        for signal in signals:
            interval_volume = _fmt_number(signal.interval_volume)
            spike_ratio = _fmt_ratio(signal.interval_spike_ratio)
            print(
                f"{signal.timestamp:%H:%M:%S} | "
                f"{signal.stock.code} | "
                f"{signal.stock.name or '-'} | "
                f"{signal.price:.2f} | "
                f"{signal.change_pct:.2f}% | "
                f"{signal.open:.2f} | "
                f"{_fmt_number(signal.current_volume)} | "
                f"{signal.volume_ratio:.2f} | "
                f"{interval_volume} | "
                f"{spike_ratio} | "
                f"{signal.server}",
                flush=True,
            )

    def _append_csv(self, rows: list[dict[str, str]]) -> None:
        exists = self.csv_path.exists()
        with self.csv_path.open("a", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            if not exists:
                writer.writeheader()
            writer.writerows(rows)

    def _write_html(self) -> None:
        body_rows = "\n".join(self._html_row(row) for row in self._rows)
        document = HTML_TEMPLATE.format(
            generated_at=html.escape(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            count=len(self._rows),
            rows=body_rows,
        )
        self.html_path.write_text(document, encoding="utf-8")

    def _write_ths_txt(self, signals: list[Signal]) -> None:
        changed = False
        for signal in signals:
            code = self._format_ths_code(signal.stock)
            if code not in self._ths_codes:
                self._ths_codes.add(code)
                changed = True
        if changed:
            lines = sorted(self._ths_codes)
            self.ths_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _load_existing_csv_rows(self) -> list[dict[str, str]]:
        if not self.csv_path.exists():
            return []
        with self.csv_path.open("r", newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))

    def _load_existing_ths_codes(self) -> set[str]:
        if not self.ths_path.exists():
            return set()
        return {
            line.strip()
            for line in self.ths_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def _format_ths_code(self, stock: Stock) -> str:
        if self.config.ths_txt_code_format == "prefix":
            return f"{stock.market_prefix}{stock.code}"
        return stock.code

    @staticmethod
    def _row(signal: Signal) -> dict[str, str]:
        return {
            "datetime": signal.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "market": str(signal.stock.market),
            "code": signal.stock.code,
            "name": signal.stock.name,
            "price": f"{signal.price:.4f}",
            "last_close": f"{signal.last_close:.4f}",
            "open": f"{signal.open:.4f}",
            "change_pct": f"{signal.change_pct:.4f}",
            "current_volume": f"{signal.current_volume:.4f}",
            "avg_volume": f"{signal.avg_volume:.4f}",
            "expected_volume": f"{signal.expected_volume:.4f}",
            "volume_ratio": f"{signal.volume_ratio:.4f}",
            "interval_volume": "" if signal.interval_volume is None else f"{signal.interval_volume:.4f}",
            "interval_spike_ratio": ""
            if signal.interval_spike_ratio is None
            else f"{signal.interval_spike_ratio:.4f}",
            "server": signal.server,
        }

    @staticmethod
    def _html_row(row: dict[str, str]) -> str:
        values = [
            "datetime",
            "code",
            "name",
            "price",
            "change_pct",
            "open",
            "current_volume",
            "volume_ratio",
            "interval_volume",
            "interval_spike_ratio",
            "server",
        ]
        cells = "".join(f"<td>{html.escape(row.get(key, ''))}</td>" for key in values)
        return f"<tr>{cells}</tr>"


CSV_FIELDS = [
    "datetime",
    "market",
    "code",
    "name",
    "price",
    "last_close",
    "open",
    "change_pct",
    "current_volume",
    "avg_volume",
    "expected_volume",
    "volume_ratio",
    "interval_volume",
    "interval_spike_ratio",
    "server",
]


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Break Watch Signals</title>
  <style>
    body {{ font-family: "Microsoft YaHei", Arial, sans-serif; margin: 24px; color: #172033; }}
    h1 {{ font-size: 22px; margin: 0 0 8px; }}
    .meta {{ color: #667085; margin-bottom: 18px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
    th, td {{ border: 1px solid #d0d5dd; padding: 8px 10px; text-align: right; }}
    th {{ background: #f2f4f7; color: #344054; }}
    td:nth-child(2), td:nth-child(3), th:nth-child(2), th:nth-child(3) {{ text-align: left; }}
    tr:nth-child(even) {{ background: #fafafa; }}
  </style>
</head>
<body>
  <h1>Break Watch Signals</h1>
  <div class="meta">Generated: {generated_at} | Count: {count}</div>
  <table>
    <thead>
      <tr>
        <th>Time</th>
        <th>Code</th>
        <th>Name</th>
        <th>Price</th>
        <th>Change %</th>
        <th>Open</th>
        <th>Volume</th>
        <th>Volume Ratio</th>
        <th>Interval Volume</th>
        <th>Spike Ratio</th>
        <th>Server</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""


def _fmt_number(value: float | None) -> str:
    if value is None:
        return "-"
    if abs(value) >= 10000:
        return f"{value / 10000:.2f}w"
    return f"{value:.0f}"


def _fmt_ratio(value: float | None) -> str:
    return "-" if value is None else f"{value:.2f}"
