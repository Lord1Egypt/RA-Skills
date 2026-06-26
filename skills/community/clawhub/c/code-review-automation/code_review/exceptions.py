"""Custom exceptions for Code Review Automation."""


class CodeReviewException(Exception):
    """Base exception for code review errors."""

    def __init__(self, message: str, suggestion: str = None):
        """
        Initialize code review exception.

        Args:
            message: Error message
            suggestion: Optional suggestion for fixing the error
        """
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)


class ConfigurationError(CodeReviewException):
    """Configuration related errors."""

    pass


class AuthenticationError(CodeReviewException):
    """Authentication related errors."""

    pass


class APIError(CodeReviewException):
    """API related errors."""

    def __init__(self, message: str, status_code: int = None, suggestion: str = None):
        """
        Initialize API error.

        Args:
            message: Error message
            status_code: Optional HTTP status code
            suggestion: Optional suggestion for fixing the error
        """
        self.status_code = status_code
        super().__init__(message, suggestion)


class RateLimitError(APIError):
    """API rate limit errors."""

    def __init__(self, message: str = None, reset_time: int = None):
        """
        Initialize rate limit error.

        Args:
            message: Error message
            reset_time: Optional Unix timestamp when rate limit resets
        """
        self.reset_time = reset_time
        message = message or "API rate limit exceeded. Please try again later."
        if reset_time:
            from datetime import datetime
            reset_dt = datetime.fromtimestamp(reset_time)
            message += f" Rate limit resets at {reset_dt.isoformat()}"
        super().__init__(message, "Wait for rate limit to reset or use API authentication")


class NetworkError(CodeReviewException):
    """Network related errors."""

    pass


class ValidationError(CodeReviewException):
    """Validation errors."""

    pass


class RepositoryError(CodeReviewException):
    """Repository related errors."""

    pass


class PullRequestError(CodeReviewException):
    """Pull request related errors."""

    pass


class DiffSizeError(ValidationError):
    """Error when diff size exceeds limit."""

    def __init__(self, actual_size: int, max_size: int):
        """
        Initialize diff size error.

        Args:
            actual_size: Actual diff size in bytes
            max_size: Maximum allowed diff size in bytes
        """
        message = f"Diff size ({actual_size} bytes) exceeds maximum allowed size ({max_size} bytes)"
        suggestion = "Consider reviewing a smaller subset of changes or increase the max_diff_size in configuration"
        super().__init__(message, suggestion)
        self.actual_size = actual_size
        self.max_size = max_size


class EmptyDiffError(ValidationError):
    """Error when diff is empty."""

    def __init__(self, pr_number: int = None):
        """
        Initialize empty diff error.

        Args:
            pr_number: Optional PR number
        """
        message = f"Pull request {pr_number} has no changes" if pr_number else "No changes found"
        suggestion = "Check if the PR contains any file changes"
        super().__init__(message, suggestion)


class ModelNotAvailableError(APIError):
    """Error when LLM model is not available."""

    def __init__(self, model: str):
        """
        Initialize model not available error.

        Args:
            model: Model name that is not available
        """
        message = f"Model '{model}' is not available or does not exist"
        suggestion = f"Check the model name and ensure it is available. Available models include: claude-3-7-sonnet-20250219, claude-3-5-sonnet-20241022"
        super().__init__(message, suggestion)
        self.model = model


class AnalysisTimeoutError(CodeReviewException):
    """Error when analysis times out."""

    def __init__(self, timeout: int):
        """
        Initialize timeout error.

        Args:
            timeout: Timeout in seconds
        """
        message = f"Analysis timed out after {timeout} seconds"
        suggestion = "Try again with a smaller diff or increase the timeout in configuration"
        super().__init__(message, suggestion)
        self.timeout = timeout
