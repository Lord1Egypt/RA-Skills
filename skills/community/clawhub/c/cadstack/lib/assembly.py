"""Assembly API for multi-part CAD assemblies.

This module provides functionality for creating assemblies with multiple
parts and constraints (mate, align, angle).

Architecture:
┌─────────────────────────────────────────────────────────────────┐
│                        Assembly API                              │
│  Assembly.add_part() → Assembly.add_constraint() → solve()      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Constraint Solver                           │
│  Mate | Align | Angle | Distance | Coincident                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend Layer                              │
│  Transforms parts according to solved constraints               │
└─────────────────────────────────────────────────────────────────┘
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import logging

from lib.exceptions import CADStackError, ConstraintError

logger = logging.getLogger(__name__)


class ConstraintType(Enum):
    """Types of assembly constraints."""
    MATE = "mate"           # Faces together, normals opposite
    ALIGN = "align"         # Faces together, normals same direction
    ANGLE = "angle"         # Angle between faces/edges
    DISTANCE = "distance"   # Fixed distance between features
    COINCIDENT = "coincident"  # Points/axes at same location
    PARALLEL = "parallel"   # Faces/edges parallel
    PERPENDICULAR = "perpendicular"  # Faces/edges perpendicular
    TANGENT = "tangent"     # Curve/surface tangent


class FeatureType(Enum):
    """Types of features that can be constrained."""
    FACE = "face"
    EDGE = "edge"
    VERTEX = "vertex"
    AXIS = "axis"
    PLANE = "plane"
    POINT = "point"


@dataclass
class FeatureReference:
    """Reference to a feature on a part.

    Attributes:
        part_name: Name of the part in the assembly
        feature_type: Type of feature (face, edge, vertex, etc.)
        feature_name: Name or identifier of the feature
        selection: Optional selection criteria (e.g., "top", "bottom", index)
    """
    part_name: str
    feature_type: FeatureType
    feature_name: str
    selection: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.part_name}.{self.feature_name}"


@dataclass
class Constraint:
    """Assembly constraint between two features.

    Attributes:
        constraint_type: Type of constraint
        feature1: First feature reference
        feature2: Second feature reference
        offset: Offset distance (for mate/align/distance)
        angle: Angle in degrees (for angle constraint)
        name: Optional constraint name
    """
    constraint_type: ConstraintType
    feature1: FeatureReference
    feature2: FeatureReference
    offset: float = 0.0
    angle: float = 0.0
    name: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.constraint_type.value}({self.feature1} → {self.feature2})"


@dataclass
class PartInstance:
    """Instance of a part in an assembly.

    Attributes:
        name: Unique instance name
        part_type: Type of part (from parts library or custom)
        position: (x, y, z) position
        rotation: (rx, ry, rz) rotation in degrees
        fixed: Whether the part is fixed in place
        metadata: Additional metadata (material, color, etc.)
    """
    name: str
    part_type: str
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    fixed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class AssemblyConstraintError(CADStackError):
    """Error in assembly constraint definition or solving."""

    def __init__(self, message: str, constraint: Optional[Constraint] = None):
        hint = "Check constraint references and ensure parts exist in assembly"
        super().__init__(message, hint=hint)
        self.constraint = constraint


@dataclass
class AssemblyResult:
    """Result of solving an assembly.

    Attributes:
        success: Whether the assembly was solved successfully
        positions: Dict of part_name to (x, y, z) position
        rotations: Dict of part_name to (rx, ry, rz) rotation
        warnings: List of warnings during solving
        errors: List of errors during solving
    """
    success: bool
    positions: Dict[str, Tuple[float, float, float]] = field(default_factory=dict)
    rotations: Dict[str, Tuple[float, float, float]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class Assembly:
    """Multi-part assembly with constraints.

    Example:
        >>> assembly = Assembly("bracket_assembly")
        >>> assembly.add_part("bracket", "custom", fixed=True)
        >>> assembly.add_part("screw_m3", "screw_metric")
        >>> assembly.add_constraint(
        ...     ConstraintType.MATE,
        ...     FeatureReference("bracket", FeatureType.FACE, "hole_face"),
        ...     FeatureReference("screw_m3", FeatureType.FACE, "head_bottom")
        ... )
        >>> result = assembly.solve()
    """

    def __init__(self, name: str):
        """Initialize an assembly.

        Args:
            name: Assembly name
        """
        self.name = name
        self._parts: Dict[str, PartInstance] = {}
        self._constraints: List[Constraint] = []
        self._solved = False

    def add_part(
        self,
        name: str,
        part_type: str,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        fixed: bool = False,
        **metadata
    ) -> "Assembly":
        """Add a part to the assembly.

        Args:
            name: Unique instance name
            part_type: Type of part (from parts library or custom)
            position: Initial (x, y, z) position
            rotation: Initial (rx, ry, rz) rotation in degrees
            fixed: Whether the part is fixed in place
            **metadata: Additional metadata

        Returns:
            self for method chaining

        Raises:
            AssemblyConstraintError: If part name already exists
        """
        if name in self._parts:
            raise AssemblyConstraintError(f"Part '{name}' already exists in assembly")

        self._parts[name] = PartInstance(
            name=name,
            part_type=part_type,
            position=position,
            rotation=rotation,
            fixed=fixed,
            metadata=metadata
        )
        self._solved = False
        return self

    def add_constraint(
        self,
        constraint_type: ConstraintType,
        feature1: FeatureReference,
        feature2: FeatureReference,
        offset: float = 0.0,
        angle: float = 0.0,
        name: Optional[str] = None
    ) -> "Assembly":
        """Add a constraint between two features.

        Args:
            constraint_type: Type of constraint
            feature1: First feature reference
            feature2: Second feature reference
            offset: Offset distance (for mate/align/distance)
            angle: Angle in degrees (for angle constraint)
            name: Optional constraint name

        Returns:
            self for method chaining

        Raises:
            AssemblyConstraintError: If referenced parts don't exist
        """
        # Validate part references
        if feature1.part_name not in self._parts:
            raise AssemblyConstraintError(
                f"Part '{feature1.part_name}' not found in assembly",
                constraint=None
            )
        if feature2.part_name not in self._parts:
            raise AssemblyConstraintError(
                f"Part '{feature2.part_name}' not found in assembly",
                constraint=None
            )

        constraint = Constraint(
            constraint_type=constraint_type,
            feature1=feature1,
            feature2=feature2,
            offset=offset,
            angle=angle,
            name=name or f"{constraint_type.value}_{len(self._constraints)}"
        )

        self._constraints.append(constraint)
        self._solved = False
        return self

    def mate(
        self,
        part1: str, feature1: str,
        part2: str, feature2: str,
        offset: float = 0.0
    ) -> "Assembly":
        """Add a mate constraint (faces together, normals opposite).

        Convenience method for common constraint type.

        Args:
            part1: First part name
            feature1: First feature name
            part2: Second part name
            feature2: Second feature name
            offset: Offset distance

        Returns:
            self for method chaining
        """
        return self.add_constraint(
            ConstraintType.MATE,
            FeatureReference(part1, FeatureType.FACE, feature1),
            FeatureReference(part2, FeatureType.FACE, feature2),
            offset=offset
        )

    def align(
        self,
        part1: str, feature1: str,
        part2: str, feature2: str,
        offset: float = 0.0
    ) -> "Assembly":
        """Add an align constraint (faces together, same direction).

        Convenience method for common constraint type.

        Args:
            part1: First part name
            feature1: First feature name
            part2: Second part name
            feature2: Second feature name
            offset: Offset distance

        Returns:
            self for method chaining
        """
        return self.add_constraint(
            ConstraintType.ALIGN,
            FeatureReference(part1, FeatureType.FACE, feature1),
            FeatureReference(part2, FeatureType.FACE, feature2),
            offset=offset
        )

    def distance(
        self,
        part1: str, feature1: str,
        part2: str, feature2: str,
        distance: float
    ) -> "Assembly":
        """Add a distance constraint.

        Args:
            part1: First part name
            feature1: First feature name
            part2: Second part name
            feature2: Second feature name
            distance: Distance value

        Returns:
            self for method chaining
        """
        return self.add_constraint(
            ConstraintType.DISTANCE,
            FeatureReference(part1, FeatureType.FACE, feature1),
            FeatureReference(part2, FeatureType.FACE, feature2),
            offset=distance
        )

    def angle(
        self,
        part1: str, feature1: str,
        part2: str, feature2: str,
        angle_degrees: float
    ) -> "Assembly":
        """Add an angle constraint.

        Args:
            part1: First part name
            feature1: First feature name
            part2: Second part name
            feature2: Second feature name
            angle_degrees: Angle in degrees

        Returns:
            self for method chaining
        """
        return self.add_constraint(
            ConstraintType.ANGLE,
            FeatureReference(part1, FeatureType.FACE, feature1),
            FeatureReference(part2, FeatureType.FACE, feature2),
            angle=angle_degrees
        )

    def solve(self) -> AssemblyResult:
        """Solve the assembly constraints.

        Returns:
            AssemblyResult with solved positions and rotations
        """
        result = AssemblyResult(success=True)

        # Check for fixed parts
        fixed_parts = [p for p in self._parts.values() if p.fixed]
        if not fixed_parts and self._parts:
            result.warnings.append("No fixed parts - first part will be fixed")
            # Fix the first part
            first_part = list(self._parts.values())[0]
            first_part.fixed = True

        # Initialize result with current positions
        for name, part in self._parts.items():
            result.positions[name] = part.position
            result.rotations[name] = part.rotation

        # Simple constraint solving (placeholder for full solver)
        # In a full implementation, this would use a constraint solver
        # like the one in FreeCAD's Assembly module or a custom solver
        for constraint in self._constraints:
            try:
                self._solve_constraint(constraint, result)
            except Exception as e:
                result.errors.append(f"Failed to solve {constraint}: {e}")
                result.success = False

        self._solved = result.success
        return result

    def _solve_constraint(self, constraint: Constraint, result: AssemblyResult):
        """Solve a single constraint.

        This is a simplified solver that handles basic cases.
        A full implementation would use numerical optimization.

        Args:
            constraint: Constraint to solve
            result: AssemblyResult to update
        """
        part1 = self._parts.get(constraint.feature1.part_name)
        part2 = self._parts.get(constraint.feature2.part_name)

        if not part1 or not part2:
            raise AssemblyConstraintError(
                f"Missing part in constraint: {constraint}",
                constraint=constraint
            )

        # If part2 is not fixed, move it to satisfy the constraint
        if not part2.fixed:
            if constraint.constraint_type in (ConstraintType.MATE, ConstraintType.ALIGN):
                # For mate/align, position part2 relative to part1
                p1_pos = result.positions[part1.name]
                offset = constraint.offset

                # Simple positioning: place part2 at part1's position + offset
                # In reality, this would involve feature geometry
                result.positions[part2.name] = (
                    p1_pos[0] + offset,
                    p1_pos[1],
                    p1_pos[2]
                )

            elif constraint.constraint_type == ConstraintType.DISTANCE:
                p1_pos = result.positions[part1.name]
                result.positions[part2.name] = (
                    p1_pos[0] + constraint.offset,
                    p1_pos[1],
                    p1_pos[2]
                )

            elif constraint.constraint_type == ConstraintType.ANGLE:
                # For angle, rotate part2
                r1_rot = result.rotations[part1.name]
                result.rotations[part2.name] = (
                    r1_rot[0] + constraint.angle,
                    r1_rot[1],
                    r1_rot[2]
                )

    def list_parts(self) -> List[str]:
        """List all part names in the assembly."""
        return list(self._parts.keys())

    def list_constraints(self) -> List[str]:
        """List all constraints as strings."""
        return [str(c) for c in self._constraints]

    def get_part(self, name: str) -> Optional[PartInstance]:
        """Get a part by name."""
        return self._parts.get(name)

    @property
    def part_count(self) -> int:
        """Number of parts in the assembly."""
        return len(self._parts)

    @property
    def constraint_count(self) -> int:
        """Number of constraints in the assembly."""
        return len(self._constraints)

    def clear(self):
        """Clear all parts and constraints."""
        self._parts.clear()
        self._constraints.clear()
        self._solved = False

    def to_dict(self) -> Dict[str, Any]:
        """Export assembly to dictionary for serialization."""
        return {
            "name": self.name,
            "parts": [
                {
                    "name": p.name,
                    "type": p.part_type,
                    "position": p.position,
                    "rotation": p.rotation,
                    "fixed": p.fixed,
                    "metadata": p.metadata
                }
                for p in self._parts.values()
            ],
            "constraints": [
                {
                    "type": c.constraint_type.value,
                    "feature1": str(c.feature1),
                    "feature2": str(c.feature2),
                    "offset": c.offset,
                    "angle": c.angle,
                    "name": c.name
                }
                for c in self._constraints
            ]
        }


# =============================================================================
# Convenience Functions
# =============================================================================

def create_assembly(name: str) -> Assembly:
    """Create a new assembly.

    Args:
        name: Assembly name

    Returns:
        New Assembly instance
    """
    return Assembly(name)
