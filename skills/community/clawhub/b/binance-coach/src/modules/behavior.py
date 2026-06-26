"""
behavior.py — Behavioral bias detector & coaching engine
Analyzes trade history for emotional trading patterns
Uses coach.db for all data storage (consolidated database).
"""

import logging
from datetime import datetime, timedelta
from binance.spot import Spot
from rich.console import Console
from rich.panel import Panel
from modules.i18n import t
from modules.coach_db import CoachDB

logger  = logging.getLogger(__name__)
console = Console()


class BehaviorCoach:
    """Detects emotional trading patterns and coaches users."""

    def __init__(self, client: Spot, market, journal=None):
        self.client  = client
        self.market  = market
        self.journal = journal  # Optional DecisionJournal for fallback
        self.db      = CoachDB()

    def sync_trades(self, symbols: list, days: int = 30):
        """Pull recent trade history from Binance into coach.db, with journal fallback."""
        cutoff = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)
        api_trade_count = 0

        for symbol in symbols:
            try:
                trades = self.client.my_trades(symbol=symbol, limit=500) or []
                for trade in trades:
                    if trade["time"] < cutoff:
                        continue
                    self.db.save_trade(
                        symbol=trade["symbol"],
                        side="BUY" if trade["isBuyer"] else "SELL",
                        price=float(trade["price"]),
                        qty=float(trade["qty"]),
                        time_ms=trade["time"],
                        order_id=str(trade["id"])
                    )
                api_trade_count += len(trades)
            except Exception as e:
                logger.debug("sync_trades: skipping %s — %s", symbol, e)

        # If Binance API returned nothing, seed from journal entries
        if api_trade_count == 0 and self.journal:
            entries = self.journal.get_entries(limit=200)
            for entry in entries:
                coin = entry.get("coin", "")
                action = entry.get("action", "")
                price = entry.get("price_usd", 0)
                amount = entry.get("amount_usd")
                qty = entry.get("qty")
                created_at = entry.get("created_at", "")
                sym = coin.upper() + "USDT"
                try:
                    ts = int(datetime.strptime(created_at[:19], "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                except Exception as e:
                    logger.debug("sync_trades: bad created_at '%s' — %s", created_at, e)
                    ts = int(datetime.utcnow().timestamp() * 1000)
                if ts < cutoff:
                    continue
                effective_qty = qty if qty else (amount / price if amount and price else 0)
                self.db.save_trade(
                    symbol=sym,
                    side=action,
                    price=price,
                    qty=effective_qty or 0.0,
                    time_ms=ts,
                    order_id=f"journal_{entry.get('id', ts)}"
                )

    def calculate_fomo_score(self) -> dict:
        """
        FOMO Score: Did you buy during Fear & Greed extremes (>75 greed)?
        Higher score = more FOMO buying detected.
        """
        cutoff = int((datetime.utcnow() - timedelta(days=30)).timestamp() * 1000)
        trades = self.db.get_trades(cutoff_ms=cutoff)
        buys = [(t["time"], t["price"]) for t in trades if t["side"] == "BUY"]

        if not buys:
            return {"score": 0, "label": "N/A", "detail": "No trades in last 30 days."}

        # Current F&G
        fg = self.market.get_fear_greed()
        fg_val = fg["value"]

        # Simple heuristic: if you traded a lot when F&G was high, that's FOMO
        # We can't get historical F&G per trade easily without paid API
        # So we approximate by clustering: rapid buys near local highs
        fomo_score = 0
        if fg_val > 75:
            fomo_score += 40  # Currently buying in extreme greed
        elif fg_val > 60:
            fomo_score += 20

        # Overbuying: many buys in short windows (buying the hype)
        buy_times = sorted([row[0] for row in buys])
        rapid_buys = 0
        for i in range(1, len(buy_times)):
            if buy_times[i] - buy_times[i-1] < 3600_000:  # within 1 hour
                rapid_buys += 1
        fomo_score += min(60, rapid_buys * 10)
        fomo_score = min(100, fomo_score)  # Cap at 100

        label = t("behavior.fomo.label.low") if fomo_score < 30 else t("behavior.fomo.label.med") if fomo_score < 65 else t("behavior.fomo.label.high")
        return {
            "score": fomo_score,
            "label": label,
            "current_fg": fg_val,
            "current_fg_label": fg["classification"],
            "rapid_buy_clusters": rapid_buys,
        }

    def detect_panic_sells(self) -> list:
        """
        Detect sells that happened near the 30-day low before the sell
        AND where price has since recovered >15%.
        """
        cutoff = int((datetime.utcnow() - timedelta(days=30)).timestamp() * 1000)
        trades = self.db.get_trades(cutoff_ms=cutoff)
        sells = [(t["symbol"], t["price"], t["time"]) for t in trades if t["side"] == "SELL"]

        panic_sells = []
        for symbol, sell_price, sell_time_ms in sells:
            try:
                current = self.market.get_price(symbol)
                recovery = ((current - sell_price) / sell_price) * 100
                if recovery <= 15:
                    continue

                sell_dt = datetime.utcfromtimestamp(sell_time_ms / 1000)
                start_ms = int((sell_dt - timedelta(days=30)).timestamp() * 1000)
                raw = self.market.client.klines(
                    symbol=symbol, interval="1d",
                    startTime=start_ms, endTime=sell_time_ms, limit=30
                )
                if not raw:
                    continue
                thirty_day_low = min(float(row[3]) for row in raw)
                pct_above_low  = ((sell_price - thirty_day_low) / thirty_day_low) * 100

                if pct_above_low <= 10.0:
                    panic_sells.append({
                        "symbol": symbol,
                        "sell_price": sell_price,
                        "current_price": current,
                        "recovery_pct": round(recovery, 1),
                        "sold_at": sell_dt.strftime("%Y-%m-%d"),
                        "thirty_day_low": round(thirty_day_low, 4),
                        "pct_above_low": round(pct_above_low, 1),
                    })
            except Exception as e:
                logger.debug("detect_panic_sells: skipping %s — %s", symbol, e)
        return panic_sells

    def calculate_overtrading_index(self) -> dict:
        """Count trades per week — high frequency often leads to worse outcomes."""
        cutoff = int((datetime.utcnow() - timedelta(days=30)).timestamp() * 1000)
        trades = self.db.get_trades(cutoff_ms=cutoff)
        count = len(trades)

        per_week = count / 4.3
        label = t("behavior.overtrade.label.healthy") if per_week < 5 else t("behavior.overtrade.label.mod") if per_week < 15 else t("behavior.overtrade.label.high") if per_week < 30 else t("behavior.overtrade.label.over")
        tip = ""
        if per_week > 15:
            tip = t("behavior.overtrade.tip")

        return {
            "total_30d": count,
            "per_week_avg": round(per_week, 1),
            "label": label,
            "tip": tip,
        }

    def get_streaks(self) -> dict:
        """Get gamified streak data — days without panic selling, etc."""
        return self.db.get_streaks()

    def update_streaks(self, has_panic_sell: bool, has_recent_buy: bool):
        """Update streak counters. Call once per behavior report."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        streaks = self.db.get_streaks()

        # --- No panic sell streak ---
        nps = streaks.get("no_panic_sell", {"count": 0, "last_updated": None})
        if has_panic_sell:
            self.db.update_streak("no_panic_sell", 0, today)
        else:
            if nps["last_updated"] and nps["last_updated"] != today:
                try:
                    days = (datetime.strptime(today, "%Y-%m-%d") - 
                            datetime.strptime(nps["last_updated"], "%Y-%m-%d")).days
                except Exception:
                    days = 1
                new_count = nps["count"] + max(1, days)
                self.db.update_streak("no_panic_sell", new_count, today)
            elif not nps["last_updated"]:
                self.db.update_streak("no_panic_sell", 1, today)

        # --- DCA consistency streak (weekly) ---
        dca = streaks.get("dca_consistency", {"count": 0, "last_updated": None})
        if has_recent_buy:
            if dca["last_updated"] and dca["last_updated"] != today:
                try:
                    days = (datetime.strptime(today, "%Y-%m-%d") - 
                            datetime.strptime(dca["last_updated"], "%Y-%m-%d")).days
                except Exception:
                    days = 0
                if days >= 7:
                    self.db.update_streak("dca_consistency", dca["count"] + 1, today)
            elif not dca["last_updated"]:
                self.db.update_streak("dca_consistency", 1, today)
        else:
            if dca["last_updated"]:
                try:
                    days = (datetime.strptime(today, "%Y-%m-%d") - 
                            datetime.strptime(dca["last_updated"], "%Y-%m-%d")).days
                    if days >= 14:
                        self.db.update_streak("dca_consistency", 0, today)
                except Exception:
                    pass

    def print_behavior_report(self, symbols: list = None):
        """Print a rich behavior analysis panel."""
        # Always sync trades — fall back to journal coins if no symbols given
        if not symbols and self.journal:
            entries = self.journal.get_entries(limit=200)
            symbols = list({entry["coin"].upper() + "USDT" for entry in entries}) if entries else []
        if symbols:
            self.sync_trades(symbols)

        fomo      = self.calculate_fomo_score()
        overtrade = self.calculate_overtrading_index()
        panic     = self.detect_panic_sells()

        week_ago = int((datetime.utcnow() - timedelta(days=7)).timestamp() * 1000)
        trades = self.db.get_trades(cutoff_ms=week_ago)
        recent_buys = sum(1 for t in trades if t["side"] == "BUY")
        self.update_streaks(has_panic_sell=bool(panic), has_recent_buy=recent_buys > 0)
        streaks = self.get_streaks()  # Get fresh streaks after update

        report = f"""
[bold]🧠 {t('behavior.title')}[/bold]

[yellow]{t('behavior.fomo')}:[/yellow] {fomo['score']}/100 — {fomo['label']}
  {t('behavior.fomo.fg')}: {fomo.get('current_fg', '?')} ({fomo.get('current_fg_label', '?')})
  {t('behavior.fomo.rapid')}: {fomo.get('rapid_buy_clusters', 0)}

[yellow]{t('behavior.overtrade')}:[/yellow] {overtrade['label']}
  {t('behavior.overtrade.total')}: {overtrade['total_30d']}
  {t('behavior.overtrade.week')}: {overtrade['per_week_avg']}
  {overtrade.get('tip', '')}

[yellow]{t('behavior.panic')}:[/yellow]
"""
        if panic:
            for p in panic[:3]:
                sell_fmt = f"{p['sell_price']:.4f}"
                now_fmt = f"{p['current_price']:.4f}"
                # FIX 4: Show pct_above_low in panic sell output
                report += (
                    f"  {t('behavior.panic.found', symbol=p['symbol'], sell=sell_fmt, date=p['sold_at'], now=now_fmt, pct=p['recovery_pct'])}"
                    f"  [dim](sold {p['pct_above_low']:.1f}% above 30d low)[/dim]\n"
                )
        else:
            report += f"  {t('behavior.panic.none')}\n"

        report += f"""
[yellow]{t('behavior.streaks')}:[/yellow]
  {t('behavior.streak.no_panic')}: {t('behavior.streak.days', n=streaks['no_panic_sell']['count'])}
  {t('behavior.streak.dca')}: {t('behavior.streak.weeks', n=streaks['dca_consistency']['count'])}
"""
        console.print(Panel(report, title=f"[bold magenta]BinanceCoach — {t('behavior.title')}[/bold magenta]", border_style="magenta"))
