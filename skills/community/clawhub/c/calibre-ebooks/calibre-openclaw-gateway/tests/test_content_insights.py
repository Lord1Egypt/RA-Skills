"""Unit tests for content-insight term-frequency query building.

These tests cover the pure validation/SQL-building logic without a database, so
they run anywhere. Run with:

    .venv/bin/python -m unittest tests.test_content_insights
"""

import unittest

from app.database.postgres_db import (
    CONTENT_INSIGHT_REGCONFIGS,
    CONTENT_INSIGHT_STOPWORDS,
    build_top_terms_query,
    extract_book_search_terms,
)


class BuildTopTermsQueryTests(unittest.TestCase):
    def test_valid_regconfig_is_used(self):
        inner, _, _ = build_top_terms_query("portuguese", 1000, 4, 25)
        self.assertIn("to_tsvector('portuguese', content)", inner)
        self.assertIn("LIMIT 1000", inner)

    def test_invalid_regconfig_falls_back_to_simple(self):
        inner, _, _ = build_top_terms_query("'; DROP TABLE books;--", 500, 4, 25)
        self.assertIn("to_tsvector('simple', content)", inner)
        # The injected payload must not leak into the generated SQL.
        self.assertNotIn("DROP TABLE", inner)

    def test_sample_size_is_clamped(self):
        inner_low, _, _ = build_top_terms_query("simple", 0, 4, 25)
        self.assertIn("LIMIT 1", inner_low)
        inner_high, _, _ = build_top_terms_query("simple", 10_000_000, 4, 25)
        self.assertIn("LIMIT 50000", inner_high)

    def test_min_word_length_and_limit_are_clamped(self):
        _, min_len, limit = build_top_terms_query("simple", 1000, 0, 0)
        self.assertEqual(min_len, 1)
        self.assertEqual(limit, 1)
        _, min_len, limit = build_top_terms_query("simple", 1000, 999, 999)
        self.assertEqual(min_len, 40)
        self.assertEqual(limit, 200)

    def test_non_numeric_sample_size_raises(self):
        with self.assertRaises((TypeError, ValueError)):
            build_top_terms_query("simple", "not-a-number", 4, 25)

    def test_allow_list_and_stopwords_present(self):
        self.assertEqual(
            CONTENT_INSIGHT_REGCONFIGS, {"simple", "english", "portuguese"}
        )
        # A few representative PT/EN stopwords that must be filtered out.
        for word in ("the", "and", "de", "que", "with"):
            self.assertIn(word, CONTENT_INSIGHT_STOPWORDS)


class BookSearchTermTests(unittest.TestCase):
    def test_natural_language_query_keeps_subject_term(self):
        self.assertEqual(
            extract_book_search_terms("havia algum livro sobre catecismo?"),
            ["catecismo"],
        )

    def test_diacritics_are_normalized_for_term_extraction(self):
        self.assertEqual(
            extract_book_search_terms("Igreja Católica Apostólica Romana"),
            ["igreja", "catolica", "apostolica", "romana"],
        )


if __name__ == "__main__":
    unittest.main()
