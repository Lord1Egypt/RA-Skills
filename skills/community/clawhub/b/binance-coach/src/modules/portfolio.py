"""
portfolio.py — Portfolio analysis & health scoring
Fetches balances, calculates health score, detects concentration risk
"""

from binance.spot import Spot
from rich.console import Console
from rich.table import Table
from modules.i18n import t

console = Console()

STABLECOINS = {"USDT", "USDC", "BUSD", "DAI", "FDUSD", "TUSD"}

BNB_CHAIN_TOKENS = {
    "BNB", "CAKE", "XVS", "ALPACA", "BIFI", "BELT", "EPS", "DODO",
    "AUTO", "BUNNY", "BISWAP", "NULS"
}


class Portfolio:
    """Reads and analyzes a Binance spot portfolio."""

    def __init__(self, client: Spot, market):
        self.client = client
        self.market = market

    def get_balances(self) -> list[dict]:
        """Get non-zero spot balances with current USD values."""
        account = self.client.account()
        balances = []
        for b in account["balances"]:
            free = float(b["free"])
            locked = float(b["locked"])
            total = free + locked
            if total < 0.0001:
                continue
            asset = b["asset"]
            # Get USD value
            usd_value = self._get_usd_value(asset, total)
            if usd_value < 1:  # Skip dust
                continue
            base_asset = asset[2:] if asset.startswith("LD") else asset
            is_earn = asset.startswith("LD")
            balances.append({
                "asset": base_asset,
                "display": f"{base_asset} (Earn)" if is_earn else base_asset,
                "amount": total,
                "usd_value": usd_value,
                "is_stable": base_asset in STABLECOINS,
                "is_bnb_chain": base_asset in BNB_CHAIN_TOKENS,
            })
        # Sort by USD value desc
        balances.sort(key=lambda x: x["usd_value"], reverse=True)
        return balances

    def _get_usd_value(self, asset: str, amount: float) -> float:
        if asset in STABLECOINS:
            return amount
        # Strip LD prefix (Binance Simple Earn / Flexible Savings positions)
        base = asset[2:] if asset.startswith("LD") else asset
        for symbol in [f"{base}USDT", f"{base}BUSD", f"{base}BTC"]:
            try:
                price = float(self.client.ticker_price(symbol=symbol)["price"])
                # If priced in BTC, convert to USD
                if symbol.endswith("BTC"):
                    btc_price = float(self.client.ticker_price(symbol="BTCUSDT")["price"])
                    return amount * price * btc_price
                return amount * price
            except Exception:
                continue
        return 0.0

    def calculate_health_score(self, balances: list[dict]) -> dict:
        """
        Portfolio Health Score (0–100):
        - Diversification (30 pts)
        - Stablecoin reserve (20 pts)
        - Concentration risk (25 pts)
        - BNB chain exposure (15 pts)
        - Dust cleanup (10 pts)
        """
        total_usd = sum(b["usd_value"] for b in balances)
        if total_usd == 0:
            return {"score": 0, "breakdown": {}, "grade": "N/A", "suggestions": []}

        score = 0
        breakdown = {}
        suggestions = []

        # 1. Diversification (30 pts) — number of meaningful holdings
        non_stable = [b for b in balances if not b["is_stable"] and b["usd_value"] > 50]
        n_assets = len(non_stable)
        if n_assets >= 8:
            div_score = 30
        elif n_assets >= 5:
            div_score = 22
        elif n_assets >= 3:
            div_score = 15
        elif n_assets >= 1:
            div_score = 8
        else:
            div_score = 0
        score += div_score
        breakdown["diversification"] = div_score
        if n_assets < 5:
            suggestions.append(t("portfolio.sug.diversify", n=n_assets))

        # 2. Stablecoin reserve (20 pts)
        stable_usd = sum(b["usd_value"] for b in balances if b["is_stable"])
        stable_pct = stable_usd / total_usd * 100
        if 10 <= stable_pct <= 30:
            stable_score = 20
        elif stable_pct < 5:
            stable_score = 5
            suggestions.append(t("portfolio.sug.no_stable", pct=f"{stable_pct:.1f}"))
        elif stable_pct > 60:
            stable_score = 10
            suggestions.append(t("portfolio.sug.too_stable", pct=f"{stable_pct:.1f}"))
        else:
            stable_score = 15
        score += stable_score
        breakdown["stablecoin_reserve"] = stable_score

        # 3. Concentration risk (25 pts)
        risky = [b for b in balances if not b["is_stable"]]
        if risky:
            top_pct = risky[0]["usd_value"] / total_usd * 100
            if top_pct < 30:
                conc_score = 25
            elif top_pct < 50:
                conc_score = 15
                suggestions.append(t("portfolio.sug.conc_warn", pct=f"{top_pct:.1f}"))
            elif top_pct < 70:
                conc_score = 8
                suggestions.append(t("portfolio.sug.conc_high", asset=risky[0]["asset"], pct=f"{top_pct:.1f}"))
            else:
                conc_score = 2
                suggestions.append(t("portfolio.sug.conc_extreme", asset=risky[0]["asset"], pct=f"{top_pct:.1f}"))
        else:
            conc_score = 25
        score += conc_score
        breakdown["concentration"] = conc_score

        # 4. BNB chain exposure (15 pts)
        bnb_usd = sum(b["usd_value"] for b in balances if b["is_bnb_chain"])
        bnb_pct = bnb_usd / total_usd * 100
        if bnb_pct < 40:
            bnb_score = 15
        elif bnb_pct < 60:
            bnb_score = 10
            suggestions.append(t("portfolio.sug.bnb_chain", pct=f"{bnb_pct:.1f}"))
        else:
            bnb_score = 4
            suggestions.append(t("portfolio.sug.bnb_high", pct=f"{bnb_pct:.1f}"))
        score += bnb_score
        breakdown["chain_diversification"] = bnb_score

        # 5. Dust cleanup (10 pts)
        dust_count = sum(1 for b in balances if b["usd_value"] < 5)
        if dust_count == 0:
            dust_score = 10
        elif dust_count < 5:
            dust_score = 7
        else:
            dust_score = 3
            suggestions.append(t("portfolio.sug.dust", n=dust_count))
        score += dust_score
        breakdown["dust"] = dust_score

        # Grade
        grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F"

        return {
            "score": score,
            "grade": grade,
            "total_usd": total_usd,
            "breakdown": breakdown,
            "suggestions": suggestions,
            "stable_pct": round(stable_pct, 1),
            "n_assets": n_assets,
        }

    def print_portfolio_table(self, balances: list[dict], health: dict):
        """Pretty-print portfolio in terminal."""
        table = Table(title=f"💼 {t('portfolio.title', score=health['score'], grade=health['grade'])}")
        table.add_column(t("portfolio.col.asset"), style="cyan")
        table.add_column(t("portfolio.col.amount"), style="white")
        table.add_column(t("portfolio.col.usd"), style="green")
        table.add_column(t("portfolio.col.pct"), style="yellow")

        total = health["total_usd"]
        for b in balances:
            pct = b["usd_value"] / total * 100
            table.add_row(
                b.get("display", b["asset"]),
                f"{b['amount']:.6f}",
                f"${b['usd_value']:,.2f}",
                f"{pct:.1f}%"
            )

        table.add_section()
        table.add_row("TOTAL", "", f"${total:,.2f}", "100%")
        console.print(table)

        if health["suggestions"]:
            console.print(f"\n[yellow]{t('portfolio.suggestions')}:[/yellow]")
            for s in health["suggestions"]:
                console.print(f"  • {s}")
