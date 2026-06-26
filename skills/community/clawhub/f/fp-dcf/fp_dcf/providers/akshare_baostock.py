from __future__ import annotations

from contextlib import contextmanager, redirect_stdout
from copy import deepcopy
from datetime import date, timedelta
import io
from math import isfinite

try:
    import akshare as ak
    import baostock as bs
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover - exercised in runtime environments without deps
    ak = None
    bs = None
    np = None
    pd = None


def _require_deps() -> None:
    if ak is None or bs is None or np is None or pd is None:
        raise RuntimeError(
            "CN normalization requires akshare, baostock, numpy, and pandas. "
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


def _sum_syn(df, names):
    _require_deps()
    available = [pd.to_numeric(df[name], errors="coerce") for name in names if name in df.columns]
    if not available:
        return pd.Series(dtype=float, index=df.index)
    return pd.concat(available, axis=1).sum(axis=1, min_count=1)


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


def _prepare_statement_frame(frame):
    _require_deps()
    df = _frame_to_df(frame)
    if df.empty or "报告日" not in df.columns:
        return pd.DataFrame()

    out = df.copy()
    if "类型" in out.columns:
        consolidated = out["类型"].astype(str).str.contains("合并", na=False)
        if consolidated.any():
            out = out[consolidated]

    out["报告日"] = pd.to_datetime(out["报告日"], errors="coerce")
    out = out.dropna(subset=["报告日"]).sort_values("报告日")
    out = out.drop_duplicates(subset=["报告日"], keep="first")
    return out.set_index("报告日")


def _filter_periods(df, frequency: str):
    _require_deps()
    if df.empty:
        return df
    freq = str(frequency or "A").upper()
    if freq != "A":
        return df
    annual_mask = (df.index.month == 12) & (df.index.day == 31)
    return df.loc[annual_mask] if annual_mask.any() else df


def _latest_valid(series):
    _require_deps()
    if series is None:
        return None
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return None
    return _coerce_float(values.iloc[-1])


def _convert_cumulative_to_quarterly(series):
    _require_deps()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    if s.empty:
        return s

    out: dict[pd.Timestamp, float] = {}
    cumulative_by_year: dict[tuple[int, int], float] = {}
    for idx, raw_value in s.items():
        month = int(idx.month)
        year = int(idx.year)
        value = float(raw_value)
        if month == 3:
            standalone = value
        elif month == 6:
            standalone = value - cumulative_by_year.get((year, 3), 0.0)
        elif month == 9:
            standalone = value - cumulative_by_year.get((year, 6), 0.0)
        elif month == 12:
            standalone = value - cumulative_by_year.get((year, 9), 0.0)
        else:
            standalone = value
        cumulative_by_year[(year, month)] = value
        out[idx] = standalone

    return pd.Series(out, dtype=float).sort_index()


def _annualize_flow(series, frequency: str):
    _require_deps()
    freq = str(frequency or "A").upper()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    if s.empty:
        return s
    if freq == "A":
        return s

    quarterly = _convert_cumulative_to_quarterly(s)
    if freq == "TTM":
        return quarterly.rolling(window=4, min_periods=4).sum().dropna()
    return quarterly


def _point_in_time(series, frequency: str):
    _require_deps()
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    if s.empty:
        return s
    if str(frequency or "A").upper() == "A":
        annual_mask = (s.index.month == 12) & (s.index.day == 31)
        if annual_mask.any():
            return s.loc[annual_mask]
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
        numeric = _coerce_float(value)
        if numeric is not None:
            out[idx.date().isoformat()] = numeric
    return out


def _default_marginal_tax_rate(market: str) -> float:
    market_u = str(market or "").upper()
    return {"CN": 0.25, "HK": 0.165, "US": 0.21}.get(market_u, 0.25)


def _default_equity_risk_premium(market: str) -> float:
    market_u = str(market or "").upper()
    return {"CN": 0.06, "HK": 0.055, "US": 0.05}.get(market_u, 0.05)


def _default_risk_free_rate(market: str) -> float | None:
    market_u = str(market or "").upper()
    return {"CN": 0.025, "HK": 0.04, "US": 0.04}.get(market_u, 0.04)


def _normalize_cn_symbol(symbol: str) -> dict[str, str]:
    raw = str(symbol or "").strip().upper()
    if not raw:
        raise ValueError("ticker is required for akshare_baostock normalization")

    core = raw
    prefix = ""
    if raw.startswith(("SH.", "SZ.", "BJ.")):
        prefix, core = raw.split(".", 1)
        prefix = prefix.lower()
    elif raw.startswith(("SH", "SZ", "BJ")) and len(raw) >= 8:
        prefix = raw[:2].lower()
        core = raw[2:]
    elif raw.endswith((".SS", ".SH")):
        core = raw.split(".", 1)[0]
        prefix = "sh"
    elif raw.endswith(".SZ"):
        core = raw.split(".", 1)[0]
        prefix = "sz"
    elif raw.endswith(".BJ"):
        core = raw.split(".", 1)[0]
        prefix = "bj"
    else:
        core = "".join(ch for ch in raw if ch.isdigit())
        if not core:
            raise ValueError(f"Unsupported CN ticker format: {symbol}")
        if core.startswith(("8", "4")):
            prefix = "bj"
        elif core.startswith(("5", "6", "9")):
            prefix = "sh"
        else:
            prefix = "sz"

    suffix = {"sh": "SH", "sz": "SZ", "bj": "BJ"}[prefix]
    return {
        "core": core,
        "ak_report": f"{prefix}{core}",
        "ak_info": core,
        "baostock": f"{prefix}.{core}",
        "canonical": f"{core}.{suffix}",
    }


def _history_close(frame):
    _require_deps()
    if frame is None or frame.empty:
        return pd.Series(dtype=float)
    for column in ("close", "收盘", "Close"):
        if column in frame.columns:
            return pd.to_numeric(frame[column], errors="coerce").dropna()
    return pd.Series(dtype=float)


@contextmanager
def _baostock_session():
    _require_deps()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = bs.login()
    if getattr(result, "error_code", None) != "0":
        raise RuntimeError(f"BaoStock login failed: {getattr(result, 'error_msg', 'unknown error')}")
    try:
        yield
    finally:
        with redirect_stdout(io.StringIO()):
            try:
                bs.logout()
            except Exception:
                pass


def _resultset_to_df(resultset):
    _require_deps()
    fields = list(getattr(resultset, "fields", []) or [])
    rows: list[list[str]] = []
    error_code = getattr(resultset, "error_code", None)
    error_msg = getattr(resultset, "error_msg", None)
    while error_code == "0" and resultset.next():
        rows.append(resultset.get_row_data())
        error_code = getattr(resultset, "error_code", None)
        error_msg = getattr(resultset, "error_msg", None)
    if error_code != "0":
        raise RuntimeError(f"BaoStock query failed: {error_msg}")
    return pd.DataFrame(rows, columns=fields)


def _fetch_baostock_history(
    code: str,
    *,
    start_date: str,
    end_date: str,
    adjustflag: str = "3",
):
    _require_deps()
    result = bs.query_history_k_data_plus(
        code,
        "date,code,close",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag=adjustflag,
    )
    frame = _resultset_to_df(result)
    if not frame.empty and "date" in frame.columns:
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
        frame = frame.dropna(subset=["date"]).sort_values("date")
    return frame


def _compute_beta(symbol: str, benchmark: str) -> float | None:
    _require_deps()
    end_date = date.today()
    start_date = end_date - timedelta(days=730)

    asset_hist = _fetch_baostock_history(
        symbol,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        adjustflag="2",
    )
    bench_hist = _fetch_baostock_history(
        benchmark,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        adjustflag="2",
    )
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


def _latest_close(symbol: str) -> float | None:
    _require_deps()
    end_date = date.today()
    start_date = end_date - timedelta(days=40)
    frame = _fetch_baostock_history(
        symbol,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        adjustflag="3",
    )
    closes = _history_close(frame)
    return _coerce_float(closes.iloc[-1]) if not closes.empty else None


_STOCK_INFO_SHARES_OUT_FIELDS = (
    "总股本",
    "总股本(股)",
    "总股本（股）",
    "总股本(万股)",
    "总股本（万股）",
    "总股本(亿股)",
    "总股本（亿股）",
)

_BALANCE_SHEET_SHARE_CAPITAL_FIELDS = (
    "实收资本(或股本)",
    "实收资本（或股本）",
    "股本",
)


def _resolve_shares_out_unit(raw_field: str | None) -> str:
    field_name = str(raw_field or "")
    if "万股" in field_name:
        return "万股"
    if "亿股" in field_name:
        return "亿股"
    return "股"


def _normalize_shares_out_value(value, raw_unit: str | None) -> float | None:
    shares_out = _coerce_float(value)
    if shares_out is None:
        return None

    if raw_unit == "万股":
        return shares_out * 10_000.0
    if raw_unit == "亿股":
        return shares_out * 100_000_000.0
    return shares_out


def _lookup_stock_info_shares_out(frame):
    _require_deps()
    if frame.empty or "item" not in frame.columns or "value" not in frame.columns:
        return None, None, None

    normalized_items = frame["item"].astype(str).str.strip()
    for item_name in _STOCK_INFO_SHARES_OUT_FIELDS:
        matched = frame.loc[normalized_items == item_name, "value"]
        if matched.empty:
            continue
        raw_unit = _resolve_shares_out_unit(item_name)
        shares_out = _normalize_shares_out_value(matched.iloc[0], raw_unit)
        if shares_out is not None:
            return shares_out, item_name, raw_unit

    return None, None, None


def _lookup_latest_share_capital(balance_sheet, frequency: str):
    _require_deps()
    for field_name in _BALANCE_SHEET_SHARE_CAPITAL_FIELDS:
        share_capital = _latest_valid(
            _point_in_time(
                _syn(balance_sheet, [field_name]),
                frequency,
            )
        )
        if share_capital is not None:
            return share_capital, field_name, "股"
    return None, None, None


def _resolve_shares_out_with_source(
    stock_info,
    balance_sheet,
    frequency: str,
) -> tuple[float | None, str | None, str | None, str | None]:
    _require_deps()

    shares_out, raw_field, raw_unit = _lookup_stock_info_shares_out(_frame_to_df(stock_info))
    if shares_out is not None:
        return shares_out, "akshare:stock_individual_info_em", raw_field, raw_unit

    shares_out, raw_field, raw_unit = _lookup_latest_share_capital(balance_sheet, frequency)
    if shares_out is not None:
        return shares_out, "akshare:balance_sheet_share_capital", raw_field, raw_unit

    return None, None, None, None


def _extract_latest_snapshot(
    income_statement,
    balance_sheet,
    cash_flow_statement,
    stock_info,
    *,
    statement_frequency: str,
    market: str,
    baostock_symbol: str,
) -> dict:
    _require_deps()
    freq = str(statement_frequency or "A").upper()
    diagnostics: list[str] = []

    inc = _prepare_statement_frame(income_statement)
    bal = _prepare_statement_frame(balance_sheet)
    cfs = _prepare_statement_frame(cash_flow_statement)
    if inc.empty and bal.empty and cfs.empty:
        raise RuntimeError("AkShare returned empty statement frames")

    inc_filtered = _filter_periods(inc, freq)
    bal_filtered = _filter_periods(bal, freq)
    cfs_filtered = _filter_periods(cfs, freq)

    ebit = _annualize_flow(
        _merge_series(
            _syn(inc_filtered, ["息税前利润"]),
            _syn(inc_filtered, ["营业利润"]),
        ),
        freq,
    )
    da = _annualize_flow(
        _merge_series(
            _syn(cfs_filtered, ["固定资产折旧、油气资产折耗、生产性生物资产折旧"]),
            _syn(cfs_filtered, ["无形资产摊销"]),
            _syn(cfs_filtered, ["长期待摊费用摊销"]),
        ),
        freq,
    )
    ocf = _annualize_flow(
        _syn(cfs_filtered, ["经营活动产生的现金流量净额"]),
        freq,
    )
    capex = _annualize_flow(
        _syn(cfs_filtered, ["购建固定资产、无形资产和其他长期资产所支付的现金"]),
        freq,
    )
    if not capex.empty:
        capex = capex.abs()

    tax = _annualize_flow(_syn(inc_filtered, ["所得税费用"]), freq)
    pretax = _annualize_flow(_syn(inc_filtered, ["利润总额"]), freq)
    tax_rate = (tax / pretax).where(pretax.notna() & (pretax != 0)).clip(lower=0.0, upper=0.6)

    cash = _point_in_time(_syn(bal_filtered, ["货币资金"]), freq)
    total_debt = _point_in_time(
        _sum_syn(
            bal_filtered,
            [
                "短期借款",
                "一年内到期的非流动负债",
                "长期借款",
                "应付债券",
                "长期应付款合计",
                "长期应付款",
                "租赁负债",
            ],
        ),
        freq,
    )
    current_assets = _point_in_time(
        _merge_series(
            _syn(bal_filtered, ["流动资产合计"]),
            _syn(bal_filtered, ["流动资产"]),
        ),
        freq,
    )
    current_liabilities = _point_in_time(
        _merge_series(
            _syn(bal_filtered, ["流动负债合计"]),
            _syn(bal_filtered, ["流动负债"]),
        ),
        freq,
    )
    short_term_debt = _point_in_time(
        _sum_syn(bal_filtered, ["短期借款", "一年内到期的非流动负债"]),
        freq,
    )
    short_term_investments = _point_in_time(
        _syn(bal_filtered, ["交易性金融资产"]),
        freq,
    )
    interest_expense = _annualize_flow(
        _merge_series(
            _syn(inc_filtered, ["利息费用"]).abs(),
            _syn(inc_filtered, ["利息支出"]).abs(),
            _syn(inc_filtered, ["财务费用"]).where(_syn(inc_filtered, ["财务费用"]) > 0),
        ),
        freq,
    )
    interest_paid = _annualize_flow(
        _merge_series(
            _syn(cfs_filtered, ["支付利息、手续费及佣金的现金"]).abs(),
            _syn(cfs_filtered, ["分配股利、利润或偿付利息所支付的现金"]).abs(),
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
    ).where(current_assets.notna() & current_liabilities.reindex(current_assets.index).notna())
    nwc = (
        current_assets.fillna(0.0) - current_liabilities.reindex(current_assets.index).fillna(0.0)
    ).where(current_assets.notna() & current_liabilities.reindex(current_assets.index).notna())

    delta_periods = 4 if freq == "TTM" else 1
    op_nwc_delta = op_nwc.diff(delta_periods)
    nwc_delta = nwc.diff(delta_periods)

    shares_out, shares_out_source, shares_out_raw_field, shares_out_raw_unit = (
        _resolve_shares_out_with_source(stock_info, bal_filtered, freq)
    )
    if shares_out is None:
        diagnostics.append("shares_out_unresolved_akshare_baostock")
        diagnostics.append("capital_structure_source_unavailable_due_to_missing_shares_out")
    last_price = _latest_close(baostock_symbol)

    latest_total_debt = _latest_valid(total_debt)
    latest_cash = _latest_valid(cash)
    net_debt = None
    if latest_total_debt is not None or latest_cash is not None:
        net_debt = float((latest_total_debt or 0.0) - (latest_cash or 0.0))

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
            capital_structure_source = "akshare_baostock:market_value_using_total_debt"
        elif net_debt is not None:
            debt_for_weight = max(net_debt, 0.0)
            capital_structure_source = "akshare_baostock:market_value_using_net_debt_fallback"

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

    latest_period = None
    for series in (ebit, da, ocf, capex, interest_paid, op_nwc_delta, total_debt, cash):
        if series is not None and not series.dropna().empty:
            latest_period = series.dropna().index.max()
            break

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

    benchmark = "sh.000300"
    beta = _compute_beta(baostock_symbol, benchmark)

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
            "shares_out_source": shares_out_source,
            "shares_out_raw_field": shares_out_raw_field,
            "shares_out_raw_unit": shares_out_raw_unit,
            "historical_series": historical_series,
            "last_report_period": latest_period.date().isoformat() if latest_period is not None else None,
        },
        "assumptions": {
            "risk_free_rate": _default_risk_free_rate(market),
            "risk_free_rate_source": "market_default_cn",
            "equity_risk_premium": _default_equity_risk_premium(market),
            "equity_risk_premium_source": "market_default",
            "beta": beta,
            "beta_source": f"baostock_price_regression:{benchmark}" if beta is not None else None,
            "effective_tax_rate": _latest_valid(tax_rate),
            "effective_tax_rate_source": "akshare:tax_rate",
            "marginal_tax_rate": _default_marginal_tax_rate(market),
            "marginal_tax_rate_source": "market_default",
            "pre_tax_cost_of_debt": rd,
            "pre_tax_cost_of_debt_source": (
                "akshare:interest_expense_over_total_debt" if rd is not None else None
            ),
            "equity_weight": equity_weight,
            "debt_weight": debt_weight,
            "capital_structure_source": capital_structure_source if equity_weight is not None else None,
        },
        "currency": "CNY",
        "diagnostics": diagnostics,
    }


