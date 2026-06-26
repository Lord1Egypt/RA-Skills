from __future__ import annotations

from copy import deepcopy
from math import isfinite
import warnings

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:  # pragma: no cover - exercised in runtime environments without deps
    np = None
    pd = None
    yf = None


def _require_deps() -> None:
    if np is None or pd is None or yf is None:
        raise RuntimeError(
            "Yahoo normalization requires numpy, pandas, and yfinance. "
            "Install the project dependencies before using provider-backed normalization."
        )


def _coerce_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if isfinite(out) else None


def _frame_to_df(frame):
    _require_deps()
    return frame if isinstance(frame, pd.DataFrame) else pd.DataFrame()


def _syn(df, names):
    _require_deps()
    for name in names:
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
    return pd.Series(dtype=float, index=df.index)


def _merge_series(*series_list):
    _require_deps()
    out = None
    for series in series_list:
        if series is None:
            continue
        if out is None:
            out = series.copy()
        else:
            out = out.combine_first(series)
    if out is None:
        return pd.Series(dtype=float)
    return out


def _normalize_symbol(symbol: str, market: str | None = None) -> str:
    sym = str(symbol or "").strip().upper()
    if sym.endswith(".SH"):
        return sym[:-3] + ".SS"
    return sym


def _history_close(frame):
    _require_deps()
    if frame is None or frame.empty:
        return pd.Series(dtype=float)
    for column in ("Adj Close", "Close"):
        if column in frame.columns:
            series = frame[column]
            if isinstance(series, pd.DataFrame):
                series = series.iloc[:, 0]
            return pd.to_numeric(series, errors="coerce").dropna()
    return pd.Series(dtype=float)


def _latest_valid(series):
    _require_deps()
    if series is None:
        return None
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return None
    return _coerce_float(values.iloc[-1])


def _annualize_flow(series, frequency: str):
    _require_deps()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    freq = str(frequency or "A").upper()
    if s.empty:
        return s
    if freq == "TTM":
        return s.rolling(window=4, min_periods=4).sum().dropna()
    return s


def _point_in_time(series):
    _require_deps()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    return s


def _series_to_date_value_dict(series, *, limit: int = 3) -> dict[str, float]:
    _require_deps()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    if s.empty:
        return {}
    if limit > 0:
        s = s.iloc[-limit:]

    out: dict[str, float] = {}
    for idx, value in s.items():
        if hasattr(idx, "date"):
            key = idx.date().isoformat()
        else:
            key = str(idx)
        numeric = _coerce_float(value)
        if numeric is not None:
            out[key] = numeric
    return out


def _riskfree_ticker(market: str) -> str | None:
    market_u = str(market or "").upper()
    if market_u == "US":
        return "^TNX"
    if market_u == "HK":
        return "^TNX"
    if market_u == "CN":
        return "GCNY10YR.CNB"
    return "^TNX"


def _benchmark_ticker(market: str) -> str:
    market_u = str(market or "").upper()
    if market_u == "HK":
        return "^HSI"
    if market_u == "CN":
        return "000300.SS"
    return "^GSPC"


def _default_marginal_tax_rate(market: str) -> float:
    market_u = str(market or "").upper()
    return {"US": 0.21, "HK": 0.165, "CN": 0.25}.get(market_u, 0.25)


def _default_equity_risk_premium(market: str) -> float:
    market_u = str(market or "").upper()
    return {"US": 0.05, "HK": 0.055, "CN": 0.06}.get(market_u, 0.05)


def _safe_download(symbol: str, *, period: str = "2y", interval: str = "1d"):
    _require_deps()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Mean of empty slice", category=RuntimeWarning)
        try:
            return yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=False)
        except Exception:
            return pd.DataFrame()


