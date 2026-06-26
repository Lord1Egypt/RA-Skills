#!/usr/bin/env python3
"""
BinanceCoach — AI-Powered Trading Behavior Coach
Entry point: CLI mode and Telegram bot mode

Usage:
    python main.py                    # Interactive CLI
    python main.py --telegram         # Telegram bot mode
    python main.py --demo             # Demo mode (no API keys needed)
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from modules.i18n import t, set_lang, get_lang, AVAILABLE_LANGS

# Load env
load_dotenv()
os.makedirs("data", exist_ok=True)

# Set language from env (can be overridden at runtime with 'lang nl' command or --lang flag)
_default_lang = os.getenv("LANGUAGE", "en").lower()
try:
    set_lang(_default_lang)
except ValueError:
    set_lang("en")

console = Console()

BANNER = """
██████╗ ██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗
██╔══██╗██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝
██████╔╝██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  
██╔══██╗██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  
██████╔╝██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗
╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
       ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗
      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██║  ██║
      ██║     ██║   ██║███████║██║     ███████║
      ██║     ██║   ██║██╔══██║██║     ██╔══██║
      ╚██████╗╚██████╔╝██║  ██║╚██████╗██║  ██║
       ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""


def init_clients():
    """Initialize Binance client."""
    from binance.spot import Spot
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    if not api_key or api_key == "your_read_only_api_key_here":
        console.print("[yellow]⚠️  No Binance API keys found. Market data only (no portfolio).[/yellow]")
        return Spot()  # Public endpoints only
    return Spot(api_key=api_key, api_secret=api_secret)


def run_demo():
    """Demo mode — shows what BinanceCoach can do without API keys."""
    from modules.market import MarketData
    from modules.dca import DCAAdvisor
    from modules.education import EducationModule

    client = init_clients()
    market = MarketData(client)
    dca = DCAAdvisor(market, monthly_budget=500, risk_profile="moderate")
    edu = EducationModule()

    console.print(Panel(
        "[bold cyan]Demo Mode[/bold cyan] — Showing BinanceCoach capabilities without API keys",
        border_style="cyan"
    ))

    # Market overview
    console.print("\n[bold]📊 Market Overview[/bold]")
    for symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]:
        ctx = market.get_market_context(symbol)
        fg = ctx["fear_greed"]
        console.print(
            f"  {symbol}: ${ctx['price']:,.2f} | RSI: {ctx['rsi']} ({ctx['rsi_zone']}) | "
            f"Trend: {ctx['trend']} | vs SMA200: {ctx['vs_sma200_pct']:+.1f}%"
        )

    console.print(f"\n[bold]😱 Fear & Greed: {fg['value']} — {fg['classification']}[/bold]")

    # DCA recommendations
    console.print("\n")
    dca.print_recommendations(["BTCUSDT", "ETHUSDT", "BNBUSDT"])

    # Education tip
    console.print("\n[bold]📚 Today's Lesson:[/bold]")
    edu.explain("dca")

    # Projection
    console.print("\n[bold]📈 DCA Projection (12 months, BTCUSDT):[/bold]")
    proj = dca.project_accumulation("BTCUSDT", months=12)
    console.print(
        f"  Invest ${proj['total_invested']:,.2f} → Projected: ${proj['projected_value']:,.2f} "
        f"(+{proj['roi_pct']}% if avg 5%/mo growth)"
    )
    console.print(f"  ⚠️  {proj['note']}", style="dim")


