"""
Tests for validation result model.

Tests verify the correctness of ValidationResult model and its methods.
"""

import pytest
from toolkit.models.validation import ValidationResult


class TestValidationResult:
    """Test cases for ValidationResult model."""
    
    def test_validation_result_creation(self):
        """Test that ValidationResult can be created with defaults."""
        result = ValidationResult()
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.details is None
    
    def test_validation_result_invalid(self):
        """Test ValidationResult created as invalid."""
        result = ValidationResult(is_valid=False)
        assert result.is_valid is False
    
    def test_validation_result_with_details(self):
        """Test ValidationResult with details."""
        details = {"field": "prompt", "constraint": "max_length"}
        result = ValidationResult(details=details)
        assert result.details == details
    
    def test_add_error(self):
        """Test adding error messages."""
        result = ValidationResult()
        assert result.is_valid is True
        
        result.add_error("Prompt is required")
        assert result.is_valid is False
        assert "Prompt is required" in result.errors
        
        result.add_error("Width must be positive")
        assert len(result.errors) == 2
        assert result.is_valid is False
    
    def test_add_warning(self):
        """Test adding warning messages."""
        result = ValidationResult()
        assert result.is_valid is True
        
        result.add_warning("Large image size may take longer")
        assert result.is_valid is True  # Warnings don't affect validity
        assert "Large image size may take longer" in result.warnings
        
        result.add_warning("Using default value for height")
        assert len(result.warnings) == 2
        assert result.is_valid is True
    
    def test_add_multiple_errors_and_warnings(self):
        """Test adding multiple errors and warnings."""
        result = ValidationResult()
        
        result.add_error("Error 1")
        result.add_warning("Warning 1")
        result.add_error("Error 2")
        result.add_warning("Warning 2")
        
        assert result.is_valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 2
    
    def test_validation_result_serialization(self):
        """Test that ValidationResult can be serialized to dict."""
        result = ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            details={"field": "test"}
        )
        
        result_dict = result.model_dump()
        assert result_dict["is_valid"] is False
        assert result_dict["errors"] == ["Error 1", "Error 2"]
        assert result_dict["warnings"] == ["Warning 1"]
        assert result_dict["details"]["field"] == "test"
    
    def test_validation_result_json(self):
        """Test that ValidationResult can be serialized to JSON."""
        result = ValidationResult(
            is_valid=True,
            warnings=["Minor issue"]
        )
        
        result_json = result.model_dump_json()
        assert '"is_valid":true' in result_json
        assert '"warnings":["Minor issue"]' in result_json
    
    def test_validation_result_deep_copy(self):
        """Test that ValidationResult can be deep copied."""
        result1 = ValidationResult(
            is_valid=False,
            errors=["Error"],
            details={"key": "value"}
        )
        
        result2 = result1.model_copy(deep=True)
        assert result2.is_valid is False
        assert result2.errors == ["Error"]
        assert result2.details == {"key": "value"}
        
        # Verify it's a deep copy - lists should not be shared
        result2.add_error("New error")
        assert len(result1.errors) == 1
        assert len(result2.errors) == 2
    
    def test_validation_result_immutability_of_lists(self):
        """Test that error and warning lists can be modified."""
        result = ValidationResult()
        
        # Add errors and warnings
        result.add_error("Error 1")
        result.add_warning("Warning 1")
        
        # Verify lists are mutable (not frozen)
        assert len(result.errors) == 1
        assert len(result.warnings) == 1
