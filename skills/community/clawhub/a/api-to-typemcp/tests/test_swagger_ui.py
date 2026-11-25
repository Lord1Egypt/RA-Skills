"""Tests for bounded Swagger UI discovery (Task 6)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure scripts/ is importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".agents" / "scripts"))

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"


class SwaggerUIDiscoveryTests(unittest.TestCase):
    """Bounded Swagger UI config extraction."""

    def test_extracts_spec_url_from_inline_config(self) -> None:
        """SwaggerUIBundle({url: "/v3/openapi.json"}) → spec reference found."""
        from swagger_ui import extract_spec_reference

        html = (FIXTURES / "swagger-ui.html").read_text()
        ref = extract_spec_reference(html)
        self.assertIsNotNone(ref)
        self.assertEqual(ref["spec_url"], "/v3/openapi.json")
        self.assertEqual(ref["source_kind"], "swagger-ui-config")

    def test_no_spec_reference_returns_none(self) -> None:
        """HTML with no Swagger UI config returns None — no crawl attempted."""
        from swagger_ui import extract_spec_reference

        html = "<html><body><p>No API here</p></body></html>"
        ref = extract_spec_reference(html)
        self.assertIsNone(ref)

    def test_config_url_in_single_quotes(self) -> None:
        """Support url: '/api/swagger.json' (single-quote variant)."""
        from swagger_ui import extract_spec_reference

        html = """<script>
        SwaggerUIBundle({ url: '/api/swagger.json', dom_id: '#swagger-ui' });
        </script>"""
        ref = extract_spec_reference(html)
        self.assertIsNotNone(ref)
        self.assertEqual(ref["spec_url"], "/api/swagger.json")

    def test_config_url_in_double_quotes_with_spaces(self) -> None:
        """Support url : "/spec.yaml" (spaced colon variant)."""
        from swagger_ui import extract_spec_reference

        html = '<script>SwaggerUIBundle({ url : "/spec.yaml" })</script>'
        ref = extract_spec_reference(html)
        self.assertIsNotNone(ref)
        self.assertEqual(ref["spec_url"], "/spec.yaml")

    def test_url_key_alone_does_not_match(self) -> None:
        """A bare url key without SwaggerUIBundle context is not matched."""
        from swagger_ui import extract_spec_reference

        html = '<script>var url = "/not-swagger";</script>'
        ref = extract_spec_reference(html)
        self.assertIsNone(ref)

    def test_oversized_html_rejected(self) -> None:
        """HTML over the size limit is rejected."""
        from swagger_ui import SwaggerUIError, extract_spec_reference

        html = "x" * (2 * 1024 * 1024 + 1)
        with self.assertRaises(SwaggerUIError):
            extract_spec_reference(html)

    def test_unterminated_candidates_are_bounded(self) -> None:
        """Many incomplete SwaggerUIBundle prefixes must not trigger regex backtracking."""
        from swagger_ui import extract_spec_reference

        # Valid-size adversarial input: all candidates are unterminated.
        html = "SwaggerUIBundle({" * 80_000
        self.assertIsNone(extract_spec_reference(html))


if __name__ == "__main__":
    unittest.main()
