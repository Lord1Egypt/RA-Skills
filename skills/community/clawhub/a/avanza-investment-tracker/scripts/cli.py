#!/usr/bin/env python3
"""
CLI interface for the Avanza investment tracker.

Provides command-line access to data import, transaction processing,
price updates, and statistics calculation.
"""

import argparse
import shutil
import sys
import logging
from datetime import datetime, timedelta, date

import os
from database_handler import DatabaseHandler
from data_parser import DataParser, SpecialCases, AssetDeficit
from calculate_stats import StatCalculator


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_db(args):
    """Get database handler with connection."""
    db = DatabaseHandler(args.database)
    db.connect()
    return db


def backup_database(db, label):
    """Copy the database file next to itself before a destructive operation.

    Writes <db_file>.pre-<label>.<YYYYMMDD-HHMMSS>.bak so each destructive run
    gets a distinct backup. Returns the backup path, or None if the source
    file does not exist (new/empty database).
    """
    src = db.db_file
    if not src or not os.path.exists(src):
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = f"{src}.pre-{label}.{stamp}.bak"
    shutil.copy2(src, dst)
    logging.info(f"Automatic backup written before destructive operation: {dst}")
    return dst


def confirm_irreversible(action_desc, assume_yes=False):
    """Confirm a destructive operation with the user.

    Interactive shells get a y/N prompt. Non-interactive shells (agents, cron,
    scripts) must pass --yes explicitly; otherwise the operation is refused.
    Returns True if it is safe to proceed.
    """
    if assume_yes:
        return True
    if sys.stdin is not None and sys.stdin.isatty():
        try:
            ans = input(f"{action_desc}\nThis cannot be undone. Proceed? [y/N] ").strip().lower()
            return ans in ("y", "yes")
        except EOFError:
            return False
    logging.error(
        "Refusing destructive operation in non-interactive mode without --yes "
        f"(use --yes to skip this confirmation): {action_desc}"
    )
    return False


def prices_are_fresh(db, max_age_days=1, update_all=False):
    """
    Check if prices are fresh (updated within max_age_days).
    
    Returns:
    bool: True if prices are fresh, False otherwise
    str: Oldest price date or None if no prices
    """
    cur = db.get_cursor()
    # Get oldest price date depending on whether we check all or only held assets
    condition = "" if update_all else "WHERE amount > 0"
    result = cur.execute(
        f"SELECT MIN(latest_price_date) FROM assets {condition}"
    ).fetchone()
    
    if not result or not result[0]:
        return False, None  # No prices or no assets
    
    oldest_price_date = datetime.strptime(result[0], '%Y-%m-%d').date()
    today = datetime.today().date()
    
    is_fresh = oldest_price_date >= today - timedelta(days=max_age_days)
    return is_fresh, oldest_price_date

def any_assets_need_prices(db, update_all=False):
    """
    Check if any assets have no price date.
    
    Returns:
    bool: True if any assets need prices, False otherwise
    """
    cur = db.get_cursor()
    if update_all:
        query = "SELECT COUNT(*) FROM assets WHERE latest_price_date IS NULL"
    else:
        query = "SELECT COUNT(*) FROM assets WHERE amount > 0 AND latest_price_date IS NULL"
    result = cur.execute(query).fetchone()
    
    return result and result[0] > 0 if result else False


def stats_need_recalculation(db):
    """
    Check if statistics need recalculation.
    
    Stats need recalculation if:
    1. Never calculated before
    2. Transactions processed since last calculation
    3. Prices updated since last calculation
    """
    last_stats = db.get_metadata('last_stats_calculation')
    last_processed = db.get_metadata('last_processed')
    
    if not last_stats:
        return True  # Never calculated
    
    # Check if transactions processed since last calculation
    if last_processed and last_processed > last_stats:
        return True
    
    # Check if prices updated since last calculation
    cur = db.get_cursor()
    result = cur.execute(
        "SELECT MAX(latest_price_date) FROM assets WHERE latest_price_date IS NOT NULL"
    ).fetchone()
    
    if result and result[0]:
        latest_price_date = result[0]
        if latest_price_date > last_stats:
            return True
    
    return False


def import_data(args):
    """Import CSV data and process transactions."""
    db = get_db(args)
    special_cases = SpecialCases(args.special_cases) if args.special_cases else None
    data_parser = DataParser(db, special_cases)
    
    try:
        # Import data
        rows_added = data_parser.add_data(args.file, allow_unsettled=getattr(args, 'allow_unsettled', False))
        logging.info(f"Added {rows_added} rows to the database")

        # Auto-route sells and distribute dividends to the accounts that
        # actually hold the shares, so a transaction reported on the physical
        # account does not abort reprocessing (sells) or get mis-attributed
        # (dividends) when the shares were allocated to a virtual portfolio.
        # No-op without virtuals.
        routed_sells = route_imported_sells_to_holders(db)
        routed_divs = route_imported_dividends_to_holders(db)
        if routed_sells or routed_divs:
            logging.info(
                f"Auto-routed {routed_sells} sell(s) and {routed_divs} dividend(s) to virtual accounts holding the shares."
            )

        # Auto-allocate buys to virtual portfolios using cash + holdings
        # heuristics. Only runs when --allocate-virtual is passed. No-op
        # without virtuals.
        if getattr(args, 'allocate_virtual', False):
            allocated_buys = auto_allocate_buys_to_virtuals(db)
            if allocated_buys:
                logging.info(f"Auto-allocated {allocated_buys} buy(s) to virtual portfolios.")

        # Reset cohort tables (preserving asset_prices) so every import is a
        # clean rebuild — prevents stale cohort_assets entries from surviving
        # across imports with different transaction data.
        data_parser.reset_for_reprocessing()
        
        # Process transactions
        data_parser.process_transactions()
        logging.info("Transactions processed")
        
        # Update metadata
        now = datetime.now().isoformat()
        db.set_metadata('last_import', now)
        db.set_metadata('last_processed', now)
        
        # Clear stats timestamp since we have new data
        db.set_metadata('last_stats_calculation', '')
        
        logging.info("Import completed")
        return 0
        
    except Exception as e:
        logging.error(f"Import failed: {e}")
        return 1











def parse_date_bound(date_str, is_start_bound=False):
    """
    Parse a date string that can be YYYY, YYYY-MM, or YYYY-MM-DD.
    If is_start_bound is True:
        - YYYY resolves to YYYY-01-01
        - YYYY-MM resolves to YYYY-MM-01
    If is_start_bound is False:
        - YYYY resolves to YYYY-12-31
        - YYYY-MM resolves to YYYY-MM-<last_day_of_month>
    """
    if not date_str:
        return None
    
    import calendar
    from datetime import date
    
    date_str = date_str.strip()
    
    # 1. Try YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass
        
    # 2. Try YYYY-MM
    try:
        dt = datetime.strptime(date_str, "%Y-%m")
        year, month = dt.year, dt.month
        if is_start_bound:
            return date(year, month, 1)
        else:
            last_day = calendar.monthrange(year, month)[1]
            return date(year, month, last_day)
    except ValueError:
        pass
        
    # 3. Try YYYY
    try:
        if len(date_str) == 4 and date_str.isdigit():
            year = int(date_str)
            if is_start_bound:
                return date(year, 1, 1)
            else:
                return date(year, 12, 31)
    except ValueError:
        pass
        
    raise ValueError(f"Invalid date format: '{date_str}'. Supported formats: YYYY, YYYY-MM, YYYY-MM-DD")


def get_physical_accounts(db):
    """
    Return the list of physical (non-virtual) account IDs that have transactions.

    Returns None when no virtual accounts exist, so the caller's "no filter / all
    accounts" path is taken unchanged — preserving current behaviour for users
    who have not created any virtual portfolios. When virtuals do exist, returns
    the explicit physical-account list so aggregates exclude them by default.
    """
    virtual_map = db.get_virtual_map()
    if not virtual_map:
        return None
    cur = db.get_cursor()
    cur.execute("SELECT DISTINCT account FROM transactions")
    accounts = [r[0] for r in cur.fetchall()]
    physical = [a for a in accounts if a not in virtual_map]
    return physical or None


def resolve_accounts(db, account_arg):
    """Parse account argument and resolve display names/nicknames to account IDs.

    Returns a list of account IDs, or None to signal "no filter" (all accounts):
      * account_arg is None (unspecified) -> physical accounts only (excludes
        virtual portfolios). If no virtuals exist this returns None == all, so
        current behaviour is preserved.
      * account_arg == 'all'               -> None (truly all accounts incl. virtual).
      * account_arg == 'default'           -> the configured default set.
      * otherwise                          -> explicit comma-separated list, with
        nicknames resolved to IDs.
    """
    if account_arg is None:
        return get_physical_accounts(db)

    account_arg = account_arg.strip()
    if account_arg.lower() == 'all':
        return None
        
    if account_arg.lower() == 'default':
        default_accounts_str = db.get_metadata('default_accounts')
        if not default_accounts_str:
            return None
        raw_accounts = [acc.strip() for acc in default_accounts_str.split(',')]
    else:
        raw_accounts = [acc.strip() for acc in account_arg.split(',')]
        
    # Resolve nicknames to numeric IDs
    nicknames = db.get_all_account_nicknames()
    reverse_nicknames = {v.lower().strip(): k for k, v in nicknames.items()}
    
    resolved = []
    for acc in raw_accounts:
        acc_lower = acc.lower().strip()
        if acc_lower in reverse_nicknames:
            resolved.append(reverse_nicknames[acc_lower])
        else:
            resolved.append(acc)
    return resolved


def resolve_single_account(db, identifier):
    """Resolve a single account identifier (id or nickname) to its account ID."""
    if identifier is None:
        return None
    identifier = identifier.strip()
    nicknames = db.get_all_account_nicknames()
    reverse = {v.lower().strip(): k for k, v in nicknames.items()}
    return reverse.get(identifier.lower().strip(), identifier)


def check_price_staleness(asset_name, price_date_str, target_date, warnings_list, threshold_days=30):
    if not price_date_str or not target_date:
        return
    try:
        from datetime import datetime, date
        if isinstance(price_date_str, str):
            p_date = datetime.strptime(price_date_str, "%Y-%m-%d").date()
        elif isinstance(price_date_str, (datetime, date)):
            p_date = price_date_str if isinstance(price_date_str, date) else price_date_str.date()
        else:
            return

        if isinstance(target_date, str):
            t_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        elif isinstance(target_date, (datetime, date)):
            t_date = target_date if isinstance(target_date, date) else target_date.date()
        else:
            return

        days_stale = (t_date - p_date).days
        if days_stale > threshold_days:
            warn_msg = f"WARNING: {asset_name} priced from {price_date_str}, {days_stale} days stale for valuation date {t_date.isoformat()}"
            if warn_msg not in warnings_list:
                warnings_list.append(warn_msg)
    except Exception:
        pass


def calc_period_apy(start_val, end_val, period_dep, period_with, days, apy_mode):
    if days <= 0:
        return 0.0
    if apy_mode == 'twrr':
        if start_val > 1e-4 and end_val > 0:
            tr = end_val / start_val
            return 100 * (tr ** (365.0 / days) - 1)
        return 0.0
    else:
        # MWRR / Modified Dietz approximation
        weighted_base = start_val + 0.5 * period_dep - 0.5 * period_with
        gain = end_val - start_val - (period_dep - period_with)
        if weighted_base > 1e-4:
            hpr = gain / weighted_base
            return 100 * hpr * (365.0 / days)
        return 0.0


def get_stats_holdings(db, cohort_month=None, cohorts_start=None, cohorts_end=None, accounts=None):
    cur = db.get_cursor()
    
    # Resolve accounts
    if accounts is None:
        cur.execute("SELECT DISTINCT account FROM cohort_assets")
        accounts = [r[0] for r in cur.fetchall()]
        
    if not accounts:
        return []
        
    placeholders = ",".join("?" for _ in accounts)
    params = list(accounts)
    
    query = f"""
        SELECT a.asset, SUM(ca.amount) AS total_amount, a.latest_price, a.latest_price_date
        FROM cohort_assets ca
        JOIN assets a ON ca.asset_id = a.asset_id
        WHERE ca.account IN ({placeholders}) AND ca.amount > 0.0001
    """
    
    if cohort_month is not None:
        query += " AND ca.month = ?"
        params.append(cohort_month.isoformat() if hasattr(cohort_month, 'isoformat') else str(cohort_month))
    else:
        if cohorts_start is not None:
            query += " AND ca.month >= ?"
            params.append(cohorts_start.isoformat() if hasattr(cohorts_start, 'isoformat') else str(cohorts_start))
        if cohorts_end is not None:
            query += " AND ca.month <= ?"
            params.append(cohorts_end.isoformat() if hasattr(cohorts_end, 'isoformat') else str(cohorts_end))
            
    query += " GROUP BY a.asset HAVING SUM(ca.amount) > 0.0001 ORDER BY (SUM(ca.amount) * COALESCE(a.latest_price, 0.0)) DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    
    holdings = []
    for asset, amount, price, price_date in rows:
        p_val = price if price is not None else 0.0
        holdings.append({
            'asset': asset,
            'amount': amount,
            'price': p_val,
            'market_value': amount * p_val,
            'price_date': price_date
        })
    return holdings


def is_cohort_older(cohort_month, value_start, period):
    if value_start is None:
        return False
    
    from datetime import date, datetime
    c_year = None
    c_date = None
    
    if hasattr(cohort_month, 'year'):
        c_year = cohort_month.year
        if hasattr(cohort_month, 'month'):
            c_date = date(cohort_month.year, cohort_month.month, cohort_month.day) if hasattr(cohort_month, 'day') else date(cohort_month.year, cohort_month.month, 1)
        else:
            c_date = date(cohort_month.year, 1, 1)
    else:
        try:
            s = str(cohort_month)
            if len(s) == 4:
                c_year = int(s)
                c_date = date(c_year, 1, 1)
            elif len(s) == 7:
                dt = datetime.strptime(s, "%Y-%m")
                c_year = dt.year
                c_date = dt.date()
            else:
                dt = datetime.strptime(s[:10], "%Y-%m-%d")
                c_year = dt.year
                c_date = dt.date()
        except Exception:
            pass
            
    if c_date is None:
        return False
        
    if period == "year":
        return c_year < value_start.year
    else:
        return (c_date.year, c_date.month) < (value_start.year, value_start.month)


def create_temp_snapshot_db(db, target_date, apy_mode, special_cases_path, warnings):
    import shutil
    import os
    import time
    
    # We must ensure target_date is a date object
    if isinstance(target_date, str):
        from datetime import datetime
        t_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    else:
        t_date = target_date
        
    temp_db_path = f"{db.db_file}_temp_as_of_{int(time.time())}_{id(target_date)}.db"
    shutil.copy2(db.db_file, temp_db_path)
    
    temp_db = DatabaseHandler(temp_db_path)
    temp_db.interpolate = db.interpolate
    temp_db.connect()
    
    temp_cur = temp_db.get_cursor()
    temp_cur.execute("DELETE FROM transactions WHERE date > ?", (t_date.isoformat(),))
    
    temp_db.reset_table("cohort_data")
    temp_db.reset_table("cohort_assets")
    temp_db.reset_table("cohort_cash_flows")
    temp_db.reset_table("assets")
    temp_cur.execute("UPDATE transactions SET processed = 0")
    temp_db.commit()
    
    special_cases = SpecialCases(special_cases_path) if special_cases_path else None
    parser = DataParser(temp_db, special_cases)
    parser.process_transactions(raise_on_unprocessed=False)
    
    # Resolve prices
    held_assets_rows = temp_cur.execute("SELECT DISTINCT asset_id FROM cohort_assets WHERE amount > 0.001").fetchall()
    held_asset_ids = {row[0] for row in held_assets_rows}
    
    assets = temp_cur.execute("SELECT asset_id, asset FROM assets").fetchall()
    for asset_id, asset_name in assets:
        price, is_interpolated, gap, price_date = temp_db.get_price(asset_id, t_date)
        if price is not None and price > 0:
            temp_cur.execute("""
                UPDATE assets
                SET latest_price = ?, latest_price_date = ?
                WHERE asset_id = ?
            """, (price, price_date, asset_id))
            if asset_id in held_asset_ids:
                check_price_staleness(asset_name, price_date, t_date, warnings)
    temp_db.commit()
    
    stat_calc = StatCalculator(temp_db)
    stat_calc.calculate_cohort_stats(apy_mode=apy_mode, today=t_date)
    stat_calc.calculate_year_stats(apy_mode=apy_mode, today=t_date)
    
    return temp_db, temp_db_path


