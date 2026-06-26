"""Interface for communicating with an OpenClaw agent via the CLI.

Wraps the `openclaw agent` command to send messages and capture replies.
"""

import asyncio
import re

from loguru import logger

# Lines matching these patterns are treated as CLI noise, not agent output
_LOG_LINE_RE = re.compile(
    r"^\s*\[[\w./-]+\]"  # e.g. "[plugins] ...", "[gateway] ..."
)


class ClawAgent:
    """Send messages to an OpenClaw agent and capture its replies."""

    def __init__(self, recipient: str = ""):
        self._recipient = recipient

    async def send(self, message: str, timeout: float = 120.0) -> str:
        """Deliver *message* to the agent and return its textual reply.

        Raises RuntimeError if the subprocess exits with a non-zero code
        or produces no parseable reply.
        """
        cmd = [
            "openclaw", "agent",
            "--to", self._recipient,
            "--message", message,
        ]
        logger.info("Sending to Claw agent (%s)", self._recipient)
        logger.debug("Command: %s", cmd)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            proc.kill()
            raise RuntimeError(
                f"openclaw agent timed out after {timeout}s"
            )

        if proc.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            raise RuntimeError(
                f"openclaw agent failed (exit {proc.returncode}): {err}"
            )

        raw = stdout.decode(errors="replace")
        logger.debug("Raw CLI output:\n%s", raw)
        return self._parse_reply(raw)

    @staticmethod
    def _parse_reply(raw: str) -> str:
        """Strip CLI log lines and return only the agent's reply text."""
        lines = raw.splitlines()
        reply_lines = [
            line for line in lines
            if line.strip() and not _LOG_LINE_RE.match(line)
        ]
        reply = "\n".join(reply_lines).strip()
        if not reply:
            raise RuntimeError(
                "Could not extract a reply from openclaw output. "
                f"Raw output:\n{raw}"
            )
        return reply
