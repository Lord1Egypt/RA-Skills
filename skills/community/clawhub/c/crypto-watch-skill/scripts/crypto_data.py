"""
Crypto Data API Module

Provides a collection of functions for fetching cryptocurrency market data from OKX and CoinMarketCap.

1) get_okx_candles(inst_id, bar="1H", limit=100) -> DataFrame
2) get_fear_greed_index(days=7) -> DataFrame
3) get_okx_funding_rate(inst_id, limit=100) -> DataFrame
4) get_okx_open_interest(inst_id, period="1H", limit=100) -> DataFrame
5) get_long_short_ratio(ccy, period="1H", limit=100) -> DataFrame
6) get_okx_liquidation(inst_id, state="filled", limit=100) -> DataFrame
7) get_top_trader_long_short_position_ratio(inst_id, period="5m", begin=None, end=None, limit=100) -> DataFrame
8) get_option_open_interest_volume_ratio(ccy, period="8H") -> DataFrame
"""

import requests
import pandas as pd
import time
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ==============================================================================
# Constants
# ==============================================================================
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0", "Connection": "close"}
DEFAULT_TIMEOUT = 10


def _handle_request_error(error: Exception) -> None:
    """Handle request exceptions uniformly and print error messages."""
    if isinstance(error, requests.exceptions.ReadTimeout):
        logger.info(
            "Error: Read timeout. Network congestion or server blocking possible."
        )
    elif isinstance(error, requests.exceptions.SSLError):
        logger.info("Error: SSL handshake failed.")
    else:
        logger.info(f"Error occurred: {error}")


