"""
Cross-validation validators module.
Each validator is a function that takes indicators and scenario, returns a finding dict or None.
"""

from typing import Dict, Any, Optional, Callable, List
from functools import wraps

# Registry of all validators
_validators: List[Callable] = []


def validator(func: Callable) -> Callable:
    """Decorator to register a validator function."""
    _validators.append(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def get_all_validators() -> List[Callable]:
    """Get all registered validators."""
    return _validators.copy()


# Import all validators to register them
from . import cv_mint_ownership, cv_concentration, cv_proxy, cv_tax_scenario

__all__ = ['validator', 'get_all_validators', 'cv_mint_ownership', 'cv_concentration', 'cv_proxy', 'cv_tax_scenario']
