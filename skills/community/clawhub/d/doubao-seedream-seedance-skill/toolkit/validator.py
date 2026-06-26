"""
Parameter validator for Volcengine API Skill.

Validates parameters for various API operations.
"""

from typing import Any, List, Optional, Union, Dict
from toolkit.models.validation import ValidationResult


class Validator:
    """
    Parameter validator with comprehensive validation rules.
    
    Supports:
    - Type validation
    - Range validation
    - Required field validation
    - Custom validation rules
    """
    
    @staticmethod
    def validate_required(value: Any, field_name: str, result: ValidationResult) -> None:
        """Validate that a required field is present."""
        if value is None or (isinstance(value, str) and not value.strip()):
            result.add_error(f"{field_name} is required")
    
    @staticmethod
    def validate_type(
        value: Any,
        expected_type: type,
        field_name: str,
        result: ValidationResult
    ) -> None:
        """Validate value type."""
        if value is not None and not isinstance(value, expected_type):
            result.add_error(
                f"{field_name} must be {expected_type.__name__}, got {type(value).__name__}"
            )
    
    @staticmethod
    def validate_range(
        value: Union[int, float],
        min_val: Optional[Union[int, float]] = None,
        max_val: Optional[Union[int, float]] = None,
        field_name: str = "value",
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate numeric value is within range."""
        if result is None:
            result = ValidationResult()
        
        if value is None:
            return result
        
        if min_val is not None and value < min_val:
            result.add_error(f"{field_name} must be >= {min_val}, got {value}")
        
        if max_val is not None and value > max_val:
            result.add_error(f"{field_name} must be <= {max_val}, got {value}")
        
        return result
    
    @staticmethod
    def validate_string_length(
        value: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        field_name: str = "value",
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate string length."""
        if result is None:
            result = ValidationResult()
        
        if value is None:
            return result
        
        if min_length is not None and len(value) < min_length:
            result.add_error(
                f"{field_name} must be at least {min_length} characters, got {len(value)}"
            )
        
        if max_length is not None and len(value) > max_length:
            result.add_error(
                f"{field_name} must be at most {max_length} characters, got {len(value)}"
            )
        
        return result
    
    @staticmethod
    def validate_enum(
        value: Any,
        allowed_values: List[Any],
        field_name: str = "value",
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate value is in allowed list."""
        if result is None:
            result = ValidationResult()
        
        if value is None:
            return result
        
        if value not in allowed_values:
            result.add_error(
                f"{field_name} must be one of {allowed_values}, got {value}"
            )
        
        return result
    
    @staticmethod
    def validate_url(
        value: str,
        field_name: str = "url",
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate URL format."""
        if result is None:
            result = ValidationResult()
        
        if value is None:
            return result
        
        if not isinstance(value, str):
            result.add_error(f"{field_name} must be a string")
            return result
        
        if not (value.startswith("http://") or value.startswith("https://")):
            result.add_error(f"{field_name} must be a valid URL (http:// or https://)")
        
        return result
    
    @staticmethod
    def validate_image_dimensions(
        width: Optional[int],
        height: Optional[int],
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate image dimensions."""
        if result is None:
            result = ValidationResult()
        
        if width is not None:
            Validator.validate_range(width, 64, 2048, "width", result)
            if width % 64 != 0:
                result.add_warning("width should be multiple of 64 for best results")
        
        if height is not None:
            Validator.validate_range(height, 64, 2048, "height", result)
            if height % 64 != 0:
                result.add_warning("height should be multiple of 64 for best results")
        
        return result
    
    @staticmethod
    def validate_video_duration(
        duration: Optional[float],
        result: Optional[ValidationResult] = None
    ) -> ValidationResult:
        """Validate video duration."""
        if result is None:
            result = ValidationResult()
        
        if duration is not None:
            Validator.validate_range(duration, 1.0, 10.0, "duration", result)
        
        return result
    
    @staticmethod
    def validate_image_generation_params(
        prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs
    ) -> ValidationResult:
        """Validate parameters for image generation."""
        result = ValidationResult()
        
        # Validate prompt
        if prompt is not None:
            Validator.validate_string_length(prompt, 1, 1000, "prompt", result)
        else:
            result.add_error("prompt is required for image generation")
        
        # Validate dimensions
        Validator.validate_image_dimensions(width, height, result)
        
        return result
    
    @staticmethod
    def validate_video_generation_params(
        prompt: Optional[str] = None,
        duration: Optional[float] = None,
        **kwargs
    ) -> ValidationResult:
        """Validate parameters for video generation."""
        result = ValidationResult()
        
        # Validate prompt
        if prompt is not None:
            Validator.validate_string_length(prompt, 1, 1000, "prompt", result)
        else:
            result.add_error("prompt is required for video generation")
        
        # Validate duration
        Validator.validate_video_duration(duration, result)
        
        return result
