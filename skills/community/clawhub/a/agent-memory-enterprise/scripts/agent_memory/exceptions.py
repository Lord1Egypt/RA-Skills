"""Custom exceptions for the Agent Memory System."""


class MemoryError(Exception):
    """Base exception for all memory system errors."""


class StorageConnectionError(MemoryError):
    """Failed to connect to a storage backend."""


class MemoryNotFoundError(MemoryError):
    """Requested memory item was not found."""


class TokenBudgetExceededError(MemoryError):
    """Token budget exceeded during memory injection."""


class TaskStateError(MemoryError):
    """Invalid task state transition."""


class ConfigurationError(MemoryError):
    """Invalid configuration provided."""
