"""
telegram_bot.py — Full Telegram bot for BinanceCoach (HTML formatting)

All messages use parse_mode="HTML". No Markdown, no MarkdownV2.
Helper functions from modules/tg_utils.py handle escaping & md_to_html conversion.
"""

import os
import logging
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from binance.spot import Spot
from modules.market import MarketData
from modules.portfolio import Portfolio
from modules.dca import DCAAdvisor
from modules.alerts import AlertManager
from modules.behavior import BehaviorCoach
from modules.education import EducationModule
from modules.i18n import t, set_lang, get_lang, LESSONS, tlesson, AVAILABLE_LANGS
from modules.ai_coach import AICoach
from modules.tg_utils import e, bold, italic, code, pre, md_to_html, split_html

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger(__name__)

_uid_raw = os.getenv("TELEGRAM_USER_ID", "0").strip()
AUTHORIZED_USER = int(_uid_raw) if _uid_raw.isdigit() else 0

HTML = "HTML"

# Coin symbols to detect in user questions for /ask context enrichment
KNOWN_SYMBOLS = {
    "BTC", "ETH", "BNB", "ADA", "DOGE", "SHIB", "FLOKI", "ANKR",
    "SOL", "XRP", "DOT", "MATIC", "AVAX", "LINK", "UNI", "TRX",
    "LTC", "ATOM", "NEAR", "APT", "ARB", "OP", "INJ", "SCR",
    "PEPE", "WIF", "BONK", "TRUMP", "FARTCOIN",
}

BOT_COMMANDS = [
    BotCommand("start",       "Show help & command list"),
    BotCommand("portfolio",   "Portfolio health score & analysis"),
    BotCommand("dca",         "Smart DCA recommendations"),
    BotCommand("market",      "Market context for a coin"),
    BotCommand("fg",          "Fear & Greed index"),
    BotCommand("alert",       "Set a price/RSI alert"),
    BotCommand("alerts",      "List active alerts"),
    BotCommand("checkalerts", "Check if any alert triggered"),
    BotCommand("behavior",    "Behavioral bias analysis"),
    BotCommand("project",     "12-month DCA projection"),
    BotCommand("learn",       "Educational lessons"),
    BotCommand("coach",       "AI coaching summary"),
    BotCommand("weekly",      "AI weekly coaching brief"),
    BotCommand("ask",         "Ask Claude anything"),
    BotCommand("models",      "List Claude models"),
    BotCommand("model",       "Switch Claude model"),
    BotCommand("lang",        "Switch language (en/nl)"),
    BotCommand("news",        "Latest Binance news & announcements"),
    BotCommand("listings",    "New coin listings on Binance"),
    BotCommand("launchpool",  "Active launchpools & HODLer airdrops"),
    BotCommand("watchstatus", "Check if news watcher is active"),
    BotCommand("journal",       "Show your decision journal"),
    BotCommand("journaladd",    "Log a decision (e.g. ADA buy 0.262 100 reason)"),
    BotCommand("journaldelete", "Delete a journal entry by id"),
    BotCommand("journalperf",   "Journal P&L vs current prices"),
    BotCommand("pnl",           "P&L summary (FIFO, 365 days)"),
    BotCommand("pnlexport",     "Export P&L to CSV and send as file"),
    BotCommand("rebalance",     "Portfolio rebalancing suggestions"),
    BotCommand("targets",       "Show target allocation"),
    BotCommand("targetsset",    "Set target allocation (e.g. BTC 40 ETH 30)"),
    BotCommand("yield",         "Stablecoin yield optimizer"),
]


async def _send(update: Update, text: str, reply_markup=None):
    """Send an HTML-formatted message, auto-splitting at 4096 chars."""
    chunks = split_html(text)
    for i, chunk in enumerate(chunks):
        await update.message.reply_text(
            chunk,
            parse_mode=HTML,
            reply_markup=reply_markup if i == 0 else None,
        )


def _fmt_usd(val: float) -> str:
    """Format a USD value as a string (no HTML)."""
    return f"${val:,.2f}"

def _fmt_price(val: float) -> str:
    return f"${val:,.4f}"

def _fmt_pct(val: float, sign: bool = False) -> str:
    return f"{val:+.1f}%" if sign else f"{val:.1f}%"


