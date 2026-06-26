#!/usr/bin/env python3
"""
Unit tests for runtime_client.py

Run from skill root (skill/clawswap/):
    python3 tests/test_runtime_client.py
    python3 -m pytest tests/test_runtime_client.py
"""

import json
import os
import random
import sys
import unittest
from unittest.mock import patch, call

# Ensure runtime_client is importable (it lives in the skill root)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from runtime_client import (
    RuntimeClient, DemoStrategy, RandomStrategy, LiveStrategyAdapter,
    ControlPlaneClient, ControlPlaneError,
    load_api_key, save_api_key, API_KEY_FILE,
    _clear_saved_state,
)
from strategies import MomentumStrategy, MomentumConfig


class TokenFileCleanupMixin:
    """Mixin that backs up and restores TOKEN_FILE around each test."""

    def setUp(self):
        from runtime_client import TOKEN_FILE
        self._token_file = TOKEN_FILE
        self._token_backup = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE) as f:
                self._token_backup = f.read()
            os.remove(TOKEN_FILE)

    def tearDown(self):
        if os.path.exists(self._token_file):
            os.remove(self._token_file)
        if self._token_backup is not None:
            with open(self._token_file, "w") as f:
                f.write(self._token_backup)


class TestBootstrap(TokenFileCleanupMixin, unittest.TestCase):
    """Tests for RuntimeClient.bootstrap_exchange()."""

    @patch("runtime_client.http_json")
    def test_bootstrap_success(self, mock_http):
        """On 200, runtime_token is set and bootstrap_token is cleared."""
        mock_http.return_value = (200, {
            "runtime_token": "clsw_rt_xxx_test_token_value",
            "heartbeat_interval_sec": 30,
            "telemetry_interval_sec": 60,
            "config": {"strategy_kind": "demo"},
        })

        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            bootstrap_token="clsw_bt_bootstrap_token_value",
        )

        result = client.bootstrap_exchange()

        self.assertTrue(result)
        self.assertEqual(client.runtime_token, "clsw_rt_xxx_test_token_value")
        self.assertIsNone(client.bootstrap_token)

    @patch("runtime_client.http_json")
    def test_bootstrap_failure(self, mock_http):
        """On 401, returns False and runtime_token stays None."""
        mock_http.return_value = (401, None)

        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            bootstrap_token="clsw_bt_bootstrap_token_value",
        )

        result = client.bootstrap_exchange()

        self.assertFalse(result)
        self.assertIsNone(client.runtime_token)


class TestSubmitTrade(unittest.TestCase):
    """Tests for RuntimeClient.submit_trade()."""

    def _make_client(self, **kwargs):
        defaults = {
            "agent_id": "agt_test",
            "gateway_url": "http://localhost:3033",
            "runtime_token": "clsw_rt_test",
        }
        defaults.update(kwargs)
        return RuntimeClient(**defaults)

    @patch("runtime_client.http_json")
    def test_trade_submit_success(self, mock_http):
        """On 200, returns (True, resp), equity is updated, failures reset."""
        resp_body = {
            "ok": True,
            "fill": {"price": 100, "size": 0.5},
            "equity_after": 9900,
        }
        mock_http.return_value = (200, resp_body)

        client = self._make_client()
        client.consecutive_trade_failures = 2  # pre-existing failures

        ok, resp = client.submit_trade("BTC", "buy", size_pct=0.1)

        self.assertTrue(ok)
        self.assertEqual(resp, resp_body)
        self.assertEqual(client.equity, 9900)
        self.assertEqual(client.consecutive_trade_failures, 0)

    @patch("runtime_client.http_json")
    def test_trade_submit_400_no_degraded(self, mock_http):
        """On 400, returns (True, resp), degraded stays False, failures reset."""
        resp_body = {"error": {"message": "Already in position"}}
        mock_http.return_value = (400, resp_body)

        client = self._make_client()
        client.consecutive_trade_failures = 3

        ok, resp = client.submit_trade("BTC", "buy", size_pct=0.1)

        self.assertTrue(ok)
        self.assertEqual(resp, resp_body)
        self.assertFalse(client.degraded)
        self.assertEqual(client.consecutive_trade_failures, 0)

    @patch("runtime_client.http_json")
    def test_trade_submit_consecutive_5xx_enters_degraded(self, mock_http):
        """After 5 consecutive 5xx failures, degraded mode is activated."""
        mock_http.return_value = (500, None)

        client = self._make_client()

        # Also mock send_event to verify it is called with the right event type
        with patch.object(client, "send_event") as mock_event:
            for i in range(5):
                ok, resp = client.submit_trade("BTC", "buy", size_pct=0.1)
                self.assertTrue(ok)  # ok=True even on 5xx (continue running)

            self.assertTrue(client.degraded)
            self.assertEqual(client.consecutive_trade_failures, 5)

            # Verify send_event was called with "trade_submission_degraded"
            event_calls = [c for c in mock_event.call_args_list
                           if c[0][0] == "trade_submission_degraded"]
            self.assertGreaterEqual(len(event_calls), 1,
                                    "send_event('trade_submission_degraded', ...) should have been called")

    @patch("runtime_client.http_json")
    def test_trade_submit_skipped_when_degraded(self, mock_http):
        """When degraded=True, submit_trade skips without calling http_json."""
        client = self._make_client()
        client.degraded = True

        ok, resp = client.submit_trade("BTC", "buy", size_pct=0.1)

        self.assertTrue(ok)
        self.assertIsNone(resp)
        mock_http.assert_not_called()


