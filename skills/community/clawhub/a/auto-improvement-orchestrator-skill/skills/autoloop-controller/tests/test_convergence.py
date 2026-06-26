import pytest
from convergence import compute_weighted_score, detect_oscillation, detect_plateau


class TestDetectPlateau:
    def test_no_plateau_improving(self):
        history = [
            {"weighted_score": 0.80, "decision": "keep"},
            {"weighted_score": 0.82, "decision": "keep"},
            {"weighted_score": 0.85, "decision": "keep"},
            {"weighted_score": 0.87, "decision": "keep"},
        ]
        assert detect_plateau(history, window=3) is False

    def test_plateau_detected(self):
        history = [
            {"weighted_score": 0.85, "decision": "keep"},
            {"weighted_score": 0.83, "decision": "reject"},
            {"weighted_score": 0.84, "decision": "reject"},
            {"weighted_score": 0.82, "decision": "reject"},
        ]
        assert detect_plateau(history, window=3) is True

    def test_too_few_entries(self):
        history = [{"weighted_score": 0.80, "decision": "keep"}]
        assert detect_plateau(history, window=3) is False

    def test_exact_boundary(self):
        # Best recent equals best before — still plateau
        history = [
            {"weighted_score": 0.85, "decision": "keep"},
            {"weighted_score": 0.85, "decision": "keep"},
            {"weighted_score": 0.85, "decision": "keep"},
            {"weighted_score": 0.85, "decision": "keep"},
        ]
        assert detect_plateau(history, window=3) is True


class TestDetectOscillation:
    def test_oscillation_detected(self):
        history = [
            {"weighted_score": 0.80, "decision": "keep"},
            {"weighted_score": 0.79, "decision": "reject"},
            {"weighted_score": 0.81, "decision": "keep"},
            {"weighted_score": 0.78, "decision": "reject"},
        ]
        assert detect_oscillation(history, window=4) is True

    def test_no_oscillation(self):
        history = [
            {"weighted_score": 0.80, "decision": "keep"},
            {"weighted_score": 0.82, "decision": "keep"},
            {"weighted_score": 0.83, "decision": "keep"},
            {"weighted_score": 0.85, "decision": "keep"},
        ]
        assert detect_oscillation(history, window=4) is False

    def test_too_few(self):
        history = [{"weighted_score": 0.80, "decision": "keep"}]
        assert detect_oscillation(history, window=4) is False


class TestComputeWeightedScore:
    def test_equal_weights(self):
        scores = {"a": 0.8, "b": 0.6}
        assert compute_weighted_score(scores) == pytest.approx(0.7)

    def test_custom_weights(self):
        scores = {"a": 1.0, "b": 0.0}
        weights = {"a": 0.7, "b": 0.3}
        assert compute_weighted_score(scores, weights) == pytest.approx(0.7)

    def test_empty_scores(self):
        assert compute_weighted_score({}) == 0.0
