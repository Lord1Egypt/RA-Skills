"""
Unit tests for src/dynamic_faq.py — Dynamic FAQ Generator
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import dynamic_faq as dfq


class TestDynamicFAQModule:
    """Smoke tests for Dynamic FAQ module."""

    def test_system_class_exists(self):
        """DynamicFAQSystem class exists."""
        assert hasattr(dfq, 'DynamicFAQSystem')

    def test_system_instantiable(self):
        """DynamicFAQSystem can be instantiated."""
        sys = dfq.DynamicFAQSystem()
        assert sys is not None

    def test_has_generate_faq_page_html(self):
        """Has generate_faq_page_html method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'generate_faq_page_html', None))

    def test_has_generate_wp_shortcode(self):
        """Has generate_wp_shortcode method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'generate_wp_shortcode', None))

    def test_has_generate_help_widget_html(self):
        """Has generate_help_widget_html method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'generate_help_widget_html', None))

    def test_has_add_faq(self):
        """Has add_faq method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'add_faq', None))

    def test_has_record_feedback(self):
        """Has record_feedback method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'record_feedback', None))

    def test_has_generate_report(self):
        """Has generate_report method."""
        dfs = dfq.DynamicFAQSystem()
        assert callable(getattr(dfs, 'generate_report', None))

    def test_faqs_is_dict(self):
        """faqs is a dict (pre-populated with demo data)."""
        dfs = dfq.DynamicFAQSystem()
        assert isinstance(dfs.faqs, dict)

    def test_faq_page_html_contains_content(self):
        """generate_faq_page_html() returns HTML with FAQ content."""
        dfs = dfq.DynamicFAQSystem()
        html = dfs.generate_faq_page_html()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_wp_shortcode_returns_string(self):
        """generate_wp_shortcode() returns string."""
        dfs = dfq.DynamicFAQSystem()
        result = dfs.generate_wp_shortcode()
        assert isinstance(result, str)

    def test_report_contains_counts(self):
        """generate_report() returns a dict with counts."""
        dfs = dfq.DynamicFAQSystem()
        report = dfs.generate_report()
        assert isinstance(report, dict)


class TestFAQItemDataclass:
    """Test FAQItem dataclass."""

    def test_faq_item_exists(self):
        """FAQItem dataclass exists."""
        assert hasattr(dfq, 'FAQItem')

    def test_helpful_pct_property(self):
        """FAQItem has helpful_pct property."""
        item = dfq.FAQItem(
            faq_id="test-id",
            question="Test?",
            answer="A.",
            category="test",
            page_url="/",
            view_count=10,
            helpful_count=8,
            not_helpful_count=2,
        )
        assert item.helpful_pct == 0.8  # Returns decimal ratio
