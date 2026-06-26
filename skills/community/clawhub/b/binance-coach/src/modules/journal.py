"""
journal.py — Persistent decision journal with P&L tracking
Log DCA decisions, track performance over time, sync to OpenClaw memory.
Uses coach.db for all data storage (consolidated database).

Fixes applied:
- Context manager for all DB connections (no leaks on exception)
- Action validated to BUY/SELL only
- Negative price/amount rejected
- get_performance() accounts for SELL entries (reduces held qty)
- `if pnl is not None:` replaces falsy `if pnl:` — correctly handles $0.00
- notes sanitized (newlines stripped) before memory write
- HTML escape on all user-controlled strings in format_*_html()
- journal-delete command
- Python 3.9-compatible type hints
"""
import html as html_lib
import os
import logging
from datetime import datetime
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from modules.coach_db import CoachDB

logger = logging.getLogger(__name__)
console = Console()

VALID_ACTIONS = {"BUY", "SELL"}


class DecisionJournal:
    """Log buy/sell decisions, track performance vs current prices."""

    def __init__(self, market=None):
        self.market = market
        self.db = CoachDB()

    # ── Write ─────────────────────────────────────────────────────────────────

    def add_entry(self, coin: str, action: str, price_usd: float,
                  amount_usd: Optional[float] = None, notes: str = ""):
        coin = coin.upper().replace("USDT", "").replace("USDC", "")
        action = action.upper()

        if action not in VALID_ACTIONS:
            raise ValueError(f"Invalid action '{action}'. Use BUY or SELL.")
        if price_usd <= 0:
            raise ValueError(f"Price must be positive, got {price_usd}")
        if amount_usd is not None and amount_usd < 0:
            raise ValueError(f"Amount must be non-negative, got {amount_usd}")

        qty = (amount_usd / price_usd) if (amount_usd is not None and price_usd > 0) else None
        # Sanitize notes — strip newlines so the memory file doesn't break
        notes = notes.strip().replace("\n", " ").replace("\r", "")

        self.db.add_journal_entry(coin, action, price_usd, amount_usd, qty, notes)

        amt_display = f" (${amount_usd:,.2f})" if amount_usd is not None else ""
        console.print(f"[green]✅ Logged: {action} {coin} @ ${price_usd:,.4f}{amt_display}[/green]")
        self._sync_to_memory(coin, action, price_usd, amount_usd, notes)

    def delete_entry(self, entry_id: int) -> bool:
        # Get entry details before deletion for display
        entries = self.db.get_journal_entries(limit=500)
        entry = next((e for e in entries if e["id"] == entry_id), None)
        
        if not entry:
            console.print(f"[red]No entry with id={entry_id}[/red]")
            return False
            
        if self.db.delete_journal_entry(entry_id):
            created = entry.get("created_at", "")[:10]
            console.print(
                f"[yellow]🗑️  Deleted entry #{entry_id}: {entry['action']} {entry['coin']} "
                f"@ ${entry['price_usd']:,.4f} ({created})[/yellow]"
            )
            return True
        return False

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_entries(self, coin: Optional[str] = None, limit: int = 20) -> list:
        return self.db.get_journal_entries(coin=coin, limit=limit)

    def get_performance(self, coin: Optional[str] = None) -> list:
        """
        Unrealised P&L using average-cost method.
        SELL entries reduce held qty — prevents inflated P&L for partial exits.
        """
        entries = self.get_entries(coin=coin, limit=500)
        if not entries:
            return []

        coin_data: dict = {}
        for entry in entries:
            c = entry["coin"]
            action = entry["action"]
            price = entry["price_usd"]
            amount = entry["amount_usd"]
            qty = entry["qty"]
            
            if c not in coin_data:
                coin_data[c] = {
                    "total_bought_qty":  0.0,
                    "total_sold_qty":    0.0,
                    "total_invested":    0.0,
                    "buy_count":         0,
                    "sell_count":        0,
                }
            d = coin_data[c]
            if action == "BUY":
                d["total_bought_qty"] += qty or 0.0
                d["total_invested"]   += amount or 0.0
                d["buy_count"]        += 1
            elif action == "SELL":
                d["total_sold_qty"] += qty or 0.0
                d["sell_count"]     += 1

        results = []
        for c, d in coin_data.items():
            if d["buy_count"] == 0:
                continue  # sell-only entries can't compute avg_entry

            total_bought_qty = d["total_bought_qty"]
            total_invested   = d["total_invested"]
            avg_entry = total_invested / total_bought_qty if total_bought_qty > 0 else 0.0

            # Floor at 0 — can't hold negative qty
            held_qty   = max(0.0, total_bought_qty - d["total_sold_qty"])
            cost_basis = held_qty * avg_entry

            current_price = None
            if self.market:
                try:
                    current_price = self.market.get_price(c + "USDT")
                except Exception:
                    pass

            current_value  = held_qty * current_price if (current_price and held_qty > 0) else None
            unrealised_pnl = (current_value - cost_basis) if current_value is not None else None
            unrealised_pct = (
                unrealised_pnl / cost_basis * 100
                if (unrealised_pnl is not None and cost_basis > 0)
                else None
            )

            results.append({
                "coin":          c,
                "buy_entries":   d["buy_count"],
                "sell_entries":  d["sell_count"],
                "avg_entry":     avg_entry,
                "current_price": current_price,
                "total_invested":total_invested,
                "held_qty":      held_qty,
                "cost_basis":    cost_basis,
                "current_value": current_value,
                "unrealised_pnl":unrealised_pnl,
                "unrealised_pct":unrealised_pct,
            })

        return sorted(results, key=lambda x: abs(x["unrealised_pnl"] or 0), reverse=True)

    # ── CLI output ────────────────────────────────────────────────────────────

    def print_journal(self, coin: Optional[str] = None):
        entries = self.get_entries(coin=coin)
        if not entries:
            console.print("[yellow]No journal entries yet.[/yellow]")
            console.print('[dim]Log a decision: journal-add BTC buy 70000 100 "oversold"[/dim]')
            return

        table = Table(title="📓 Decision Journal", border_style="blue")
        table.add_column("#",        style="dim",     width=5)
        table.add_column("Date",     style="dim",     width=12)
        table.add_column("Coin",                      width=8)
        table.add_column("Action",                    width=8)
        table.add_column("Price",    justify="right", width=12)
        table.add_column("Amount $", justify="right", width=10)
        table.add_column("Notes")

        for entry in entries:
            action = entry["action"]
            created_at = entry.get("created_at", "") or ""
            amount = entry["amount_usd"]
            color = "green" if action == "BUY" else "red"
            table.add_row(
                str(entry["id"]),
                created_at[:10] if created_at else "",
                entry["coin"],
                f"[{color}]{action}[/{color}]",
                f"${entry['price_usd']:,.4f}",
                f"${amount:,.2f}" if amount is not None else "—",
                entry["notes"] or "—",
            )
        console.print(table)
        console.print("[dim]To delete an entry: journal-delete <id>[/dim]")

    def print_performance(self):
        results = self.get_performance()
        if not results:
            console.print("[yellow]No journal entries to analyse.[/yellow]")
            return

        table = Table(title="📈 Journal Performance vs Current Price", border_style="green")
        table.add_column("Coin",            width=8)
        table.add_column("Buys",  justify="right", width=6)
        table.add_column("Sells", justify="right", width=6)
        table.add_column("Avg Entry",       justify="right", width=12)
        table.add_column("Current",         justify="right", width=12)
        table.add_column("Held Qty",        justify="right", width=12)
        table.add_column("Cost Basis",      justify="right", width=12)
        table.add_column("Unrealised P&L",  justify="right", width=16)
        table.add_column("P&L %",           justify="right", width=9)

        total_cost_basis = 0.0
        total_pnl        = 0.0

        for r in results:
            pnl = r["unrealised_pnl"]
            pct = r["unrealised_pct"]
            color = "green" if (pnl or 0) >= 0 else "red"
            table.add_row(
                r["coin"],
                str(r["buy_entries"]),
                str(r["sell_entries"]) if r["sell_entries"] else "—",
                f"${r['avg_entry']:,.4f}",
                f"${r['current_price']:,.4f}" if r["current_price"] else "?",
                f"{r['held_qty']:.4f}",
                f"${r['cost_basis']:,.2f}",
                f"[{color}]${pnl:+,.2f}[/{color}]"  if pnl is not None else "?",
                f"[{color}]{pct:+.1f}%[/{color}]"   if pct is not None else "?",
            )
            total_cost_basis += r["cost_basis"]
            if pnl is not None:
                total_pnl += pnl

        console.print(table)
        color = "green" if total_pnl >= 0 else "red"
        console.print(
            f"\n[bold]Total cost basis:[/bold] ${total_cost_basis:,.2f}  "
            f"[bold]Unrealised P&L:[/bold] [{color}]${total_pnl:+,.2f}[/{color}]"
        )
        console.print("[dim]Average-cost method. SELL entries reduce held qty.[/dim]")

    # ── Telegram HTML output ──────────────────────────────────────────────────

    def format_journal_html(self, coin: Optional[str] = None) -> str:
        entries = self.get_entries(coin=coin, limit=8)
        if not entries:
            return (
                "📓 <b>Decision Journal</b>\n"
                "No entries yet.\n"
                'Add via: <code>/journaladd BTC buy 70000 100 "reason"</code>'
            )
        lines = ["📓 <b>Decision Journal</b>"]
        for entry in entries:
            action = entry["action"]
            amount = entry["amount_usd"]
            notes = entry["notes"]
            created_at = entry.get("created_at", "") or ""
            emoji     = "🟢" if action == "BUY" else "🔴"
            amt       = f" ${amount:,.0f}" if amount is not None else ""
            safe_coin  = html_lib.escape(entry["coin"])
            safe_notes = html_lib.escape(notes) if notes else ""
            lines.append(
                f"#{entry['id']} {emoji} <b>{safe_coin}</b> {action} @ ${entry['price_usd']:,.4f}{amt} — {created_at[:10]}"
            )
            if safe_notes:
                lines.append(f"   <i>{safe_notes}</i>")
        lines.append("\n<i>Delete: /journaldelete &lt;id&gt;</i>")
        return "\n".join(lines)

    def format_performance_html(self) -> str:
        results = self.get_performance()
        if not results:
            return "📈 <b>Journal Performance</b>\nNo buy entries to analyse."
        lines = ["📈 <b>Journal Performance vs Current Price</b>"]
        for r in results:
            safe_coin = html_lib.escape(r["coin"])
            if r["unrealised_pnl"] is not None:
                emoji   = "🟢" if r["unrealised_pnl"] >= 0 else "🔴"
                pct_str = f"{r['unrealised_pct']:+.1f}%" if r["unrealised_pct"] is not None else "?"
                lines.append(
                    f"{emoji} <b>{safe_coin}</b> avg ${r['avg_entry']:,.4f} → "
                    f"${r['current_price']:,.4f} (<b>{pct_str}</b>  ${r['unrealised_pnl']:+,.2f})"
                )
            else:
                lines.append(f"• <b>{safe_coin}</b> avg ${r['avg_entry']:,.4f} (price unavailable)")
        lines.append("\n<i>Average-cost method. SELL entries reduce held qty.</i>")
        return "\n".join(lines)

    # ── Memory sync ───────────────────────────────────────────────────────────

    def _sync_to_memory(self, coin: str, action: str, price_usd: float,
                        amount_usd: Optional[float] = None, notes: str = ""):
        """Append decision to OpenClaw daily memory file."""
        workspace = None
        for candidate in [
            os.path.expanduser("~/.openclaw/workspace"),
            os.path.expanduser("~/clawd/workspace"),
        ]:
            if os.path.isdir(candidate):
                workspace = candidate
                break
        if not workspace:
            return
        try:
            memory_dir = os.path.join(workspace, "memory")
            os.makedirs(memory_dir, exist_ok=True)
            today      = datetime.now().strftime("%Y-%m-%d")
            memory_file = os.path.join(memory_dir, f"{today}.md")
            amt_str    = f" (${amount_usd:,.2f})" if amount_usd is not None else ""
            note_str   = f" — {notes}" if notes else ""  # notes already sanitized in add_entry()
            entry      = f"- BinanceCoach: {action} {coin} @ ${price_usd:,.4f}{amt_str}{note_str}\n"
            with open(memory_file, "a") as f:
                f.write(entry)
        except Exception as e:
            logger.debug(f"Memory sync failed: {e}")
