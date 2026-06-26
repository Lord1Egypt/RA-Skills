"""SSE Event Bus and WebSocket manager for agentMemo v3.0.0."""
from __future__ import annotations
import asyncio
import json
from typing import Optional

from fastapi import WebSocket


class EventBus:
    def __init__(self):
        self._subscribers: list[tuple[asyncio.Queue, Optional[str]]] = []
        self._websockets: list[tuple[WebSocket, Optional[str]]] = []

    @property
    def active_websocket_count(self) -> int:
        return len(self._websockets)

    async def publish(self, event: dict):
        # SSE subscribers
        for queue, ns_filter in self._subscribers:
            if ns_filter is None or ns_filter == event.get("namespace"):
                try:
                    queue.put_nowait(event)
                except asyncio.QueueFull:
                    pass

        # WebSocket subscribers
        disconnected = []
        for ws, ns_filter in self._websockets:
            if ns_filter is None or ns_filter == event.get("namespace"):
                try:
                    await ws.send_json(event)
                except Exception:
                    disconnected.append((ws, ns_filter))
        for entry in disconnected:
            self._websockets.remove(entry)

    async def subscribe(self, namespace: Optional[str] = None):
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        entry = (queue, namespace)
        self._subscribers.append(entry)
        try:
            while True:
                event = await queue.get()
                yield json.dumps(event)
        finally:
            self._subscribers.remove(entry)

    async def ws_subscribe(self, websocket: WebSocket, namespace: Optional[str] = None):
        await websocket.accept()
        entry = (websocket, namespace)
        self._websockets.append(entry)
        try:
            while True:
                data = await websocket.receive_text()
                try:
                    msg = json.loads(data)
                    if msg.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                except (json.JSONDecodeError, TypeError):
                    pass
        except Exception:
            pass
        finally:
            if entry in self._websockets:
                self._websockets.remove(entry)


event_bus = EventBus()
