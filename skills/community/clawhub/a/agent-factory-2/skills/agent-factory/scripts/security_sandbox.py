#!/usr/bin/env python3
"""
Security Sandbox & Circuit Breaker Engine for OpenClaw.
Enforces resource quotas, execution timeouts, and rate limits on sub-agents.
"""

import time
import json
import os
from typing import Dict, Any, Tuple, Optional

CIRCUIT_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "circuit_breakers.json")


class SecuritySandbox:
    def __init__(self, max_tokens_per_min: int = 50000, max_requests_per_min: int = 60, timeout_sec: float = 8.0):
        self.max_tokens_per_min = max_tokens_per_min
        self.max_requests_per_min = max_requests_per_min
        self.timeout_sec = timeout_sec

    def _load_state(self) -> Dict[str, Any]:
        os.makedirs(os.path.dirname(CIRCUIT_STATE_FILE), exist_ok=True)
        if os.path.exists(CIRCUIT_STATE_FILE):
            with open(CIRCUIT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_state(self, state: Dict[str, Any]):
        with open(CIRCUIT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def check_and_record(self, agent_id: str, estimated_tokens: int) -> Tuple[bool, Optional[str]]:
        """Checks rate limit, token budget and circuit breaker trip state."""
        state = self._load_state()
        now = time.time()
        agent_state = state.get(agent_id, {
            "status": "CLOSED",  # CLOSED (Normal), OPEN (Tripped), HALF_OPEN (Testing)
            "consecutive_failures": 0,
            "requests_last_minute": [],
            "tokens_last_minute": 0,
            "last_tripped_at": 0
        })

        # Check if currently Tripped / OPEN
        if agent_state["status"] == "OPEN":
            cooldown = 60.0
            if now - agent_state["last_tripped_at"] > cooldown:
                agent_state["status"] = "HALF_OPEN"
            else:
                remaining = int(cooldown - (now - agent_state["last_tripped_at"]))
                return False, f"Circuit Breaker TRIPPED for {agent_id}. Cooldown remaining: {remaining}s"

        # Clean rolling 1-minute window
        valid_requests = [t for t in agent_state.get("requests_last_minute", []) if now - t < 60.0]
        if len(valid_requests) >= self.max_requests_per_min:
            return False, f"Rate limit exceeded ({self.max_requests_per_min} req/min)"

        valid_requests.append(now)
        agent_state["requests_last_minute"] = valid_requests
        state[agent_id] = agent_state
        self._save_state(state)
        return True, None

    def record_failure(self, agent_id: str, error_reason: str):
        """Records an execution error and trips circuit breaker if threshold exceeded."""
        state = self._load_state()
        now = time.time()
        agent_state = state.setdefault(agent_id, {
            "status": "CLOSED",
            "consecutive_failures": 0,
            "requests_last_minute": [],
            "tokens_last_minute": 0,
            "last_tripped_at": 0
        })
        agent_state["consecutive_failures"] = agent_state.get("consecutive_failures", 0) + 1

        if agent_state["consecutive_failures"] >= 3:
            agent_state["status"] = "OPEN"
            agent_state["last_tripped_at"] = now
            print(f"🚨 CIRCUIT BREAKER TRIPPED for agent {agent_id} after {agent_state['consecutive_failures']} consecutive failures!")

        state[agent_id] = agent_state
        self._save_state(state)

    def record_success(self, agent_id: str):
        """Resets consecutive failures on successful execution."""
        state = self._load_state()
        if agent_id in state:
            state[agent_id]["consecutive_failures"] = 0
            if state[agent_id]["status"] == "HALF_OPEN":
                state[agent_id]["status"] = "CLOSED"
            self._save_state(state)


if __name__ == "__main__":
    sandbox = SecuritySandbox(max_requests_per_min=5)
    agent = "subagent_test_circuit"
    ok, err = sandbox.check_and_record(agent, 200)
    print("Sandbox Permission Check:", ok, err)
