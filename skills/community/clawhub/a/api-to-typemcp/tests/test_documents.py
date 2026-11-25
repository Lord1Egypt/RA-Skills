"""Tests for bounded Markdown/HTML document extraction (Task 6)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure scripts/ is importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".agents" / "scripts"))

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"


class MarkdownExtractionTests(unittest.TestCase):
    """Bounded Markdown API reference extraction."""

    def test_extracts_operations_from_markdown(self) -> None:
        """Clear METHOD /path lines produce operations with evidence."""
        from documents import extract_operations

        md = (FIXTURES / "api-reference.md").read_text()
        ops = extract_operations(md, source_kind="markdown")
        methods = {(op["method"], op["path"]) for op in ops}
        self.assertIn(("GET", "/pets"), methods)
        self.assertIn(("GET", "/pets/{petId}"), methods)
        self.assertIn(("POST", "/pets"), methods)
        self.assertIn(("DELETE", "/pets/{petId}"), methods)
        self.assertEqual(len(ops), 4)

    def test_operations_have_evidence(self) -> None:
        """Each operation carries a line-number evidence snippet."""
        from documents import extract_operations

        md = (FIXTURES / "api-reference.md").read_text()
        ops = extract_operations(md, source_kind="markdown")
        for op in ops:
            self.assertIn("evidence", op)
            self.assertIn("line", op["evidence"])
            self.assertIn("snippet", op["evidence"])
            self.assertIsInstance(op["evidence"]["line"], int)
            self.assertGreater(len(op["evidence"]["snippet"]), 0)

    def test_ambiguous_prose_produces_no_operations(self) -> None:
        """Prose without clear METHOD /path patterns yields nothing."""
        from documents import extract_operations

        text = "The API supports pets. You can create, read, update, and delete them."
        ops = extract_operations(text, source_kind="markdown")
        self.assertEqual(ops, [])

    def test_evidence_snippets_are_redacted(self) -> None:
        """Evidence is deterministic endpoint-only text, never source prose."""
        from documents import extract_operations

        md = "GET /pets api_key=supersecretvalue Authorization: Bearer TOPSECRET_123456"
        ops = extract_operations(md, source_kind="markdown")
        self.assertEqual(len(ops), 1)
        snippet = ops[0]["evidence"]["snippet"]
        self.assertEqual(snippet, "GET /pets")
        self.assertNotIn("supersecretvalue", snippet)
        self.assertNotIn("TOPSECRET_123456", snippet)

    def test_rejects_dot_segment_paths(self) -> None:
        """Paths whose runtime normalization changes the target are rejected."""
        from documents import DocumentError, extract_operations

        for path in ("/public/../admin", "/public/%2e%2e/admin", "/./admin"):
            with self.subTest(path=path):
                with self.assertRaises(DocumentError):
                    extract_operations(f"GET {path}", source_kind="markdown")

    def test_absolute_candidate_is_supported(self) -> None:
        """Clear absolute HTTP URLs are retained for intake normalization."""
        from documents import extract_operations

        ops = extract_operations("GET https://api.example.test/v1/pets", source_kind="markdown")
        self.assertEqual(ops[0]["path"], "https://api.example.test/v1/pets")


class HtmlExtractionTests(unittest.TestCase):
    """Bounded HTML API reference extraction."""

    def test_extracts_operations_from_html(self) -> None:
        """<code>GET /pets</code> inside HTML produces operations."""
        from documents import extract_operations

        html = (FIXTURES / "api-reference.html").read_text()
        ops = extract_operations(html, source_kind="html")
        methods = {(op["method"], op["path"]) for op in ops}
        self.assertIn(("GET", "/pets"), methods)
        self.assertIn(("POST", "/pets"), methods)
        self.assertIn(("GET", "/pets/{petId}"), methods)
        self.assertEqual(len(ops), 3)

    def test_html_operations_have_evidence(self) -> None:
        """HTML operations carry section/evidence context."""
        from documents import extract_operations

        html = (FIXTURES / "api-reference.html").read_text()
        ops = extract_operations(html, source_kind="html")
        for op in ops:
            self.assertIn("evidence", op)
            self.assertGreater(len(op["evidence"]["snippet"]), 0)


class DocumentSafetyTests(unittest.TestCase):
    """Safety bounds for document extraction."""

    def test_oversized_document_rejected(self) -> None:
        """Documents over the size limit are rejected."""
        from documents import DocumentError, extract_operations

        text = "GET /pets\n" * 300_000
        with self.assertRaises(DocumentError):
            extract_operations(text, source_kind="markdown")

    def test_all_document_operations_require_confirmation(self) -> None:
        """Every document-derived operation is flagged for user confirmation."""
        from documents import extract_operations

        md = (FIXTURES / "api-reference.md").read_text()
        ops = extract_operations(md, source_kind="markdown")
        for op in ops:
            self.assertTrue(
                op.get("requires_confirmation", False),
                f"Operation {op} missing requires_confirmation flag",
            )

    def test_html_tags_stripped_from_snippets(self) -> None:
        """Evidence snippets from HTML must not contain raw tags."""
        from documents import extract_operations

        html = "<p><code>GET /pets</code></p>"
        ops = extract_operations(html, source_kind="html")
        self.assertEqual(len(ops), 1)
        self.assertNotIn("<", ops[0]["evidence"]["snippet"])
        self.assertNotIn(">", ops[0]["evidence"]["snippet"])


if __name__ == "__main__":
    unittest.main()
