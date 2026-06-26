"""
Cloud Relay Client — connects to the ChatClaw cloud WebSocket relay.

Handles:
  - Connecting to wss://api.sumeralabs.com/ws/agent/{api_key}
  - Auto-reconnect with exponential backoff
  - Bidirectional message relay between cloud dashboard and local skill
"""

import asyncio
import json
import logging
import websockets

logger = logging.getLogger(__name__)


class RelayClient:
    """WebSocket client that connects to the ChatClaw cloud relay."""

    def __init__(self, cloud_url: str, api_key: str):
        self.url         = f"{cloud_url}/ws/agent/{api_key}"
        self._log_url    = f"{cloud_url}/ws/agent/{api_key[:6]}***"  # redacted for logs
        self.ws          = None
        self._connected  = asyncio.Event()
        self._backoff    = 5    # initial retry delay (seconds)
        self._max_backoff = 60

    @property
    def connected(self) -> bool:
        return self.ws is not None and self.ws.open

    async def connect(self):
        """Connect to the cloud relay with exponential backoff auto-reconnect."""
        # Clear the event at the START of every connect attempt so that any
        # in-flight receive() calls block correctly while we (re)connect.
        # Without this, a stale "set" event after a disconnect would let
        # receive() call recv() on a dead socket before the new socket is ready.
        self._connected.clear()

        backoff = self._backoff
        while True:
            try:
                logger.info(f"Connecting to cloud relay: {self._log_url}...")
                self.ws = await websockets.connect(
                    self.url,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=5,
                    max_size=None,        # no message-size cap for large agent responses
                )
                logger.info("Connected to cloud relay ✓")
                self._connected.set()
                backoff = self._backoff  # reset on success
                return
            except Exception as e:
                logger.warning(f"Cloud connection failed: {e}. Retrying in {backoff}s...")
                self._connected.clear()
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, self._max_backoff)

    async def receive(self) -> dict:
        """
        Block until the relay is connected, then return the next JSON message.
        Raises websockets.ConnectionClosed if the connection drops.
        """
        await self._connected.wait()
        raw  = await self.ws.recv()
        data = json.loads(raw) if isinstance(raw, str) else raw
        logger.debug(f"Cloud → Local: {json.dumps(data)[:200]}")
        return data

    async def send(self, message: dict) -> None:
        """
        Send a JSON message to the cloud relay.
        Blocks until connected — safe to call immediately after connect() returns.
        """
        await self._connected.wait()
        await self.ws.send(json.dumps(message))
        logger.debug(f"Local → Cloud: {json.dumps(message)[:200]}")

    async def close(self) -> None:
        """Gracefully close the connection and reset state."""
        self._connected.clear()
        if self.ws:
            await self.ws.close()
        logger.info("Cloud relay connection closed")