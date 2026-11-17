"""
Integration tests for design gate - serialization and persistence.
"""

import pytest
import json
from src import DesignGate, Design, Component, TechStack, ImpactScope, GateResult


class TestSerialization:
    """Test JSON serialization roundtrips."""

    def test_component_json_roundtrip(self):
        """Component survives JSON roundtrip."""
        comp = Component("API", "Handle requests", ["GET", "POST"])
        s = json.dumps(comp.to_dict())
        loaded = Component.from_dict(json.loads(s))
        assert loaded.name == comp.name
        assert loaded.responsibility == comp.responsibility
        assert loaded.interfaces == comp.interfaces

    def test_tech_stack_json_roundtrip(self):
        """TechStack survives JSON roundtrip."""
        stack = TechStack("python", "django", "postgres", ["redis", "celery"])
        s = json.dumps(stack.to_dict())
        loaded = TechStack.from_dict(json.loads(s))
        assert loaded.language == stack.language
        assert loaded.framework == stack.framework
        assert loaded.database == stack.database
        assert loaded.external_deps == stack.external_deps

    def test_impact_scope_json_roundtrip(self):
        """ImpactScope survives JSON roundtrip."""
        impact = ImpactScope(["m1", "m2"], True, True, "high")
        s = json.dumps(impact.to_dict())
        loaded = ImpactScope.from_dict(json.loads(s))
        assert loaded.affected_modules == impact.affected_modules
        assert loaded.breaking_changes is True
        assert loaded.migration_needed is True
        assert loaded.risk_level == "high"

    def test_design_json_roundtrip(self):
        """Design with nested objects survives JSON roundtrip."""
        design = Design(
            title="My Design",
            description="A design",
            components=[Component("C1", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        s = json.dumps(design.to_dict())
        loaded = Design.from_dict(json.loads(s))
        assert loaded.title == design.title
        assert len(loaded.components) == 1
        assert loaded.components[0].name == "C1"
        assert loaded.tech_stack.language == "python"
        assert loaded.impact_scope.risk_level == "medium"

    def test_gate_result_json_roundtrip(self):
        """GateResult survives JSON roundtrip."""
        result = GateResult("architecture", True, 90.0, "ok", {"k": "v"})
        s = json.dumps(result.to_dict())
        loaded = GateResult.from_dict(json.loads(s))
        assert loaded.check_name == "architecture"
        assert loaded.passed is True
        assert loaded.score == 90.0
        assert loaded.details == {"k": "v"}

    def test_design_with_none_tech_stack_serialize(self):
        """Design with None tech_stack serializes to None."""
        design = Design(title="t", description="d", tech_stack=None, impact_scope=None)
        d = design.to_dict()
        assert d["tech_stack"] is None
        assert d["impact_scope"] is None
        loaded = Design.from_dict(d)
        assert loaded.tech_stack is None
        assert loaded.impact_scope is None


class TestPersistence:
    """Test persistence scenarios."""

    def test_design_persist_and_reload(self):
        """A full design can be persisted and reloaded, then checked."""
        gate = DesignGate()
        design = Design(
            title="Persisted",
            description="persisted design",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        data = design.to_dict()
        reloaded = Design.from_dict(data)
        results_before = gate.run_all_checks(design)
        results_after = gate.run_all_checks(reloaded)
        assert [r.score for r in results_before] == [r.score for r in results_after]

    def test_results_persist_and_reload(self):
        """A list of GateResults can be persisted and reloaded."""
        gate = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        serialized = json.dumps([r.to_dict() for r in results])
        reloaded = [GateResult.from_dict(d) for d in json.loads(serialized)]
        assert len(reloaded) == 3
        assert all(r.passed for r in reloaded)
        assert reloaded[0].check_name == "architecture"

    def test_full_design_roundtrip_with_nested(self):
        """Full design with multiple components roundtrips correctly."""
        design = Design(
            title="Multi",
            description="multi component",
            components=[
                Component("API", "requests", ["GET", "POST"]),
                Component("DB", "storage", ["read", "write"]),
                Component("Auth", "auth", ["login", "logout"]),
            ],
            dependencies=["dep1", "dep2"],
            tech_stack=TechStack("typescript", "react", "postgres", ["axios"]),
            impact_scope=ImpactScope(["m1", "m2"], True, True, "high"),
        )
        s = json.dumps(design.to_dict())
        loaded = Design.from_dict(json.loads(s))
        assert len(loaded.components) == 3
        assert loaded.components[2].name == "Auth"
        assert len(loaded.dependencies) == 2
        assert loaded.tech_stack.external_deps == ["axios"]
        assert loaded.impact_scope.breaking_changes is True


class TestMultiGateIntegration:
    """Test multiple gates integration."""

    def test_multiple_gates_same_design(self):
        """Multiple gates produce identical results for the same design."""
        gate1 = DesignGate()
        gate2 = DesignGate()
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        r1 = gate1.run_all_checks(design)
        r2 = gate2.run_all_checks(design)
        assert [a.score for a in r1] == [b.score for b in r2]

    def test_multiple_gates_different_thresholds(self):
        """Gates with different thresholds disagree on pass/fail."""
        strict = DesignGate(pass_threshold=95.0)
        lax = DesignGate(pass_threshold=50.0)
        # Missing interfaces only -> score 90
        design = Design(
            title="t", description="d",
            components=[Component("C", "r", [])],
            dependencies=["dep"],
        )
        strict_result = strict.check_architecture(design)
        lax_result = lax.check_architecture(design)
        assert strict_result.score == 90.0
        assert strict_result.passed is False
        assert lax_result.passed is True


class TestCombinedChecks:
    """Test combined check scenarios."""

    def test_run_all_with_full_valid_design(self):
        """A fully valid design passes all checks overall."""
        gate = DesignGate()
        design = Design(
            title="Full",
            description="full valid design",
            components=[
                Component("API", "requests", ["GET"]),
                Component("DB", "storage", ["read"]),
            ],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert all(r.passed for r in results)
        assert gate.overall_pass(results) is True

    def test_run_all_with_empty_design(self):
        """An empty design fails all checks."""
        gate = DesignGate()
        design = Design(title="t", description="")
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert all(not r.passed for r in results)
        assert gate.overall_pass(results) is False


class TestEdgeSerialization:
    """Test edge-case serialization."""

    def test_empty_lists_serialization(self):
        """Empty lists serialize and reload cleanly."""
        comp = Component("C", "r", [])
        stack = TechStack("python", "django", "postgres", [])
        impact = ImpactScope([], False, False, "medium")
        for obj in (comp, stack, impact):
            s = json.dumps(obj.to_dict())
            assert json.loads(s) is not None
        # ImpactScope empty list reloads
        loaded = ImpactScope.from_dict(json.loads(json.dumps(impact.to_dict())))
        assert loaded.affected_modules == []

    def test_unicode_in_design_serialization(self):
        """Unicode content in design survives JSON roundtrip."""
        design = Design(
            title="设计标题",
            description="包含中文描述",
            components=[Component("组件", "职责", ["接口"])],
            dependencies=["依赖"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["模块1"], False, False, "medium"),
        )
        s = json.dumps(design.to_dict(), ensure_ascii=False)
        loaded = Design.from_dict(json.loads(s))
        assert loaded.title == "设计标题"
        assert loaded.description == "包含中文描述"
        assert loaded.components[0].name == "组件"
        assert loaded.impact_scope.affected_modules == ["模块1"]