def run_cli():
    """Interactive CLI mode — delegates to _dispatch_command() for all commands."""
    from modules.market import MarketData
    from modules.portfolio import Portfolio
    from modules.dca import DCAAdvisor
    from modules.alerts import AlertManager
    from modules.behavior import BehaviorCoach
    from modules.education import EducationModule
    from modules.ai_coach import AICoach
    from modules.journal import DecisionJournal

    client = init_clients()
    market = MarketData(client)
    portfolio = Portfolio(client, market)
    dca = DCAAdvisor(
        market,
        monthly_budget=float(os.getenv("DCA_BUDGET_MONTHLY", 500)),
        risk_profile=os.getenv("RISK_PROFILE", "moderate")
    )
    alert_mgr = AlertManager(market)
    _journal  = DecisionJournal(market=market)
    behavior  = BehaviorCoach(client, market, journal=_journal)
    edu = EducationModule()

    # AI coach — optional, graceful fallback if no API key
    ai = None
    try:
        ai = AICoach()
        ai_status = f"[green]AI: {ai.model}[/green]"
    except ValueError:
        ai_status = "[yellow]AI: no key[/yellow]"

    console.print(BANNER, style="cyan")
    console.print("[bold cyan]BinanceCoach — AI Trading Behavior Coach[/bold cyan]")
    console.print(f"[dim]Lang: {get_lang().upper()} | {ai_status} | Type 'help' for commands[/dim]\n")

    while True:
        try:
            cmd = input("coach> ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Goodbye! Trade smart. 👋[/yellow]")
            break

        if not cmd:
            continue

        parts = cmd.split()

        # Handle `lang` specially — affects REPL state, not in _dispatch_command
        if parts[0].lower() == "lang":
            if len(parts) > 1 and parts[1].lower() in AVAILABLE_LANGS:
                set_lang(parts[1].lower())
                console.print(f"[green]{t('cli.lang_switched')}[/green]")
            else:
                lang_list = "\n".join(
                    f"  {'→' if code == get_lang() else ' '} [cyan]{code}[/cyan]  {label}"
                    for code, label in AVAILABLE_LANGS.items()
                )
                console.print(t("cli.lang_list", langs=lang_list))
            continue

        # Delegate all other commands to the shared dispatcher
        should_continue = _dispatch_command(
            cmd, client, market, portfolio, dca,
            alert_mgr, behavior, edu, ai, console
        )
        if not should_continue:
            break


def run_telegram():
    """Start the Telegram bot."""
    import asyncio
    from modules.market import MarketData
    from bot.telegram_bot import build_app

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        console.print("[red]❌ TELEGRAM_BOT_TOKEN not set in .env[/red]")
        console.print("[dim]Add it with: TELEGRAM_BOT_TOKEN=your_token_here[/dim]")
        return

    client = init_clients()
    market = MarketData(client)
    app = build_app(client, market)

    async def _print_bot_info():
        info = await app.bot.get_me()
        console.print(f"[green]🤖 Bot started: @{info.username} (ID: {info.id})[/green]")
        console.print(f"[dim]Authorized user: {os.getenv('TELEGRAM_USER_ID', 'anyone')}[/dim]")

    asyncio.get_event_loop().run_until_complete(_print_bot_info()) if not app.running else None
    console.print("[green]🤖 Starting Telegram bot... (Ctrl+C to stop)[/green]")
    app.run_polling()


def run_command(cmd_str: str):
    """
    Non-interactive single-command mode for OpenClaw skill / scripting.
    No banner, no prompt — just output the result and exit.
    Used by: openclaw-skill/binance-coach/scripts/bc.sh
    """
    from modules.market import MarketData
    from modules.portfolio import Portfolio
    from modules.dca import DCAAdvisor
    from modules.alerts import AlertManager
    from modules.behavior import BehaviorCoach
    from modules.education import EducationModule
    from modules.journal import DecisionJournal

    client = init_clients()
    market = MarketData(client)
    portfolio = Portfolio(client, market)
    dca = DCAAdvisor(
        market,
        monthly_budget=float(os.getenv("DCA_BUDGET_MONTHLY", 500)),
        risk_profile=os.getenv("RISK_PROFILE", "moderate")
    )
    alert_mgr  = AlertManager(market)
    _journal_b = DecisionJournal(market=market)
    behavior   = BehaviorCoach(client, market, journal=_journal_b)
    edu = EducationModule()

    try:
        ai = None
        from modules.ai_coach import AICoach
        ai = AICoach()
    except Exception:
        pass

    # Reuse the same dispatch logic as the interactive CLI
    _dispatch_command(
        cmd_str.strip(), client, market, portfolio, dca,
        alert_mgr, behavior, edu, ai, console
    )