def print_risk_metrics_table(risk_metrics, beta_ticker=None):
    p_start = risk_metrics['period_start'].isoformat()
    p_end = risk_metrics['period_end'].isoformat()
    
    print(f"\nPortfolio Risk Metrics ({p_start} to {p_end})")
    print("==================================================")
    print(f"Standard Deviation:     {risk_metrics['annualized_stddev']*100:.1f}%")
    print(f"Sharpe Ratio:           {risk_metrics['sharpe_ratio']:.2f}")
    print(f"Sortino Ratio:          {risk_metrics['sortino_ratio']:.2f}")
    
    dd_val = risk_metrics['max_drawdown'] * 100
    peak = risk_metrics['max_drawdown_peak']
    trough = risk_metrics['max_drawdown_trough']
    if peak and trough:
        peak_str = peak.strftime("%Y-%m")
        trough_str = trough.strftime("%Y-%m")
        print(f"Maximum Drawdown:      -{dd_val:.1f}%  ({peak_str} to {trough_str})")
    else:
        print(f"Maximum Drawdown:      -{dd_val:.1f}%")
        
    if risk_metrics['beta'] is not None:
        ticker = beta_ticker if beta_ticker else '^OMXSPI'
        print(f"Beta vs {ticker}:         {risk_metrics['beta']:.2f}")


def cohort_bounds(cohort_month, period):
    """Return (cohorts_start, cohorts_end) for a single cohort given its
    representative month-end date and the grouping period ('year' or 'month').
    """
    import calendar
    if hasattr(cohort_month, 'year') and hasattr(cohort_month, 'month'):
        y, m = cohort_month.year, cohort_month.month
        if period == "year":
            return date(y, 1, 1), date(y, 12, 31)
        last = calendar.monthrange(y, m)[1]
        return date(y, m, 1), date(y, m, last)
    # Fallback: treat as a single point
    return cohort_month, cohort_month


def format_cohort_risk_inline(cohort_risk, beta_ticker=None):
    """Format a single cohort's risk metrics as inline print lines (no header)."""
    lines = [
        f"Std Dev: {cohort_risk['annualized_stddev']*100:.1f}%",
        f"Sharpe: {cohort_risk['sharpe_ratio']:.2f}",
        f"Sortino: {cohort_risk['sortino_ratio']:.2f}",
    ]
    dd_val = cohort_risk['max_drawdown'] * 100
    peak = cohort_risk['max_drawdown_peak']
    trough = cohort_risk['max_drawdown_trough']
    if peak and trough:
        lines.append(f"Max Drawdown: -{dd_val:.1f}%  ({peak.strftime('%Y-%m')} to {trough.strftime('%Y-%m')})")
    else:
        lines.append(f"Max Drawdown: -{dd_val:.1f}%")
    if cohort_risk['beta'] is not None:
        ticker = beta_ticker if beta_ticker else '^OMXSPI'
        lines.append(f"Beta vs {ticker}: {cohort_risk['beta']:.2f}")
    return lines


def format_cohort_risk_json(cohort_risk):
    """Format a single cohort's risk metrics for JSON output."""
    return {
        'annualized_stddev': cohort_risk['annualized_stddev'],
        'sharpe_ratio': cohort_risk['sharpe_ratio'],
        'sortino_ratio': cohort_risk['sortino_ratio'],
        'max_drawdown': cohort_risk['max_drawdown'],
        'max_drawdown_peak': cohort_risk['max_drawdown_peak'].isoformat() if cohort_risk['max_drawdown_peak'] else None,
        'max_drawdown_trough': cohort_risk['max_drawdown_trough'].isoformat() if cohort_risk['max_drawdown_trough'] else None,
        'beta': cohort_risk['beta'],
        'risk_free_rate': cohort_risk['risk_free_rate'],
    }


