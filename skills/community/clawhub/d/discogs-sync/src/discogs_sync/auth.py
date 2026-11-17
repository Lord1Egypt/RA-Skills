"""Authentication flow for Discogs (personal access token)."""

from __future__ import annotations

import click
import discogs_client

from .config import get_tokens, save_user_token
from .exceptions import AuthenticationError

USER_AGENT = "DiscogsSyncTool/0.1"


def run_token_auth_flow() -> dict:
    """Run the personal access token authentication flow.

    Prompts for a token (input hidden), validates it via client.identity(), and stores it.
    Returns dict with user_token and username.
    """
    token = click.prompt("Enter your Discogs personal access token", hide_input=True)

    client = discogs_client.Client(USER_AGENT, user_token=token)

    try:
        identity = client.identity()
        username = identity.username
    except Exception as e:
        raise AuthenticationError(f"Token validation failed: {e}") from e

    save_user_token(token, username)

    return {"user_token": token, "username": username}


def check_auth() -> dict | None:
    """Return the configured personal access token settings, or None."""
    return get_tokens()