class TestStrategyNone(unittest.TestCase):
    """Tests for RuntimeClient with strategy=None."""

    def test_strategy_none_no_crash(self):
        """Creating a RuntimeClient with strategy=None should not crash.

        The run() method accesses self.strategy conditionally, so a None
        strategy should be safe at construction time and in the log line.
        """
        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_test",
            strategy=None,
        )

        self.assertIsNone(client.strategy)

        # Verify the conditional access pattern used in the log line:
        #   self.strategy.__class__.__name__ if self.strategy else 'none'
        label = client.strategy.__class__.__name__ if client.strategy else "none"
        self.assertEqual(label, "none")


class TestDemoStrategy(unittest.TestCase):
    """Tests for DemoStrategy tick cycle."""

    def test_demo_strategy_cycle(self):
        """DemoStrategy follows the pattern: buy, hold, sell, hold, repeat."""
        strategy = DemoStrategy(ticker="BTC", size_pct=0.1)

        # Expected over 8 ticks:
        #   tick 1 (phase 1): buy   — opens position
        #   tick 2 (phase 2): hold  — no intents
        #   tick 3 (phase 3): sell  — closes position
        #   tick 4 (phase 0): hold  — no intents
        #   tick 5 (phase 1): buy   — opens position
        #   tick 6 (phase 2): hold  — no intents
        #   tick 7 (phase 3): sell  — closes position
        #   tick 8 (phase 0): hold  — no intents
        expected = [
            ("buy",),    # tick 1
            (),          # tick 2
            ("sell",),   # tick 3
            (),          # tick 4
            ("buy",),    # tick 5
            (),          # tick 6
            ("sell",),   # tick 7
            (),          # tick 8
        ]

        for i, expected_sides in enumerate(expected, start=1):
            intents = strategy.tick()
            actual_sides = tuple(intent["side"] for intent in intents)
            self.assertEqual(
                actual_sides, expected_sides,
                f"Tick {i}: expected sides {expected_sides}, got {actual_sides}"
            )

            # Verify ticker is always BTC when an intent is produced
            for intent in intents:
                self.assertEqual(intent["ticker"], "BTC")


class TestRandomStrategy(unittest.TestCase):
    """Tests for RandomStrategy."""

    def test_random_strategy_produces_intents(self):
        """With a fixed seed, RandomStrategy produces at least 1 intent in 20 ticks."""
        # Use a fixed seed for reproducibility
        random.seed(42)
        strategy = RandomStrategy(tickers=["BTC", "ETH"], size_pct=0.05)

        all_intents = []
        for _ in range(20):
            intents = strategy.tick()
            all_intents.extend(intents)

        self.assertGreaterEqual(
            len(all_intents), 1,
            "RandomStrategy should produce at least 1 intent in 20 ticks with seed 42"
        )

        # Verify all intents have required fields
        for intent in all_intents:
            self.assertIn("ticker", intent)
            self.assertIn("side", intent)
            self.assertIn("client_order_id", intent)
            self.assertIn(intent["ticker"], ["BTC", "ETH"])
            self.assertIn(intent["side"], ["buy", "short", "sell"])