def stats(args):
    """Smart statistics command with automatic updates."""
    db = get_db(args)
    db.interpolate = not getattr(args, 'no_interpolation', False)
    
    # Parse account filter
    accounts = resolve_accounts(db, args.account)
    
    as_of = None
    cohorts_start = None
    cohorts_end = None
    value_start = None
    value_end = None
    
    try:
        as_of = parse_date_bound(getattr(args, 'as_of', None), is_start_bound=False)
        
        cohort_raw = getattr(args, 'cohort', None)
        if cohort_raw is not None:
            c_start_raw = getattr(args, 'cohorts_start', None)
            c_end_raw = getattr(args, 'cohorts_end', None)
            if c_start_raw is not None or c_end_raw is not None:
                logging.error("Cannot specify both --cohort and --cohorts-start/--cohorts-end")
                return 1
                
            import re
            if re.match(r"^\d{4}-\d{2}$", cohort_raw):
                c_start_raw = cohort_raw
                c_end_raw = cohort_raw
                if getattr(args, 'period', 'default') == 'default':
                    args.period = 'month'
            elif re.match(r"^\d{4}$", cohort_raw):
                c_start_raw = f"{cohort_raw}-01"
                c_end_raw = f"{cohort_raw}-12"
                if getattr(args, 'period', 'default') == 'default':
                    args.period = 'year'
            else:
                logging.error(f"Invalid --cohort format: '{cohort_raw}'. Must be YYYY-MM or YYYY.")
                return 1
        else:
            c_start_raw = getattr(args, 'cohorts_start', None)
            c_end_raw = getattr(args, 'cohorts_end', None)
            
        v_start_raw = getattr(args, 'from_date', None)
        v_end_raw = getattr(args, 'to', None)
        
        if v_end_raw is None and as_of is not None:
            v_end_raw = getattr(args, 'as_of', None)
            
        cohorts_start = parse_date_bound(c_start_raw, is_start_bound=True)
        cohorts_end = parse_date_bound(c_end_raw, is_start_bound=False)
        value_start = parse_date_bound(v_start_raw, is_start_bound=True)
        value_end = parse_date_bound(v_end_raw, is_start_bound=False)
        
    except ValueError as e:
        logging.error(str(e))
        return 1

    # Date filters trigger temp DB snapshotting
    has_date_filters = (as_of is not None or value_start is not None or value_end is not None)

    # Update prices if needed (only if not running past historical query or if force)
    update_all = getattr(args, 'update_all', False)
    if args.update_prices == 'always':
        # Force price update
        fresh, oldest_date = prices_are_fresh(db, update_all=update_all)
        if fresh:
            logging.info(f"Prices are already fresh (oldest: {oldest_date}), updating anyway...")
        try:
            stat_calc = StatCalculator(db)
            stat_calc.update_prices(force=True, update_all=update_all)
            
            # Update metadata
            now = datetime.now().isoformat()
            db.set_metadata('last_price_update', now)
            
            # Clear stats timestamp since prices changed
            db.set_metadata('last_stats_calculation', '')
            
            logging.info("Prices updated successfully")
        except Exception as e:
            logging.error(f"Failed to update prices: {e}")
            return 1
            
    elif args.update_prices == 'auto' and not has_date_filters:
        fresh, oldest_date = prices_are_fresh(db, update_all=update_all)
        need_prices = any_assets_need_prices(db, update_all=update_all)
        
        if not fresh or need_prices:
            if need_prices:
                logging.info("Some assets have no prices, updating...")
            else:
                logging.info(f"Prices are stale (oldest: {oldest_date}), updating...")
            
            try:
                stat_calc = StatCalculator(db)
                stat_calc.update_prices(force=True, update_all=update_all)
                
                # Update metadata
                now = datetime.now().isoformat()
                db.set_metadata('last_price_update', now)
                
                # Clear stats timestamp since prices changed
                db.set_metadata('last_stats_calculation', '')
                
                logging.info("Prices updated successfully")
            except Exception as e:
                logging.error(f"Failed to update prices: {e}")
                return 1
    
    # Calculate stats if needed
    apy_mode = getattr(args, 'apy_mode', 'mwrr')
    # Force recalculation if APY mode changed
    last_apy_mode = db.get_metadata('last_apy_mode') or 'mwrr'
    if last_apy_mode == 'modified-dietz':
        last_apy_mode = 'mwrr'
    apy_mode_changed = (apy_mode != last_apy_mode)
    if not has_date_filters and (args.force or apy_mode_changed or stats_need_recalculation(db)):
        try:
            stat_calc = StatCalculator(db)
            stat_calc.calculate_cohort_stats(apy_mode=apy_mode)
            stat_calc.calculate_year_stats(apy_mode=apy_mode)
            
            # Update metadata
            now = datetime.now().isoformat()
            db.set_metadata('last_stats_calculation', now)
            db.set_metadata('last_apy_mode', apy_mode)
            
            logging.info("Statistics calculated")
        except Exception as e:
            logging.error(f"Failed to calculate statistics: {e}")
            return 1
    
    # Display statistics
    start_temp_db = None
    start_temp_db_path = None
    end_temp_db = None
    end_temp_db_path = None
    
    try:
        # Determine effective end target date
        target_end_date = value_end if value_end is not None else as_of
        if target_end_date is None and (value_start is not None or cohorts_start is not None or cohorts_end is not None):
            target_end_date = date.today()
            
        warnings = []
        if value_start is not None:
            # Double snapshot calculation
            start_temp_db, start_temp_db_path = create_temp_snapshot_db(db, value_start, apy_mode, getattr(args, 'special_cases', None), warnings)
            end_temp_db, end_temp_db_path = create_temp_snapshot_db(db, target_end_date, apy_mode, getattr(args, 'special_cases', None), warnings)
            active_db = end_temp_db
        elif target_end_date is not None:
            # Single snapshot calculation
            end_temp_db, end_temp_db_path = create_temp_snapshot_db(db, target_end_date, apy_mode, getattr(args, 'special_cases', None), warnings)
            active_db = end_temp_db
        else:
            # Main database
            active_db = db
            
        stat_calc = StatCalculator(active_db)
        period = args.period
        if period == 'default':
            period = active_db.get_metadata('default_stats_period') or 'month'

        kwargs = {
            'period': period,
            'deposits': args.deposits,
            'apy_mode': apy_mode
        }
        
        # Add account filter if specified
        if accounts is not None:
            kwargs['accounts'] = accounts
            
        # Get start/end maps for delta calculation
        start_map = {}
        if value_start is not None:
            start_calc = StatCalculator(start_temp_db)
            start_kwargs = kwargs.copy()
            start_kwargs['end_date'] = value_start
            start_stats = start_calc.get_stats(**start_kwargs)
            
            def get_key(d):
                if hasattr(d, 'isoformat'):
                    return d.isoformat()
                return str(d)
                
            start_map = { get_key(r[0]): r for r in start_stats }
            
            end_calc = StatCalculator(end_temp_db)
            end_kwargs = kwargs.copy()
            end_kwargs['end_date'] = target_end_date
            end_stats = end_calc.get_stats(**end_kwargs)
            
            stats_list = []
            days = (target_end_date - value_start).days
            for end_row in end_stats:
                date_key = get_key(end_row[0])
                if date_key in start_map:
                    start_row = start_map[date_key]
                    
                    p_dep = end_row[1] - start_row[1]
                    p_with = end_row[2] - start_row[2]
                    p_val = end_row[3]
                    p_gain = end_row[4] - start_row[4]
                    p_real = end_row[5] - start_row[5]
                    p_unreal = end_row[6] - start_row[6]
                    
                    base_cap = start_row[3] + p_dep
                    if base_cap > 1e-4:
                        p_gain_pct = 100.0 * p_gain / base_cap
                        p_real_pct = 100.0 * p_real / base_cap
                        p_unreal_pct = 100.0 * p_unreal / base_cap
                    else:
                        p_gain_pct = p_real_pct = p_unreal_pct = 0.0
                        
                    p_apy = calc_period_apy(start_row[3], p_val, p_dep, p_with, days, apy_mode)
                    
                    stats_list.append((
                        end_row[0], p_dep, p_with, p_val, p_gain, p_real, p_unreal,
                        p_gain_pct, p_real_pct, p_unreal_pct, p_apy, start_row[3]
                    ))
                else:
                    # Cohort didn't exist at value_start
                    stats_list.append(end_row + (0.0,))
        else:
            if target_end_date is not None:
                kwargs['end_date'] = target_end_date
            stats_list = stat_calc.get_stats(**kwargs)
            
        # Filter by deposits parameter for double snapshot
        if value_start is not None and args.deposits == "current":
            stats_list = [row for row in stats_list if row[3] > 0 or (get_key(row[0]) in start_map and start_map[get_key(row[0])][3] > 0)]

        # Apply cohorts range filtering
        filtered_stats = []
        for row in stats_list:
            row_date = row[0]
            if isinstance(row_date, str):
                if '-' in row_date:
                    rd = datetime.strptime(row_date, "%Y-%m-%d").date()
                else:
                    rd = date(int(row_date), 12, 31)
            else:
                rd = row_date
                
            if cohorts_start is not None and rd < cohorts_start:
                continue
            if cohorts_end is not None and rd > cohorts_end:
                continue
            filtered_stats.append(row)
        stats_list = filtered_stats
        
        # Calculate overall blended APY for the period/cohorts
        portfolio_apy = None
        if value_start is not None:
            total_val = sum(row[3] for row in stats_list)
            total_dep = sum(row[1] for row in stats_list)
            total_with = sum(row[2] for row in stats_list)
            start_val = sum(start_map[get_key(row[0])][3] for row in stats_list if get_key(row[0]) in start_map)
            days = (target_end_date - value_start).days
            portfolio_apy = calc_period_apy(start_val, total_val, total_dep, total_with, days, apy_mode)
        else:
            if cohorts_start is not None or cohorts_end is not None:
                if len(stats_list) == 1:
                    portfolio_apy = stats_list[0][10]
                else:
                    total_dep = sum(row[1] for row in stats_list)
                    if total_dep > 0:
                        portfolio_apy = sum(row[1] * (row[10] if row[10] is not None else 0.0) for row in stats_list) / total_dep
                    else:
                        portfolio_apy = 0.0
            else:
                acc_list = accounts if accounts is not None else 'all'
                total_val = sum(row[3] for row in stats_list)
                portfolio_apy, _ = stat_calc.calculate_account_apy(acc_list, apy_mode=apy_mode, end_date=target_end_date, current_value=total_val)
                
        if portfolio_apy is None:
            portfolio_apy = 0.0

        # Calculate risk metrics if requested
        risk_enabled = getattr(args, 'risk', False) or getattr(args, 'beta', None) is not None
        risk_metrics = None
        # Summary mode shows a single portfolio-level risk section; the standard
        # cohort breakdown computes per-cohort risk inline (see the loop below).
        if risk_enabled and getattr(args, 'summary', False):
            from risk_calculator import RiskCalculator
            calc_end_date = target_end_date if target_end_date is not None else date.today()
            calculator = RiskCalculator(
                db=db,
                accounts=args.account,
                from_date=value_start,
                to_date=calc_end_date,
                cohorts_start=cohorts_start,
                cohorts_end=cohorts_end,
                beta_ticker=getattr(args, 'beta', None),
                interpolate=db.interpolate
            )
            try:
                risk_metrics = calculator.calculate(portfolio_apy=portfolio_apy / 100.0)
            except Exception as e:
                logging.error(f"Failed to calculate risk metrics: {e}")
        
        # Output summary mode or standard list mode
        if getattr(args, 'summary', False):
            total_dep = sum(row[1] for row in stats_list)
            total_with = sum(row[2] for row in stats_list)
            total_val = sum(row[3] for row in stats_list)
            total_gain = sum(row[4] for row in stats_list)
            total_real = sum(row[5] for row in stats_list)
            total_unreal = sum(row[6] for row in stats_list)
            
            blended_apy = portfolio_apy
            start_val = 0.0
            if value_start is not None:
                start_val = sum(start_map[get_key(row[0])][3] for row in stats_list if get_key(row[0]) in start_map)
                
            holdings = []
            if getattr(args, 'positions', False):
                holdings = get_stats_holdings(active_db, cohorts_start=cohorts_start, cohorts_end=cohorts_end, accounts=accounts)
                for h in holdings:
                    check_price_staleness(h['asset'], h['price_date'], target_end_date or date.today(), warnings)
                    
            if getattr(args, 'format', 'table') == 'json':
                import json
                net_transfers = total_val + total_with - start_val - total_dep - total_gain
                result = {
                    'period': f"{value_start.isoformat()} to {target_end_date.isoformat()}" if value_start else "all",
                    'deposits': total_dep,
                    'withdrawals': total_with,
                    'current_value': total_val,
                    'total_gain': total_gain,
                    'total_gain_percent': (total_gain / (start_val + total_dep) * 100) if ((start_val + total_dep) > 0) else 0.0,
                    'apy': blended_apy
                }
                if abs(net_transfers) > 0.01:
                    result['net_transfers'] = net_transfers
                if value_start is not None:
                    result['start_value'] = start_val
                if accounts is not None and len(accounts) == 1:
                    acc_id = list(accounts)[0]
                    nicknames = db.get_all_account_nicknames()
                    result['account'] = acc_id
                    result['display_name'] = nicknames.get(acc_id, acc_id)
                if getattr(args, 'positions', False):
                    total_assets_val = sum(h['market_value'] for h in holdings)
                    result['holdings'] = [
                        {
                            'asset': h['asset'],
                            'amount': h['amount'],
                            'price': h['price'],
                            'market_value': h['market_value'],
                            'allocation_percent': (h['market_value'] / total_assets_val * 100) if total_assets_val > 0 else 0.0
                        }
                        for h in holdings
                    ]
                if risk_metrics:
                    result['risk'] = {
                        'annualized_return': risk_metrics['annualized_return'],
                        'annualized_stddev': risk_metrics['annualized_stddev'],
                        'sharpe_ratio': risk_metrics['sharpe_ratio'],
                        'sortino_ratio': risk_metrics['sortino_ratio'],
                        'max_drawdown': risk_metrics['max_drawdown'],
                        'max_drawdown_peak': risk_metrics['max_drawdown_peak'].isoformat() if risk_metrics['max_drawdown_peak'] else None,
                        'max_drawdown_trough': risk_metrics['max_drawdown_trough'].isoformat() if risk_metrics['max_drawdown_trough'] else None,
                        'beta': risk_metrics['beta'],
                        'risk_free_rate': risk_metrics['risk_free_rate'],
                        'year_returns': risk_metrics['year_returns']
                    }
                print(json.dumps(result, indent=2))
            else:
                is_portfolio = getattr(args, 'is_portfolio', False)
                if is_portfolio and accounts is not None and len(accounts) == 1:
                    account_id = list(accounts)[0]
                    nicknames = db.get_all_account_nicknames()
                    nickname = nicknames.get(account_id)
                    account_label = f"Account {account_id}"
                    if nickname:
                        account_label += f" ({nickname})"
                else:
                    account_label = None
                    
                period_label = f"{value_start.isoformat()} to {target_end_date.isoformat()}" if value_start else "all cohorts"
                if account_label:
                    header_title = f"{account_label} — {period_label}" if value_start else account_label
                else:
                    header_title = f"Summary — {period_label}"
                print(f"{header_title}\n")
                net_transfers = total_val + total_with - start_val - total_dep - total_gain
                if value_start is not None:
                    print(f"Start Value:       {start_val:,.0f} SEK")
                print(f"Total Deposited:   {total_dep:,.0f} SEK")
                print(f"Total Withdrawn:   {total_with:,.0f} SEK")
                if abs(net_transfers) > 0.01:
                    trans_sign = "+" if net_transfers > 0 else ""
                    print(f"Net Transfers:     {trans_sign}{net_transfers:,.0f} SEK")
                print(f"Current Value:     {total_val:,.0f} SEK")
                
                gl_sign = "+" if total_gain > 0 else ""
                gain_pct = (total_gain / (start_val + total_dep) * 100) if ((start_val + total_dep) > 0) else 0.0
                gl_pct_sign = "+" if gain_pct > 0 else ""
                print(f"Total Gain:       {gl_sign}{total_gain:,.0f} SEK ({gl_pct_sign}{gain_pct:.1f}%)")
                
                apy_str = f"{blended_apy:.1f}%" if blended_apy is not None else "N/A"
                print(f"Blended APY:       {apy_str} ({apy_mode.upper()})")
                
                if getattr(args, 'positions', False):
                    print()
                    print("Holdings:")
                    if holdings:
                        name_w = max(max(len(h['asset']) for h in holdings), 9)
                        print(f"  {'Fund Name':<{name_w}} {'Market Value':>15} {'Allocation':>11}")
                        total_assets_val = sum(h['market_value'] for h in holdings)
                        for h in holdings:
                            alloc = (h['market_value'] / total_assets_val * 100) if total_assets_val > 0 else 0.0
                            print(f"  {h['asset']:<{name_w}} {h['market_value']:>15,.0f} SEK {alloc:>10.1f}%")
                        print(f"  {'Total':<{name_w}} {total_assets_val:>15,.0f} SEK {'100.0%':>11}")
                    else:
                        print("  None")
                if risk_metrics:
                    print_risk_metrics_table(risk_metrics, beta_ticker=getattr(args, 'beta', None))
        else:
            # Cohort-level breakdown mode
            if getattr(args, 'format', 'table') == 'json':
                import json
                from risk_calculator import RiskCalculator
                def serialize_date(d):
                    if hasattr(d, 'isoformat'):
                        return d.isoformat()
                    return str(d)
                calc_end_date = target_end_date if target_end_date is not None else date.today()
                json_data = []
                for row in stats_list:
                    if row[1] > 0 or row[3] > 0:
                        cohort_month = row[0]
                        cohort_data = {
                            'date': serialize_date(cohort_month),
                            'withdrawal': row[2],
                            'value': row[3],
                            'total_gainloss': row[4],
                            'total_gainloss_percent': row[7],
                            'realized_gainloss': row[5],
                            'realized_gainloss_percent': row[8],
                            'unrealized_gainloss': row[6],
                            'unrealized_gainloss_percent': row[9],
                            'apy': row[10]
                        }
                        if value_start is not None and is_cohort_older(cohort_month, value_start, period):
                            start_val = row[11] if len(row) > 11 else 0.0
                            cohort_data['start_value'] = start_val
                        else:
                            cohort_data['deposit'] = row[1]
                        if getattr(args, 'positions', False):
                            cohort_holdings = get_stats_holdings(active_db, cohort_month=cohort_month, accounts=accounts)
                            for h in cohort_holdings:
                                check_price_staleness(h['asset'], h['price_date'], target_end_date or date.today(), warnings)
                            total_assets_val = sum(h['market_value'] for h in cohort_holdings)
                            cohort_data['holdings'] = [
                                {
                                    'asset': h['asset'],
                                    'amount': h['amount'],
                                    'price': h['price'],
                                    'market_value': h['market_value'],
                                    'allocation_percent': (h['market_value'] / total_assets_val * 100) if total_assets_val > 0 else 0.0
                                }
                                for h in cohort_holdings
                            ]
                        if risk_enabled:
                            cs, ce = cohort_bounds(cohort_month, period)
                            cohort_calculator = RiskCalculator(
                                db=db,
                                accounts=args.account,
                                from_date=cs,
                                to_date=calc_end_date,
                                cohorts_start=cs,
                                cohorts_end=ce,
                                beta_ticker=getattr(args, 'beta', None),
                                interpolate=db.interpolate
                            )
                            try:
                                cohort_risk = cohort_calculator.calculate(
                                    portfolio_apy=(row[10] or 0.0) / 100.0
                                )
                                cohort_data['risk'] = format_cohort_risk_json(cohort_risk)
                            except Exception as e:
                                logging.error(f"Failed to calculate risk metrics for cohort {cohort_month}: {e}")
                        json_data.append(cohort_data)
                print(json.dumps({'cohorts': json_data}, indent=2))
            else:
                from risk_calculator import RiskCalculator
                calc_end_date = target_end_date if target_end_date is not None else date.today()
                for row in stats_list:
                    if row[1] > 0 or row[3] > 0:
                        cohort_month = row[0]
                        if hasattr(cohort_month, 'year'):
                            if period == "year":
                                display_date = cohort_month.year
                            else:
                                display_date = cohort_month.strftime("%b %Y")
                        else:
                            display_date = str(cohort_month)
                            
                        print(display_date)
                        if value_start is not None and is_cohort_older(cohort_month, value_start, period):
                            start_val = row[11] if len(row) > 11 else 0.0
                            print(f"Start Value: {start_val:.0f}")
                        else:
                            print(f"Deposited: {row[1]:.0f}")
                        print(f"Value: {row[3]:.0f}")
                        print(f"Withdrawal: {row[2]:.0f}")
                        gl_sign = "+" if row[4] > 0 else ""
                        gl_pct_sign = "+" if row[7] > 0 else ""
                        print(f"Gain/Loss: {gl_sign}{row[4]:.0f} ({gl_pct_sign}{row[7]:.1f}%)")
                        un_sign = "+" if row[6] > 0 else ""
                        un_pct_sign = "+" if row[9] > 0 else ""
                        print(f"- Unrealized: {un_sign}{row[6]:.0f} ({un_pct_sign}{row[9]:.1f}%)")
                        re_sign = "+" if row[5] > 0 else ""
                        re_pct_sign = "+" if row[8] > 0 else ""
                        print(f"- Realized: {re_sign}{row[5]:.0f} ({re_pct_sign}{row[8]:.1f}%)")
                        apy_str = f"{row[10]:.1f}%" if row[10] is not None else "N/A"
                        print(f"APY: {apy_str}")
                        
                        if risk_enabled:
                            cs, ce = cohort_bounds(cohort_month, period)
                            cohort_calculator = RiskCalculator(
                                db=db,
                                accounts=args.account,
                                from_date=cs,
                                to_date=calc_end_date,
                                cohorts_start=cs,
                                cohorts_end=ce,
                                beta_ticker=getattr(args, 'beta', None),
                                interpolate=db.interpolate
                            )
                            try:
                                cohort_risk = cohort_calculator.calculate(
                                    portfolio_apy=(row[10] or 0.0) / 100.0
                                )
                                for line in format_cohort_risk_inline(
                                    cohort_risk, beta_ticker=getattr(args, 'beta', None)
                                ):
                                    print(line)
                            except Exception as e:
                                logging.error(f"Failed to calculate risk metrics for cohort {cohort_month}: {e}")
                        
                        if getattr(args, 'positions', False):
                            cohort_holdings = get_stats_holdings(active_db, cohort_month=cohort_month, accounts=accounts)
                            for h in cohort_holdings:
                                check_price_staleness(h['asset'], h['price_date'], target_end_date or date.today(), warnings)
                            if cohort_holdings:
                                print("  Holdings:")
                                name_w = max(max(len(h['asset']) for h in cohort_holdings), 9)
                                print(f"    {'Fund Name':<{name_w}} {'Market Value':>15} {'Allocation':>11}")
                                total_assets_val = sum(h['market_value'] for h in cohort_holdings)
                                for h in cohort_holdings:
                                    alloc = (h['market_value'] / total_assets_val * 100) if total_assets_val > 0 else 0.0
                                    print(f"    {h['asset']:<{name_w}} {h['market_value']:>15,.0f} SEK {alloc:>10.1f}%")
                            else:
                                print("  Holdings: None")
                        print()
                        
        if warnings and not getattr(args, 'quiet', False):
            import sys
            for warning in warnings:
                print(warning, file=sys.stderr)
                
        return 0
        
    except Exception as e:
        logging.error(f"Failed to show statistics: {e}")
        return 1
    finally:
        for t_db, t_path in [(start_temp_db, start_temp_db_path), (end_temp_db, end_temp_db_path)]:
            if t_db is not None:
                t_db.disconnect()
                import gc
                gc.collect()
                if t_path and os.path.exists(t_path):
                    try:
                        os.remove(t_path)
                    except Exception as e:
                        logging.warning(f"Failed to remove temp db file: {e}")


def status(args):
    """Show system status."""
    db = get_db(args)
    
    print("=== Investment Tracker Status ===")
    
    # Database stats
    stats_list = ["Transactions", "Processed", "Unprocessed", "Assets", "Capital"]
    db_stats = db.get_db_stats(stats_list)
    
    print(f"\nDatabase:")
    print(f"  Transactions: {db_stats.get('Transactions', 0)}")
    print(f"  Processed: {db_stats.get('Processed', 0)}")
    print(f"  Unprocessed: {db_stats.get('Unprocessed', 0)}")
    print(f"  Assets: {db_stats.get('Assets', 0)}")
    print(f"  Capital: {db_stats.get('Capital', 0):.0f} SEK")
    
    min_date, max_date = db.get_date_range()
    if min_date and max_date:
        print(f"  Date range: {min_date} to {max_date}")
    elif min_date or max_date:
        print(f"  Date range: {min_date or max_date}")
    
    # Price freshness
    fresh, oldest_date = prices_are_fresh(db)
    price_status = "Fresh" if fresh else "Stale"
    print(f"\nPrices:")
    print(f"  Status: {price_status}")
    if oldest_date:
        print(f"  Oldest price date: {oldest_date}")
    
    # Metadata
    metadata = db.get_all_metadata()
    print(f"\nMetadata:")
    for key in ['last_import', 'last_processed', 'last_price_update', 'last_stats_calculation']:
        value = metadata.get(key, 'Never')
        print(f"  {key}: {value}")
    
    # Stats freshness
    needs_recalc = stats_need_recalculation(db)
    print(f"\nStatistics:")
    print(f"  Need recalculation: {'Yes' if needs_recalc else 'No'}")
    
    return 0


