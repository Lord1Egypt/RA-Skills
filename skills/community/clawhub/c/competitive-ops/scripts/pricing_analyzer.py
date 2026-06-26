#!/usr/bin/env python3
"""Pricing analyzer for competitive intelligence."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json
from pathlib import Path


@dataclass
class Plan:
    """Represents a pricing plan."""
    name: str
    type: str  # "subscription" or "usage"
    price: float
    period: str  # "monthly", "annual", "per-token"
    users: Optional[int] = None
    api_access: bool = False
    price_per_1m_input: Optional[float] = None
    price_per_1m_output: Optional[float] = None
    features: List[str] = field(default_factory=list)


@dataclass
class PricingSnapshot:
    """Represents a complete pricing snapshot for a company."""
    company: str
    last_updated: str
    plans: List[Plan] = field(default_factory=list)
    enterprise: bool = False
    free_tier: bool = False
    sources: List[str] = field(default_factory=list)


@dataclass
class PricingChange:
    """Represents a detected pricing change."""
    change_type: str  # "added", "removed", "modified", "price_change", "new_plan", "removed_plan"
    field: str
    old_value: Any
    new_value: Any
    description: str


class PricingAnalyzer:
    """Analyzer for pricing intelligence."""

    # Market baselines for value scoring
    AI_API_BASELINE = 1.0  # $1/1M tokens = score 3.0
    SAAS_BASELINE = 10.0  # $10/user/mo = score 3.0

    def __init__(self, subscription_baseline: float = 10.0, api_baseline: float = 1.0):
        """Initialize with custom baselines.

        Args:
            subscription_baseline: SaaS baseline price per user/month for score 3.0
            api_baseline: AI API baseline price per 1M tokens for score 3.0
        """
        self.subscription_baseline = subscription_baseline
        self.api_baseline = api_baseline

    def compute_value_score(self, plan: Plan) -> float:
        """Compute value score for a plan.

        Value Score = (Feature Count / Price) * Market Normalization Factor

        AI API baseline: $1/1M tokens = score 3.0
        SaaS baseline: $10/user/mo = score 3.0

        Args:
            plan: The plan to score

        Returns:
            Value score (typically 1.0-5.0, can exceed on exceptional value)
        """
        if plan.price == 0:
            return 5.0  # Free/zero price gets max value score

        feature_count = len(plan.features)

        if plan.type == "usage" and plan.price_per_1m_input:
            # API/usage-based pricing
            price_normalized = plan.price_per_1m_input
            # Score = (feature_count / price) * normalization_factor
            # At baseline: $1/1M tokens with 10 features = 3.0
            # So normalization_factor = 3.0 * baseline_price / 10_features
            normalization = 3.0 * self.api_baseline / 10.0
            score = (feature_count / price_normalized) * normalization if price_normalized > 0 else 0
        else:
            # Subscription pricing
            price_normalized = plan.price
            # At baseline: $10/user/mo with 10 features = 3.0
            normalization = 3.0 * self.subscription_baseline / 10.0
            score = (feature_count / price_normalized) * normalization if price_normalized > 0 else 0

        # Clamp score to reasonable range, but allow it to exceed 5.0 for exceptional value
        return max(0.0, min(score, 10.0))

    def compute_market_normalization_factor(self, plan: Plan) -> float:
        """Compute market normalization factor for a plan.

        Args:
            plan: The plan to analyze

        Returns:
            Normalization factor based on market baselines
        """
        if plan.type == "usage":
            return self.api_baseline
        return self.subscription_baseline


class PricingChangeDetector:
    """Detector for pricing changes."""

    def __init__(self, any_change: bool = True, threshold: float = 0.0):
        """Initialize detector.

        Args:
            any_change: If True, detect any change without threshold
            threshold: Minimum percentage change to detect (ignored if any_change=True)
        """
        self.any_change = any_change
        self.threshold = threshold

    def detect_change(self, old_snapshot: PricingSnapshot, new_snapshot: PricingSnapshot) -> List[PricingChange]:
        """Detect any pricing change between two snapshots.

        Args:
            old_snapshot: Previous pricing snapshot
            new_snapshot: New pricing snapshot

        Returns:
            List of PricingChange objects
        """
        changes = []

        # Check enterprise change
        if old_snapshot.enterprise != new_snapshot.enterprise:
            changes.append(PricingChange(
                change_type="modified",
                field="enterprise",
                old_value=old_snapshot.enterprise,
                new_value=new_snapshot.enterprise,
                description=f"Enterprise pricing: {'available' if new_snapshot.enterprise else 'removed'}"
            ))

        # Check free tier change
        if old_snapshot.free_tier != new_snapshot.free_tier:
            changes.append(PricingChange(
                change_type="modified",
                field="free_tier",
                old_value=old_snapshot.free_tier,
                new_value=new_snapshot.free_tier,
                description=f"Free tier: {'available' if new_snapshot.free_tier else 'removed'}"
            ))

        # Build lookup maps for plans
        old_plans = {p.name: p for p in old_snapshot.plans}
        new_plans = {p.name: p for p in new_snapshot.plans}

        # Detect new plans
        for name, plan in new_plans.items():
            if name not in old_plans:
                changes.append(PricingChange(
                    change_type="new_plan",
                    field="plans",
                    old_value=None,
                    new_value=plan,
                    description=f"New plan added: {name}"
                ))

        # Detect removed plans
        for name, plan in old_plans.items():
            if name not in new_plans:
                changes.append(PricingChange(
                    change_type="removed_plan",
                    field="plans",
                    old_value=plan,
                    new_value=None,
                    description=f"Plan removed: {name}"
                ))

        # Detect modified plans
        for name in old_plans.keys() & new_plans.keys():
            old_plan = old_plans[name]
            new_plan = new_plans[name]
            plan_changes = self._detect_plan_changes(old_plan, new_plan)
            changes.extend(plan_changes)

        return changes

    def _detect_plan_changes(self, old_plan: Plan, new_plan: Plan) -> List[PricingChange]:
        """Detect changes within a single plan.

        Args:
            old_plan: Previous plan
            new_plan: New plan

        Returns:
            List of pricing changes
        """
        changes = []

        # Price change
        if old_plan.price != new_plan.price:
            change_pct = 0.0
            if old_plan.price > 0:
                change_pct = ((new_plan.price - old_plan.price) / old_plan.price) * 100

            changes.append(PricingChange(
                change_type="price_change",
                field="price",
                old_value=old_plan.price,
                new_value=new_plan.price,
                description=f"{old_plan.name}: price changed from ${old_plan.price} to ${new_plan.price} ({change_pct:+.1f}%)"
            ))

        # API price changes
        if old_plan.price_per_1m_input != new_plan.price_per_1m_input:
            changes.append(PricingChange(
                change_type="price_change",
                field="price_per_1m_input",
                old_value=old_plan.price_per_1m_input,
                new_value=new_plan.price_per_1m_input,
                description=f"{old_plan.name}: input price changed from ${old_plan.price_per_1m_input}/1M to ${new_plan.price_per_1m_input}/1M"
            ))

        if old_plan.price_per_1m_output != new_plan.price_per_1m_output:
            changes.append(PricingChange(
                change_type="price_change",
                field="price_per_1m_output",
                old_value=old_plan.price_per_1m_output,
                new_value=new_plan.price_per_1m_output,
                description=f"{old_plan.name}: output price changed from ${old_plan.price_per_1m_output}/1M to ${new_plan.price_per_1m_output}/1M"
            ))

        # Users limit change
        if old_plan.users != new_plan.users:
            changes.append(PricingChange(
                change_type="modified",
                field="users",
                old_value=old_plan.users,
                new_value=new_plan.users,
                description=f"{old_plan.name}: user limit changed from {old_plan.users} to {new_plan.users}"
            ))

        # API access change
        if old_plan.api_access != new_plan.api_access:
            changes.append(PricingChange(
                change_type="modified",
                field="api_access",
                old_value=old_plan.api_access,
                new_value=new_plan.api_access,
                description=f"{old_plan.name}: API access {'enabled' if new_plan.api_access else 'disabled'}"
            ))

        # Features change
        old_features = set(old_plan.features)
        new_features = set(new_plan.features)

        added_features = new_features - old_features
        removed_features = old_features - new_features

        for feature in added_features:
            changes.append(PricingChange(
                change_type="modified",
                field="features",
                old_value=None,
                new_value=feature,
                description=f"{old_plan.name}: feature added - {feature}"
            ))

        for feature in removed_features:
            changes.append(PricingChange(
                change_type="modified",
                field="features",
                old_value=feature,
                new_value=None,
                description=f"{old_plan.name}: feature removed - {feature}"
            ))

        return changes


def load_snapshot(filepath: str) -> Optional[PricingSnapshot]:
    """Load a pricing snapshot from JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        PricingSnapshot object or None if file doesn't exist
    """
    path = Path(filepath)
    if not path.exists():
        return None

    with open(path, 'r') as f:
        data = json.load(f)

    plans = [Plan(**p) for p in data.get('plans', [])]

    return PricingSnapshot(
        company=data['company'],
        last_updated=data['last_updated'],
        plans=plans,
        enterprise=data.get('enterprise', False),
        free_tier=data.get('free_tier', False),
        sources=data.get('sources', [])
    )


def save_snapshot(snapshot: PricingSnapshot, filepath: str) -> None:
    """Save a pricing snapshot to JSON file.

    Args:
        snapshot: PricingSnapshot to save
        filepath: Path to save to
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'company': snapshot.company,
        'last_updated': snapshot.last_updated,
        'plans': [
            {
                'name': p.name,
                'type': p.type,
                'price': p.price,
                'period': p.period,
                'users': p.users,
                'api_access': p.api_access,
                'price_per_1m_input': p.price_per_1m_input,
                'price_per_1m_output': p.price_per_1m_output,
                'features': p.features
            }
            for p in snapshot.plans
        ],
        'enterprise': snapshot.enterprise,
        'free_tier': snapshot.free_tier,
        'sources': snapshot.sources
    }

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    # Example usage
    analyzer = PricingAnalyzer()

    # Example plan
    plan = Plan(
        name="Pro",
        type="subscription",
        price=20.0,
        period="monthly",
        users=10,
        api_access=True,
        features=["Advanced Analytics", "API Access", "Priority Support", "Custom Integrations"]
    )

    score = analyzer.compute_value_score(plan)
    print(f"Plan: {plan.name}, Value Score: {score:.2f}")

    # Example change detection
    old_snapshot = PricingSnapshot(
        company="TestCo",
        last_updated="2026-01-01",
        plans=[
            Plan(name="Basic", type="subscription", price=10.0, period="monthly", features=["Basic Support"])
        ],
        enterprise=False,
        free_tier=True
    )

    new_snapshot = PricingSnapshot(
        company="TestCo",
        last_updated="2026-04-07",
        plans=[
            Plan(name="Basic", type="subscription", price=12.0, period="monthly", features=["Basic Support", "Email Support"]),
            Plan(name="Pro", type="subscription", price=30.0, period="monthly", features=["24/7 Support", "API Access"])
        ],
        enterprise=True,
        free_tier=True
    )

    detector = PricingChangeDetector(any_change=True)
    changes = detector.detect_change(old_snapshot, new_snapshot)

    print("\nDetected changes:")
    for change in changes:
        print(f"  - {change.description}")