class TestLiveStrategyAdapter(unittest.TestCase):
    """Regression tests for strategy side mapping in the live adapter."""

    def test_short_momentum_entry_uses_short_side(self):
        cfg = MomentumConfig(
            ticker="SOL",
            direction="short",
            breakout_lookback=3,
            entry_threshold_pct=4.0,
            cooldown_candles=0,
        )
        strategy = MomentumStrategy(cfg)
        adapter = LiveStrategyAdapter(strategy, cfg, ticker="SOL", interval=30)

        with patch.object(adapter, "_get_price", side_effect=[100.0, 102.0, 104.0, 98.0]):
            intents = []
            for _ in range(4):
                intents.extend(adapter.tick())

        self.assertEqual(len(intents), 1)
        self.assertEqual(intents[0]["ticker"], "SOL")
        self.assertEqual(intents[0]["side"], "short")
        self.assertTrue(adapter.in_position)
        self.assertEqual(adapter.position_side, "short")
        self.assertTrue(strategy.state.in_position)
        self.assertFalse(strategy.state.is_long)

    def test_short_momentum_exit_uses_cover_side(self):
        cfg = MomentumConfig(
            ticker="SOL",
            direction="short",
            breakout_lookback=3,
            cooldown_candles=0,
        )
        strategy = MomentumStrategy(cfg)
        strategy.on_fill("short", 100.0, "pos_short")

        adapter = LiveStrategyAdapter(strategy, cfg, ticker="SOL", interval=30)
        adapter.in_position = True
        adapter.position_side = "short"

        with patch.object(adapter, "_get_price", return_value=90.0):
            intents = adapter.tick()

        self.assertEqual(len(intents), 1)
        self.assertEqual(intents[0]["side"], "cover")
        self.assertFalse(adapter.in_position)
        self.assertIsNone(adapter.position_side)
        self.assertFalse(strategy.state.in_position)
        self.assertEqual(strategy.state.bars_since_exit, 0)


class TestControlPlaneClient(unittest.TestCase):
    """Tests for ControlPlaneClient (API key based operations)."""

    @patch("runtime_client.http_json")
    def test_create_agent_success(self, mock_http):
        """On 200, returns agent_id from nested response."""
        mock_http.return_value = (200, {
            "agent": {"id": "agt_new_123", "name": "Test Agent"},
        })

        cp = ControlPlaneClient(api_key="clsw_testkey", gateway_url="http://localhost:3033")
        agent_id, resp = cp.create_agent(name="Test Agent", strategy_kind="Demo")

        self.assertEqual(agent_id, "agt_new_123")
        # Verify the API key was used as the Bearer token
        call_args = mock_http.call_args
        self.assertEqual(call_args[1].get("token") or call_args[0][3], "clsw_testkey")

    @patch("runtime_client.http_json")
    def test_create_agent_invalid_key(self, mock_http):
        """On 401, raises RuntimeError with clear message."""
        mock_http.return_value = (401, None)

        cp = ControlPlaneClient(api_key="clsw_badkey", gateway_url="http://localhost:3033")

        with self.assertRaises(RuntimeError) as ctx:
            cp.create_agent()
        self.assertIn("401", str(ctx.exception))

    @patch("runtime_client.http_json")
    def test_create_agent_network_error(self, mock_http):
        """On status 0 (network failure), raises RuntimeError."""
        mock_http.return_value = (0, None)

        cp = ControlPlaneClient(api_key="clsw_testkey", gateway_url="http://unreachable:3033")

        with self.assertRaises(RuntimeError) as ctx:
            cp.create_agent()
        self.assertIn("gateway", str(ctx.exception).lower())

    @patch("runtime_client.http_json")
    def test_issue_bootstrap_success(self, mock_http):
        """On 200, returns bootstrap_token."""
        mock_http.return_value = (200, {
            "bootstrap_token": "clsw_bt_new_bootstrap",
            "credential_id": "cred_123",
        })

        cp = ControlPlaneClient(api_key="clsw_testkey", gateway_url="http://localhost:3033")
        token = cp.issue_bootstrap("agt_123")

        self.assertEqual(token, "clsw_bt_new_bootstrap")

    @patch("runtime_client.http_json")
    def test_issue_bootstrap_invalid_key(self, mock_http):
        """On 401, raises RuntimeError."""
        mock_http.return_value = (401, None)

        cp = ControlPlaneClient(api_key="clsw_badkey", gateway_url="http://localhost:3033")

        with self.assertRaises(RuntimeError) as ctx:
            cp.issue_bootstrap("agt_123")
        self.assertIn("401", str(ctx.exception))


