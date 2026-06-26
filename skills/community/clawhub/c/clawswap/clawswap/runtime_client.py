#!/usr/bin/env python3
"""
ClawSwap Self-Hosted Runtime Client
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Speaks the /runtime/v1/* protocol to connect a self-hosted agent to ClawSwap.

Lifecycle:
  A. Auto-register (if API key provided and no saved state):
     1. Create self-hosted paper agent via POST /api/v1/agents
     2. Issue bootstrap token via POST /api/v1/agents/:id/bootstrap
  B. Bootstrap exchange: swap clsw_bt_* token for clsw_rt_* runtime token
  C. Heartbeat loop (every 30s)
  D. Telemetry reports (every 60s)
  E. Strategy loop → trade intents via POST /runtime/v1/trade

Usage:
    # Auto-register with API key (creates agent + bootstraps automatically):
    python3 runtime_client.py --api-key clsw_xxxxx

    # Or via env var:
    CLAWSWAP_API_KEY=clsw_xxxxx python3 runtime_client.py

    # Manual bootstrap (from dashboard):
    python3 runtime_client.py --agent-id agt_xxx --bootstrap-token clsw_bt_xxx

    # Reconnect with saved state (auto-detected from .runtime_token):
    python3 runtime_client.py

Environment variables:
    CLAWSWAP_API_KEY           API key from Dashboard Settings (for auto-register)
    CLAWSWAP_GATEWAY_URL       Gateway base URL (default: https://api.clawswap.trade)
    CLAWSWAP_BOOTSTRAP_TOKEN   Bootstrap token for manual bootstrap
    CLAWSWAP_RUNTIME_TOKEN     Runtime token for reconnection
    CLAWSWAP_AGENT_ID          Agent ID
"""

import argparse
import json
import logging
import os
import platform
import random
import signal
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("clawswap.runtime")

RUNTIME_VERSION = "0.2.0"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SKILL_DIR, ".runtime_token")
API_KEY_FILE = os.path.join(SKILL_DIR, ".clawswap_api_key")


# ── Strategy Adapter ────────────────────────────────────────────────────────

class DemoStrategy:
    """Simple demo strategy: alternates buy/sell on a single ticker.

    Produces one trade intent per tick. Cycles through:
      1. Buy ticker with size_pct of cash
      2. Wait (hold)
      3. Sell (close position)
      4. Wait (hold)
    """

    def __init__(self, ticker="BTC", size_pct=0.1, interval=30):
        self.ticker = ticker.upper()
        self.size_pct = size_pct
        self.interval = interval  # seconds between strategy ticks
        self.tick_count = 0
        self.in_position = False
        self._trade_counter = 0

    def tick(self):
        """Called every `interval` seconds. Returns list of trade intents."""
        self.tick_count += 1
        intents = []

        # Simple cycle: buy on tick 1, sell on tick 3, repeat every 4 ticks
        phase = self.tick_count % 4

        if phase == 1 and not self.in_position:
            self._trade_counter += 1
            intents.append({
                "ticker": self.ticker,
                "side": "buy",
                "size_pct": self.size_pct,
                "client_order_id": f"demo_{self._trade_counter:04d}",
            })
            self.in_position = True
        elif phase == 3 and self.in_position:
            self._trade_counter += 1
            intents.append({
                "ticker": self.ticker,
                "side": "sell",
                "client_order_id": f"demo_{self._trade_counter:04d}",
            })
            self.in_position = False

        return intents


