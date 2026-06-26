"""Custom exception hierarchy for CADStack.

This module defines a structured exception hierarchy that enables:
- Programmatic error handling by type
- User-friendly error messages with recovery hints
- Consistent error logging and tracking
"""

from typing import Optional, List


# =============================================================================
# Constants
# =============================================================================

MAX_DIMENSION_MM = 100000.0  # 100 meters in mm - reasonable upper bound for CAD parts


class CADStackError(Exception):
    """Base exception for all CADStack errors.

    All CADStack exceptions inherit from this class, allowing callers
    to catch all CAD-related errors with a single except clause.

    Attributes:
        message: Human-readable error description
        hint: Optional suggestion for how to resolve the error
        details: Additional context for debugging
    """

    def __init__(
        self,
        message: str,
        hint: Optional[str] = None,
        details: Optional[dict] = None
    ):
        self.message = message
        self.hint = hint
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.hint:
            parts.append(f"Hint: {self.hint}")
        return "\n".join(parts)

    def to_dict(self) -> dict:
        """Convert exception to dictionary for logging/serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "hint": self.hint,
            "details": self.details,
        }


# =============================================================================
# Backend Errors
# =============================================================================

class BackendError(CADStackError):
    """Base class for backend-related errors."""
    pass


class BackendNotAvailableError(BackendError):
    """Raised when a requested CAD backend is not available.

    This typically means the CAD software is not installed or not accessible.
    """

    def __init__(self, backend_name: str, reason: Optional[str] = None):
        self.backend_name = backend_name
        message = f"CAD backend '{backend_name}' is not available"
        if reason:
            message += f": {reason}"

        hints = {
            "cadquery": "Install with: pip install cadquery",
            "freecad": "Install FreeCAD and ensure FreeCAD.so is in your Python path",
            "autocad": "AutoCAD backend requires Windows with pywin32 and AutoCAD running",
            "solidworks": "SolidWorks backend requires Windows with pywin32 and SolidWorks running",
            "fusion360": "Fusion 360 backend requires the bridge add-in to be running",
        }

        super().__init__(
            message=message,
            hint=hints.get(backend_name, f"Check that {backend_name} is properly installed"),
            details={"backend": backend_name}
        )


class BackendInitError(BackendError):
    """Raised when backend initialization fails after availability check."""
    pass


# =============================================================================
# Validation Errors
# =============================================================================

class ValidationError(CADStackError):
    """Base class for validation errors."""
    pass


class InvalidDimensionError(ValidationError):
    """Raised when a dimension value is invalid.

    Invalid values include:
    - Negative dimensions for sizes
    - Zero dimensions where positive required
    - NaN or Infinity values
    - Values outside reasonable bounds
    """

    def __init__(
        self,
        dimension_name: str,
        value: float,
        reason: str = "invalid value"
    ):
        self.dimension_name = dimension_name
        self.value = value
        message = f"Invalid dimension '{dimension_name}': {value} ({reason})"

        super().__init__(
            message=message,
            hint=f"Provide a positive number for {dimension_name}",
            details={"dimension": dimension_name, "value": value, "reason": reason}
        )


class ScriptValidationError(ValidationError):
    """Raised when a CAD script fails security validation.

    This exception is raised when dangerous patterns are detected
    in scripts that will be executed via exec().
    """

    def __init__(self, warnings: List[str]):
        self.warnings = warnings
        message = "Script validation failed - dangerous patterns detected"

        super().__init__(
            message=message,
            hint="Remove the flagged patterns from your script",
            details={"warnings": warnings}
        )


# =============================================================================
# Operation Errors
# =============================================================================

class OperationError(CADStackError):
    """Base class for operation-related errors."""
    pass


class ExportFailedError(OperationError):
    """Raised when export to a file format fails."""

    def __init__(
        self,
        format: str,
        filepath: str,
        reason: Optional[str] = None
    ):
        self.format = format
        self.filepath = filepath
        message = f"Export to {format.upper()} failed: {filepath}"
        if reason:
            message += f" ({reason})"

        hints = {
            "permission": "Check file permissions and directory access",
            "empty": "Cannot export an empty document - create objects first",
            "geometry": "Geometry may be invalid for this export format",
            "disk": "Check available disk space",
        }

        hint_key = reason.lower() if reason else None
        super().__init__(
            message=message,
            hint=hints.get(hint_key, "Check the file path and format compatibility"),
            details={"format": format, "filepath": filepath, "reason": reason}
        )


class EmptyDocumentError(OperationError):
    """Raised when attempting operations on an empty document."""

    def __init__(self, operation: str = "export"):
        self.operation = operation
        super().__init__(
            message=f"Cannot {operation}: document has no objects",
            hint="Create objects in the document before attempting this operation",
            details={"operation": operation}
        )


class BooleanOpError(OperationError):
    """Raised when a boolean operation fails."""

    def __init__(self, operation: str, reason: Optional[str] = None):
        self.operation = operation
        message = f"Boolean {operation} operation failed"
        if reason:
            message += f": {reason}"

        super().__init__(
            message=message,
            hint="Ensure both objects have valid geometry and intersect appropriately",
            details={"operation": operation, "reason": reason}
        )


class FeatureOpError(OperationError):
    """Raised when a feature operation (fillet, chamfer) fails."""

    def __init__(self, operation: str, reason: Optional[str] = None):
        self.operation = operation
        message = f"{operation.capitalize()} operation failed"
        if reason:
            message += f": {reason}"

        super().__init__(
            message=message,
            hint="Check that the radius/distance is valid for the selected edges",
            details={"operation": operation, "reason": reason}
        )


# =============================================================================
# Assembly Errors (for future Assembly API)
# =============================================================================

class AssemblyError(CADStackError):
    """Base class for assembly-related errors."""
    pass


class ConstraintError(AssemblyError):
    """Raised when an assembly constraint cannot be satisfied."""

    def __init__(self, constraint_type: str, part1: str, part2: str, reason: Optional[str] = None):
        self.constraint_type = constraint_type
        self.part1 = part1
        self.part2 = part2
        message = f"Cannot apply {constraint_type} constraint between '{part1}' and '{part2}'"
        if reason:
            message += f": {reason}"

        super().__init__(
            message=message,
            hint="Verify that both parts exist and the referenced features are valid",
            details={"constraint_type": constraint_type, "part1": part1, "part2": part2}
        )


class PartNotFoundError(AssemblyError):
    """Raised when a referenced part is not found in the assembly."""

    def __init__(self, part_name: str, available_parts: List[str] = None):
        self.part_name = part_name
        self.available_parts = available_parts or []
        message = f"Part '{part_name}' not found in assembly"

        hint = f"Available parts: {', '.join(self.available_parts)}" if self.available_parts else None
        super().__init__(
            message=message,
            hint=hint,
            details={"part_name": part_name, "available_parts": available_parts}
        )


# =============================================================================
# Template Errors (for Jinja2 templates)
# =============================================================================

class TemplateError(CADStackError):
    """Base class for template-related errors."""
    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a template file is not found."""

    def __init__(self, template_name: str, search_paths: List[str] = None):
        self.template_name = template_name
        self.search_paths = search_paths or []
        message = f"Template '{template_name}' not found"

        super().__init__(
            message=message,
            hint=f"Searched in: {', '.join(search_paths)}" if search_paths else "Check template name",
            details={"template_name": template_name, "search_paths": search_paths}
        )


