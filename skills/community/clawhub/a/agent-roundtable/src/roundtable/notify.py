"""Notification dispatcher for Roundtable discussions.

Framework-agnostic: sends notifications via a pluggable send_fn callback.
No direct dependency on Hermes or any messaging platform SDK.

Usage:
    notifier = Notifier(config, send_fn=my_send_function)
    notifier.notify("speech", discussion_id="rt_xxx", ...)

The send_fn signature:
    def send_fn(platform: str, chat_id: str, message: str) -> None:
        ...
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

# Default event set
ALL_EVENTS = {"round_start", "speech", "round_end", "concluded"}


class Notifier:
    """Dispatches discussion events to configured messaging channels.

    Args:
        config: Notification config dict with keys:
            - enabled (bool): Whether notifications are active
            - channels (list): List of {platform, chat_id} dicts
            - events (list): Event names to subscribe to
        send_fn: Callback(platform, chat_id, message) that delivers the message.
            Must not raise — exceptions are caught and logged.
    """

    def __init__(
        self,
        config: dict[str, Any] | None,
        send_fn: Callable[[str, str, str], None] | None = None,
    ):
        self._config = config or {}
        self._channels: list[dict[str, str]] = self._config.get("channels", [])
        self._enabled = self._config.get("enabled", bool(self._channels))
        self._events: set[str] = set(self._config.get("events", list(ALL_EVENTS)))
        self._send_fn = send_fn

    @property
    def enabled(self) -> bool:
        return self._enabled and bool(self._channels) and self._send_fn is not None

    def should_notify(self, event: str) -> bool:
        """Check if this event should be notified."""
        return self.enabled and event in self._events

    def notify(
        self,
        event: str,
        *,
        discussion_id: str,
        topic: str = "",
        **kwargs: Any,
    ) -> None:
        """Send a notification for the given event.

        Silently swallows all exceptions — notifications must never
        block the discussion flow.
        """
        if not self.should_notify(event):
            return

        try:
            message = self._format_message(event, discussion_id=discussion_id, topic=topic, **kwargs)
            if not message:
                return
            self._dispatch(message)
        except Exception as e:
            logger.warning("Notification dispatch failed for event=%s: %s", event, e)

    def _dispatch(self, message: str) -> None:
        """Send message to all configured channels."""
        for ch in self._channels:
            platform = ch.get("platform", "feishu")
            chat_id = ch.get("chat_id", "")
            if not chat_id:
                continue
            try:
                if self._send_fn:
                    self._send_fn(platform, chat_id, message)
            except Exception as e:
                logger.warning(
                    "Failed to send notification to %s:%s: %s",
                    platform,
                    chat_id,
                    e,
                )

    def _format_message(
        self,
        event: str,
        *,
        discussion_id: str,
        topic: str = "",
        **kwargs: Any,
    ) -> str | None:
        """Format a human-readable message for the event.

        Returns None if the event type is unknown.
        """
        short_id = discussion_id[:12] if len(discussion_id) > 12 else discussion_id
        header = f"🔔 圆桌讨论 [{short_id}]"
        if topic:
            # Truncate topic to 30 chars
            t = topic[:30] + ("..." if len(topic) > 30 else "")
            header += f" {t}"

        if event == "round_start":
            round_num = kwargs.get("round_num", "?")
            prev_summary = kwargs.get("prev_summary", "")
            lines = [header, f"📢 第{round_num}轮讨论开始"]
            if prev_summary:
                # Truncate to 200 chars
                ps = prev_summary[:200] + ("..." if len(prev_summary) > 200 else "")
                lines.append(f"上轮回顾: {ps}")
            return "\n".join(lines)

        elif event == "speech":
            participant = kwargs.get("participant", "unknown")
            display_name = kwargs.get("display_name", participant)
            role = kwargs.get("role", "")
            round_num = kwargs.get("round_num", "?")
            content = kwargs.get("content", "")
            # Truncate content to 200 chars
            ct = content[:200] + ("..." if len(content) > 200 else "")
            role_str = f"({role})" if role else ""
            lines = [
                header,
                f"💬 第{round_num}轮 | {display_name}{role_str} 发言:",
                ct,
            ]
            return "\n".join(lines)

        elif event == "round_end":
            round_num = kwargs.get("round_num", "?")
            convergence = kwargs.get("convergence")
            key_points = kwargs.get("key_points", [])
            lines = [header, f"✅ 第{round_num}轮讨论结束"]
            if convergence is not None:
                lines.append(f"收敛度: {convergence:.2f}")
            if key_points:
                lines.append("本轮关键观点:")
                for pt in key_points[:5]:  # Max 5 points
                    lines.append(f"  • {pt[:100]}")
            return "\n".join(lines)

        elif event == "concluded":
            conclusion = kwargs.get("conclusion", "")
            convergence = kwargs.get("convergence")
            consensus = kwargs.get("consensus_points", [])
            disagreements = kwargs.get("disagreement_points", [])
            lines = [header, "🏁 讨论结束"]
            if convergence is not None:
                lines.append(f"最终收敛度: {convergence:.2f}")
            if conclusion:
                lines.append(f"结论: {conclusion}")
            if consensus:
                lines.append(f"共识点({len(consensus)}): " + "; ".join(consensus[:3])[:200])
            if disagreements:
                lines.append(f"分歧点({len(disagreements)}): " + "; ".join(disagreements[:3])[:200])
            return "\n".join(lines)

        return None


def validate_notification_config(config: Any) -> list[str]:
    """Validate notification config and return list of error messages.

    Returns empty list if valid.
    """
    errors = []
    if not isinstance(config, dict):
        return ["notifications must be an object"]

    if "channels" in config:
        channels = config["channels"]
        if not isinstance(channels, list):
            errors.append("channels must be an array")
        else:
            for i, ch in enumerate(channels):
                if not isinstance(ch, dict):
                    errors.append(f"channels[{i}] must be an object")
                elif not ch.get("chat_id"):
                    errors.append(f"channels[{i}].chat_id is required")

    if "events" in config:
        events = config["events"]
        if not isinstance(events, list):
            errors.append("events must be an array")
        else:
            unknown = set(events) - ALL_EVENTS
            if unknown:
                errors.append(f"unknown events: {', '.join(unknown)}")

    return errors