def _merge_missing(target: dict, updates: dict) -> None:
    for key, value in updates.items():
        if value is None:
            continue
        if target.get(key) in (None, ""):
            target[key] = value


def fetch_akshare_baostock_snapshot(
    ticker_symbol: str,
    *,
    market: str = "CN",
    statement_frequency: str = "A",
) -> dict:
    _require_deps()
    market_u = str(market or "CN").upper()
    if market_u != "CN":
        raise ValueError("akshare_baostock normalization currently supports market=CN only")

    symbols = _normalize_cn_symbol(ticker_symbol)
    stock_info = pd.DataFrame()
    if hasattr(ak, "stock_individual_info_em"):
        try:
            stock_info = ak.stock_individual_info_em(symbol=symbols["ak_info"])
        except Exception:
            stock_info = pd.DataFrame()
    with _baostock_session():
        normalized = _extract_latest_snapshot(
            ak.stock_financial_report_sina(stock=symbols["ak_report"], symbol="利润表"),
            ak.stock_financial_report_sina(stock=symbols["ak_report"], symbol="资产负债表"),
            ak.stock_financial_report_sina(stock=symbols["ak_report"], symbol="现金流量表"),
            stock_info,
            statement_frequency=statement_frequency,
            market=market_u,
            baostock_symbol=symbols["baostock"],
        )

    assumptions = deepcopy(normalized.get("assumptions", {}))
    if assumptions.get("marginal_tax_rate") in (None, ""):
        assumptions["marginal_tax_rate"] = _default_marginal_tax_rate(market_u)
        assumptions["marginal_tax_rate_source"] = "market_default"
    if assumptions.get("equity_risk_premium") in (None, ""):
        assumptions["equity_risk_premium"] = _default_equity_risk_premium(market_u)
        assumptions["equity_risk_premium_source"] = "market_default"
    if assumptions.get("risk_free_rate") in (None, ""):
        assumptions["risk_free_rate"] = _default_risk_free_rate(market_u)
        assumptions["risk_free_rate_source"] = "market_default_cn"

    return {
        "provider": "akshare_baostock",
        "normalized_symbol": symbols["canonical"],
        "statement_frequency": str(statement_frequency or "A").upper(),
        "currency": normalized.get("currency"),
        "fundamentals": deepcopy(normalized.get("fundamentals", {})),
        "assumptions": assumptions,
        "diagnostics": list(normalized.get("diagnostics", [])),
    }


