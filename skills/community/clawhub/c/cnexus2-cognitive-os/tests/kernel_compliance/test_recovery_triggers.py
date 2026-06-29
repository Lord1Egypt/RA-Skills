"""Test stub: L2 recovery triggers — auto-generated from 02_stability_spec/03."""
import pytest
from kernel.identity_position import evaluate_recovery

# ---- §2 Trigger conditions ----
def test_recovery_triggered_on_identity_correction_failure():
    """recovery_triggers §2: correction failure with reentrant oscillation >= 0.7."""
    correction_result = {
        "triggered": True, "correction_path": "attractor_pull",
        "convergence_proven": False, "reentrant_oscillation": True,
        "status": "failed"
    }
    result = evaluate_recovery(correction_result=correction_result)
    assert result["triggered"] is True
    assert result["severity"] >= 0.7

def test_recovery_triggered_on_persona_loss():
    """recovery_triggers §2: persona loss (L0-01 persistent fail) triggers severity 1.0."""
    drift_result = {"L0-01": {"passed": False}, "L0-02": {"passed": True},
                    "anomaly_count": 3}
    correction_result = {"status": "failed"}
    result = evaluate_recovery(
        drift_result=drift_result,
        correction_result=correction_result,
        consecutive_iterations_with_persona_loss=4
    )
    assert result["severity"] == 1.0

# ---- §3.1 REFUGE mode exit conditions ----
def test_refuge_exit_requires_2_clean_rounds():
    """recovery_triggers §3.1: REFUGE exit requires 2+ rounds with no anomalies."""
    drift_history = [
        {"all_passed": True},
        {"all_passed": True},
    ]
    result = evaluate_recovery(
        in_refuge=True,
        drift_history=drift_history,
        iterations_in_refuge=5
    )
    assert result.get("rearm_conditions_met") is True

# ---- §5: anti-jitter — 3 round minimum stay ----
def test_anti_jitter_minimum_stay():
    """recovery_triggers §5: cannot rearm within first 3 rounds of a new level."""
    result = evaluate_recovery(
        current_level="L2",
        iterations_in_level=2,
        drift_history=[{"all_passed": True}] * 2
    )
    assert result.get("rearm_conditions_met") is False or result.get("anti_jitter_active") is True
