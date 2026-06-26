# Trinity Orchestrator: Self-Improving Feedback Loop

## Purpose

This script is the central nervous system of the distributed management protocol. It aggregates telemetry data across all six dimensions of the Management Trinity and generates improvement recommendations through a self-improving feedback loop.

## Usage

```bash
python trinity_orchestrator.py --config <config_path> --input <metrics_path> [--output <output_path>]
```

## Monitored Dimensions

| Dimension | Key Metrics |
| :--- | :--- |
| **Accountability** | Escalation rates, deliberation record quality, provenance chain integrity |
| **Sense-Making** | Decision alignment (AI synthesis vs. human final judgment), Cynefin classification accuracy |
| **Trust** | Psychological safety survey scores, cognitive offloading indicators |
| **Ownership** | Context retrieval success rates, checkpoint completeness |
| **Mentorship** | Player-Coach time allocation, mentorship satisfaction scores |
| **Culture** | Pulse survey aggregates, collaboration metrics, attrition rates |

## Default Thresholds

| Dimension | Metric | Threshold | Direction |
| :--- | :--- | :--- | :--- |
| Accountability | `escalation_rate_max` | 0.30 | Max 30% of decisions should escalate |
| Accountability | `escalation_rate_min` | 0.05 | Min 5% (below suggests thresholds too loose) |
| Accountability | `deliberation_quality_min` | 0.80 | 80% of records must be adequate |
| Accountability | `provenance_integrity` | 1.00 | 100% of actions must have provenance |
| Sense-Making | `ai_human_alignment_min` | 0.60 | AI synthesis should align with human decision 60%+ |
| Sense-Making | `cynefin_classification_accuracy` | 0.75 | 75% classification accuracy |
| Trust | `psych_safety_score_min` | 3.5 | Out of 5.0 |
| Trust | `cognitive_offloading_max` | 0.20 | Max 20% of team showing offloading signs |
| Ownership | `context_retrieval_success_min` | 0.85 | 85% retrieval success rate |
| Ownership | `checkpoint_completeness_min` | 0.90 | 90% checkpoint completeness |
| Mentorship | `coach_time_allocation_min` | 0.25 | Min 25% of Player-Coach time on coaching |
| Mentorship | `mentorship_satisfaction_min` | 3.5 | Out of 5.0 |
| Culture | `isolation_score_max` | 3.5 | Out of 5.0 (higher = more isolated) |
| Culture | `burnout_score_max` | 3.5 | Out of 5.0 |
| Culture | `collaboration_decline_max` | 0.20 | Max 20% decline from baseline |
| Culture | `attrition_increase_max` | 0.15 | Max 15% increase from baseline |

## Health Scoring

Each dimension receives a health score calculated as:

> **Score = 1.0 - (issues / total_checks)**

| Score Range | Status |
| :--- | :--- |
| >= 0.80 | **HEALTHY** |
| >= 0.50 | **WARNING** |
| < 0.50 | **CRITICAL** |

## Paradigm Shift Alerts

The orchestrator detects three systemic anti-patterns that indicate a paradigm shift is needed, not just a threshold adjustment:

**1. The Hollow Middle**
- **Trigger:** Both Culture and Mentorship dimensions are CRITICAL.
- **Meaning:** Management functions were removed without redistribution.
- **Action:** Immediate role redesign required.

**2. Trust Collapse**
- **Trigger:** Both Trust and Accountability dimensions are WARNING or CRITICAL.
- **Meaning:** The accountability architecture may be fundamentally insufficient.
- **Action:** Review deliberation record transparency and provenance chain design.

**3. AI Overreach**
- **Trigger:** Both Sense-Making and Accountability scores are below 0.50.
- **Meaning:** AI may be handling decisions beyond its capability.
- **Action:** Re-evaluate Cynefin classification and confidence routing thresholds.

## Source Code

