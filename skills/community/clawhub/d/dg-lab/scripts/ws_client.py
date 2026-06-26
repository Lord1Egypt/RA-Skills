#!/usr/bin/env python3
"""DG-LAB WebSocket Controller.

Connects to a DG-LAB relay server as a third-party terminal and exposes
a local HTTP API for the AI agent to send control commands.

SECURITY MANIFEST:
  Environment variables accessed: none
  External endpoints called: ws://HOST:PORT (user-specified DG-LAB relay server, default localhost)
  Local files read: scripts/presets.json
  Local files written: none
  Network listeners: HTTP on 127.0.0.1:PORT (default 8899, loopback only)

Architecture:
  AI Agent --HTTP--> this script --WebSocket--> Relay Server --WS--> DG-LAB APP --BLE--> Device

Usage:
  python ws_client.py --ws-url ws://HOST:PORT [--port 8899] [--strength-limit 50]

HTTP Endpoints:
  GET  /status           - Connection and device status
  GET  /qrcode           - QR code URL for APP pairing
  GET  /presets           - List available waveform presets
  POST /strength         - Control channel strength
  POST /waveform         - Send waveform to channel
  POST /clear            - Clear waveform queue
  POST /stop             - Graceful shutdown
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
import threading
import time
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from pathlib import Path

try:
    import websockets
    import websockets.exceptions
except ImportError:
    print("ERROR: 'websockets' package required. Install: pip install websockets", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from waveform import get_preset, list_presets, validate_hex_data  # noqa: E402

logger = logging.getLogger("dglab")

# ---------------------------------------------------------------------------
# Safety
# ---------------------------------------------------------------------------

class SafetyGuard:
    """Enforces strength limits and rate limiting."""

    def __init__(self, strength_limit: int = 50):
        self.strength_limit = max(0, min(200, strength_limit))
        self._last_strength_cmd_time: float = 0
        self._min_cmd_interval: float = 0.1  # 100ms between strength commands

    def check_strength_set(self, value: int) -> int:
        if not 0 <= value <= self.strength_limit:
            raise ValueError(
                f"Strength {value} exceeds safety limit {self.strength_limit} "
                f"(allowed: 0-{self.strength_limit})"
            )
        self._rate_check()
        return value

    def check_strength_change(self, current: int, delta: int, increasing: bool) -> int:
        if increasing and current + delta > self.strength_limit:
            raise ValueError(
                f"Increase rejected: {current} + {delta} = {current + delta} > limit {self.strength_limit}"
            )
        self._rate_check()
        return delta

    def _rate_check(self):
        now = time.monotonic()
        elapsed = now - self._last_strength_cmd_time
        if elapsed < self._min_cmd_interval:
            raise ValueError(
                f"Rate limit: wait {self._min_cmd_interval - elapsed:.0f}ms between strength commands"
            )
        self._last_strength_cmd_time = now


# ---------------------------------------------------------------------------
# WebSocket Session
# ---------------------------------------------------------------------------

class DGLabSession:
    """Manages the persistent WebSocket connection to the DG-LAB relay server."""

    def __init__(self, ws_url: str, safety: SafetyGuard):
        self.ws_url = ws_url
        self.safety = safety
        self.client_id: str | None = None
        self.target_id: str | None = None
        self._ws = None
        self.connected = False
        self.paired = False
        self.strength_a = 0
        self.strength_b = 0
        self.limit_a = 200
        self.limit_b = 200
        self.last_feedback: int | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._stop_event = asyncio.Event()
        self._error: str | None = None
        self._message_log: list[dict] = []
        self._max_log = 50

    @property
    def qr_url(self) -> str | None:
        if not self.client_id:
            return None
        return (
            f"https://www.dungeon-lab.com/app-download.php"
            f"#DGLAB-SOCKET#{self.ws_url}/{self.client_id}"
        )

    def status_dict(self) -> dict:
        return {
            "connected": self.connected,
            "paired": self.paired,
            "client_id": self.client_id,
            "target_id": self.target_id,
            "qr_url": self.qr_url,
            "strength_a": self.strength_a,
            "strength_b": self.strength_b,
            "device_limit_a": self.limit_a,
            "device_limit_b": self.limit_b,
            "safety_limit": self.safety.strength_limit,
            "last_feedback": self.last_feedback,
            "error": self._error,
        }

    # -- Connection lifecycle ------------------------------------------------

    async def run(self):
        """Main loop: connect, listen, reconnect on failure."""
        while not self._stop_event.is_set():
            try:
                await self._connect_and_listen()
            except (
                websockets.exceptions.ConnectionClosed,
                websockets.exceptions.WebSocketException,
                OSError,
            ) as e:
                self._error = f"Connection lost: {e}"
                logger.warning("Connection lost: %s. Reconnecting in 3s...", e)
                self.connected = False
                self.paired = False
                await asyncio.sleep(3)
            except asyncio.CancelledError:
                break
        await self._disconnect()

    async def _connect_and_listen(self):
        logger.info("Connecting to %s ...", self.ws_url)
        self._ws = await websockets.connect(
            self.ws_url,
            ping_interval=30,
            ping_timeout=10,
            close_timeout=5,
        )
        self.connected = True
        self._error = None
        logger.info("WebSocket connected, waiting for clientId...")

        init_msg = await asyncio.wait_for(self._ws.recv(), timeout=10)
        data = json.loads(init_msg)
        if data.get("type") == "bind" and data.get("clientId"):
            self.client_id = data["clientId"]
            logger.info("Received clientId: %s", self.client_id)
            logger.info("QR URL: %s", self.qr_url)
        else:
            raise RuntimeError(f"Unexpected init message: {data}")

        async for raw in self._ws:
            if self._stop_event.is_set():
                break
            try:
                msg = json.loads(raw)
                self._handle_message(msg)
            except json.JSONDecodeError:
                logger.warning("Non-JSON message: %s", raw[:200])

    def _handle_message(self, msg: dict):
        msg_type = msg.get("type")
        message = str(msg.get("message", ""))

        self._message_log.append({"time": time.time(), "data": msg})
        if len(self._message_log) > self._max_log:
            self._message_log.pop(0)

        if msg_type == "bind":
            if message == "200":
                self.target_id = msg.get("targetId")
                self.paired = True
                self._error = None
                logger.info("Paired with APP (targetId: %s)", self.target_id)
            elif message == "400":
                self._error = "Bind failed: clientId already bound by another"
                logger.error(self._error)
            elif message == "401":
                self._error = "Bind failed: target client does not exist"
                logger.error(self._error)

        elif msg_type == "break":
            self.paired = False
            self.target_id = None
            self.strength_a = 0
            self.strength_b = 0
            logger.warning("APP disconnected (code: %s)", message)

        elif msg_type == "heartbeat":
            pass

        elif msg_type == "error":
            self._error = f"Server error: {message}"
            logger.error(self._error)

        else:
            if message.startswith("strength-"):
                parts = message[len("strength-"):].split("+")
                if len(parts) == 4:
                    try:
                        self.strength_a = int(parts[0])
                        self.strength_b = int(parts[1])
                        self.limit_a = int(parts[2])
                        self.limit_b = int(parts[3])
                    except ValueError:
                        logger.warning("Malformed strength feedback: %s", message)
            elif message.startswith("feedback-"):
                try:
                    self.last_feedback = int(message[len("feedback-"):])
                except ValueError:
                    pass

    async def _disconnect(self):
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        self.connected = False
        self.paired = False

    def request_stop(self):
        self._stop_event.set()

    # -- Commands ------------------------------------------------------------

    def _require_paired(self):
        if not self.paired or not self._ws:
            raise RuntimeError("Not paired with APP. Scan the QR code first.")

    async def send_strength(self, channel: str, action: str, value: int = 1):
        self._require_paired()
        ch_num = self._parse_channel_num(channel)
        current = self.strength_a if ch_num == 1 else self.strength_b

        if action == "set":
            self.safety.check_strength_set(value)
            payload = self._build_msg(type=3, channel=ch_num, strength=value)
        elif action == "increase":
            self.safety.check_strength_change(current, value, increasing=True)
            payload = self._build_msg(type=2, channel=ch_num)
        elif action == "decrease":
            self.safety.check_strength_change(current, value, increasing=False)
            payload = self._build_msg(type=1, channel=ch_num)
        else:
            raise ValueError(f"Unknown action '{action}'. Use: set, increase, decrease")

        await self._ws.send(json.dumps(payload))
        logger.info("Strength %s ch=%s val=%d", action, channel, value)

    async def send_waveform(self, channel: str, data: list[str], duration: int = 5):
        self._require_paired()
        validate_hex_data(data)
        ch = channel.upper()
        if ch not in ("A", "B"):
            raise ValueError("Channel must be 'A' or 'B'")

        payload = {
            "type": "clientMsg",
            "channel": ch,
            "time": max(1, min(duration, 60)),
            "message": f"{ch}:{json.dumps(data)}",
            "clientId": self.client_id,
            "targetId": self.target_id,
        }

        raw = json.dumps(payload)
        if len(raw) > 1950:
            raise ValueError(f"Message too long ({len(raw)} > 1950 chars). Reduce waveform entries.")
        await self._ws.send(raw)
        logger.info("Waveform sent: ch=%s entries=%d duration=%ds", ch, len(data), duration)

    async def clear_channel(self, channel: str):
        self._require_paired()
        ch_num = self._parse_channel_num(channel)
        payload = self._build_msg(type=4, message=f"clear-{ch_num}")
        await self._ws.send(json.dumps(payload))
        logger.info("Cleared waveform queue: ch=%s", channel)

    async def emergency_stop(self):
        """Set both channels to zero strength and clear queues."""
        if not self._ws or not self.paired:
            return
        try:
            for ch in (1, 2):
                p = self._build_msg(type=3, channel=ch, strength=0)
                await self._ws.send(json.dumps(p))
                p2 = self._build_msg(type=4, message=f"clear-{ch}")
                await self._ws.send(json.dumps(p2))
            logger.warning("EMERGENCY STOP executed")
        except Exception as e:
            logger.error("Emergency stop failed: %s", e)

    # -- Helpers -------------------------------------------------------------

    @staticmethod
    def _parse_channel_num(channel: str) -> int:
        ch = channel.upper()
        if ch == "A" or ch == "1":
            return 1
        if ch == "B" or ch == "2":
            return 2
        raise ValueError(f"Invalid channel '{channel}'. Use A/B or 1/2.")

    def _build_msg(self, **kwargs) -> dict:
        base = {
            "message": kwargs.pop("message", "set channel"),
            "clientId": self.client_id,
            "targetId": self.target_id,
        }
        base.update(kwargs)
        return base


# ---------------------------------------------------------------------------
# HTTP Control API
# ---------------------------------------------------------------------------

class APIHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler that bridges to the async DGLabSession."""

    session: DGLabSession
    loop: asyncio.AbstractEventLoop
    server_shutdown: threading.Event

    def log_message(self, format, *args):
        logger.debug("HTTP %s", format % args)

    def _json_response(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def _run_async(self, coro):
        """Submit a coroutine to the event loop and wait for result."""
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result(timeout=10)

    # -- Routes --------------------------------------------------------------

    def do_GET(self):
        try:
            if self.path == "/status":
                self._json_response(200, self.session.status_dict())
            elif self.path == "/qrcode":
                url = self.session.qr_url
                if url:
                    self._json_response(200, {"qr_url": url, "hint": "APP扫描此二维码完成配对"})
                else:
                    self._json_response(503, {"error": "Not connected yet, no clientId"})
            elif self.path == "/presets":
                self._json_response(200, {"presets": list_presets()})
            else:
                self._json_response(404, {"error": f"Unknown endpoint: {self.path}"})
        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_POST(self):
        try:
            body = self._read_json_body()

            if self.path == "/strength":
                result = self._handle_strength(body)
                self._json_response(200, result)

            elif self.path == "/waveform":
                result = self._handle_waveform(body)
                self._json_response(200, result)

            elif self.path == "/clear":
                channel = body.get("channel", "A")
                self._run_async(self.session.clear_channel(channel))
                self._json_response(200, {"ok": True, "action": f"Cleared channel {channel}"})

            elif self.path == "/emergency-stop":
                self._run_async(self.session.emergency_stop())
                self._json_response(200, {"ok": True, "action": "Emergency stop executed"})

            elif self.path == "/stop":
                self._json_response(200, {"ok": True, "action": "Shutting down"})
                self.session.request_stop()
                self.server_shutdown.set()

            else:
                self._json_response(404, {"error": f"Unknown endpoint: {self.path}"})

        except (ValueError, RuntimeError) as e:
            self._json_response(400, {"error": str(e)})
        except Exception as e:
            logger.exception("API error")
            self._json_response(500, {"error": str(e)})

    def _handle_strength(self, body: dict) -> dict:
        channel = body.get("channel", "A")
        action = body.get("action", "set")
        value = int(body.get("value", 1))

        self._run_async(self.session.send_strength(channel, action, value))
        return {
            "ok": True,
            "action": f"strength {action}",
            "channel": channel,
            "value": value,
        }

    def _handle_waveform(self, body: dict) -> dict:
        channel = body.get("channel", "A")
        duration = int(body.get("duration", 5))
        preset = body.get("preset")
        data = body.get("data")

        if preset:
            data = get_preset(preset)
        elif data:
            validate_hex_data(data)
        else:
            raise ValueError("Provide 'preset' name or 'data' array of HEX entries")

        self._run_async(self.session.send_waveform(channel, data, duration))
        return {
            "ok": True,
            "channel": channel,
            "preset": preset,
            "entries": len(data),
            "duration": duration,
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_http_server(port: int, session: DGLabSession, loop: asyncio.AbstractEventLoop,
                    shutdown_event: threading.Event):
    handler = partial(APIHandler)
    handler.session = session
    handler.loop = loop
    handler.server_shutdown = shutdown_event

    # Attach class-level attributes
    APIHandler.session = session
    APIHandler.loop = loop
    APIHandler.server_shutdown = shutdown_event

    httpd = HTTPServer(("127.0.0.1", port), APIHandler)
    httpd.timeout = 1
    logger.info("HTTP API listening on http://127.0.0.1:%d", port)
    while not shutdown_event.is_set():
        httpd.handle_request()
    httpd.server_close()


def main():
    parser = argparse.ArgumentParser(description="DG-LAB WebSocket Controller")
    parser.add_argument("--ws-url", required=True, help="WebSocket relay server URL (e.g. ws://localhost:9999)")
    parser.add_argument("--port", type=int, default=8899, help="Local HTTP API port (default: 8899)")
    parser.add_argument("--strength-limit", type=int, default=50, help="Safety strength limit 0-200 (default: 50)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    safety = SafetyGuard(strength_limit=args.strength_limit)
    session = DGLabSession(ws_url=args.ws_url, safety=safety)
    shutdown_event = threading.Event()

    loop = asyncio.new_event_loop()

    def ws_thread():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session.run())

    ws_t = threading.Thread(target=ws_thread, daemon=True)
    ws_t.start()

    # Allow WS to connect before starting HTTP
    time.sleep(1)

    def sig_handler(sig, frame):
        logger.info("Signal %s received, shutting down...", sig)
        session.request_stop()
        shutdown_event.set()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    logger.info("=== DG-LAB Controller ===")
    logger.info("WS Server : %s", args.ws_url)
    logger.info("HTTP API  : http://127.0.0.1:%d", args.port)
    logger.info("Strength  : limit=%d", safety.strength_limit)
    logger.info("========================")

    try:
        run_http_server(args.port, session, loop, shutdown_event)
    except KeyboardInterrupt:
        pass
    finally:
        session.request_stop()
        shutdown_event.set()
        loop.call_soon_threadsafe(loop.stop)
        ws_t.join(timeout=5)
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    main()
