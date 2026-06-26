"""
news.py — Binance News, Listings & Launchpool fetcher
Fetches from the public Binance CMS API (no API key required).
Tracks seen articles in data/seen_news.db to avoid duplicate alerts.
"""

import os
import sqlite3
import logging
import requests
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()

# PID file for the watcher daemon
WATCHER_PID_FILE = Path(__file__).parent.parent / "data" / "news_watcher.pid"

CMS_URL = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
HEADERS = {"User-Agent": "Mozilla/5.0 BinanceCoach/1.0"}
DB_PATH = Path(__file__).parent.parent / "data" / "seen_news.db"

LAUNCHPOOL_KEYWORDS = [
    "launchpool", "hodler", "hodl", "airdrop", "simple earn",
    "megadrop", "bnb vault", "earn subscription"
]


class BinanceNews:
    """Fetches and tracks Binance announcements, new listings, and launchpools."""

    def __init__(self, portfolio=None):
        self.portfolio = portfolio
        self._init_db()

    def _init_db(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS seen "
                "(article_id INTEGER PRIMARY KEY, seen_at TEXT)"
            )
            conn.commit()

    def _is_seen(self, article_id: int) -> bool:
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute(
                "SELECT 1 FROM seen WHERE article_id=?", (article_id,)
            ).fetchone() is not None

    def _mark_seen(self, article_id: int):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seen VALUES (?,?)",
                (article_id, datetime.now().isoformat())
            )
            conn.commit()

    def get_articles(self, catalog_id: int, limit: int = 5) -> list:
        """Fetch articles from the Binance CMS API for a given catalog."""
        try:
            r = requests.get(
                CMS_URL,
                params={"type": 1, "pageNo": 1, "pageSize": limit, "catalogId": catalog_id},
                headers=HEADERS,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            raw_articles = data["data"]["catalogs"][0]["articles"]
            result = []
            for a in raw_articles:
                code = a.get("code", "")
                url = f"https://www.binance.com/en/support/announcement/{code}" if code else ""
                ts = a.get("releaseDate", 0)
                date_str = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d") if ts else "?"
                result.append({
                    "id": a["id"],
                    "title": a["title"],
                    "date": date_str,
                    "url": url,
                })
            return result
        except Exception as e:
            logger.error(f"Binance CMS API error (catalog {catalog_id}): {e}")
            return []

    def get_new_listings(self, limit: int = 5) -> list:
        """Get new coin listings (catalog 48)."""
        return self.get_articles(48, limit)

    def get_latest_news(self, limit: int = 5) -> list:
        """Get latest Binance news (catalog 49)."""
        return self.get_articles(49, limit)

    def get_launchpool(self, limit: int = 5) -> list:
        """Get launchpool/HODLer airdrop announcements from catalog 48."""
        articles = self.get_articles(48, limit=20)
        filtered = [
            a for a in articles
            if any(kw in a["title"].lower() for kw in LAUNCHPOOL_KEYWORDS)
        ]
        return filtered[:limit]

    def _portfolio_assets(self) -> set:
        """Return set of held asset symbols (e.g. {'BTC', 'ETH', 'BNB'})."""
        if not self.portfolio:
            return set()
        try:
            balances = self.portfolio.get_balances()
            return {b["asset"].upper() for b in balances if b.get("usd_value", 0) > 1}
        except Exception:
            return set()

    def _coin_relevance(self, title: str):
        """Check if any portfolio asset appears in the article title. Returns asset or None."""
        assets = self._portfolio_assets()
        title_upper = title.upper()
        for asset in assets:
            if asset in title_upper:
                return asset
        return None

    def get_new_unseen(self, catalog_id: int, limit: int = 20) -> list:
        """Return only articles not yet seen, and mark them as seen."""
        articles = self.get_articles(catalog_id, limit)
        new = [a for a in articles if not self._is_seen(a["id"])]
        for a in new:
            self._mark_seen(a["id"])
        return new

    def check_and_format_new(self) -> dict:
        """
        Check for new unseen articles across listings + news.
        Returns dict with has_new, listings, launchpool, news, portfolio_hits.
        """
        new_listings_all = self.get_new_unseen(48, limit=10)
        new_news = self.get_new_unseen(49, limit=10)

        launchpool = [
            a for a in new_listings_all
            if any(kw in a["title"].lower() for kw in LAUNCHPOOL_KEYWORDS)
        ]
        listings = [a for a in new_listings_all if a not in launchpool]

        portfolio_hits = []
        for a in listings + launchpool + new_news:
            match = self._coin_relevance(a["title"])
            if match:
                portfolio_hits.append({**a, "matched_asset": match})

        return {
            "has_new": bool(listings or launchpool or new_news),
            "listings": listings,
            "launchpool": launchpool,
            "news": new_news,
            "portfolio_hits": portfolio_hits,
        }

    # ── Rich CLI output ──────────────────────────────────────────────────────

    def print_news(self, articles: list, title: str = "📰 Latest News"):
        if not articles:
            console.print("[yellow]No news found.[/yellow]")
            return
        table = Table(title=title, border_style="blue", show_lines=False)
        table.add_column("Date", style="dim", width=12, no_wrap=True)
        table.add_column("Title")
        for a in articles:
            table.add_row(a["date"], a["title"])
        console.print(table)

    def print_listings(self, articles: list):
        if not articles:
            console.print("[yellow]No new listings found.[/yellow]")
            return
        self.print_news(articles, "🆕 New Listings")

    def print_launchpool(self, articles: list):
        if not articles:
            console.print("[yellow]No active launchpools or airdrops found.[/yellow]")
            return
        self.print_news(articles, "🌾 Launchpool & HODLer Airdrops")

    # ── Telegram HTML output ─────────────────────────────────────────────────

    def _fmt_articles_html(self, articles: list, title: str) -> str:
        if not articles:
            return f"<b>{title}</b>\nNone found."
        lines = [f"<b>{title}</b>"]
        for a in articles:
            url = a.get("url", "")
            date = a.get("date", "")
            if url:
                lines.append(f'• <a href="{url}">{a["title"]}</a> <i>({date})</i>')
            else:
                lines.append(f'• <b>{a["title"]}</b> <i>({date})</i>')
        return "\n".join(lines)

    def format_news_html(self, articles: list, title: str = "📰 Latest Binance News") -> str:
        return self._fmt_articles_html(articles, title)

    def format_listings_html(self, articles: list) -> str:
        return self._fmt_articles_html(articles, "🆕 New Listings")

    def format_launchpool_html(self, articles: list) -> str:
        return self._fmt_articles_html(articles, "🌾 Launchpool &amp; HODLer Airdrops")


# ── Watcher daemon ───────────────────────────────────────────────────────────

def _is_openclaw_mode() -> bool:
    """Detect if running under OpenClaw (no bot token, but openclaw CLI available)."""
    import shutil
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if token:
        return False  # Has bot token, use direct Telegram API
    return shutil.which("openclaw") is not None


def _send_openclaw(chat_id: str, text: str) -> bool:
    """Send message via OpenClaw CLI. Returns True on success."""
    import subprocess
    try:
        # Use openclaw message send with Telegram target
        result = subprocess.run(
            ["openclaw", "message", "send",
             "--channel", "telegram",
             "--to", f"telegram:{chat_id}",
             "--message", text],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True
        logger.warning(f"openclaw message send failed: {result.stderr}")
        return False
    except Exception as e:
        logger.warning(f"openclaw send error: {e}")
        return False


def _send_telegram(token: str, chat_id: str, text: str):
    """Send a Telegram message via Bot API or OpenClaw fallback.
    Token is passed as a path segment (Telegram's standard), but we suppress
    it from any error messages to avoid accidental log exposure.
    """
    # OpenClaw mode: use CLI instead of direct API
    if not token and _is_openclaw_mode():
        _send_openclaw(chat_id, text)
        return

    if not token:
        logger.warning("No TELEGRAM_BOT_TOKEN and openclaw not available — cannot send")
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as e:
        # Redact token from error string before logging
        safe_err = str(e).replace(token, "<redacted>")
        logger.error(f"Telegram send failed: {safe_err}")


def run_watcher(interval: int = 60, portfolio=None):
    """
    Blocking watcher loop. Polls Binance CMS every `interval` seconds.
    Sends Telegram notifications when new listings/launchpools/news appear.
    Writes PID to data/news_watcher.pid for stop/status.
    
    Supports two modes:
    1. Direct Telegram API (TELEGRAM_BOT_TOKEN set)
    2. OpenClaw mode (no token, uses `openclaw message send`)
    """
    import os
    import time
    import signal

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_USER_ID", "")
    openclaw_mode = _is_openclaw_mode()

    # Need either token OR openclaw CLI, plus a chat_id
    if not chat_id:
        console.print("[red]❌ TELEGRAM_USER_ID must be set in .env to use watch mode.[/red]")
        return

    if not token and not openclaw_mode:
        console.print("[red]❌ Neither TELEGRAM_BOT_TOKEN nor openclaw CLI found.[/red]")
        console.print("[dim]Set TELEGRAM_BOT_TOKEN in .env, or install OpenClaw.[/dim]")
        return

    # Write PID file
    WATCHER_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    WATCHER_PID_FILE.write_text(str(os.getpid()))

    def _cleanup(signum=None, frame=None):
        try:
            WATCHER_PID_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    news_mod = BinanceNews(portfolio=portfolio)
    mode_label = "OpenClaw" if openclaw_mode else "Telegram Bot API"
    console.print(f"[green]👁  BinanceCoach watcher started (interval: {interval}s)[/green]")
    console.print(f"[dim]Mode: {mode_label} | Notifying Telegram user {chat_id}. Press Ctrl+C to stop.[/dim]")

    # Send startup message
    _send_telegram(token, chat_id,
        f"👁 <b>BinanceCoach Watcher started</b>\n"
        f"Mode: {mode_label}\n"
        f"Checking for new listings &amp; announcements every <b>{interval}s</b>."
    )

    while True:
        try:
            result = news_mod.check_and_format_new()
            if result["has_new"]:
                parts = []
                if result["launchpool"]:
                    parts.append(news_mod.format_launchpool_html(result["launchpool"]))
                if result["listings"]:
                    parts.append(news_mod.format_listings_html(result["listings"]))
                if result["news"]:
                    parts.append(news_mod.format_news_html(result["news"], "📰 New Binance Announcement"))
                if result["portfolio_hits"]:
                    hits = "\n".join(
                        f"⚡ {h.get('matched_asset','?')}: {h['title']}"
                        for h in result["portfolio_hits"]
                    )
                    parts.append(f"<b>⚡ Affects your portfolio:</b>\n{hits}")
                if parts:
                    msg = "\n\n".join(parts)
                    # Split at 4096 chars
                    while msg:
                        _send_telegram(token, chat_id, msg[:4096])
                        msg = msg[4096:]
                    console.print(f"[green]🔔 Sent notification ({len(result['listings'])} listings, "
                                  f"{len(result['launchpool'])} launchpools, "
                                  f"{len(result['news'])} news)[/green]")
        except Exception as e:
            logger.warning(f"Watcher poll error: {e}")

        time.sleep(interval)


def watcher_status() -> dict:
    """Check if the watcher daemon is running. Returns dict with running, pid."""
    import os
    if not WATCHER_PID_FILE.exists():
        return {"running": False, "pid": None}
    try:
        pid = int(WATCHER_PID_FILE.read_text().strip())
        os.kill(pid, 0)  # Signal 0 = check existence only
        return {"running": True, "pid": pid}
    except (ProcessLookupError, PermissionError, ValueError):
        WATCHER_PID_FILE.unlink(missing_ok=True)
        return {"running": False, "pid": None}


def stop_watcher() -> bool:
    """Stop the running watcher daemon. Returns True if stopped."""
    import os
    import signal as _signal
    status = watcher_status()
    if not status["running"]:
        return False
    try:
        os.kill(status["pid"], _signal.SIGTERM)
        WATCHER_PID_FILE.unlink(missing_ok=True)
        return True
    except Exception:
        return False
