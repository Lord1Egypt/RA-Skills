"""
Test suite for design gate skill - core functionality.
"""

import pytest
from src import DesignGate, Design, Component, TechStack, ImpactScope, GateResult


class TestDesignGateInit:
    """Test DesignGate initialization."""

    def test_init_default_threshold(self):
        """Default pass threshold is 60.0."""
        gate = DesignGate()
        assert gate.pass_threshold == 60.0

    def test_init_custom_threshold(self):
        """Custom threshold can be set."""
        gate = DesignGate(pass_threshold=80.0)
        assert gate.pass_threshold == 80.0


class TestCheckArchitecture:
    """Test check_architecture functionality."""

    def test_valid_architecture_passes(self):
        """A well-formed design passes with full score."""
        gate = DesignGate()
        design = Design(
            title="Valid Design",
            description="A valid design",
            components=[
                Component("API", "Handle requests", ["GET", "POST"]),
                Component("DB", "Store data", ["read", "write"]),
            ],
            dependencies=["auth-service"],
        )
        result = gate.check_architecture(design)
        assert result.passed is True
        assert result.score == 100.0
        assert result.check_name == "architecture"

    def test_no_components_fails(self):
        """Design without components fails."""
        gate = DesignGate()
        design = Design(
            title="Empty",
            description="desc",
            components=[],
            dependencies=["dep"],
        )
        result = gate.check_architecture(design)
        assert result.passed is False
        assert result.score == 50.0

    def test_missing_responsibility(self):
        """Missing responsibility reduces score but still passes."""
        gate = DesignGate()
        design = Design(
            title="t",
            description="d",
            components=[Component("C1", "", ["i1"])],
            dependencies=["dep"],
        )
        result = gate.check_architecture(design)
        assert result.passed is True
        assert result.score == 85.0
        assert any("responsibility" in i for i in result.details["issues"])

    def test_missing_interfaces(self):
        """Missing interfaces reduces score by 10."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C1", "resp", [])],
            dependencies=["dep"],
        )
        result = gate.check_architecture(design)
        assert result.score == 90.0

    def test_too_many_components(self):
        """More than 20 components triggers too-many penalty."""
        gate = DesignGate()
        comps = [Component(f"C{i}", "r", ["i"]) for i in range(25)]
        design = Design(title="t", description="d", components=comps, dependencies=["dep"])
        result = gate.check_architecture(design)
        assert result.score == 90.0
        assert any("Too many" in i for i in result.details["issues"])

    def test_no_dependencies(self):
        """No dependencies reduces score by 10."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C1", "r", ["i"])],
            dependencies=[],
        )
        result = gate.check_architecture(design)
        assert result.score == 90.0

    def test_no_description(self):
        """No description reduces score by 10."""
        gate = DesignGate()
        design = Design(
            title="t", description="",
            components=[Component("C1", "r", ["i"])],
            dependencies=["dep"],
        )
        result = gate.check_architecture(design)
        assert result.score == 90.0


class TestCheckFeasibility:
    """Test check_feasibility functionality."""

    def test_valid_stack_passes(self):
        """A known stack passes with full score."""
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres", ["redis"])
        result = gate.check_feasibility(stack)
        assert result.passed is True
        assert result.score == 100.0

    def test_no_language_fails(self):
        """Missing language fails feasibility."""
        gate = DesignGate()
        stack = TechStack("", "django", "postgres")
        result = gate.check_feasibility(stack)
        assert result.passed is False
        assert result.score == 50.0

    def test_unknown_language(self):
        """Unknown language reduces score but still passes."""
        gate = DesignGate()
        stack = TechStack("brainfuck", "django", "postgres")
        result = gate.check_feasibility(stack)
        assert result.passed is True
        assert result.score == 85.0

    def test_no_framework(self):
        """Missing framework reduces score by 25."""
        gate = DesignGate()
        stack = TechStack("python", "", "postgres")
        result = gate.check_feasibility(stack)
        assert result.score == 75.0

    def test_unknown_framework(self):
        """Unknown framework reduces score by 10."""
        gate = DesignGate()
        stack = TechStack("python", "unknown-fw", "postgres")
        result = gate.check_feasibility(stack)
        assert result.score == 90.0

    def test_no_database(self):
        """Missing database reduces score by 20."""
        gate = DesignGate()
        stack = TechStack("python", "django", "")
        result = gate.check_feasibility(stack)
        assert result.score == 80.0

    def test_too_many_deps(self):
        """More than 20 external deps triggers penalty."""
        gate = DesignGate()
        stack = TechStack("python", "django", "postgres", [f"dep{i}" for i in range(25)])
        result = gate.check_feasibility(stack)
        assert result.score == 85.0
        assert result.details["external_dep_count"] == 25


class TestCheckImpactScope:
    """Test check_impact_scope functionality."""

    def test_valid_impact_passes(self):
        """A valid impact scope passes with full score."""
        gate = DesignGate()
        impact = ImpactScope(["mod1", "mod2"], False, False, "medium")
        result = gate.check_impact_scope(impact)
        assert result.passed is True
        assert result.score == 100.0

    def test_no_affected_modules_fails(self):
        """No affected modules fails impact scope."""
        gate = DesignGate()
        impact = ImpactScope([], False, False, "medium")
        result = gate.check_impact_scope(impact)
        assert result.passed is False
        assert result.score == 50.0

    def test_invalid_risk_level(self):
        """Invalid risk level reduces score by 25."""
        gate = DesignGate()
        impact = ImpactScope(["mod1"], False, False, "extreme")
        result = gate.check_impact_scope(impact)
        assert result.score == 75.0

    def test_breaking_changes_low_risk(self):
        """Breaking changes with low risk reduces score by 20."""
        gate = DesignGate()
        impact = ImpactScope(["mod1"], True, False, "low")
        result = gate.check_impact_scope(impact)
        assert result.score == 80.0

    def test_migration_without_breaking(self):
        """Migration needed without breaking changes reduces score by 15."""
        gate = DesignGate()
        impact = ImpactScope(["mod1"], False, True, "medium")
        result = gate.check_impact_scope(impact)
        assert result.score == 85.0


class TestRunAllChecks:
    """Test run_all_checks functionality."""

    def test_run_all_returns_three_results(self):
        """run_all_checks returns exactly 3 results in order."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        names = [r.check_name for r in results]
        assert names == ["architecture", "feasibility", "impact_scope"]


class TestOverallPass:
    """Test overall_pass functionality."""

    def test_overall_pass_all_passed(self):
        """All passing results yields overall pass."""
        gate = DesignGate()
        results = [
            GateResult("a", True, 90, "ok", {}),
            GateResult("b", True, 80, "ok", {}),
        ]
        assert gate.overall_pass(results) is True

    def test_overall_fail_when_any_fails(self):
        """Any failing result yields overall fail."""
        gate = DesignGate()
        results = [
            GateResult("a", True, 90, "ok", {}),
            GateResult("b", False, 30, "bad", {}),
        ]
        assert gate.overall_pass(results) is False

    def test_overall_fail_empty(self):
        """Empty results yields overall fail."""
        gate = DesignGate()
        assert gate.overall_pass([]) is False
