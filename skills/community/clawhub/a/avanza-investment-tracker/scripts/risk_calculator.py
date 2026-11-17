import shutil
import os
import time
import math
import logging
import calendar
import bisect
import urllib.parse
from collections import defaultdict
import requests
from datetime import date, datetime
from data_parser import DataParser, SpecialCases
from database_handler import DatabaseHandler

class HistoricalTracker(DataParser):
    """
    Subclass of DataParser that tracks and records historical cash balances
    and asset holdings chronologically during the transaction processing loop.
    """
    def __init__(self, db: DatabaseHandler, cohorts_start=None, cohorts_end=None, special_cases=None):
        super().__init__(db, special_cases)
        self.cohorts_start = cohorts_start
        self.cohorts_end = cohorts_end
        # Map date -> { 'cash': {account: amount}, 'assets': {account: {asset_id: amount}} }
        self.history = {}
        self.max_date_processed = None

    def get_current_state(self):
        """Query database tables to construct the current snapshot of cash and assets."""
        query_cash = "SELECT account, SUM(capital) FROM cohort_data"
        params_cash = []
        if self.cohorts_start or self.cohorts_end:
            query_cash += " WHERE 1=1"
            if self.cohorts_start:
                query_cash += " AND month >= ?"
                params_cash.append(self.cohorts_start.isoformat())
            if self.cohorts_end:
                query_cash += " AND month <= ?"
                params_cash.append(self.cohorts_end.isoformat())
        query_cash += " GROUP BY account"
        self.data_cur.execute(query_cash, params_cash)
        cash = {row[0]: row[1] for row in self.data_cur.fetchall()}

        query_assets = "SELECT account, asset_id, SUM(amount) FROM cohort_assets WHERE amount > 0"
        params_assets = []
        if self.cohorts_start or self.cohorts_end:
            if self.cohorts_start:
                query_assets += " AND month >= ?"
                params_assets.append(self.cohorts_start.isoformat())
            if self.cohorts_end:
                query_assets += " AND month <= ?"
                params_assets.append(self.cohorts_end.isoformat())
        query_assets += " GROUP BY account, asset_id"
        self.data_cur.execute(query_assets, params_assets)
        assets = {}
        for account, asset_id, amount in self.data_cur.fetchall():
            if account not in assets:
                assets[account] = {}
            assets[account][asset_id] = amount
            
        return {
            'cash': cash,
            'assets': assets
        }

    def _on_transaction_processed(self, row: tuple) -> None:
        """
        Snapshot holdings after each transaction. Only the last state of each
        date is kept (later transactions on the same date overwrite it).
        """
        t_date_str = row[0]
        if isinstance(t_date_str, str):
            t_date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        else:
            t_date = t_date_str
        if self.max_date_processed is None or t_date >= self.max_date_processed:
            self.max_date_processed = t_date
            self.history[t_date] = self.get_current_state()


def generate_monthly_dates(start_date: date, end_date: date) -> list:
    """Generate monthly end-of-month dates between start_date and end_date."""
    dates = []
    # Start with the end of the month prior to start_date
    if start_date.month == 1:
        prev_month_end = date(start_date.year - 1, 12, 31)
    else:
        prev_month_end = date(
            start_date.year,
            start_date.month - 1,
            calendar.monthrange(start_date.year, start_date.month - 1)[1]
        )
    dates.append(prev_month_end)
    
    curr = start_date
    while True:
        last_day = calendar.monthrange(curr.year, curr.month)[1]
        month_end = date(curr.year, curr.month, last_day)
        
        if month_end >= end_date:
            break
            
        dates.append(month_end)
        
        if curr.month == 12:
            curr = date(curr.year + 1, 1, 1)
        else:
            curr = date(curr.year, curr.month + 1, 1)
            
    dates.append(end_date)
    
    # Remove duplicates
    unique_dates = []
    for d in dates:
        if d not in unique_dates:
            unique_dates.append(d)
            
    return unique_dates