def _compute_beta(symbol: str, benchmark: str) -> float | None:
    _require_deps()
    asset_hist = _safe_download(symbol)
    bench_hist = _safe_download(benchmark)
    asset = _history_close(asset_hist)
    bench = _history_close(bench_hist)
    if asset.empty or bench.empty:
        return None
    df = pd.concat([asset.rename("asset"), bench.rename("bench")], axis=1).dropna()
    if df.shape[0] < 60:
        return None
    rets = df.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
    if rets.shape[0] < 60:
        return None
    var = float(rets["bench"].var())
    if not isfinite(var) or var <= 1e-10:
        return None
    cov = float(rets["asset"].cov(rets["bench"]))
    beta = cov / var
    if not isfinite(beta) or abs(beta) > 5:
        return None
    return float(beta)


def _fetch_riskfree_rate(market: str) -> tuple[float | None, str | None]:
    _require_deps()
    ticker = _riskfree_ticker(market)
    if not ticker:
        return None, None
    frame = _safe_download(ticker, period="1mo", interval="1d")
    series = _history_close(frame)
    if series.empty:
        return None, None
    value = _coerce_float(series.iloc[-1])
    if value is None:
        return None, None

    if ticker in {"^TNX", "^FVX"}:
        if value >= 20:
            value = value / 1000.0
        elif value >= 1:
            value = value / 100.0
    elif ticker == "^IRX":
        if value >= 1:
            value = value / 100.0
    elif value >= 1:
        value = value / 100.0

    if value is None or value <= 0:
        return None, None
    return value, f"yahoo:{ticker}"


