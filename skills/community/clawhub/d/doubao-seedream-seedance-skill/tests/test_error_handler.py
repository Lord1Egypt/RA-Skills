"""
Tests for error handling framework.

Tests verify error message generation and categorization.
"""

import pytest
from toolkit.error_handler import (
    VolcengineError,
    ErrorCategory,
    AuthenticationError,
    RateLimitError,
    InvalidInputError,
    APIError,
    NetworkError,
    FileError,
    TaskError,
    handle_api_error
)


class TestVolcengineError:
    """Test cases for base VolcengineError."""
    
    def test_basic_error_creation(self):
        """Test creating a basic error."""
        error = VolcengineError(
            message="Test error",
            category=ErrorCategory.API_ERROR
        )
        assert error.message == "Test error"
        assert error.category == ErrorCategory.API_ERROR
        assert error.retry_possible is False
    
    def test_error_with_all_fields(self):
        """Test error with all optional fields."""
        error = VolcengineError(
            message="Test error",
            category=ErrorCategory.API_ERROR,
            original_error="Original error message",
            solution="Try this solution",
            retry_possible=True,
            context={"key": "value"}
        )
        assert error.message == "Test error"
        assert error.original_error == "Original error message"
        assert error.solution == "Try this solution"
        assert error.retry_possible is True
        assert error.context == {"key": "value"}
    
    def test_to_user_message_basic(self):
        """Test user message generation."""
        error = VolcengineError(
            message="Something went wrong",
            category=ErrorCategory.API_ERROR
        )
        message = error.to_user_message()
        assert "❌ Something went wrong" in message
    
    def test_to_user_message_with_solution(self):
        """Test user message with solution."""
        error = VolcengineError(
            message="Something went wrong",
            category=ErrorCategory.API_ERROR,
            solution="Try this fix"
        )
        message = error.to_user_message()
        assert "❌ Something went wrong" in message
        assert "💡 Solution: Try this fix" in message
    
    def test_to_user_message_with_retry(self):
        """Test user message with retry indication."""
        error = VolcengineError(
            message="Temporary error",
            category=ErrorCategory.API_ERROR,
            retry_possible=True
        )
        message = error.to_user_message()
        assert "🔄 You can retry this operation" in message


class TestAuthenticationError:
    """Test cases for AuthenticationError."""
    
    def test_authentication_error(self):
        """Test authentication error creation."""
        error = AuthenticationError()
        assert error.category == ErrorCategory.AUTHENTICATION
        assert "ARK_API_KEY" in error.solution
        assert error.retry_possible is False
    
    def test_authentication_error_custom_message(self):
        """Test authentication error with custom message."""
        error = AuthenticationError(message="Invalid API key")
        assert error.message == "Invalid API key"


class TestRateLimitError:
    """Test cases for RateLimitError."""
    
    def test_rate_limit_error(self):
        """Test rate limit error creation."""
        error = RateLimitError()
        assert error.category == ErrorCategory.RATE_LIMIT
        assert error.retry_possible is True
        assert "wait" in error.solution.lower()
    
    def test_rate_limit_error_with_retry_after(self):
        """Test rate limit error with retry time."""
        error = RateLimitError(retry_after=60)
        assert error.retry_after == 60
        assert "60 seconds" in error.solution


class TestInvalidInputError:
    """Test cases for InvalidInputError."""
    
    def test_invalid_input_error(self):
        """Test invalid input error creation."""
        error = InvalidInputError(message="Invalid parameter")
        assert error.category == ErrorCategory.INVALID_INPUT
        assert error.retry_possible is False
    
    def test_invalid_input_error_with_field(self):
        """Test invalid input error with field name."""
        error = InvalidInputError(message="Width must be positive", field="width")
        assert error.field == "width"
        assert "width parameter" in error.solution


class TestAPIError:
    """Test cases for APIError."""
    
    def test_api_error(self):
        """Test API error creation."""
        error = APIError()
        assert error.category == ErrorCategory.API_ERROR
        assert error.retry_possible is True
    
    def test_api_error_with_status_code_4xx(self):
        """Test API error with 4xx status code."""
        error = APIError(status_code=400)
        assert error.status_code == 400
        assert "try again later" in error.solution.lower()
    
    def test_api_error_with_status_code_5xx(self):
        """Test API error with 5xx status code."""
        error = APIError(status_code=500)
        assert error.status_code == 500
        assert "server error" in error.solution.lower()


class TestNetworkError:
    """Test cases for NetworkError."""
    
    def test_network_error(self):
        """Test network error creation."""
        error = NetworkError()
        assert error.category == ErrorCategory.NETWORK_ERROR
        assert error.retry_possible is True
        assert "internet connection" in error.solution.lower()


class TestFileError:
    """Test cases for FileError."""
    
    def test_file_error(self):
        """Test file error creation."""
        error = FileError(message="File not found")
        assert error.category == ErrorCategory.FILE_ERROR
        assert error.retry_possible is False
    
    def test_file_error_with_path(self):
        """Test file error with file path."""
        error = FileError(message="Cannot read file", file_path="/tmp/test.png")
        assert error.file_path == "/tmp/test.png"
        assert "/tmp/test.png" in error.solution


class TestTaskError:
    """Test cases for TaskError."""
    
    def test_task_error(self):
        """Test task error creation."""
        error = TaskError(message="Task failed")
        assert error.category == ErrorCategory.TASK_ERROR
        assert error.retry_possible is True
    
    def test_task_error_with_id(self):
        """Test task error with task ID."""
        error = TaskError(message="Task timeout", task_id="task-123")
        assert error.task_id == "task-123"


class TestHandleAPIError:
    """Test cases for handle_api_error function."""
    
    def test_handle_auth_error(self):
        """Test handling authentication errors."""
        original = Exception("401 Unauthorized")
        error = handle_api_error(original)
        assert isinstance(error, AuthenticationError)
    
    def test_handle_rate_limit_error(self):
        """Test handling rate limit errors."""
        original = Exception("429 Too Many Requests")
        error = handle_api_error(original)
        assert isinstance(error, RateLimitError)
    
    def test_handle_network_error(self):
        """Test handling network errors."""
        original = Exception("Connection timeout")
        error = handle_api_error(original)
        assert isinstance(error, NetworkError)
    
    def test_handle_file_error(self):
        """Test handling file errors."""
        original = Exception("File not found")
        error = handle_api_error(original)
        assert isinstance(error, FileError)
    
    def test_handle_generic_error(self):
        """Test handling generic errors."""
        original = Exception("Unknown error occurred")
        error = handle_api_error(original)
        assert isinstance(error, APIError)
