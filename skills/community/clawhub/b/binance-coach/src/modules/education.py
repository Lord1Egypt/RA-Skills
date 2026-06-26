"""
education.py — Contextual education module
Explains concepts in plain language based on what's happening in the user's portfolio
All content lives in i18n.py (LESSONS dict) for full EN/NL support.
"""

from rich.console import Console
from rich.panel import Panel
from modules.i18n import t, tlesson, LESSONS

console = Console()


class EducationModule:
    """Serves contextual education based on portfolio/market conditions."""

    def explain(self, topic: str):
        """Print an educational panel on a topic (current language)."""
        lesson = tlesson(topic)
        if not lesson:
            console.print(f"[red]{t('edu.not_found', topic=topic)}[/red]")
            return
        console.print(Panel(
            lesson["content"],
            title=f"[bold cyan]📚 {lesson['title']}[/bold cyan]",
            border_style="cyan"
        ))

    def get_lesson_text(self, topic: str) -> str | None:
        """Return lesson as plain string (for Telegram bot)."""
        lesson = tlesson(topic)
        if not lesson:
            return None
        return f"*📚 {lesson['title']}*\n\n{lesson['content']}"

    def get_contextual_tips(self, market_ctx: dict, health: dict = None) -> list[tuple]:
        """Return relevant (topic, reason) tuples based on current market conditions."""
        tips = []
        rsi = market_ctx.get("rsi", 50)
        fg = market_ctx.get("fear_greed", {}).get("value", 50)

        if rsi < 30:
            tips.append(("rsi_oversold", f"RSI is {rsi:.1f}"))
        elif rsi > 70:
            tips.append(("rsi_overbought", f"RSI is {rsi:.1f}"))

        if fg < 25:
            tips.append(("fear_greed", f"F&G = {fg} (Extreme Fear)"))
        elif fg > 75:
            tips.append(("fear_greed", f"F&G = {fg} (Extreme Greed)"))

        if health and health.get("score", 100) < 60:
            tips.append(("concentration_risk", "Portfolio health score is low"))

        return tips

    def list_lessons(self):
        """List available lessons in current language."""
        from rich.table import Table
        table = Table(title=t("edu.table.title"))
        table.add_column(t("edu.table.key"), style="cyan")
        table.add_column(t("edu.table.title_col"), style="white")
        for key in LESSONS:
            lesson = tlesson(key)
            table.add_row(key, lesson["title"] if lesson else key)
        console.print(table)

    def list_lessons_text(self) -> str:
        """Return lessons list as plain string (for Telegram)."""
        lines = [f"*📚 {t('edu.table.title')}:*\n"]
        for key in LESSONS:
            lesson = tlesson(key)
            title = lesson["title"] if lesson else key
            lines.append(f"• `{key}` — {title}")
        return "\n".join(lines)
