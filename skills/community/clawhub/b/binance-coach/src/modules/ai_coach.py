"""
ai_coach.py — Real AI coaching engine using Claude (Anthropic)

Features:
- Portfolio coaching summary (personalized advice in natural language)
- AI-powered alert explanations (dynamic context, not canned text)
- Weekly coaching brief (behavioral patterns + action plan)
- Free-form Q&A about your portfolio/market
- Dynamic model selection via Anthropic API

Model is configurable via .env AI_MODEL or at runtime with 'model' command.
Default: claude-haiku-4-5-20251001 (fast + cost-efficient for frequent use)
"""

import os
import logging
import anthropic
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from modules.i18n import t, get_lang

logger = logging.getLogger(__name__)

console = Console()

# Known models with descriptions (fallback if API listing fails)
KNOWN_MODELS = [
    {
        "id": "claude-haiku-4-5-20251001",
        "name": "Claude Haiku 4.5",
        "desc": "Fast & cheap — best for frequent coaching calls",
        "recommended_for": "daily use ⭐ default",
    },
    {
        "id": "claude-sonnet-4-5-20250929",
        "name": "Claude Sonnet 4.5",
        "desc": "Balanced — deeper insights, moderate cost",
        "recommended_for": "weekly briefs, detailed analysis",
    },
    {
        "id": "claude-sonnet-4-6",
        "name": "Claude Sonnet 4.6",
        "desc": "Latest Sonnet — best balance of speed and quality",
        "recommended_for": "general AI coaching",
    },
    {
        "id": "claude-sonnet-4-20250514",
        "name": "Claude Sonnet 4",
        "desc": "Sonnet 4 stable release",
        "recommended_for": "reliable coaching summaries",
    },
    {
        "id": "claude-opus-4-5-20251101",
        "name": "Claude Opus 4.5",
        "desc": "Very powerful — deep reasoning, higher cost",
        "recommended_for": "complex portfolio reviews",
    },
    {
        "id": "claude-opus-4-6",
        "name": "Claude Opus 4.6",
        "desc": "Most powerful — best reasoning, highest cost",
        "recommended_for": "deep strategy analysis",
    },
    {
        "id": "claude-opus-4-20250514",
        "name": "Claude Opus 4",
        "desc": "Opus 4 stable — extremely capable",
        "recommended_for": "complex analysis",
    },
    {
        "id": "claude-opus-4-1-20250805",
        "name": "Claude Opus 4.1",
        "desc": "Opus with enhanced reasoning",
        "recommended_for": "multi-step strategy",
    },
    {
        "id": "claude-3-haiku-20240307",
        "name": "Claude Haiku 3 (legacy)",
        "desc": "Older Haiku — very fast, lower capability",
        "recommended_for": "simple Q&A",
    },
]


