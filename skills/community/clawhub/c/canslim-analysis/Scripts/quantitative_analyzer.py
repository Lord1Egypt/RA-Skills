import concurrent.futures
import json
import logging
import os
import warnings
from datetime import datetime
from io import StringIO
from time import sleep
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import yfinance as yf
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("canslim_analysis.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=FutureWarning)

MIN_EPS_GROWTH = 0.25
MIN_ANNUAL_EPS_GROWTH = 0.25
MIN_RS_RATING = 80.0
MIN_VOLUME_RATIO = 1.5
MIN_VOLUME_SKEW = 1.2
MIN_INSTITUTIONAL_OWNERSHIP = 0.30
NEAR_HIGH_THRESHOLD = 0.10

MARKET_LOOKBACK_DAYS = 200
MIN_HISTORY_DAYS = 250
MAX_WORKERS = 5
DEFAULT_UNIVERSE_LIMIT = None
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

SCHEMA_VERSION = "2.1"


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None or pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_ratio(value: Any) -> Optional[float]:
    raw = safe_float(value)
    if raw is None:
        return None
    if raw < 0:
        return 0.0
    if raw <= 1.0:
        return raw
    if raw <= 2.0:
        return 1.0
    if raw <= 100.0:
        return min(raw / 100.0, 1.0)
    return 1.0


def pct_text(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def default_ai_pending() -> Dict[str, Any]:
    return {
        "N_New_Catalyst": None,
        "N_Catalyst_Details": "",
        "S_Float_Tightness": None,
        "S_Float_Details": "",
        "I_Institutional_Quality": None,
        "I_Institutional_Details": "",
    }


def get_sp500_tickers() -> List[str]:
    logger.info("Fetching S&P 500 tickers from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            table = pd.read_html(StringIO(response.text))[0]
            tickers = table["Symbol"].str.replace(".", "-", regex=False).tolist()
            logger.info("Fetched %s S&P 500 tickers", len(tickers))
            return tickers
        except Exception as exc:
            last_error = exc
            logger.warning(
                "Attempt %s/%s failed fetching tickers: %s",
                attempt + 1,
                MAX_RETRIES,
                exc,
            )
            if attempt < MAX_RETRIES - 1:
                sleep(RETRY_DELAY)

    raise RuntimeError(f"Failed to fetch S&P 500 tickers: {last_error}")


def assess_market_direction() -> str:
    logger.info("Assessing market direction...")
    indices = {"S&P 500": "^GSPC", "Nasdaq": "^IXIC"}
    uptrend_count = 0

    for name, ticker in indices.items():
        try:
            hist = yf.Ticker(ticker).history(period="1y", auto_adjust=False)
            if hist.empty or len(hist) < MARKET_LOOKBACK_DAYS:
                logger.warning("Insufficient market history for %s", name)
                continue

            close = hist["Close"]
            current_price = float(close.iloc[-1])
            sma_50 = float(close.tail(50).mean())
            sma_200 = float(close.tail(200).mean())

            if current_price > sma_50 and current_price > sma_200 and sma_50 > sma_200:
                uptrend_count += 1
                logger.info(
                    "%s in confirmed uptrend: price=%.2f, 50MA=%.2f, 200MA=%.2f",
                    name,
                    current_price,
                    sma_50,
                    sma_200,
                )
            else:
                logger.info(
                    "%s not in confirmed uptrend: price=%.2f, 50MA=%.2f, 200MA=%.2f",
                    name,
                    current_price,
                    sma_50,
                    sma_200,
                )
        except Exception as exc:
            logger.error("Error assessing %s: %s", name, exc)

    if uptrend_count == 2:
        return "Confirmed Uptrend"
    if uptrend_count == 1:
        return "Under Pressure"
    return "Downtrend"


def get_eps_series(frame: pd.DataFrame, row_names: List[str]) -> Optional[List[float]]:
    if frame is None or frame.empty:
        return None

    for row_name in row_names:
        if row_name in frame.index:
            series = frame.loc[row_name].dropna()
            values = [safe_float(v) for v in series.tolist()]
            values = [v for v in values if v is not None]
            if values:
                return values
    return None


def calculate_cagr(newest: float, oldest: float, periods: int) -> Optional[float]:
    if periods <= 0 or newest <= 0 or oldest <= 0:
        return None
    try:
        return (newest / oldest) ** (1 / periods) - 1
    except Exception:
        return None


def get_annual_eps_growth(stock: yf.Ticker) -> Optional[float]:
    try:
        eps_values = get_eps_series(stock.income_stmt, ["Diluted EPS", "Basic EPS"])
        if not eps_values or len(eps_values) < 3:
            return None

        newest = eps_values[0]
        oldest = eps_values[-1]
        periods = len(eps_values) - 1
        return calculate_cagr(newest, oldest, periods)
    except Exception:
        return None


def get_quarterly_eps_acceleration(stock: yf.Ticker) -> Dict[str, Any]:
    result = {
        "is_accelerating": False,
        "latest_yoy_growth": None,
        "previous_yoy_growth": None,
        "eps_values": [],
    }

    try:
        eps_values = get_eps_series(
            stock.quarterly_income_stmt,
            ["Diluted EPS", "Basic EPS"],
        )
        if not eps_values:
            return result

        result["eps_values"] = eps_values

        if len(eps_values) >= 5 and eps_values[4] not in (None, 0):
            result["latest_yoy_growth"] = (
                eps_values[0] - eps_values[4]
            ) / abs(eps_values[4])

        if len(eps_values) >= 6 and eps_values[5] not in (None, 0):
            result["previous_yoy_growth"] = (
                eps_values[1] - eps_values[5]
            ) / abs(eps_values[5])

        latest_yoy = result["latest_yoy_growth"]
        previous_yoy = result["previous_yoy_growth"]

        if latest_yoy is not None and previous_yoy is not None:
            result["is_accelerating"] = (
                latest_yoy > 0 and previous_yoy > 0 and latest_yoy > previous_yoy
            )

        return result
    except Exception:
        return result


def analyze_supply_demand(hist: pd.DataFrame) -> Dict[str, Any]:
    result = {
        "S_Quant_Met": False,
        "S_Quant_Details": "",
        "S_Score": 0,
        "Today_Volume_Strong": False,
        "Volume_Skew_Positive": False,
        "Vol_Today": None,
        "Vol_50D_Avg": None,
    }

    if hist is None or hist.empty or len(hist) < 60:
        result["S_Quant_Details"] = "Insufficient volume history"
        return result

    vol_today = safe_float(hist["Volume"].iloc[-1])
    vol_50d_avg = safe_float(hist["Volume"].tail(50).mean())
    if vol_today is not None:
        result["Vol_Today"] = vol_today
    if vol_50d_avg is not None:
        result["Vol_50D_Avg"] = vol_50d_avg

    if vol_today is not None and vol_50d_avg not in (None, 0):
        result["Today_Volume_Strong"] = vol_today >= (vol_50d_avg * MIN_VOLUME_RATIO)

    last_60 = hist.tail(60).copy()
    up_days = last_60[last_60["Close"] > last_60["Open"]]
    down_days = last_60[last_60["Close"] < last_60["Open"]]

    if not up_days.empty and not down_days.empty:
        avg_up_volume = safe_float(up_days["Volume"].mean())
        avg_down_volume = safe_float(down_days["Volume"].mean())
        if avg_up_volume is not None and avg_down_volume not in (None, 0):
            result["Volume_Skew_Positive"] = avg_up_volume >= (
                avg_down_volume * MIN_VOLUME_SKEW
            )

    result["S_Score"] = int(result["Today_Volume_Strong"]) + int(
        result["Volume_Skew_Positive"]
    )
    result["S_Quant_Met"] = result["S_Score"] >= 2

    details = []
    if result["Today_Volume_Strong"]:
        details.append("Today volume >= 1.5x 50-day average")
    if result["Volume_Skew_Positive"]:
        details.append("Up-day volume skew positive")
    if not details:
        details.append("No strong quantitative S signal")
    result["S_Quant_Details"] = ", ".join(details)

    return result


def analyze_institutional_ownership(info: Dict[str, Any]) -> Dict[str, Any]:
    ownership = normalize_ratio(info.get("heldPercentInstitutions"))
    quant_flag = ownership is not None and ownership >= MIN_INSTITUTIONAL_OWNERSHIP

    details = "Institutional ownership unavailable"
    if ownership is not None:
        details = f"{ownership * 100:.1f}% institutional ownership"

    return {
        "I_Quant_Flag": quant_flag,
        "I_Quant_Details": details,
        "Institutional_Ownership": ownership,
    }


def analyze_new_highs(hist: pd.DataFrame) -> Dict[str, Any]:
    result = {
        "N_Technical_Met": False,
        "N_Technical_Details": "",
        "Near_52_Week_High": False,
        "Recent_Breakout": False,
        "Pct_From_High": None,
        "High_52_Week": None,
    }

    if hist is None or hist.empty or len(hist) < 50:
        result["N_Technical_Details"] = "Insufficient price history"
        return result

    current_price = safe_float(hist["Close"].iloc[-1])
    high_52w = safe_float(hist["Close"].max())
    if current_price is None or high_52w in (None, 0):
        result["N_Technical_Details"] = "Unable to compute 52-week high"
        return result

    result["High_52_Week"] = high_52w
    pct_from_high = (high_52w - current_price) / high_52w
    result["Pct_From_High"] = pct_from_high
    result["Near_52_Week_High"] = pct_from_high <= NEAR_HIGH_THRESHOLD

    if len(hist) >= 21:
        prior_high = safe_float(hist["Close"].iloc[:-1].tail(20).max())
        if prior_high is not None:
            result["Recent_Breakout"] = current_price > prior_high

    result["N_Technical_Met"] = (
        result["Near_52_Week_High"] or result["Recent_Breakout"]
    )

    details = []
    if result["Near_52_Week_High"]:
        details.append(f"Within {pct_from_high * 100:.1f}% of 52-week high")
    else:
        details.append(f"{pct_from_high * 100:.1f}% below 52-week high")
    if result["Recent_Breakout"]:
        details.append("Recent breakout above prior 20-day high")
    result["N_Technical_Details"] = ", ".join(details)

    return result


def fetch_stock_data(ticker: str) -> Optional[Dict[str, Any]]:
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info or {}
            hist = stock.history(period="1y", auto_adjust=False)

            if hist.empty or len(hist) < MIN_HISTORY_DAYS:
                return None

            current_price = safe_float(hist["Close"].iloc[-1])
            price_1y_ago = safe_float(hist["Close"].iloc[0])
            if current_price is None or price_1y_ago in (None, 0):
                return None

            return_1y = (current_price - price_1y_ago) / abs(price_1y_ago)

            eps_accel = get_quarterly_eps_acceleration(stock)
            quarterly_eps_growth = safe_float(info.get("earningsQuarterlyGrowth"))
            if quarterly_eps_growth is None:
                quarterly_eps_growth = eps_accel.get("latest_yoy_growth")

            annual_eps_growth = get_annual_eps_growth(stock)

            s_result = analyze_supply_demand(hist)
            i_result = analyze_institutional_ownership(info)
            n_result = analyze_new_highs(hist)

            return {
                "Ticker": ticker,
                "Company_Name": info.get("shortName", ticker),
                "Current_Price": round(current_price, 2),
                "Return_1Y": return_1y,
                "Quarterly_EPS_Growth": quarterly_eps_growth,
                "EPS_Accelerating": bool(eps_accel.get("is_accelerating", False)),
                "Annual_EPS_Growth": annual_eps_growth,
                "Float_Shares": safe_float(info.get("floatShares")),
                "Institutional_Ownership": i_result["Institutional_Ownership"],
                "S_Quant_Met": s_result["S_Quant_Met"],
                "S_Quant_Details": s_result["S_Quant_Details"],
                "S_Score": s_result["S_Score"],
                "Today_Volume_Strong": s_result["Today_Volume_Strong"],
                "Volume_Skew_Positive": s_result["Volume_Skew_Positive"],
                "Vol_Today": s_result["Vol_Today"],
                "Vol_50D_Avg": s_result["Vol_50D_Avg"],
                "I_Quant_Flag": i_result["I_Quant_Flag"],
                "I_Quant_Details": i_result["I_Quant_Details"],
                "N_Technical_Met": n_result["N_Technical_Met"],
                "N_Technical_Details": n_result["N_Technical_Details"],
                "Near_52_Week_High": n_result["Near_52_Week_High"],
                "Recent_Breakout": n_result["Recent_Breakout"],
                "Pct_From_High": n_result["Pct_From_High"],
                "High_52_Week": n_result["High_52_Week"],
            }
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                sleep(RETRY_DELAY)

    logger.debug("%s failed after retries: %s", ticker, last_error)
    return None


def build_c_details(quarterly_eps_growth: float, accelerating: bool) -> str:
    details = [f"Q EPS Growth: {quarterly_eps_growth * 100:.1f}%"]
    if accelerating:
        details.append("accelerating")
    return " (" .join(details[:-1]) + f" ({details[-1]})" if len(details) > 1 else details[0]


def build_stock_record(row: pd.Series) -> Dict[str, Any]:
    quarterly_eps_growth = safe_float(row.get("Quarterly_EPS_Growth"))
    annual_eps_growth = safe_float(row.get("Annual_EPS_Growth"))
    rs_rating = safe_float(row.get("RS_Rating")) or 0.0

    c_met = quarterly_eps_growth is not None and quarterly_eps_growth >= MIN_EPS_GROWTH
    a_met = annual_eps_growth is not None and annual_eps_growth >= MIN_ANNUAL_EPS_GROWTH
    l_met = rs_rating >= MIN_RS_RATING

    c_details = (
        build_c_details(quarterly_eps_growth, bool(row.get("EPS_Accelerating", False)))
        if quarterly_eps_growth is not None
        else "Quarterly EPS growth unavailable"
    )
    a_details = (
        f"Annual EPS CAGR: {annual_eps_growth * 100:.1f}%"
        if annual_eps_growth is not None
        else "Annual EPS growth unavailable"
    )

    stock = {
        "Ticker": row["Ticker"],
        "Company_Name": row["Company_Name"],
        "Quantitative_Metrics": {
            "C_Met": bool(c_met),
            "C_Details": c_details,
            "Quarterly_EPS_Growth": quarterly_eps_growth,
            "EPS_Accelerating": bool(row.get("EPS_Accelerating", False)),
            "A_Met": bool(a_met),
            "A_Details": a_details,
            "Annual_EPS_Growth": annual_eps_growth,
            "L_Met": bool(l_met),
            "RS_Rating": round(rs_rating, 1),
            "S_Quant_Met": bool(row.get("S_Quant_Met", False)),
            "S_Quant_Details": row.get("S_Quant_Details", ""),
            "S_Score": int(row.get("S_Score", 0)),
            "Today_Volume_Strong": bool(row.get("Today_Volume_Strong", False)),
            "Volume_Skew_Positive": bool(row.get("Volume_Skew_Positive", False)),
            "I_Quant_Flag": bool(row.get("I_Quant_Flag", False)),
            "I_Quant_Details": row.get("I_Quant_Details", ""),
            "N_Technical_Met": bool(row.get("N_Technical_Met", False)),
            "N_Technical_Details": row.get("N_Technical_Details", ""),
            "Near_52_Week_High": bool(row.get("Near_52_Week_High", False)),
            "Recent_Breakout": bool(row.get("Recent_Breakout", False)),
            "Pct_From_High": safe_float(row.get("Pct_From_High")),
            "Current_Price": safe_float(row.get("Current_Price")),
            "Float_Shares": safe_float(row.get("Float_Shares")),
            "Institutional_Ownership": normalize_ratio(
                row.get("Institutional_Ownership")
            ),
            "High_52_Week": safe_float(row.get("High_52_Week")),
            "Vol_Today": safe_float(row.get("Vol_Today")),
            "Vol_50D_Avg": safe_float(row.get("Vol_50D_Avg")),
            "Schema_Version": SCHEMA_VERSION,
            # Backward-compatible aliases
            "S_Met": bool(row.get("S_Quant_Met", False)),
            "S_Details": row.get("S_Quant_Details", ""),
            "I_Met": bool(row.get("I_Quant_Flag", False)),
            "I_Details": row.get("I_Quant_Details", ""),
            "N_Met": bool(row.get("N_Technical_Met", False)),
            "N_Details": row.get("N_Technical_Details", ""),
        },
        "AI_Qualitative_Checks_Pending": default_ai_pending(),
    }
    return stock


def main() -> None:
    logger.info("--- Starting Fixed CANSLIM Quantitative Analysis ---")

    market_direction = assess_market_direction()
    tickers = get_sp500_tickers()

    if DEFAULT_UNIVERSE_LIMIT:
        tickers = tickers[:DEFAULT_UNIVERSE_LIMIT]

    stock_rows: List[Dict[str, Any]] = []
    failed_fetches = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_stock_data, ticker): ticker for ticker in tickers}
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Downloading market data",
            unit="stock",
        ):
            result = future.result()
            if result is None:
                failed_fetches += 1
            else:
                stock_rows.append(result)

    if not stock_rows:
        logger.error("No stock data retrieved. Exiting.")
        return

    df = pd.DataFrame(stock_rows)
    df["RS_Rating"] = (
        df["Return_1Y"].rank(pct=True, method="average").mul(99).clip(1, 99).round(1)
    )

    passed_stocks: List[Dict[str, Any]] = []
    skipped_for_missing_fundamentals = 0

    for _, row in tqdm(
        df.iterrows(),
        total=len(df),
        desc="Evaluating criteria",
        unit="stock",
    ):
        quarterly_eps_growth = safe_float(row.get("Quarterly_EPS_Growth"))
        annual_eps_growth = safe_float(row.get("Annual_EPS_Growth"))

        if quarterly_eps_growth is None or annual_eps_growth is None:
            skipped_for_missing_fundamentals += 1
            continue

        c_met = quarterly_eps_growth >= MIN_EPS_GROWTH
        a_met = annual_eps_growth >= MIN_ANNUAL_EPS_GROWTH
        l_met = safe_float(row.get("RS_Rating")) is not None and row["RS_Rating"] >= MIN_RS_RATING

        if c_met and a_met and l_met:
            passed_stocks.append(build_stock_record(row))

    passed_stocks.sort(
        key=lambda x: x["Quantitative_Metrics"]["RS_Rating"],
        reverse=True,
    )

    output_data = {
        "Metadata": {
            "Schema_Version": SCHEMA_VERSION,
            "Date_Run": datetime.now().strftime("%Y-%m-%d"),
            "Market_Direction_M": market_direction,
            "Total_Universe_Scanned": len(tickers),
            "Successfully_Evaluated": len(df),
            "Failed_Fetches": failed_fetches,
            "Skipped_For_Missing_Fundamentals": skipped_for_missing_fundamentals,
            "Stocks_Passed_To_AI": len(passed_stocks),
            "Fixes_Applied": [
                "Canonical schema preserved across pipeline",
                "A criterion uses EPS CAGR instead of ROE proxy",
                "Technical N separated from AI catalyst N",
                "S scoring separated into quantitative accumulation and AI float confirmation",
                "I final scoring reserved for AI institutional-quality validation",
            ],
        },
        "Stocks": passed_stocks,
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "intermediate_canslim.json")

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(output_data, handle, indent=4)

    logger.info("Market direction: %s", market_direction)
    logger.info("Successfully evaluated: %s", len(df))
    logger.info("Skipped for missing fundamentals: %s", skipped_for_missing_fundamentals)
    logger.info("Passed to AI phase: %s", len(passed_stocks))
    logger.info("Results saved to: %s", output_path)


if __name__ == "__main__":
    main()