def delete_tx(args):
    """Delete individual transaction(s) and rebuild derived tables (issue #80).

    Targets real (origin='avanza') transactions via --date+--asset, --since, or a
    precise --tx-id. 'Intern överföring' funding transfers left orphaned by a
    deleted allocated buy are removed too (mirroring 'account allocate --undo').
    --cascade widens the match across the account family (same date+asset) so a
    trade and its allocated split are removed together. After the delete, every
    transaction is reprocessed so the assets/cohort tables are rebuilt cleanly --
    there is no path to the orphaned state where derived tables still reflect a
    deleted transaction.
    """
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()

    # --- flag validation ---
    if args.asset and not args.date:
        logging.error("--asset can only be used together with --date.")
        return 1
    if args.account and args.tx_id is not None:
        logging.error("--account cannot be combined with --tx-id (the rowid is already precise).")
        return 1

    select_cols = "rowid, date, account, transaction_type, asset_name, amount, total, origin"
    real = "AND (origin = 'avanza' OR origin IS NULL)"

    if args.tx_id is not None:
        row = cur.execute(
            f"SELECT {select_cols} FROM transactions WHERE rowid = ?", (args.tx_id,)
        ).fetchone()
        if not row:
            logging.error(f"No transaction with rowid {args.tx_id}.")
            return 1
        matched = [row]
    elif args.since:
        since = _parse_exact_date(args.since)
        q = f"SELECT {select_cols} FROM transactions WHERE date >= ? {real}"
        params = [since]
        if args.account:
            q += " AND account = ?"
            params.append(resolve_single_account(db, args.account))
        matched = list(cur.execute(q + " ORDER BY rowid", params).fetchall())
    else:  # --date + --asset
        if not args.asset:
            logging.error("--date requires --asset (use --tx-id or --since otherwise).")
            return 1
        target_date = _parse_exact_date(args.date)
        q = f"SELECT {select_cols} FROM transactions WHERE date = ? AND asset_name = ? {real}"
        params = [target_date, args.asset.strip()]
        if args.account:
            q += " AND account = ?"
            params.append(resolve_single_account(db, args.account))
        matched = list(cur.execute(q + " ORDER BY rowid", params).fetchall())

    if not matched:
        logging.error("No matching transaction(s) found.")
        return 1

    virtual_map = db.get_virtual_map()

    # --- cascade: widen the match across the account family by (date, asset_name) ---
    if args.cascade:
        seen = {m[0] for m in matched}
        for m in list(matched):
            tx_date, asset_name = m[1], m[4]
            for acct in _account_family(m[2], virtual_map):
                for r in cur.execute(
                        f"SELECT {select_cols} FROM transactions "
                        "WHERE date = ? AND asset_name = ? AND account = ? " + real,
                        (tx_date, asset_name, acct)):
                    if r[0] not in seen:
                        matched.append(r)
                        seen.add(r[0])

    matched_rowids = {m[0] for m in matched}

    # --- funding-transfer cleanup for deleted allocated buys (mirrors allocate --undo) ---
    fund_pair_rowids = set()
    for m in matched:
        rowid, tx_date, acct, ttype, asset_name, amount, total, origin = m
        if ttype == 'Köp' and acct in virtual_map:
            parent = virtual_map[acct]
            fund_date = tx_date - timedelta(days=1)
            for r in cur.execute(
                    f"SELECT {select_cols} FROM transactions "
                    "WHERE transaction_type = 'Intern överföring' AND origin = 'virtual' "
                    "AND date = ? AND (account = ? OR account = ?)",
                    (fund_date, acct, parent)):
                fund_pair_rowids.add(r[0])

    def _fmt(r):
        return (f"rowid={r[0]} {r[1]} {r[2]} {r[3]} '{r[4]}' "
                f"amount={r[5]} total={r[6]} ({r[7]})")

    logging.info(f"Will delete {len(matched_rowids)} transaction(s):")
    for m in matched:
        logging.info("  " + _fmt(m))
    if fund_pair_rowids:
        fund_rows = cur.execute(
            f"SELECT {select_cols} FROM transactions WHERE rowid IN "
            f"({','.join('?' * len(fund_pair_rowids))}) ORDER BY rowid",
            tuple(fund_pair_rowids)).fetchall()
        logging.info(f"And {len(fund_pair_rowids)} orphaned virtual funding transfer(s):")
        for r in fund_rows:
            logging.info("  " + _fmt(r))

    if args.dry_run:
        logging.info("[dry-run] No changes written. Re-run without --dry-run to apply.")
        return 0

    all_ids = matched_rowids | fund_pair_rowids
    if not confirm_irreversible(
        f"delete-tx will permanently delete {len(all_ids)} transaction row(s) "
        "and rebuild derived tables.",
        getattr(args, 'yes', False),
    ):
        return 1
    backup_database(db, "delete-tx")
    placeholders = ",".join("?" * len(all_ids))
    cur.execute(f"DELETE FROM transactions WHERE rowid IN ({placeholders})", tuple(all_ids))
    deleted = cur.rowcount
    db.commit()
    logging.info(f"Deleted {deleted} transaction row(s).")

    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        logging.error(
            "Reprocessing failed after deletion (e.g. a sell left without its matching "
            "buy). The rows are deleted but derived tables need attention; inspect the "
            "logs and re-import or adjust."
        )
        return 1
    logging.info("Derived tables rebuilt.")
    return 0


def reset(args):
    """Reset database state."""
    db = get_db(args)
    special_cases = SpecialCases(args.special_cases) if args.special_cases else None
    data_parser = DataParser(db, special_cases)
    
    try:
        if getattr(args, 'hard', False):
            if not confirm_irreversible(
                "reset --hard will DELETE all transactions, statistics, and prices "
                "from the database.",
                getattr(args, 'yes', False),
            ):
                return 1
            backup_database(db, "reset-hard")
            # Hard reset: delete all transaction and calculation tables
            tables_to_reset = [
                "transactions", "cohort_data", "cohort_assets", "assets",
                "cohort_cash_flows", "asset_prices", "cohort_stats", "year_stats"
            ]
            for t in ["account_cohort_stats", "account_year_stats"]:
                if t in db.tables:
                    tables_to_reset.append(t)
            
            for table in tables_to_reset:
                db.reset_table(table)
            
            logging.info("Database hard reset successfully (deleted all transaction and calculation tables)")
        else:
            data_parser.reset_processed_transactions()
            logging.info("Database reset successfully")
        
        # Clear metadata
        for key in ['last_processed', 'last_stats_calculation']:
            db.set_metadata(key, '')
        
        return 0
        
    except Exception as e:
        logging.error(f"Failed to reset database: {e}")
        return 1


def settings_default_stats_period(args):
    """Set default period for stats command."""
    db = get_db(args)
    
    period = args.period.strip().lower()
    if period in ('month', 'year'):
        db.set_metadata('default_stats_period', period)
        logging.info(f"Default stats period set to '{period}'")
    else:
        logging.error("Invalid period: must be 'month' or 'year'")
        return 1

def settings_default_accounts(args):
    """Set default accounts for filtering."""
    db = get_db(args)
    
    accounts = args.accounts.strip()
    if accounts.lower() == 'all':
        # Store empty string to indicate all accounts
        db.set_metadata('default_accounts', '')
        logging.info("Default accounts set to 'all' (all accounts)")
    else:
        # Validate comma-separated list
        account_list = [acc.strip() for acc in accounts.split(',')]
        if not all(acc for acc in account_list):
            logging.error("Invalid account list: empty account found")
            return 1
        
        # Store as comma-separated string
        db.set_metadata('default_accounts', ','.join(account_list))
        logging.info(f"Default accounts set to: {', '.join(account_list)}")
    
    return 0


def account_nickname(args):
    """Set or remove account nicknames."""
    db = get_db(args)
    
    if args.remove:
        # Remove nickname for specified account
        account = args.remove.strip()
        if db.remove_account_nickname(account):
            logging.info(f"Removed nickname for account '{account}'")
        else:
            logging.info(f"No nickname set for account '{account}'")
    elif args.list:
        # List all nicknames
        nicknames = db.get_all_account_nicknames()
        if nicknames:
            print("Account nicknames:")
            for account, nickname in sorted(nicknames.items()):
                print(f"  {account}: {nickname}")
        else:
            print("No account nicknames set")
    elif args.account and args.nickname is not None:
        # Set nickname
        account = args.account.strip()
        nickname = args.nickname.strip()
        db.set_account_nickname(account, nickname)
        logging.info(f"Set nickname for account '{account}' to '{nickname}'")
    else:
        logging.error("Must specify --remove, --list, or both account and nickname")
        return 1
    
    return 0


def accounts_summary(args):
    """Show account summaries with asset values and cash."""
    db = get_db(args)
    
    # Parse account filter (same logic as stats)
    accounts = resolve_accounts(db, args.account)
    
    # Update prices if needed (same logic as stats)
    update_all = getattr(args, 'update_all', False)
    if args.update_prices == 'always':
        # Force price update
        fresh, oldest_date = prices_are_fresh(db, update_all=update_all)
        if fresh:
            logging.info(f"Prices are already fresh (oldest: {oldest_date}), updating anyway...")
        try:
            stat_calc = StatCalculator(db)
            stat_calc.update_prices(force=True, update_all=update_all)
            
            # Update metadata
            now = datetime.now().isoformat()
            db.set_metadata('last_price_update', now)
            
            logging.info("Prices updated successfully")
        except Exception as e:
            logging.error(f"Failed to update prices: {e}")
            return 1
            
    elif args.update_prices == 'auto':
        fresh, oldest_date = prices_are_fresh(db, update_all=update_all)
        need_prices = any_assets_need_prices(db, update_all=update_all)
        
        if not fresh or need_prices:
            if need_prices:
                logging.info("Some assets have no prices, updating...")
            else:
                logging.info(f"Prices are stale (oldest: {oldest_date}), updating...")
            
            try:
                stat_calc = StatCalculator(db)
                stat_calc.update_prices(force=True, update_all=update_all)
                
                # Update metadata
                now = datetime.now().isoformat()
                db.set_metadata('last_price_update', now)
                
                logging.info("Prices updated successfully")
            except Exception as e:
                logging.error(f"Failed to update prices: {e}")
                return 1
    
    # Display account summary
    try:
        stat_calc = StatCalculator(db)
        # When unspecified or 'all', show the full hierarchical tree (physical
        # accounts with their virtual children). An explicit list is shown flat.
        show_tree = args.account is None or (
            isinstance(args.account, str) and args.account.strip().lower() == 'all'
        )
        if getattr(args, 'format', 'table') == 'json':
            summaries = stat_calc.get_account_summaries(None if show_tree else accounts)
            nicknames = db.get_all_account_nicknames()
            virtual_map = db.get_virtual_map()
            json_data = []
            for account, cash, asset_value, total in summaries:
                json_data.append({
                    'account': account,
                    'display_name': nicknames.get(account, account),
                    'is_virtual': account in virtual_map,
                    'parent_account': virtual_map.get(account),
                    'cash': cash,
                    'assets': asset_value,
                    'total': total
                })
            import json
            print(json.dumps(json_data, indent=2))
        else:
            if show_tree:
                print_account_tree(stat_calc, db)
            else:
                stat_calc.print_account_summary(accounts=accounts)
        return 0
        
    except Exception as e:
        logging.error(f"Failed to show account summary: {e}")
        return 1

    return 0


def portfolio(args):
    """Show portfolio snapshot as an alias to stats --positions --summary."""
    fmt = getattr(args, 'format', 'table')
    if fmt not in ('table', 'json'):
        fmt = 'table'
        
    stats_args = argparse.Namespace(
        database=args.database,
        special_cases=getattr(args, 'special_cases', None),
        account=args.account,
        apy_mode=getattr(args, 'apy_mode', 'mwrr'),
        as_of=getattr(args, 'as_of', None),
        cohorts_start=getattr(args, 'cohorts_start', None),
        cohorts_end=getattr(args, 'cohorts_end', None),
        cohort=getattr(args, 'cohort', None),
        from_date=getattr(args, 'from_date', None),
        to=getattr(args, 'to', None),
        positions=True,
        summary=True,
        is_portfolio=True,
        format=fmt,
        quiet=getattr(args, 'quiet', False),
        no_interpolation=getattr(args, 'no_interpolation', False),
        risk=getattr(args, 'risk', False),
        beta=getattr(args, 'beta', None),
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False
    )
    return stats(stats_args)


