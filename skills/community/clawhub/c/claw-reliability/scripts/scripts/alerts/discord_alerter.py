"""
claw-reliability: Discord webhook alerter.
Setup: Discord Channel Settings > Integrations > Webhooks > Copy URL
"""

import json
import urllib.request
import urllib.error
from alerts.base import BaseAlerter, Alert, Severity
from alerts.sanitizer import sanitize_text, sanitize_details


class DiscordAlerter(BaseAlerter):
    COLORS = {Severity.INFO: 0x3498DB, Severity.WARNING: 0xF39C12, Severity.CRITICAL: 0xE74C3C}

    def __init__(self, webhook_url):
        if not webhook_url:
            raise ValueError("Discord webhook_url is required")
        self.webhook_url = webhook_url

    def send_alert(self, alert):
        safe_message = sanitize_text(alert.message)
        safe_details = sanitize_details(alert.details)
        embed = {
            "title": f"🦞 claw-reliability — {alert.alert_type.value.replace('_', ' ').title()}",
            "description": safe_message,
            "color": self.COLORS.get(alert.severity, 0x95A5A6),
            "timestamp": alert.timestamp,
            "fields": [{"name": k.replace("_", " ").title(), "value": str(v)[:1024], "inline": True}
                       for k, v in safe_details.items()],
            "footer": {"text": f"Severity: {alert.severity.value.upper()}"}
        }
        payload = {"embeds": [embed], "username": "claw-reliability"}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.webhook_url, data=data,
                                      headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status in (200, 204)
        except Exception as e:
            print(f"[claw-reliability] Discord alert failed: {e}")
            return False
