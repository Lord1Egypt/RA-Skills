"""Tiered pricing unit tests (AgentLISA tier table)."""

import pytest

from agentsafe.explorer import SourceBundle, SourceFile
from agentsafe.pricing import (
    AUDIT_PRICING_TIERS,
    CUSTOM_PRICING_CONTACT_URL,
    MAX_AUDIT_SOURCE_LINES,
    ContractTooLargeError,
    audit_price_for_lines,
    count_source_lines,
    pricing_summary,
)


def _bundle(*line_counts: int, path: str = "c.sol") -> SourceBundle:
    files = []
    for n in line_counts:
        content = "\n".join(f"line{i};" for i in range(n)) + "\n\n"
        files.append(SourceFile(path=path, content=content))
    return SourceBundle(is_verified=True, contract_name="C", files=files)


class TestCountSourceLines:
    def test_counts_non_blank_lines_across_sol_files(self):
        assert count_source_lines(_bundle(10)) == 10
        assert count_source_lines(_bundle(10, 20)) == 30

    def test_blank_lines_are_excluded(self):
        b = SourceBundle(
            is_verified=True,
            contract_name="C",
            files=[SourceFile(path="c.sol", content="a;\n\n\nb;\n   \n")],
        )
        assert count_source_lines(b) == 2

    def test_non_sol_files_ignored(self):
        b = SourceBundle(
            is_verified=True,
            contract_name="C",
            files=[
                SourceFile(path="c.sol", content="a;\n"),
                SourceFile(path="meta.json", content="a;\nb;\n"),
            ],
        )
        assert count_source_lines(b) == 1


class TestAuditPriceForLines:
    @pytest.mark.parametrize(
        ("lines", "price"),
        [
            (0, "$0.50"),
            (1, "$0.50"),
            (100, "$0.50"),
            (101, "$2.50"),
            (500, "$2.50"),
            (501, "$5.00"),
            (1000, "$5.00"),
            (1001, "$25.00"),
            (5000, "$25.00"),
        ],
    )
    def test_tier_boundaries(self, lines, price):
        assert audit_price_for_lines(lines) == price

    def test_above_largest_tier_raises(self):
        with pytest.raises(ContractTooLargeError, match="custom pricing"):
            audit_price_for_lines(MAX_AUDIT_SOURCE_LINES + 1)

    def test_5001_lines_exactly_is_rejected(self):
        """Boundary: the 5,000-line maximum is inclusive; 5,001 must not be
        billable."""
        assert audit_price_for_lines(5000) == "$25.00"
        with pytest.raises(ContractTooLargeError):
            audit_price_for_lines(5001)

    def test_negative_lines_rejected(self):
        with pytest.raises(ValueError):
            audit_price_for_lines(-1)


class TestPricingSummary:
    def test_summary_lists_all_tiers_and_custom_contact(self):
        s = pricing_summary()
        assert [t["price"] for t in s[: len(AUDIT_PRICING_TIERS)]] == [
            p for _, p in AUDIT_PRICING_TIERS
        ]
        custom = s[-1]
        assert custom["price"] == "custom"
        assert custom["contact"] == CUSTOM_PRICING_CONTACT_URL