def export_transactions(args):
    import os
    db = get_db(args)
    cur = db.get_cursor()
    
    # Resolve accounts
    accounts = resolve_accounts(db, args.account)
    
    # Query transactions
    query = "SELECT date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin FROM transactions"
    params = []
    if accounts is not None:
        placeholders = ','.join('?' for _ in accounts)
        query += f" WHERE account IN ({placeholders})"
        params.extend(accounts)
    query += " ORDER BY date ASC, rowid ASC"
    
    cur.execute(query, params)
    rows = cur.fetchall()
    
    # CSV Header
    header = "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat"
    
    csv_lines = [header]
    
    def format_cell(val, is_numeric=False):
        if val is None:
            return "-" if is_numeric else ""
        if is_numeric:
            if val == 0 or val == 0.0:
                return "-"
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            return str(val).replace('.', ',')
        return str(val)
        
    for row in rows:
        cells = [
            format_cell(row[0]),  # Datum
            format_cell(row[1]),  # Konto
            format_cell(row[2]),  # Typ av transaktion
            format_cell(row[3]),  # Värdepapper/beskrivning
            format_cell(row[4], is_numeric=True),  # Antal
            format_cell(row[5], is_numeric=True),  # Kurs
            format_cell(row[6], is_numeric=True),  # Belopp
            format_cell(row[7], is_numeric=True),  # Courtage
            format_cell(row[8]),  # Valuta
            format_cell(row[9]),  # ISIN
            "-"                   # Resultat
        ]
        csv_lines.append(";".join(cells))
        
    content = "\n".join(csv_lines) + "\n"
    
    if args.output == '-':
        print(content, end='')
    else:
        # Ensure parent directory exists
        out_path = args.output
        parent_dir = os.path.dirname(out_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Successfully exported {len(rows)} transactions to '{out_path}'")
        
    return 0


def _parse_exact_date(date_str):
    """Parse a strict YYYY-MM-DD date string into a date object."""
    return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()


def reprocess_after_virtual_change(db, special_cases_path):
    """Reset cohort tables and reprocess all transactions after a virtual
    portfolio mutation. Returns 0 on success, 1 if reprocessing fails (e.g. an
    AssetDeficit from a sell/dividend allocated without matching shares)."""
    special_cases = SpecialCases(special_cases_path) if special_cases_path else None
    parser = DataParser(db, special_cases)
    db.connect()
    parser.reset_for_reprocessing()
    try:
        parser.process_transactions()
    except AssetDeficit:
        logging.error("Reprocessing failed: one or more transactions could not be processed.")
        logging.error("This usually means a sell/dividend was allocated to a virtual account")
        logging.error("without the corresponding shares/capital being there. Inspect the logs above.")
        return 1
    now = datetime.now().isoformat()
    db.set_metadata('last_processed', now)
    db.set_metadata('last_stats_calculation', '')
    return 0


def _account_family(account, virtual_map):
    """Return the set of accounts considered 'related' to `account` for sell
    routing: itself, its parent (if virtual) plus siblings, or its virtual
    children (if physical)."""
    family = {account}
    parent = virtual_map.get(account)
    if parent:
        family.add(parent)
        for v, p in virtual_map.items():
            if p == parent:
                family.add(v)
    else:
        for v, p in virtual_map.items():
            if p == account:
                family.add(v)
    return family


def route_imported_sells_to_holders(db):
    """Reassign sells whose own account does not hold the asset to the account
    that does (typically a virtual child), so reprocessing does not abort with
    AssetDeficit. Intended to run after add_data and before reset_for_reprocessing.

    Authority for "who holds what" is the pre-import cohort_assets snapshot (the
    last-processed state). Rule per sell of N shares of X on account A:
      * if A holds >= N -> leave (it will process against A's own shares)
      * elif a related account holds the shortfall -> route/split there
        (drain A first, then the largest related holder)
      * else -> leave (genuine over-sell; reprocessing surfaces a clear error)

    Returns the number of sells routed or split. No-op when no virtuals exist.
    """
    db.connect()
    virtual_map = db.get_virtual_map()
    if not virtual_map:
        return 0
    cur = db.get_cursor()

    cur.execute(
        "SELECT rowid, date, account, asset_name, amount, price, total, courtage, currency, isin "
        "FROM transactions WHERE transaction_type='Sälj' AND origin='avanza'"
    )
    sells = cur.fetchall()
    if not sells:
        return 0

    routed = 0
    for row in sells:
        rowid, tx_date, account, asset, amount, price, total, courtage, currency, isin = row
        sell_shares = abs(amount)

        cur.execute(
            "SELECT ca.account, SUM(ca.amount) AS held "
            "FROM cohort_assets ca JOIN assets a ON ca.asset_id = a.asset_id "
            "WHERE a.asset = ? AND ca.amount > 0 "
            "GROUP BY ca.account",
            (asset,)
        )
        holders = {r[0]: r[1] for r in cur.fetchall()}
        if not holders:
            continue  # nobody holds it yet (e.g. buy in same CSV) -> leave

        a_held = holders.get(account, 0)
        if a_held + 1e-6 >= sell_shares:
            continue  # account covers the sell

        family = _account_family(account, virtual_map)
        candidates = sorted(
            [(acc, h) for acc, h in holders.items() if acc != account and acc in family],
            key=lambda x: -x[1]
        )
        if not candidates:
            continue  # only unrelated holders — unexpected; leave for manual

        largest_acc, largest_held = candidates[0]
        shortfall = sell_shares - a_held

        if largest_held + 1e-6 < shortfall:
            logging.warning(
                f"Sell of {sell_shares} '{asset}' on '{account}' needs {shortfall:.4f} from virtuals "
                f"but largest holder '{largest_acc}' holds {largest_held:.4f}; left for manual allocation."
            )
            continue

        if len(candidates) > 1:
            logging.warning(
                f"Multiple virtuals hold '{asset}'; routing sell to '{largest_acc}' (largest holding). "
                f"Re-allocate manually if a different split was intended."
            )

        sign = -1 if amount < 0 else 1
        if a_held <= 1e-6:
            # Account holds none: move the entire sell to the virtual holder.
            cur.execute("UPDATE transactions SET account = ? WHERE rowid = ?", (largest_acc, rowid))
            logging.info(f"Auto-routed sell of {sell_shares} '{asset}' from '{account}' to '{largest_acc}'.")
        else:
            # Split: account sells what it holds, virtual sells the shortfall.
            frac = a_held / sell_shares
            acct_total = total * frac
            acct_courtage = courtage * frac
            cur.execute(
                "UPDATE transactions SET amount = ?, total = ?, courtage = ? WHERE rowid = ?",
                (sign * a_held, acct_total, acct_courtage, rowid)
            )
            cur.execute(
                "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
                "VALUES (?, ?, 'Sälj', ?, ?, ?, ?, ?, ?, ?, 'avanza')",
                (tx_date, largest_acc, asset, sign * shortfall, price,
                 total - acct_total, courtage - acct_courtage, currency, isin)
            )
            logging.info(
                f"Auto-split sell of {sell_shares} '{asset}': {a_held} on '{account}', "
                f"{shortfall} routed to '{largest_acc}'."
            )
        routed += 1

    if routed:
        db.commit()
    return routed


def route_imported_dividends_to_holders(db):
    """Distribute dividends across the accounts that actually hold the asset, so
    each account is credited for the shares it holds. Without this, a dividend
    on the physical account credits only that account's holdings (and dumps any
    leftover there), understating virtual portfolios that hold the shares.

    Rule per dividend (proportional, since a dividend is paid per share held):
      * if only the dividend's own account holds the asset -> leave
      * otherwise split the dividend across every related holder so each gets a
        row sized to its actual holdings (own account keeps/reuses the original
        row; every other holder gets a new row).
    No-op without virtuals. Returns the number of dividends redistributed.
    """
    db.connect()
    virtual_map = db.get_virtual_map()
    if not virtual_map:
        return 0
    cur = db.get_cursor()

    cur.execute(
        "SELECT rowid, date, account, asset_name, amount, price, total, courtage, currency, isin "
        "FROM transactions WHERE transaction_type='Utdelning' AND origin='avanza'"
    )
    dividends = cur.fetchall()
    if not dividends:
        return 0

    routed = 0
    for row in dividends:
        rowid, tx_date, account, asset, amount, dps, total, courtage, currency, isin = row
        cur.execute(
            "SELECT ca.account, SUM(ca.amount) AS held "
            "FROM cohort_assets ca JOIN assets a ON ca.asset_id = a.asset_id "
            "WHERE a.asset = ? AND ca.amount > 0 GROUP BY ca.account",
            (asset,)
        )
        holders = {r[0]: r[1] for r in cur.fetchall()}
        if not holders:
            continue
        others = {acc: s for acc, s in holders.items() if acc != account}
        if not others:
            continue  # only the dividend's own account holds; leave
        family = _account_family(account, virtual_map)
        others = {acc: s for acc, s in others.items() if acc in family}
        if not others:
            continue  # only unrelated holders; leave

        a_held = holders.get(account, 0)
        # Per-holder distribution sized to actual holdings: own account first
        # (reuses the original row), then each other holder (new rows).
        distribution = []
        if a_held > 1e-6:
            distribution.append((account, a_held))
        for acc, shares in others.items():
            distribution.append((acc, shares))
        if not distribution:
            continue

        # Split the original SEK total proportionally across holders instead
        # of recomputing shares * dps: the price column is in the instrument's
        # currency (e.g. DKK) while `total` is in SEK, so recomputing silently
        # mixes currencies and understates the dividend (issue #83).
        total_shares = sum(s for _, s in distribution)
        first_acc, first_shares = distribution[0]
        first_total = total * first_shares / total_shares
        cur.execute(
            "UPDATE transactions SET account = ?, amount = ?, total = ? WHERE rowid = ?",
            (first_acc, first_shares, first_total, rowid)
        )
        for acc, shares in distribution[1:]:
            cur.execute(
                "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
                "VALUES (?, ?, 'Utdelning', ?, ?, ?, ?, ?, ?, ?, 'avanza')",
                (tx_date, acc, asset, shares, dps, total * shares / total_shares, courtage, currency, isin)
            )
        logging.info(
            f"Auto-distributed dividend on '{asset}' ({amount} shares, total {total}) across holders: "
            f"{[(a, round(s, 2)) for a, s in distribution]}."
        )
        routed += 1

    if routed:
        db.commit()
    return routed


def auto_allocate_buys_to_virtuals(db):
    """Auto-allocate imported buys on parent accounts to the virtual that
    should hold them, using cash and holdings heuristics.

    Runs after auto-routing of sells/dividends, before reset_for_reprocessing.
    Uses the pre-import cohort snapshot (last-processed state) for capital and
    holdings lookups. No-op without virtuals.

    Heuristics per buy (Koep, origin='avanza') on a parent that cannot fund it:
      1. A virtual that both holds the asset and can be funded -> allocate there.
         If multiple, pick the largest holder (WARNING).
      2. New asset (nobody holds it) and exactly one virtual can fund -> allocate.
      3. Everything else -> leave with WARNING.

    'Can be funded' = virtual_capital + remaining_parent_capital >= buy_cost.
    The shortfall is transferred from parent to virtual via a direct Intern
    oeverfoering insert (origin='virtual'), dated the day before the buy.

    Returns the number of buys re-allocated.
    """
    db.connect()
    virtual_map = db.get_virtual_map()
    if not virtual_map:
        return 0
    cur = db.get_cursor()

    parents_with_virtuals = {}
    for v, p in virtual_map.items():
        parents_with_virtuals.setdefault(p, set()).add(v)
    if not parents_with_virtuals:
        return 0

    parent_list = list(parents_with_virtuals.keys())
    ph = ','.join('?' * len(parent_list))

    cur.execute(
        f"SELECT rowid, date, account, asset_name, amount, price, total "
        f"FROM transactions WHERE transaction_type='Köp' AND origin='avanza' "
        f"AND account IN ({ph}) ORDER BY date ASC, rowid ASC",
        parent_list
    )
    buys = cur.fetchall()
    if not buys:
        return 0

    # Running adjustments from transfers and buy consumptions within this
    # function.  Queried capital is the pre-import snapshot filtered to the
    # buy's month (capital from later months is not available yet at the
    # buy's date during reprocessing); adjustments reflect prior allocations.
    adjustments = {}

    def _avail(acc, buy_month):
        cur.execute(
            "SELECT COALESCE(SUM(capital), 0) FROM cohort_data "
            "WHERE account = ? AND capital > 0 AND month <= ?",
            (acc, buy_month)
        )
        return cur.fetchone()[0] + adjustments.get(acc, 0)

    allocated = 0
    for rowid, tx_date_str, account, asset, amount, price, total in buys:
        buy_cost = abs(total)
        tx_date_str = str(tx_date_str)  # normalise date objects from SQLite
        buy_month = tx_date_str[:7]

        # Step 0: Can the parent fund this buy alone?
        if _avail(account, buy_month) + 1e-3 >= buy_cost:
            continue

        virtuals = parents_with_virtuals[account]

        # Look up asset_id for holdings check
        cur.execute("SELECT asset_id FROM assets WHERE asset = ?", (asset,))
        asset_row = cur.fetchone()
        asset_id = asset_row[0] if asset_row else None

        # Step 1: Virtuals that both hold the asset AND can be funded
        holders_with_cash = []
        total_held_anywhere = 0.0
        if asset_id:
            cur.execute(
                "SELECT account, SUM(amount) AS held "
                "FROM cohort_assets WHERE asset_id = ? AND amount > 0 "
                "GROUP BY account",
                (asset_id,)
            )
            all_holders = {r[0]: r[1] for r in cur.fetchall()}
            total_held_anywhere = sum(all_holders.values())
            parent_cash = _avail(account, buy_month)
            for v in virtuals:
                held = all_holders.get(v, 0)
                if held > 1e-6:
                    v_cash = _avail(v, buy_month)
                    if v_cash + parent_cash + 1e-3 >= buy_cost:
                        holders_with_cash.append((v, held, v_cash))

        if holders_with_cash:
            holders_with_cash.sort(key=lambda x: -x[1])
            target, target_held, target_cash = holders_with_cash[0]
            if len(holders_with_cash) > 1:
                logging.warning(
                    f"Multiple virtuals hold '{asset}'; allocating buy of {abs(amount)} shares "
                    f"to '{target}' (largest holding of {target_held:.1f})."
                )
            else:
                logging.info(
                    f"Auto-allocated buy of {abs(amount)} '{asset}' on '{account}' -> '{target}' "
                    f"(holds {target_held:.1f} shares, can fund)."
                )
        elif total_held_anywhere < 1e-6:
            # Step 2: New asset (nobody holds it) -- which virtuals can fund?
            parent_cash = _avail(account, buy_month)
            fundable = []
            for v in virtuals:
                v_cash = _avail(v, buy_month)
                if v_cash + parent_cash + 1e-3 >= buy_cost:
                    fundable.append((v, v_cash))

            if len(fundable) == 1:
                target = fundable[0][0]
                target_cash = fundable[0][1]
                logging.info(
                    f"Auto-allocated buy of new asset '{asset}' on '{account}' -> '{target}' "
                    f"(only virtual with sufficient cash)."
                )
            else:
                if len(fundable) > 1:
                    logging.warning(
                        f"Buy of new asset '{asset}' on '{account}': parent can't fund "
                        f"({_avail(account, buy_month):.0f} SEK), multiple virtuals have cash "
                        f"-- manual allocation needed."
                    )
                else:
                    logging.warning(
                        f"Buy of '{asset}' on '{account}': no account can fund the "
                        f"{buy_cost:.0f} SEK cost -- manual allocation needed."
                    )
                continue
        else:
            # Step 3: Asset is held by virtual(s) but none can be funded
            logging.warning(
                f"Buy of '{asset}' on '{account}': held by virtual(s) but none can "
                f"be funded -- manual allocation needed."
            )
            continue

        # -- Execute allocation --
        cur.execute("UPDATE transactions SET account = ? WHERE rowid = ?", (target, rowid))

        # Fund: transfer shortfall from parent to virtual
        shortfall = max(0, buy_cost - target_cash)
        if shortfall > 1e-4:
            fund_date = str(_parse_exact_date(tx_date_str) - timedelta(days=1))
            cur.execute(
                "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
                "VALUES (?, ?, 'Intern överföring', ?, 0, 0, ?, 0, 'SEK', '-', 'virtual')",
                (fund_date, account, f"Transfer to {target}", -shortfall)
            )
            cur.execute(
                "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
                "VALUES (?, ?, 'Intern överföring', ?, 0, 0, ?, 0, 'SEK', '-', 'virtual')",
                (fund_date, target, f"Transfer from {account}", shortfall)
            )
            adjustments[account] = adjustments.get(account, 0) - shortfall
            adjustments[target] = adjustments.get(target, 0) + shortfall
            logging.info(
                f"  Moved {shortfall:.0f} SEK from '{account}' to '{target}' to fund the buy "
                f"(virtual had {target_cash:.0f} SEK)."
            )
        else:
            logging.info(
                f"  '{target}' has sufficient capital ({target_cash:.0f} SEK); no transfer needed."
            )

        adjustments[target] = adjustments.get(target, 0) - buy_cost
        allocated += 1

    if allocated:
        db.commit()
    return allocated


def _insert_internal_transfer_pair(db, from_acc, to_acc, amount, tx_date):
    """Insert a paired 'Intern överföring' (origin='virtual') moving `amount`
    from `from_acc` to `to_acc` on `tx_date`. The pair is consumed by
    handle_internal_transfer on reprocessing. Returns True on success.
    """
    cur = db.get_cursor()
    cur.execute("SELECT COALESCE(SUM(total), 0) FROM transactions WHERE account = ?", (from_acc,))
    bal = cur.fetchone()[0]
    if bal + 1e-4 < amount:
        logging.error(f"Source account '{from_acc}' has insufficient capital ({bal:.0f}) for transfer of {amount:.0f} SEK.")
        return False
    # Negative total on source (OUT), positive on destination (IN).
    cur.execute(
        "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
        "VALUES (?, ?, 'Intern överföring', ?, 0, 0, ?, 0, 'SEK', '-', 'virtual')",
        (tx_date, from_acc, f"Transfer to {to_acc}", -amount)
    )
    cur.execute(
        "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
        "VALUES (?, ?, 'Intern överföring', ?, 0, 0, ?, 0, 'SEK', '-', 'virtual')",
        (tx_date, to_acc, f"Transfer from {from_acc}", amount)
    )
    db.commit()
    return True


def account_create(args):
    """Create a virtual portfolio under a parent (physical) account."""
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()
    name = args.name.strip()
    parent = resolve_single_account(db, args.parent)

    if db.is_virtual_account(parent):
        logging.error(f"Parent account '{parent}' is itself a virtual portfolio. Nesting is not allowed.")
        return 1
    cur.execute("SELECT COUNT(*) FROM transactions WHERE account = ?", (parent,))
    if cur.fetchone()[0] == 0:
        logging.error(f"Parent account '{parent}' has no transactions. Use a real Avanza account.")
        return 1
    cur.execute("SELECT account_id FROM accounts WHERE account_id = ?", (name,))
    if cur.fetchone():
        logging.error(f"An account named '{name}' already exists.")
        return 1
    cur.execute("SELECT COUNT(*) FROM transactions WHERE account = ?", (name,))
    if cur.fetchone()[0] > 0:
        logging.error(f"Name '{name}' collides with an existing transaction account.")
        return 1

    cur.execute(
        "INSERT INTO accounts (account_id, nickname, is_virtual, parent_account) VALUES (?, ?, 1, ?)",
        (name, name, parent)
    )
    db.commit()
    logging.info(f"Created virtual portfolio '{name}' under parent '{parent}'.")

    if args.starting_cash and args.starting_cash > 0:
        tx_date = _parse_exact_date(args.starting_cash_date) if args.starting_cash_date else date.today()
        if _insert_internal_transfer_pair(db, parent, name, args.starting_cash, tx_date):
            logging.info(f"Funded '{name}' with {args.starting_cash:.0f} SEK from '{parent}'.")
            if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
                return 1
        else:
            logging.warning("Virtual portfolio created but not funded (insufficient capital on parent).")
            logging.warning("Fund it later with `account transfer-cash`.")
    return 0


def account_allocate(args):
    """Allocate a transaction (full or partial split) to a virtual portfolio,
    or undo a prior allocation by targeting the parent account."""
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()
    to_account = resolve_single_account(db, args.to)
    tx_date = _parse_exact_date(args.tx_date)
    asset = args.tx_asset.strip()

    # ── Undo mode: target is a physical (parent) account ──────────────────
    # Moves transactions back from a virtual to the parent and deletes the
    # funding transfer pair — no compensating transactions are created.
    if not db.is_virtual_account(to_account):
        if not args.from_account:
            logging.error("Undo requires --from <virtual> to identify which virtual to pull from.")
            return 1
        source = resolve_single_account(db, args.from_account)
        if not db.is_virtual_account(source):
            logging.error(f"Source '{source}' is not a virtual portfolio.")
            return 1
        actual_parent = db.get_account_parent(source)
        if to_account != actual_parent:
            logging.error(
                f"Target '{to_account}' is not the parent of virtual '{source}' "
                f"(parent is '{actual_parent}')."
            )
            return 1
        if args.shares is not None:
            logging.error(
                "Partial undo (--shares) is not supported. Undo the full allocation, "
                "then re-allocate with the correct split."
            )
            return 1

        cur.execute(
            "SELECT rowid, date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin "
            "FROM transactions WHERE date = ? AND account = ? AND asset_name = ? AND origin = 'avanza' "
            "ORDER BY rowid",
            (tx_date, source, asset)
        )
        matches = cur.fetchall()
        if not matches:
            logging.error(f"No transactions found on '{source}' for '{asset}' on {tx_date}.")
            return 1

        allocatable = ('Köp', 'Sälj', 'Utdelning', 'Räntor', 'Ränta', 'Inlåningsränta', 'Utlåningsränta',
                       'Tillgångsinsättning', 'Värdepappersuttag', 'Intern överföring',
                       'Insättning', 'Autogiroinsättning', 'Uttag')
        count = 0
        for m in matches:
            if m[3] not in allocatable:
                logging.warning(f"Skipping {m[3]} (rowid {m[0]}) — not allocatable.")
                continue
            cur.execute("UPDATE transactions SET account = ? WHERE rowid = ?", (to_account, m[0]))
            count += 1

        fund_date = tx_date - timedelta(days=1)
        cur.execute(
            "DELETE FROM transactions "
            "WHERE transaction_type = 'Intern överföring' AND origin = 'virtual' "
            "AND date = ? AND (account = ? OR account = ?)",
            (str(fund_date), to_account, source)
        )
        deleted = cur.rowcount

        db.commit()
        logging.info(
            f"Undid allocation: moved {count} transaction(s) from '{source}' back to '{to_account}', "
            f"deleted {deleted} funding transfer row(s)."
        )
        if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
            return 1
        return 0

    # ── Normal allocate mode: target is a virtual portfolio ───────────────
    parent = db.get_account_parent(to_account)
    source = resolve_single_account(db, args.from_account) if args.from_account else parent
    if not source:
        logging.error("No source account resolved (virtual has no parent and no --from given).")
        return 1

    cur.execute(
        "SELECT rowid, date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin "
        "FROM transactions WHERE date = ? AND account = ? AND asset_name = ? AND origin = 'avanza' "
        "ORDER BY rowid",
        (tx_date, source, asset)
    )
    matches = cur.fetchall()
    if not matches:
        logging.error(f"No transactions found on '{source}' for '{asset}' on {tx_date}.")
        return 1

    allocatable = ('Köp', 'Sälj', 'Utdelning', 'Räntor', 'Ränta', 'Inlåningsränta', 'Utlåningsränta',
                   'Tillgångsinsättning', 'Värdepappersuttag', 'Intern överföring', 'Insättning', 'Autogiroinsättning', 'Uttag')

    # Capital that must follow the shares: a buy (Köp) consumes capital, so when
    # it is moved to the virtual the virtual must be funded with the buy's cost,
    # otherwise reprocessing fails (the buy is unfundable on the virtual). We
    # transfer only the shortfall — if the virtual already has capital (e.g. from
    # a prior sell), the existing funds are used and no transfer is needed.
    buy_cost_to_move = 0.0

    if args.shares is None:
        count = 0
        for m in matches:
            if m[3] not in allocatable:
                logging.warning(f"Skipping {m[3]} (rowid {m[0]}) — not allocatable.")
                continue
            cur.execute("UPDATE transactions SET account = ? WHERE rowid = ?", (to_account, m[0]))
            if m[3] == 'Köp':
                buy_cost_to_move += abs(m[7])
            count += 1
        logging.info(f"Allocated {count} transaction(s) from '{source}' to '{to_account}'.")
    else:
        shares = args.shares
        split_count = 0
        for m in matches:
            if m[3] not in ('Köp', 'Sälj'):
                logging.warning(f"Partial --shares skipped for {m[3]} (rowid {m[0]}); only Köp/Sälj supported.")
                continue
            rowid, d, acc, ttype, aname, amount, price, total, courtage, currency, isin = m
            orig_shares = abs(amount)
            if shares > orig_shares + 1e-6:
                logging.error(f"Requested {shares} shares but rowid {rowid} only has {orig_shares}.")
                return 1
            if shares < orig_shares - 1e-6:
                remaining = orig_shares - shares
                frac = shares / orig_shares
                moved_total = total * frac
                moved_courtage = courtage * frac
                sign = 1 if amount >= 0 else -1
                cur.execute(
                    "UPDATE transactions SET amount = ?, total = ?, courtage = ? WHERE rowid = ?",
                    (sign * remaining, total - moved_total, courtage - moved_courtage, rowid)
                )
                cur.execute(
                    "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'avanza')",
                    (d, to_account, ttype, aname, sign * shares, price, moved_total, moved_courtage, currency, isin)
                )
                if ttype == 'Köp':
                    buy_cost_to_move += abs(moved_total)
                split_count += 1
            else:
                cur.execute("UPDATE transactions SET account = ? WHERE rowid = ?", (to_account, rowid))
                if ttype == 'Köp':
                    buy_cost_to_move += abs(total)
                split_count += 1
        logging.info(f"Split/allocated {split_count} transaction(s): {shares} shares to '{to_account}'.")

    if buy_cost_to_move > 1e-4:
        fund_date = tx_date - timedelta(days=1)
        buy_month = tx_date.strftime("%Y-%m")
        cur.execute(
            "SELECT COALESCE(SUM(capital), 0) FROM cohort_data "
            "WHERE account = ? AND capital > 0 AND month <= ?",
            (to_account, buy_month)
        )
        virtual_cash = cur.fetchone()[0]
        shortfall = buy_cost_to_move - virtual_cash
        if shortfall > 1e-4:
            if not _insert_internal_transfer_pair(db, source, to_account, shortfall, fund_date):
                db.conn.rollback()
                logging.error("Could not move capital to fund the allocated buy(s); rolled back.")
                return 1
            logging.info(
                f"Moved {shortfall:.0f} SEK from '{source}' to '{to_account}' to fund the allocated buy(s) "
                f"(virtual had {virtual_cash:.0f} SEK)."
            )
        else:
            logging.info(
                f"Virtual '{to_account}' has sufficient capital ({virtual_cash:.0f} SEK) "
                f"for the allocated buy(s); no transfer needed."
            )

    db.commit()
    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        return 1
    return 0


def account_transfer_cash(args):
    """Move cash between accounts via an internal transfer pair."""
    db = get_db(args)
    db.connect()
    from_acc = resolve_single_account(db, args.from_account)
    to_acc = resolve_single_account(db, args.to)
    tx_date = _parse_exact_date(args.date)
    amount = args.amount
    if amount <= 0:
        logging.error("Amount must be positive.")
        return 1
    if not _insert_internal_transfer_pair(db, from_acc, to_acc, amount, tx_date):
        return 1
    logging.info(f"Transferred {amount:.0f} SEK from '{from_acc}' to '{to_acc}' on {tx_date}.")
    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        return 1
    return 0


def _perform_asset_transfer(db, from_acc, to_acc, asset, shares, tx_date):
    """Insert the Sälj -> Intern överföring -> Köp rows for an asset move
    (all origin='virtual'). Performs lookups (price, currency, isin) internally.
    Does NOT commit or reprocess. Returns (proceeds, price) on success or None
    on failure (caller should rollback)."""
    cur = db.get_cursor()
    cur.execute("SELECT asset_id FROM assets WHERE asset = ?", (asset,))
    row = cur.fetchone()
    if not row:
        logging.error(f"Unknown asset '{asset}'.")
        return None
    asset_id = row[0]

    price, _, _, _ = db.get_price(asset_id, tx_date)
    if not price or price <= 0:
        logging.error(f"No price available for '{asset}' on {tx_date}; cannot value the transfer.")
        return None
    proceeds = shares * price

    cur.execute(
        "SELECT currency, isin FROM transactions WHERE asset_name = ? AND currency IS NOT NULL AND currency != '' ORDER BY rowid LIMIT 1",
        (asset,)
    )
    meta = cur.fetchone()
    currency = meta[0] if meta and meta[0] else 'SEK'
    isin = meta[1] if meta and meta[1] else '-'

    # 1. Sälj on source (amount negative, total positive proceeds)
    cur.execute(
        "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
        "VALUES (?, ?, 'Sälj', ?, ?, ?, ?, 0, ?, ?, 'virtual')",
        (tx_date, from_acc, asset, -shares, price, proceeds, currency, isin)
    )
    # 2. Cash transfer pair (source -> destination)
    if not _insert_internal_transfer_pair(db, from_acc, to_acc, proceeds, tx_date):
        return None
    # 3. Köp on destination (amount positive, total negative cost)
    cur.execute(
        "INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, origin) "
        "VALUES (?, ?, 'Köp', ?, ?, ?, ?, 0, ?, ?, 'virtual')",
        (tx_date, to_acc, asset, shares, price, -proceeds, currency, isin)
    )
    return (proceeds, price)


def account_transfer(args):
    """Move an asset position between accounts.

    Implemented as a decomposition (sell -> cash transfer -> rebuy), all rows
    tagged origin='virtual'. This composes the existing proven handlers, is
    correct on every statistics path, and gives the destination a fresh cost
    basis at the transfer price (the source realizes its gain up to the
    transfer — an honest 'this position left the strategy' bookkeeping).
    """
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()
    from_acc = resolve_single_account(db, args.from_account)
    to_acc = resolve_single_account(db, args.to)
    asset = args.asset.strip()
    shares = args.shares
    tx_date = _parse_exact_date(args.date)
    if shares <= 0:
        logging.error("Shares must be positive.")
        return 1

    cur.execute("SELECT asset_id FROM assets WHERE asset = ?", (asset,))
    row = cur.fetchone()
    if not row:
        logging.error(f"Unknown asset '{asset}'.")
        return 1
    asset_id = row[0]
    cur.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM cohort_assets WHERE asset_id = ? AND account = ? AND amount > 0",
        (asset_id, from_acc)
    )
    held = cur.fetchone()[0]
    if held + 1e-6 < shares:
        logging.error(f"Source '{from_acc}' holds only {held:.4f} shares of '{asset}'; cannot transfer {shares}.")
        return 1

    result = _perform_asset_transfer(db, from_acc, to_acc, asset, shares, tx_date)
    if result is None:
        db.conn.rollback()
        logging.error("Asset transfer failed (likely insufficient capital on source for the cash leg); rolled back.")
        return 1
    proceeds, price = result
    db.commit()
    logging.info(f"Transferred {shares} shares of '{asset}' from '{from_acc}' to '{to_acc}' @ {price:.2f} (value {proceeds:.0f} SEK).")
    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        return 1
    return 0


