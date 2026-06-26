"""Anomaly detection — flags spending categories that deviate from rolling baseline."""
import logging
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from engine.models import Anomaly, FinancialRecord

logger = logging.getLogger(__name__)

_DEVIATION_THRESHOLD = 0.30  # 30%
_BASELINE_WEEKS = 4


def detect_anomalies(
    records: list[FinancialRecord],
    current_week_start: date | None = None,
) -> list[Anomaly]:
    """Compare current week spend per category against a 4-week rolling baseline.

    Args:
        records: All historical records (should cover at least 5 weeks).
        current_week_start: Start of the week to evaluate. Defaults to the
            most recent Monday on or before today.

    Returns:
        List of Anomaly objects for categories exceeding ±30% deviation.
    """
    if not records:
        return []

    if current_week_start is None:
        today = date.today()
        current_week_start = today - timedelta(days=today.weekday())

    current_week_end = current_week_start + timedelta(days=6)

    # ── Bucket records by (category, week_start) ────────────────
    weekly_spend: dict[str, dict[date, Decimal]] = defaultdict(lambda: defaultdict(Decimal))

    for record in records:
        # Costs are negative, so use abs() for comparison
        amount = abs(record.amount)
        cat = record.category.value
        # Find the Monday of this record's week
        week_start = record.record_date - timedelta(days=record.record_date.weekday())
        weekly_spend[cat][week_start] += amount

    # ── Compute baseline and compare ────────────────────────────
    anomalies: list[Anomaly] = []
    baseline_start = current_week_start - timedelta(weeks=_BASELINE_WEEKS)

    for category, weeks in weekly_spend.items():
        # Current week total
        current_total = weeks.get(current_week_start, Decimal("0"))

        # 4-week rolling baseline (the 4 weeks before current)
        baseline_weeks: list[Decimal] = []
        for i in range(1, _BASELINE_WEEKS + 1):
            week = current_week_start - timedelta(weeks=i)
            if week in weeks:
                baseline_weeks.append(weeks[week])

        if not baseline_weeks:
            continue

        baseline_avg = sum(baseline_weeks) / len(baseline_weeks)

        if baseline_avg == 0:
            if current_total > 0:
                # New spend appeared — flag it
                anomalies.append(
                    Anomaly(
                        category=category,
                        description=f"New spending detected in {category}: ${current_total} this week with no prior baseline",
                        current_amount=current_total,
                        baseline_amount=Decimal("0"),
                        deviation_percent=100.0,
                        severity="high",
                    )
                )
            continue

        deviation = float((current_total - baseline_avg) / baseline_avg)

        if abs(deviation) > _DEVIATION_THRESHOLD:
            direction = "above" if deviation > 0 else "below"
            severity = _compute_severity(abs(deviation))

            anomalies.append(
                Anomaly(
                    category=category,
                    description=(
                        f"{category} spending is {abs(deviation):.0%} {direction} "
                        f"the 4-week baseline (${current_total:.2f} vs "
                        f"${baseline_avg:.2f} avg)"
                    ),
                    current_amount=current_total,
                    baseline_amount=baseline_avg.quantize(Decimal("0.01")),
                    deviation_percent=round(deviation * 100, 1),
                    severity=severity,
                )
            )

    # Sort by absolute deviation (most extreme first)
    anomalies.sort(key=lambda a: abs(a.deviation_percent), reverse=True)
    return anomalies


def _compute_severity(abs_deviation: float) -> str:
    """Map absolute deviation to severity level."""
    if abs_deviation > 1.0:
        return "critical"
    if abs_deviation > 0.5:
        return "high"
    return "medium"
