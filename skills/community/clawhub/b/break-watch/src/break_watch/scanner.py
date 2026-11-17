from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Protocol

from .config import AppConfig, ScanConfig
from .models import HistoryBaseline, Quote, Signal, Stock
from .trading_time import is_trading_time, trading_progress

logger = logging.getLogger(__name__)


class QuoteClient(Protocol):
    @property
    def current_server(self) -> str:
        ...

    def get_quotes(self, stocks: list[Stock]) -> list[Quote]:
        ...

    def get_daily_bars(self, stock: Stock, count: int) -> list[dict[str, Any]]:
        ...


class SignalSink(Protocol):
    def emit(self, signals: list[Signal]) -> None:
        ...


@dataclass(slots=True)
class VolumeWindow:
    window_size: int
    previous_volume: float | None = None
    recent_intervals: deque[float] = field(default_factory=deque)

    def observe(self, current_volume: float, min_samples: int) -> tuple[float | None, float | None]:
        if self.previous_volume is None:
            self.previous_volume = current_volume
            return None, None

        interval_volume = max(0.0, current_volume - self.previous_volume)
        self.previous_volume = current_volume

        spike_ratio: float | None = None
        if len(self.recent_intervals) >= min_samples:
            avg_interval = sum(self.recent_intervals) / len(self.recent_intervals)
            if avg_interval > 0:
                spike_ratio = interval_volume / avg_interval

        self.recent_intervals.append(interval_volume)
        while len(self.recent_intervals) > self.window_size:
            self.recent_intervals.popleft()

        return interval_volume, spike_ratio


class SignalEvaluator:
    def __init__(self, config: ScanConfig):
        self.config = config
        self._volume_windows: dict[tuple[int, str], VolumeWindow] = {}

    def evaluate(
        self,
        quote: Quote,
        baseline: HistoryBaseline,
        progress: float,
        timestamp: datetime,
        server: str,
    ) -> Signal | None:
        if not self._has_valid_quote(quote):
            return None
        if not baseline.ready or baseline.sample_days < self.config.history_days:
            return None
        if progress <= 0:
            return None

        expected_volume = baseline.avg_volume * progress
        if expected_volume <= 0:
            return None

        change_pct = (quote.price / quote.last_close - 1) * 100
        is_bullish_candle = quote.price > quote.open
        is_rising = quote.price >= quote.last_close * (1 + self.config.min_rise_pct / 100)
        volume_ratio = quote.volume / expected_volume
        is_history_volume_breakout = volume_ratio >= self.config.volume_ratio_threshold

        window = self._volume_windows.setdefault(
            quote.stock.key,
            VolumeWindow(window_size=self.config.interval_spike_window),
        )
        interval_volume, interval_spike_ratio = window.observe(
            quote.volume,
            self.config.interval_spike_min_samples,
        )
        is_interval_spike_ready = interval_spike_ratio is not None
        is_interval_volume_spike = (
            not is_interval_spike_ready
            or interval_spike_ratio >= self.config.interval_spike_threshold
        )

        if not (is_bullish_candle and is_rising and is_history_volume_breakout and is_interval_volume_spike):
            return None

        return Signal(
            stock=quote.stock,
            timestamp=timestamp,
            price=quote.price,
            last_close=quote.last_close,
            open=quote.open,
            change_pct=change_pct,
            current_volume=quote.volume,
            avg_volume=baseline.avg_volume,
            expected_volume=expected_volume,
            volume_ratio=volume_ratio,
            interval_volume=interval_volume,
            interval_spike_ratio=interval_spike_ratio,
            server=server,
        )

    @staticmethod
    def _has_valid_quote(quote: Quote) -> bool:
        return quote.price > 0 and quote.open > 0 and quote.last_close > 0 and quote.volume >= 0


