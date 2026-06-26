"""
pnl.py — P&L calculator using Binance trade history (FIFO method)

Fixes applied:
- 90-day window → 365 days (90-day window gave wrong cost basis for anything
  bought earlier — old purchases were missing, making unrealised P&L fiction)
- limit 500 → 1000 (Binance supports up to 1000; 500 silently missed trades)
- Commission column removed — was computing BNB_qty * BTC_price = nonsense;
  replaced with a disclaimer in the footer
- Hardcoded ["BTC","ETH","BNB"] fallback removed — failing API should fail loudly
- Export uses timestamped filename — prevents silently overwriting previous exports
- Optional[dict] instead of dict|None — Python 3.9 compatibility
- Removed unused Panel import
"""
import csv
import logging
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()

DATA_DIR   = Path(__file__).parent.parent / "data"
DEFAULT_DAYS = 365


class PnLCalculator:
    """FIFO-based P&L calculator using Binance trade history, with journal fallback."""

    def __init__(self, client, market, portfolio, journal=None):
        self.client    = client
        self.market    = market
        self.portfolio = portfolio
        self.journal   = journal  # Optional DecisionJournal for fallback
        self._convert_cache = None  # Cache convert trades to avoid repeated API calls
        self._convert_cache_days = None

    def _get_trades(self, symbol: str, days: int = DEFAULT_DAYS) -> list:
        try:
            start_ms = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
            trades   = self.client.my_trades(symbol=symbol, limit=1000, startTime=start_ms)
            return trades or []
        except Exception as e:
            logger.warning(f"Could not fetch trades for {symbol}: {e}")
            return []

    def _get_convert_trades(self, days: int = DEFAULT_DAYS) -> list:
        """
        Fetch Binance Convert trades (users who DCA via Convert instead of spot).
        Uses /sapi/v1/convert/tradeFlow endpoint.
        Returns normalized list compatible with my_trades format.
        Results are cached to avoid repeated API calls.
        """
        # Return cached result if available for same or longer window
        if self._convert_cache is not None and self._convert_cache_days and self._convert_cache_days >= days:
            return self._convert_cache

        try:
            start_ms = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
            end_ms   = int(datetime.now().timestamp() * 1000)

            # Binance Convert API requires signed request
            response = self.client.send_request(
                "GET",
                "/sapi/v1/convert/tradeFlow",
                {"startTime": start_ms, "endTime": end_ms, "limit": 1000}
            )

            if not response or "list" not in response:
                return []

            normalized = []
            for trade in response["list"]:
                # Convert trade structure:
                # {quoteId, orderId, orderStatus, fromAsset, fromAmount, toAsset, toAmount, ...}
                from_asset = trade.get("fromAsset", "")
                to_asset   = trade.get("toAsset", "")
                from_amt   = float(trade.get("fromAmount", 0))
                to_amt     = float(trade.get("toAmount", 0))
                ts         = trade.get("createTime", 0)

                # Determine if this is a BUY or SELL from crypto perspective
                # If fromAsset is stablecoin → buying crypto (toAsset)
                # If toAsset is stablecoin → selling crypto (fromAsset)
                stables = {"USDT", "USDC", "BUSD", "FDUSD", "DAI", "TUSD"}

                if from_asset in stables:
                    # Buying crypto with stablecoin
                    symbol = to_asset + from_asset
                    price  = from_amt / to_amt if to_amt > 0 else 0
                    normalized.append({
                        "symbol":  symbol,
                        "isBuyer": True,
                        "price":   price,
                        "qty":     to_amt,
                        "time":    ts,
                        "id":      f"convert_{trade.get('orderId', ts)}",
                        "source":  "convert",
                    })
                elif to_asset in stables:
                    # Selling crypto for stablecoin
                    symbol = from_asset + to_asset
                    price  = to_amt / from_amt if from_amt > 0 else 0
                    normalized.append({
                        "symbol":  symbol,
                        "isBuyer": False,
                        "price":   price,
                        "qty":     from_amt,
                        "time":    ts,
                        "id":      f"convert_{trade.get('orderId', ts)}",
                        "source":  "convert",
                    })
                else:
                    # Crypto-to-crypto swap (e.g., BTC → ETH)
                    # Treat as sell fromAsset, buy toAsset
                    # For P&L purposes, we need a USD price — skip these for now
                    logger.debug(f"Skipping crypto-to-crypto convert: {from_asset} → {to_asset}")

            # Cache results
            self._convert_cache = normalized
            self._convert_cache_days = days
            return normalized

        except Exception as e:
            logger.debug(f"Convert trades fetch failed (may not be enabled): {e}")
            return []

    def _get_trades_extended(self, symbol: str) -> tuple:
        """Try progressively wider windows. Returns (trades, days_used)."""
        for days in [365, 730, 1095]:
            trades = self._get_trades(symbol, days=days)
            if trades:
                return trades, days
        return [], 365

    def diagnose_api(self) -> dict:
        """Check why my_trades might be returning nothing."""
        result = {"permissions": [], "account_ok": False, "sample_trades": 0, 
                  "convert_trades": 0, "notes": []}
        try:
            account = self.client.account()
            result["permissions"]  = account.get("permissions", [])
            result["account_ok"]   = True
        except Exception as e:
            result["notes"].append(f"Account fetch failed: {e}")
            return result

        # Try BTC trades with no time filter
        try:
            trades = self.client.my_trades(symbol="BTCUSDT", limit=5)
            result["sample_trades"] = len(trades or [])
        except Exception as e:
            result["notes"].append(f"my_trades error: {e}")

        # Also check Convert trades
        try:
            convert = self._get_convert_trades(days=90)
            result["convert_trades"] = len(convert)
            if convert:
                result["notes"].append(f"Found {len(convert)} Convert trades (included in P&L).")
        except Exception:
            pass

        perms = result["permissions"]
        if not any("SPOT" in p or "TRD" in p for p in perms):
            result["notes"].append("No SPOT trading permissions found — Read access only?")
        if result["sample_trades"] == 0 and result["convert_trades"] == 0:
            result["notes"].append(
                "Zero trades returned. Possible reasons: "
                "(1) coins deposited/transferred from another account, "
                "(2) all trades are outside the time window, "
                "(3) API key missing trade-history read permission."
            )
        return result

    def _pnl_from_journal(self) -> list:
        """Fall back to journal data when Binance API returns no trades."""
        if not self.journal:
            return []
        return self.journal.get_performance()

    def _pnl_from_coach_db(self) -> list:
        """Build FIFO P&L from coach.db order_history (source of truth)."""
        try:
            from modules.coach_db import CoachDB
            db = CoachDB()
            if not db.has_orders():
                return []
            orders = db.get_orders(days=1095)
            # Group by symbol
            from collections import defaultdict, deque
            symbol_orders = defaultdict(list)
            for o in orders:
                symbol_orders[o["symbol"]].append(o)

            results = []
            for symbol, sym_orders in symbol_orders.items():
                asset     = symbol.replace("USDT","").replace("USDC","")
                buy_queue = deque()
                realised  = 0.0
                total_bought = 0.0
                total_sold   = 0.0
                trade_count  = len(sym_orders)

                for o in sorted(sym_orders, key=lambda x: x["timestamp"] or 0):
                    price = float(o["price"] or 0)
                    qty   = float(o["qty"] or 0)
                    if o["side"] == "BUY":
                        buy_queue.append([price, qty])
                        total_bought += price * qty
                    else:
                        remaining = qty
                        total_sold += price * qty
                        while remaining > 0 and buy_queue:
                            op, oq = buy_queue[0]
                            matched = min(remaining, oq)
                            realised += matched * (price - op)
                            remaining -= matched
                            if matched >= oq:
                                buy_queue.popleft()
                            else:
                                buy_queue[0][1] -= matched

                held_qty   = sum(q for _, q in buy_queue)
                cost_basis = sum(p * q for p, q in buy_queue)
                avg_entry  = cost_basis / held_qty if held_qty > 0 else 0.0

                try:
                    current_price = self.market.get_price(symbol)
                except Exception:
                    current_price = None

                current_value  = held_qty * current_price if (current_price and held_qty > 0) else None
                unrealised_pnl = (current_value - cost_basis) if current_value is not None else None
                unrealised_pct = (
                    unrealised_pnl / cost_basis * 100
                    if (unrealised_pnl is not None and cost_basis > 0) else None
                )

                if held_qty > 0 or realised != 0:
                    results.append({
                        "symbol": symbol, "asset": asset,
                        "total_trades": trade_count,
                        "total_bought_usd": total_bought,
                        "total_sold_usd": total_sold,
                        "realised_pnl": realised,
                        "held_qty": held_qty,
                        "avg_entry": avg_entry,
                        "cost_basis": cost_basis,
                        "current_price": current_price,
                        "current_value": current_value,
                        "unrealised_pnl": unrealised_pnl,
                        "unrealised_pct": unrealised_pct,
                        "source": "coach_db",
                    })
            return sorted(results, key=lambda x: abs(x["realised_pnl"] + (x["unrealised_pnl"] or 0)), reverse=True)
        except Exception as e:
            logger.warning(f"coach_db P&L failed: {e}")
            return []

    def calculate_coin_pnl(self, symbol: str, days: int = DEFAULT_DAYS) -> Optional[dict]:
        """FIFO P&L for a single coin (default: last 365 days). Includes Convert trades."""
        symbol = symbol.upper()
        if not symbol.endswith("USDT"):
            symbol += "USDT"

        # Fetch both spot trades AND convert trades
        trades = self._get_trades(symbol, days=days)
        convert_trades = [t for t in self._get_convert_trades(days=days) if t["symbol"] == symbol]
        trades = trades + convert_trades

        if not trades:
            return None

        asset     = symbol.replace("USDT", "").replace("USDC", "")
        buy_queue = deque()          # [price, qty]
        realised_pnl    = 0.0
        total_bought_usd = 0.0
        total_sold_usd   = 0.0

        for t in sorted(trades, key=lambda x: x["time"]):
            price = float(t["price"])
            qty   = float(t["qty"])

            if t["isBuyer"]:
                buy_queue.append([price, qty])
                total_bought_usd += price * qty
            else:
                remaining = qty
                total_sold_usd += price * qty
                while remaining > 0 and buy_queue:
                    oldest_price, oldest_qty = buy_queue[0]
                    matched = min(remaining, oldest_qty)
                    realised_pnl += matched * (price - oldest_price)
                    remaining    -= matched
                    if matched >= oldest_qty:
                        buy_queue.popleft()
                    else:
                        buy_queue[0][1] -= matched
                # If remaining > 0 here, we sold more than we bought in this window.
                # This means purchases are outside the window — log it so user knows.
                if remaining > 0:
                    logger.warning(
                        f"{symbol}: {remaining:.6f} units sold with no matching buy in "
                        f"last {days} days. Cost basis may be understated — consider "
                        f"increasing the window (--days flag)."
                    )

        held_qty   = sum(q for _, q in buy_queue)
        cost_basis = sum(p * q for p, q in buy_queue)
        avg_entry  = cost_basis / held_qty if held_qty > 0 else 0.0

        try:
            current_price = self.market.get_price(symbol)
        except Exception:
            current_price = None

        current_value  = held_qty * current_price if (current_price and held_qty > 0) else None
        unrealised_pnl = (current_value - cost_basis) if current_value is not None else None
        unrealised_pct = (
            unrealised_pnl / cost_basis * 100
            if (unrealised_pnl is not None and cost_basis > 0)
            else None
        )

        return {
            "symbol":           symbol,
            "asset":            asset,
            "total_trades":     len(trades),
            "total_bought_usd": total_bought_usd,
            "total_sold_usd":   total_sold_usd,
            "realised_pnl":     realised_pnl,
            "held_qty":         held_qty,
            "avg_entry":        avg_entry,
            "cost_basis":       cost_basis,
            "current_price":    current_price,
            "current_value":    current_value,
            "unrealised_pnl":   unrealised_pnl,
            "unrealised_pct":   unrealised_pct,
        }

    def calculate_portfolio_pnl(self, days: int = DEFAULT_DAYS) -> list:
        """P&L for all held non-stable coins."""
        try:
            balances = self.portfolio.get_balances()
        except Exception as e:
            logger.error(f"Could not fetch portfolio balances: {e}")
            return []

        coins = [
            b["asset"] for b in balances
            if not b["is_stable"] and b["usd_value"] > 1
        ]
        if not coins:
            return []

        results = []
        for coin in coins[:12]:
            result = self.calculate_coin_pnl(coin + "USDT", days=days)
            if result:
                results.append(result)

        return sorted(
            results,
            key=lambda x: abs(x["realised_pnl"] + (x["unrealised_pnl"] or 0)),
            reverse=True,
        )

    # ── CLI output ────────────────────────────────────────────────────────────

    def print_pnl(self, symbol: str = None, days: int = DEFAULT_DAYS):
        # 1. Try coach.db order_history first (source of truth)
        console.print(f"[dim]Checking local order history database...[/dim]")
        db_results = self._pnl_from_coach_db()
        if db_results:
            if symbol:
                sym = symbol.upper()
                if not sym.endswith("USDT"):
                    sym += "USDT"
                db_results = [r for r in db_results if r["symbol"] == sym]
            if db_results:
                console.print("[dim cyan]📦 Using coach.db order history (source of truth)[/dim cyan]")
                self._print_results(db_results, days=1095, source="coach.db")
                return

        if symbol:
            console.print(f"[dim]Fetching {symbol.upper()} trade history (extended scan)...[/dim]")
            trades, days_used = self._get_trades_extended(symbol.upper() if symbol.upper().endswith("USDT") else symbol.upper() + "USDT")
            if trades:
                result = self.calculate_coin_pnl(symbol, days=days_used)
                results = [result] if result else []
            else:
                results = []
        else:
            console.print(f"[dim]Fetching trade history from Binance (extended scan)...[/dim]")
            # Try extended window first
            for try_days in [365, 730, 1095]:
                results = self.calculate_portfolio_pnl(days=try_days)
                if results:
                    days = try_days
                    break

        if not results:
            # Diagnose why and fall back to journal
            diag = self.diagnose_api()
            console.print("\n[yellow]⚠️  No trade history found via Binance API.[/yellow]")
            console.print(f"[dim]Account permissions: {', '.join(diag['permissions']) or 'unknown'}[/dim]")
            for note in diag["notes"]:
                console.print(f"[dim]  → {note}[/dim]")

            # Try journal fallback
            journal_results = self._pnl_from_journal()
            if journal_results:
                console.print(
                    "\n[cyan]📓 Falling back to Decision Journal data for P&L analysis...[/cyan]"
                )
                self._print_journal_pnl(journal_results)
            else:
                console.print(
                    "\n[dim]No journal entries found either. "
                    "Log decisions with: journal-add BTC buy 70000 100 \"reason\"[/dim]"
                )
            return

        table = Table(title=f"💰 P&L Summary — {days}-day window, FIFO", border_style="green")
        table.add_column("Coin",           width=7)
        table.add_column("Trades",         justify="right", width=7)
        table.add_column("Avg Entry",      justify="right", width=12)
        table.add_column("Current",        justify="right", width=12)
        table.add_column("Cost Basis",     justify="right", width=12)
        table.add_column("Realised P&L",   justify="right", width=14)
        table.add_column("Unrealised P&L", justify="right", width=15)
        table.add_column("Total P&L",      justify="right", width=12)

        total_realised   = 0.0
        total_unrealised = 0.0

        for r in results:
            realised   = r["realised_pnl"]
            unrealised = r["unrealised_pnl"] or 0.0
            total      = realised + unrealised
            total_realised   += realised
            total_unrealised += unrealised

            rc = "green" if realised   >= 0 else "red"
            uc = "green" if unrealised >= 0 else "red"
            tc = "green" if total      >= 0 else "red"

            table.add_row(
                r["asset"],
                str(r["total_trades"]),
                f"${r['avg_entry']:,.4f}"    if r["avg_entry"]     else "—",
                f"${r['current_price']:,.4f}" if r["current_price"] else "?",
                f"${r['cost_basis']:,.2f}",
                f"[{rc}]${realised:+,.2f}[/{rc}]",
                (f"[{uc}]${unrealised:+,.2f}[/{uc}]"
                 if r["unrealised_pnl"] is not None else "?"),
                f"[{tc}]${total:+,.2f}[/{tc}]",
            )

        console.print(table)
        grand = total_realised + total_unrealised
        rc = "green" if total_realised   >= 0 else "red"
        uc = "green" if total_unrealised >= 0 else "red"
        gc = "green" if grand            >= 0 else "red"
        console.print(
            f"\n[bold]Realised:[/bold] [{rc}]${total_realised:+,.2f}[/{rc}]  "
            f"[bold]Unrealised:[/bold] [{uc}]${total_unrealised:+,.2f}[/{uc}]  "
            f"[bold]Grand Total:[/bold] [{gc}]${grand:+,.2f}[/{gc}]"
        )
        console.print(
            "[dim]⚠️  FIFO method. Commission costs excluded (use 'pnl-export' for "
            "Koinly/CoinTracking which calculates fees properly). If you hold coins "
            f"bought before the {days}-day window, cost basis may be understated.[/dim]"
        )

    def _print_results(self, results: list, days: int = 365, source: str = "Binance API"):
        """Shared renderer for pnl results regardless of source."""
        table = Table(title=f"💰 P&L Summary — {source}", border_style="green")
        table.add_column("Coin",           width=7)
        table.add_column("Trades",         justify="right", width=7)
        table.add_column("Avg Entry",      justify="right", width=12)
        table.add_column("Current",        justify="right", width=12)
        table.add_column("Cost Basis",     justify="right", width=12)
        table.add_column("Realised P&L",   justify="right", width=14)
        table.add_column("Unrealised P&L", justify="right", width=15)
        table.add_column("Total P&L",      justify="right", width=12)

        total_realised   = 0.0
        total_unrealised = 0.0

        for r in results:
            realised   = r.get("realised_pnl", 0) or 0
            unrealised = r.get("unrealised_pnl") or 0.0
            total      = realised + unrealised
            total_realised   += realised
            total_unrealised += unrealised
            rc = "green" if realised   >= 0 else "red"
            uc = "green" if unrealised >= 0 else "red"
            tc = "green" if total      >= 0 else "red"
            asset = r.get("asset") or r.get("coin") or "?"
            table.add_row(
                asset,
                str(r.get("total_trades", r.get("buy_entries","?"))),
                f"${r['avg_entry']:,.4f}"     if r.get("avg_entry")     else "—",
                f"${r['current_price']:,.4f}" if r.get("current_price") else "?",
                f"${r.get('cost_basis',0):,.2f}",
                f"[{rc}]${realised:+,.2f}[/{rc}]",
                f"[{uc}]${unrealised:+,.2f}[/{uc}]" if r.get("unrealised_pnl") is not None else "?",
                f"[{tc}]${total:+,.2f}[/{tc}]",
            )

        console.print(table)
        grand = total_realised + total_unrealised
        rc = "green" if total_realised   >= 0 else "red"
        uc = "green" if total_unrealised >= 0 else "red"
        gc = "green" if grand            >= 0 else "red"
        console.print(
            f"\n[bold]Realised:[/bold] [{rc}]${total_realised:+,.2f}[/{rc}]  "
            f"[bold]Unrealised:[/bold] [{uc}]${total_unrealised:+,.2f}[/{uc}]  "
            f"[bold]Grand Total:[/bold] [{gc}]${grand:+,.2f}[/{gc}]"
        )

    def _print_journal_pnl(self, journal_results: list):
        """Render P&L table from journal data (fallback when Binance API has no trades)."""
        table = Table(
            title="💰 P&L Summary — from Decision Journal (no Binance trade history found)",
            border_style="yellow"
        )
        table.add_column("Coin",            width=7)
        table.add_column("Buys",            justify="right", width=6)
        table.add_column("Sells",           justify="right", width=6)
        table.add_column("Avg Entry",       justify="right", width=13)
        table.add_column("Current",         justify="right", width=13)
        table.add_column("Cost Basis",      justify="right", width=12)
        table.add_column("Unrealised P&L",  justify="right", width=15)
        table.add_column("P&L %",           justify="right", width=9)

        total_cost  = 0.0
        total_pnl   = 0.0

        for r in journal_results:
            pnl = r.get("unrealised_pnl")
            pct = r.get("unrealised_pct")
            color = "green" if (pnl or 0) >= 0 else "red"
            table.add_row(
                r["coin"],
                str(r["buy_entries"]),
                str(r["sell_entries"]) if r.get("sell_entries") else "—",
                f"${r['avg_entry']:,.4f}",
                f"${r['current_price']:,.4f}" if r.get("current_price") else "?",
                f"${r['cost_basis']:,.2f}",
                f"[{color}]${pnl:+,.2f}[/{color}]" if pnl is not None else "?",
                f"[{color}]{pct:+.1f}%[/{color}]"  if pct is not None else "?",
            )
            total_cost += r.get("cost_basis", 0)
            if pnl is not None:
                total_pnl += pnl

        console.print(table)
        color = "green" if total_pnl >= 0 else "red"
        console.print(
            f"\n[bold]Total cost basis:[/bold] ${total_cost:,.2f}  "
            f"[bold]Unrealised P&L:[/bold] [{color}]${total_pnl:+,.2f}[/{color}]"
        )
        console.print(
            "[dim]⚠️  Based on manually logged journal entries, not Binance API trade history. "
            "Average-cost method. For full accuracy, ensure your API key has "
            "'Enable Reading' + trade history permissions on Binance.[/dim]"
        )

    def export_csv(self, days: int = DEFAULT_DAYS) -> Path:
        """Export P&L to a timestamped CSV. Returns path to the file."""
        console.print(f"[dim]Fetching trade history ({days} days)...[/dim]")
        results = self.calculate_portfolio_pnl(days=days)
        if not results:
            console.print("[yellow]No data to export.[/yellow]")
            return None

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = DATA_DIR / f"pnl_export_{timestamp}.csv"

        with open(export_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "coin", f"trades_{days}d", "avg_entry_usd", "current_price_usd",
                "held_qty", "cost_basis_usd", "current_value_usd",
                "realised_pnl_usd", "unrealised_pnl_usd", "unrealised_pct",
                "total_bought_usd", "total_sold_usd",
            ])
            for r in results:
                writer.writerow([
                    r["asset"],
                    r["total_trades"],
                    round(r["avg_entry"],       8),
                    r["current_price"]            or "",
                    round(r["held_qty"],        8),
                    round(r["cost_basis"],      2),
                    round(r["current_value"],   2) if r["current_value"]   is not None else "",
                    round(r["realised_pnl"],    2),
                    round(r["unrealised_pnl"],  2) if r["unrealised_pnl"]  is not None else "",
                    round(r["unrealised_pct"],  2) if r["unrealised_pct"]  is not None else "",
                    round(r["total_bought_usd"],2),
                    round(r["total_sold_usd"],  2),
                ])

        console.print(f"[green]✅ Exported to {export_path}[/green]")
        console.print("[dim]Import into Koinly or CoinTracking for a full tax report.[/dim]")
        return export_path

    # ── Telegram HTML output ──────────────────────────────────────────────────

    def format_pnl_html(self, symbol: str = None, days: int = DEFAULT_DAYS) -> str:
        if symbol:
            r = self.calculate_coin_pnl(symbol, days=days)
            results = [r] if r else []
        else:
            results = self.calculate_portfolio_pnl(days=days)

        if not results:
            return f"💰 <b>P&amp;L Summary</b>\nNo trade history found (last {days} days)."

        lines = [f"💰 <b>P&amp;L Summary — {days}-day window, FIFO</b>"]
        total_pnl = 0.0
        for r in results:
            total = r["realised_pnl"] + (r["unrealised_pnl"] or 0.0)
            total_pnl += total
            emoji   = "🟢" if total >= 0 else "🔴"
            pct_str = f" ({r['unrealised_pct']:+.1f}%)" if r["unrealised_pct"] is not None else ""
            lines.append(
                f"{emoji} <b>{r['asset']}</b> avg ${r['avg_entry']:,.4f} "
                f"→ total <b>${total:+,.2f}</b>{pct_str}"
            )

        grand_emoji = "🟢" if total_pnl >= 0 else "🔴"
        lines.append(f"\n{grand_emoji} <b>Grand Total: ${total_pnl:+,.2f}</b>")
        lines.append(
            f"<i>FIFO, {days}-day window, fees excluded. "
            "Use /pnlexport for a CSV compatible with Koinly/CoinTracking.</i>"
        )
        return "\n".join(lines)
