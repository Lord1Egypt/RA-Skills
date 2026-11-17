"""Shared exception types.

Kept in their own module so `sources.py` can be imported (and API probes
run) without Playwright installed.
"""


class ApiUnavailable(RuntimeError):
    """Plain-HTTP path is blocked or refused; caller should try the browser."""


class NeedsLogin(RuntimeError):
    """The page is a login wall and no human has logged in yet."""


class Blocked(RuntimeError):
    """A bot wall would not clear."""
