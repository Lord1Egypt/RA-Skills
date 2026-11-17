"""
End-to-end tests for design gate - complete real-world workflows.
"""

import pytest
import json
from src import DesignGate, Design, Component, TechStack, ImpactScope, GateResult


class TestCompleteDesignGateE2E:
    """Test complete design gate workflows."""

    def test_full_valid_design_workflow(self):
        """A complete valid design passes the entire gate."""
        gate = DesignGate()
        design = Design(
            title="User Service",
            description="User management microservice",
            components=[
                Component("UserController", "Handle HTTP", ["GET", "POST", "PUT", "DELETE"]),
                Component("UserRepository", "Persist users", ["save", "find"]),
                Component("UserValidator", "Validate input", ["validate"]),
            ],
            dependencies=["auth-service", "notification-service"],
            tech_stack=TechStack("python", "django", "postgres", ["redis", "celery"]),
            impact_scope=ImpactScope(["user-module", "auth-module"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert gate.overall_pass(results) is True
        assert all(r.score == 100.0 for r in results)

    def test_full_invalid_design_workflow(self):
        """A complete invalid design fails the entire gate."""
        gate = DesignGate()
        design = Design(
            title="",
            description="",
            components=[],
            dependencies=[],
            tech_stack=TechStack("", "", ""),
            impact_scope=ImpactScope([], False, False, "extreme"),
        )
        results = gate.run_all_checks(design)
        assert len(results) == 3
        assert gate.overall_pass(results) is False
        assert all(not r.passed for r in results)


class TestRealWorldScenariosE2E:
    """Test realistic design scenarios."""

    def test_microservice_architecture_validation(self):
        """Validate a realistic microservice design."""
        gate = DesignGate()
        design = Design(
            title="Order Service",
            description="Order processing microservice with payment integration",
            components=[
                Component("OrderAPI", "Expose REST endpoints", ["POST /orders"]),
                Component("PaymentGateway", "Integrate payments", ["charge"]),
                Component("OrderRepo", "Persist orders", ["create", "get"]),
            ],
            dependencies=["payment-provider", "inventory-service"],
            tech_stack=TechStack("java", "spring", "postgres", ["kafka"]),
            impact_scope=ImpactScope(["order", "payment"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert gate.overall_pass(results) is True
        assert results[0].details["component_count"] == 3

    def test_database_migration_design(self):
        """Validate a database migration design (breaking + migration)."""
        gate = DesignGate()
        design = Design(
            title="DB Migration",
            description="Migrate from MySQL to PostgreSQL",
            components=[
                Component("SchemaMigrator", "Migrate schema", ["migrate"]),
                Component("DataBackfill", "Backfill data", ["backfill"]),
            ],
            dependencies=["flyway"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(
                affected_modules=["db", "orm", "migrations"],
                breaking_changes=True,
                migration_needed=True,
                risk_level="high",
            ),
        )
        results = gate.run_all_checks(design)
        assert gate.overall_pass(results) is True
        assert results[2].details["risk_level"] == "high"
        assert results[2].details["breaking_changes"] is True

    def test_new_feature_design(self):
        """Validate a new feature design."""
        gate = DesignGate()
        design = Design(
            title="Search Feature",
            description="Add full-text search to the application",
            components=[
                Component("SearchIndexer", "Index content", ["index"]),
                Component("SearchQuery", "Run queries", ["search"]),
            ],
            dependencies=["elasticsearch"],
            tech_stack=TechStack("typescript", "express", "postgres"),
            impact_scope=ImpactScope(["search-module"], False, False, "low"),
        )
        results = gate.run_all_checks(design)
        assert gate.overall_pass(results) is True


class TestGateDecisionE2E:
    """Test gate pass/block decisions."""

    def test_gate_blocks_bad_design(self):
        """Gate blocks a severely deficient design."""
        gate = DesignGate()
        design = Design(
            title="Bad",
            description="",
            components=[],
            dependencies=[],
            tech_stack=TechStack("", "", ""),
            impact_scope=ImpactScope([], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert gate.overall_pass(results) is False
        blocked = [r.check_name for r in results if not r.passed]
        assert "architecture" in blocked
        assert "feasibility" in blocked
        assert "impact_scope" in blocked

    def test_gate_approves_good_design(self):
        """Gate approves a well-formed design."""
        gate = DesignGate()
        design = Design(
            title="Good",
            description="A good design",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        results = gate.run_all_checks(design)
        assert gate.overall_pass(results) is True
        approved = [r.check_name for r in results if r.passed]
        assert len(approved) == 3


class TestBatchE2E:
    """Test batch validation."""

    def test_batch_design_validation(self):
        """Validate multiple designs in batch."""
        gate = DesignGate()
        good = Design(
            title="Good",
            description="d",
            components=[Component("C", "r", ["i"])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        bad = Design(
            title="Bad",
            description="",
            components=[],
            dependencies=[],
            tech_stack=TechStack("", "", ""),
            impact_scope=ImpactScope([], False, False, "medium"),
        )
        marginal = Design(
            title="Marginal",
            description="d",
            components=[Component("C", "r", [])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        batch = [good, bad, marginal]
        outcomes = [gate.overall_pass(gate.run_all_checks(d)) for d in batch]
        assert outcomes == [True, False, True]


class TestPersistenceE2E:
    """Test end-to-end persistence."""

    def test_save_load_full_design_e2e(self):
        """A design persisted to JSON and reloaded produces identical checks."""
        gate = DesignGate()
        design = Design(
            title="Persisted Service",
            description="A persisted design validated end to end",
            components=[
                Component("API", "Handle requests", ["GET", "POST"]),
                Component("Repo", "Persist data", ["save"]),
            ],
            dependencies=["dep1", "dep2"],
            tech_stack=TechStack("python", "fastapi", "postgres", ["sqlalchemy"]),
            impact_scope=ImpactScope(["m1", "m2"], True, True, "high"),
        )
        original_results = gate.run_all_checks(design)

        # Persist and reload
        persisted = json.dumps(design.to_dict())
        reloaded = Design.from_dict(json.loads(persisted))
        reloaded_results = gate.run_all_checks(reloaded)

        assert [r.score for r in original_results] == [r.score for r in reloaded_results]
        assert [r.passed for r in original_results] == [r.passed for r in reloaded_results]
        assert gate.overall_pass(reloaded_results) is True


class TestThresholdE2E:
    """Test threshold behavior end to end."""

    def test_strict_threshold_blocks_marginal_design(self):
        """A strict threshold blocks a design that passes the default gate."""
        default_gate = DesignGate()
        strict_gate = DesignGate(pass_threshold=95.0)
        # Missing interfaces only -> architecture score 90
        marginal = Design(
            title="Marginal",
            description="d",
            components=[Component("C", "r", [])],
            dependencies=["dep"],
            tech_stack=TechStack("python", "django", "postgres"),
            impact_scope=ImpactScope(["m1"], False, False, "medium"),
        )
        default_results = default_gate.run_all_checks(marginal)
        strict_results = strict_gate.run_all_checks(marginal)
        assert default_gate.overall_pass(default_results) is True
        assert strict_gate.overall_pass(strict_results) is False
        assert strict_results[0].passed is False
