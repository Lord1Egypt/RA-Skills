"""Notification system — Telegram, email, or log."""

import os
import requests
from typing import Dict, List, Optional


class Notifier:
    """Send alerts about repository health changes."""

    def __init__(self, telegram_chat_id: str = None, telegram_token: str = None):
        self.telegram_chat_id = telegram_chat_id
        self.telegram_token = telegram_token

    def send_telegram(self, message: str) -> bool:
        """Send a message via Telegram bot."""
        if not self.telegram_token or not self.telegram_chat_id:
            return False
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            resp = requests.post(url, data={
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }, timeout=10)
            resp.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def notify(
        self,
        repo: str,
        vibe_score: int,
        delta: int,
        issues: List[str],
        pr_url: str = None
    ):
        """Send a notification about a repository's health."""
        status_emoji = "🟢" if vibe_score >= 80 else "🟡" if vibe_score >= 60 else "🟠" if vibe_score >= 40 else "🔴"
        delta_emoji = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"

        message = (
            f"{status_emoji} *{repo}*\n"
            f"Vibe: *{vibe_score}/100* {delta_emoji} {delta:+d}\n"
        )

        if issues:
            message += f"\n🚨 Issues:\n"
            for issue in issues[:5]:  # Limit to top 5
                message += f"  • {issue}\n"
            if len(issues) > 5:
                message += f"  ...and {len(issues) - 5} more\n"

        if pr_url:
            message += f"\n🔗 [Open PR]({pr_url})"

        # Try Telegram, fall back to print/log
        if self.send_telegram(message):
            print(f"Telegram notification sent for {repo}")
        else:
            print(f"[NOTIFY] {repo}: {vibe_score} ({delta:+d}) — {len(issues)} issues")