class LiveStrategyAdapter:
    """Adapts a strategies/ class (on_candle/get_signal/get_exit_signal) to the
    tick() interface used by RuntimeClient.

    Fetches real-time mid-price from Hyperliquid on each tick, feeds it as a
    candle, and converts signals to trade intents.
    """

    def __init__(self, strategy, cfg, ticker="BTC", interval=30):
        self.strategy = strategy
        self.cfg = cfg
        self.ticker = ticker.upper()
        self.interval = interval
        self.in_position = False
        self.position_side = None
        self._trade_counter = 0

    def _get_price(self):
        """Fetch live mid-price from Hyperliquid."""
        try:
            data = json.dumps({"type": "allMids"}).encode()
            req = Request(
                "https://api.hyperliquid.xyz/info",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "ClawSwap-RuntimeClient/1.0",
                },
                method="POST",
            )
            with urlopen(req, timeout=10) as resp:
                mids = json.load(resp)
            price_str = mids.get(self.ticker)
            if price_str:
                return float(price_str)
        except Exception as e:
            log.debug(f"Price fetch failed: {e}")
        return 0.0

    def tick(self):
        """Fetch price, feed candle, check signals, return trade intents."""
        price = self._get_price()
        if price <= 0:
            return []

        candle = {
            "open": price, "high": price, "low": price,
            "close": price, "volume": 0,
        }
        if hasattr(self.strategy, "on_candle"):
            self.strategy.on_candle(candle)

        intents = []
        self._trade_counter += 1
        coid = f"live_{self._trade_counter:04d}"

        if not self.in_position:
            sig = self.strategy.get_signal() if hasattr(self.strategy, "get_signal") else None
            if sig == "sell" and getattr(self.cfg, "direction", None) == "short":
                sig = "short"
            if sig in ("buy", "short"):
                size_pct = getattr(self.cfg, "position_size_pct", 0.2)
                intents.append({
                    "ticker": self.ticker,
                    "side": sig,
                    "size_pct": size_pct,
                    "client_order_id": coid,
                })
                self.in_position = True
                self.position_side = "long" if sig == "buy" else "short"
                if hasattr(self.strategy, "on_fill"):
                    self.strategy.on_fill(sig, price, coid)
        else:
            exit_sig = self.strategy.get_exit_signal(price) if hasattr(self.strategy, "get_exit_signal") else None
            if exit_sig:
                close_side = "cover" if self.position_side == "short" else "sell"
                intents.append({
                    "ticker": self.ticker,
                    "side": close_side,
                    "client_order_id": coid,
                })
                self.in_position = False
                self.position_side = None
                if hasattr(self.strategy, "on_fill"):
                    self.strategy.on_fill(close_side, price, coid)

        return intents


class RandomStrategy:
    """Random walk strategy for testing: randomly opens/closes positions on multiple tickers."""

    def __init__(self, tickers=None, size_pct=0.05, interval=20):
        self.tickers = [t.upper() for t in (tickers or ["BTC", "ETH"])]
        self.size_pct = size_pct
        self.interval = interval
        self.positions = set()  # tickers currently held
        self._trade_counter = 0

    def tick(self):
        """Called every `interval` seconds. Returns list of trade intents."""
        intents = []
        ticker = random.choice(self.tickers)
        self._trade_counter += 1
        coid = f"rand_{self._trade_counter:04d}"

        if ticker in self.positions:
            # 60% chance to close
            if random.random() < 0.6:
                intents.append({"ticker": ticker, "side": "sell", "client_order_id": coid})
                self.positions.discard(ticker)
        else:
            # 40% chance to open
            if random.random() < 0.4:
                side = random.choice(["buy", "short"])
                intents.append({
                    "ticker": ticker,
                    "side": side,
                    "size_pct": self.size_pct,
                    "client_order_id": coid,
                })
                self.positions.add(ticker)

        return intents


