"""Structured exception hierarchy for discord-cli."""

from __future__ import annotations


class DiscordCLIError(Exception):
    """Base exception for discord-cli."""


class NotAuthenticatedError(DiscordCLIError):
    """Raised when the Discord token is missing or invalid."""


class RateLimitError(DiscordCLIError):
    """Raised when the Discord API rate limit is exhausted after retries."""


class GuildNotFoundError(DiscordCLIError):
    """Raised when a guild cannot be resolved by name or ID."""


class NetworkError(DiscordCLIError):
    """Raised on connection or HTTP errors."""
