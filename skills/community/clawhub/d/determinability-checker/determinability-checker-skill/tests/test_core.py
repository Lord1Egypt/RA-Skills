"""
Core Algorithm Unit Tests
Run: pytest tests/test_core.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import DeterminabilityCore
from skill.types import Config, DeterminabilityResult


def test_determined_case():
    """Simple determinable case."""
    configs = [
        Config("A", {"obs": "x", "target": 1}),
        Config("B", {"obs": "y", "target": 0}),
    ]
    result = DeterminabilityCore.check(
        configs,
        lambda C: C.data["obs"],
        lambda C: C.data["target"]
    )
    assert result.result == DeterminabilityResult.DETERMINED
    assert result.decision_table.mapping == {"x": 1, "y": 0}


def test_not_determined_case():
    """Non-determinable case: same observation, different targets."""
    configs = [
        Config("A", {"obs": "x", "target": 1}),
        Config("B", {"obs": "x", "target": 0}),
    ]
    result = DeterminabilityCore.check(
        configs,
        lambda C: C.data["obs"],
        lambda C: C.data["target"]
    )
    assert result.result == DeterminabilityResult.NOT_DETERMINED
    assert result.counterexample is not None
    assert result.counterexample.config1.config_id == "A"
    assert result.counterexample.config2.config_id == "B"


def test_evidence_cover():
    """Test evidence cover computation."""
    configs = [
        Config("C1", {"obs": "same", "tool": "code", "hash": "valid", "target": 1}),
        Config("C2", {"obs": "same", "tool": "code", "hash": "none", "target": 0}),
    ]
    evidences = [
        ("tool", lambda C: C.data["tool"]),
        ("hash", lambda C: C.data["hash"]),
    ]
    result = DeterminabilityCore.check(
        configs,
        lambda C: C.data["obs"],
        lambda C: C.data["target"],
        evidences
    )
    assert result.result == DeterminabilityResult.NOT_DETERMINED
    minimal = DeterminabilityCore.find_minimal_evidence_cover(result.conflict_graph, evidences)
    assert "hash" in minimal


if __name__ == "__main__":
    test_determined_case()
    test_not_determined_case()
    test_evidence_cover()
    print("All tests passed.")