def _is_num(s: str) -> bool:
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def _dispatch_command(cmd_str, client, market, portfolio, dca, alert_mgr, behavior, edu, ai, console):
    """
    Shared command dispatcher — used by both run_cli() and run_command().
    Returns True to continue loop, False to exit (for 'quit').
    """
    import re as _re
    parts = cmd_str.strip().split()
    if not parts:
        return True

    if parts[0] in ("quit", "exit", "q"):
        return False

    elif parts[0] == "portfolio":
        console.print()
        try:
            balances = portfolio.get_balances()
            health   = portfolio.calculate_health_score(balances)
            portfolio.print_portfolio_table(balances, health)
            fg = None
            try:
                fg = market.get_fear_greed()
            except Exception:
                pass
            portfolio.save_snapshot(balances, health, fg=fg)  # auto-save to coach.db

            # Issue #7: Suggest import-orders if order history is empty
            from modules.coach_db import CoachDB
            db = CoachDB()
            if not db.has_orders():
                console.print()
                console.print("[dim]💡 Tip: Run [cyan]import-orders[/cyan] to import your Binance trade history.[/dim]")
                console.print("[dim]   This enables P&L tracking, behavior analysis, and better coaching.[/dim]")
        except Exception as e:
            msg = str(e)
            if "401" in msg or "Invalid API-key" in msg:
                console.print("[red]❌ Binance API error: Invalid or expired API key.[/red]")
                console.print("[dim]→ Go to binance.com → API Management → check your key is active and has 'Enable Reading' permission.[/dim]")
            else:
                console.print(f"[red]❌ Portfolio error: {e}[/red]")

    elif parts[0] == "dca":
        if len(parts) > 1:
            symbols = [s.upper() for s in parts[1:]]
        else:
            # FIX 5: Auto-detect from portfolio holdings
            try:
                _bals = portfolio.get_balances()
                symbols = [
                    b["asset"] + "USDT"
                    for b in _bals
                    if not b["is_stable"] and b["usd_value"] > 10
                ]
                valid = []
                for sym in symbols[:6]:  # Max 6 coins
                    try:
                        market.get_price(sym)
                        valid.append(sym)
                    except Exception:
                        pass
                symbols = valid if valid else ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
            except Exception:
                symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        console.print(f"\n[dim]📐 Getting DCA recommendations for {', '.join(symbols)}...[/dim]")
        dca.print_recommendations(symbols)

    elif parts[0] == "market":
        symbol = parts[1].upper() if len(parts) > 1 else "BTCUSDT"
        ctx = market.get_market_context(symbol)
        fg = ctx["fear_greed"]
        console.print(Panel(
            f"{t('market.price')}: [bold]${ctx['price']:,.4f}[/bold]\n"
            f"{t('market.rsi')}: [bold]{ctx['rsi']}[/bold] ({ctx['rsi_zone_label']})\n"
            f"{t('market.trend')}: {ctx['trend']}\n"
            f"{t('market.sma50')}: ${ctx['sma_50']:,.2f}\n"
            f"{t('market.sma200')}: ${ctx['sma_200']:,.2f}\n"
            f"{t('market.vs_sma200')}: {ctx['vs_sma200_pct']:+.1f}%\n"
            f"{t('market.fear_greed')}: {fg['value']} ({fg['classification']})",
            title=t("market.title", symbol=symbol), border_style="blue"
        ))

    elif parts[0] == "fg":
        fg = market.get_fear_greed()
        val = fg["value"]
        advice = (
            t("cli.fg_accumulate") if val < 30 else
            t("cli.fg_careful") if val > 75 else
            t("cli.fg_neutral")
        )
        console.print(Panel(
            f"{t('cli.fg_score')}: [bold]{val}/100[/bold]\n"
            f"{t('cli.fg_status')}: [bold]{fg['classification']}[/bold]\n\n"
            f"[italic]{advice}[/italic]",
            title=t("cli.fg_title"), border_style="yellow"
        ))

    elif parts[0] == "behavior":
        # FIX 1: Sync trades from portfolio before analysis
        try:
            _bals = portfolio.get_balances()
            _syms = [b["asset"] + "USDT" for b in _bals if not b["is_stable"] and b["usd_value"] > 5]
        except Exception:
            _syms = []
        behavior.print_behavior_report(symbols=_syms)

    elif parts[0] == "alert":
        if len(parts) < 4:
            console.print("[yellow]Usage: alert SYMBOL above/below/rsi_above/rsi_below VALUE[/yellow]")
        else:
            sym, cond, val_ = parts[1].upper(), parts[2].lower(), float(parts[3])
            notes = " ".join(parts[4:]) if len(parts) > 4 else ""
            alert_mgr.add_alert(sym, cond, val_, notes)
            console.print(f"[green]{t('alert.set', symbol=sym, condition=cond, threshold=val_)}[/green]")

    elif parts[0] == "alerts":
        alert_mgr.list_alerts()

    elif parts[0] in ("check-alerts", "checkalerts"):
        fired = alert_mgr.check_alerts()
        if not fired:
            console.print(f"[green]{t('alert.none_triggered')}[/green]")
        for f in fired:
            console.print(Panel(f.get("context", ""), title=t("alert.triggered_title", symbol=f["symbol"])))

    elif parts[0] == "learn":
        topic = parts[1].lower() if len(parts) > 1 else ""
        if not topic:
            edu.list_lessons()
        else:
            edu.explain(topic)

    elif parts[0] == "project":
        # FIX 7: Show 3 scenarios (bear/base/bull) with per-asset growth rates
        symbol = parts[1].upper() if len(parts) > 1 else "BTCUSDT"
        proj = dca.project_accumulation(symbol, months=12)
        sc = proj.get("scenarios", {})
        bear = sc.get("bear", {})
        base = sc.get("base", {})
        bull = sc.get("bull", {})
        console.print(Panel(
            f"[dim]Asset growth assumption: {proj['monthly_growth_assumed']}%/month[/dim]\n\n"
            f"[red]🐻 Bear  ({bear.get('monthly_growth_pct', 0)}%/mo):[/red]  invest ${bear.get('total_invested', 0):,.0f} → ${bear.get('projected_value', 0):,.0f}  ({bear.get('roi_pct', 0):+.1f}%)\n"
            f"[yellow]📊 Base  ({base.get('monthly_growth_pct', 0)}%/mo):[/yellow] invest ${base.get('total_invested', 0):,.0f} → ${base.get('projected_value', 0):,.0f}  ({base.get('roi_pct', 0):+.1f}%)\n"
            f"[green]🐂 Bull  ({bull.get('monthly_growth_pct', 0)}%/mo):[/green]  invest ${bull.get('total_invested', 0):,.0f} → ${bull.get('projected_value', 0):,.0f}  ({bull.get('roi_pct', 0):+.1f}%)\n\n"
            f"[dim]{proj['note']}[/dim]",
            title=f"📅 {symbol} — 12-Month DCA Projection", border_style="green"
        ))

    elif parts[0] in ("coach", "weekly", "ask", "models", "model") and ai:
        if parts[0] == "models":
            ai.print_models_table()
        elif parts[0] == "model":
            if len(parts) > 1:
                ai.set_model(parts[1])
                console.print(f"[green]✅ Model set to: {ai.model}[/green]")
        elif parts[0] == "coach":
            console.print("[dim]🤖 Calling Claude...[/dim]")
            balances = portfolio.get_balances()
            health = portfolio.calculate_health_score(balances)
            ctx = market.get_market_context("BTCUSDT")
            fomo = behavior.calculate_fomo_score()
            over = behavior.calculate_overtrading_index()
            beh_data = {"fomo_score": fomo["score"], "fomo_label": fomo["label"],
                        "overtrade_label": over["label"], "panic_list": []}
            result = ai.coaching_summary(health, ctx, beh_data)
            ai.print_response("🤖 Coaching Summary", result)
        elif parts[0] == "weekly":
            console.print("[dim]🤖 Calling Claude...[/dim]")
            balances = portfolio.get_balances()
            health = portfolio.calculate_health_score(balances)
            ctx = market.get_market_context("BTCUSDT")
            fomo = behavior.calculate_fomo_score()
            over = behavior.calculate_overtrading_index()
            beh_data = {"fomo_score": fomo["score"], "fomo_label": fomo["label"],
                        "overtrade_label": over["label"], "panic_list": []}
            market_summary = {"trend": ctx["trend"], "fg_value": ctx["fear_greed"]["value"],
                              "fg_label": ctx["fear_greed"]["classification"]}
            dca_recs = [dca.get_recommendation(s) for s in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]]
            result = ai.weekly_brief(health, beh_data, market_summary, dca_recs)
            ai.print_response("📋 Weekly Brief", result)
        elif parts[0] == "ask":
            question = " ".join(parts[1:])
            console.print("[dim]🤖 Calling Claude...[/dim]")
            balances = portfolio.get_balances() if client else []
            health = portfolio.calculate_health_score(balances) if balances else {}
            total = health.get("total_usd") or 1
            for b in balances:
                b["pct"] = b["usd_value"] / total * 100
            fomo = behavior.calculate_fomo_score()
            over = behavior.calculate_overtrading_index()
            fg = market.get_fear_greed()
            mentioned = {w.upper() for w in _re.findall(r"\b[A-Za-z]{2,10}\b", question)
                         if w.upper() in {"BTC","ETH","BNB","ADA","DOGE","SHIB","FLOKI","ANKR",
                                           "SOL","XRP","DOT","MATIC","AVAX","LINK","UNI","SCR"}} | {"BTC"}
            coin_data = {}
            for sym in mentioned:
                try:
                    coin_data[sym] = market.get_market_context(sym + "USDT")
                except Exception:
                    pass
            ctx_dict = {
                "total_usd": health.get("total_usd", 0), "score": health.get("score"),
                "grade": health.get("grade"), "stable_pct": health.get("stable_pct", 0),
                "suggestions": health.get("suggestions", []), "holdings": balances[:10],
                "fg_value": fg["value"], "fg_label": fg["classification"],
                "fomo_score": fomo.get("score", 0), "overtrade_label": over.get("label", "?"),
                "panic_count": 0, "coin_data": coin_data,
            }
            result = ai.chat(question, ctx_dict)
            ai.print_response("💬 Claude Answer", result, "green")
    elif parts[0] in ("coach", "weekly", "ask") and not ai:
        console.print("[yellow]⚠️  No Anthropic API key configured. Add ANTHROPIC_API_KEY to .env[/yellow]")

    elif parts[0] == "lang":
        if len(parts) > 1 and parts[1].lower() in AVAILABLE_LANGS:
            set_lang(parts[1].lower())
            console.print(f"[green]{t('cli.lang_switched')}[/green]")
        else:
            lang_list = "\n".join(
                f"  {'→' if code == get_lang() else ' '} [cyan]{code}[/cyan]  {label}"
                for code, label in AVAILABLE_LANGS.items()
            )
            console.print(t("cli.lang_list", langs=lang_list))

    # ── Decision Journal ────────────────────────────────────────────────────
    elif parts[0] == "journal":
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        coin_filter = parts[1] if len(parts) > 1 else None
        j.print_journal(coin=coin_filter)

    elif parts[0] == "journal-add":
        # Usage: journal-add COIN BUY/SELL PRICE [AMOUNT_USD] [notes...]
        if len(parts) < 4:
            console.print("[red]Usage: journal-add COIN BUY/SELL PRICE [AMOUNT_USD] [notes...][/red]")
            console.print("[dim]Example: journal-add ADA buy 0.262 100 \"oversold -49% SMA200\"[/dim]")
        else:
            from modules.journal import DecisionJournal
            j = DecisionJournal(market=market)
            coin_arg   = parts[1]
            action_arg = parts[2]
            try:
                price_arg = float(parts[3])
            except ValueError:
                console.print(f"[red]Invalid price: {parts[3]}[/red]")
                return
            # Fix: use `is not None` check — float(0) is falsy, would wrongly shift notes_start
            amount_arg = float(parts[4]) if len(parts) > 4 and _is_num(parts[4]) else None
            notes_start = 5 if amount_arg is not None else 4
            notes_arg   = " ".join(parts[notes_start:]) if len(parts) > notes_start else ""
            try:
                j.add_entry(coin_arg, action_arg, price_arg, amount_arg, notes_arg)
            except ValueError as e:
                console.print(f"[red]❌ {e}[/red]")

    elif parts[0] == "journal-delete":
        # journal-delete <id>
        if len(parts) < 2 or not parts[1].isdigit():
            console.print("[red]Usage: journal-delete <id>[/red]")
            console.print("[dim]Find the id with: journal[/dim]")
        else:
            from modules.journal import DecisionJournal
            j = DecisionJournal(market=market)
            j.delete_entry(int(parts[1]))

    elif parts[0] == "journal-perf":
        from modules.journal import DecisionJournal
        j = DecisionJournal(market=market)
        j.print_performance()

    # ── Snapshot ────────────────────────────────────────────────────────────
    elif parts[0] == "snapshot":
        try:
            balances = portfolio.get_balances()
            health   = portfolio.calculate_health_score(balances)
            from modules.coach_db import CoachDB
            from datetime import datetime
            db    = CoachDB()
            today = datetime.now().strftime("%Y-%m-%d")
            if db.has_snapshot_for(today):
                console.print(f"[yellow]📸 Snapshot already saved for today ({today}).[/yellow]")
            else:
                portfolio.save_snapshot(balances, health)
                console.print(f"[green]📸 Portfolio snapshot saved for {today} — ${health['total_usd']:,.2f}[/green]")
        except Exception as e:
            console.print(f"[red]Snapshot failed: {e}[/red]")

    # ── History ─────────────────────────────────────────────────────────────
    elif parts[0] == "history":
        from modules.history import HistoryAnalyzer
        from modules.coach_db import CoachDB
        days_arg = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 7
        ha = HistoryAnalyzer(CoachDB(), market)
        if days_arg == 1 or (len(parts) > 1 and parts[1] in ["yesterday", "vs"]):
            ha.print_today_vs_yesterday()
        else:
            ha.print_today_vs_yesterday()
            console.print()
            ha.print_history(days=days_arg)

    # ── DCA History ──────────────────────────────────────────────────────────
    elif parts[0] == "dca-history":
        from modules.coach_db import CoachDB
        from rich.table import Table as RTable
        symbol_filter = parts[1].upper() if len(parts) > 1 else None
        db   = CoachDB()
        rows = db.get_dca_history(symbol=symbol_filter, limit=20)
        if not rows:
            console.print("[yellow]No DCA analysis history yet. Run 'bc.sh dca' first.[/yellow]")
        else:
            t2 = RTable(title="📐 DCA Analysis History", border_style="magenta")
            t2.add_column("Date",       width=12)
            t2.add_column("Symbol",     width=10)
            t2.add_column("Price",      justify="right", width=12)
            t2.add_column("RSI",        justify="right", width=7)
            t2.add_column("F&G",        justify="right", width=6)
            t2.add_column("Multiplier", justify="right", width=10)
            t2.add_column("Weekly $",   justify="right", width=10)
            for r in rows:
                mc = "green" if r["multiplier"] >= 1.1 else ("red" if r["multiplier"] < 0.9 else "white")
                t2.add_row(
                    r["date"], r["symbol"],
                    f"${r['price']:,.4f}" if r["price"] else "—",
                    f"{r['rsi']:.1f}" if r["rsi"] else "—",
                    str(r["fg_score"]) if r["fg_score"] else "—",
                    f"[{mc}]×{r['multiplier']:.2f}[/{mc}]",
                    f"${r['weekly_amount']:,.2f}" if r["weekly_amount"] else "—",
                )
            console.print(t2)

    # ── Confirm DCA action ───────────────────────────────────────────────────
    elif parts[0] == "confirm":
        # confirm <analysis_id> yes|no [amount] [notes...]
        from modules.coach_db import CoachDB
        if len(parts) < 3:
            console.print("[red]Usage: confirm <id> yes|no [amount] [notes][/red]")
        else:
            try:
                analysis_id  = int(parts[1])
                decision     = parts[2].lower()
                amount       = float(parts[3]) if len(parts) > 3 and parts[3].replace(".","").isdigit() else None
                notes        = " ".join(parts[4:]) if len(parts) > 4 else ""
                action_type  = "dca_confirmed" if decision in ["yes","y","ja"] else "dca_skipped"
                db = CoachDB()
                # Look up symbol from analysis
                hist = db.get_dca_history(limit=100)
                rec  = next((r for r in hist if r["id"] == analysis_id), None)
                symbol = rec["symbol"] if rec else "UNKNOWN"
                db.save_user_action(analysis_id, symbol, action_type, amount, notes)
                emoji = "✅" if action_type == "dca_confirmed" else "⏭️"
                console.print(f"{emoji} Logged: {action_type} for analysis #{analysis_id} ({symbol})"
                               + (f" — ${amount:,.2f}" if amount else ""))
            except Exception as e:
                console.print(f"[red]Confirm failed: {e}[/red]")

    # ── Import orders from Binance ───────────────────────────────────────────
    elif parts[0] == "import-orders":
        from modules.coach_db import CoachDB
        from datetime import datetime
        db = CoachDB()
        existing = db.get_order_count()
        console.print(f"\n[bold]📥 Binance Order History Import[/bold]")
        console.print(f"[dim]Orders already in DB: {existing}[/dim]\n")
        console.print("This will fetch your filled order history from Binance and store it")
        console.print("locally in coach.db. Your data never leaves your machine.\n")
        console.print("[yellow]Do you want to import your Binance order history? (yes/no)[/yellow] ", end="")
        try:
            import sys
            if sys.stdin.isatty():
                answer = input("").strip().lower()
            else:
                # Non-interactive mode (--command flag) — require explicit opt-in via env var
                answer = os.getenv("BC_IMPORT_ORDERS_CONFIRM", "no").strip().lower()
                if answer != "yes":
                    console.print("\n[dim]Non-interactive mode: set BC_IMPORT_ORDERS_CONFIRM=yes to auto-confirm.[/dim]")
        except Exception as e:
            logger.debug("import-orders: could not read stdin — %s", e)
            answer = "no"
        if answer not in ["yes", "y", "ja"]:
            console.print("[dim]Import cancelled.[/dim]")
        else:
            all_assets = ["BTC","ETH","ADA","DOGE","SHIB","ANKR","FLOKI","BNB","SCR",
                          "MONKY","TRUMP","NIGHT","OPN","SOL","XRP","AVAX","DOT","LINK","MATIC"]
            imported = 0
            skipped  = 0
            for asset in all_assets:
                for quote in ["USDT","USDC"]:
                    try:
                        orders = client.get_orders(symbol=asset+quote, limit=500)
                        filled = [o for o in (orders or []) if o["status"] == "FILLED"]
                        for o in filled:
                            price    = float(o["price"]) if float(o["price"]) > 0 else (
                                float(o.get("cummulativeQuoteQty",0)) / float(o["executedQty"])
                                if float(o["executedQty"]) > 0 else 0
                            )
                            spent    = float(o.get("cummulativeQuoteQty", 0))
                            ts       = o["time"]
                            date_str = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d")
                            db.save_order(
                                symbol   = asset + quote,
                                side     = o["side"],
                                price    = price,
                                qty      = float(o["executedQty"]),
                                spent_quote = spent,
                                date     = date_str,
                                timestamp= ts,
                                source   = "binance_api",
                                order_id = str(o["orderId"]),
                            )
                            imported += 1
                    except Exception:
                        skipped += 1
            console.print(f"[green]✅ Imported {imported} orders into coach.db[/green]")
            if skipped:
                console.print(f"[dim]{skipped} symbols skipped (no history or error)[/dim]")

    # ── P&L Calculator ──────────────────────────────────────────────────────
    elif parts[0] == "pnl":
        from modules.pnl import PnLCalculator
        from modules.journal import DecisionJournal
        j   = DecisionJournal(market=market)
        pnl = PnLCalculator(client, market, portfolio, journal=j)
        symbol_arg = parts[1].upper() if len(parts) > 1 else None
        pnl.print_pnl(symbol=symbol_arg)

    elif parts[0] == "pnl-export":
        from modules.pnl import PnLCalculator
        from modules.journal import DecisionJournal
        j   = DecisionJournal(market=market)
        pnl = PnLCalculator(client, market, portfolio, journal=j)
        pnl.export_csv()

    # ── Rebalancing ─────────────────────────────────────────────────────────
    elif parts[0] == "rebalance":
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio)
        rb.print_rebalance()

    elif parts[0] == "targets":
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio)
        rb.print_targets()

    elif parts[0] == "targets-set":
        # targets-set BTC 40 ETH 30 BNB 20 ADA 10
        from modules.rebalance import RebalanceAdvisor
        rb = RebalanceAdvisor(portfolio)
        alloc_parts = parts[1:]
        allocations = {}
        i = 0
        while i < len(alloc_parts) - 1:
            try:
                coin_k = alloc_parts[i].upper()
                pct_v  = float(alloc_parts[i + 1])
                allocations[coin_k] = pct_v
                i += 2
            except (ValueError, IndexError):
                i += 1
        if allocations:
            rb.set_targets(allocations)
        else:
            console.print("[red]Usage: targets-set BTC 40 ETH 30 BNB 20 ADA 10[/red]")

    # ── Yield Optimizer ─────────────────────────────────────────────────────
    elif parts[0] == "yield":
        from modules.yield_optimizer import YieldOptimizer
        yo = YieldOptimizer(client, portfolio)
        yo.print_yield()

    elif parts[0] == "news":
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_latest_news(limit=limit)
        news_mod.print_news(articles)

    elif parts[0] == "listings":
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_new_listings(limit=limit)
        news_mod.print_listings(articles)

    elif parts[0] == "launchpool":
        from modules.news import BinanceNews
        news_mod = BinanceNews()
        articles = news_mod.get_launchpool(limit=5)
        news_mod.print_launchpool(articles)

    elif parts[0] == "watch":
        interval = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 60
        from modules.news import run_watcher, watcher_status
        status = watcher_status()
        if status["running"]:
            console.print(f"[yellow]⚠️  Watcher already running (PID {status['pid']}). Run 'watch-stop' first.[/yellow]")
        else:
            try:
                _bals = portfolio.get_balances()
                _portfolio_arg = portfolio
            except Exception:
                _portfolio_arg = None
            run_watcher(interval=interval, portfolio=_portfolio_arg)

    elif parts[0] == "watch-stop":
        from modules.news import stop_watcher
        stopped = stop_watcher()
        if stopped:
            console.print("[green]✅ Watcher stopped.[/green]")
        else:
            console.print("[yellow]No watcher running.[/yellow]")

    elif parts[0] == "watch-status":
        from modules.news import watcher_status
        status = watcher_status()
        if status["running"]:
            console.print(f"[green]✅ Watcher running (PID {status['pid']})[/green]")
        else:
            console.print("[yellow]Watcher not running.[/yellow]")

    elif parts[0] == "news-check":
        from modules.news import BinanceNews
        try:
            _portfolio_for_news = portfolio
        except Exception:
            _portfolio_for_news = None
        news_mod = BinanceNews(portfolio=_portfolio_for_news)
        result = news_mod.check_and_format_new()
        if result["has_new"]:
            if result["listings"]:
                news_mod.print_listings(result["listings"])
            if result["launchpool"]:
                news_mod.print_launchpool(result["launchpool"])
            if result["news"]:
                news_mod.print_news(result["news"])
            if result["portfolio_hits"]:
                console.print("\n[bold yellow]⚡ Portfolio-relevant news:[/bold yellow]")
                for hit in result["portfolio_hits"]:
                    console.print(f"  • [{hit.get('matched_asset', '')}] {hit['title']}")
        else:
            console.print("[green]✅ No new announcements since last check.[/green]")

    elif parts[0] == "help":
        console.print(t("cli.help"))

    else:
        console.print(f"[yellow]{t('general.unknown_cmd', cmd=parts[0])}[/yellow]")

    return True


def main():
    parser = argparse.ArgumentParser(description="BinanceCoach — AI Trading Behavior Coach")
    parser.add_argument("--telegram", action="store_true", help="Run as Telegram bot")
    parser.add_argument("--demo", action="store_true", help="Demo mode (no API keys)")
    parser.add_argument("--lang", choices=["en", "nl"], default=None, help="Language (en/nl)")
    parser.add_argument("--command", "-c", type=str, default=None,
                        help="Run a single command non-interactively (for skill/scripting use)")
    args = parser.parse_args()

    if args.lang:
        set_lang(args.lang)

    if args.demo:
        run_demo()
    elif args.telegram:
        run_telegram()
    elif args.command:
        run_command(args.command)
    else:
        run_cli()


if __name__ == "__main__":
    main()
