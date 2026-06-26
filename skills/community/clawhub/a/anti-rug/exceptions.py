"""
Custom exceptions for Anti-Rug Token Security Checker.
"""


class AntiRugError(Exception):
    """Base exception for all Anti-Rug errors."""
    pass


class NetworkError(AntiRugError):
    """Raised when network request fails (timeout, connection error)."""
    pass


class APIError(AntiRugError):
    """Raised when API returns non-success status."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class ContractNotFoundError(AntiRugError):
    """Raised when contract address is not found on the chain."""
    pass


class ParseError(AntiRugError):
    """Raised when response parsing fails."""
    pass


class UnsupportedChainError(AntiRugError):
    """Raised when chain ID is not supported."""
    pass


class ValidationError(AntiRugError):
    """Raised when input validation fails."""
    pass
