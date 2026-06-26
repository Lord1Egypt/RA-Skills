"""
Tests for parameter validator.

Tests verify validation rules and error messages.
"""

import pytest
from toolkit.validator import Validator
from toolkit.models.validation import ValidationResult


class TestValidator:
    """Test cases for Validator."""
    
    def test_validate_required_present(self):
        """Test required validation with value present."""
        result = ValidationResult()
        Validator.validate_required("value", "field", result)
        assert result.is_valid is True
    
    def test_validate_required_missing(self):
        """Test required validation with value missing."""
        result = ValidationResult()
        Validator.validate_required(None, "field", result)
        assert result.is_valid is False
        assert "field is required" in result.errors[0]
    
    def test_validate_required_empty_string(self):
        """Test required validation with empty string."""
        result = ValidationResult()
        Validator.validate_required("", "field", result)
        assert result.is_valid is False
    
    def test_validate_type_correct(self):
        """Test type validation with correct type."""
        result = ValidationResult()
        Validator.validate_type("string", str, "field", result)
        assert result.is_valid is True
    
    def test_validate_type_incorrect(self):
        """Test type validation with incorrect type."""
        result = ValidationResult()
        Validator.validate_type("string", int, "field", result)
        assert result.is_valid is False
        assert "must be int" in result.errors[0]
    
    def test_validate_type_none_allowed(self):
        """Test type validation with None value."""
        result = ValidationResult()
        Validator.validate_type(None, int, "field", result)
        assert result.is_valid is True
    
    def test_validate_range_in_range(self):
        """Test range validation with value in range."""
        result = Validator.validate_range(5, min_val=1, max_val=10)
        assert result.is_valid is True
    
    def test_validate_range_below_min(self):
        """Test range validation with value below min."""
        result = Validator.validate_range(0, min_val=1, field_name="value")
        assert result.is_valid is False
        assert "must be >=" in result.errors[0]
    
    def test_validate_range_above_max(self):
        """Test range validation with value above max."""
        result = Validator.validate_range(11, max_val=10, field_name="value")
        assert result.is_valid is False
        assert "must be <=" in result.errors[0]
    
    def test_validate_range_none_value(self):
        """Test range validation with None value."""
        result = Validator.validate_range(None, min_val=1, max_val=10)
        assert result.is_valid is True
    
    def test_validate_string_length_valid(self):
        """Test string length validation with valid length."""
        result = Validator.validate_string_length("test", min_length=1, max_length=10)
        assert result.is_valid is True
    
    def test_validate_string_length_too_short(self):
        """Test string length validation with too short string."""
        result = Validator.validate_string_length("ab", min_length=3, field_name="value")
        assert result.is_valid is False
        assert "at least 3 characters" in result.errors[0]
    
    def test_validate_string_length_too_long(self):
        """Test string length validation with too long string."""
        result = Validator.validate_string_length("abcdefghijk", max_length=10, field_name="value")
        assert result.is_valid is False
        assert "at most 10 characters" in result.errors[0]
    
    def test_validate_enum_valid(self):
        """Test enum validation with valid value."""
        result = Validator.validate_enum("option1", ["option1", "option2"], "field")
        assert result.is_valid is True
    
    def test_validate_enum_invalid(self):
        """Test enum validation with invalid value."""
        result = Validator.validate_enum("option3", ["option1", "option2"], "field")
        assert result.is_valid is False
        assert "must be one of" in result.errors[0]
    
    def test_validate_url_valid_http(self):
        """Test URL validation with valid HTTP URL."""
        result = Validator.validate_url("http://example.com/image.jpg")
        assert result.is_valid is True
    
    def test_validate_url_valid_https(self):
        """Test URL validation with valid HTTPS URL."""
        result = Validator.validate_url("https://example.com/image.jpg")
        assert result.is_valid is True
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URL."""
        result = Validator.validate_url("not-a-url")
        assert result.is_valid is False
        assert "must be a valid URL" in result.errors[0]
    
    def test_validate_url_not_string(self):
        """Test URL validation with non-string value."""
        result = Validator.validate_url(123, "url")
        assert result.is_valid is False
        assert "must be a string" in result.errors[0]
    
    def test_validate_image_dimensions_valid(self):
        """Test image dimensions validation with valid values."""
        result = Validator.validate_image_dimensions(1024, 768)
        assert result.is_valid is True
    
    def test_validate_image_dimensions_too_small(self):
        """Test image dimensions validation with too small values."""
        result = Validator.validate_image_dimensions(32, 32)
        assert result.is_valid is False
        assert len(result.errors) == 2
    
    def test_validate_image_dimensions_too_large(self):
        """Test image dimensions validation with too large values."""
        result = Validator.validate_image_dimensions(4096, 4096)
        assert result.is_valid is False
        assert len(result.errors) == 2
    
    def test_validate_image_dimensions_not_multiple_64(self):
        """Test image dimensions warning for non-multiple of 64."""
        result = Validator.validate_image_dimensions(100, 100)
        assert result.is_valid is True
        assert len(result.warnings) == 2
    
    def test_validate_video_duration_valid(self):
        """Test video duration validation with valid value."""
        result = Validator.validate_video_duration(5.0)
        assert result.is_valid is True
    
    def test_validate_video_duration_too_short(self):
        """Test video duration validation with too short value."""
        result = Validator.validate_video_duration(0.5)
        assert result.is_valid is False
        assert "must be >=" in result.errors[0]
    
    def test_validate_video_duration_too_long(self):
        """Test video duration validation with too long value."""
        result = Validator.validate_video_duration(15.0)
        assert result.is_valid is False
        assert "must be <=" in result.errors[0]
    
    def test_validate_image_generation_params_valid(self):
        """Test image generation params validation with valid params."""
        result = Validator.validate_image_generation_params(
            prompt="test image",
            width=1024,
            height=768
        )
        assert result.is_valid is True
    
    def test_validate_image_generation_params_missing_prompt(self):
        """Test image generation params validation without prompt."""
        result = Validator.validate_image_generation_params()
        assert result.is_valid is False
        assert "prompt is required" in result.errors[0]
    
    def test_validate_image_generation_params_invalid_dimensions(self):
        """Test image generation params validation with invalid dimensions."""
        result = Validator.validate_image_generation_params(
            prompt="test",
            width=32,
            height=4096
        )
        assert result.is_valid is False
        assert len(result.errors) >= 2
    
    def test_validate_video_generation_params_valid(self):
        """Test video generation params validation with valid params."""
        result = Validator.validate_video_generation_params(
            prompt="test video",
            duration=5.0
        )
        assert result.is_valid is True
    
    def test_validate_video_generation_params_missing_prompt(self):
        """Test video generation params validation without prompt."""
        result = Validator.validate_video_generation_params(duration=5.0)
        assert result.is_valid is False
        assert "prompt is required" in result.errors[0]
    
    def test_validate_video_generation_params_invalid_duration(self):
        """Test video generation params validation with invalid duration."""
        result = Validator.validate_video_generation_params(
            prompt="test",
            duration=20.0
        )
        assert result.is_valid is False
