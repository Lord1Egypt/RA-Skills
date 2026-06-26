"""
Error handling framework for Volcengine API Skill.

Provides user-friendly error messages with actionable solutions.
"""

from typing import Optional, List, Dict, Any
from enum import Enum


class ErrorCategory(str, Enum):
    """Categories of errors for better organization."""
    
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    INVALID_INPUT = "invalid_input"
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    FILE_ERROR = "file_error"
    TASK_ERROR = "task_error"


class VolcengineError(Exception):
    """
    Base exception for all Volcengine API errors.
    
    Provides user-friendly error messages and actionable solutions.
    """
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        original_error: Optional[str] = None,
        solution: Optional[str] = None,
        retry_possible: bool = False,
        context: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.category = category
        self.original_error = original_error
        self.solution = solution
        self.retry_possible = retry_possible
        self.context = context or {}
        super().__init__(self.message)
    
    def to_user_message(self) -> str:
        """Generate user-friendly error message."""
        parts = [f"❌ {self.message}"]
        
        if self.solution:
            parts.append(f"\n💡 Solution: {self.solution}")
        
        if self.retry_possible:
            parts.append("\n🔄 You can retry this operation.")
        
        return "\n".join(parts)


class AuthenticationError(VolcengineError):
    """API authentication failed."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.AUTHENTICATION,
            solution="Please check your ARK_API_KEY is set correctly. "
                    "You can set it via environment variable or configuration file.",
            retry_possible=False,
            **kwargs
        )


class RateLimitError(VolcengineError):
    """API rate limit exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None, **kwargs):
        solution = "Please wait before making more requests."
        if retry_after:
            solution = f"Please wait {retry_after} seconds before retrying."
        
        super().__init__(
            message=message,
            category=ErrorCategory.RATE_LIMIT,
            solution=solution,
            retry_possible=True,
            **kwargs
        )
        self.retry_after = retry_after


class InvalidInputError(VolcengineError):
    """Invalid input parameters provided."""
    
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        solution = f"Please check the {field} parameter." if field else "Please check your input parameters."
        
        super().__init__(
            message=message,
            category=ErrorCategory.INVALID_INPUT,
            solution=solution,
            retry_possible=False,
            **kwargs
        )
        self.field = field


class APIError(VolcengineError):
    """General API error from Volcengine."""
    
    def __init__(self, message: str = "API request failed", status_code: Optional[int] = None, **kwargs):
        solution = "Please try again later. If the problem persists, contact support."
        if status_code and status_code >= 500:
            solution = "Server error occurred. Please try again in a few moments."
        
        super().__init__(
            message=message,
            category=ErrorCategory.API_ERROR,
            solution=solution,
            retry_possible=True,
            **kwargs
        )
        self.status_code = status_code


class NetworkError(VolcengineError):
    """Network connectivity error."""
    
    def __init__(self, message: str = "Network connection failed", **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.NETWORK_ERROR,
            solution="Please check your internet connection and try again.",
            retry_possible=True,
            **kwargs
        )


class FileError(VolcengineError):
    """File operation error."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        solution = "Please check the file path and permissions."
        if file_path:
            solution = f"Please check the file: {file_path}"
        
        super().__init__(
            message=message,
            category=ErrorCategory.FILE_ERROR,
            solution=solution,
            retry_possible=False,
            **kwargs
        )
        self.file_path = file_path


class TaskError(VolcengineError):
    """Task execution error."""
    
    def __init__(self, message: str, task_id: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.TASK_ERROR,
            solution="Please check the task parameters and try again.",
            retry_possible=True,
            **kwargs
        )
        self.task_id = task_id


def handle_api_error(error: Exception) -> VolcengineError:
    """
    Convert raw API errors to user-friendly VolcengineError.
    
    Args:
        error: Original exception from API call
        
    Returns:
        Appropriate VolcengineError subclass
    """
    error_str = str(error).lower()
    
    # Authentication errors
    if "401" in error_str or "403" in error_str or "unauthorized" in error_str or "api key" in error_str:
        return AuthenticationError(original_error=str(error))
    
    # Rate limit errors
    if "429" in error_str or "rate limit" in error_str or "too many requests" in error_str:
        return RateLimitError(original_error=str(error))
    
    # Network errors
    if "connection" in error_str or "timeout" in error_str or "network" in error_str:
        return NetworkError(original_error=str(error))
    
    # File errors
    if "file" in error_str or "path" in error_str or "not found" in error_str:
        return FileError(message="File operation failed", original_error=str(error))
    
    # Default to generic API error
    return APIError(original_error=str(error))
