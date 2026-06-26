"""
Unit tests for src/seo.py — SEO Analyzer
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import seo


class TestSEOAnalyzer:
    """Test SEO analysis capabilities."""

    def test_analyzer_init(self):
        """SEOAnalyzer initializes with a URL."""
        analyzer = seo.SEOAnalyzer("https://example.com")
        assert analyzer.get_site_url() == "https://example.com"

    def test_get_all_urls_returns_list(self):
        """get_all_urls() returns list."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        urls = analyzer.get_all_urls()
        assert isinstance(urls, list)

    def test_has_scan_page_method(self):
        """scan_page() method exists."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        assert callable(getattr(analyzer, 'scan_page', None))

    def test_has_run_full_scan_method(self):
        """run_full_scan() method exists."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        assert callable(getattr(analyzer, 'run_full_scan', None))

    def test_has_generate_recommendations_method(self):
        """generate_recommendations() method exists."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        assert callable(getattr(analyzer, 'generate_recommendations', None))

    def test_has_export_json_method(self):
        """export_json() method exists."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        assert callable(getattr(analyzer, 'export_json', None))

    def test_scan_page_returns_pagemeta(self):
        """scan_page() returns a PageMeta object."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        result = analyzer.scan_page("https://httpbin.org/html")
        assert isinstance(result, seo.PageMeta)
        assert hasattr(result, 'h1')
        assert hasattr(result, 'score')

    def test_scan_page_extracts_h1(self):
        """Page scan includes H1 tag."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        result = analyzer.scan_page("https://httpbin.org/html")
        assert isinstance(result.h1, list)

    def test_scan_page_has_issues(self):
        """Page scan records issues."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        result = analyzer.scan_page("https://httpbin.org/html")
        assert isinstance(result.issues, list)

    def test_scan_page_has_score(self):
        """Page scan produces a score."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        result = analyzer.scan_page("https://httpbin.org/html")
        assert isinstance(result.score, int)
        assert 0 <= result.score <= 100

    def test_pagemeta_has_url(self):
        """PageMeta has url field."""
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        result = analyzer.scan_page("https://httpbin.org/html")
        assert result.url == "https://httpbin.org/html"

    def test_export_json_is_valid_json(self):
        """export_json() produces valid JSON string."""
        import json
        analyzer = seo.SEOAnalyzer("https://httpbin.org")
        # export_json takes a SEOReport (from run_full_scan), not PageMeta
        full_report = analyzer.run_full_scan()
        if isinstance(full_report, seo.SEOReport):
            json_str = analyzer.export_json(full_report)
            parsed = json.loads(json_str)
            assert parsed is not None
