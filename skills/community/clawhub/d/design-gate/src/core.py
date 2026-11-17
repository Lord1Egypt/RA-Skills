"""
Design gate checker core.
"""

from typing import List, Dict
from .models import (
    Design,
    TechStack,
    ImpactScope,
    GateResult,
    VALID_RISK_LEVELS,
)


class DesignGate:
    """Design gate checker for architecture, feasibility, and impact scope validation."""

    PASS_THRESHOLD = 60.0

    # Known supported languages/frameworks for feasibility validation.
    SUPPORTED_LANGUAGES = {
        "python", "javascript", "typescript", "java",
        "go", "rust", "csharp", "ruby",
    }
    SUPPORTED_FRAMEWORKS = {
        "django", "flask", "fastapi", "react", "vue", "angular",
        "spring", "express", "gin", "rails",
    }

    def __init__(self, pass_threshold: float = None):
        self.pass_threshold = (
            pass_threshold if pass_threshold is not None else self.PASS_THRESHOLD
        )

    def _make_result(
        self, check_name: str, score: float, message: str, details: Dict
    ) -> GateResult:
        """Build a clamped GateResult."""
        clamped = max(0.0, min(100.0, float(score)))
        return GateResult(
            check_name=check_name,
            passed=clamped >= self.pass_threshold,
            score=clamped,
            message=message,
            details=details,
        )

    def check_architecture(self, design: Design) -> GateResult:
        """Check architecture reasonableness."""
        issues: List[str] = []
        score = 100.0

        components = design.components or []
        if not components:
            score -= 50.0
            issues.append("No components defined")
        else:
            missing_resp = [c.name for c in components if not c.responsibility]
            if missing_resp:
                score -= 15.0
                issues.append(f"Components missing responsibility: {missing_resp}")

            missing_iface = [c.name for c in components if not c.interfaces]
            if missing_iface:
                score -= 10.0
                issues.append(f"Components missing interfaces: {missing_iface}")

            if len(components) > 20:
                score -= 10.0
                issues.append(
                    f"Too many components ({len(components)}), consider splitting design"
                )

        if not design.dependencies:
            score -= 10.0
            issues.append("No dependencies documented")

        if not design.description:
            score -= 10.0
            issues.append("No description provided")

        message = (
            "Architecture check passed" if score >= self.pass_threshold
            else "Architecture check failed"
        )
        details = {
            "component_count": len(components),
            "dependency_count": len(design.dependencies or []),
            "issues": issues,
            "has_description": bool(design.description),
        }
        return self._make_result("architecture", score, message, details)

    def check_feasibility(self, tech_stack: TechStack) -> GateResult:
        """Check technical feasibility."""
        if tech_stack is None:
            tech_stack = TechStack("", "", "")

        issues: List[str] = []
        score = 100.0

        if not tech_stack.language:
            score -= 50.0
            issues.append("No language specified")
        elif tech_stack.language.lower() not in self.SUPPORTED_LANGUAGES:
            score -= 15.0
            issues.append(f"Unknown language: {tech_stack.language}")

        if not tech_stack.framework:
            score -= 25.0
            issues.append("No framework specified")
        elif tech_stack.framework.lower() not in self.SUPPORTED_FRAMEWORKS:
            score -= 10.0
            issues.append(f"Unknown framework: {tech_stack.framework}")

        if not tech_stack.database:
            score -= 20.0
            issues.append("No database specified")

        dep_count = len(tech_stack.external_deps or [])
        if dep_count > 20:
            score -= 15.0
            issues.append(f"Too many external dependencies ({dep_count})")

        message = (
            "Feasibility check passed" if score >= self.pass_threshold
            else "Feasibility check failed"
        )
        details = {
            "language": tech_stack.language,
            "framework": tech_stack.framework,
            "database": tech_stack.database,
            "external_dep_count": dep_count,
            "issues": issues,
        }
        return self._make_result("feasibility", score, message, details)

    def check_impact_scope(self, impact: ImpactScope) -> GateResult:
        """Check impact scope assessment."""
        if impact is None:
            impact = ImpactScope()

        issues: List[str] = []
        score = 100.0

        if not impact.affected_modules:
            score -= 50.0
            issues.append("No affected modules listed")

        if impact.risk_level not in VALID_RISK_LEVELS:
            score -= 25.0
            issues.append(f"Invalid risk level: {impact.risk_level}")
        else:
            if impact.breaking_changes and impact.risk_level == "low":
                score -= 20.0
                issues.append("Breaking changes flagged but risk level is low")

            if impact.migration_needed and not impact.breaking_changes:
                score -= 15.0
                issues.append("Migration needed but no breaking changes flagged")

        if impact.risk_level in ("high", "critical") and len(impact.affected_modules or []) > 10:
            score -= 10.0
            issues.append("High risk with many affected modules, ensure migration plan")

        message = (
            "Impact scope check passed" if score >= self.pass_threshold
            else "Impact scope check failed"
        )
        details = {
            "affected_module_count": len(impact.affected_modules or []),
            "breaking_changes": impact.breaking_changes,
            "migration_needed": impact.migration_needed,
            "risk_level": impact.risk_level,
            "issues": issues,
        }
        return self._make_result("impact_scope", score, message, details)

    def run_all_checks(self, design: Design) -> List[GateResult]:
        """Run all available checks on a design."""
        results: List[GateResult] = []
        results.append(self.check_architecture(design))

        tech_stack = design.tech_stack
        if tech_stack is None:
            tech_stack = TechStack("", "", "")
        results.append(self.check_feasibility(tech_stack))

        impact = design.impact_scope
        if impact is None:
            impact = ImpactScope()
        results.append(self.check_impact_scope(impact))
        return results

    def overall_pass(self, results: List[GateResult]) -> bool:
        """Return True only if all checks passed."""
        if not results:
            return False
        return all(r.passed for r in results)
