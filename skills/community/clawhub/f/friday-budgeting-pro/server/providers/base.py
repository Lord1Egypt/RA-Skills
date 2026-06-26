"""
server/providers/base.py — Abstract base class for bank provider integrations.

All bank provider implementations must subclass BankProvider and implement
the four abstract methods below.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BankProvider(ABC):
    """Abstract base class defining the bank provider interface."""

    #: Human-readable provider name (e.g. "plaid", "wealthsimple").
    name: str

    @abstractmethod
    def create_link_token(self, user_id: str) -> str:
        """
        Create a Link token for the given *user_id*.

        Returns the link_token string that the frontend passes to the
        provider's Link flow.

        Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
        """
        ...

    @abstractmethod
    def exchange_public_token(self, public_token: str) -> dict:
        """
        Exchange a public token for a persistent access token.

        Returns a dict with keys:
            ``access_token`` — the provider access token (plaintext; encrypt before persisting)
            ``item_id``       — the provider item ID

        Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
        """
        ...

    @abstractmethod
    def sync_transactions(self, access_token: str, cursor: str | None) -> dict:
        """
        Incrementally sync transactions for the item associated with *access_token*.

        Parameters
        ----------
        access_token : str
            Plaintext provider access token.  Caller is responsible for decrypting
            before passing here; see server.crypto.decrypt.
        cursor : str or None
            Pagination cursor from a previous call.  Pass ``None`` for the initial
            fetch (returns all historical transactions).

        Returns a dict with keys:
            ``added``       — list of added transaction objects
            ``modified``    — list of modified transaction objects
            ``removed``     — list of removed transaction objects
            ``next_cursor`` — cursor string for the next incremental call
        """
        ...

    @abstractmethod
    def get_item_status(self, access_token: str) -> dict:
        """
        Retrieve the current status of the item associated with *access_token*.

        Returns a dict with keys:
            ``error_code``    — provider error code string, or None
            ``error_message`` — human-readable error message, or None
            ``item_id``       — provider item ID
        """
        ...
