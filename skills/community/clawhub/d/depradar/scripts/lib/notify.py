"""Notification backends for /depradar.

Supports:
  --notify=slack://WEBHOOK_URL   POST breaking change summary to Slack
  --notify=file:///path/out.json Write JSON report to file
  stdout (default)               No notification — rendered to terminal
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Optional


def parse_notify_target(target: str) -> Optional[dict]:
    """Parse a --notify=TARGET string into a {type, dest} dict.

    Supported targets:
        slack://https://hooks.slack.com/services/...
        slack://hooks.slack.com/services/...
        file:///absolute/path/report.json
        file://relative/path/report.json

    Returns None if the target format is unrecognized.
    """
    if target.startswith("slack://"):
        webhook = target[len("slack://"):]
        if not webhook.startswith("http"):
            webhook = "https://" + webhook
        return {"type": "slack", "dest": webhook}

    if target.startswith("file://"):
        path_str = target[len("file://"):]
        return {"type": "file", "dest": path_str}

    return None


def send_notification(target_dict: dict, report_dict: dict) -> None:
    """Dispatch a notification based on target_dict from parse_notify_target().

    Raises on failure (caller should catch and warn).
    """
    ntype = target_dict.get("type")
    dest  = target_dict.get("dest", "")

    if ntype == "slack":
        _send_slack(dest, report_dict)
    elif ntype == "file":
        _write_file(dest, report_dict)
    else:
        raise ValueError(f"Unknown notification type: {ntype!r}")


def _send_slack(webhook_url: str, report: dict) -> None:
    """POST a Slack Block Kit message to webhook_url."""
    blocks = _build_slack_blocks(report)
    payload = json.dumps({"blocks": blocks}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        if resp.status not in (200, 204):
            raise RuntimeError(f"Slack webhook returned HTTP {resp.status}")


def _write_file(path_str: str, report: dict) -> None:
    """Write the report JSON to a file."""
    out_path = Path(path_str)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _build_slack_blocks(report: dict) -> list:
    """Build a Slack Block Kit message summarising breaking changes."""
    breaking = report.get("packages_with_breaking_changes", [])
    project  = report.get("project_path", "")

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🔴 depradar: {len(breaking)} breaking change(s) found",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Project:* `{project}`",
            },
        },
    ]

    for pkg in breaking[:10]:  # Slack has block limits
        name    = pkg.get("package", "?")
        current = pkg.get("current_version", "?")
        latest  = pkg.get("latest_version", "?")
        score   = pkg.get("score", 0)
        changes = pkg.get("breaking_changes", [])
        impact  = pkg.get("impact_locations", [])

        summary_parts = [f"*{name}*  `{current}` → `{latest}`  score: {score}"]

        if changes:
            first_change = changes[0]
            desc = first_change.get("description", "")[:120]
            summary_parts.append(f"> {desc}")

        if impact:
            summary_parts.append(
                f"Affects {len(impact)} file(s): "
                + ", ".join(
                    f"`{loc.get('file_path', '?').split('/')[-1]}`"
                    for loc in impact[:3]
                )
            )

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(summary_parts),
            },
        })

    if len(breaking) > 10:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"_... and {len(breaking) - 10} more. Run `/depradar` for full report._",
            },
        })

    blocks.append({"type": "divider"})
    return blocks
