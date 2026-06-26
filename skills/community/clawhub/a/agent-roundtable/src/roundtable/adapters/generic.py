"""Generic Python API adapter for Roundtable.

For use outside any specific agent framework. Provides a simple,
importable interface that works in any Python script.

Usage::

    from roundtable.adapters.generic import Roundtable

    rt = Roundtable()
    result = rt.init(topic="...", participants=[...])
    result = rt.speak(discussion_id, "alice", "Hello!")

With notifications::

    def my_send(platform, chat_id, message):
        print(f"[{platform}:{chat_id}] {message}")

    rt = Roundtable(send_fn=my_send)
    result = rt.init(
        topic="...",
        participants=[...],
        notifications={
            "enabled": True,
            "channels": [{"platform": "console", "chat_id": "default"}],
        },
    )
"""

from __future__ import annotations

import builtins
from collections.abc import Callable
from typing import Any

from roundtable.core import RoundtableCore
from roundtable.db import RoundtableDB


class Roundtable:
    """Simple facade over RoundtableCore.

    All methods return dicts (JSON-serializable). Errors are returned
    as ``{"error": "message"}`` dicts instead of raising exceptions,
    making it safe for untrusted callers.

    Args:
        db_path: Optional path to the SQLite database file.
        send_fn: Optional callback(platform, chat_id, message) for notifications.
    """

    def __init__(
        self,
        db_path: str | None = None,
        send_fn: Callable[[str, str, str], None] | None = None,
    ):
        db = RoundtableDB(db_path) if db_path else RoundtableDB()
        self._core = RoundtableCore(db, send_fn=send_fn)

    def init(
        self,
        topic: str,
        participants: builtins.list[dict[str, Any]],
        *,
        notifications: dict[str, Any] | None = None,
        web: bool = False,
        web_port: int = 8199,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new discussion.

        Args:
            topic: Discussion topic.
            participants: List of participant dicts (min 2).
            notifications: Optional notification config dict.
            web: If True, start a web viewer for live viewing.
            web_port: Port for the web viewer (default 8199).
            **kwargs: Additional arguments passed to create_discussion.
        """
        try:
            return self._core.create_discussion(
                topic,
                participants,
                notifications=notifications,
                web=web,
                web_port=web_port,
                **kwargs,
            )
        except (ValueError, Exception) as e:
            return {"error": str(e)}

    def speak(
        self,
        discussion_id: str,
        participant: str,
        content: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Record a speech."""
        try:
            return self._core.speak(discussion_id, participant, content, **kwargs)
        except Exception as e:
            return {"error": str(e)}

    def read(self, discussion_id: str, **kwargs: Any) -> dict[str, Any]:
        """Read discussion history."""
        try:
            return self._core.read(discussion_id, **kwargs)
        except Exception as e:
            return {"error": str(e)}

    def get_status(self, discussion_id: str) -> dict[str, Any]:
        """Get discussion status."""
        try:
            return self._core.status(discussion_id)
        except Exception as e:
            return {"error": str(e)}

    def summarize(self, discussion_id: str, *, compact: bool = False) -> dict[str, Any]:
        """Get summary data."""
        try:
            return self._core.summarize(discussion_id, compact=compact)
        except Exception as e:
            return {"error": str(e)}

    def end(
        self,
        discussion_id: str,
        *,
        force: bool = False,
        conclusion: str | None = None,
    ) -> dict[str, Any]:
        """End a discussion."""
        try:
            return self._core.end_discussion(discussion_id, force=force, conclusion=conclusion)
        except Exception as e:
            return {"error": str(e)}

    def list(self, **kwargs: Any) -> dict[str, Any]:
        """List discussions."""
        try:
            return self._core.list_discussions(**kwargs)
        except Exception as e:
            return {"error": str(e)}

    def advance(self, discussion_id: str) -> dict[str, Any]:
        """Explicitly advance to the next round.

        Use when auto-advance doesn't trigger. If max_rounds is exceeded,
        the discussion is automatically concluded.
        """
        try:
            return self._core.advance(discussion_id)
        except Exception as e:
            return {"error": str(e)}

    def run_demo(
        self,
        *,
        topic: str | None = None,
        participants: builtins.list[dict[str, Any]] | None = None,
        max_rounds: int = 3,
        verbose: bool = True,
        web: bool = False,
        web_port: int = 8199,
    ) -> dict[str, Any]:
        """Run a complete demo discussion with pre-scripted content.

        Simulates a realistic multi-round discussion. Prints formatted
        output to terminal when verbose=True.

        Args:
            topic: Custom topic (uses default demo topic if None).
            participants: Custom participants (uses default if None).
            max_rounds: Number of rounds (default 3).
            verbose: Print formatted output to stdout.
            web: If True, start a web viewer and publish speeches live.
            web_port: Preferred port for the web viewer (default 8199).
        """
        try:
            return self._core.run_demo(
                topic=topic,
                participants=participants,
                max_rounds=max_rounds,
                verbose=verbose,
                web=web,
                web_port=web_port,
            )
        except Exception as e:
            return {"error": str(e)}

    def notify(
        self,
        discussion_id: str,
        event: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Manually trigger a notification for a discussion event.

        Valid events: round_start, speech, round_end, concluded.
        """
        try:
            return self._core.notify(discussion_id, event, **kwargs)
        except Exception as e:
            return {"error": str(e)}

    # ------------------------------------------------------------------
    # API Aliases
    # ------------------------------------------------------------------

    def create_discussion(
        self,
        topic: str,
        participants: builtins.list[dict[str, Any]],
        *,
        notifications: dict[str, Any] | None = None,
        web: bool = False,
        web_port: int = 8199,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new discussion. Alias for init."""
        return self.init(
            topic,
            participants,
            notifications=notifications,
            web=web,
            web_port=web_port,
            **kwargs,
        )

    def end_discussion(
        self,
        discussion_id: str,
        *,
        force: bool = False,
        conclusion: str | None = None,
    ) -> dict[str, Any]:
        """End a discussion. Alias for end."""
        return self.end(discussion_id, force=force, conclusion=conclusion)

    def list_discussions(self, **kwargs: Any) -> dict[str, Any]:
        """List discussions. Alias for list."""
        return self.list(**kwargs)

    def status(self, discussion_id: str) -> dict[str, Any]:
        """Get discussion status. Alias for get_status."""
        return self.get_status(discussion_id)
