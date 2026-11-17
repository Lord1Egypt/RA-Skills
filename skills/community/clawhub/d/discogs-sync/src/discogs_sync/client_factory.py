"""Build authenticated Discogs Client instances."""

from __future__ import annotations

import discogs_client

from .auth import USER_AGENT, check_auth
from .exceptions import AuthenticationError


def build_client() -> discogs_client.Client:
    """Build a Discogs client using the configured personal access token.

    Raises AuthenticationError if no token is configured.
    """
    tokens = check_auth()
    if not tokens:
        raise AuthenticationError(
            "Not authenticated. Set DISCOGS_USER_TOKEN or run 'discogs-sync auth'."
        )

    return discogs_client.Client(USER_AGENT, user_token=tokens["user_token"])
