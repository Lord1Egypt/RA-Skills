"""
server/providers/wealthsimple.py — Wealthsimple stub implementation of BankProvider.

Full implementation is tracked in issue #31.
All methods raise NotImplementedError until that work lands.
"""

from __future__ import annotations

from server.providers.base import BankProvider


class WealthsimpleProvider(BankProvider):
    """Stub Wealthsimple implementation — not yet functional.

    See issue #31 for the full implementation roadmap.
    """

    name = "wealthsimple"

    def create_link_token(self, user_id: str) -> str:
        raise NotImplementedError("Wealthsimple provider not implemented yet — see #31")

    def exchange_public_token(self, public_token: str) -> dict:
        raise NotImplementedError("Wealthsimple provider not implemented yet — see #31")

    def sync_transactions(self, access_token: str, cursor: str | None = None) -> dict:
        raise NotImplementedError("Wealthsimple provider not implemented yet — see #31")

    def get_item_status(self, access_token: str) -> dict:
        raise NotImplementedError("Wealthsimple provider not implemented yet — see #31")