def get_holdings_at_date(history: dict, target_date: date, accounts_filter: list) -> tuple:
    """Find the holdings (cash and asset shares) as of a target date."""
    tx_dates = sorted(history.keys())
    idx = bisect.bisect_right(tx_dates, target_date)
    
    if idx == 0:
        return 0.0, {}
        
    d = tx_dates[idx - 1]
    state = history[d]
    
    cash = 0.0
    for acc, val in state['cash'].items():
        if accounts_filter is None or acc in accounts_filter:
            cash += val
            
    assets_shares = {}
    for acc, assets in state['assets'].items():
        if accounts_filter is None or acc in accounts_filter:
            for asset_id, amount in assets.items():
                assets_shares[asset_id] = assets_shares.get(asset_id, 0.0) + amount
                
    return cash, assets_shares


def fetch_riksbanken_rate(from_date: date, to_date: date) -> float:
    """
    Fetch the average repo rate (policy rate) from Riksbanken SWEA API.
    Fallback to 2.0% (0.02) if offline or call fails.

    Raw daily observations are cached for the widest range seen so far; a
    request whose [from_date, to_date] falls within the cached range is
    answered by filtering cached observations (no HTTP). This makes the
    N-cohort case (e.g. --risk over many monthly cohorts, each with a
    different from_date but the same to_date) issue a single HTTP call for
    the widest cohort rather than one per cohort.
    """
    cache = fetch_riksbanken_rate._cache
    cached_from = cache.get('from')
    cached_to = cache.get('to')
    observations = cache.get('observations', [])

    if (cached_from is not None
            and from_date >= cached_from
            and to_date <= cached_to):
        # Sub-range of the cached observations: filter and average locally.
        relevant = [obs['value'] for obs in observations
                    if from_date <= obs['date'] <= to_date]
        if relevant:
            return (sum(relevant) / len(relevant)) / 100.0
        return 0.02

    # Need to fetch. Widen the requested range to cover any previously cached
    # range so subsequent sub-range requests still hit the cache.
    fetch_from = from_date if cached_from is None else min(from_date, cached_from)
    fetch_to = to_date if cached_to is None else max(to_date, cached_to)
    url = f"https://api.riksbank.se/swea/v1/Observations/SECBREPOEFF/{fetch_from.isoformat()}/{fetch_to.isoformat()}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json"
    }
    result = 0.02
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                parsed = []
                for obs in data:
                    if 'value' in obs and 'date' in obs:
                        obs_date_str = obs['date']
                        try:
                            obs_date = datetime.strptime(obs_date_str, "%Y-%m-%d").date()
                        except (ValueError, TypeError):
                            continue
                        parsed.append({'date': obs_date, 'value': float(obs['value'])})
                if parsed:
                    cache['from'] = fetch_from
                    cache['to'] = fetch_to
                    cache['observations'] = parsed
                    relevant = [obs['value'] for obs in parsed
                                if from_date <= obs['date'] <= to_date]
                    if relevant:
                        result = (sum(relevant) / len(relevant)) / 100.0
    except Exception as e:
        logging.debug(f"Failed to fetch Riksbanken policy rate: {e}")
    return result

fetch_riksbanken_rate._cache = {}


def clear_riksbanken_cache():
    """Clear the Riksbanken rate observation cache (used by tests)."""
    fetch_riksbanken_rate._cache.clear()


def fetch_yahoo_benchmark_prices(ticker: str, start_date: date, end_date: date) -> list:
    """Fetch daily closing prices for a benchmark ticker from Yahoo Finance."""
    encoded_ticker = urllib.parse.quote(ticker)
    start_ts = int(time.mktime(start_date.timetuple()))
    end_ts = int(time.mktime(end_date.timetuple()))
    
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded_ticker}?period1={start_ts}&period2={end_ts}&interval=1d"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                res = result[0]
                timestamps = res.get("timestamp", [])
                indicators = res.get("indicators", {})
                
                adjclose_list = indicators.get("adjclose", [{}])[0].get("adjclose", [])
                close_list = indicators.get("quote", [{}])[0].get("close", [])
                prices = adjclose_list if adjclose_list else close_list
                
                bench_prices = []
                for ts, price in zip(timestamps, prices):
                    if price is not None:
                        dt = date.fromtimestamp(ts)
                        bench_prices.append((dt, float(price)))
                return sorted(bench_prices, key=lambda x: x[0])
        else:
            logging.warning(f"Failed to fetch Yahoo Finance benchmark prices for {ticker} (Status: {r.status_code})")
    except Exception as e:
        logging.warning(f"Failed to fetch Yahoo Finance benchmark prices for {ticker}: {e}")
    return []


