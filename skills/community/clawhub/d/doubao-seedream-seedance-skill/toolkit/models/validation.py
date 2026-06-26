"""
Validation result model for Volcengine API Skill.

This module contains the ValidationResult model for parameter validation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """
    Model for representing validation results.
    
    Tracks validation status, errors, and warnings for parameter validation.
    
    Attributes:
        is_valid: Whether validation passed
        errors: List of error messages
        warnings: List of warning messages
        details: Additional validation details
    """
    
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    details: Optional[Dict[str, Any]] = None
    
    def add_error(self, message: str) -> None:
        """
        Add an error message and mark validation as failed.
        
        Args:
            message: Error message to add
        """
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """
        Add a warning message.
        
        Args:
            message: Warning message to add
        """
        self.warnings.append(message)