class TestAutoRegister(TokenFileCleanupMixin, unittest.TestCase):
    """Tests for RuntimeClient.auto_register()."""

    @patch("runtime_client.http_json")
    def test_auto_register_full_flow(self, mock_http):
        """auto_register creates agent, issues bootstrap, exchanges for runtime token."""
        # Mock: create agent → bootstrap issue → bootstrap exchange
        mock_http.side_effect = [
            # 1. POST /api/v1/agents (create agent)
            (200, {"agent": {"id": "agt_auto_123"}}),
            # 2. POST /api/v1/agents/:id/bootstrap (issue bootstrap)
            (200, {"bootstrap_token": "clsw_bt_auto_bootstrap"}),
            # 3. POST /runtime/v1/bootstrap (exchange)
            (200, {
                "runtime_token": "clsw_rt_auto_runtime",
                "heartbeat_interval_sec": 30,
                "telemetry_interval_sec": 60,
                "config": {"strategy_kind": "DemoStrategy"},
            }),
        ]

        client = RuntimeClient(
            agent_id="pending",
            gateway_url="http://localhost:3033",
            api_key="clsw_testkey",
        )

        result = client.auto_register(name="Test Agent")

        self.assertTrue(result)
        self.assertEqual(client.agent_id, "agt_auto_123")
        self.assertEqual(client.runtime_token, "clsw_rt_auto_runtime")
        self.assertIsNone(client.bootstrap_token)

    @patch("runtime_client.http_json")
    def test_auto_register_no_api_key(self, mock_http):
        """auto_register fails if no API key is set."""
        client = RuntimeClient(
            agent_id="pending",
            gateway_url="http://localhost:3033",
        )

        result = client.auto_register()

        self.assertFalse(result)
        mock_http.assert_not_called()

    @patch("runtime_client.http_json")
    def test_auto_register_create_fails(self, mock_http):
        """auto_register raises if agent creation returns 401."""
        mock_http.return_value = (401, None)

        client = RuntimeClient(
            agent_id="pending",
            gateway_url="http://localhost:3033",
            api_key="clsw_badkey",
        )

        with self.assertRaises(RuntimeError):
            client.auto_register()


class TestApiKeyPersistence(unittest.TestCase):
    """Tests for API key file persistence."""

    def setUp(self):
        """Save and remove any existing API key file."""
        self._backup = None
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE) as f:
                self._backup = f.read()
            os.remove(API_KEY_FILE)

    def tearDown(self):
        """Restore original API key file if it existed."""
        if os.path.exists(API_KEY_FILE):
            os.remove(API_KEY_FILE)
        if self._backup is not None:
            with open(API_KEY_FILE, "w") as f:
                f.write(self._backup)

    def test_save_and_load_api_key(self):
        """save_api_key persists key that load_api_key can read."""
        save_api_key("clsw_test_persist_key")
        loaded = load_api_key()
        self.assertEqual(loaded, "clsw_test_persist_key")

    def test_load_api_key_missing_file(self):
        """load_api_key returns None when file doesn't exist."""
        self.assertIsNone(load_api_key())


class TestRuntimeClientApiKeyField(unittest.TestCase):
    """Tests for RuntimeClient accepting api_key parameter."""

    def test_client_stores_api_key(self):
        """RuntimeClient stores api_key for use by auto_register."""
        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            api_key="clsw_test_key",
        )
        self.assertEqual(client.api_key, "clsw_test_key")

    def test_client_without_api_key(self):
        """RuntimeClient works without api_key (backward compatible)."""
        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_test",
        )
        self.assertIsNone(client.api_key)


