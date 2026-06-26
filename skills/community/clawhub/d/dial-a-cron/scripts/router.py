#!/usr/bin/env python3
"""
Dial-a-Cron — Delivery Router (Full)
Routes LLM cron output to any target: log, file, Telegram, A2A, webhook, email.

Severity levels (ascending):
    silent → log → info → alert → urgent
"""

import json
import re
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

SEVERITY_ORDER = ["silent", "log", "info", "alert", "urgent"]
LOG_DIR = os.environ.get("DAC_LOG_DIR", str(Path(__file__).parent.parent / "logs"))


@dataclass
class RoutingSpec:
    to: str                          # target (user, agent, channel, or "log"/"silent")
    channel: str = "telegram"        # "telegram" | "a2a" | "log" | "silent" | "webhook" | "file" | "email"
    when: list[str] = field(default_factory=lambda: ["alert", "urgent"])
    match: list[str] = field(default_factory=list)   # keyword/regex match on body
    target_id: Optional[str] = None  # Telegram chat ID, webhook URL, file path, email, agent ID


@dataclass
class RoutingResult:
    severity: str
    routed_to: list[str]
    delivered: bool
    log_path: Optional[str] = None
    message: Optional[str] = None
    errors: list[str] = field(default_factory=list)


class DeliveryRouter:
    def __init__(self, specs: list[RoutingSpec], job_id: str = "unknown"):
        self.specs = specs
        self.job_id = job_id

    def _matches_content(self, body: str, keywords: list[str]) -> bool:
        if not keywords:
            return True
        for kw in keywords:
            if re.search(kw, body, re.IGNORECASE):
                return True
        return False

    def _severity_matches(self, severity: str, when_list: list[str]) -> bool:
        for w in when_list:
            if severity == w:
                return True
            if w.startswith(">="):
                threshold = w[2:]
                try:
                    if SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index(threshold):
                        return True
                except ValueError:
                    pass
        return False

    def _format_message(self, severity: str, summary: str, body: str, job_id: str) -> str:
        icon = {"silent": "[-]", "log": "[LOG]", "info": "[i]", "alert": "[!]", "urgent": "[!!!]"}.get(severity, "[?]")
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        return f"{icon} {job_id} -- {now}\n\n{summary}"

    def _log_to_file(self, job_id: str, severity: str, summary: str, body: str) -> str:
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        log_path = str(Path(LOG_DIR) / f"{job_id}.log")
        now = datetime.now(timezone.utc).isoformat()
        entry = f"[{now}] [{severity.upper()}] {summary}\n"
        with open(log_path, "a") as f:
            f.write(entry)
        return log_path

    def _deliver_telegram(self, spec: RoutingSpec, message: str) -> Optional[str]:
        """Deliver via OpenClaw message tool (shell out to openclaw CLI)."""
        target = spec.target_id or spec.to
        try:
            cmd = f'openclaw message send --to "{target}" --message "{message[:4000]}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"Telegram delivery failed: {result.stderr[:200]}"
            return None
        except Exception as e:
            return f"Telegram delivery error: {e}"

    def _deliver_webhook(self, spec: RoutingSpec, severity: str, summary: str, body: str) -> Optional[str]:
        """POST JSON to a webhook URL."""
        url = spec.target_id
        if not url:
            return "Webhook: no target_id (URL) specified"
        payload = json.dumps({
            "job_id": self.job_id,
            "severity": severity,
            "summary": summary,
            "body": body[:2000],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }).encode()
        try:
            req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(req, timeout=15) as resp:
                if resp.status >= 400:
                    return f"Webhook returned {resp.status}"
            return None
        except Exception as e:
            return f"Webhook error: {e}"

    def _deliver_file(self, spec: RoutingSpec, severity: str, summary: str, body: str) -> Optional[str]:
        """Append to a file."""
        file_path = spec.target_id
        if not file_path:
            return "File delivery: no target_id (path) specified"
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            now = datetime.now(timezone.utc).isoformat()
            entry = f"\n## [{now}] [{severity.upper()}] {self.job_id}\n{summary}\n"
            if body and body != summary:
                entry += f"\n{body[:2000]}\n"
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(entry)
            return None
        except Exception as e:
            return f"File delivery error: {e}"

    def _deliver_a2a(self, spec: RoutingSpec, message: str) -> Optional[str]:
        """Send via A2A (shell out)."""
        agent = spec.target_id or spec.to
        try:
            cmd = f'openclaw a2a send --to "{agent}" --message "{message[:2000]}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"A2A delivery failed: {result.stderr[:200]}"
            return None
        except Exception as e:
            return f"A2A delivery error: {e}"

    def _deliver_email(self, spec: RoutingSpec, severity: str, summary: str, body: str) -> Optional[str]:
        """Send email via gog CLI."""
        to_addr = spec.target_id
        if not to_addr:
            return "Email: no target_id (address) specified"
        try:
            subject = f"[Dial-a-Cron] [{severity.upper()}] {self.job_id}"
            full_body = f"{summary}\n\n{body[:4000]}" if body != summary else summary
            cmd = f'gog gmail send --to "{to_addr}" --subject "{subject}" --body "{full_body[:4000]}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"Email failed: {result.stderr[:200]}"
            return None
        except Exception as e:
            return f"Email error: {e}"

    def route(
        self,
        severity: str,
        summary: str,
        body: str = "",
        buttons: list[dict] = None,
    ) -> RoutingResult:
        routed_to = []
        delivered = False
        log_path = None
        errors = []
        message = self._format_message(severity, summary, body, self.job_id)

        for spec in self.specs:
            sev_match = self._severity_matches(severity, spec.when) if spec.when else True
            if not sev_match:
                continue
            if spec.match and not self._matches_content(body + " " + summary, spec.match):
                continue

            target = spec.to
            channel = spec.channel
            routed_to.append(f"{target}({channel})")
            error = None

            if channel == "log" or target == "log":
                log_path = self._log_to_file(self.job_id, severity, summary, body)
                delivered = True

            elif channel == "silent" or target == "silent" or severity == "silent":
                log_path = self._log_to_file(self.job_id, severity, f"[silent] {summary}", "")
                delivered = True

            elif channel == "telegram":
                error = self._deliver_telegram(spec, message)
                if not error:
                    delivered = True

            elif channel == "webhook":
                error = self._deliver_webhook(spec, severity, summary, body)
                if not error:
                    delivered = True

            elif channel == "file":
                error = self._deliver_file(spec, severity, summary, body)
                if not error:
                    delivered = True

            elif channel == "a2a":
                error = self._deliver_a2a(spec, message)
                if not error:
                    delivered = True

            elif channel == "email":
                error = self._deliver_email(spec, severity, summary, body)
                if not error:
                    delivered = True

            else:
                error = f"Unknown channel: {channel}"

            if error:
                errors.append(error)
                # Still log it as fallback
                log_path = self._log_to_file(self.job_id, severity, f"[delivery-error] {error}: {summary}", body)

        if not routed_to:
            log_path = self._log_to_file(self.job_id, severity, f"[unrouted] {summary}", "")
            routed_to = ["log(fallback)"]

        return RoutingResult(
            severity=severity,
            routed_to=routed_to,
            delivered=delivered,
            log_path=log_path,
            message=message,
            errors=errors,
        )


