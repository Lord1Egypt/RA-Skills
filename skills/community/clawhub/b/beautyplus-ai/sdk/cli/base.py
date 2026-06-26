"""CLI base classes for BeautyPlus AI SDK."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Protocol
import argparse


class CliInterface(Protocol):
    """CLI interface definition for external callers."""

    def run_task(
        self,
        task_name: str,
        input_src: str,
        params: Optional[Dict] = None,
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> Dict:
        """Run a task and return result."""
        ...

    def query_task(self, task_id: str) -> Dict:
        """Query task status."""
        ...

    def spawn_run_task(
        self,
        task: str,
        input_src: str,
        params: Optional[Dict] = None,
        deliver_to: Optional[str] = None,
        deliver_channel: Optional[str] = None,
        run_timeout_seconds: int = 3600,
    ) -> Dict:
        """Generate async task configuration."""
        ...


class CliCommand(ABC):
    """Base class for CLI commands."""

    name: str = ""
    help: str = ""

    @classmethod
    @abstractmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        """Register this command with the subparser."""
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """Execute the command and return exit code."""
        pass


class NotifierInterface(Protocol):
    """Interface for notification channels."""

    def send_image(
        self, image_source: str, recipient: str, caption: str = ""
    ) -> Dict:
        """Send image notification."""
        ...

    def send_video(
        self,
        video_path: str,
        recipient: str,
        video_url: str = "",
        cover_url: str = "",
        duration: int = 0,
        caption: str = "",
    ) -> Dict:
        """Send video notification."""
        ...
