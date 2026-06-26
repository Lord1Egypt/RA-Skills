"""
tests/test_providers.py — Tests for the bank provider abstraction layer.

Verifies that PlaidProvider and WealthsimpleProvider satisfy the
BankProvider interface contract.
"""

import pytest

from server.providers.base import BankProvider
from server.providers.plaid import PlaidProvider
from server.providers.wealthsimple import WealthsimpleProvider

# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class TestPlaidProviderInterface:
    def test_is_bank_provider_subclass(self):
        """PlaidProvider must be a subclass of BankProvider."""
        assert issubclass(PlaidProvider, BankProvider)

    def test_instance_is_bank_provider(self):
        """PlaidProvider instances must satisfy isinstance(obj, BankProvider)."""
        assert isinstance(PlaidProvider(), BankProvider)

    def test_name_attribute(self):
        """PlaidProvider must declare name = 'plaid'."""
        assert PlaidProvider.name == "plaid"
        assert PlaidProvider().name == "plaid"


class TestWealthsimpleProviderInterface:
    def test_is_bank_provider_subclass(self):
        """WealthsimpleProvider must be a subclass of BankProvider."""
        assert issubclass(WealthsimpleProvider, BankProvider)

    def test_instance_is_bank_provider(self):
        """WealthsimpleProvider instances must satisfy isinstance(obj, BankProvider)."""
        assert isinstance(WealthsimpleProvider(), BankProvider)

    def test_name_attribute(self):
        """WealthsimpleProvider must declare name = 'wealthsimple'."""
        assert WealthsimpleProvider.name == "wealthsimple"
        assert WealthsimpleProvider().name == "wealthsimple"

    def test_create_link_token_raises_not_implemented(self):
        """WealthsimpleProvider.create_link_token() must raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            WealthsimpleProvider().create_link_token("any-user")

    def test_exchange_public_token_raises_not_implemented(self):
        """WealthsimpleProvider.exchange_public_token() must raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            WealthsimpleProvider().exchange_public_token("any-token")

    def test_sync_transactions_raises_not_implemented(self):
        """WealthsimpleProvider.sync_transactions() must raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            WealthsimpleProvider().sync_transactions("any-token")

    def test_get_item_status_raises_not_implemented(self):
        """WealthsimpleProvider.get_item_status() must raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            WealthsimpleProvider().get_item_status("any-token")
