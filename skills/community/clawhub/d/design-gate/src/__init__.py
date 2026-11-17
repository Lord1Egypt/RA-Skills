"""
Design Gate Skill
A design gate checker for architecture validation, feasibility analysis, and impact scope assessment.
"""

from .core import DesignGate
from .models import (
    Design,
    Component,
    TechStack,
    ImpactScope,
    GateResult,
    RiskLevel,
)

__version__ = "1.0.0"
__all__ = [
    "DesignGate",
    "Design",
    "Component",
    "TechStack",
    "ImpactScope",
    "GateResult",
    "RiskLevel",
]
