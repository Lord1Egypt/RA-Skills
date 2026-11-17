from __future__ import annotations

import logging
from typing import Any, Callable, TypeVar

from .config import TdxConfig, TdxServer
from .models import Quote, Stock

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TdxClientError(RuntimeError):
    pass


class TdxClient:
    def __init__(self, config: TdxConfig):
        self.config = config
        self._api: Any | None = None
        self._server_index = 0
        self._connected_server: TdxServer | None = None

    @property
    def current_server(self) -> str:
        return self._connected_server.label if self._connected_server else "-"

    def close(self) -> None:
        if self._api is not None:
            try:
                self._api.disconnect()
            except Exception:
                logger.debug("Ignoring tdx disconnect failure.", exc_info=True)
        self._api = None
        self._connected_server = None

    def get_security_count(self, market: int) -> int:
        return int(self._request(lambda api: api.get_security_count(market)))

    def get_security_list(self, market: int, start: int) -> list[dict[str, Any]]:
        result = self._request(
            lambda api: api.get_security_list(market, start),
            allow_none=True,
        )
        if result is None:
            logger.warning("TDX security list returned no data: market=%s start=%s", market, start)
            return []
        return list(result or [])

    def get_quotes(self, stocks: list[Stock]) -> list[Quote]:
        if not stocks:
            return []
        raw_quotes = self._request(
            lambda api: api.get_security_quotes([(stock.market, stock.code) for stock in stocks])
        )
        if not raw_quotes:
            return []

        stock_by_key = {stock.key: stock for stock in stocks}
        quotes: list[Quote] = []
        for item in raw_quotes:
            quote = self._quote_from_item(item, stock_by_key)
            if quote is not None:
                quotes.append(quote)
        return quotes

    def get_daily_bars(self, stock: Stock, count: int) -> list[dict[str, Any]]:
        # category 9 is daily K-line in pytdx.
        return list(self._request(lambda api: api.get_security_bars(9, stock.market, stock.code, 0, count)) or [])

    def _request(self, operation: Callable[[Any], T], allow_none: bool = False) -> T | None:
        attempts = max(1, len(self.config.servers) * (self.config.reconnect_retries + 1))
        last_error: Exception | None = None

        for _ in range(attempts):
            try:
                self._ensure_connected()
                assert self._api is not None
                result = operation(self._api)
                if result is None:
                    if allow_none:
                        return None
                    raise TdxClientError("TDX request returned no data.")
                return result
            except Exception as exc:
                last_error = exc
                logger.warning("TDX request failed on %s: %s", self.current_server, exc)
                self.close()
                self._server_index = (self._server_index + 1) % len(self.config.servers)

        raise TdxClientError(f"TDX request failed after {attempts} attempts.") from last_error

    def _ensure_connected(self) -> None:
        if self._api is not None and self._connected_server is not None:
            return

        last_error: Exception | None = None
        for offset in range(len(self.config.servers)):
            index = (self._server_index + offset) % len(self.config.servers)
            server = self.config.servers[index]
            try:
                api = self._create_api()
                connected = api.connect(
                    server.host,
                    server.port,
                    time_out=self.config.timeout_seconds,
                )
                if not connected:
                    raise TdxClientError("connect returned false")
                self._api = api
                self._server_index = index
                self._connected_server = server
                logger.info("Connected to TDX server %s", server.label)
                return
            except Exception as exc:
                last_error = exc
                logger.warning("Failed to connect TDX server %s: %s", server.label, exc)

        raise TdxClientError("All TDX servers are unavailable.") from last_error

    @staticmethod
    def _create_api() -> Any:
        try:
            from pytdx.hq import TdxHq_API
        except ImportError as exc:
            raise TdxClientError(
                "pytdx is not installed. Run: .\\venv\\Scripts\\python.exe -m pip install -r requirements.txt"
            ) from exc
        return TdxHq_API(heartbeat=True)

    @staticmethod
    def _quote_from_item(item: dict[str, Any], stock_by_key: dict[tuple[int, str], Stock]) -> Quote | None:
        code = str(item.get("code", "")).strip()
        market = _market_from_quote(item, code)
        stock = stock_by_key.get((market, code))
        if stock is None:
            return None

        name = str(item.get("name") or stock.name or "").strip()
        if name and name != stock.name:
            stock = Stock(market=stock.market, code=stock.code, name=name)

        return Quote(
            stock=stock,
            price=_float_field(item, "price"),
            open=_float_field(item, "open"),
            last_close=_float_field(item, "last_close"),
            volume=_float_field(item, "vol", "volume"),
            amount=_optional_float_field(item, "amount"),
        )


def _market_from_quote(item: dict[str, Any], code: str) -> int:
    market = item.get("market")
    if market is not None:
        try:
            return int(market)
        except (TypeError, ValueError):
            pass
    if code.startswith("6"):
        return 1
    return 0


def _float_field(item: dict[str, Any], *names: str) -> float:
    for name in names:
        value = item.get(name)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def _optional_float_field(item: dict[str, Any], name: str) -> float | None:
    value = item.get(name)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