def account_list(args):
    """List all virtual portfolios with parent, cash, assets, total and APY."""
    db = get_db(args)
    db.connect()
    virtual_map = db.get_virtual_map()
    if not virtual_map:
        if getattr(args, 'format', 'table') == 'json':
            print("[]")
        else:
            print("No virtual portfolios.")
        return 0

    stat_calc = StatCalculator(db)
    summaries = {s[0]: s for s in stat_calc.get_account_summaries(None)}
    nicknames = db.get_all_account_nicknames()
    apy_mode = getattr(args, 'apy_mode', 'mwrr')

    rows = []
    for v_id in sorted(virtual_map):
        parent = virtual_map[v_id]
        s = summaries.get(v_id)
        cash = s[1] if s else 0.0
        assets = s[2] if s else 0.0
        total = s[3] if s else 0.0
        try:
            apy, _ = stat_calc.calculate_account_apy(v_id, apy_mode=apy_mode, current_value=total)
        except Exception:
            apy = None
        rows.append((v_id, parent, cash, assets, total, apy))

    if getattr(args, 'format', 'table') == 'json':
        import json
        data = [{
            'virtual': r[0],
            'display_name': nicknames.get(r[0], r[0]),
            'parent_account': r[1],
            'cash': r[2],
            'assets': r[3],
            'total': r[4],
            'apy': r[5],
        } for r in rows]
        print(json.dumps(data, indent=2))
    else:
        print(f"{'Virtual':<20} {'Parent':<14} {'Cash (SEK)':>12} {'Assets (SEK)':>12} {'Total (SEK)':>12} {'APY':>9}")
        print("-" * 83)
        for v_id, parent, cash, assets, total, apy in rows:
            apy_s = f"{apy:.1f}%" if apy is not None else "N/A"
            disp = nicknames.get(v_id, v_id)
            print(f"{disp:<20} {parent:<14} {cash:>12.0f} {assets:>12.0f} {total:>12.0f} {apy_s:>9}")
    return 0


def account_close(args):
    """Move all holdings and residual cash from a virtual portfolio back to a
    destination (its parent by default). The virtual account row is preserved so
    its historical cohort data remains available; it simply ends up empty."""
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()
    name = resolve_single_account(db, args.name)
    if not db.is_virtual_account(name):
        logging.error(f"'{args.name}' is not a virtual portfolio.")
        return 1
    parent = db.get_account_parent(name)
    dest = resolve_single_account(db, args.to) if getattr(args, 'to', None) else parent
    if not dest:
        logging.error("No destination account (virtual has no parent and no --to given).")
        return 1
    tx_date = _parse_exact_date(args.date)

    # Enumerate current holdings on the virtual (post-last-reprocess state).
    cur.execute(
        "SELECT a.asset, SUM(ca.amount) AS held "
        "FROM cohort_assets ca JOIN assets a ON ca.asset_id = a.asset_id "
        "WHERE ca.account = ? AND ca.amount > 0.0001 "
        "GROUP BY a.asset ORDER BY a.asset",
        (name,)
    )
    holdings = [(r[0], r[1]) for r in cur.fetchall()]

    # Residual cash currently sitting on the virtual (from funding not spent on assets).
    cur.execute("SELECT COALESCE(SUM(capital), 0) FROM cohort_data WHERE account = ?", (name,))
    residual_cash = cur.fetchone()[0]

    if not holdings and residual_cash <= 1e-4:
        logging.info(f"Virtual '{name}' has no holdings and no cash; nothing to close.")
        return 0

    moved_assets = 0
    for asset, shares in holdings:
        if _perform_asset_transfer(db, name, dest, asset, shares, tx_date) is None:
            db.conn.rollback()
            logging.error(f"Failed to transfer '{asset}' during close; rolled back.")
            return 1
        moved_assets += 1

    if residual_cash > 1e-4:
        if not _insert_internal_transfer_pair(db, name, dest, residual_cash, tx_date):
            db.conn.rollback()
            logging.error(f"Failed to move residual cash ({residual_cash:.0f} SEK) during close; rolled back.")
            return 1

    db.commit()
    logging.info(
        f"Closed virtual '{name}': moved {moved_assets} asset(s) + {residual_cash:.0f} SEK cash to '{dest}'. "
        f"Virtual account row preserved for history."
    )
    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        return 1
    return 0