def _extract_latest_snapshot(ticker, statement_frequency: str, market: str) -> dict:
    _require_deps()
    freq = str(statement_frequency or "A").upper()
    use_quarterly = freq in {"Q", "TTM"}

    inc = _frame_to_df(
        ticker.quarterly_financials if use_quarterly else ticker.financials
    ).T
    bal = _frame_to_df(
        ticker.quarterly_balance_sheet if use_quarterly else ticker.balance_sheet
    ).T
    cfs = _frame_to_df(
        ticker.quarterly_cashflow if use_quarterly else ticker.cashflow
    ).T

    for frame in (inc, bal, cfs):
        if not frame.empty:
            try:
                frame.index = pd.to_datetime(frame.index)
            except Exception:
                pass
            frame.sort_index(inplace=True)

    if inc.empty and bal.empty and cfs.empty:
        raise RuntimeError("Yahoo returned empty statement frames")

    ebit = _annualize_flow(
        _syn(inc, ["Operating Income", "OperatingIncome", "Operating Income or Loss", "EBIT"]),
        freq,
    )
    da = _annualize_flow(
        _merge_series(
            _syn(cfs, ["Depreciation", "Depreciation And Amortization", "Reconciled Depreciation"]),
            _syn(cfs, ["DepreciationAmortizationDepletion", "Depreciation And Amortization"]),
        ),
        freq,
    )
    ocf = _annualize_flow(
        _merge_series(
            _syn(
                cfs,
                [
                    "Total Cash From Operating Activities",
                    "Operating Cash Flow",
                    "Net Cash Provided by Operating Activities",
                    "Net Cash Provided By Operating Activities",
                    "Cash Flow From Continuing Operating Activities",
                ],
            )
        ),
        freq,
    )
    fcf = _annualize_flow(_syn(cfs, ["Free Cash Flow", "FreeCashFlow"]), freq)

    capex = _merge_series(
        _syn(
            cfs,
            [
                "Capital Expenditures",
                "Capital Expenditure",
                "Capital Expenditure Reported",
                "Investments In Property Plant And Equipment",
                "Purchase Of PPE",
                "Net PPE Purchase And Sale",
            ],
        )
    )
    if not capex.empty:
        capex = capex.sort_index()
        capex = capex.where(capex <= 0, -capex).abs()
        capex = _annualize_flow(capex, freq)
    elif not ocf.empty and not fcf.empty:
        capex = (ocf - fcf).abs()

    tax = _annualize_flow(
        _syn(inc, ["Tax Provision", "TaxProvision", "Income Tax Expense"]),
        freq,
    )
    pretax = _annualize_flow(
        _syn(inc, ["Income Before Tax", "Pretax Income", "PretaxIncome"]),
        freq,
    )
    tax_rate = (tax / pretax).where(pretax.notna() & (pretax != 0))
    tax_rate = tax_rate.fillna(_annualize_flow(_syn(inc, ["Tax Rate For Calcs", "TaxRateForCalcs"]), freq))
    tax_rate = tax_rate.clip(lower=0.0, upper=0.6)

    cash = _point_in_time(
        _merge_series(
            _syn(bal, ["Cash And Cash Equivalents", "CashAndCashEquivalents"]),
            _syn(bal, ["Cash Cash Equivalents And Short Term Investments"]),
        )
    )
    total_debt = _point_in_time(
        _merge_series(
            _syn(bal, ["Total Debt", "Short Long Term Debt Total", "TotalDebt"]),
            _syn(bal, ["Current Debt And Capital Lease Obligation", "Current Debt"]),
        )
    )
    reported_net_debt = _point_in_time(
        _syn(bal, ["Net Debt", "NetDebt"])
    )
    current_assets = _point_in_time(
        _merge_series(
            _syn(bal, ["Total Current Assets", "TotalCurrentAssets"]),
            _syn(bal, ["Current Assets", "CurrentAssets"]),
        )
    )
    current_liabilities = _point_in_time(
        _merge_series(
            _syn(bal, ["Total Current Liabilities", "TotalCurrentLiabilities"]),
            _syn(bal, ["Current Liabilities", "CurrentLiabilities"]),
        )
    )
    short_term_debt = _point_in_time(
        _merge_series(
            _syn(bal, ["Current Debt", "CurrentDebt"]),
            _syn(bal, ["Short Term Debt", "ShortTermDebt"]),
            _syn(bal, ["Short Term Borrowings", "ShortTermBorrowings"]),
        )
    )
    short_term_investments = _point_in_time(
        _merge_series(
            _syn(bal, ["Short Term Investments", "ShortTermInvestments"]),
            _syn(bal, ["Marketable Securities", "Trading Securities"]),
        )
    )
    interest_expense = _annualize_flow(
        _syn(inc, ["Interest Expense", "InterestExpense"]),
        freq,
    )
    interest_paid = _annualize_flow(
        _syn(
            cfs,
            [
                "Interest Paid Supplemental Data",
                "Interest Paid",
                "Cash Interest Paid",
                "Interest Paid On Debt",
            ],
        ),
        freq,
    )

    op_nwc = (
        current_assets.fillna(0.0)
        - cash.reindex(current_assets.index).fillna(0.0)
        - short_term_investments.reindex(current_assets.index).fillna(0.0)
        - (
            current_liabilities.reindex(current_assets.index).fillna(0.0)
            - short_term_debt.reindex(current_assets.index).fillna(0.0)
        )
    )
    op_nwc = op_nwc.where(current_assets.notna() & current_liabilities.reindex(current_assets.index).notna())
    nwc = (
        current_assets.fillna(0.0) - current_liabilities.reindex(current_assets.index).fillna(0.0)
    ).where(current_assets.notna() & current_liabilities.reindex(current_assets.index).notna())

    delta_periods = 4 if freq == "TTM" else 1
    op_nwc_delta = op_nwc.diff(delta_periods)
    nwc_delta = nwc.diff(delta_periods)

    shares_out = None
    try:
        shares_full = ticker.get_shares_full(start=None, end=None)
        if shares_full is not None and not shares_full.empty:
            shares_out = _coerce_float(shares_full.dropna().iloc[-1])
    except Exception:
        shares_out = None
    if shares_out is None:
        try:
            fast_info = getattr(ticker, "fast_info", {}) or {}
            shares_out = _coerce_float(fast_info.get("shares"))
        except Exception:
            shares_out = None

    last_price = None
    try:
        last_hist = ticker.history(period="1mo", interval="1d", auto_adjust=False)
        prices = _history_close(last_hist)
        last_price = _coerce_float(prices.iloc[-1]) if not prices.empty else None
    except Exception:
        last_price = None
    if last_price is None:
        try:
            fast_info = getattr(ticker, "fast_info", {}) or {}
            last_price = _coerce_float(fast_info.get("lastPrice") or fast_info.get("regularMarketPrice"))
        except Exception:
            last_price = None

    latest_period = None
    for series in (ebit, da, ocf, capex, interest_paid, op_nwc_delta, nwc_delta, total_debt, cash):
        if series is not None and not series.dropna().empty:
            latest_period = series.dropna().index.max()
            break

    latest_total_debt = _latest_valid(total_debt)
    latest_cash = _latest_valid(cash)
    net_debt = None
    if latest_total_debt is not None or latest_cash is not None:
        net_debt = float((latest_total_debt or 0.0) - (latest_cash or 0.0))
    if net_debt is None:
        net_debt = _latest_valid(reported_net_debt)

    latest_interest = _latest_valid(interest_expense)
    latest_interest_paid = _latest_valid(interest_paid)
    latest_ocf = _latest_valid(ocf)
    rd = None
    if latest_interest is not None and latest_total_debt and latest_total_debt > 0:
        rd = min(abs(latest_interest) / latest_total_debt, 0.25)

    equity_weight = None
    debt_weight = None
    capital_structure_source = None
    if last_price is not None and shares_out is not None and shares_out > 0:
        market_equity = last_price * shares_out
        debt_for_weight = None
        if latest_total_debt is not None:
            debt_for_weight = max(latest_total_debt, 0.0)
            capital_structure_source = "yahoo:market_value_using_total_debt"
        elif net_debt is not None:
            debt_for_weight = max(net_debt, 0.0)
            capital_structure_source = "yahoo:market_value_using_net_debt_fallback"

        total_capital = market_equity + (debt_for_weight or 0.0)
        if total_capital > 0:
            equity_weight = market_equity / total_capital
            debt_weight = (debt_for_weight or 0.0) / total_capital

    delta_nwc = _latest_valid(op_nwc_delta)
    delta_nwc_source = "op_nwc_delta"
    if delta_nwc is None:
        delta_nwc = _latest_valid(nwc_delta)
        delta_nwc_source = "nwc_delta"
    delta_nwc_history = _merge_series(op_nwc_delta, nwc_delta)

    historical_series = {
        key: value
        for key, value in {
            "ebit": _series_to_date_value_dict(ebit),
            "ocf": _series_to_date_value_dict(ocf),
            "da": _series_to_date_value_dict(da),
            "capex": _series_to_date_value_dict(capex),
            "delta_nwc": _series_to_date_value_dict(delta_nwc_history),
            "interest_paid": _series_to_date_value_dict(interest_paid),
            "interest_expense": _series_to_date_value_dict(interest_expense),
        }.items()
        if value
    }

    currency = None
    try:
        info = ticker.get_info() or {}
        currency = info.get("currency")
    except Exception:
        currency = None

    return {
        "fundamentals": {
            "ebit": _latest_valid(ebit),
            "ocf": latest_ocf,
            "da": _latest_valid(da) or 0.0,
            "capex": _latest_valid(capex) or 0.0,
            "delta_nwc": delta_nwc,
            "delta_nwc_source": delta_nwc_source if delta_nwc is not None else None,
            "interest_paid": latest_interest_paid,
            "interest_expense": latest_interest,
            "cash": latest_cash,
            "total_debt": latest_total_debt,
            "net_debt": net_debt,
            "shares_out": shares_out,
            "historical_series": historical_series,
            "last_report_period": latest_period.date().isoformat() if latest_period is not None else None,
        },
        "assumptions": {
            "effective_tax_rate": _latest_valid(tax_rate),
            "effective_tax_rate_source": "yahoo:tax_rate",
            "marginal_tax_rate": _default_marginal_tax_rate(market),
            "marginal_tax_rate_source": "market_default",
            "pre_tax_cost_of_debt": rd,
            "pre_tax_cost_of_debt_source": "yahoo:interest_expense_over_total_debt" if rd is not None else None,
            "equity_weight": equity_weight,
            "debt_weight": debt_weight,
            "capital_structure_source": capital_structure_source if equity_weight is not None else None,
        },
        "currency": currency,
    }