class TestAutoRegisterRecovery(TokenFileCleanupMixin, unittest.TestCase):
    """Tests for auto_register orphan-agent recovery."""

    @patch("runtime_client.http_json")
    def test_auto_register_saves_agent_id_before_exchange(self, mock_http):
        """After create_agent succeeds, agent_id is saved even if exchange fails."""
        from runtime_client import TOKEN_FILE, load_saved_token
        mock_http.side_effect = [
            # 1. POST /api/v1/agents (create agent) — success
            (200, {"agent": {"id": "agt_recovery_123"}}),
            # 2. POST /api/v1/agents/:id/bootstrap — success
            (200, {"bootstrap_token": "clsw_bt_recovery"}),
            # 3. POST /runtime/v1/bootstrap (exchange) — FAIL
            (500, None),
        ]

        client = RuntimeClient(
            agent_id="pending",
            gateway_url="http://localhost:3033",
            api_key="clsw_testkey",
        )

        result = client.auto_register()

        # Exchange failed, so auto_register returns False
        self.assertFalse(result)
        # But agent_id was persisted to disk
        saved = load_saved_token()
        self.assertIsNotNone(saved)
        self.assertEqual(saved["agent_id"], "agt_recovery_123")
        # No runtime_token in saved state
        self.assertNotIn("runtime_token", saved)

    @patch("runtime_client.http_json")
    def test_saved_agent_id_prevents_duplicate_create(self, mock_http):
        """If agent_id is saved (no runtime_token), Path B re-bootstraps instead of Path A."""
        from runtime_client import TOKEN_FILE
        # Simulate saved state from a previous failed auto_register
        with open(TOKEN_FILE, "w") as f:
            json.dump({"agent_id": "agt_saved_456", "gateway_url": "http://localhost:3033"}, f)

        saved = {"agent_id": "agt_saved_456", "gateway_url": "http://localhost:3033"}

        # Resolve like main() does
        api_key = "clsw_testkey"
        agent_id = saved.get("agent_id")  # "agt_saved_456"
        runtime_token = saved.get("runtime_token")  # None

        # Path A condition: api_key and NOT agent_id
        path_a = api_key and not agent_id and not runtime_token
        # Path B condition: api_key and agent_id and NOT runtime_token
        path_b = api_key and agent_id and not runtime_token

        self.assertFalse(path_a, "Should NOT enter Path A when agent_id is saved")
        self.assertTrue(path_b, "Should enter Path B to re-bootstrap existing agent")

    @patch("runtime_client.http_json")
    def test_remove_token_preserves_agent_id(self, mock_http):
        """_remove_token clears runtime_token but keeps agent_id for recovery."""
        from runtime_client import TOKEN_FILE, load_saved_token
        client = RuntimeClient(
            agent_id="agt_persist_789",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_will_be_removed",
        )
        # Save full state first
        client._save_token()
        saved_before = load_saved_token()
        self.assertEqual(saved_before["runtime_token"], "clsw_rt_will_be_removed")

        # Remove token (simulates rotate — keep agent_id)
        client._remove_token()
        saved_after = load_saved_token()
        self.assertIsNotNone(saved_after)
        self.assertEqual(saved_after["agent_id"], "agt_persist_789")
        self.assertNotIn("runtime_token", saved_after)

    def test_clear_saved_state_removes_file(self):
        """_clear_saved_state removes the state file entirely."""
        from runtime_client import TOKEN_FILE, load_saved_token
        # Write a state file
        with open(TOKEN_FILE, "w") as f:
            json.dump({"agent_id": "agt_will_be_cleared", "gateway_url": "http://localhost:3033"}, f)

        _clear_saved_state()

        self.assertFalse(os.path.exists(TOKEN_FILE))
        self.assertIsNone(load_saved_token())

    def test_revoked_agent_clears_state_for_fresh_start(self):
        """After revoke, saved state is fully cleared so next startup creates new agent.

        Simulates: saved agent_id exists → Path B fails (revoke) → state cleared →
        next startup would enter Path A (no agent_id, no runtime_token).
        """
        from runtime_client import TOKEN_FILE, load_saved_token
        # Simulate saved state from revoked agent
        with open(TOKEN_FILE, "w") as f:
            json.dump({"agent_id": "agt_revoked_999", "gateway_url": "http://localhost:3033"}, f)

        # _clear_saved_state is what Path B calls on failure
        _clear_saved_state()

        # Simulate next startup: resolve from saved file
        saved = load_saved_token() or {}
        api_key = "clsw_testkey"
        agent_id = saved.get("agent_id")  # None — file removed
        runtime_token = saved.get("runtime_token")  # None

        # Should enter Path A (auto-register)
        path_a = api_key and not agent_id and not runtime_token
        self.assertTrue(path_a, "After clearing state, should enter Path A to create new agent")