def get_benchmark_price(bench_prices: list, target_date: date) -> float:
    """Get the benchmark price closest to or on the target date."""
    if not bench_prices:
        return 0.0
    dates = [x[0] for x in bench_prices]
    idx = bisect.bisect_right(dates, target_date)
    if idx == 0:
        return bench_prices[0][1]
    return bench_prices[idx - 1][1]


class RiskCalculator:
    """Reconstructs portfolio history and calculates risk metrics."""
    def __init__(self, db: DatabaseHandler, accounts=None, from_date=None, to_date=None, 
                 cohorts_start=None, cohorts_end=None, beta_ticker=None, interpolate=True):
        self.db = db
        self.accounts = accounts if accounts is not None else 'all'
        self.from_date = from_date
        self.to_date = to_date
        self.cohorts_start = cohorts_start
        self.cohorts_end = cohorts_end
        self.beta_ticker = beta_ticker
        self.interpolate = interpolate

    def calculate(self, portfolio_apy: float) -> dict:
        """Perform the chronological reconstruction and calculate all metrics.

        portfolio_apy is the annualized return (as a fraction, e.g. 0.07 for 7%)
        for the period/scope under evaluation. It is computed once by the caller
        (cli.stats) so the risk metrics and the displayed APY stay consistent.
        """
        from cli import resolve_accounts
        cur = self.db.get_cursor()
        
        accounts_list = resolve_accounts(self.db, self.accounts)
        
        # 1. Resolve date bounds
        to_date = self.to_date
        if to_date is None:
            to_date = date.today()
        elif isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            
        from_date = self.from_date
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            
        if from_date is None:
            if self.cohorts_start is not None:
                from_date = self.cohorts_start
            else:
                if accounts_list:
                    placeholders = ",".join("?" for _ in accounts_list)
                    query = f"SELECT MIN(date) FROM transactions WHERE account IN ({placeholders})"
                    cur.execute(query, accounts_list)
                else:
                    cur.execute("SELECT MIN(date) FROM transactions")
                row = cur.fetchone()
                first_tx_date = row[0] if row else None
                if first_tx_date:
                    if isinstance(first_tx_date, str):
                        from_date = datetime.strptime(first_tx_date, "%Y-%m-%d").date()
                    else:
                        from_date = first_tx_date
                else:
                    from_date = date(2018, 1, 1)

        # Ensure correct date order
        if from_date > to_date:
            raise ValueError(f"Start date {from_date} cannot be after end date {to_date}")

        # 2. Reconstruct historical holdings state
        history, cf_by_month = self.get_historical_holdings(to_date)
        sampling_dates = generate_monthly_dates(from_date, to_date)
        
        # 3. Calculate portfolio values at each monthly end date
        portfolio_values = []
        for t in sampling_dates:
            cash, assets_shares = get_holdings_at_date(history, t, accounts_list)
            asset_value = 0.0
            for asset_id, shares in assets_shares.items():
                if shares > 0.0001:
                    price, _, _, _ = self.db.get_price(asset_id, t, interpolate=self.interpolate)
                    if price is not None and price > 0:
                        asset_value += shares * price
            portfolio_values.append(cash + asset_value)

        # 3b. Trim leading zero-value months (common when evaluating specific
        # cohorts or recently opened accounts). Cash flows that predate the
        # new start are reassigned to the first period (section 4) so they
        # are not lost.
        first_val_idx = None
        for idx, val in enumerate(portfolio_values):
            if val > 0.01:
                first_val_idx = idx
                break
        if first_val_idx is not None and first_val_idx > 0:
            start_slice = first_val_idx - 1
            sampling_dates = sampling_dates[start_slice:]
            portfolio_values = portfolio_values[start_slice:]

        # 4. Build cash flows with correct timing AND correct cohort scoping.
        #    Deposits: raw transactions with actual dates, filtered by
        #    allocation month for cohort membership.
        #    Withdrawals: cohort_data.withdrawal (correctly scoped — large
        #    withdrawals that pull pre-cohort capital are excluded by the
        #    cohort system), approximated at mid-month for timing.
        cash_flows_by_date = defaultdict(float)

        # Build cash flows from raw transactions with actual dates.
        # Deposits (Insättning etc.) are always included. For non-cohort
        # mode, Uttag (withdrawals) are also included directly. For cohort
        # mode, withdrawals come from cf_by_month (below) which has correct
        # transaction-month timing from cohort_cash_flows.
        if accounts_list:
            placeholders = ",".join("?" for _ in accounts_list)
            query = (f"SELECT date, transaction_type, total, amount, price "
                     f"FROM transactions "
                     f"WHERE date > ? AND date <= ? AND account IN ({placeholders})")
            params = [sampling_dates[0].isoformat(), to_date.isoformat()] + accounts_list
        else:
            query = ("SELECT date, transaction_type, total, amount, price "
                     "FROM transactions WHERE date > ? AND date <= ?")
            params = [sampling_dates[0].isoformat(), to_date.isoformat()]

        is_cohort = self.cohorts_start is not None or self.cohorts_end is not None

        # For cohort mode: collect Uttag transactions by allocation month,
        # so cf_by_month amounts can be distributed across actual transaction
        # dates (see below) instead of allocation months.
        uttag_by_alloc = defaultdict(list)  # alloc_month_date -> [(tx_date, total)]

        cur.execute(query, params)
        for date_str, tx_type, total, amount, price in cur.fetchall():
            if isinstance(date_str, str):
                tx_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                tx_date = date_str

            # For cohort mode, only include transactions whose allocation
            # month is within the cohort range.
            if is_cohort:
                am = DataParser.allocate_to_month(tx_date)
                if self.cohorts_start is not None and am < self.cohorts_start:
                    continue
                if self.cohorts_end is not None and am > self.cohorts_end:
                    continue
                # Collect Uttag for proportional distribution of cf_by_month
                if tx_type == "Uttag":
                    uttag_by_alloc[am].append((tx_date, total))

            if tx_type in ("Insättning", "Autogiroinsättning", "Intern överföring"):
                cash_flows_by_date[tx_date] += total
            elif tx_type == "Tillgångsinsättning":
                cash_flows_by_date[tx_date] += amount * price
            elif tx_type == "Uttag" and not is_cohort:
                # Non-cohort: withdrawals from raw transactions directly.
                cash_flows_by_date[tx_date] += total

        # Cohort cash flows (withdrawals, fees, taxes) from cohort_cash_flows.
        # Distribute across actual Uttag transaction dates proportionally so
        # that Modified Dietz time-weighting uses when the cash flow actually
        # occurred, not the allocation month (which can differ by up to 10
        # days due to the cutoff). For months with no Uttag (fees only),
        # use mid-month approximation.
        if is_cohort:
            for m_str, cf_amt in cf_by_month.items():
                m_date = datetime.strptime(m_str, "%Y-%m-%d").date() if isinstance(m_str, str) else m_str
                uttags = uttag_by_alloc.get(m_date, [])
                raw_total = sum(t for _, t in uttags)
                if uttags and abs(raw_total) > 0.01:
                    for tx_date, tx_total in uttags:
                        cash_flows_by_date[tx_date] += cf_amt * (tx_total / raw_total)
                else:
                    # No Uttag for this allocation month — fees only
                    cf_date = date(m_date.year, m_date.month, 15)
                    cash_flows_by_date[cf_date] += cf_amt

        # Assign cash flows to sampling periods, keeping (date, amount) pairs
        # for Modified Dietz time-weighting.
        period_cash_flows = []  # per period: list of (date, amount)
        for i in range(1, len(sampling_dates)):
            t_start = sampling_dates[i-1]
            t_end = sampling_dates[i]
            flows = []
            for d, cf in cash_flows_by_date.items():
                if i == 1:
                    if t_start <= d <= t_end:
                        flows.append((d, cf))
                else:
                    if t_start < d <= t_end:
                        flows.append((d, cf))
            period_cash_flows.append(flows)

        # 5. Compute monthly returns using Modified Dietz.
        #    r = (v_end - v_start - cf_total) / (v_start + Σ(w_i · cf_i))
        #    where w_i = (t_end - d_i) / (t_end - t_start) time-weights each
        #    cash flow by how much of the period it was invested. This handles
        #    large cash flows into small balances gracefully (the original
        #    simple-Dietz formula exploded when cf dominated v_start).
        returns = []
        for i in range(1, len(sampling_dates)):
            v_start = portfolio_values[i-1]
            v_end = portfolio_values[i]
            flows = period_cash_flows[i-1]
            t_start = sampling_dates[i-1]
            t_end = sampling_dates[i]
            period_len = (t_end - t_start).days

            cf_total = sum(amt for _, amt in flows)

            if v_start > 0.01 and period_len > 0:
                weighted_cf = sum(
                    amt * (t_end - d).days / period_len for d, amt in flows
                )
                denominator = v_start + weighted_cf
                # Modified Dietz requires positive average capital. A negative
                # denominator means withdrawals exceeded deposits on a time-
                # weighted basis (e.g. a large withdrawal followed by a large
                # transfer-in within the same period). The return is undefined
                # in this case — set to 0 rather than producing a misleading
                # value.
                if denominator > 0.01:
                    r = (v_end - v_start - cf_total) / denominator
                else:
                    r = 0.0
            elif period_len > 0 and v_start <= 0.01:
                # Leading period with no starting capital: use weighted cf
                # as the denominator (all return is on the deposited capital).
                weighted_cf = sum(
                    amt * (t_end - d).days / period_len for d, amt in flows
                )
                if weighted_cf > 0.01:
                    r = (v_end - v_start - cf_total) / weighted_cf
                else:
                    r = 0.0
            else:
                r = 0.0
            returns.append(r)

        # 6. Fetch Risk-Free Rate
        rf_rate = fetch_riksbanken_rate(from_date, to_date)
        
        # 7. Overall return (APY) is provided by the caller to ensure the risk
        # metrics use the same APY figure that is displayed in the stats table.
        overall_return = portfolio_apy

        # 8. Calculate risk metrics.
        # The numerator uses the caller-supplied annualized return (APY) so the
        # ratios stay consistent with the APY shown in the stats table; the
        # denominator is the annualized volatility of the monthly Modified
        # Dietz returns computed above. The two come from different return
        # series by design (display consistency over theoretical purity).
        n = len(returns)
        if n < 2:
            annualized_stddev = 0.0
            sharpe = 0.0
            sortino = 0.0
        else:
            # Variance is shift-invariant, so using raw returns here is
            # numerically equivalent to using (r - rf_monthly) excess returns.
            mean_r = sum(returns) / n
            variance = sum((r - mean_r) ** 2 for r in returns) / (n - 1)
            stddev = math.sqrt(variance)
            annualized_stddev = stddev * math.sqrt(12)

            if annualized_stddev > 0.0001:
                sharpe = (overall_return - rf_rate) / annualized_stddev
            else:
                sharpe = 0.0

            # Sortino measures downside deviation relative to the monthly
            # risk-free rate as the minimum acceptable return (MAR).
            rf_monthly = rf_rate / 12.0
            downside_diffs = [min(r - rf_monthly, 0.0) for r in returns]
            downside_variance = sum(diff ** 2 for diff in downside_diffs) / (n - 1)
            downside_stddev = math.sqrt(downside_variance)
            annualized_downside_stddev = downside_stddev * math.sqrt(12)

            if annualized_downside_stddev > 0.0001:
                sortino = (overall_return - rf_rate) / annualized_downside_stddev
            else:
                sortino = 0.0

        # 9. Maximum Drawdown (cumulative return index). The index is floored
        # at a tiny positive value as a safety net so drawdown is always
        # strictly less than 100%.
        max_dd = 0.0
        peak = 1.0
        peak_date = sampling_dates[0]
        trough_date = None
        current_peak_date = sampling_dates[0]

        index_value = 1.0
        index_points = [(sampling_dates[0], 1.0)]
        for i, r in enumerate(returns):
            index_value *= (1.0 + r)
            if index_value < 1e-9:
                index_value = 1e-9
            index_points.append((sampling_dates[i+1], index_value))

        for dt, val in index_points:
            if val > peak:
                peak = val
                current_peak_date = dt
            if peak > 1e-9:
                dd = (peak - val) / peak
                if dd > max_dd:
                    max_dd = dd
                    peak_date = current_peak_date
                    trough_date = dt

        # 10. Beta vs benchmark
        beta = None
        if self.beta_ticker:
            bench_prices = fetch_yahoo_benchmark_prices(self.beta_ticker, sampling_dates[0], to_date)
            if bench_prices:
                bench_values = [get_benchmark_price(bench_prices, t) for t in sampling_dates]
                bench_returns = []
                for i in range(1, len(sampling_dates)):
                    b_start = bench_values[i-1]
                    b_end = bench_values[i]
                    if b_start > 0.0001:
                        r_bench = (b_end - b_start) / b_start
                    else:
                        r_bench = 0.0
                    bench_returns.append(r_bench)

                if len(returns) >= 2 and len(bench_returns) >= 2:
                    mean_bench = sum(bench_returns) / len(bench_returns)
                    mean_port = sum(returns) / len(returns)

                    covariance = sum((r_p - mean_port) * (r_b - mean_bench) for r_p, r_b in zip(returns, bench_returns)) / (len(returns) - 1)
                    variance_bench = sum((r_b - mean_bench) ** 2 for r_b in bench_returns) / (len(bench_returns) - 1)

                    if variance_bench > 1e-8:
                        beta = covariance / variance_bench

        # 11. Returns by Calendar Year. Compound the monthly Modified Dietz
        #     returns whose period ends in each year. This links the same
        #     per-period series used for volatility and drawdown, so yearly
        #     figures stay consistent with the rest of the metrics and robust
        #     to large intra-year cash flows (a full-year simple Dietz would
        #     mis-weight mid-year flows).
        year_returns = {}
        for i, r in enumerate(returns):
            y = sampling_dates[i + 1].year
            year_returns[y] = year_returns.get(y, 1.0) * (1.0 + r)
        year_returns = {y: v - 1.0 for y, v in year_returns.items()}

        return {
            'period_start': sampling_dates[0],
            'period_end': to_date,
            'annualized_return': overall_return,
            'annualized_stddev': annualized_stddev,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'max_drawdown': max_dd,
            'max_drawdown_peak': peak_date,
            'max_drawdown_trough': trough_date,
            'beta': beta,
            'risk_free_rate': rf_rate,
            'year_returns': year_returns
        }

    def get_historical_holdings(self, end_date: date) -> dict:
        """Run transaction parser chronologically in a temporary DB and capture holdings."""
        db_file = self.db.db_file
        temp_db_path = f"{db_file}_temp_risk_{int(time.time())}_{id(self)}.db"
        shutil.copy2(db_file, temp_db_path)
        
        temp_db = DatabaseHandler(temp_db_path)
        temp_db.interpolate = self.interpolate
        temp_db.connect()
        
        temp_cur = temp_db.get_cursor()
        
        # We delete transactions after end_date to avoid parsing future events
        temp_cur.execute("DELETE FROM transactions WHERE date > ?", (end_date.isoformat(),))
        
        temp_db.reset_table("cohort_data")
        temp_db.reset_table("cohort_assets")
        temp_db.reset_table("cohort_cash_flows")
        temp_db.reset_table("assets")
        temp_cur.execute("UPDATE transactions SET processed = 0")
        temp_db.commit()
        
        special_cases_path = "data/special_cases.json"
        special_cases = SpecialCases(special_cases_path) if os.path.exists(special_cases_path) else None
        
        tracker = HistoricalTracker(temp_db, self.cohorts_start, self.cohorts_end, special_cases)
        try:
            tracker.process_transactions(raise_on_unprocessed=False)
            history = tracker.history

            # Query cohort-specific cash flows (withdrawals, fees, taxes).
            # Keyed by transaction_month so the caller can distribute each
            # month's total across the actual Uttag transaction dates for
            # Modified Dietz time-weighting.
            cur = temp_db.get_cursor()
            query_cf = "SELECT transaction_month, SUM(amount) FROM cohort_cash_flows"
            params_cf = []
            if self.cohorts_start or self.cohorts_end:
                query_cf += " WHERE 1=1"
                if self.cohorts_start:
                    query_cf += " AND cohort_month >= ?"
                    params_cf.append(self.cohorts_start.isoformat())
                if self.cohorts_end:
                    query_cf += " AND cohort_month <= ?"
                    params_cf.append(self.cohorts_end.isoformat())
            query_cf += " GROUP BY transaction_month"
            cur.execute(query_cf, params_cf)
            cf_by_month = {row[0]: row[1] for row in cur.fetchall()}
        finally:
            temp_db.disconnect()
            try:
                os.remove(temp_db_path)
            except Exception:
                pass

        return history, cf_by_month
