"""
dca.py — Smart DCA Advisor
Suggests optimal DCA amounts based on RSI, Fear & Greed, and price vs MAs
"""

from rich.console import Console
from rich.table import Table
from modules.i18n import t

console = Console()

# Multipliers based on market conditions
DCA_MULTIPLIERS = {
    # (rsi_zone, fg_zone): multiplier
    # Oversold RSI
    ("oversold", "extreme_fear"):    2.0,   # Best possible buying opportunity
    ("oversold", "fear"):            1.8,
    ("oversold", "neutral"):         1.4,
    ("oversold", "greed"):           1.2,   # Oversold despite greed — unusual, still good
    ("oversold", "extreme_greed"):   1.0,   # Oversold + euphoria = caution, but RSI wins
    # Neutral-low RSI
    ("neutral-low", "extreme_fear"): 1.7,
    ("neutral-low", "fear"):         1.5,
    ("neutral-low", "neutral"):      1.0,   # Base DCA amount
    ("neutral-low", "greed"):        0.8,
    ("neutral-low", "extreme_greed"): 0.5,
    # Neutral RSI
    ("neutral", "extreme_fear"):     1.3,
    ("neutral", "fear"):             1.1,
    ("neutral", "neutral"):          1.0,
    ("neutral", "greed"):            0.8,
    ("neutral", "extreme_greed"):    0.3,
    # Neutral-high RSI
    ("neutral-high", "extreme_fear"): 1.0,
    ("neutral-high", "fear"):        0.8,
    ("neutral-high", "neutral"):     0.8,
    ("neutral-high", "greed"):       0.6,
    ("neutral-high", "extreme_greed"): 0.25,
    # Overbought RSI
    ("overbought", "extreme_fear"):  0.6,   # Overbought but market is fearful — contradictory, be cautious
    ("overbought", "fear"):          0.5,
    ("overbought", "neutral"):       0.4,
    ("overbought", "greed"):         0.4,   # Reduce buys when market is expensive
    ("overbought", "extreme_greed"): 0.2,   # Very reduced; don't chase tops
}

# FIX 7: Conservative monthly growth assumptions (median historical performance, risk-adjusted)
ASSET_MONTHLY_GROWTH = {
    "BTC": 0.040,   "ETH": 0.040,   "BNB": 0.038,
    "SOL": 0.045,   "ADA": 0.030,   "XRP": 0.030,
    "DOT": 0.028,   "AVAX": 0.040,  "LINK": 0.038,
    "MATIC": 0.030, "UNI": 0.030,   "DOGE": 0.025,
    "SHIB": 0.020,  "FLOKI": 0.018, "ANKR": 0.022,
    "SCR": 0.020,
}
DEFAULT_MONTHLY_GROWTH = 0.030  # Conservative default for unknown assets


def classify_fg(value: int) -> str:
    if value <= 20:   return "extreme_fear"
    if value <= 40:   return "fear"
    if value <= 60:   return "neutral"
    if value <= 80:   return "greed"
    return "extreme_greed"