class AICoach:
    """Claude-powered trading behavior coach."""

    def __init__(self, model: str = None):
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key or api_key == "your_anthropic_key_here":
            raise ValueError("ANTHROPIC_API_KEY not set. Add it to your .env file.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model or os.getenv("AI_MODEL", "claude-haiku-4-5-20251001")

    def _lang_instruction(self) -> str:
        lang = get_lang()
        if lang == "nl":
            return "Respond entirely in Dutch (Nederlands). Use informal 'je/jij' tone."
        return "Respond in English."

    def list_models(self) -> list[dict]:
        """Fetch available models from Anthropic API, fall back to known list."""
        try:
            models = self.client.models.list()
            result = []
            for m in models.data:
                known = next((k for k in KNOWN_MODELS if k["id"] == m.id), None)
                result.append({
                    "id": m.id,
                    "name": known["name"] if known else m.id,
                    "desc": known["desc"] if known else "—",
                    "recommended_for": known["recommended_for"] if known else "—",
                    "created": getattr(m, "created_at", None),
                })
            # Sort: newest first
            result.sort(key=lambda x: x.get("created") or "", reverse=True)
            return result
        except Exception as exc:
            logger.debug("Could not fetch models from API: %s", exc)
            return KNOWN_MODELS

    def set_model(self, model_id: str):
        """Switch the active model."""
        self.model = model_id
        # Persist to env at runtime
        os.environ["AI_MODEL"] = model_id

    def _call(self, system: str, user: str, max_tokens: int = 1024) -> str:
        """Core API call with error handling."""
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text

    # ── Coaching Summary ──────────────────────────────────────────────────

    def coaching_summary(self, portfolio: dict, market_ctx: dict, behavior: dict) -> str:
        """
        Generate a personalized AI coaching summary based on portfolio,
        current market conditions, and behavioral analysis.
        """
        lang_note = self._lang_instruction()
        system = f"""You are BinanceCoach, an expert crypto trading behavior coach.
Your job is to give concise, honest, actionable advice to retail crypto traders.
You understand behavioral finance, technical analysis, and risk management.
Be direct, not preachy. Use data to back your points. {lang_note}
Format your response with clear sections using markdown headers."""

        user = f"""Please provide a personalized coaching summary based on this data:

## Portfolio
- Total value: ${portfolio['total_usd']:,.2f}
- Health score: {portfolio['score']}/100 (Grade {portfolio['grade']})
- Holdings: {portfolio['n_assets']} meaningful positions
- Stablecoin reserve: {portfolio['stable_pct']}%
- Current issues: {', '.join(portfolio['suggestions']) if portfolio['suggestions'] else 'none'}

## Market Conditions (BTC as benchmark)
- BTC price: ${market_ctx['price']:,.2f}
- RSI: {market_ctx['rsi']} ({market_ctx['rsi_zone']})
- Trend: {market_ctx['trend']}
- vs 200-day SMA: {market_ctx['vs_sma200_pct']:+.1f}%
- Fear & Greed: {market_ctx['fear_greed']['value']} ({market_ctx['fear_greed']['classification']})

## Behavioral Analysis
- FOMO score: {behavior.get('fomo_score', 0)}/100 ({behavior.get('fomo_label', 'N/A')})
- Trades last 30d: {behavior.get('total_trades', 0)} ({behavior.get('per_week', 0)}/week)
- Overtrading label: {behavior.get('overtrade_label', 'N/A')}
- Recent panic sells detected: {behavior.get('panic_count', 0)}

Give a 3-section coaching summary:
1. **What you're doing well** (if anything)
2. **Main risks right now** (be specific and data-driven)
3. **3 concrete actions to take this week**

Keep it under 300 words. Be honest, even if it's uncomfortable."""

        return self._call(system, user, max_tokens=600)

    # ── Alert Explanation ─────────────────────────────────────────────────

    def explain_alert(self, symbol: str, condition: str, threshold: float,
                      trigger_value: float, market_ctx: dict) -> str:
        """
        Generate an AI-powered, dynamic alert explanation.
        Much richer than the rule-based version.
        """
        lang_note = self._lang_instruction()
        system = f"""You are BinanceCoach. A price/RSI alert just triggered for a user.
Explain concisely what this means, why it matters, and what action (if any) to consider.
Be specific, data-driven. 2-3 short paragraphs max. {lang_note}"""

        user = f"""Alert triggered: {symbol} {condition} {threshold}
Actual value at trigger: {trigger_value}

Current market data:
- Price: ${market_ctx['price']:,.4f}
- RSI: {market_ctx['rsi']} ({market_ctx['rsi_zone']})
- Trend: {market_ctx['trend']}
- vs 200-day SMA: {market_ctx['vs_sma200_pct']:+.1f}%
- Fear & Greed: {market_ctx['fear_greed']['value']} ({market_ctx['fear_greed']['classification']})
- Above SMA50: {market_ctx['above_sma50']}
- Above SMA200: {market_ctx['above_sma200']}

Explain what this alert means in context. What should the user consider doing (or not doing)?
Keep it brief and actionable."""

        return self._call(system, user, max_tokens=400)

    # ── Weekly Coaching Brief ─────────────────────────────────────────────

    def weekly_brief(self, portfolio: dict, behavior: dict,
                     market_summary: dict, dca_recs: list[dict]) -> str:
        """
        Generate a weekly coaching brief: what happened, patterns, action plan.
        """
        lang_note = self._lang_instruction()
        system = f"""You are BinanceCoach writing a weekly coaching brief for a crypto trader.
Be concise, direct, and data-driven. Tone: like a good financial coach — honest but not harsh.
{lang_note}"""

        dca_lines = "\n".join(
            f"- {r['symbol']}: ×{r['multiplier']} → ${r['suggested_weekly_usd']:.2f}/week"
            for r in dca_recs[:3]
        )

        user = f"""Weekly Coaching Brief — {datetime.now().strftime('%d %b %Y')}

Portfolio: ${portfolio['total_usd']:,.2f} | Score {portfolio['score']}/100 ({portfolio['grade']})

Behavior this week:
- FOMO score: {behavior.get('fomo_score', 0)}/100
- Trades: {behavior.get('total_trades', 0)} ({behavior.get('per_week', 0)}/week)
- Panic sells: {behavior.get('panic_count', 0)}
- Overtrade label: {behavior.get('overtrade_label', 'N/A')}

Market: BTC {market_summary.get('trend','?')} | F&G {market_summary.get('fg_value','?')} ({market_summary.get('fg_label','?')})

DCA Recommendations:
{dca_lines}

Write a weekly brief with:
1. **This Week's Summary** (2-3 sentences, what the data shows)
2. **Behavioral Pattern Alert** (anything concerning in their trading behavior?)
3. **Market Outlook** (brief, based on indicators — no price predictions)
4. **Action Plan** (3 bullet points for next week)

Max 350 words."""

        return self._call(system, user, max_tokens=700)

    # ── Free-form Chat ────────────────────────────────────────────────────

    def chat(self, question: str, context: dict = None) -> str:
        """
        Answer a free-form question about the user's portfolio or market.

        context dict (all optional, but more = better answers):
          total_usd, score, grade, stable_pct, suggestions  — portfolio health
          holdings        — list of {asset, usd_value, pct, display}
          fg_value, fg_label                                 — Fear & Greed
          fomo_score, overtrade_label, panic_count           — behavior
          coin_data       — dict of {SYMBOL: market_context} for mentioned coins
        """
        lang_note = self._lang_instruction()
        system = f"""You are BinanceCoach, an AI crypto trading coach with expertise in:
- Behavioral finance and emotional trading patterns
- Technical analysis (RSI, moving averages, support/resistance)
- Portfolio management and risk assessment
- Dollar cost averaging strategies
- Crypto market dynamics

You have access to the user's LIVE portfolio data below. Use it to give specific,
personalized advice. Never ask for data you already have.
Answer questions concisely and practically. {lang_note}
If you don't know something specific, say so. Never invent price data."""

        ctx = context or {}
        blocks = []

        # ── Portfolio block ───────────────────────────────────────────────
        if ctx.get("total_usd"):
            blocks.append(f"""## Your Portfolio (live data)
- Total value: ${ctx['total_usd']:,.2f}
- Health score: {ctx.get('score', '?')}/100 (Grade {ctx.get('grade', '?')})
- Stablecoin reserve: {ctx.get('stable_pct', 0)}%""")
            if ctx.get("suggestions"):
                blocks[-1] += "\n- Issues: " + "; ".join(ctx["suggestions"][:3])

        # ── Holdings block ────────────────────────────────────────────────
        if ctx.get("holdings"):
            holdings_lines = []
            for h in ctx["holdings"][:10]:
                label = h.get("display", h.get("asset", "?"))
                pct   = h.get("pct", 0)
                usd   = h.get("usd_value", 0)
                holdings_lines.append(f"  - {label}: ${usd:,.2f} ({pct:.1f}%)")
            blocks.append("## Holdings\n" + "\n".join(holdings_lines))

        # ── Market sentiment block ────────────────────────────────────────
        if ctx.get("fg_value") is not None:
            blocks.append(f"""## Market Sentiment
- Fear & Greed: {ctx['fg_value']} ({ctx.get('fg_label', '?')})""")

        # ── Behavior block ────────────────────────────────────────────────
        if ctx.get("fomo_score") is not None:
            blocks.append(f"""## Your Trading Behavior
- FOMO score: {ctx['fomo_score']}/100
- Overtrading: {ctx.get('overtrade_label', '?')}
- Recent panic sells: {ctx.get('panic_count', 0)}""")

        # ── Coin-specific blocks ──────────────────────────────────────────
        for sym, mkt in (ctx.get("coin_data") or {}).items():
            try:
                fg_val = mkt["fear_greed"]["value"]
                fg_lbl = mkt["fear_greed"]["classification"]
                blocks.append(f"""## {sym} (live market data)
- Price: ${mkt['price']:,.4f}
- RSI: {mkt['rsi']} ({mkt.get('rsi_zone_label', mkt.get('rsi_zone', '?'))})
- Trend: {mkt.get('trend', '?')}
- vs 200-day SMA: {mkt.get('vs_sma200_pct', 0):+.1f}%
- Fear & Greed: {fg_val} ({fg_lbl})""")
            except Exception:
                pass

        context_block = "\n\n".join(blocks)
        if context_block:
            context_block += "\n\n---\n\n"

        user = f"{context_block}Question: {question}"
        return self._call(system, user, max_tokens=600)

    # ── Display helpers ───────────────────────────────────────────────────

    def print_response(self, title: str, content: str, color: str = "cyan"):
        """Pretty-print an AI response in a Rich panel."""
        console.print(Panel(
            Markdown(content),
            title=f"[bold {color}]🤖 {title} — {self.model}[/bold {color}]",
            border_style=color,
            padding=(1, 2),
        ))

    def print_models_table(self, models: list[dict]):
        """Display available models in a Rich table."""
        from rich.table import Table
        table = Table(title=f"🤖 Available Claude Models (active: [green]{self.model}[/green])")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Best for", style="yellow")

        for m in models:
            style = "bold green" if m["id"] == self.model else ""
            marker = " ✓" if m["id"] == self.model else ""
            table.add_row(
                f"[{style}]{m['id']}{marker}[/{style}]" if style else m["id"] + marker,
                m["name"],
                m["desc"],
                m["recommended_for"],
            )
        console.print(table)
        console.print(f"\n[dim]Change with: [cyan]model <id>[/cyan] — e.g. model claude-sonnet-4-5[/dim]")