def _merge_missing(target: dict, updates: dict) -> None:
    for key, value in updates.items():
        if value is None:
            continue
        if target.get(key) in (None, ""):
            target[key] = value


def fetch_yahoo_snapshot(
    ticker_symbol: str,
    *,
    market: str = "US",
    statement_frequency: str = "A",
) -> dict:
    _require_deps()
    if not ticker_symbol:
        raise ValueError("ticker is required for yahoo normalization")

    statement_frequency = str(statement_frequency or "A").upper()
    yf_symbol = _normalize_symbol(ticker_symbol, market)
    ticker = yf.Ticker(yf_symbol)
    normalized = _extract_latest_snapshot(ticker, statement_frequency, market)

    risk_free_rate, risk_free_source = _fetch_riskfree_rate(market)
    benchmark = _benchmark_ticker(market)
    beta = _compute_beta(yf_symbol, benchmark)

    assumptions = deepcopy(normalized.get("assumptions", {}))
    if risk_free_rate is not None:
        assumptions["risk_free_rate"] = risk_free_rate
        assumptions["risk_free_rate_source"] = risk_free_source
    if assumptions.get("equity_risk_premium") in (None, ""):
        assumptions["equity_risk_premium"] = _default_equity_risk_premium(market)
        assumptions["equity_risk_premium_source"] = "market_default"
    if beta is not None:
        assumptions["beta"] = beta
        assumptions["beta_source"] = f"yahoo_price_regression:{benchmark}"
    if assumptions.get("marginal_tax_rate") in (None, ""):
        assumptions["marginal_tax_rate"] = _default_marginal_tax_rate(market)
        assumptions["marginal_tax_rate_source"] = "market_default"

    return {
        "provider": "yahoo",
        "normalized_symbol": yf_symbol,
        "statement_frequency": statement_frequency,
        "currency": normalized.get("currency"),
        "fundamentals": deepcopy(normalized.get("fundamentals", {})),
        "assumptions": assumptions,
    }


