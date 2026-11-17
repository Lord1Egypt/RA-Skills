"""Legal-page and confirmed-configuration tests (gntlisa5).

Checks that the owner-confirmed values (entity, jurisdiction, effective
date, refund rule, privacy principle, contact) are present in the published
documents, and that no legal page still claims placeholder-only contact
information.
"""

from pathlib import Path

import pytest

from agentsafe.config import Settings, validate_runtime_settings
from agentsafe.pricing import AUDIT_PRICING_TIERS, CUSTOM_PRICING_CONTACT_URL, pricing_summary

ROOT = Path(__file__).resolve().parent.parent
TOS = (ROOT / "TERMS_OF_SERVICE.md").read_text(encoding="utf-8")
PRIVACY = (ROOT / "PRIVACY_POLICY.md").read_text(encoding="utf-8")
REFUND = (ROOT / "REFUND_POLICY.md").read_text(encoding="utf-8")

OWNER_EMAIL = "lunanoach@gmail.com"  # owner-confirmed support address
INQUIRY_URL = "https://tally.so/r/laby7B"


class TestTermsOfService:
    def test_owner_entity_and_jurisdiction(self):
        assert "workfern" in TOS
        assert "Hong Kong" in TOS

    def test_effective_date(self):
        assert "October 21, 2026" in TOS

    def test_tier_table_matches_canonical_pricing(self):
        for _, price in AUDIT_PRICING_TIERS:
            assert price.replace("$", "") in TOS  # 0.50 / 2.50 / 5.00 / 25.00

    def test_enterprise_interception_documented(self):
        assert "ENTERPRISE_INQUIRY_REQUIRED" in TOS
        assert INQUIRY_URL in TOS
        assert "5,000" in TOS

    def test_refund_rule_present(self):
        assert "non-refundable" in TOS
        assert "full refund" in TOS

    def test_contact_email_present_in_all_documents(self):
        # the owner-confirmed support address appears in every legal document
        assert OWNER_EMAIL in TOS
        assert OWNER_EMAIL in PRIVACY
        assert OWNER_EMAIL in REFUND
        # no stale malformed-address flags remain
        assert "malformed" not in TOS
        assert "malformed" not in PRIVACY
        assert "malformed" not in REFUND

    def test_publication_note_still_requires_owner_url(self):
        assert "TODO — OWNER INPUT REQUIRED: final publication URL" in TOS


class TestRefundPolicy:
    def test_confirmed_rule_stated_verbatim(self):
        assert "AI audit reports are virtual digital products generated instantly." in REFUND
        assert "non-refundable" in REFUND
        assert "full refund" in REFUND
        assert "No additional exceptions or promises" in REFUND

    def test_maps_to_settlement_flow(self):
        assert "settles only" in REFUND or "only after" in REFUND

    def test_email_present_without_stale_flag(self):
        assert OWNER_EMAIL in REFUND
        assert "malformed" not in REFUND

    def test_consumer_protection_caveat_present(self):
        assert "consumer-protection" in REFUND


class TestPrivacyPolicy:
    def test_declared_principle_categories(self):
        for term in ("wallet address", "transaction", "contract address"):
            assert term in PRIVACY.lower()

    def test_ip_logs_disclosed_with_30_day_retention(self):
        # v2.0 policy: IP logging is explicit, bounded, and purpose-stated
        assert "IP" in PRIVACY
        assert "30 days" in PRIVACY
        assert "anti-DDoS" in PRIVACY

    def test_third_parties_documented(self):
        for party in ("PayAI", "Etherscan", "GitHub", "LLM"):
            assert party in PRIVACY

    def test_pseudonymity_caveat(self):
        assert "pseudonymous" in PRIVACY

    def test_no_invented_retention_or_encryption_guarantees(self):
        assert "TODO — OWNER INPUT" in PRIVACY  # unresolved items stay visible
        assert "encrypted" not in PRIVACY.lower()
        assert "real names" in PRIVACY  # explicit no-names statement


class TestConfirmedPaymentConfiguration:
    """gntlisa5 Section 4: Base Mainnet + confirmed payee validate cleanly."""

    PAYEE = "0x03ee35B45382d19b7BDcE1A2B1eD72Aae01c48cc"

    @pytest.mark.parametrize(
        "price,amount",
        [
            ("$0.50", "500000"),
            ("$2.50", "2500000"),
            ("$5.00", "5000000"),
            ("$25.00", "25000000"),
        ],
    )
    def test_price_amounts_are_exact_integer_units(self, price, amount):
        """The canonical pricing function quotes tier prices that convert to
        exact USDC base units (6 decimals, no floating-point)."""
        from decimal import Decimal

        from agentsafe.pricing import audit_price_for_lines

        for max_lines, tier_price in AUDIT_PRICING_TIERS:
            if tier_price == price:
                quoted = audit_price_for_lines(max_lines)
                assert quoted == price
                break
        # exact-decimal (not float) conversion: USD x 10^6 == integer units
        usd = int(Decimal(price[1:]) * 10**6)
        assert str(usd) == amount

    def test_mainnet_settings_with_confirmed_payee_validate(self):
        s = Settings(
            _env_file=None,
            INFURA_ETH_ENDPOINT="https://rpc.test",
            ETHERSCAN_API_KEY="k",
            GITHUB_TOKEN="ghp-t",
            GITHUB_REPO="owner/repo",
            LLM_PROVIDERS_JSON="[]",
            TASK_STORE="memory",
            PAYMENTS_ENABLED=True,
            X402_NETWORK="eip155:8453",
            X402_ALLOW_MAINNET=True,
            X402_PAY_TO=self.PAYEE,
            X402_SDK_VERSION="2.25.0",
            X402_FACILITATOR_URL="https://facilitator.payai.network",
            X402_PRICE="$0.01",
        )
        validate_runtime_settings(s, require_llm=False)
        assert s.X402_NETWORK == "eip155:8453"  # Base Mainnet, not Sepolia
        assert s.X402_PAY_TO.lower() == self.PAYEE.lower()

    def test_health_pricing_summary_has_enterprise_contact(self):
        s = pricing_summary()
        assert s[-1]["contact"] == CUSTOM_PRICING_CONTACT_URL
