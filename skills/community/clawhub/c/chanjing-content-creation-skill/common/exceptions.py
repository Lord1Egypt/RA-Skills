from __future__ import annotations

class SkillError(Exception):
    """Base error for shared skill infrastructure."""


class SkillConfigError(SkillError):
    """Raised when local configuration is missing or invalid."""


class SkillExecutionError(SkillError):
    """Raised when a script invocation fails."""


class SkillHTTPError(SkillError):
    """Raised when an HTTP request fails."""


class SkillTimeoutError(SkillError):
    """Raised when polling or script execution exceeds timeout."""