def enrich_payload_from_yahoo(payload: dict, *, snapshot: dict | None = None) -> dict:
    _require_deps()
    out = deepcopy(payload)
    assumptions = out.setdefault("assumptions", {})
    fundamentals = out.setdefault("fundamentals", {})
    prefill_warnings = list(out.get("_prefill_warnings", []))
    prefill_diagnostics = list(out.get("_prefill_diagnostics", []))

    ticker_symbol = out.get("ticker")
    market = out.get("market", "US")
    if not ticker_symbol:
        raise ValueError("ticker is required for yahoo normalization")

    statement_frequency = str(out.get("statement_frequency") or "A").upper()
    provider_snapshot = snapshot or fetch_yahoo_snapshot(
        ticker_symbol,
        market=market,
        statement_frequency=statement_frequency,
    )

    _merge_missing(fundamentals, provider_snapshot.get("fundamentals", {}))
    _merge_missing(assumptions, provider_snapshot.get("assumptions", {}))

    if out.get("currency") in (None, "") and provider_snapshot.get("currency"):
        out["currency"] = provider_snapshot["currency"]

    if assumptions.get("risk_free_rate") in (None, ""):
        prefill_warnings.append("yahoo_risk_free_rate_unavailable_engine_default_will_apply")

    if assumptions.get("beta") in (None, ""):
        prefill_warnings.append("yahoo_beta_unavailable_engine_default_will_apply")

    if assumptions.get("pre_tax_cost_of_debt") in (None, ""):
        prefill_warnings.append("yahoo_cost_of_debt_unavailable_engine_default_may_apply")

    if assumptions.get("capital_structure_source") == "yahoo:market_value_using_net_debt_fallback":
        prefill_warnings.append("yahoo_total_debt_unavailable_used_net_debt_for_capital_structure")

    prefill_diagnostics.append(f"provider_normalization:yahoo:{statement_frequency}")
    out["_prefill_warnings"] = prefill_warnings
    out["_prefill_diagnostics"] = prefill_diagnostics
    out["provider"] = "yahoo"
    out["normalized_symbol"] = provider_snapshot.get("normalized_symbol") or _normalize_symbol(ticker_symbol, market)
    return out