def evaluate_severity(output: str, errors: int = 0) -> str:
    if errors >= 3:
        return "urgent"
    if errors >= 2:
        return "alert"
    output_lower = output.lower()
    if any(w in output_lower for w in ["urgent", "critical", "down", "unreachable", "failed", "error"]):
        return "alert"
    if any(w in output_lower for w in ["warning", "slow", "degraded", "unusual"]):
        return "info"
    if any(w in output_lower for w in ["complete", "synced", "ok", "healthy", "no change", "noop"]):
        return "log"
    return "info"


if __name__ == "__main__":
    specs = [
        RoutingSpec(to="bobby", channel="telegram", when=["alert", "urgent"], target_id="8301484123"),
        RoutingSpec(to="faceman", channel="a2a", when=["info"], match=["revenue", "demo", "product"]),
        RoutingSpec(to="ops-hook", channel="webhook", when=["alert"], target_id="https://hooks.example.com/ops"),
        RoutingSpec(to="report", channel="file", when=[">=info"], target_id="reports/daily-cron-report.md"),
        RoutingSpec(to="log", channel="log", when=["silent", "log", "info", "alert", "urgent"]),
    ]
    router = DeliveryRouter(specs, job_id="test-job")

    r = router.route("info", "Found 2 revenue signals", "revenue demo product pipeline")
    print(f"Test 1 (info+revenue): routed to {r.routed_to}, errors: {r.errors}")

    r = router.route("alert", "Helga2 unreachable", "connection refused")
    print(f"Test 2 (alert): routed to {r.routed_to}, errors: {r.errors}")

    r = router.route("silent", "No changes", "")
    print(f"Test 3 (silent): routed to {r.routed_to}")