class TemplateRenderError(TemplateError):
    """Raised when template rendering fails."""

    def __init__(self, template_name: str, reason: str):
        self.template_name = template_name
        message = f"Failed to render template '{template_name}': {reason}"

        super().__init__(
            message=message,
            hint="Check that all required parameters are provided",
            details={"template_name": template_name, "reason": reason}
        )


# =============================================================================
# Utility Functions
# =============================================================================

def raise_for_dimension(name: str, value: float, allow_zero: bool = False, max_value: float = MAX_DIMENSION_MM):
    """Validate a dimension value and raise InvalidDimensionError if invalid.

    Args:
        name: Name of the dimension (for error messages)
        value: The value to validate
        allow_zero: Whether zero is allowed
        max_value: Maximum allowed value (default 100m in mm)

    Raises:
        InvalidDimensionError: If the value is invalid
    """
    import math

    if value is None:
        raise InvalidDimensionError(name, value, "value is None")

    if math.isnan(value):
        raise InvalidDimensionError(name, value, "value is NaN")

    if math.isinf(value):
        raise InvalidDimensionError(name, value, "value is infinite")

    if value < 0:
        raise InvalidDimensionError(name, value, "value is negative")

    if not allow_zero and value == 0:
        raise InvalidDimensionError(name, value, "value is zero")

    if value > max_value:
        raise InvalidDimensionError(name, value, f"value exceeds maximum ({max_value})")