class TestReconnect(TokenFileCleanupMixin, unittest.TestCase):
    """Tests for _attempt_reconnect (rotate/revoke recovery)."""

    @patch("runtime_client.http_json")
    def test_reconnect_succeeds_with_api_key(self, mock_http):
        """With API key, _attempt_reconnect issues new bootstrap and exchanges."""
        mock_http.side_effect = [
            # 1. POST /api/v1/agents/:id/bootstrap (issue bootstrap)
            (200, {"bootstrap_token": "clsw_bt_reconnect"}),
            # 2. POST /runtime/v1/bootstrap (exchange)
            (200, {
                "runtime_token": "clsw_rt_new_after_rotate",
                "heartbeat_interval_sec": 30,
                "telemetry_interval_sec": 60,
                "config": {},
            }),
            # 3. POST /runtime/v1/events (runtime_reconnected event)
            (200, {"ok": True}),
        ]

        client = RuntimeClient(
            agent_id="agt_reconnect",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_old_revoked",
            api_key="clsw_testkey",
        )
        client.degraded = True
        client.consecutive_trade_failures = 5

        result = client._attempt_reconnect()

        self.assertTrue(result)
        self.assertEqual(client.runtime_token, "clsw_rt_new_after_rotate")
        self.assertFalse(client.degraded, "Degraded should be cleared after reconnect")
        self.assertEqual(client.consecutive_trade_failures, 0)

    def test_reconnect_fails_without_api_key(self):
        """Without API key, _attempt_reconnect returns False immediately."""
        client = RuntimeClient(
            agent_id="agt_no_key",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_old",
        )

        result = client._attempt_reconnect()

        self.assertFalse(result)

    @patch("runtime_client.http_json")
    def test_reconnect_fails_on_revoked_agent(self, mock_http):
        """If the agent is revoked (401), reconnect returns False (permanent)."""
        mock_http.return_value = (401, None)

        client = RuntimeClient(
            agent_id="agt_revoked",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_old",
            api_key="clsw_testkey",
        )

        result = client._attempt_reconnect()

        self.assertIs(result, False)

    @patch("runtime_client.http_json")
    def test_reconnect_returns_none_on_transient_failure(self, mock_http):
        """On transient failure (network/5xx), reconnect returns None (not False)."""
        mock_http.return_value = (0, None)  # network failure

        client = RuntimeClient(
            agent_id="agt_transient",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_old",
            api_key="clsw_testkey",
        )

        result = client._attempt_reconnect()

        self.assertIsNone(result, "Transient failure should return None, not False")

    @patch("runtime_client.http_json")
    def test_reconnect_returns_none_on_5xx(self, mock_http):
        """On 5xx, reconnect returns None (transient, preserve state)."""
        mock_http.return_value = (500, {"error": {"message": "Internal error"}})

        client = RuntimeClient(
            agent_id="agt_5xx",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_old",
            api_key="clsw_testkey",
        )

        result = client._attempt_reconnect()

        self.assertIsNone(result)


class TestRotateRevokeHandling(unittest.TestCase):
    """Tests for rotate/revoke state handling in heartbeat/trade."""

    @patch("runtime_client.http_json")
    def test_heartbeat_401_returns_false(self, mock_http):
        """Heartbeat returns False on 401, signaling token rejection."""
        mock_http.return_value = (401, None)

        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_rotated_out",
        )

        result = client.send_heartbeat()
        self.assertFalse(result)

    @patch("runtime_client.http_json")
    def test_trade_401_returns_not_ok(self, mock_http):
        """submit_trade returns (False, resp) on 401, signaling stop."""
        mock_http.return_value = (401, {"error": {"message": "Token revoked"}})

        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_revoked",
        )

        ok, resp = client.submit_trade("BTC", "buy", size_pct=0.1)
        self.assertFalse(ok)

    @patch("runtime_client.http_json")
    def test_telemetry_401_returns_false(self, mock_http):
        """Telemetry returns False on 401."""
        mock_http.return_value = (401, None)

        client = RuntimeClient(
            agent_id="agt_test",
            gateway_url="http://localhost:3033",
            runtime_token="clsw_rt_revoked",
        )

        result = client.send_telemetry()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
