#!/usr/bin/env python3
"""
Webhook & Alert Dispatcher for OpenClaw Agent Factory.
Sends notifications (Slack, Discord, Custom Webhooks) on mesh events.
"""

import json
import os
import urllib.request
import urllib.error
import time
from typing import Dict, Any, Optional

ALERTS_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "alerts_history.jsonl")


def dispatch_alert(
    event_type: str,
    title: str,
    message: str,
    severity: str = "INFO",  # INFO, WARNING, CRITICAL, SUCCESS
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Dispatches an alert to configured webhooks and logs to local history."""
    os.makedirs(os.path.dirname(ALERTS_LOG_FILE), exist_ok=True)

    payload = {
        "timestamp": time.time(),
        "event_type": event_type,
        "severity": severity,
        "title": title,
        "message": message,
        "metadata": metadata or {}
    }

    # Log locally
    with open(ALERTS_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

    # Send to Webhook URL if set in env
    webhook_url = os.environ.get("OPENCLAW_ALERT_WEBHOOK_URL")
    if webhook_url:
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req, timeout=3.0)
        except Exception as e:
            print(f"[Webhook Error] Failed to dispatch alert: {e}")

    # Console display with colors
    colors = {
        "INFO": "\033[94mℹ️",
        "SUCCESS": "\033[92m🎉",
        "WARNING": "\033[93m⚠️",
        "CRITICAL": "\033[91m🚨"
    }
    reset = "\033[0m"
    icon = colors.get(severity, "ℹ️")
    print(f"{icon} [{severity}] {title} : {message}{reset}")

    return payload


if __name__ == "__main__":
    dispatch_alert(
        event_type="SUBAGENT_PROMOTED",
        title="Nouveau sous-agent déployé",
        message="subagent_invoice_extraction (v1.0.0) a réussi l'évaluation 4D avec 73.5% d'économie de tokens.",
        severity="SUCCESS",
        metadata={"agent_id": "subagent_invoice_extraction", "version": "v1.0.0"}
    )
