"""
Data models for design gate.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from enum import Enum


class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class Component:
    """Component definition."""
    name: str
    responsibility: str
    interfaces: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "responsibility": self.responsibility,
            "interfaces": list(self.interfaces),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Component":
        return cls(
            name=data["name"],
            responsibility=data.get("responsibility", ""),
            interfaces=list(data.get("interfaces", [])),
        )


@dataclass
class TechStack:
    """Technology stack definition."""
    language: str
    framework: str
    database: str
    external_deps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "language": self.language,
            "framework": self.framework,
            "database": self.database,
            "external_deps": list(self.external_deps),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TechStack":
        return cls(
            language=data.get("language", ""),
            framework=data.get("framework", ""),
            database=data.get("database", ""),
            external_deps=list(data.get("external_deps", [])),
        )


@dataclass
class ImpactScope:
    """Impact scope definition."""
    affected_modules: List[str] = field(default_factory=list)
    breaking_changes: bool = False
    migration_needed: bool = False
    risk_level: str = "medium"

    def to_dict(self) -> Dict:
        return {
            "affected_modules": list(self.affected_modules),
            "breaking_changes": self.breaking_changes,
            "migration_needed": self.migration_needed,
            "risk_level": self.risk_level,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ImpactScope":
        return cls(
            affected_modules=list(data.get("affected_modules", [])),
            breaking_changes=data.get("breaking_changes", False),
            migration_needed=data.get("migration_needed", False),
            risk_level=data.get("risk_level", "medium"),
        )


@dataclass
class Design:
    """Design definition."""
    title: str
    description: str
    components: List[Component] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tech_stack: TechStack = None
    impact_scope: ImpactScope = None

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "components": [c.to_dict() for c in self.components],
            "dependencies": list(self.dependencies),
            "tech_stack": self.tech_stack.to_dict() if self.tech_stack else None,
            "impact_scope": self.impact_scope.to_dict() if self.impact_scope else None,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Design":
        tech_stack = TechStack.from_dict(data["tech_stack"]) if data.get("tech_stack") else None
        impact_scope = ImpactScope.from_dict(data["impact_scope"]) if data.get("impact_scope") else None
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            components=[Component.from_dict(c) for c in data.get("components", [])],
            dependencies=list(data.get("dependencies", [])),
            tech_stack=tech_stack,
            impact_scope=impact_scope,
        )


@dataclass
class GateResult:
    """Gate check result."""
    check_name: str
    passed: bool
    score: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "GateResult":
        return cls(
            check_name=data["check_name"],
            passed=data["passed"],
            score=data["score"],
            message=data.get("message", ""),
            details=dict(data.get("details", {})),
        )
