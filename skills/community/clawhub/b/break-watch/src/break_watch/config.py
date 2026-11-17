from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TdxServer:
    host: str
    port: int

    @property
    def label(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass(frozen=True, slots=True)
class TdxConfig:
    servers: tuple[TdxServer, ...]
    timeout_seconds: float = 5.0
    reconnect_retries: int = 2
    quote_batch_size: int = 80


@dataclass(frozen=True, slots=True)
class ScanConfig:
    mode: str = "all"
    watchlist: tuple[str, ...] = ()
    exclude_star_market: bool = True
    exclude_bse: bool = True
    scan_interval_seconds: int = 30
    history_days: int = 20
    volume_ratio_threshold: float = 2.0
    interval_spike_threshold: float = 2.0
    interval_spike_window: int = 5
    interval_spike_min_samples: int = 3
    min_rise_pct: float = 1.0
    market_hours_only: bool = True
    repeat_alert: bool = False


@dataclass(frozen=True, slots=True)
class OutputConfig:
    log_dir: Path
    data_dir: Path
    result_dir: Path
    csv_enabled: bool = True
    html_enabled: bool = True
    ths_txt_enabled: bool = True
    ths_txt_code_format: str = "plain"
    console_enabled: bool = True


@dataclass(frozen=True, slots=True)
class AppConfig:
    path: Path
    root_dir: Path
    tdx: TdxConfig
    scan: ScanConfig
    output: OutputConfig


DEFAULT_SERVERS = (
    TdxServer("119.6.200.40", 7709),
    TdxServer("182.140.139.191", 7709),
    TdxServer("218.200.222.134", 7709),
    TdxServer("182.150.28.166", 7709),
)


def load_config(path: str | Path = "config.toml") -> AppConfig:
    config_path = Path(path).expanduser().resolve()
    if not config_path.exists():
        raise ConfigError(
            f"Config file not found: {config_path}. Copy config.example.toml to config.toml first."
        )

    with config_path.open("rb") as file:
        raw = tomllib.load(file)

    if not isinstance(raw, dict):
        raise ConfigError("Config root must be a table.")

    root_dir = config_path.parent
    tdx = _parse_tdx(raw.get("tdx", {}))
    scan = _parse_scan(raw.get("scan", {}))
    output = _parse_output(raw.get("output", {}), root_dir)

    return AppConfig(
        path=config_path,
        root_dir=root_dir,
        tdx=tdx,
        scan=scan,
        output=output,
    )


def _parse_tdx(raw: Any) -> TdxConfig:
    table = _table(raw, "tdx")
    servers_raw = table.get("servers", [])
    servers: list[TdxServer] = []

    if servers_raw:
        if not isinstance(servers_raw, list):
            raise ConfigError("tdx.servers must be a list.")
        for item in servers_raw:
            server = _table(item, "tdx.servers[]")
            host = str(server.get("host", "")).strip()
            port = _int(server.get("port", 7709), "tdx.servers[].port")
            if not host:
                raise ConfigError("tdx.servers[].host cannot be empty.")
            if port <= 0:
                raise ConfigError("tdx.servers[].port must be positive.")
            servers.append(TdxServer(host, port))
    else:
        servers.extend(DEFAULT_SERVERS)

    timeout_seconds = _float(table.get("timeout_seconds", 5), "tdx.timeout_seconds")
    reconnect_retries = _int(table.get("reconnect_retries", 2), "tdx.reconnect_retries")
    quote_batch_size = _int(table.get("quote_batch_size", 80), "tdx.quote_batch_size")

    if timeout_seconds <= 0:
        raise ConfigError("tdx.timeout_seconds must be positive.")
    if reconnect_retries < 0:
        raise ConfigError("tdx.reconnect_retries cannot be negative.")
    if quote_batch_size <= 0:
        raise ConfigError("tdx.quote_batch_size must be positive.")

    return TdxConfig(
        servers=tuple(servers),
        timeout_seconds=timeout_seconds,
        reconnect_retries=reconnect_retries,
        quote_batch_size=quote_batch_size,
    )


def _parse_scan(raw: Any) -> ScanConfig:
    table = _table(raw, "scan")
    mode = str(table.get("mode", "all")).strip().lower()
    if mode not in {"all", "watchlist"}:
        raise ConfigError('scan.mode must be "all" or "watchlist".')

    watchlist_raw = table.get("watchlist", [])
    if not isinstance(watchlist_raw, list):
        raise ConfigError("scan.watchlist must be a list.")
    watchlist = tuple(str(item).strip() for item in watchlist_raw if str(item).strip())

    scan = ScanConfig(
        mode=mode,
        watchlist=watchlist,
        exclude_star_market=_bool(table.get("exclude_star_market", True), "scan.exclude_star_market"),
        exclude_bse=_bool(table.get("exclude_bse", True), "scan.exclude_bse"),
        scan_interval_seconds=_int(table.get("scan_interval_seconds", 30), "scan.scan_interval_seconds"),
        history_days=_int(table.get("history_days", 20), "scan.history_days"),
        volume_ratio_threshold=_float(table.get("volume_ratio_threshold", 2.0), "scan.volume_ratio_threshold"),
        interval_spike_threshold=_float(table.get("interval_spike_threshold", 2.0), "scan.interval_spike_threshold"),
        interval_spike_window=_int(table.get("interval_spike_window", 5), "scan.interval_spike_window"),
        interval_spike_min_samples=_int(table.get("interval_spike_min_samples", 3), "scan.interval_spike_min_samples"),
        min_rise_pct=_float(table.get("min_rise_pct", 1.0), "scan.min_rise_pct"),
        market_hours_only=_bool(table.get("market_hours_only", True), "scan.market_hours_only"),
        repeat_alert=_bool(table.get("repeat_alert", False), "scan.repeat_alert"),
    )

    if scan.mode == "watchlist" and not scan.watchlist:
        raise ConfigError("scan.watchlist cannot be empty when scan.mode is watchlist.")
    if scan.scan_interval_seconds <= 0:
        raise ConfigError("scan.scan_interval_seconds must be positive.")
    if scan.history_days <= 0:
        raise ConfigError("scan.history_days must be positive.")
    if scan.volume_ratio_threshold <= 0:
        raise ConfigError("scan.volume_ratio_threshold must be positive.")
    if scan.interval_spike_threshold <= 0:
        raise ConfigError("scan.interval_spike_threshold must be positive.")
    if scan.interval_spike_window <= 0:
        raise ConfigError("scan.interval_spike_window must be positive.")
    if scan.interval_spike_min_samples <= 0:
        raise ConfigError("scan.interval_spike_min_samples must be positive.")
    if scan.interval_spike_min_samples > scan.interval_spike_window:
        raise ConfigError("scan.interval_spike_min_samples cannot exceed scan.interval_spike_window.")
    if scan.min_rise_pct < 0:
        raise ConfigError("scan.min_rise_pct cannot be negative.")

    return scan


def _parse_output(raw: Any, root_dir: Path) -> OutputConfig:
    table = _table(raw, "output")
    code_format = str(table.get("ths_txt_code_format", "plain")).strip().lower()
    if code_format not in {"plain", "prefix"}:
        raise ConfigError('output.ths_txt_code_format must be "plain" or "prefix".')

    return OutputConfig(
        log_dir=_resolve_dir(root_dir, table.get("log_dir", "logs")),
        data_dir=_resolve_dir(root_dir, table.get("data_dir", "data")),
        result_dir=_resolve_dir(root_dir, table.get("result_dir", "output")),
        csv_enabled=_bool(table.get("csv_enabled", True), "output.csv_enabled"),
        html_enabled=_bool(table.get("html_enabled", True), "output.html_enabled"),
        ths_txt_enabled=_bool(table.get("ths_txt_enabled", True), "output.ths_txt_enabled"),
        ths_txt_code_format=code_format,
        console_enabled=_bool(table.get("console_enabled", True), "output.console_enabled"),
    )


def _resolve_dir(root_dir: Path, value: Any) -> Path:
    path = Path(str(value)).expanduser()
    if not path.is_absolute():
        path = root_dir / path
    return path.resolve()


def _table(value: Any, name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError(f"{name} must be a table.")
    return value


def _int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ConfigError(f"{name} must be an integer.")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be an integer.") from exc


def _float(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ConfigError(f"{name} must be a number.")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be a number.") from exc


def _bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigError(f"{name} must be true or false.")
    return value
