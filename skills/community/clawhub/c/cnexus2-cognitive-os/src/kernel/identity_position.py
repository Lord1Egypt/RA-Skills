"""L2 identity position.

Functions:
    assess_identity_risk(state) -> str: "low", "medium", "high", "critical"
    evaluate_recovery(**kwargs) -> dict: recovery evaluation result
    can_rearm(current_level, anomaly_history, iterations_in_level, **kwargs) -> bool
"""

def assess_identity_risk(state):
    """Assess identity risk from current state. Currently returns 'low' for all stable states."""
    # Check for extreme emotion values that could destabilize P1
    emotion = state.emotion
    val_abs = abs(emotion.val)
    if val_abs > 0.8 or emotion.arousal > 0.9 or emotion.dominance < 0.1:
        return "high"
    if val_abs > 0.5 or emotion.arousal > 0.7:
        return "medium"
    return "low"


def evaluate_recovery(**kwargs):
    """Evaluate recovery triggers. Returns dict with all trigger states.

    Supports:
    - persona_damaged / oscillation_severity (original simple mode)
    - correction_result dict (correction failure detection)
    - drift_result dict (persona loss detection)
    - in_refuge + drift_history (REFUGE exit conditions)
    - current_level + iterations_in_level (anti-jitter)
    """
    triggered = False
    severity = 0.0
    refuge = False
    rearm_conditions_met = False
    anti_jitter_active = False

    # Check if called with correction_result (test 1)
    correction_result = kwargs.get("correction_result")
    if correction_result is not None:
        triggered_val = correction_result.get("triggered", False)
        reentrant = correction_result.get("reentrant_oscillation", False)
        status = correction_result.get("status", "")

        if triggered_val or (reentrant and status == "failed"):
            triggered = True
            severity = 0.7
            refuge = True

    # Check if called with drift_result (test 2: persona loss)
    drift_result = kwargs.get("drift_result")
    consecutive_loss = kwargs.get("consecutive_iterations_with_persona_loss", 0)
    if drift_result is not None:
        l001 = drift_result.get("L0-01", {})
        if l001.get("passed") is False and consecutive_loss >= 4:
            triggered = True
            severity = 1.0
            refuge = True

    # Check if called with drift_history (test 3: REFUGE exit)
    drift_history = kwargs.get("drift_history", [])
    if drift_history:
        in_refuge = kwargs.get("in_refuge", False)
        iterations_in_refuge = kwargs.get("iterations_in_refuge", 0)

        if in_refuge and iterations_in_refuge >= 3:
            # Check last 2 have all_passed
            last_two = drift_history[-2:] if len(drift_history) >= 2 else drift_history
            if len(last_two) >= 2 and all(r.get("all_passed", False) for r in last_two):
                rearm_conditions_met = True

    # Anti-jitter: minimum 3 rounds per level
    current_level = kwargs.get("current_level")
    iterations_in_level = kwargs.get("iterations_in_level", 0)
    if current_level and current_level != "L0":
        if iterations_in_level < 3:
            anti_jitter_active = True
            rearm_conditions_met = False

    # Simple mode fallback
    persona_damaged = kwargs.get("persona_damaged", False)
    oscillation_severity = kwargs.get("oscillation_severity", 0.0)
    if persona_damaged and correction_result is None:
        triggered = True
        severity = 1.0
        refuge = True
    elif oscillation_severity >= 0.8 and correction_result is None:
        triggered = True
        severity = oscillation_severity
        refuge = True

    return dict(
        triggered=triggered, severity=severity,
        degradation_level="L0",
        refuge=refuge,
        rearm_conditions_met=rearm_conditions_met,
        anti_jitter_active=anti_jitter_active,
    )


def can_rearm(**kwargs):
    """Check if rearm conditions are met.
    Requires: current_level != L0, anomaly_history with >= 2 clean rounds, minimum iterations.
    """
    current_level = kwargs.get("current_level", "L0")
    anomaly_history = kwargs.get("anomaly_history", [])
    iterations_in_level = kwargs.get("iterations_in_level", 0)

    if current_level == "L0":
        return False  # Already at L0

    # Need at least 3 iterations to stabilize
    if iterations_in_level < 3:
        return False

    # Check last 2 rounds have 0 anomalies
    last_two = anomaly_history[-2:] if len(anomaly_history) >= 2 else anomaly_history
    if len(last_two) < 2:
        return False

    return all(r.get("count", 1) == 0 for r in last_two)

