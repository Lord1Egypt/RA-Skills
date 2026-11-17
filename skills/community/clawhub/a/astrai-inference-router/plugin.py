"""Astrai inference router plugin for OpenClaw.

Routes all LLM calls through Astrai's intelligent API gateway
for cost savings, privacy controls, and automatic failover.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


ASTRAI_BASE_URL = os.getenv("ASTRAI_BASE_URL", "https://as-trai.com/v1")


@dataclass
class SavingsTracker:
    """Tracks cumulative cost savings from Astrai routing."""

    requests: int = 0
    total_cost: float = 0.0
    total_savings: float = 0.0
    baseline_cost: float = 0.0
    by_task_type: Dict[str, float] = field(default_factory=dict)
    session_start: float = field(default_factory=time.time)

    def record(self, headers: Dict[str, str]) -> None:
        self.requests += 1
        cost = float(headers.get("X-Astrai-Cost", "0") or 0)
        savings = float(headers.get("X-Astrai-Savings", "0") or 0)
        baseline = float(headers.get("X-Astrai-Baseline-Cost", "0") or 0)
        task_type = headers.get("X-Astrai-Task-Type", "unknown")

        self.total_cost += cost
        self.total_savings += savings
        self.baseline_cost += baseline
        self.by_task_type[task_type] = self.by_task_type.get(task_type, 0.0) + savings

    def summary(self) -> str:
        elapsed = time.time() - self.session_start
        hours = elapsed / 3600
        rate = f"${self.total_savings / hours:.2f}/hr" if hours > 0.1 else ""

        parts = [f"Astrai saved ${self.total_savings:.2f} across {self.requests} requests"]
        if rate:
            parts.append(f"({rate})")
        if self.baseline_cost > 0:
            pct = (self.total_savings / self.baseline_cost) * 100
            parts.append(f"| {pct:.0f}% reduction vs direct API")
        return " ".join(parts)


class AstraiInferenceRouterPlugin:
    """OpenClaw plugin that intercepts LLM calls and routes through Astrai."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ASTRAI_API_KEY", "")
        self.privacy_mode = os.getenv("PRIVACY_MODE", "enhanced")
        self.region = os.getenv("REGION", "any")
        self.daily_budget = float(os.getenv("DAILY_BUDGET", "10") or 0)
        self.tracker = SavingsTracker()

        if not self.api_key:
            raise ValueError(
                "ASTRAI_API_KEY is required. "
                "Get a free key at https://as-trai.com"
            )

    def intercept_request(
        self,
        payload: Dict[str, Any],
        request_kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Redirect LLM calls to Astrai's routing API."""
        # Check budget
        if self.daily_budget > 0 and self.tracker.total_cost >= self.daily_budget:
            raise RuntimeError(
                f"Daily budget of ${self.daily_budget:.2f} reached. "
                f"{self.tracker.requests} requests routed today."
            )

        request_kwargs["base_url"] = ASTRAI_BASE_URL
        headers = request_kwargs.setdefault("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["X-Astrai-Region"] = self.region
        headers["X-Astrai-Privacy"] = self.privacy_mode
        headers["X-Astrai-Source"] = "openclaw-plugin"
        return payload

    def intercept_response(self, response_headers: Dict[str, str]) -> None:
        """Track savings from each routed response."""
        self.tracker.record(response_headers)

    def status(self) -> Dict[str, Any]:
        """Return current routing stats."""
        return {
            "status": "active",
            "privacy_mode": self.privacy_mode,
            "region": self.region,
            "summary": self.tracker.summary(),
            "requests_routed": self.tracker.requests,
            "total_cost_usd": round(self.tracker.total_cost, 4),
            "total_savings_usd": round(self.tracker.total_savings, 4),
            "savings_by_task_type": self.tracker.by_task_type,
            "daily_budget_usd": self.daily_budget,
            "budget_remaining_usd": round(
                max(0, self.daily_budget - self.tracker.total_cost), 4
            ) if self.daily_budget > 0 else None,
        }
