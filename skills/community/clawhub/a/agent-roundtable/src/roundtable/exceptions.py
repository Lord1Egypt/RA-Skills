"""Custom exceptions for the Roundtable library.

All exceptions inherit from both RoundtableError and ValueError
for backward compatibility with code that catches ValueError.
"""


class RoundtableError(ValueError):
    """Base exception for all roundtable errors."""


class DiscussionNotFoundError(RoundtableError):
    """Raised when a discussion ID does not match any existing discussion."""


class DiscussionNotActiveError(RoundtableError):
    """Raised when an operation requires an active discussion but it is not."""


class InvalidParticipantError(RoundtableError):
    """Raised when a participant is not valid for the given discussion."""


class InvalidSpeechOrderError(RoundtableError):
    """Raised when an unrecognized speech_order value is provided."""


class InvalidFindingTypeError(RoundtableError):
    """Raised when an unrecognized finding type is provided."""


class InvalidReplyToError(RoundtableError):
    """Raised when reply_to references a non-existent speech."""