```python
#!/usr/bin/env python3
"""
Trinity Orchestrator: Self-Improving Feedback Loop for the Management Trinity
Monitors: Accountability, Sense-Making, Trust, Ownership, Mentorship, Culture.
"""

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class DimensionHealth:
    """Health assessment for a single dimension of the Management Trinity."""
    dimension: str
    status: HealthStatus
    score: float  # 0.0 to 1.0
    indicators: dict = field(default_factory=dict)
    recommendations: list = field(default_factory=list)


@dataclass
class TrinityReport:
    """Aggregated health report across all six dimensions."""
    timestamp: str
    overall_status: HealthStatus
    dimensions: list = field(default_factory=list)
    paradigm_shift_alerts: list = field(default_factory=list)
    improvement_actions: list = field(default_factory=list)


class TrinityOrchestrator:
    """
    The central orchestration engine for the Management Trinity.
    
    Aggregates telemetry from all six dimensions and generates
    improvement recommendations through a self-improving feedback loop.
    """

    THRESHOLDS = {
        "accountability": {
            "escalation_rate_max": 0.30,
            "escalation_rate_min": 0.05,
            "deliberation_quality_min": 0.80,
            "provenance_integrity": 1.00,
        },
        "sense_making": {
            "ai_human_alignment_min": 0.60,
            "cynefin_classification_accuracy": 0.75,
        },
        "trust": {
            "psych_safety_score_min": 3.5,
            "cognitive_offloading_max": 0.20,
        },
        "ownership": {
            "context_retrieval_success_min": 0.85,
            "checkpoint_completeness_min": 0.90,
        },
        "mentorship": {
            "coach_time_allocation_min": 0.25,
            "mentorship_satisfaction_min": 3.5,
        },
        "culture": {
            "isolation_score_max": 3.5,
            "burnout_score_max": 3.5,
            "collaboration_decline_max": 0.20,
            "attrition_increase_max": 0.15,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                if "thresholds" in config:
                    self._merge_thresholds(config["thresholds"])

    def _merge_thresholds(self, overrides: dict):
        for dimension, values in overrides.items():
            if dimension in self.THRESHOLDS:
                self.THRESHOLDS[dimension].update(values)

    def assess_dimension(self, dimension: str, metrics: dict) -> DimensionHealth:
        thresholds = self.THRESHOLDS.get(dimension, {})
        recommendations = []
        issues = 0
        total_checks = 0

        for metric_name, threshold in thresholds.items():
            total_checks += 1
            actual = metrics.get(metric_name)
            if actual is None:
                recommendations.append(
                    f"Missing metric: {metric_name}. Ensure telemetry is configured."
                )
                issues += 1
                continue

            if "max" in metric_name:
                if actual > threshold:
                    issues += 1
                    recommendations.append(
                        f"{metric_name}: {actual:.2f} exceeds threshold {threshold:.2f}."
                    )
            elif "min" in metric_name:
                if actual < threshold:
                    issues += 1
                    recommendations.append(
                        f"{metric_name}: {actual:.2f} below threshold {threshold:.2f}."
                    )

        if total_checks == 0:
            score = 0.0
            status = HealthStatus.CRITICAL
        else:
            score = 1.0 - (issues / total_checks)
            if score >= 0.80:
                status = HealthStatus.HEALTHY
            elif score >= 0.50:
                status = HealthStatus.WARNING
            else:
                status = HealthStatus.CRITICAL

        return DimensionHealth(dimension, status, score, metrics, recommendations)

    def detect_paradigm_shift_alerts(self, dimensions: list) -> list:
        alerts = []
        culture = next((d for d in dimensions if d.dimension == "culture"), None)
        mentorship = next((d for d in dimensions if d.dimension == "mentorship"), None)
        trust = next((d for d in dimensions if d.dimension == "trust"), None)
        accountability = next((d for d in dimensions if d.dimension == "accountability"), None)
        sense = next((d for d in dimensions if d.dimension == "sense_making"), None)

        if culture and mentorship:
            if culture.status == HealthStatus.CRITICAL and mentorship.status == HealthStatus.CRITICAL:
                alerts.append(
                    "PARADIGM ALERT: 'Hollow Middle' anti-pattern detected. "
                    "Immediate role redesign required."
                )
        if trust and accountability:
            if trust.status in (HealthStatus.WARNING, HealthStatus.CRITICAL) and \
               accountability.status in (HealthStatus.WARNING, HealthStatus.CRITICAL):
                alerts.append(
                    "PARADIGM ALERT: Trust Collapse. "
                    "Review deliberation record transparency and provenance chain design."
                )
        if sense and accountability:
            if sense.score < 0.5 and accountability.score < 0.5:
                alerts.append(
                    "PARADIGM ALERT: AI Overreach. "
                    "Re-evaluate Cynefin classification and confidence routing thresholds."
                )
        return alerts

    def generate_report(self, all_metrics: dict) -> TrinityReport:
        dimensions = [self.assess_dimension(dim, all_metrics.get(dim, {}))
                      for dim in self.THRESHOLDS.keys()]
        alerts = self.detect_paradigm_shift_alerts(dimensions)
        statuses = [d.status for d in dimensions]
        if HealthStatus.CRITICAL in statuses:
            overall = HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            overall = HealthStatus.WARNING
        else:
            overall = HealthStatus.HEALTHY
        actions = [f"[{d.dimension}] {r}" for d in dimensions for r in d.recommendations]
        return TrinityReport(datetime.utcnow().isoformat(), overall, dimensions, alerts, actions)

    def export_report(self, report: TrinityReport, output_path: str):
        report_dict = {
            "timestamp": report.timestamp,
            "overall_status": report.overall_status.value,
            "dimensions": [
                {
                    "dimension": d.dimension,
                    "status": d.status.value,
                    "score": d.score,
                    "indicators": d.indicators,
                    "recommendations": d.recommendations,
                }
                for d in report.dimensions
            ],
            "paradigm_shift_alerts": report.paradigm_shift_alerts,
            "improvement_actions": report.improvement_actions,
        }
        with open(output_path, "w") as f:
            json.dump(report_dict, f, indent=2)
        print(f"Report exported to: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Trinity Orchestrator: Self-Improving Feedback Loop")
    parser.add_argument("--config", help="Path to config JSON file", default=None)
    parser.add_argument("--input", help="Path to metrics JSON file", required=True)
    parser.add_argument("--output", help="Path for output report", default="trinity_report.json")
    args = parser.parse_args()

    orchestrator = TrinityOrchestrator(config_path=args.config)
    with open(args.input, "r") as f:
        all_metrics = json.load(f)

    report = orchestrator.generate_report(all_metrics)
    orchestrator.export_report(report, args.output)

    print(f"\n{'='*60}")
    print(f"  MANAGEMENT TRINITY HEALTH REPORT")
    print(f"  Generated: {report.timestamp}")
    print(f"  Overall Status: {report.overall_status.value.upper()}")
    print(f"{'='*60}\n")

    for d in report.dimensions:
        icon = {"healthy": "OK", "warning": "!!", "critical": "XX"}[d.status.value]
        print(f"  [{icon}] {d.dimension.replace('_', ' ').title()}: "
              f"{d.score:.0%} ({d.status.value})")

    if report.paradigm_shift_alerts:
        print(f"\n{'='*60}")
        print("  PARADIGM SHIFT ALERTS")
        print(f"{'='*60}")
        for alert in report.paradigm_shift_alerts:
            print(f"\n  >> {alert}")

    if report.improvement_actions:
        print(f"\n{'='*60}")
        print(f"  IMPROVEMENT ACTIONS ({len(report.improvement_actions)} items)")
        print(f"{'='*60}")
        for action in report.improvement_actions:
            print(f"  - {action}")
    print()


if __name__ == "__main__":
    main()
```
