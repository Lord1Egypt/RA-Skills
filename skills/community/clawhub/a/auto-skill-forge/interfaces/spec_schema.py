"""Skill spec schema for --from-spec mode."""

from dataclasses import dataclass, field
from typing import Any
import yaml
from pathlib import Path


@dataclass
class SkillSpec:
    """Structured specification for generating a new Skill."""

    name: str
    purpose: str
    inputs: list[dict] = field(default_factory=list)
    outputs: list[dict] = field(default_factory=list)
    quality_criteria: list[dict] = field(default_factory=list)
    domain_knowledge: list[str] = field(default_factory=list)
    reference_skills: list[str] = field(default_factory=list)
    critical_constraints: list[str] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path) -> "SkillSpec":
        """Load a SkillSpec from a YAML file."""
        data = yaml.safe_load(path.read_text())
        return cls(
            **{k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        )

    def validate(self) -> list[str]:
        """Return a list of validation errors (empty if valid)."""
        errors = []
        if not self.name:
            errors.append("name is required")
        if not self.purpose:
            errors.append("purpose is required")
        if len(self.name) > 50:
            errors.append("name too long (max 50 chars)")
        if not self.name.replace("-", "").replace("_", "").isalnum():
            errors.append(
                "name must contain only alphanumeric, hyphens, underscores"
            )
        return errors