def get_okx_candles(
    inst_id: str, bar: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get K-line data for OKX trading pairs."""
    url = "https://www.okx.com/api/v5/market/candles"
    params = {"instId": inst_id, "bar": bar, "limit": limit}
    try:
        logger.info(
            "Fetching OKX candles: inst_id=%s bar=%s limit=%d", inst_id, bar, limit
        )
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "0":
            logger.info("OKX candles API returned non-zero code: %s", data.get("code"))
            return None
        candles = data.get("data", [])
        df = pd.DataFrame(
            candles,
            columns=[
                "ts",
                "open",
                "high",
                "low",
                "close",
                "vol",
                "volCcy",
                "volCcyQuote",
                "confirm",
            ],
        )
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
        df = df[["datetime", "open", "high", "low", "close", "vol"]]
        for col in ["open", "high", "low", "close", "vol"]:
            df[col] = pd.to_numeric(df[col])
        df = df.sort_values("datetime").reset_index(drop=True)
        return df
    except Exception as e:
        _handle_request_error(e)
        return None


def get_fear_greed_index(days: int = 7) -> Optional[pd.DataFrame]:
    """Get Fear & Greed Index historical data (alternative.me)."""
    url = "https://api.alternative.me/fng/"
    params = {"limit": days}
    try:
        logger.info("Fetching Fear & Greed index: days=%d", days)
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("metadata", {}).get("error"):
            logger.info("Fear & Greed API error in response metadata")
            return None
        if data.get("data"):
            df = pd.DataFrame(data["data"])
            df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
            df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df[["date", "value", "value_classification"]]
            return df
        return None
    except Exception as e:
        _handle_request_error(e)
        return None


def get_okx_funding_rate(inst_id: str, limit: int = 100) -> Optional[pd.DataFrame]:
    """Get OKX perpetual contract funding rate history and current rate."""
    url_history = "https://www.okx.com/api/v5/public/funding-rate-history"
    url_current = "https://www.okx.com/api/v5/public/funding-rate"
    params_history = {"instId": inst_id, "limit": limit}
    params_current = {"instId": inst_id}
    try:
        logger.info("Fetching OKX funding rate: inst_id=%s limit=%d", inst_id, limit)
        res_hist = requests.get(
            url_history, params=params_history, timeout=DEFAULT_TIMEOUT
        )
        res_hist.raise_for_status()
        data_hist = res_hist.json()
        if data_hist.get("code") != "0":
            logger.info(
                "OKX funding history API returned non-zero code: %s",
                data_hist.get("code"),
            )
            return None
        df_hist = pd.DataFrame(data_hist["data"])
        df_hist = df_hist[["fundingTime", "fundingRate", "realizedRate"]]
        df_hist["type"] = "Settled"
        res_curr = requests.get(
            url_current, params=params_current, timeout=DEFAULT_TIMEOUT
        )
        res_curr.raise_for_status()
        data_curr = res_curr.json()
        if data_curr.get("code") != "0":
            logger.info(
                "OKX funding current API returned non-zero code: %s",
                data_curr.get("code"),
            )
            return None
        curr_record = data_curr["data"][0]
        row_0 = {
            "fundingTime": curr_record["fundingTime"],
            "fundingRate": curr_record["fundingRate"],
            "realizedRate": None,
            "type": "Current/Predicted",
        }
        df_curr = pd.DataFrame([row_0])
        df_final = pd.concat([df_curr, df_hist], axis=0, ignore_index=True)
        df_final["datetime"] = pd.to_datetime(
            pd.to_numeric(df_final["fundingTime"]), unit="ms"
        )
        df_final["fundingRate"] = pd.to_numeric(df_final["fundingRate"])
        df_final["realizedRate"] = pd.to_numeric(df_final["realizedRate"])
        df_final = df_final[["datetime", "fundingRate", "realizedRate", "type"]]
        return df_final
    except Exception as e:
        _handle_request_error(e)
        return None


def get_okx_open_interest(
    inst_id: str, period: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX Open Interest (including USD value)."""
    timeout_seconds = 30
    url_history = (
        "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history"
    )
    url_current_oi = "https://www.okx.com/api/v5/public/open-interest"
    url_mark_price = "https://www.okx.com/api/v5/public/mark-price"
    try:
        logger.info(
            "Fetching OKX open interest: inst_id=%s, period=%s, limit=%d",
            inst_id,
            period,
            limit,
        )
        params_hist = {"instId": inst_id, "period": period, "limit": limit}
        res_hist = requests.get(
            url_history,
            params=params_hist,
            headers=DEFAULT_HEADERS,
            timeout=timeout_seconds,
        )
        res_hist.raise_for_status()
        data_hist = res_hist.json()
        if data_hist.get("code") != "0":
            logger.info(
                "OKX open interest history API returned non-zero code: %s",
                data_hist.get("code"),
            )
            return None
        df_hist = pd.DataFrame(
            data_hist["data"], columns=["ts", "oi", "oiCcy", "oiUsd"]
        )
        df_hist = df_hist[["ts", "oiCcy", "oiUsd"]]
        df_hist["type"] = "History"
        res_curr = requests.get(
            url_current_oi,
            params={"instId": inst_id},
            headers=DEFAULT_HEADERS,
            timeout=timeout_seconds,
        )
        curr_data = res_curr.json()["data"][0]
        res_price = requests.get(
            url_mark_price,
            params={"instId": inst_id},
            headers=DEFAULT_HEADERS,
            timeout=timeout_seconds,
        )
        price_data = res_price.json()["data"][0]
        current_oi_ccy = float(curr_data["oiCcy"])
        current_price = float(price_data["markPx"])
        current_oi_usd = current_oi_ccy * current_price
        row_0 = {
            "ts": curr_data["ts"],
            "oiCcy": curr_data["oiCcy"],
            "oiUsd": current_oi_usd,
            "type": "Current (Real-time)",
        }
        df_curr = pd.DataFrame([row_0])
        df_final = pd.concat([df_curr, df_hist], axis=0, ignore_index=True)
        df_final["datetime"] = pd.to_datetime(pd.to_numeric(df_final["ts"]), unit="ms")
        df_final["oiCcy"] = pd.to_numeric(df_final["oiCcy"])
        df_final["oiUsd"] = pd.to_numeric(df_final["oiUsd"])
        df_final = df_final[["datetime", "oiCcy", "oiUsd", "type"]]
        return df_final
    except Exception as e:
        _handle_request_error(e)
        return None


def get_long_short_ratio(
    ccy: str, period: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX elite trader long/short account ratio. Simplified implementation, single request max 100 records."""
    base_url = (
        "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-account-ratio"
    )
    params = {"ccy": ccy, "period": period, "limit": limit}
    try:
        logger.info(
            "Fetching OKX long/short ratio: ccy=%s period=%s limit=%d",
            ccy,
            period,
            limit,
        )
        resp = requests.get(base_url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "0":
            logger.info(
                "OKX long/short API returned non-zero code: %s", data.get("code")
            )
            return None
        records = data.get("data", [])
        if not records:
            return None
        df = pd.DataFrame(records, columns=["ts", "longShortPosRatio"])
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
        df["longShortPosRatio"] = pd.to_numeric(df["longShortPosRatio"])
        df = df[["datetime", "longShortPosRatio"]]
        df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
        # Ensure we return exactly limit rows (API may return more or ignore limit)
        if len(df) > limit:
            df = df.head(limit)
        return df
    except Exception as e:
        _handle_request_error(e)
        return None


def get_okx_liquidation(
    inst_id: str, state: str = "filled", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX perpetual contract liquidation order data."""
    url = "https://www.okx.com/api/v5/public/liquidation-orders"
    if inst_id.endswith("-SWAP"):
        inst_family = inst_id[:-5]
    else:
        inst_family = inst_id
    params = {
        "instType": "SWAP",
        "instFamily": inst_family,
        "state": state,
        "limit": limit,
    }
    try:
        logger.info(
            "Fetching OKX liquidation: inst_id=%s, state=%s, limit=%d",
            inst_id,
            state,
            limit,
        )
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "0":
            logger.info(
                "OKX liquidation API returned non-zero code: %s", data.get("code")
            )
            return None
        data_list = data.get("data", [])
        if not data_list:
            return None
        all_details = []
        for item in data_list:
            for detail in item.get("details", []):
                all_details.append(
                    {
                        "ts": detail["ts"],
                        "side": detail["side"],
                        "bkPx": detail["bkPx"],
                        "sz": detail["sz"],
                    }
                )
        if not all_details:
            return None
        df = pd.DataFrame(all_details)
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
        df["bkPx"] = pd.to_numeric(df["bkPx"])
        df["sz"] = pd.to_numeric(df["sz"])
        df = df[["datetime", "side", "bkPx", "sz"]]
        df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        _handle_request_error(e)
        return None


def get_top_trader_long_short_position_ratio(
    inst_id: str,
    period: str = "5m",
    begin: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 100,
) -> Optional[pd.DataFrame]:
    """Get OKX elite trader long/short position ratio. Simplified implementation."""
    url = "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-position-ratio-contract-top-trader"
    params = {"instId": inst_id, "period": period, "limit": limit}
    if begin:
        params["begin"] = begin
    if end:
        params["end"] = end
    try:
        logger.info(
            "Fetching OKX top trader long/short ratio: inst_id=%s period=%s",
            inst_id,
            period,
        )
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "0":
            logger.info("OKX top trader ratio API code: %s", data.get("code"))
            return None
        records = data.get("data", [])
        if not records:
            return None
        df = pd.DataFrame(records, columns=["ts", "longShortPosRatio"])
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
        df["longShortPosRatio"] = pd.to_numeric(df["longShortPosRatio"])
        df = df[["datetime", "longShortPosRatio"]]
        df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        _handle_request_error(e)
        return None


def get_option_open_interest_volume_ratio(
    ccy: str, period: str = "8H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get call/put option open interest ratio and volume ratio."""
    url = "https://www.okx.com/api/v5/rubik/stat/option/open-interest-volume-ratio"
    params = {"ccy": ccy, "period": period}
    try:
        logger.info(
            "Fetching OKX option OI/volume ratio: ccy=%s period=%s limit=%d",
            ccy,
            period,
            limit,
        )
        resp = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "0":
            logger.info("OKX option ratio API non-zero code: %s", data.get("code"))
            return None
        records = data.get("data", [])
        if not records:
            return None
        df = pd.DataFrame(records, columns=["ts", "oiRatio", "volRatio"])
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
        df["oiRatio"] = pd.to_numeric(df["oiRatio"])
        df["volRatio"] = pd.to_numeric(df["volRatio"])
        df = df[["datetime", "oiRatio", "volRatio"]]
        df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
        # Ensure we return exactly limit rows (API may return more)
        if len(df) > limit:
            df = df.head(limit)
        return df
    except Exception as e:
        _handle_request_error(e)
        return None


def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    if df is not None:
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
    else:
        logger.info("No data to save to CSV.")


if __name__ == "__main__":
    logger.info(
        "Crypto data module test run. You can import and call functions from other modules."
    )