class DCAAdvisor:
    """Calculates smart DCA amounts based on current market conditions."""

    def __init__(self, market, monthly_budget: float = 500.0, risk_profile: str = "moderate"):
        self.market = market
        self.monthly_budget = monthly_budget
        self.risk_profile = risk_profile

        # Risk profile adjustments
        self.risk_modifier = {
            "conservative": 0.7,
            "moderate": 1.0,
            "aggressive": 1.3,
        }.get(risk_profile, 1.0)

    def get_recommendation(self, symbol: str) -> dict:
        """
        Get DCA recommendation for a symbol.
        Returns suggested amount, rationale, and projected accumulation.
        """
        ctx = self.market.get_market_context(symbol)
        rsi_zone = ctx["rsi_zone"]
        fg_val = ctx["fear_greed"]["value"]
        fg_zone = classify_fg(fg_val)
        fg_label = ctx["fear_greed"]["classification"]

        # Get matrix multiplier
        key = (rsi_zone, fg_zone)
        matrix_mult = DCA_MULTIPLIERS.get(key, 1.0)

        # FIX 2: SMA200 modifier — price relative to 200-day moving average
        vs_sma200 = ctx["vs_sma200_pct"]
        if vs_sma200 < -30:
            sma_modifier = 1.25   # Deep discount — strong accumulation signal
        elif vs_sma200 < -20:
            sma_modifier = 1.15   # Good discount
        elif vs_sma200 < -10:
            sma_modifier = 1.07   # Slight discount
        elif vs_sma200 <= 10:
            sma_modifier = 1.0    # Fair value
        elif vs_sma200 <= 25:
            sma_modifier = 0.90   # Slight premium
        elif vs_sma200 <= 40:
            sma_modifier = 0.80   # Expensive
        else:
            sma_modifier = 0.70   # Very expensive — reduce significantly

        multiplier = matrix_mult * sma_modifier * self.risk_modifier

        # Weekly DCA base (monthly / 4)
        weekly_base = self.monthly_budget / 4

        # FIX 3: Hard cap — never more than 50% of monthly budget in one week
        MAX_WEEKLY = self.monthly_budget * 0.5
        raw_weekly = round(weekly_base * multiplier, 2)
        capped = raw_weekly > MAX_WEEKLY
        suggested_weekly = min(raw_weekly, MAX_WEEKLY)
        suggested_weekly = round(suggested_weekly, 2)

        # Rationale
        rationale = self._build_rationale(
            ctx, rsi_zone, fg_zone, fg_val, fg_label,
            multiplier, matrix_mult, sma_modifier, capped, MAX_WEEKLY
        )

        # How much of the asset you'd buy at current price
        coin_amount = suggested_weekly / ctx["price"]

        # Discount/premium vs SMA200
        direction = t("dca.reason.deep_discount", pct=f"{abs(vs_sma200):.1f}") if vs_sma200 < 0 else t("dca.reason.premium", pct=f"{vs_sma200:.1f}")
        price_note = direction

        return {
            "symbol": symbol,
            "price": ctx["price"],
            "rsi": ctx["rsi"],
            "rsi_zone": rsi_zone,
            "rsi_zone_label": ctx.get("rsi_zone_label", rsi_zone),
            "fg_value": fg_val,
            "fg_label": fg_label,
            "multiplier": multiplier,
            "sma_modifier": sma_modifier,
            "base_weekly_usd": weekly_base,
            "suggested_weekly_usd": suggested_weekly,
            "coin_amount": round(coin_amount, 8),
            "rationale": rationale,
            "price_vs_sma200": vs_sma200,
            "price_note": price_note,
            "trend": ctx["trend"],
            "capped": capped,
        }

    def _build_rationale(self, ctx, rsi_zone, fg_zone, fg_val, fg_label, multiplier,
                         matrix_mult=None, sma_modifier=None, capped=False, max_weekly=None) -> list[str]:
        reasons = []
        rsi = ctx["rsi"]

        if rsi < 30:
            reasons.append(t("dca.reason.rsi_oversold", rsi=f"{rsi:.1f}"))
        elif rsi > 70:
            reasons.append(t("dca.reason.rsi_overbought", rsi=f"{rsi:.1f}"))
        else:
            reasons.append(t("dca.reason.rsi_neutral", rsi=f"{rsi:.1f}"))

        if fg_val <= 25:
            reasons.append(t("dca.reason.extreme_fear", fg=fg_val))
        elif fg_val >= 75:
            reasons.append(t("dca.reason.extreme_greed", fg=fg_val))
        else:
            reasons.append(t("dca.reason.fg_neutral", fg=fg_val, label=fg_label))

        # FIX 2: Show SMA200 modifier contribution with actual numbers
        vs_sma200 = ctx["vs_sma200_pct"]
        if sma_modifier is not None and sma_modifier != 1.0:
            if vs_sma200 < -20:
                reasons.append(f"📉 SMA200 discount {vs_sma200:+.1f}% → ×{sma_modifier:.2f} boost applied")
            elif vs_sma200 > 10:
                reasons.append(f"📈 SMA200 premium {vs_sma200:+.1f}% → ×{sma_modifier:.2f} reduction applied")
            else:
                reasons.append(f"📊 SMA200: {vs_sma200:+.1f}% → ×{sma_modifier:.2f} modifier")
        elif vs_sma200 < -20:
            reasons.append(t("dca.reason.deep_discount", pct=f"{abs(vs_sma200):.1f}"))
        elif vs_sma200 > 30:
            reasons.append(t("dca.reason.premium", pct=f"{vs_sma200:.1f}"))

        if not ctx["above_sma50"]:
            reasons.append(t("dca.reason.below_sma50"))

        if multiplier > 1.0:
            reasons.append(t("dca.reason.increase", mult=f"{multiplier:.2f}"))
        elif multiplier < 1.0:
            reasons.append(t("dca.reason.reduce", mult=f"{multiplier:.2f}"))
        else:
            reasons.append(t("dca.reason.normal", mult=f"{multiplier:.2f}"))

        # FIX 3: Note if budget cap was applied
        if capped and max_weekly is not None:
            reasons.append(f"⚠️  Weekly cap applied: ${max_weekly:.2f} (50% of monthly budget)")

        return reasons

    def print_recommendations(self, symbols: list[str]):
        """Print DCA recommendations for multiple symbols."""
        profile_label = t(f"dca.profile.{self.risk_profile}") or self.risk_profile.title()
        table = Table(title=f"📐 {t('dca.title', budget=self.monthly_budget, profile=profile_label)}")
        table.add_column(t("dca.col.symbol"), style="cyan")
        table.add_column(t("dca.col.price"), style="white")
        table.add_column(t("dca.col.rsi"), style="yellow")
        table.add_column(t("dca.col.fg"), style="yellow")
        table.add_column(t("dca.col.multiplier"), style="magenta")
        table.add_column(t("dca.col.weekly"), style="green bold")
        table.add_column(t("dca.col.coins"), style="white")
        table.add_column(t("dca.col.vs_sma200"), style="blue")

        recs = []
        for symbol in symbols:
            rec = self.get_recommendation(symbol)
            recs.append(rec)
            multiplier_str = f"×{rec['multiplier']:.2f}"
            if rec['multiplier'] > 1.3:
                multiplier_str = f"[green]{multiplier_str}[/green]"
            elif rec['multiplier'] < 0.7:
                multiplier_str = f"[red]{multiplier_str}[/red]"

            vs_color = "green" if rec["price_vs_sma200"] < 0 else "red"
            rsi_label = rec.get("rsi_zone_label", rec["rsi_zone"])[:6]
            weekly_str = f"${rec['suggested_weekly_usd']:,.2f}"
            if rec.get("capped"):
                weekly_str += " [dim](capped)[/dim]"
            table.add_row(
                rec["symbol"],
                f"${rec['price']:,.4f}",
                f"{rec['rsi']} ({rsi_label})",
                f"{rec['fg_value']} ({rec['fg_label'][:4]})",
                multiplier_str,
                weekly_str,
                f"{rec['coin_amount']:.6f}",
                f"[{vs_color}]{rec['price_vs_sma200']:+.1f}%[/{vs_color}]",
            )

        console.print(table)

        # FIX 5: Print rationale for ALL symbols (compact per coin)
        for rec in recs:
            console.print(f"\n[bold]{t('dca.why', symbol=rec['symbol'])}[/bold]")
            for r in rec["rationale"]:
                console.print(f"  {r}")

    def project_accumulation(self, symbol: str, months: int = 12) -> dict:
        """Project portfolio value assuming consistent DCA. FIX 7: per-asset growth + 3 scenarios."""
        rec = self.get_recommendation(symbol)
        price = rec["price"]
        weekly = rec["suggested_weekly_usd"]
        monthly = weekly * 4.3

        # FIX 7: Get asset-specific growth rate
        base_asset = symbol.replace("USDT", "").replace("BUSD", "")
        base_growth = ASSET_MONTHLY_GROWTH.get(base_asset, DEFAULT_MONTHLY_GROWTH)

        results = {}
        for scenario, growth in [("bear", base_growth * 0.5), ("base", base_growth), ("bull", base_growth * 2.0)]:
            total_coins = 0.0
            total_invested = 0.0
            for month in range(1, months + 1):
                projected_price = price * ((1 + growth) ** month)
                coins_this_month = monthly / projected_price
                total_coins += coins_this_month
                total_invested += monthly
            final_price = price * ((1 + growth) ** months)
            portfolio_value = total_coins * final_price
            results[scenario] = {
                "total_invested": round(total_invested, 2),
                "projected_value": round(portfolio_value, 2),
                "roi_pct": round((portfolio_value - total_invested) / total_invested * 100, 1),
                "monthly_growth_pct": round(growth * 100, 1),
            }

        return {
            "months": months,
            "asset": base_asset,
            "monthly_growth_assumed": round(base_growth * 100, 1),
            "scenarios": results,
            # Backward compat keys (base scenario)
            "total_invested": results["base"]["total_invested"],
            "projected_value": results["base"]["projected_value"],
            "roi_pct": results["base"]["roi_pct"],
            "note": t("dca.projection.note"),
        }
