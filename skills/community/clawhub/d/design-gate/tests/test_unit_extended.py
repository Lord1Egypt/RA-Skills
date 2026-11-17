"""
Extended unit tests for design gate - boundary, exception, concurrency scenarios.
"""

import pytest
import threading
from src import DesignGate, Design, Component, TechStack, ImpactScope, GateResult, RiskLevel
from src.models import VALID_RISK_LEVELS


class TestBoundaryScenarios:
    """Test boundary scenarios."""

    def test_empty_components_list(self):
        """Empty components list triggers no-components penalty."""
        gate = DesignGate()
        design = Design(title="t", description="d", components=[], dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.passed is False
        assert result.score == 50.0

    def test_none_tech_stack_in_run_all(self):
        """run_all_checks handles None tech_stack gracefully."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=None,
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert results[1].passed is False

    def test_none_impact_scope_in_run_all(self):
        """run_all_checks handles None impact_scope gracefully."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=None,
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert results[2].passed is False

    def test_empty_strings_in_tech_stack(self):
        """All-empty tech stack fails with very low score."""
        gate = DesignGate()
        stack = TechStack("", "", "")
        result = gate.check_feasibility(stack)
        assert result.passed is False
        assert result.score == 5.0

    def test_max_components_boundary(self):
        """Exactly 20 components does NOT trigger too-many penalty."""
        gate = DesignGate()
        comps = [Component(f"C{i}", "r", ["i"]) for i in range(20)]
        design = Design(title="t", description="d", components=comps, dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.score == 100.0

    def test_one_over_max_components(self):
        """21 components triggers too-many penalty."""
        gate = DesignGate()
        comps = [Component(f"C{i}", "r", ["i"]) for i in range(21)]
        design = Design(title="t", description="d", components=comps, dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.score == 90.0
        assert any("Too many" in i for i in result.details["issues"])

    def test_empty_affected_modules_list(self):
        """Empty affected modules fails."""
        gate = DesignGate()
        impact = ImpactScope([], False, False, "medium")
        result = gate.check_impact_scope(impact)
        assert result.passed is False

    def test_zero_external_deps(self):
        """Zero external deps does not trigger penalty."""
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres", [])
        result = gate.check_feasibility(stack)
        assert result.score == 100.0
        assert result.details["external_dep_count"] == 0


class TestExceptionAndDefaults:
    """Test exception handling and defaults."""

    def test_invalid_risk_level_enum_value(self):
        """Invalid risk level enum value raises ValueError."""
        with pytest.raises(ValueError):
            RiskLevel("extreme")

    def test_component_from_dict_missing_name_raises(self):
        """Component.from_dict raises KeyError when name missing."""
        with pytest.raises(KeyError):
            Component.from_dict({"responsibility": "r"})

    def test_design_from_dict_missing_title_raises(self):
        """Design.from_dict raises KeyError when title missing."""
        with pytest.raises(KeyError):
            Design.from_dict({"description": "d"})

    def test_gate_result_from_dict_partial(self):
        """GateResult.from_dict fills defaults for missing fields."""
        result = GateResult.from_dict({"check_name": "x", "passed": True, "score": 90.0})
        assert result.check_name == "x"
        assert result.message == ""
        assert result.details == {}

    def test_check_feasibility_none_tech_stack(self):
        """check_feasibility handles None tech_stack."""
        gate = DesignGate()
        result = gate.check_feasibility(None)
        assert result.passed is False
        assert result.score == 5.0

    def test_check_impact_scope_none_impact(self):
        """check_impact_scope handles None impact."""
        gate = DesignGate()
        result = gate.check_impact_scope(None)
        assert result.passed is False
        assert result.score == 50.0


class TestScoreClamping:
    """Test score clamping behavior."""

    def test_score_clamped_to_zero(self):
        """Score below zero is clamped to zero."""
        gate = DesignGate()
        stack = TechStack("", "", "", [f"d{i}" for i in range(25)])
        result = gate.check_feasibility(stack)
        assert result.score == 0.0
        assert result.passed is False

    def test_score_capped_at_hundred(self):
        """Valid design keeps score at 100 (no upper exceed)."""
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres")
        result = gate.check_feasibility(stack)
        assert result.score == 100.0

    def test_make_result_clamps_directly(self):
        """_make_result clamps out-of-range scores."""
        gate = DesignGate()
        high = gate._make_result("x", 150.0, "m", {})
        assert high.score == 100.0
        low = gate._make_result("x", -30.0, "m", {})
        assert low.score == 0.0


class TestRiskLevels:
    """Test all valid risk levels."""

    def test_risk_level_low_valid(self):
        gate = DesignGate()
        impact = ImpactScope(["m1"], False, False, "low")
        result = gate.check_impact_scope(impact)
        assert result.score == 100.0
        assert result.details["risk_level"] == "low"

    def test_risk_level_medium_valid(self):
        gate = DesignGate()
        impact = ImpactScope(["m1"], False, False, "medium")
        result = gate.check_impact_scope(impact)
        assert result.score == 100.0

    def test_risk_level_high_valid(self):
        gate = DesignGate()
        impact = ImpactScope(["m1"], False, False, "high")
        result = gate.check_impact_scope(impact)
        assert result.score == 100.0

    def test_risk_level_critical_valid(self):
        gate = DesignGate()
        impact = ImpactScope(["m1"], False, False, "critical")
        result = gate.check_impact_scope(impact)
        assert result.score == 100.0


class TestConcurrencySafety:
    """Test concurrent check safety."""

    def test_concurrent_check_architecture(self):
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
        )
        scores = []

        def run():
            scores.append(gate.check_architecture(design).score)

        threads = [threading.Thread(target=run) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(scores) == 10
        assert all(s == scores[0] for s in scores)

    def test_concurrent_check_feasibility(self):
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres")
        scores = []

        def run():
            scores.append(gate.check_feasibility(stack).score)

        threads = [threading.Thread(target=run) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(scores) == 10
        assert all(s == 100.0 for s in scores)

    def test_concurrent_run_all_checks(self):
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        counts = []

        def run():
            counts.append(len(gate.run_all_checks(design)))

        threads = [threading.Thread(target=run) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(counts) == 10
        assert all(c == 3 for c in counts)


class TestDetailsContent:
    """Test details dict content."""

    def test_architecture_details_has_component_count(self):
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C1", "r", ["i"]), Component("C2", "r", ["i"])],
            dependencies=["dep"],
        )
        result = gate.check_architecture(design)
        assert result.details["component_count"] == 2
        assert result.details["dependency_count"] == 1
        assert result.details["has_description"] is True
        assert result.details["issues"] == []

    def test_feasibility_details_has_dep_count(self):
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres", ["redis", "celery"])
        result = gate.check_feasibility(stack)
        assert result.details["external_dep_count"] == 2
        assert result.details["language"] == "python"

    def test_impact_details_has_risk_level(self):
        gate = DesignGate()
        impact = ImpactScope(["m1", "m2"], True, True, "high")
        result = gate.check_impact_scope(impact)
        assert result.details["risk_level"] == "high"
        assert result.details["breaking_changes"] is True
        assert result.details["affected_module_count"] == 2


class TestPassThresholdEdge:
    """Test pass threshold edge behavior."""

    def test_threshold_exact_boundary_pass(self):
        """Score exactly at threshold passes."""
        gate = DesignGate(pass_threshold=50.0)
        design = Design(title="t", description="d", components=[], dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.score == 50.0
        assert result.passed is True

    def test_threshold_just_above_fails(self):
        """Score below threshold fails."""
        gate = DesignGate(pass_threshold=51.0)
        design = Design(title="t", description="d", components=[], dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.score == 50.0
        assert result.passed is False

    def test_threshold_zero_passes_everything(self):
        """Threshold zero makes any clamped score pass."""
        gate = DesignGate(pass_threshold=0.0)
        stack = TechStack("", "", "", [f"d{i}" for i in range(25)])
        result = gate.check_feasibility(stack)
        assert result.score == 0.0
        assert result.passed is True