class ScanRunner:
    def __init__(
        self,
        config: AppConfig,
        client: QuoteClient,
        sink: SignalSink,
        now: Callable[[], datetime] = datetime.now,
        sleeper: Callable[[float], None] = time.sleep,
    ):
        self.config = config
        self.client = client
        self.sink = sink
        self.now = now
        self.sleeper = sleeper
        self.evaluator = SignalEvaluator(config.scan)
        self._emitted: set[tuple[int, str, date]] = set()

    def build_baselines(self, stocks: Iterable[Stock]) -> dict[tuple[int, str], HistoryBaseline]:
        baselines: dict[tuple[int, str], HistoryBaseline] = {}
        count = self.config.scan.history_days + 5
        today = self.now().date()

        for index, stock in enumerate(stocks, start=1):
            try:
                bars = self.client.get_daily_bars(stock, count)
                baseline = calculate_history_baseline(stock, bars, self.config.scan.history_days, today)
            except Exception:
                logger.exception("Failed to load daily bars for %s", stock.display_code)
                continue

            if baseline.ready and baseline.sample_days >= self.config.scan.history_days:
                baselines[stock.key] = baseline
            else:
                logger.warning(
                    "Skip %s because history bars are insufficient: %s/%s",
                    stock.display_code,
                    baseline.sample_days,
                    self.config.scan.history_days,
                )

            if index % 200 == 0:
                logger.info("Loaded history baselines: %s", index)

        return baselines

    def scan_once(self, stocks: list[Stock], baselines: dict[tuple[int, str], HistoryBaseline]) -> list[Signal]:
        timestamp = self.now()
        progress = trading_progress(timestamp)
        signals: list[Signal] = []

        for batch in _chunks(stocks, self.config.tdx.quote_batch_size):
            quotes = self.client.get_quotes(batch)
            for quote in quotes:
                baseline = baselines.get(quote.stock.key)
                if baseline is None:
                    continue
                signal = self.evaluator.evaluate(
                    quote=quote,
                    baseline=baseline,
                    progress=progress,
                    timestamp=timestamp,
                    server=self.client.current_server,
                )
                if signal is None or self._should_skip_repeat(signal):
                    continue
                self._mark_emitted(signal)
                signals.append(signal)

        if signals:
            self.sink.emit(signals)
        return signals

    def run_forever(self, stocks: list[Stock], baselines: dict[tuple[int, str], HistoryBaseline]) -> None:
        while True:
            timestamp = self.now()
            if self.config.scan.market_hours_only and not is_trading_time(timestamp):
                logger.info("Outside market hours, waiting for next scan.")
                self.sleeper(self.config.scan.scan_interval_seconds)
                continue

            try:
                signals = self.scan_once(stocks, baselines)
                logger.info("Scan finished, signals=%s", len(signals))
            except Exception:
                logger.exception("Scan round failed.")

            self.sleeper(self.config.scan.scan_interval_seconds)

    def _should_skip_repeat(self, signal: Signal) -> bool:
        if self.config.scan.repeat_alert:
            return False
        return (signal.stock.market, signal.stock.code, signal.timestamp.date()) in self._emitted

    def _mark_emitted(self, signal: Signal) -> None:
        self._emitted.add((signal.stock.market, signal.stock.code, signal.timestamp.date()))


def calculate_history_baseline(
    stock: Stock,
    bars: list[dict[str, Any]],
    history_days: int,
    today: date | None = None,
) -> HistoryBaseline:
    today = today or date.today()
    dated_volumes: list[tuple[date, float]] = []
    undated_volumes: list[float] = []

    for bar in bars:
        bar_date = _bar_date(bar)
        if bar_date == today:
            continue
        volume = _bar_volume(bar)
        if volume <= 0:
            continue
        if bar_date is None:
            undated_volumes.append(volume)
        else:
            dated_volumes.append((bar_date, volume))

    dated_volumes.sort(key=lambda item: item[0])
    volumes = [volume for _, volume in dated_volumes] or undated_volumes
    selected = volumes[-history_days:]
    avg_volume = sum(selected) / len(selected) if selected else 0.0
    return HistoryBaseline(stock=stock, avg_volume=avg_volume, sample_days=len(selected))


def _bar_volume(bar: dict[str, Any]) -> float:
    for key in ("vol", "volume"):
        value = bar.get(key)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def _bar_date(bar: dict[str, Any]) -> date | None:
    try:
        if {"year", "month", "day"}.issubset(bar):
            return date(int(bar["year"]), int(bar["month"]), int(bar["day"]))
        raw = bar.get("datetime") or bar.get("date")
        if raw:
            return datetime.fromisoformat(str(raw)[:10]).date()
    except (TypeError, ValueError):
        return None
    return None


def _chunks(items: list[Stock], size: int) -> Iterable[list[Stock]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]