def account_delete(args):
    """Delete a virtual portfolio and reverse all of its effects.

    Reverts origin='avanza' transactions back to the parent, deletes every
    origin='virtual' transaction tied to the virtual (including partner legs
    on other accounts), removes the account row, and reprocesses.

    Unlike 'close', which creates transfer transactions and preserves the
    account row for history, 'delete' is a clean teardown that leaves no
    trace of the virtual.
    """
    db = get_db(args)
    db.connect()
    cur = db.get_cursor()
    name = resolve_single_account(db, args.name)
    if not db.is_virtual_account(name):
        logging.error(f"'{args.name}' is not a virtual portfolio.")
        return 1
    parent = db.get_account_parent(name)
    if not parent:
        logging.error(f"Virtual '{name}' has no parent account; cannot determine revert target.")
        return 1

    if not confirm_irreversible(
        f"account delete will permanently remove virtual portfolio '{name}', revert its "
        "real transactions to '{parent}', delete every synthetic transaction tied to it, "
        "and erase its historical performance data.",
        getattr(args, 'yes', False),
    ):
        return 1
    backup_database(db, "account-delete")

    # Step 1: Collect (date, asset) pairs from asset-transfer legs on the virtual
    # so we can clean up partner Sälj/Köp rows on other accounts.
    cur.execute(
        "SELECT date, asset_name FROM transactions "
        "WHERE account = ? AND origin = 'virtual' AND transaction_type IN ('Sälj', 'Köp')",
        (name,)
    )
    transfer_pairs = [(r[0], r[1]) for r in cur.fetchall()]

    # Step 2: Revert real (avanza) transactions to the parent.
    cur.execute(
        "UPDATE transactions SET account = ? WHERE account = ? AND origin = 'avanza'",
        (parent, name)
    )
    reverted = cur.rowcount

    # Step 3: Delete all remaining transactions on the virtual (all origin='virtual').
    cur.execute("DELETE FROM transactions WHERE account = ?", (name,))
    deleted_on_v = cur.rowcount

    # Step 4: Delete Intern överföring partner legs on other accounts.
    cur.execute(
        "DELETE FROM transactions "
        "WHERE origin = 'virtual' AND transaction_type = 'Intern överföring' "
        "AND (asset_name = ? OR asset_name = ?)",
        (f"Transfer to {name}", f"Transfer from {name}")
    )
    deleted_partners = cur.rowcount

    # Step 5: Delete asset-transfer partner legs on other accounts.
    deleted_transfer_legs = 0
    for tx_date, asset in transfer_pairs:
        cur.execute(
            "DELETE FROM transactions "
            "WHERE origin = 'virtual' AND transaction_type IN ('Sälj', 'Köp') "
            "AND date = ? AND asset_name = ? AND account != ?",
            (tx_date, asset, parent)
        )
        deleted_transfer_legs += cur.rowcount

    # Step 6: Delete the account row.
    cur.execute("DELETE FROM accounts WHERE account_id = ?", (name,))

    db.commit()
    logging.info(
        f"Deleted virtual '{name}': reverted {reverted} transaction(s) to parent '{parent}', "
        f"removed {deleted_on_v} synthetic transaction(s) on '{name}', "
        f"{deleted_partners} transfer partner(s), {deleted_transfer_legs} asset-transfer partner(s)."
    )
    if reprocess_after_virtual_change(db, getattr(args, 'special_cases', None)) != 0:
        return 1
    return 0


def print_account_tree(stat_calc, db):
    """Print account summaries hierarchically: each physical account shows its
    combined (self + virtual children) value, with the children listed indented
    beneath. The TOTAL sums physical rows only (children are a breakdown, so no
    double counting)."""
    summaries = stat_calc.get_account_summaries(None)
    if not summaries:
        print("No account data found")
        return
    summary_map = {s[0]: s for s in summaries}
    virtual_map = db.get_virtual_map()
    nicknames = db.get_all_account_nicknames()

    children_of = {}
    for v_id, parent in virtual_map.items():
        children_of.setdefault(parent, []).append(v_id)

    def display(account):
        nick = nicknames.get(account)
        return nick if nick else account

    physical = [a for a in summary_map if a not in virtual_map]
    physical.sort(key=lambda a: summary_map[a][3], reverse=True)

    total_cash = total_assets = total_total = 0.0
    print(f"{'Account':<30} {'Cash (SEK)':>12} {'Assets (SEK)':>12} {'Total (SEK)':>12}")
    print("-" * 70)
    for phys in physical:
        ps = summary_map[phys]
        kids = sorted(children_of.get(phys, []), key=lambda v: summary_map.get(v, (0, 0, 0, 0))[3], reverse=True)
        kids = [k for k in kids if k in summary_map]
        comb_cash = ps[1] + sum(summary_map[k][1] for k in kids)
        comb_assets = ps[2] + sum(summary_map[k][2] for k in kids)
        comb_total = ps[3] + sum(summary_map[k][3] for k in kids)
        label = display(phys) + (" [incl. virtuals]" if kids else "")
        print(f"{label:<30} {comb_cash:>12.0f} {comb_assets:>12.0f} {comb_total:>12.0f}")
        for k in kids:
            ks = summary_map[k]
            klabel = "  -- " + display(k) + " [V]"
            print(f"{klabel:<30} {ks[1]:>12.0f} {ks[2]:>12.0f} {ks[3]:>12.0f}")
        total_cash += comb_cash
        total_assets += comb_assets
        total_total += comb_total

    # Orphaned virtuals (parent not present in summaries)
    for v_id, parent in virtual_map.items():
        if v_id in summary_map and parent not in summary_map:
            vs = summary_map[v_id]
            vlabel = "  -- " + display(v_id) + " [V]"
            print(f"{vlabel:<30} {vs[1]:>12.0f} {vs[2]:>12.0f} {vs[3]:>12.0f}")
            total_cash += vs[1]
            total_assets += vs[2]
            total_total += vs[3]

    print("-" * 70)
    print(f"{'TOTAL':<30} {total_cash:>12.0f} {total_assets:>12.0f} {total_total:>12.0f}")