def enrich_payload_from_akshare_baostock(payload: dict, *, snapshot: dict | None = None) -> dict:
    _require_deps()
    out = deepcopy(payload)
    assumptions = out.setdefault("assumptions", {})
    fundamentals = out.setdefault("fundamentals", {})
    prefill_warnings = list(out.get("_prefill_warnings", []))
    prefill_diagnostics = list(out.get("_prefill_diagnostics", []))

    ticker_symbol = out.get("ticker")
    market = out.get("market", "CN")
    if not ticker_symbol:
        raise ValueError("ticker is required for akshare_baostock normalization")

    statement_frequency = str(out.get("statement_frequency") or "A").upper()
    provider_snapshot = snapshot or fetch_akshare_baostock_snapshot(
        ticker_symbol,
        market=market,
        statement_frequency=statement_frequency,
    )

    _merge_missing(fundamentals, provider_snapshot.get("fundamentals", {}))
    _merge_missing(assumptions, provider_snapshot.get("assumptions", {}))

    if out.get("currency") in (None, "") and provider_snapshot.get("currency"):
        out["currency"] = provider_snapshot["currency"]

    if assumptions.get("risk_free_rate") in (None, ""):
        prefill_warnings.append("akshare_baostock_risk_free_rate_unavailable_engine_default_will_apply")
    if assumptions.get("beta") in (None, ""):
        prefill_warnings.append("akshare_baostock_beta_unavailable_engine_default_will_apply")
    if assumptions.get("pre_tax_cost_of_debt") in (None, ""):
        prefill_warnings.append("akshare_baostock_cost_of_debt_unavailable_engine_default_may_apply")
    if assumptions.get("capital_structure_source") == "akshare_baostock:market_value_using_net_debt_fallback":
        prefill_warnings.append("akshare_baostock_total_debt_unavailable_used_net_debt_for_capital_structure")
    for diagnostic in provider_snapshot.get("diagnostics", []):
        if diagnostic not in prefill_diagnostics:
            prefill_diagnostics.append(diagnostic)

    prefill_diagnostics.append(f"provider_normalization:akshare_baostock:{statement_frequency}")
    out["_prefill_warnings"] = prefill_warnings
    out["_prefill_diagnostics"] = prefill_diagnostics
    out["provider"] = "akshare_baostock"
    out["normalized_symbol"] = provider_snapshot.get("normalized_symbol")
    return out
