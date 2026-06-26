"""Tests for extraction module."""

import pytest
from email_bridge.extraction import (
    extract_verification_codes,
    extract_action_links,
    extract_from_email,
    VerificationCode,
    ActionLink,
)


class TestVerificationCodeExtraction:
    def test_numeric_code_with_context(self):
        text = "Your verification code is 123456. Enter this code to verify your account."
        codes = extract_verification_codes(text)

        assert len(codes) >= 1
        assert any(c.code == "123456" for c in codes)

    def test_chinese_verification_code(self):
        text = "您的验证码是：888999。请在5分钟内输入。"
        codes = extract_verification_codes(text)

        assert len(codes) >= 1
        assert any(c.code == "888999" for c in codes)

    def test_alphanumeric_code(self):
        text = "Your security code is: ABC123XY"
        codes = extract_verification_codes(text)

        # Should find the alphanumeric code
        assert len(codes) >= 1
        found = any("ABC" in c.code.upper() or "XY" in c.code.upper() for c in codes)
        assert found

    def test_dashed_code(self):
        text = "Enter confirmation code AB12-CD34 to continue"
        codes = extract_verification_codes(text)

        assert len(codes) >= 1
        assert any("-" in c.code for c in codes)

    def test_empty_text(self):
        codes = extract_verification_codes("")
        assert codes == []

        codes = extract_verification_codes(None)
        assert codes == []

    def test_filters_out_years(self):
        text = "In 2024 we launched our product. Your code is 1234."
        codes = extract_verification_codes(text)

        # Should find 1234 but not 2024 (it's a year)
        assert any(c.code == "1234" for c in codes)
        assert not any(c.code == "2024" for c in codes)

    def test_otp_keyword(self):
        text = "OTP: 998877"
        codes = extract_verification_codes(text)

        assert len(codes) >= 1
        assert any(c.code == "998877" for c in codes)


class TestVerificationCodeFalsePositives:
    """Tests for filtering out false positives."""

    def test_filters_order_numbers(self):
        """Order/invoice numbers should not be treated as verification codes."""
        text = "Your order #123456 has been shipped. Track your package."
        codes = extract_verification_codes(text)
        # Should not match 123456 as a verification code
        assert not any(c.code == "123456" for c in codes)

    def test_filters_invoice_numbers(self):
        """Invoice numbers should not be treated as verification codes."""
        text = "Invoice INV-123456 is due on March 30th."
        codes = extract_verification_codes(text)
        # INV-123456 should not be extracted as a verification code
        assert not any("123456" in c.code for c in codes)

    def test_filters_phone_numbers(self):
        """Phone numbers should not be treated as verification codes."""
        text = "Call us at 1234567890 for support."
        codes = extract_verification_codes(text)
        # 10-digit number should not be extracted
        assert not any(c.code == "1234567890" for c in codes)

    def test_filters_tracking_numbers(self):
        """Long tracking numbers should not be treated as verification codes."""
        text = "Tracking number: 123456789012345"
        codes = extract_verification_codes(text)
        # 15-digit number is too long for a verification code
        assert not any("123456789012345" in c.code for c in codes)

    def test_filters_credit_card_like_numbers(self):
        """Credit card-like patterns should not be treated as verification codes."""
        text = "Card ending in 123456789012"
        codes = extract_verification_codes(text)
        # 12-digit number is too long
        assert not any("123456789012" in c.code for c in codes)

    def test_real_verification_code_still_works(self):
        """Real verification codes should still be extracted."""
        text = "Your verification code is 123456. Do not share it."
        codes = extract_verification_codes(text)
        assert any(c.code == "123456" for c in codes)

    def test_real_code_with_context_still_works(self):
        """Codes with verification context should still be extracted."""
        text = "GitHub: Your security code is 789012"
        codes = extract_verification_codes(text)
        assert any(c.code == "789012" for c in codes)

    def test_filters_price_like_numbers(self):
        """Numbers that look like prices should not be codes."""
        # Note: This is tricky - 1999 could be a code or a price
        # But without context, we should be conservative
        text = "Your total is 1999 dollars."
        codes = extract_verification_codes(text)
        # Without verification context, should not extract
        assert not any(c.code == "1999" for c in codes)

    def test_filters_plain_numbers_without_context(self):
        """Plain numbers without verification context should not be extracted."""
        text = "The meeting is at 1234 Main Street, room 5678."
        codes = extract_verification_codes(text)
        # These are not verification codes
        assert not any(c.code == "1234" for c in codes)
        assert not any(c.code == "5678" for c in codes)


class TestActionLinkExtraction:
    def test_verify_link_from_text(self):
        text = "Click here to verify your email: https://example.com/verify?token=abc123"
        links = extract_action_links(text)

        assert len(links) >= 1
        verify_link = next((l for l in links if l.link_type == "verify"), None)
        assert verify_link is not None
        assert "example.com" in verify_link.url

    def test_reset_link_from_html(self):
        html = """
        <html>
        <body>
        <p>Click below to reset your password:</p>
        <a href="https://example.com/reset-password?token=xyz">Reset Password</a>
        </body>
        </html>
        """
        links = extract_action_links("", html)

        reset_link = next((l for l in links if l.link_type == "reset"), None)
        assert reset_link is not None
        assert reset_link.text == "Reset Password"

    def test_unsubscribe_link(self):
        text = "To stop receiving emails, visit https://example.com/unsubscribe"
        links = extract_action_links(text)

        unsub_link = next((l for l in links if l.link_type == "unsubscribe"), None)
        assert unsub_link is not None

    def test_multiple_links(self):
        html = """
        <a href="https://example.com/verify">Verify Email</a>
        <a href="https://example.com/reset">Reset Password</a>
        <a href="https://example.com/home">Visit Homepage</a>
        """
        links = extract_action_links("", html)

        # Should have verify and reset links (not homepage - it's not an action)
        action_types = [l.link_type for l in links]
        assert "verify" in action_types or "reset" in action_types

    def test_empty_content(self):
        links = extract_action_links("")
        # May have some links found, but no action links classified
        assert all(l.link_type == "unknown" for l in links) or len(links) == 0


class TestExtractFromEmail:
    def test_full_extraction(self):
        subject = "Your verification code"
        body_text = """
        Your verification code is 123456.

        Click here to verify: https://example.com/verify
        """
        body_html = """
        <a href="https://example.com/verify">Verify Now</a>
        """

        result = extract_from_email(subject, body_text, body_html)

        assert "codes" in result
        assert "links" in result
        assert len(result["codes"]) >= 1
        assert len(result["links"]) >= 1

    def test_chinese_email(self):
        subject = "您的验证码"
        body_text = "您的验证码是：666888，请在10分钟内使用。"

        result = extract_from_email(subject, body_text)

        assert len(result["codes"]) >= 1
        assert any(c.code == "666888" for c in result["codes"])


class TestVerificationCodeDataclass:
    def test_code_creation(self):
        code = VerificationCode(code="123456", context="GitHub")
        assert code.code == "123456"
        assert code.context == "GitHub"

    def test_optional_context(self):
        code = VerificationCode(code="123456")
        assert code.context is None


class TestActionLinkDataclass:
    def test_link_creation(self):
        link = ActionLink(
            url="https://example.com/verify",
            link_type="verify",
            domain="example.com",
            text="Verify Email"
        )
        assert link.url == "https://example.com/verify"
        assert link.link_type == "verify"
        assert link.domain == "example.com"
        assert link.text == "Verify Email"