def report(args):
    """Generate an investment report with a virtual-portfolio section and a
    virtual-vs-parent-vs-benchmark performance comparison.

    Reuses calculate_account_apy for per-account returns, the
    v_virtual_portfolio_rollup view for combined totals, and (optionally)
    Yahoo Finance for the benchmark period return.
    """
    db = get_db(args)
    db.interpolate = not getattr(args, 'no_interpolation', False)
    apy_mode = getattr(args, 'apy_mode', 'mwrr')
    benchmark = getattr(args, 'benchmark', None)
    fmt = getattr(args, 'format', 'table')

    update_all = getattr(args, 'update_all', False)
    if getattr(args, 'update_prices', 'auto') == 'always':
        try:
            StatCalculator(db).update_prices(force=True, update_all=update_all)
            db.set_metadata('last_price_update', datetime.now().isoformat())
            db.set_metadata('last_stats_calculation', '')
        except Exception as e:
            logging.error(f"Failed to update prices: {e}")
            return 1
    elif getattr(args, 'update_prices', 'auto') == 'auto':
        fresh, _ = prices_are_fresh(db, update_all=update_all)
        if not fresh or any_assets_need_prices(db, update_all=update_all):
            try:
                StatCalculator(db).update_prices(force=True, update_all=update_all)
                db.set_metadata('last_price_update', datetime.now().isoformat())
                db.set_metadata('last_stats_calculation', '')
            except Exception as e:
                logging.warning(f"Price update skipped: {e}")

    db.connect()
    cur = db.get_cursor()
    stat_calc = StatCalculator(db)
    summaries = {s[0]: s for s in stat_calc.get_account_summaries(None)}
    virtual_map = db.get_virtual_map()
    nicknames = db.get_all_account_nicknames()

    apy = {}
    for acc in summaries:
        try:
            a, _ = stat_calc.calculate_account_apy(acc, apy_mode=apy_mode, current_value=summaries[acc][3])
        except Exception:
            a = None
        apy[acc] = a

    cur.execute(
        "SELECT parent_account, parent_display_name, own_total, virtual_total, combined_total, virtual_count "
        "FROM v_virtual_portfolio_rollup"
    )
    rollup = {}
    for r in cur.fetchall():
        rollup[r[0]] = dict(zip(
            ['parent_account', 'parent_display_name', 'own_total', 'virtual_total', 'combined_total', 'virtual_count'], r))

    physical = sorted((a for a in summaries if a not in virtual_map),
                      key=lambda a: summaries[a][3], reverse=True)
    total_value = sum(s[3] for s in summaries.values())
    phys_own = sum(summaries[a][3] for a in physical)
    virt_total = sum(summaries[a][3] for a in virtual_map if a in summaries)

    dep = withd = 0.0
    if physical:
        ph = ",".join("?" for _ in physical)
        cur.execute(
            f"SELECT COALESCE(SUM(deposit),0), COALESCE(SUM(withdrawal),0) FROM cohort_data WHERE account IN ({ph})",
            physical)
        dep, withd = cur.fetchone()
    net_invested = (dep or 0) - (withd or 0)
    total_gain = total_value - net_invested
    try:
        blended, _ = stat_calc.calculate_account_apy('all', apy_mode=apy_mode, current_value=total_value)
    except Exception:
        blended = None

    # Optional benchmark period return (annualized) over the portfolio's lifetime
    benchmark_apy = None
    if benchmark:
        min_date_str, _ = db.get_date_range()
        if min_date_str:
            try:
                from risk_calculator import fetch_yahoo_benchmark_prices, get_benchmark_price
                start = datetime.strptime(str(min_date_str)[:10], "%Y-%m-%d").date()
                end = date.today()
                prices = fetch_yahoo_benchmark_prices(benchmark, start, end)
                if prices:
                    sp = get_benchmark_price(prices, start)
                    ep = get_benchmark_price(prices, end)
                    days = (end - start).days
                    if sp and sp > 0 and ep > 0 and days > 0:
                        benchmark_apy = 100 * ((ep / sp) ** (365.0 / days) - 1)
            except Exception as e:
                logging.warning(f"Could not compute benchmark return: {e}")

    children_of = {}
    for v, p in virtual_map.items():
        children_of.setdefault(p, []).append(v)

    def fmt_apy(v):
        return f"{v:.1f}%" if v is not None else "N/A"

    if fmt == 'json':
        import json
        def acc_node(a):
            s = summaries.get(a)
            return {
                'account': a,
                'display_name': nicknames.get(a, a),
                'is_virtual': a in virtual_map,
                'parent_account': virtual_map.get(a),
                'cash': s[1] if s else 0.0,
                'assets': s[2] if s else 0.0,
                'total': s[3] if s else 0.0,
                'apy': apy.get(a),
            }
        accounts_tree = []
        for pa in physical:
            node = acc_node(pa)
            node['children'] = [acc_node(v) for v in sorted(children_of.get(pa, []), key=lambda x: summaries.get(x, (0, 0, 0, 0))[3], reverse=True) if v in summaries]
            accounts_tree.append(node)
        virtual_section = []
        for v in sorted(virtual_map):
            if v not in summaries:
                continue
            p = virtual_map[v]
            comb = rollup.get(p, {}).get('combined_total') or 0.0
            vt = summaries[v][3]
            virtual_section.append({
                'virtual': v, 'parent_account': p, 'value': vt, 'apy': apy.get(v),
                'pct_of_combined': (vt / comb * 100) if comb > 0 else 0.0,
            })
        result = {
            'as_of': date.today().isoformat(),
            'overview': {
                'physical_count': len(physical),
                'virtual_count': len(virtual_map),
                'total_value': total_value,
                'physical_own': phys_own,
                'virtual_total': virt_total,
                'total_deposited': dep or 0,
                'total_withdrawn': withd or 0,
                'total_gain': total_gain,
                'total_gain_pct': (total_gain / net_invested * 100) if net_invested > 0 else 0.0,
                'blended_apy': blended,
                'apy_mode': apy_mode,
            },
            'accounts': accounts_tree,
            'virtual_portfolios': virtual_section,
            'comparison': {
                'benchmark': benchmark,
                'benchmark_apy': benchmark_apy,
                'rows': [
                    {
                        'account': a, 'display_name': nicknames.get(a, a),
                        'type': 'virtual' if a in virtual_map else 'physical',
                        'apy': apy.get(a),
                        'vs_parent': (apy[a] - apy[virtual_map[a]])
                                     if (a in virtual_map and apy.get(a) is not None and apy.get(virtual_map[a]) is not None)
                                     else None,
                        'vs_benchmark': (apy[a] - benchmark_apy)
                                        if (benchmark_apy is not None and apy.get(a) is not None) else None,
                    }
                    for a in list(physical) + sorted(virtual_map) if a in summaries
                ],
            },
        }
        print(json.dumps(result, indent=2))
        return 0

    # ---- text report ----
    print(f"=== Investment Report (as of {date.today().isoformat()}) ===\n")
    print("Portfolio overview")
    print(f"  Physical accounts:   {len(physical)}")
    print(f"  Virtual portfolios:  {len(virtual_map)}")
    print(f"  Total value:         {total_value:,.0f} SEK")
    print(f"    (physical own:     {phys_own:,.0f}  +  virtual:  {virt_total:,.0f})")
    print(f"  Total deposited:     {dep or 0:,.0f} SEK")
    gl_sign = "+" if total_gain >= 0 else ""
    gl_pct = (total_gain / net_invested * 100) if net_invested > 0 else 0.0
    print(f"  Total gain:          {gl_sign}{total_gain:,.0f} SEK ({gl_sign}{gl_pct:.1f}%)")
    print(f"  Blended APY (all):   {fmt_apy(blended)} ({apy_mode.upper()})")

    print("\nAccounts")
    print(f"  {'Account':<24} {'Cash':>10} {'Assets':>10} {'Total':>10} {'APY':>8}")
    print("  " + "-" * 66)
    for pa in physical:
        s = summaries[pa]
        print(f"  {nicknames.get(pa, pa):<24} {s[1]:>10,.0f} {s[2]:>10,.0f} {s[3]:>10,.0f} {fmt_apy(apy.get(pa)):>8}")
        for v in sorted(children_of.get(pa, []), key=lambda x: summaries.get(x, (0, 0, 0, 0))[3], reverse=True):
            if v not in summaries:
                continue
            vs = summaries[v]
            label = (nicknames.get(v, v) + " [V]")[:24]
            print(f"    -- {label:<22} {vs[1]:>10,.0f} {vs[2]:>10,.0f} {vs[3]:>10,.0f} {fmt_apy(apy.get(v)):>8}")

    if virtual_map:
        print("\nVirtual portfolios")
        print(f"  {'Virtual':<16} {'Parent':<10} {'Value':>10} {'APY':>8} {'% of combined':>14}")
        print("  " + "-" * 62)
        for v in sorted(virtual_map):
            if v not in summaries:
                continue
            p = virtual_map[v]
            comb = rollup.get(p, {}).get('combined_total') or 0.0
            vt = summaries[v][3]
            pct = (vt / comb * 100) if comb > 0 else 0.0
            print(f"  {nicknames.get(v, v):<16} {p:<10} {vt:>10,.0f} {fmt_apy(apy.get(v)):>8} {pct:>13.1f}%")

    print("\nPerformance comparison" + (f" vs {benchmark}" if benchmark else ""))
    header = f"  {'Account':<24} {'Type':<10} {'APY':>8} {'vs parent':>11}"
    if benchmark:
        header += f" {'vs benchmark':>14}"
    print(header)
    print("  " + "-" * (66 + (14 if benchmark else 0)))
    for a in physical:
        line = f"  {nicknames.get(a, a):<24} {'physical':<10} {fmt_apy(apy.get(a)):>8} {'--':>11}"
        if benchmark and benchmark_apy is not None and apy.get(a) is not None:
            line += f" {apy[a] - benchmark_apy:>+13.1f} pp"
        print(line)
    for v in sorted(virtual_map):
        if v not in summaries:
            continue
        p = virtual_map[v]
        vs_parent = (apy[v] - apy[p]) if (apy.get(v) is not None and apy.get(p) is not None) else None
        vstr = f"{vs_parent:>+10.1f} pp" if vs_parent is not None else f"{'--':>11}"
        line = f"  {nicknames.get(v, v):<24} {'virtual':<10} {fmt_apy(apy.get(v)):>8} {vstr}"
        if benchmark and benchmark_apy is not None and apy.get(v) is not None:
            line += f" {apy[v] - benchmark_apy:>+13.1f} pp"
        print(line)
    if benchmark:
        print(f"  {benchmark:<24} {'benchmark':<10} {fmt_apy(benchmark_apy):>8}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Avanza investment tracker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s import transactions.csv
  %(prog)s stats --update-prices auto
  %(prog)s status
        """
    )
    
    parser.add_argument(
        '--database',
        default='data/asset_data.db',
        help='Path to SQLite database (default: data/asset_data.db)'
    )
    parser.add_argument(
        '--special-cases',
        default='data/special_cases.json',
        help='Path to special cases JSON file (default: data/special_cases.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import CSV data and process transactions')
    import_parser.add_argument('file', help='Path to CSV file')
    import_parser.add_argument(
        '--allocate-virtual', action='store_true',
        help='Auto-allocate buys to virtual portfolios using cash + holdings heuristics'
    )
    import_parser.add_argument(
        '--allow-unsettled', action='store_true',
        help='Import pending-nota trades (non-SEK buy/sell with empty Courtage/Valutakurs) instead of deferring them'
    )
    import_parser.set_defaults(func=import_data)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics with smart updates')
    stats_parser.add_argument(
        '--period',
        choices=['default', 'month', 'year'],
        default='default',
        help='Time period to show (default)'
    )
    stats_parser.add_argument(
        '--deposits',
        choices=['current', 'all'],
        default='current',
        help='Which deposits to include (default: current)'
    )
    stats_parser.add_argument(
        '--accumulated',
        action='store_true',
        help='Show accumulated statistics'
    )
    stats_parser.add_argument(
        '--update-prices',
        choices=['auto', 'always', 'never'],
        default='auto',
        help='When to update prices (default: auto)'
    )
    stats_parser.add_argument(
        '--update-all',
        action='store_true',
        help='Update all assets in database regardless of whether they are currently held'
    )
    stats_parser.add_argument(
        '--force',
        action='store_true',
        help='Force statistics recalculation'
    )
    stats_parser.add_argument(
        '--account',
        default=None,
        help='Accounts to include: omit for physical-only (default), "all" includes virtual portfolios, "default", or comma-separated list'
    )
    stats_parser.add_argument(
        '--apy-mode',
        choices=['mwrr', 'twrr'],
        default='mwrr',
        help='APY calculation method (default: mwrr)'
    )
    stats_parser.add_argument(
        '--as-of',
        default=None,
        help='Show statistics as of a previous date (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    stats_parser.add_argument(
        '--cohorts-start',
        default=None,
        help='Start date for filtering cohorts by creation date (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    stats_parser.add_argument(
        '--cohorts-end',
        default=None,
        help='End date for filtering cohorts by creation date (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    stats_parser.add_argument(
        '--cohort',
        default=None,
        help='Shorthand to filter by a single cohort month (YYYY-MM) or year (YYYY) (default: None)'
    )
    stats_parser.add_argument(
        '--from',
        dest='from_date',
        default=None,
        help='Start date for valuation performance period (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    stats_parser.add_argument(
        '--to',
        default=None,
        help='End date for valuation performance period (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    stats_parser.add_argument(
        '--positions', '-p',
        action='store_true',
        help='Show asset positions/holdings for each cohort'
    )
    stats_parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Consolidate cohort stats and positions into a single overview'
    )
    stats_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    stats_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress price data staleness warnings'
    )
    stats_parser.add_argument(
        '--no-interpolation',
        action='store_true',
        help='Disable linear interpolation for sparse historical price data'
    )
    stats_parser.add_argument(
        '--risk',
        action='store_true',
        help='Calculate and display portfolio-level risk metrics (Stddev, Sharpe, Sortino, Max Drawdown)'
    )
    stats_parser.add_argument(
        '--beta',
        nargs='?',
        const='^OMXSPI',
        default=None,
        help='Include beta calculation vs specified benchmark (default: ^OMXSPI if flag is passed)'
    )
    stats_parser.set_defaults(func=stats)
    
    # Settings command
    settings_parser = subparsers.add_parser('settings', help='Manage settings')
    settings_subparsers = settings_parser.add_subparsers(dest='settings_command', help='Settings command')
    
    # Default stats period subcommand
    default_stats_period_parser = settings_subparsers.add_parser('default-stats-period', help='Set default stats period')
    default_stats_period_parser.add_argument('period', choices=['month', 'year'], help='Default period: "month" or "year"')
    default_stats_period_parser.set_defaults(func=settings_default_stats_period)

    # Default accounts subcommand
    default_accounts_parser = settings_subparsers.add_parser('default-accounts', help='Set default accounts')
    default_accounts_parser.add_argument('accounts', help='Comma-separated list of account numbers, or "all" for all accounts')
    default_accounts_parser.set_defaults(func=settings_default_accounts)

    # Accounts command (show account summaries)
    accounts_parser = subparsers.add_parser('accounts', help='Show account summaries with asset values and cash')
    accounts_parser.add_argument(
        '--account',
        default=None,
        help='Accounts to include: omit for the full tree (default), "all", "default", or comma-separated list'
    )
    accounts_parser.add_argument(
        '--update-prices',
        choices=['auto', 'always', 'never'],
        default='auto',
        help='When to update prices (default: auto)'
    )
    accounts_parser.add_argument(
        '--update-all',
        action='store_true',
        help='Update all assets in database regardless of whether they are currently held'
    )
    accounts_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    accounts_parser.set_defaults(func=accounts_summary)
    
    # Portfolio command (show portfolio snapshot)
    portfolio_parser = subparsers.add_parser('portfolio', help='Show portfolio snapshot')
    portfolio_parser.add_argument(
        '--as-of',
        default=None,
        help='Valuation date (YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    portfolio_parser.add_argument(
        '--cohorts-start',
        default=None,
        help='Start date for filtering cohorts by creation date (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    portfolio_parser.add_argument(
        '--cohorts-end',
        default=None,
        help='End date for filtering cohorts by creation date (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    portfolio_parser.add_argument(
        '--cohort',
        default=None,
        help='Shorthand to filter by a single cohort month (YYYY-MM) or year (YYYY) (default: None)'
    )
    portfolio_parser.add_argument(
        '--from',
        dest='from_date',
        default=None,
        help='Start date for valuation performance period (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    portfolio_parser.add_argument(
        '--to',
        default=None,
        help='End date for valuation performance period (formats: YYYY, YYYY-MM, YYYY-MM-DD)'
    )
    portfolio_parser.add_argument(
        '--account',
        default=None,
        help='Accounts to include: omit for physical-only (default), "all" includes virtual portfolios, "default", or comma-separated list'
    )
    portfolio_parser.add_argument(
        '--apy-mode',
        choices=['mwrr', 'twrr'],
        default='mwrr',
        help='APY calculation method (default: mwrr)'
    )
    portfolio_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    portfolio_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress price data staleness warnings'
    )
    portfolio_parser.add_argument(
        '--no-interpolation',
        action='store_true',
        help='Disable linear interpolation for sparse historical price data'
    )
    portfolio_parser.add_argument(
        '--risk',
        action='store_true',
        help='Calculate and display portfolio-level risk metrics (Stddev, Sharpe, Sortino, Max Drawdown)'
    )
    portfolio_parser.add_argument(
        '--beta',
        nargs='?',
        const='^OMXSPI',
        default=None,
        help='Include beta calculation vs specified benchmark (default: ^OMXSPI if flag is passed)'
    )
    portfolio_parser.set_defaults(func=portfolio)
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export transactions to CSV')
    export_parser.add_argument(
        '--output',
        default='transactions_export.csv',
        help='Path to the output CSV file (default: transactions_export.csv)'
    )
    export_parser.add_argument(
        '--account',
        default=None,
        help='Account ID or display name to filter (omit for all including virtual)'
    )
    export_parser.set_defaults(func=export_transactions)

    # Virtual portfolios command group (issue #74)
    account_parser = subparsers.add_parser(
        'account', help='Manage accounts: virtual sub-portfolios and nicknames'
    )
    account_sub = account_parser.add_subparsers(dest='account_command')

    ap_create = account_sub.add_parser('create', help='Create a virtual sub-portfolio under a parent account')
    ap_create.add_argument('--name', required=True, help='Name for the sub-portfolio (used as its account ID)')
    ap_create.add_argument('--parent', required=True, help='Parent (physical) account ID or nickname')
    ap_create.add_argument('--starting-cash', type=float, default=None, help='Optional starting cash to transfer from parent')
    ap_create.add_argument('--starting-cash-date', default=None, help='Date for the starting cash transfer (YYYY-MM-DD; default today)')
    ap_create.set_defaults(func=account_create)

    ap_alloc = account_sub.add_parser('allocate', help='Allocate a transaction (full or partial split) to a virtual sub-portfolio')
    ap_alloc.add_argument('--tx-date', required=True, help='Transaction date (YYYY-MM-DD)')
    ap_alloc.add_argument('--tx-asset', required=True, help='Asset name of the transaction')
    ap_alloc.add_argument('--to', required=True, help='Virtual sub-portfolio to allocate to')
    ap_alloc.add_argument('--from', dest='from_account', default=None, help="Source account (default: the sub-portfolio's parent)")
    ap_alloc.add_argument('--shares', type=float, default=None, help='Shares to allocate (partial split); omit for full allocation')
    ap_alloc.set_defaults(func=account_allocate)

    ap_cash = account_sub.add_parser('transfer-cash', help='Move cash between accounts')
    ap_cash.add_argument('--amount', type=float, required=True, help='Amount (SEK) to transfer')
    ap_cash.add_argument('--from', dest='from_account', required=True, help='Source account')
    ap_cash.add_argument('--to', required=True, help='Destination account')
    ap_cash.add_argument('--date', required=True, help='Transfer date (YYYY-MM-DD)')
    ap_cash.set_defaults(func=account_transfer_cash)

    ap_xfer = account_sub.add_parser('transfer', help='Move an asset position between accounts (sell -> cash -> rebuy)')
    ap_xfer.add_argument('--asset', required=True, help='Asset name to transfer')
    ap_xfer.add_argument('--shares', type=float, required=True, help='Number of shares to transfer')
    ap_xfer.add_argument('--from', dest='from_account', required=True, help='Source account')
    ap_xfer.add_argument('--to', required=True, help='Destination account')
    ap_xfer.add_argument('--date', required=True, help='Transfer date (YYYY-MM-DD)')
    ap_xfer.set_defaults(func=account_transfer)

    ap_list = account_sub.add_parser('list', help='List all virtual sub-portfolios with value and APY')
    ap_list.add_argument('--apy-mode', choices=['mwrr', 'twrr'], default='mwrr', help='APY calculation method (default: mwrr)')
    ap_list.add_argument('--format', choices=['table', 'json'], default='table', help='Output format (default: table)')
    ap_list.set_defaults(func=account_list)

    ap_close = account_sub.add_parser('close', help='Move all holdings and cash back to parent (liquidate/merge a sub-portfolio)')
    ap_close.add_argument('--name', required=True, help='Virtual sub-portfolio to close')
    ap_close.add_argument('--to', default=None, help="Destination account (default: the sub-portfolio's parent)")
    ap_close.add_argument('--date', required=True, help='Close date (YYYY-MM-DD)')
    ap_close.set_defaults(func=account_close)

    # Delete: clean teardown (revert transactions, remove all traces)
    ap_delete = account_sub.add_parser('delete', help='Delete a virtual portfolio and reverse all of its effects')
    ap_delete.add_argument('--name', required=True, help='Virtual sub-portfolio to delete')
    ap_delete.add_argument('--yes', action='store_true',
        help='Skip the destructive-operation confirmation (for non-interactive use)')
    ap_delete.set_defaults(func=account_delete)

    # Nickname management (moved here from `settings account-nickname`)
    ap_nick = account_sub.add_parser('nickname', help='Set, list, or remove account nicknames')
    ap_nick.add_argument('account', nargs='?', help='Account to set nickname for')
    ap_nick.add_argument('nickname', nargs='?', help='Nickname for the account')
    ap_nick.add_argument('--remove', metavar='ACCOUNT', help='Remove nickname for specified account')
    ap_nick.add_argument('--list', action='store_true', help='List all account nicknames')
    ap_nick.set_defaults(func=account_nickname)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    status_parser.set_defaults(func=status)

    # Report command (issue #74 phase 3): virtual section + benchmark comparison
    report_parser = subparsers.add_parser(
        'report', help='Investment report with a virtual-portfolio section and benchmark comparison')
    report_parser.add_argument(
        '--benchmark', nargs='?', const='^OMXSPI', default=None,
        help='Benchmark ticker for the performance comparison (default: ^OMXSPI if flag is passed)')
    report_parser.add_argument(
        '--apy-mode', choices=['mwrr', 'twrr'], default='mwrr', help='APY calculation method (default: mwrr)')
    report_parser.add_argument(
        '--update-prices', choices=['auto', 'always', 'never'], default='auto',
        help='When to update prices (default: auto)')
    report_parser.add_argument(
        '--update-all', action='store_true', help='Update prices for all assets, held or not')
    report_parser.add_argument(
        '--format', choices=['table', 'json'], default='table', help='Output format (default: table)')
    report_parser.add_argument(
        '--no-interpolation', action='store_true', help='Disable linear price interpolation')
    report_parser.set_defaults(func=report)

    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset database state')
    reset_parser.add_argument(
        '--hard',
        action='store_true',
        help='Hard reset: delete all transactions, stats, and prices'
    )
    reset_parser.add_argument(
        '--yes',
        action='store_true',
        help='Skip the destructive-operation confirmation (for non-interactive use)'
    )
    reset_parser.set_defaults(func=reset)

    # delete-tx command (issue #80)
    deltx_parser = subparsers.add_parser(
        'delete-tx',
        help='Delete individual transaction(s) and rebuild derived tables')
    deltx_mode = deltx_parser.add_mutually_exclusive_group(required=True)
    deltx_mode.add_argument('--tx-id', type=int,
        help='Delete a single transaction by internal rowid (most precise)')
    deltx_mode.add_argument('--date',
        help='Exact date YYYY-MM-DD (requires --asset)')
    deltx_mode.add_argument('--since',
        help='Delete all transactions on/after YYYY-MM-DD (optionally filtered by --account)')
    deltx_parser.add_argument('--asset', help='Asset name to match (requires --date)')
    deltx_parser.add_argument('--account', help='Restrict matching to one account (id or nickname)')
    deltx_parser.add_argument('--cascade', action='store_true',
        help='Also delete related rows across the account family (same date+asset)')
    deltx_parser.add_argument('--dry-run', action='store_true',
        help='Show what would be deleted without writing')
    deltx_parser.add_argument('--yes', action='store_true',
        help='Skip the destructive-operation confirmation (for non-interactive use)')
    deltx_parser.set_defaults(func=delete_tx)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'account' and not getattr(args, 'account_command', None):
        account_parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())