"""
tests/test_wealthsimple_plaid.py — Verify Wealthsimple can connect via Plaid.

Wealthsimple Cash is supported by Plaid as a standard Canadian institution.
These tests confirm that:

1. PlaidProvider.create_link_token() does NOT filter by institution — any
   Plaid-supported institution (including Wealthsimple Cash) can connect.
2. The link token request uses country_codes=["CA"], which covers Wealthsimple.
3. No institution_id or institution_filter parameter is present in the request,
   which would block non-RBC/BMO institutions.

Wealthsimple Trade/Invest is NOT supported via Plaid's standard API — that
would require an unofficial route (tracked separately in issue #31 via the
wealthsimple.py stub provider).
"""

import os
import unittest
from unittest.mock import MagicMock, patch


def _env() -> dict:
    return {
        "PLAID_ENV": "sandbox",
        "PLAID_CLIENT_ID": "test-client-id",
        "PLAID_SECRET": "test-secret",
    }


def _mock_plaid_api(mock_api_cls: MagicMock) -> MagicMock:
    return mock_api_cls.return_value


class TestNoInstitutionFiltering(unittest.TestCase):
    """Confirm that create_link_token does not restrict to specific institutions."""

    @patch("server.providers.plaid.plaid_api.PlaidApi")
    def test_link_token_request_has_no_institution_id(self, mock_api_cls):
        """LinkTokenCreateRequest must NOT include an institution_id field.

        If institution_id were set, only that institution could connect via
        the Plaid Link modal — which would block Wealthsimple (and any bank
        that isn't explicitly listed).
        """
        api = _mock_plaid_api(mock_api_cls)
        api.link_token_create.return_value = {"link_token": "link-sandbox-abc123"}

        with patch.dict(os.environ, _env(), clear=False):
            from server.providers.plaid import PlaidProvider

            PlaidProvider().create_link_token()

        call_args = api.link_token_create.call_args
        self.assertIsNotNone(call_args, "link_token_create was not called")
        request = call_args[0][0]

        # Verify no institution-level restriction is present.
        # plaid-python raises AttributeError for unknown attrs, so hasattr
        # is the appropriate check here.
        self.assertFalse(
            hasattr(request, "institution_id") and request.institution_id,
            "institution_id should not be set — it would block all non-listed institutions",
        )

    @patch("server.providers.plaid.plaid_api.PlaidApi")
    def test_link_token_uses_canada_country_code(self, mock_api_cls):
        """CA country code must be present so Canadian institutions are available.

        Wealthsimple is a Canadian institution. If CA is absent from
        country_codes, Plaid Link would not offer it.
        """
        api = _mock_plaid_api(mock_api_cls)
        api.link_token_create.return_value = {"link_token": "link-sandbox-abc123"}

        with patch.dict(os.environ, _env(), clear=False):
            from server.providers.plaid import PlaidProvider

            PlaidProvider().create_link_token()

        call_args = api.link_token_create.call_args
        request = call_args[0][0]

        # country_codes must include CA.
        country_codes = [str(cc) for cc in request.country_codes]
        self.assertIn(
            "CA",
            country_codes,
            f"CA must be in country_codes so Canadian banks (incl. Wealthsimple) "
            f"are available; got: {country_codes}",
        )

    @patch("server.providers.plaid.plaid_api.PlaidApi")
    def test_link_token_creation_succeeds(self, mock_api_cls):
        """Smoke test: create_link_token() returns a non-empty token string."""
        api = _mock_plaid_api(mock_api_cls)
        api.link_token_create.return_value = {"link_token": "link-sandbox-wealthsimple-test-token"}

        with patch.dict(os.environ, _env(), clear=False):
            from server.providers.plaid import PlaidProvider

            token = PlaidProvider().create_link_token(user_id="wealthsimple-test-user")

        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0, "link_token must not be empty")
        api.link_token_create.assert_called_once()

    @patch("server.providers.plaid.plaid_api.PlaidApi")
    def test_any_user_id_works_for_wealthsimple_flow(self, mock_api_cls):
        """User ID is arbitrary — no institution-specific ID is required.

        This confirms any user_id (not tied to an institution) is accepted,
        which means the Plaid Link flow is institution-agnostic.
        """
        api = _mock_plaid_api(mock_api_cls)
        api.link_token_create.return_value = {"link_token": "link-sandbox-abc"}

        with patch.dict(os.environ, _env(), clear=False):
            from server.providers.plaid import PlaidProvider

            token = PlaidProvider().create_link_token(user_id="test-user-wealthsimple")

        call_args = api.link_token_create.call_args
        request = call_args[0][0]
        self.assertEqual(request.user.client_user_id, "test-user-wealthsimple")


if __name__ == "__main__":
    unittest.main()