def build_app(client: Spot, market: MarketData):
    """Build and return the fully configured Telegram bot application."""

    portfolio_mod = Portfolio(client, market)
    dca_advisor   = DCAAdvisor(
        market,
        monthly_budget=float(os.getenv("DCA_BUDGET_MONTHLY", 500)),
        risk_profile=os.getenv("RISK_PROFILE", "moderate"),
    )
    behavior_mod  = BehaviorCoach(client, market)
    alert_mgr     = AlertManager(market, telegram_notify=None)

    try:
        ai = AICoach()
    except ValueError:
        ai = None
        logger.warning("Anthropic API key missing — AI commands disabled")

    _app_ref: list = []

    async def notify_async(msg: str):
        if _app_ref and AUTHORIZED_USER:
            try:
                await _app_ref[0].bot.send_message(
                    chat_id=AUTHORIZED_USER,
                    text=msg,
                    parse_mode=HTML,
                )
            except Exception as exc:
                logger.error("notify_async failed: %s", exc)

    # ── Auth ──────────────────────────────────────────────────────────────

    async def auth(update: Update) -> bool:
        if update.effective_user.id != AUTHORIZED_USER:
            await update.message.reply_text(t("general.unauthorized"))
            return False
        return True

    async def require_ai(update: Update) -> bool:
        if ai is None:
            await _send(update, t("tg.ai.no_key"))
            return False
        return True

    def collect_behavior() -> dict:
        # Sync recent trades first so analysis reflects actual history
        try:
            behavior_mod.sync_trades(["DOGEUSDT", "ADAUSDT", "BTCUSDT", "ETHUSDT",
                                       "BNBUSDT", "SHIBUSDT", "ANKRUSDT", "FLOKIUSDT"], days=30)
        except Exception:
            pass  # Non-fatal: analysis works on cached DB data
        fomo      = behavior_mod.calculate_fomo_score()
        overtrade = behavior_mod.calculate_overtrading_index()
        panic     = behavior_mod.detect_panic_sells()
        return {
            "fomo_raw":        fomo,
            "fomo_score":      fomo["score"],
            "fomo_label":      fomo["label"],
            "over_raw":        overtrade,
            "total_trades":    overtrade["total_30d"],
            "per_week":        overtrade["per_week_avg"],
            "overtrade_label": overtrade["label"],
            "panic_list":      panic,
        }

    # ── /start ────────────────────────────────────────────────────────────

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, t("tg.start"))

    # ── /lang ─────────────────────────────────────────────────────────────

    async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        args = context.args
        if args and args[0].lower() in AVAILABLE_LANGS:
            set_lang(args[0].lower())
            await _send(update, t("tg.lang_set"))
            return
        buttons = [
            InlineKeyboardButton(label, callback_data="setlang:" + lang_code)
            for lang_code, label in AVAILABLE_LANGS.items()
        ]
        keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            t("tg.lang_choose"),
            parse_mode=HTML,
            reply_markup=markup,
        )

    async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query.from_user.id != AUTHORIZED_USER:
            await query.answer("⛔ Unauthorized")
            return
        await query.answer()
        lang_code = query.data.split(":", 1)[1]
        if lang_code in AVAILABLE_LANGS:
            set_lang(lang_code)
            await query.edit_message_text(t("tg.lang_set"), parse_mode=HTML)

    # ── /portfolio ────────────────────────────────────────────────────────

    async def portfolio_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, t("tg.analyzing"))
        try:
            balances = portfolio_mod.get_balances()
            health   = portfolio_mod.calculate_health_score(balances)

            title     = t("portfolio.title", score=health["score"], grade=health["grade"])
            total_str = _fmt_usd(health["total_usd"])

            lines = [
                "💼 " + bold(title),
                "",
                t("portfolio.total") + ": " + bold(total_str),
                t("portfolio.stablecoins") + ": " + str(health["stable_pct"]) + "%",
                t("portfolio.holdings") + ": " + str(health["n_assets"]),
                "",
                bold(t("portfolio.top_holdings") + ":"),
            ]
            for b in balances[:8]:
                pct      = b["usd_value"] / health["total_usd"] * 100
                asset    = e(b.get("display", b["asset"]))
                val_str  = code(_fmt_usd(b["usd_value"]))
                pct_str  = _fmt_pct(pct)
                lines.append("• " + asset + ": " + val_str + " (" + pct_str + ")")

            if health["suggestions"]:
                lines += ["", bold(t("portfolio.suggestions") + ":")]
                for s in health["suggestions"]:
                    lines.append("• " + e(s))

            await _send(update, "\n".join(lines))
        except Exception as exc:
            await _send(update, t("tg.error", error=e(str(exc))))

    # ── /dca ──────────────────────────────────────────────────────────────

    async def dca_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        symbols = [s.upper() for s in context.args] if context.args else ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        await _send(update, t("tg.fetching_dca", symbols=e(", ".join(symbols))))

        for symbol in symbols[:3]:
            try:
                rec = dca_advisor.get_recommendation(symbol)

                price_str   = code(_fmt_price(rec["price"]))
                rsi_str     = code(str(rec["rsi"]))
                rsi_zone    = e(rec.get("rsi_zone_label", rec["rsi_zone"]))
                fg_str      = code(str(rec["fg_value"]))
                fg_label    = e(rec["fg_label"])
                sma_str     = code(_fmt_pct(rec["price_vs_sma200"], sign=True))
                weekly_str  = bold(t("dca.col.weekly") + ": " + _fmt_usd(rec["suggested_weekly_usd"]))
                base_info   = italic(t("tg.dca_base",
                                       base=str(round(rec["base_weekly_usd"], 2)),
                                       mult=str(rec["multiplier"])))

                lines = [
                    "📐 " + bold(symbol + " DCA"),
                    "",
                    t("market.price") + ": " + price_str,
                    t("market.rsi") + ": " + rsi_str + " (" + rsi_zone + ")",
                    t("market.fear_greed") + ": " + fg_str + " (" + fg_label + ")",
                    t("market.vs_sma200") + ": " + sma_str,
                    "",
                    "💰 " + weekly_str,
                    base_info,
                    "",
                    t("tg.dca_why"),
                ]
                for r in rec["rationale"]:
                    lines.append(e(r))

                await _send(update, "\n".join(lines))
            except Exception as exc:
                await _send(update, "❌ " + bold(symbol) + ": " + e(str(exc)))

    # ── /market ───────────────────────────────────────────────────────────

    async def market_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        try:
            ctx = market.get_market_context(symbol)
            fg  = ctx["fear_greed"]

            lines = [
                "📊 " + bold(t("market.title", symbol=e(symbol))),
                "",
                t("market.price")      + ":  " + code(_fmt_price(ctx["price"])),
                t("market.rsi")        + ":    " + code(str(ctx["rsi"])) + " (" + e(ctx["rsi_zone_label"]) + ")",
                t("market.trend")      + ":  " + e(ctx["trend"]),
                t("market.sma50")      + ": " + code(_fmt_usd(ctx["sma_50"])),
                t("market.sma200")     + ": " + code(_fmt_usd(ctx["sma_200"])),
                t("market.ema21")      + ": " + code(_fmt_usd(ctx["ema_21"])),
                t("market.vs_sma200")  + ": " + code(_fmt_pct(ctx["vs_sma200_pct"], sign=True)),
                t("market.fear_greed") + ": " + code(str(fg["value"])) + " (" + e(fg["classification"]) + ")",
            ]
            await _send(update, "\n".join(lines))
        except Exception as exc:
            await _send(update, "❌ " + bold(symbol) + ": " + e(str(exc)))

    # ── /fg ───────────────────────────────────────────────────────────────

    async def fg_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        fg  = market.get_fear_greed()
        val = fg["value"]
        emj = "😱" if val < 25 else "😰" if val < 40 else "😐" if val < 55 else "😄" if val < 75 else "🤑"
        advice = (
            t("tg.fg_accumulate") if val < 30 else
            t("tg.fg_careful")    if val > 75 else
            t("tg.fg_neutral")
        )
        lines = [
            emj + " " + bold(t("cli.fg_title")),
            "",
            t("cli.fg_score")  + ": " + bold(str(val) + "/100"),
            t("cli.fg_status") + ": " + bold(e(fg["classification"])),
            "",
            italic(e(advice)),
        ]
        await _send(update, "\n".join(lines))

    # ── /alert ────────────────────────────────────────────────────────────

    async def alert_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        args = context.args
        if len(args) < 3:
            await _send(update, t("tg.alert_usage"))
            return
        symbol    = args[0].upper()
        condition = args[1].lower()
        if condition not in ("above", "below", "rsi_above", "rsi_below"):
            await _send(update, t("tg.alert_usage"))
            return
        try:
            threshold = float(args[2])
        except ValueError:
            await _send(update, t("tg.alert_usage"))
            return
        notes = " ".join(args[3:]) if len(args) > 3 else ""
        alert_mgr.add_alert(symbol, condition, threshold, notes)
        await _send(update, t("tg.alert_set",
                               symbol=e(symbol),
                               condition=e(condition),
                               threshold=e(str(threshold))))

    # ── /alerts ───────────────────────────────────────────────────────────

    async def alerts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        alerts = alert_mgr.db.get_active_alerts()
        if not alerts:
            await _send(update, t("alert.none"))
            return
        lines = [bold(t("alert.title") + ":"), ""]
        for alert in alerts:
            created_at = alert.get("created_at", "") or ""
            line = "• " + code(alert["symbol"]) + " " + e(alert["condition"]) + " " + code(str(alert["threshold"]))
            if alert["notes"]:
                line += " — " + italic(e(alert["notes"]))
            if created_at:
                line += " " + italic("(set " + e(created_at[:10]) + ")")
            lines.append(line)
        await _send(update, "\n".join(lines))

    # ── /checkalerts ──────────────────────────────────────────────────────

    async def checkalerts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, t("tg.checking_alerts"))
        fired = alert_mgr.check_alerts()
        if not fired:
            await _send(update, t("alert.none_triggered"))
            return
        for f in fired:
            sym     = e(f["symbol"])
            header  = "🔔 " + bold(t("alert.triggered_title", symbol=sym)) + "\n\n"
            body    = md_to_html(f.get("context", ""))
            await _send(update, header + body)

    # ── /behavior ─────────────────────────────────────────────────────────

    async def behavior_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "🧠 " + e(t("behavior.title")) + "...")
        try:
            beh      = collect_behavior()
            fomo_raw = beh["fomo_raw"]
            over_raw = beh["over_raw"]

            lines = [
                "🧠 " + bold(t("behavior.title")),
                "",
                t("tg.behavior.fomo") + " " + code(str(beh["fomo_score"]) + "/100") + " — " + e(beh["fomo_label"]),
                t("behavior.fomo.fg") + ": " + code(str(fomo_raw.get("current_fg", "?"))) +
                    " (" + e(str(fomo_raw.get("current_fg_label", "?"))) + ")",
                "",
                t("tg.behavior.overtrade") + " " + e(beh["overtrade_label"]),
                t("behavior.overtrade.total") + ": " + str(beh["total_trades"]),
                t("behavior.overtrade.week") + ": " + str(beh["per_week"]),
            ]
            if over_raw.get("tip"):
                lines.append("💡 " + italic(e(over_raw["tip"])))

            lines += ["", t("tg.behavior.panic")]
            if beh["panic_list"]:
                for p in beh["panic_list"][:3]:
                    sell_str    = code(_fmt_price(p["sell_price"]))
                    now_str     = code(_fmt_price(p["current_price"]))
                    recov_str   = bold("(+" + str(p["recovery_pct"]) + "%)")
                    sym_str     = code(p["symbol"])
                    lines.append(
                        "⚠️ Sold " + sym_str + " @ " + sell_str +
                        " (" + e(p["sold_at"]) + ") → now " + now_str + " " + recov_str
                    )
            else:
                lines.append(t("behavior.panic.none"))

            lines += ["", bold(t("behavior.streaks") + ":")]
            streaks = behavior_mod.get_streaks()
            lines.append(
                "• " + t("behavior.streak.no_panic") + ": " +
                code(str(streaks["no_panic_sell"]["count"])) + " " +
                t("behavior.streak.days", n="")
            )
            lines.append(
                "• " + t("behavior.streak.dca") + ": " +
                code(str(streaks["dca_consistency"]["count"])) + " " +
                t("behavior.streak.weeks", n="")
            )

            await _send(update, "\n".join(lines))
        except Exception as exc:
            await _send(update, t("tg.error", error=e(str(exc))))

    # ── /project ──────────────────────────────────────────────────────────

    async def project_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        try:
            proj = dca_advisor.project_accumulation(symbol, months=12)
            lines = [
                "📈 " + bold(t("dca.projection.title", symbol=e(symbol), months=12)),
                "",
                t("dca.projection.invested") + ": " + bold(_fmt_usd(proj["total_invested"])),
                t("dca.projection.value")    + ": " + bold(_fmt_usd(proj["projected_value"])),
                t("dca.projection.roi")      + ": " + bold("+" + str(proj["roi_pct"]) + "%"),
                "",
                italic(e(proj["note"])),
            ]
            await _send(update, "\n".join(lines))
        except Exception as exc:
            await _send(update, "❌ " + bold(symbol) + ": " + e(str(exc)))

    # ── /learn ────────────────────────────────────────────────────────────

    async def learn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not context.args:
            lines = ["📚 " + bold(t("edu.table.title") + ":"), ""]
            for key in LESSONS:
                lesson = tlesson(key)
                title  = e(lesson["title"]) if lesson else e(key)
                lines.append("• " + code(key) + " — " + title)
            lines.append(t("tg.learn_list_suffix"))
            await _send(update, "\n".join(lines))
            return

        topic  = context.args[0].lower()
        lesson = tlesson(topic)
        if not lesson:
            await _send(update, t("tg.learn_not_found", topic=e(topic)))
            return

        header = "📚 " + bold(e(lesson["title"])) + "\n\n"
        body   = e(lesson["content"])
        await _send(update, header + body)

    # ── /coach ────────────────────────────────────────────────────────────

    async def coach_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not await require_ai(update): return
        await _send(update, t("tg.ai.analyzing"))
        try:
            balances = portfolio_mod.get_balances()
            health   = portfolio_mod.calculate_health_score(balances)
            ctx      = market.get_market_context("BTCUSDT")
            beh_data = collect_behavior()
            result   = ai.coaching_summary(health, ctx, beh_data)
            header   = "🤖 " + bold("Coaching Summary") + " " + code(ai.model) + "\n\n"
            await _send(update, header + md_to_html(result))
        except Exception as exc:
            await _send(update, t("tg.ai.error", error=e(str(exc))))

    # ── /weekly ───────────────────────────────────────────────────────────

    async def weekly_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not await require_ai(update): return
        await _send(update, t("tg.ai.weekly"))
        try:
            balances       = portfolio_mod.get_balances()
            health         = portfolio_mod.calculate_health_score(balances)
            ctx            = market.get_market_context("BTCUSDT")
            beh_data       = collect_behavior()
            market_summary = {
                "trend":    ctx["trend"],
                "fg_value": ctx["fear_greed"]["value"],
                "fg_label": ctx["fear_greed"]["classification"],
            }
            dca_recs = [dca_advisor.get_recommendation(s) for s in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]]
            result   = ai.weekly_brief(health, beh_data, market_summary, dca_recs)
            header   = "📋 " + bold("Weekly Brief") + " " + code(ai.model) + "\n\n"
            await _send(update, header + md_to_html(result))
        except Exception as exc:
            await _send(update, t("tg.ai.error", error=e(str(exc))))

    # ── /ask ──────────────────────────────────────────────────────────────

    async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not await require_ai(update): return
        if not context.args:
            example = "wat moet ik doen met mijn DOGE positie?" if get_lang() == "nl" else "should I buy more BTC now?"
            await _send(update, t("tg.ai.no_question", example=e(example)))
            return

        question = " ".join(context.args)
        await _send(update, t("tg.ai.asking"))

        try:
            import re

            # ── 1. Portfolio + behavior ───────────────────────────────────
            balances = portfolio_mod.get_balances()
            health   = portfolio_mod.calculate_health_score(balances)
            beh_data = collect_behavior()
            fg       = market.get_fear_greed()

            # Enrich balances with pct field
            total = health["total_usd"] or 1
            for b in balances:
                b["pct"] = b["usd_value"] / total * 100

            # ── 2. Detect coin symbols in the question ────────────────────
            #    Match word-boundary uppercase tokens OR lowercase coin names
            words = re.findall(r"\b[A-Za-z]{2,10}\b", question)
            mentioned_symbols = set()
            for w in words:
                upper = w.upper()
                if upper in KNOWN_SYMBOLS:
                    mentioned_symbols.add(upper)
            # Also check holdings — if user says "my portfolio" fetch BTC too
            if not mentioned_symbols or any(
                kw in question.lower() for kw in ("portfolio", "holdings", "alles", "everything")
            ):
                mentioned_symbols.add("BTC")

            # ── 3. Fetch market data for mentioned coins ──────────────────
            coin_data = {}
            for sym in mentioned_symbols:
                pair = sym + "USDT" if not sym.endswith("USDT") else sym
                try:
                    coin_data[sym] = market.get_market_context(pair)
                except Exception:
                    pass

            # ── 4. Build full context dict ────────────────────────────────
            ctx = {
                "total_usd":       health["total_usd"],
                "score":           health["score"],
                "grade":           health["grade"],
                "stable_pct":      health["stable_pct"],
                "suggestions":     health["suggestions"],
                "holdings":        balances[:10],
                "fg_value":        fg["value"],
                "fg_label":        fg["classification"],
                "fomo_score":      beh_data["fomo_score"],
                "overtrade_label": beh_data["overtrade_label"],
                "panic_count":     len(beh_data["panic_list"]),
                "coin_data":       coin_data,
            }

            result = ai.chat(question, ctx)
            header = "💬 " + bold("Claude") + " " + code(ai.model) + "\n\n"
            await _send(update, header + md_to_html(result))
        except Exception as exc:
            await _send(update, t("tg.ai.error", error=e(str(exc))))

    # ── /models ───────────────────────────────────────────────────────────

    async def models_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not await require_ai(update): return
        models = ai.list_models()
        lines  = [
            "🤖 " + bold("Available Claude Models"),
            "Active: " + code(ai.model),
            "",
        ]
        for m in models:
            marker = " ✅" if m["id"] == ai.model else ""
            lines.append("• " + code(e(m["id"])) + marker)
            lines.append("  " + italic(e(m["desc"])))
        lines += ["", t("tg.ai.models_footer")]
        await _send(update, "\n".join(lines))

    # ── /model ────────────────────────────────────────────────────────────

    async def model_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        if not await require_ai(update): return
        if not context.args:
            await _send(update, t("tg.ai.model_usage"))
            return
        ai.set_model(context.args[0])
        await _send(update, t("tg.ai.model_switched", model=e(ai.model)))

    # ── Build app ─────────────────────────────────────────────────────────

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

    app = Application.builder().token(token).build()
    _app_ref.append(app)
    alert_mgr.telegram_notify = notify_async

    handlers = [
        ("start",        start),
        ("lang",         lang_cmd),
        ("portfolio",    portfolio_cmd),
        ("dca",          dca_cmd),
        ("market",       market_cmd),
        ("fg",           fg_cmd),
        ("alert",        alert_cmd),
        ("alerts",       alerts_cmd),
        ("checkalerts",  checkalerts_cmd),
        ("behavior",     behavior_cmd),
        ("project",      project_cmd),
        ("learn",        learn_cmd),
        ("coach",        coach_cmd),
        ("weekly",       weekly_cmd),
        ("ask",          ask_cmd),
        ("models",       models_cmd),
        ("model",        model_cmd),
    ]
    for cmd, fn in handlers:
        app.add_handler(CommandHandler(cmd, fn))

    app.add_handler(CallbackQueryHandler(lang_callback, pattern=r"^setlang:"))

    # ── News / Listings / Launchpool commands ─────────────────────────────

    async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Fetching latest Binance news...</i>")
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_latest_news(limit=5)
        await _send(update, news_mod.format_news_html(articles))

    async def listings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Fetching new listings...</i>")
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_new_listings(limit=5)
        await _send(update, news_mod.format_listings_html(articles))

    async def launchpool_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Checking launchpools &amp; airdrops...</i>")
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_launchpool(limit=5)
        await _send(update, news_mod.format_launchpool_html(articles))

    app.add_handler(CommandHandler("news",        news_cmd))
    app.add_handler(CommandHandler("listings",    listings_cmd))
    app.add_handler(CommandHandler("launchpool",  launchpool_cmd))

    # ── Decision Journal ─────────────────────────────────────────────────────

    async def journal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        coin_arg = context.args[0].upper() if context.args else None
        await _send(update, j.format_journal_html(coin=coin_arg))

    async def journaladd_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usage: /journaladd COIN BUY/SELL PRICE [AMOUNT] [notes...]"""
        if not await auth(update): return
        args = context.args
        if not args or len(args) < 3:
            await _send(update,
                "❌ Usage: <code>/journaladd COIN BUY/SELL PRICE [AMOUNT] [notes...]</code>\n"
                "Example: <code>/journaladd ADA buy 0.262 100 oversold -49% SMA200</code>"
            )
            return
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        coin_arg   = args[0]
        action_arg = args[1]
        try:
            price_arg = float(args[2])
        except ValueError:
            await _send(update, f"❌ Invalid price: <code>{args[2]}</code>")
            return
        # Fix: is not None check — amount=0 is valid but falsy
        try:
            amount_arg = float(args[3]) if len(args) > 3 and _is_num_str(args[3]) else None
        except (ValueError, IndexError):
            amount_arg = None
        notes_start = 4 if amount_arg is not None else 3
        notes_arg   = " ".join(args[notes_start:]) if len(args) > notes_start else ""
        try:
            j.add_entry(coin_arg, action_arg, price_arg, amount_arg, notes_arg)
            await _send(update,
                f"✅ Logged: <b>{action_arg.upper()} {coin_arg.upper()}</b> @ ${price_arg:,.4f}"
                + (f" (${amount_arg:,.2f})" if amount_arg is not None else "")
                + (f"\n<i>{notes_arg}</i>" if notes_arg else "")
            )
        except ValueError as e:
            await _send(update, f"❌ {e}")

    async def journaldelete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usage: /journaldelete <id>"""
        if not await auth(update): return
        if not context.args or not context.args[0].isdigit():
            await _send(update, "❌ Usage: <code>/journaldelete &lt;id&gt;</code>\nFind the id with /journal")
            return
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        ok = j.delete_entry(int(context.args[0]))
        if ok:
            await _send(update, f"🗑️ Entry #{context.args[0]} deleted.")
        else:
            await _send(update, f"❌ No entry with id={context.args[0]}")

    async def journalperf_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Calculating journal performance...</i>")
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        await _send(update, j.format_performance_html())

    app.add_handler(CommandHandler("journal",       journal_cmd))
    app.add_handler(CommandHandler("journaladd",    journaladd_cmd))
    app.add_handler(CommandHandler("journaldelete", journaldelete_cmd))
    app.add_handler(CommandHandler("journalperf",   journalperf_cmd))

    # ── P&L Calculator ───────────────────────────────────────────────────────

    async def pnl_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Fetching trade history from Binance (365 days)...</i>")
        from modules.pnl import PnLCalculator
        pnl_mod = PnLCalculator(client, market, portfolio_mod)
        sym = context.args[0].upper() if context.args else None
        await _send(update, pnl_mod.format_pnl_html(symbol=sym))

    async def pnlexport_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Generating P&amp;L export (365 days)...</i>")
        from modules.pnl import PnLCalculator
        pnl_mod = PnLCalculator(client, market, portfolio_mod)
        export_path = pnl_mod.export_csv()
        if export_path and export_path.exists():
            await update.message.reply_document(
                document=open(export_path, "rb"),
                filename=export_path.name,
                caption=(
                    "💰 P&L Export (FIFO, 365 days)\n"
                    "Import into Koinly or CoinTracking for a full tax report.\n"
                    "⚠️ Not tax advice — fees excluded."
                )
            )
        else:
            await _send(update, "❌ No trade history found to export.")

    app.add_handler(CommandHandler("pnl",       pnl_cmd))
    app.add_handler(CommandHandler("pnlexport", pnlexport_cmd))

    # ── Rebalancing ──────────────────────────────────────────────────────────

    async def rebalance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Analysing portfolio vs targets...</i>")
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio_mod)
        await _send(update, rb.format_rebalance_html())

    async def targets_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio_mod)
        await _send(update, rb.format_targets_html())

    async def targetsset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        # /targetsset BTC 40 ETH 30 BNB 20 ADA 10
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio_mod)
        args = context.args
        if not args:
            await _send(update, "❌ Usage: <code>/targetsset BTC 40 ETH 30 BNB 20 ADA 10</code>")
            return
        allocations = {}
        i = 0
        while i < len(args) - 1:
            try:
                allocations[args[i].upper()] = float(args[i + 1])
                i += 2
            except (ValueError, IndexError):
                i += 1
        if not allocations:
            await _send(update, "❌ Usage: <code>/targetsset BTC 40 ETH 30 BNB 20 ADA 10</code>")
            return
        # Show what's being replaced before saving
        old_targets = rb._load_targets()
        ok = rb.set_targets(allocations)
        if ok:
            lines = ["✅ <b>Target allocation saved:</b>"]
            for coin, pct in sorted(allocations.items(), key=lambda x: -x[1]):
                lines.append(f"• <b>{coin}</b> — {pct:.1f}%")
            if old_targets:
                lines.append("\n<i>Previous targets were replaced.</i>")
            await _send(update, "\n".join(lines))
        else:
            total = sum(allocations.values())
            await _send(update, f"❌ Targets must sum to 100% (got {total:.1f}%). Check your numbers.")

    app.add_handler(CommandHandler("rebalance",  rebalance_cmd))
    app.add_handler(CommandHandler("targets",    targets_cmd))
    app.add_handler(CommandHandler("targetsset", targetsset_cmd))

    # ── Yield Optimizer ──────────────────────────────────────────────────────

    async def yield_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        await _send(update, "<i>Checking Binance Simple Earn rates...</i>")
        from modules.yield_optimizer import YieldOptimizer
        yo = YieldOptimizer(client, portfolio_mod)
        await _send(update, yo.format_yield_html())

    def _is_num_str(s: str) -> bool:
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False

    app.add_handler(CommandHandler("yield", yield_cmd))

    async def watchstatus_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await auth(update): return
        from modules.news import watcher_status
        status = watcher_status()
        if status["running"]:
            await _send(update, f"👁 <b>Watcher is running</b> (PID {status['pid']})\nPolling Binance every 2 min via bot job queue.")
        else:
            await _send(update, "🔴 <b>Standalone watcher not running.</b>\nThe bot's built-in job checks every 2 min automatically while the bot is active.\nFor always-on watching, run: <code>bc.sh watch-bg</code> on your server.")

    app.add_handler(CommandHandler("watchstatus", watchstatus_cmd))

    # ── Background alert polling ───────────────────────────────────────────
    ALERT_POLL_INTERVAL = 300  # seconds (5 minutes)
    authorized_uid = int(os.getenv("TELEGRAM_USER_ID", "0"))

    async def poll_alerts(context) -> None:
        """Background job: check alerts every 5 min, push notification if triggered."""
        try:
            fired = alert_mgr.check_alerts()
            if not fired:
                return
            for f in fired:
                raw = f.get("context", "")
                # Convert any leftover Markdown to HTML
                html = md_to_html(raw) if raw else (
                    f"<b>🔔 {e(f['symbol'])} Alert Triggered!</b>\n"
                    f"Condition: <code>{e(f['condition'])} {f['threshold']}</code>"
                )
                try:
                    await context.bot.send_message(
                        chat_id=authorized_uid,
                        text=html,
                        parse_mode=HTML,
                    )
                    logger.info("Alert notification sent for %s", f["symbol"])
                except Exception as send_err:
                    logger.warning("Failed to send alert notification: %s", send_err)
        except Exception as exc:
            logger.warning("Alert poll error: %s", exc)

    async def news_check_job(context) -> None:
        """Background job: check for new Binance announcements every 30 min."""
        try:
            from modules.news import BinanceNews
            news_mod = BinanceNews(portfolio=portfolio_mod)
            result = news_mod.check_and_format_new()
            if not result["has_new"] or not authorized_uid:
                return
            parts_html = []
            if result["launchpool"]:
                parts_html.append(news_mod.format_launchpool_html(result["launchpool"]))
            if result["listings"]:
                parts_html.append(news_mod.format_listings_html(result["listings"]))
            if result["news"]:
                parts_html.append(news_mod.format_news_html(result["news"], "📰 New Binance Announcement"))
            if result["portfolio_hits"]:
                hits_text = "\n".join(
                    f"⚡ {h.get('matched_asset','?')}: {h['title']}"
                    for h in result["portfolio_hits"]
                )
                parts_html.append(f"<b>⚡ Affects your portfolio:</b>\n{hits_text}")
            if parts_html:
                msg = "\n\n".join(parts_html)
                for chunk in split_html(msg):
                    await context.bot.send_message(
                        chat_id=authorized_uid,
                        text=chunk,
                        parse_mode=HTML,
                    )
        except Exception as exc:
            logger.warning("News check job error: %s", exc)

    async def post_init(application: Application):
        await application.bot.set_my_commands(BOT_COMMANDS)
        logger.info("Bot commands registered with Telegram")

        if authorized_uid:
            application.job_queue.run_repeating(
                poll_alerts,
                interval=ALERT_POLL_INTERVAL,
                first=60,
                name="alert_poller",
            )
            logger.info("Alert poller started — checking every %ds", ALERT_POLL_INTERVAL)
            application.job_queue.run_repeating(
                news_check_job,
                interval=120,  # 2 minutes
                first=90,      # first check after 90 seconds
                name="news_poller",
            )
            logger.info("News poller started — checking every 2 minutes")
        else:
            logger.warning("TELEGRAM_USER_ID not set — alert/news polling disabled")

    app.post_init = post_init

    return app
