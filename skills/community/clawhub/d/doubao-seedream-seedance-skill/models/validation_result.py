from typing import Any, Dict, List, Optional


class ValidationResult:
    """Lightweight validation result model used by volcengine-api.

    This model intentionally keeps a simple surface: whether the validation
    passed, a collection of error messages, and an optional details dictionary
    with extra context.
    """

    __slots__ = ("is_valid", "errors", "details")

    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None, details: Optional[Dict[str, Any]] = None):
        self.is_valid = bool(is_valid)
        self.errors = list(errors) if errors is not None else []
        self.details = dict(details) if details is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {"is_valid": self.is_valid, "errors": self.errors, "details": self.details}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValidationResult):
            return NotImplemented
        return self.is_valid == other.is_valid and self.errors == other.errors and self.details == other.details

    def __repr__(self) -> str:
        return f"ValidationResult(is_valid={self.is_valid}, errors={self.errors}, details={self.details})"
