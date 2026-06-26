"""
yield_optimizer.py — Stablecoin yield optimizer

Fixes applied:
- New Simple Earn API tried first, old Savings API as fallback (was backwards)
- Both API failures now logged as warnings instead of swallowed silently
  (silent failure → all stablecoins show "idle" even if actually enrolled)
- `if monthly_yield is not None:` replaces falsy `if monthly_yield:`
  (0% APR asset was incorrectly shown as "idle" instead of "enrolled, 0%")
- `total_idle` renamed to `total_stablecoins` — it was including earning assets too,
  the name was misleading
- `self.market` removed — it was stored but never used
- Python 3.9-compatible type hints
"""
import logging
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()

STABLECOINS = {"USDT", "USDC", "BUSD", "TUSD", "FDUSD", "DAI", "USD1", "USDP", "USDE"}


class YieldOptimizer:
    def __init__(self, client, portfolio):
        self.client    = client
        self.portfolio = portfolio

    def _get_earn_rate(self, asset: str) -> Optional[float]:
        """
        Fetch best available APR (%) for an asset from Binance Simple Earn.
        Tries the current Simple Earn v2 API first, falls back to legacy Savings API.
        Returns None only if both fail (logs a warning so the caller knows).
        """
        # 1. Current Simple Earn Flexible endpoint (preferred)
        try:
            resp = self.client.simple_earn_flexible_product_list(asset=asset, current=1, size=5)
            rows = resp.get("data", {}).get("rows", [])
            if rows:
                rates = [float(r.get("latestAnnualPercentageRate", 0)) for r in rows]
                return max(rates) * 100
        except Exception as e:
            logger.debug(f"Simple Earn v2 API failed for {asset}: {e}")

        # 2. Legacy Savings API fallback (deprecated but may still work)
        try:
            resp = self.client.get_flexible_product_list(asset=asset, status="SUBSCRIBABLE")
            if resp:
                rates = [float(r.get("latestAnnualPercentageRate", 0)) for r in resp]
                if rates:
                    return max(rates) * 100
        except Exception as e:
            logger.debug(f"Legacy Savings API failed for {asset}: {e}")

        logger.warning(
            f"Could not fetch Simple Earn rate for {asset} — both APIs failed. "
            "Balance will show as 'rate unavailable', not necessarily idle."
        )
        return None

    def analyze(self) -> dict:
        try:
            balances = self.portfolio.get_balances()
        except Exception as e:
            return {"error": str(e)}

        stable_holdings = [
            b for b in balances
            if b["asset"].upper() in STABLECOINS and b["usd_value"] > 0.5
        ]

        if not stable_holdings:
            return {
                "stable_holdings":  [],
                "total_stablecoins": 0.0,
                "total_monthly":    0.0,
                "total_annual":     0.0,
            }

        results = []
        total_stablecoins = sum(b["usd_value"] for b in stable_holdings)
        total_monthly = 0.0
        total_annual  = 0.0

        for b in stable_holdings:
            asset = b["asset"].upper()
            usd   = b["usd_value"]
            apr   = self._get_earn_rate(asset)

            monthly = usd * apr / 100 / 12 if apr is not None else None
            annual  = usd * apr / 100       if apr is not None else None

            if monthly is not None:
                total_monthly += monthly
                total_annual  += annual

            results.append({
                "asset":         asset,
                "usd_value":     usd,
                "apr":           apr,
                "monthly_yield": monthly,
                "annual_yield":  annual,
            })

        return {
            "stable_holdings":   sorted(results, key=lambda x: -x["usd_value"]),
            "total_stablecoins": total_stablecoins,
            "total_monthly":     total_monthly,
            "total_annual":      total_annual,
        }

    # ── CLI output ────────────────────────────────────────────────────────────

    def print_yield(self):
        result = self.analyze()
        if "error" in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        if not result["stable_holdings"]:
            console.print("[yellow]No stablecoin holdings found.[/yellow]")
            return

        table = Table(title="💵 Stablecoin Yield Optimizer", border_style="green")
        table.add_column("Asset",         width=8)
        table.add_column("Balance",       justify="right", width=12)
        table.add_column("APR",           justify="right", width=8)
        table.add_column("Monthly Yield", justify="right", width=15)
        table.add_column("Annual Yield",  justify="right", width=13)
        table.add_column("Status")

        idle_usd = 0.0
        for r in result["stable_holdings"]:
            apr = r["apr"]
            if apr is None:
                # API failed — don't assume idle, say unknown
                status  = "[dim]❓ Rate unavailable[/dim]"
                monthly = "[dim]?[/dim]"
                annual  = "[dim]?[/dim]"
                apr_str = "?"
            elif apr > 0:
                status  = "[green]✅ Earning[/green]"
                monthly = f"[green]+${r['monthly_yield']:,.2f}[/green]"
                annual  = f"[green]+${r['annual_yield']:,.2f}[/green]"
                apr_str = f"{apr:.2f}%"
            else:
                # APR returned but 0% — enrolled but earning nothing
                status  = "[yellow]⚠️ 0% APR[/yellow]"
                monthly = "[yellow]$0.00[/yellow]"
                annual  = "[yellow]$0.00[/yellow]"
                apr_str = "0%"
                idle_usd += r["usd_value"]

            table.add_row(
                r["asset"],
                f"${r['usd_value']:,.2f}",
                apr_str,
                monthly,
                annual,
                status,
            )

        console.print(table)

        if result["total_monthly"] > 0:
            console.print(Panel(
                f"[bold green]+${result['total_monthly']:,.2f} / month[/bold green]  "
                f"([dim]+${result['total_annual']:,.2f} / year[/dim])\n"
                f"[dim]Total stablecoins tracked: ${result['total_stablecoins']:,.2f}[/dim]",
                title="💰 Earning Potential",
                border_style="green"
            ))
        if idle_usd > 1:
            console.print(Panel(
                f"[yellow]${idle_usd:,.2f} enrolled at 0% APR — consider switching products.[/yellow]",
                title="⚠️ Zero-yield Holdings",
                border_style="yellow"
            ))

    # ── Telegram HTML output ──────────────────────────────────────────────────

    def format_yield_html(self) -> str:
        result = self.analyze()
        if "error" in result:
            return f"💵 <b>Yield Optimizer</b>\nError: {result['error']}"
        if not result["stable_holdings"]:
            return "💵 <b>Yield Optimizer</b>\nNo stablecoin holdings found."

        lines = ["💵 <b>Stablecoin Yield Optimizer</b>"]
        idle_usd = 0.0
        for r in result["stable_holdings"]:
            if r["monthly_yield"] is not None and r["monthly_yield"] > 0:
                lines.append(
                    f"✅ <b>{r['asset']}</b> ${r['usd_value']:,.2f} "
                    f"@ {r['apr']:.2f}% APR → <b>+${r['monthly_yield']:,.2f}/mo</b>"
                )
            elif r["apr"] == 0:
                idle_usd += r["usd_value"]
                lines.append(f"⚠️ <b>{r['asset']}</b> ${r['usd_value']:,.2f} — enrolled at 0% APR")
            elif r["apr"] is None:
                lines.append(f"❓ <b>{r['asset']}</b> ${r['usd_value']:,.2f} — rate unavailable")
            else:
                idle_usd += r["usd_value"]
                lines.append(f"💤 <b>{r['asset']}</b> ${r['usd_value']:,.2f} — idle, not earning")

        if result["total_monthly"] > 0:
            lines.append(
                f"\n💰 <b>Total: +${result['total_monthly']:,.2f}/month "
                f"(+${result['total_annual']:,.2f}/year)</b>"
            )
        if idle_usd > 1:
            lines.append(
                f"\n⚠️ ${idle_usd:,.2f} at 0% — consider enabling Binance Simple Earn."
            )
        return "\n".join(lines)
