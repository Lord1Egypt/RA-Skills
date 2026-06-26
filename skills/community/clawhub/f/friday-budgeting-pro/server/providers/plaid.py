"""
server/providers/plaid.py — Plaid implementation of BankProvider.

Wraps the plaid-python SDK.  All business logic is ported directly from the
original server/plaid_client.py; behaviour is intentionally identical.

Environment variables
---------------------
PLAID_ENV        : sandbox | development | production  (default: sandbox)
PLAID_CLIENT_ID  : Plaid client ID (required)
PLAID_SECRET     : Plaid secret for the configured environment (required)

Security note
-------------
Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
This module never touches encryption or the database; it only communicates
with the Plaid API using plaintext tokens supplied by the caller.
"""

from __future__ import annotations

import os

import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from server.providers.base import BankProvider

# Use URL strings directly so we don't depend on which Environment constants
# the installed plaid-python version exposes (>= 14 dropped Development).
_ENV_MAP: dict[str, str] = {
    "sandbox": "https://sandbox.plaid.com",
    "development": "https://development.plaid.com",
    "production": "https://production.plaid.com",
}

_APP_NAME = "Friday Budgeting Pro"


class PlaidProvider(BankProvider):
    """Concrete Plaid implementation of the BankProvider interface.

    Parameters
    ----------
    env : str or None
        Plaid environment to use: ``'sandbox'``, ``'development'``, or
        ``'production'``.  When *None* (the default), falls back to the
        ``PLAID_ENV`` environment variable (default: ``'sandbox'``).
    client_id : str or None
        Plaid client ID.  When *None*, falls back to the ``PLAID_CLIENT_ID``
        environment variable.
    secret : str or None
        Plaid secret.  When *None*, falls back to the ``PLAID_SECRET``
        environment variable.
    """

    name = "plaid"

    def __init__(
        self,
        env: str | None = None,
        client_id: str | None = None,
        secret: str | None = None,
    ) -> None:
        resolved = (env or os.environ.get("PLAID_ENV", "sandbox")).lower()
        if resolved not in _ENV_MAP:
            raise ValueError(
                f"Invalid Plaid env '{resolved}'. Must be one of: " + ", ".join(_ENV_MAP)
            )
        self.env: str = resolved
        self._client_id: str | None = client_id
        self._secret: str | None = secret

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_client(self) -> plaid_api.PlaidApi:
        """Instantiate a PlaidApi client using ``self.env``.

        Credentials are resolved in priority order:
        1. Values passed directly to ``PlaidProvider.__init__`` (from DB)
        2. ``PLAID_CLIENT_ID`` / ``PLAID_SECRET`` environment variables
        """
        raw_env = self.env

        client_id = self._client_id or os.environ.get("PLAID_CLIENT_ID")
        if not client_id:
            raise EnvironmentError(
                "Plaid client_id is not configured. "
                "Run configure_plaid() or set PLAID_CLIENT_ID in the environment."
            )

        secret = self._secret or os.environ.get("PLAID_SECRET")
        if not secret:
            raise EnvironmentError(
                "Plaid secret is not configured. "
                "Run configure_plaid() or set PLAID_SECRET in the environment."
            )

        configuration = plaid.Configuration(
            host=_ENV_MAP[raw_env],
            api_key={
                "clientId": client_id,
                "secret": secret,
            },
        )
        api_client = plaid.ApiClient(configuration)
        return plaid_api.PlaidApi(api_client)

    # ------------------------------------------------------------------
    # BankProvider interface
    # ------------------------------------------------------------------

    def create_link_token(self, user_id: str = "friday-bp-user") -> str:
        """
        Create a Plaid Link token for the given *user_id*.

        Returns the ``link_token`` string that the frontend passes to Plaid Link.

        Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
        """
        client = self._build_client()
        import os as _os

        # CA only — matches old working test app; US+CA causes OAuth issues with Canadian banks
        _redirect_uri = _os.environ.get("PLAID_REDIRECT_URI")
        _kwargs = dict(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name=_APP_NAME,
            products=[Products("transactions")],
            country_codes=[CountryCode("CA")],
            language="en",
        )
        if _redirect_uri:
            _kwargs["redirect_uri"] = _redirect_uri
        request = LinkTokenCreateRequest(**_kwargs)
        response = client.link_token_create(request)
        return response["link_token"]

    def exchange_public_token(self, public_token: str) -> dict:
        """
        Exchange a public token from Plaid Link for a persistent access token.

        Returns a dict with keys:
            ``access_token`` — the Plaid access token (plaintext; encrypt before persisting)
            ``item_id``       — the Plaid item ID

        Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
        """
        client = self._build_client()
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        return {
            "access_token": response["access_token"],
            "item_id": response["item_id"],
        }

    def sync_transactions(self, access_token: str, cursor: str | None = None) -> dict:
        """
        Incrementally sync transactions for the item associated with *access_token*.

        Parameters
        ----------
        access_token : str
            Plaintext Plaid access token.  Caller is responsible for decrypting
            before passing here; see server.crypto.decrypt.
        cursor : str or None
            Pagination cursor from a previous call.  Pass ``None`` for the initial
            fetch (returns all historical transactions).

        Returns a dict with keys:
            ``added``       — list of added transaction objects
            ``modified``    — list of modified transaction objects
            ``removed``     — list of removed transaction objects
            ``next_cursor`` — cursor string for the next incremental call

        Callers MUST encrypt tokens via server.crypto.encrypt before persisting.
        """
        client = self._build_client()
        kwargs: dict = {"access_token": access_token}
        if cursor is not None:
            kwargs["cursor"] = cursor

        request = TransactionsSyncRequest(**kwargs)
        response = client.transactions_sync(request)
        return {
            "added": response["added"],
            "modified": response["modified"],
            "removed": response["removed"],
            "next_cursor": response["next_cursor"],
            "accounts": response.get("accounts", []),
        }

    def get_item_status(self, access_token: str) -> dict:
        """
        Retrieve the current status of the Plaid item via /item/get.

        Returns a dict with keys:
            ``error_code``    — Plaid error code string, or None
            ``error_message`` — human-readable error message, or None
            ``item_id``       — Plaid item ID
        """
        client = self._build_client()
        request = ItemGetRequest(access_token=access_token)
        response = client.item_get(request)

        error = (
            response.get("error")
            if isinstance(response, dict)
            else getattr(response, "error", None)
        )
        item = (
            response.get("item") if isinstance(response, dict) else getattr(response, "item", None)
        )

        error_code = None
        error_message = None
        if error is not None:
            error_code = (
                error.get("error_code")
                if isinstance(error, dict)
                else getattr(error, "error_code", None)
            )
            error_message = (
                error.get("error_message")
                if isinstance(error, dict)
                else getattr(error, "error_message", None)
            )

        item_id = None
        if item is not None:
            item_id = (
                item.get("item_id") if isinstance(item, dict) else getattr(item, "item_id", None)
            )

        return {
            "error_code": error_code,
            "error_message": error_message,
            "item_id": item_id,
        }

    def get_institution_name(self, access_token: str) -> str:
        """Return institution name for an access token."""
        from plaid.model.country_code import CountryCode
        from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
        from plaid.model.item_get_request import ItemGetRequest

        client = self._build_client()
        item = client.item_get(ItemGetRequest(access_token=access_token))
        inst_id = item["item"]["institution_id"]
        inst = client.institutions_get_by_id(
            InstitutionsGetByIdRequest(
                institution_id=inst_id,
                country_codes=[CountryCode("US"), CountryCode("CA")],
            )
        )
        return inst["institution"]["name"]