def http_json(method, url, data=None, token=None, timeout=15):
    """Send an HTTP request and return (status_code, response_body_dict | None)."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ClawSwap-RuntimeClient/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, json.load(resp)
    except HTTPError as e:
        try:
            err_body = json.loads(e.read().decode())
        except Exception:
            err_body = None
        return e.code, err_body
    except (URLError, Exception) as e:
        log.warning(f"Request failed: {e}")
        return 0, None


def get_host_fingerprint():
    """Generate a simple host fingerprint for the bootstrap exchange."""
    return f"{platform.node()}/{platform.system()}/{platform.machine()}"


class ControlPlaneError(RuntimeError):
    """Error from a control-plane API call, carrying the HTTP status code."""

    def __init__(self, message, status=0):
        super().__init__(message)
        self.status = status


# ── Control Plane Client ──────────────────────────────────────────────────

class ControlPlaneClient:
    """Uses an API key to call control-plane endpoints (create agent, issue bootstrap)."""

    def __init__(self, api_key, gateway_url):
        self.api_key = api_key
        self.gateway_url = gateway_url.rstrip("/")

    def create_agent(self, name="OpenClaw Agent", strategy_kind="DemoStrategy"):
        """Create a self-hosted paper agent via POST /api/v1/agents.

        Returns (agent_id, response_dict) on success, raises on failure.
        """
        log.info(f"Creating self-hosted paper agent: {name} ({strategy_kind})")

        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/api/v1/agents",
            data={
                "name": name,
                "strategy_kind": strategy_kind,
                "hosting_mode": "self_hosted",
                "runtime_mode": "paper",
                "strategy_source": "self_hosted",
            },
            token=self.api_key,
        )

        if status == 200 and resp:
            agent_id = resp["agent"]["id"]
            log.info(f"Agent created: {agent_id}")
            return agent_id, resp
        elif status == 401:
            raise ControlPlaneError("API key rejected (401). Key may be invalid or revoked.", status=401)
        elif status == 0:
            raise ControlPlaneError("Cannot reach gateway. Check CLAWSWAP_GATEWAY_URL.", status=0)
        else:
            msg = resp.get("error", {}).get("message", str(resp)) if resp else f"HTTP {status}"
            raise ControlPlaneError(f"Agent creation failed: {msg}", status=status)

    def issue_bootstrap(self, agent_id):
        """Issue a bootstrap token via POST /api/v1/agents/:id/bootstrap.

        Returns bootstrap_token on success.
        Raises ControlPlaneError with .status on failure (401, 0, 5xx, etc.).
        """
        log.info(f"Issuing bootstrap token for agent {agent_id}")

        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/api/v1/agents/{agent_id}/bootstrap",
            token=self.api_key,
        )

        if status == 200 and resp:
            bootstrap_token = resp["bootstrap_token"]
            log.info(f"Bootstrap token issued: {bootstrap_token[:16]}...")
            return bootstrap_token
        elif status == 401:
            raise ControlPlaneError("API key rejected (401). Key may be invalid or revoked.", status=401)
        elif status == 0:
            raise ControlPlaneError("Cannot reach gateway. Check CLAWSWAP_GATEWAY_URL.", status=0)
        else:
            msg = resp.get("error", {}).get("message", str(resp)) if resp else f"HTTP {status}"
            raise ControlPlaneError(f"Bootstrap token issuance failed: {msg}", status=status)


class RuntimeClient:
    """Minimal runtime client that speaks the /runtime/v1/* protocol."""

    def __init__(self, agent_id, gateway_url, bootstrap_token=None, runtime_token=None,
                 strategy=None, api_key=None):
        self.agent_id = agent_id
        self.gateway_url = gateway_url.rstrip("/")
        self.bootstrap_token = bootstrap_token
        self.runtime_token = runtime_token
        self.running = False
        self.strategy = strategy
        self.api_key = api_key

        # Intervals (may be overridden by server response)
        self.heartbeat_interval = 30
        self.telemetry_interval = 60

        # Simulated telemetry values
        self.equity = 10000.0
        self.pnl_pct = 0.0

        # Trade failure tracking — consecutive failures trigger degraded mode
        self.consecutive_trade_failures = 0
        self.max_consecutive_failures = 5  # enter degraded mode after this many
        self.degraded = False

    def bootstrap_exchange(self):
        """Exchange bootstrap token for a runtime token via POST /runtime/v1/bootstrap."""
        if not self.bootstrap_token:
            log.error("No bootstrap token available")
            return False

        log.info(f"Exchanging bootstrap token ({self.bootstrap_token[:16]}...)")

        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/runtime/v1/bootstrap",
            data={
                "agent_id": self.agent_id,
                "runtime_version": RUNTIME_VERSION,
                "host_fingerprint": get_host_fingerprint(),
            },
            token=self.bootstrap_token,
        )

        if status == 200 and resp:
            self.runtime_token = resp["runtime_token"]
            self.bootstrap_token = None  # consumed

            # Server may override intervals
            self.heartbeat_interval = resp.get("heartbeat_interval_sec", 30)
            self.telemetry_interval = resp.get("telemetry_interval_sec", 60)

            config = resp.get("config", {})
            log.info(f"Bootstrap exchange OK")
            log.info(f"  Runtime token: {self.runtime_token[:16]}...")
            log.info(f"  Strategy: {config.get('strategy_kind', '?')}")
            log.info(f"  Heartbeat: {self.heartbeat_interval}s, Telemetry: {self.telemetry_interval}s")

            self._save_token()
            return True
        else:
            msg = resp.get("error", {}).get("message", str(resp)) if resp else f"HTTP {status}"
            log.error(f"Bootstrap exchange failed: {msg}")
            return False

    def auto_register(self, name="OpenClaw Agent", strategy_kind="DemoStrategy"):
        """Auto-register: create agent + issue bootstrap + exchange.

        Uses the API key to call control-plane, then bootstraps into runtime mode.
        Persists agent_id immediately after creation so that a failed bootstrap
        exchange does not cause orphan agents on retry.
        Returns True on success.
        """
        if not self.api_key:
            log.error("No API key available for auto-registration")
            return False

        cp = ControlPlaneClient(self.api_key, self.gateway_url)

        # Step 1: Create agent
        agent_id, _ = cp.create_agent(name=name, strategy_kind=strategy_kind)
        self.agent_id = agent_id

        # Persist agent_id immediately so retries reuse it instead of creating again
        self._save_partial_state()

        # Step 2: Issue bootstrap token
        bootstrap_token = cp.issue_bootstrap(agent_id)
        self.bootstrap_token = bootstrap_token

        # Step 3: Exchange bootstrap for runtime token
        return self.bootstrap_exchange()

    def send_heartbeat(self):
        """Send heartbeat via POST /runtime/v1/heartbeat."""
        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/runtime/v1/heartbeat",
            data={"agent_id": self.agent_id},
            token=self.runtime_token,
        )

        if status == 200:
            log.debug("Heartbeat OK")
            return True
        elif status == 401:
            log.warning("Heartbeat rejected (401) — token may be revoked or rotated")
            return False
        else:
            log.warning(f"Heartbeat failed: HTTP {status}")
            return True  # transient error, keep trying

    def send_telemetry(self):
        """Send telemetry via POST /runtime/v1/telemetry."""
        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/runtime/v1/telemetry",
            data={
                "agent_id": self.agent_id,
                "current_equity": round(self.equity, 2),
                "current_pnl_pct": round(self.pnl_pct, 4),
            },
            token=self.runtime_token,
        )

        if status == 200:
            log.debug("Telemetry OK")
            return True
        elif status == 401:
            log.warning("Telemetry rejected (401) — token may be revoked")
            return False
        else:
            log.warning(f"Telemetry failed: HTTP {status}")
            return True

    def send_event(self, event_type, payload=None):
        """Send a discrete event via POST /runtime/v1/events."""
        status, resp = http_json(
            "POST",
            f"{self.gateway_url}/runtime/v1/events",
            data={
                "agent_id": self.agent_id,
                "event_type": event_type,
                "payload": payload or {},
            },
            token=self.runtime_token,
        )

        if status == 200:
            log.info(f"Event sent: {event_type}")
            return True
        elif status == 401:
            log.warning("Event rejected (401)")
            return False
        else:
            log.warning(f"Event failed: HTTP {status}")
            return True

    def submit_trade(self, ticker, side, size_pct=None, leverage=None, client_order_id=None):
        """Submit a trade intent via POST /runtime/v1/trade.

        Args:
            ticker: e.g. "BTC", "ETH"
            side: "buy" (open long), "short" (open short), "sell" (close long), "cover" (close short)
            size_pct: fraction of cash to use (0.01–1.0), only for opens
            leverage: optional leverage override
            client_order_id: optional client-supplied ID for tracing

        Returns:
            (ok: bool, fill_result: dict | None)
            ok=False means token revoked — caller should stop.
            ok=True means continue (even on trade rejection).
        """
        if self.degraded:
            log.warning("Skipping trade — in degraded mode due to consecutive failures")
            return True, None

        data = {
            "agent_id": self.agent_id,
            "ticker": ticker,
            "side": side,
        }
        if size_pct is not None:
            data["size_pct"] = size_pct
        if leverage is not None:
            data["leverage"] = leverage
        if client_order_id is not None:
            data["client_order_id"] = client_order_id

        for attempt in range(3):
            status, resp = http_json(
                "POST",
                f"{self.gateway_url}/runtime/v1/trade",
                data=data,
                token=self.runtime_token,
            )

            if status == 200 and resp:
                fill = resp.get("fill", {})
                log.info(
                    f"Trade filled: {side} {ticker} | "
                    f"price={fill.get('price', '?')} size={fill.get('size', '?')} "
                    f"pnl={fill.get('pnl', '-')} | "
                    f"equity={resp.get('equity_after', '?')}"
                )
                self.equity = resp.get("equity_after", self.equity)
                self.consecutive_trade_failures = 0
                return True, resp
            elif status == 401:
                log.warning("Trade rejected (401) — token revoked")
                return False, resp
            elif status == 400:
                # Business logic rejection (duplicate position, no cash, etc.)
                # Not a failure — reset counter, don't retry
                msg = resp.get("error", {}).get("message", str(resp)) if resp else f"HTTP {status}"
                log.warning(f"Trade rejected (400): {msg}")
                self.consecutive_trade_failures = 0
                return True, resp
            elif status == 0 and attempt < 2:
                log.warning(f"Trade request failed, retrying ({attempt + 1}/3)...")
                time.sleep(2 ** attempt)
                continue
            else:
                # 5xx or final network failure
                self.consecutive_trade_failures += 1
                log.error(
                    f"Trade failed: HTTP {status} "
                    f"(consecutive failures: {self.consecutive_trade_failures}/{self.max_consecutive_failures})"
                )
                if self.consecutive_trade_failures >= self.max_consecutive_failures:
                    self.degraded = True
                    log.error("Entering DEGRADED mode — strategy trading suspended")
                    self.send_event("trade_submission_degraded", {
                        "consecutive_failures": self.consecutive_trade_failures,
                        "last_status": status,
                        "ticker": ticker,
                        "side": side,
                    })
                return True, resp

        # All retries exhausted
        self.consecutive_trade_failures += 1
        log.error(
            f"Trade failed after 3 retries "
            f"(consecutive failures: {self.consecutive_trade_failures}/{self.max_consecutive_failures})"
        )
        if self.consecutive_trade_failures >= self.max_consecutive_failures:
            self.degraded = True
            log.error("Entering DEGRADED mode — strategy trading suspended")
            self.send_event("trade_submission_degraded", {
                "consecutive_failures": self.consecutive_trade_failures,
                "ticker": ticker,
                "side": side,
            })
        return True, None

    def _attempt_reconnect(self):
        """Attempt to reconnect after a 401 (token rotated or revoked).

        If an API key is available, tries to issue a new bootstrap token and
        exchange it.

        Returns:
            True  — reconnect succeeded, caller should continue running.
            False — reconnect failed permanently (401); caller should clear state and exit.
            None  — reconnect failed transiently; caller should exit but preserve state.
        """
        if not self.api_key:
            return False

        log.info("Attempting reconnect with API key...")
        self.runtime_token = None
        cp = ControlPlaneClient(self.api_key, self.gateway_url)

        try:
            bootstrap_token = cp.issue_bootstrap(self.agent_id)
            self.bootstrap_token = bootstrap_token
            if self.bootstrap_exchange():
                log.info("Reconnect successful — runtime token refreshed")
                self.degraded = False
                self.consecutive_trade_failures = 0
                self.send_event("runtime_reconnected", {"version": RUNTIME_VERSION})
                return True
        except ControlPlaneError as e:
            if e.status == 401:
                log.error(f"Reconnect failed (permanent): {e}")
                return False
            log.error(f"Reconnect failed (transient): {e}")
            return None
        except RuntimeError as e:
            log.error(f"Reconnect failed: {e}")
            return None

        return None

    def run(self):
        """Main loop: heartbeat + telemetry + strategy."""
        # Step 1: get a runtime token (bootstrap or existing)
        if not self.runtime_token:
            if not self.bootstrap_exchange():
                log.error("Cannot start without a runtime token. Exiting.")
                sys.exit(1)
        else:
            log.info(f"Using existing runtime token ({self.runtime_token[:16]}...)")

        self.running = True
        log.info("=" * 50)
        log.info(f"Runtime client ONLINE — agent {self.agent_id}")
        log.info(f"  Gateway: {self.gateway_url}")
        log.info(f"  Strategy: {self.strategy.__class__.__name__ if self.strategy else 'none'}")
        log.info(f"  Heartbeat: {self.heartbeat_interval}s, Telemetry: {self.telemetry_interval}s")
        log.info("=" * 50)

        # Send startup event
        self.send_event("runtime_started", {"version": RUNTIME_VERSION})

        last_heartbeat = 0.0
        last_telemetry = 0.0
        last_strategy = 0.0

        while self.running:
            now = time.time()

            # Heartbeat
            if now - last_heartbeat >= self.heartbeat_interval:
                if not self.send_heartbeat():
                    # Token rejected — try to reconnect if we have an API key
                    reconnect = self._attempt_reconnect()
                    if reconnect is True:
                        last_heartbeat = now
                        continue
                    if reconnect is False:
                        # 401 — agent permanently revoked; clear state for fresh start
                        log.error("Agent permanently rejected. Clearing state.")
                        _clear_saved_state()
                    else:
                        # Transient failure — preserve state for retry
                        log.error("Reconnect failed (transient). Retry later.")
                    sys.exit(1)
                last_heartbeat = now

            # Strategy tick
            if self.strategy and now - last_strategy >= self.strategy.interval:
                intents = self.strategy.tick()
                for intent in intents:
                    ok, resp = self.submit_trade(
                        ticker=intent["ticker"],
                        side=intent["side"],
                        size_pct=intent.get("size_pct"),
                        client_order_id=intent.get("client_order_id"),
                    )
                    if not ok:
                        # Token rejected — try to reconnect
                        reconnect = self._attempt_reconnect()
                        if reconnect is True:
                            break  # skip remaining intents, resume on next tick
                        if reconnect is False:
                            log.error("Agent permanently rejected. Clearing state.")
                            _clear_saved_state()
                        else:
                            log.error("Reconnect failed (transient). Retry later.")
                        sys.exit(1)
                last_strategy = now

            # Telemetry
            if now - last_telemetry >= self.telemetry_interval:
                self.send_telemetry()
                last_telemetry = now

            time.sleep(min(self.heartbeat_interval, self.strategy.interval if self.strategy else 10, 10))

        log.info("Runtime client stopped")

    def stop(self):
        """Signal the main loop to stop."""
        self.running = False

    def _save_partial_state(self):
        """Persist agent_id + gateway_url without runtime_token.

        Called immediately after create_agent() so that if bootstrap_exchange()
        fails, the next startup will reuse this agent_id instead of creating
        another one (avoiding orphan agents).
        """
        try:
            data = {
                "agent_id": self.agent_id,
                "gateway_url": self.gateway_url,
            }
            # Preserve existing runtime_token if present
            existing = load_saved_token() or {}
            if existing.get("runtime_token"):
                data["runtime_token"] = existing["runtime_token"]
            with open(TOKEN_FILE, "w") as f:
                json.dump(data, f, indent=2)
            os.chmod(TOKEN_FILE, 0o600)
            log.info(f"Agent state saved (agent_id={self.agent_id})")
        except Exception as e:
            log.warning(f"Could not save partial state: {e}")

    def _save_token(self):
        """Persist runtime token to disk for reconnection."""
        try:
            data = {
                "agent_id": self.agent_id,
                "runtime_token": self.runtime_token,
                "gateway_url": self.gateway_url,
            }
            with open(TOKEN_FILE, "w") as f:
                json.dump(data, f, indent=2)
            os.chmod(TOKEN_FILE, 0o600)
            log.info(f"Runtime token saved to {TOKEN_FILE}")
        except Exception as e:
            log.warning(f"Could not save token: {e}")

    def _remove_token(self):
        """Clear runtime_token from state file (after revocation).

        Preserves agent_id so the next startup can re-bootstrap the same agent
        instead of creating a new one.
        """
        try:
            if os.path.exists(TOKEN_FILE):
                existing = load_saved_token() or {}
                agent_id = existing.get("agent_id")
                gateway_url = existing.get("gateway_url")
                if agent_id:
                    # Keep agent_id, clear runtime_token
                    with open(TOKEN_FILE, "w") as f:
                        json.dump({"agent_id": agent_id, "gateway_url": gateway_url}, f, indent=2)
                    log.info(f"Runtime token cleared, agent_id preserved ({agent_id})")
                else:
                    os.remove(TOKEN_FILE)
        except Exception:
            pass


def load_saved_token():
    """Load previously saved runtime token from disk."""
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return None


def _clear_saved_state():
    """Remove the saved state file entirely (agent_id + runtime_token).

    Used when a saved agent is permanently unreachable (revoked/deleted) and
    the client needs to fall back to creating a fresh agent on next startup.
    """
    try:
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            log.info(f"Saved state cleared ({TOKEN_FILE})")
    except Exception:
        pass


def load_api_key():
    """Load API key from file (~/.clawswap_api_key or local .clawswap_api_key)."""
    try:
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE) as f:
                key = f.read().strip()
                if key:
                    return key
    except Exception:
        pass
    return None


def save_api_key(api_key):
    """Persist API key to file for future use."""
    try:
        with open(API_KEY_FILE, "w") as f:
            f.write(api_key)
        os.chmod(API_KEY_FILE, 0o600)
        log.info(f"API key saved to {API_KEY_FILE}")
    except Exception as e:
        log.warning(f"Could not save API key: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="ClawSwap Self-Hosted Runtime Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--api-key", help="API key from Dashboard Settings (or CLAWSWAP_API_KEY env)")
    parser.add_argument("--agent-id", help="Agent ID (or CLAWSWAP_AGENT_ID env)")
    parser.add_argument("--agent-name", default="OpenClaw Agent", help="Agent name for auto-registration")
    parser.add_argument("--gateway", help="Gateway URL (or CLAWSWAP_GATEWAY_URL env)")
    parser.add_argument("--bootstrap-token", help="Bootstrap token (or CLAWSWAP_BOOTSTRAP_TOKEN env)")
    parser.add_argument("--runtime-token", help="Runtime token (or CLAWSWAP_RUNTIME_TOKEN env)")
    parser.add_argument("--strategy", default="demo",
                        help="Strategy: demo | random | none | mean_reversion | momentum | grid | breakout | short_momentum | dual_ma | range_scalper | adaptive (default: demo)")
    parser.add_argument("--ticker", default="BTC", help="Ticker for demo strategy (default: BTC)")
    parser.add_argument("--strategy-interval", type=int, default=30,
                        help="Seconds between strategy ticks (default: 30)")
    args = parser.parse_args()

    # Load .env files: local .env (skill root) then gateway/tests/.env.e2e
    # Later files do NOT override earlier ones or real env vars.
    env_files = [
        os.path.join(SKILL_DIR, ".env"),
        os.path.join(SKILL_DIR, "..", "..", "gateway", "tests", ".env.e2e"),
    ]
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        if v and k.strip() not in os.environ:
                            os.environ[k.strip()] = v.strip()

    # Resolve from args → env → saved file
    saved = load_saved_token() or {}

    api_key = args.api_key or os.environ.get("CLAWSWAP_API_KEY") or load_api_key()
    agent_id = args.agent_id or os.environ.get("CLAWSWAP_AGENT_ID") or saved.get("agent_id")
    gateway_url = args.gateway or os.environ.get("CLAWSWAP_GATEWAY_URL") or os.environ.get("GATEWAY_URL") or saved.get("gateway_url", "https://api.clawswap.trade")
    bootstrap_token = args.bootstrap_token or os.environ.get("CLAWSWAP_BOOTSTRAP_TOKEN")
    runtime_token = args.runtime_token or os.environ.get("CLAWSWAP_RUNTIME_TOKEN") or saved.get("runtime_token")

    # Persist API key if provided via CLI/env for future runs
    if api_key and not load_api_key():
        save_api_key(api_key)

    # Build strategy
    strategy = None
    strategy_kind = args.strategy
    if args.strategy == "demo":
        strategy = DemoStrategy(ticker=args.ticker, interval=args.strategy_interval)
        strategy_kind = "DemoStrategy"
    elif args.strategy == "random":
        strategy = RandomStrategy(interval=args.strategy_interval)
        strategy_kind = "RandomStrategy"
    elif args.strategy == "none":
        strategy = None
        strategy_kind = "None"
    else:
        # Load a real strategy from strategies/
        try:
            sys.path.insert(0, SKILL_DIR)
            from strategies import STRATEGY_MAP, _ALIAS_DEFAULTS
            if args.strategy not in STRATEGY_MAP:
                log.error(f"Unknown strategy: {args.strategy}. Available: {list(STRATEGY_MAP.keys())}")
                sys.exit(1)
            StratClass, CfgClass = STRATEGY_MAP[args.strategy]
            cfg_kwargs = {"ticker": args.ticker}
            if args.strategy in _ALIAS_DEFAULTS:
                cfg_kwargs.update(_ALIAS_DEFAULTS[args.strategy])
            cfg = CfgClass(**cfg_kwargs)
            strat_instance = StratClass(cfg)
            strategy = LiveStrategyAdapter(
                strat_instance, cfg, ticker=args.ticker, interval=args.strategy_interval,
            )
            strategy_kind = args.strategy
            log.info(f"Loaded strategy: {args.strategy} ({StratClass.__name__})")
        except ImportError as e:
            log.error(f"Cannot load strategy '{args.strategy}': {e}")
            sys.exit(1)

    # ── Path A: auto-register with API key ──────────────────────────────
    # If saved state has agent_id but no runtime_token, skip creation and
    # go to Path B (re-bootstrap) to avoid orphan agent duplication.
    if api_key and not agent_id and not runtime_token and not bootstrap_token:
        log.info("Auto-registration mode: creating agent with API key")
        client = RuntimeClient(
            agent_id="pending",
            gateway_url=gateway_url,
            api_key=api_key,
            strategy=strategy,
        )

        try:
            if not client.auto_register(name=args.agent_name, strategy_kind=strategy_kind):
                log.error("Auto-registration failed. Exiting.")
                sys.exit(1)
        except RuntimeError as e:
            log.error(f"Auto-registration failed: {e}")
            sys.exit(1)

        def _shutdown(sig, frame):
            log.info("Shutdown signal received")
            client.send_event("runtime_stopped", {"reason": "signal"})
            client.stop()

        signal.signal(signal.SIGINT, _shutdown)
        signal.signal(signal.SIGTERM, _shutdown)

        client.run()
        return

    # ── Path B: re-bootstrap existing agent with API key ────────────────
    if api_key and agent_id and not runtime_token and not bootstrap_token:
        log.info(f"Re-bootstrapping agent {agent_id} with API key")
        cp = ControlPlaneClient(api_key, gateway_url)
        try:
            bootstrap_token = cp.issue_bootstrap(agent_id)
        except ControlPlaneError as e:
            if e.status == 401:
                # 401 = API key invalid OR agent revoked/deleted — permanent.
                # Clear saved state and fall back to Path A (create new agent).
                log.warning(f"Agent {agent_id} rejected (401): {e}")
                log.info("Clearing saved agent state and creating a new agent...")
                _clear_saved_state()
                client = RuntimeClient(
                    agent_id="pending",
                    gateway_url=gateway_url,
                    api_key=api_key,
                    strategy=strategy,
                )

                try:
                    if not client.auto_register(name=args.agent_name, strategy_kind=strategy_kind):
                        log.error("Auto-registration failed. Exiting.")
                        sys.exit(1)
                except RuntimeError as e2:
                    log.error(f"Auto-registration failed: {e2}")
                    sys.exit(1)

                def _shutdown(sig, frame):
                    log.info("Shutdown signal received")
                    client.send_event("runtime_stopped", {"reason": "signal"})
                    client.stop()

                signal.signal(signal.SIGINT, _shutdown)
                signal.signal(signal.SIGTERM, _shutdown)

                client.run()
                return
            else:
                # Transient failure (network=0, 5xx, etc.) — keep saved
                # agent_id intact so the next startup retries the same agent.
                log.error(f"Re-bootstrap failed (transient): {e}")
                log.error("Saved agent state preserved. Please retry later.")
                sys.exit(1)

    # ── Path C: manual / reconnect ──────────────────────────────────────
    if not agent_id:
        print("Error: --agent-id or CLAWSWAP_AGENT_ID required (or use --api-key for auto-registration)")
        sys.exit(1)

    if not bootstrap_token and not runtime_token:
        print("Error: need --api-key, --bootstrap-token, or --runtime-token")
        print("  Option 1: Use --api-key (from Dashboard Settings) for auto-registration")
        print("  Option 2: Use --bootstrap-token (from Dashboard Agent Detail)")
        print("  Option 3: Use --runtime-token (from saved state)")
        sys.exit(1)

    client = RuntimeClient(
        agent_id=agent_id,
        gateway_url=gateway_url,
        bootstrap_token=bootstrap_token,
        runtime_token=runtime_token,
        strategy=strategy,
        api_key=api_key,
    )

    def _shutdown(sig, frame):
        log.info("Shutdown signal received")
        client.send_event("runtime_stopped", {"reason": "signal"})
        client.stop()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    client.run()


if __name__ == "__main__":
    main()
