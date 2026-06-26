from __future__ import annotations

import unittest

from free_search.quality import (
    _tokenize,
    deduplicate_results,
    filter_low_quality,
    optimize_results,
    rerank_results,
    relevance_score,
    title_similarity,
)


class TestTokenize(unittest.TestCase):
    def test_english(self) -> None:
        tokens = _tokenize("Hello World test")
        self.assertEqual(tokens, {"hello", "world", "test"})

    def test_chinese(self) -> None:
        tokens = _tokenize("测试 搜索")
        self.assertIn("测试", tokens)
        self.assertIn("搜索", tokens)

    def test_empty(self) -> None:
        self.assertEqual(_tokenize(""), set())
        self.assertEqual(_tokenize("   "), set())


class TestRelevanceScore(unittest.TestCase):
    def test_perfect_match(self) -> None:
        score = relevance_score("python tutorial", "Python Tutorial", "Learn Python tutorial basics")
        self.assertGreater(score, 0.8)

    def test_no_match(self) -> None:
        score = relevance_score("python tutorial", "Cat Videos", "Funny animal compilation")
        self.assertLess(score, 0.1)

    def test_partial_match(self) -> None:
        score = relevance_score("python tutorial", "Python Guide", "A comprehensive guide")
        self.assertGreater(score, 0.2)
        self.assertLess(score, 0.8)

    def test_empty_query(self) -> None:
        self.assertEqual(relevance_score("", "Title", "Snippet"), 0.0)


class TestTitleSimilarity(unittest.TestCase):
    def test_identical(self) -> None:
        self.assertEqual(title_similarity("Hello World", "hello world"), 1.0)

    def test_different(self) -> None:
        sim = title_similarity("Python Tutorial", "Cat Videos")
        self.assertLess(sim, 0.2)

    def test_partial(self) -> None:
        sim = title_similarity("Python Tutorial Guide", "Python Tutorial Basics")
        self.assertGreater(sim, 0.4)

    def test_empty(self) -> None:
        self.assertEqual(title_similarity("", ""), 1.0)
        self.assertEqual(title_similarity("test", ""), 0.0)


class TestDeduplicate(unittest.TestCase):
    def test_url_dedup(self) -> None:
        results = [
            {"title": "A", "url": "https://example.com/page", "snippet": "s1"},
            {"title": "B", "url": "https://example.com/page", "snippet": "s2"},
        ]
        deduped = deduplicate_results(results)
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["title"], "A")

    def test_title_similarity_dedup(self) -> None:
        results = [
            {"title": "Python Tutorial for Beginners", "url": "https://a.com/1", "snippet": "s1"},
            {"title": "Python Tutorial for Beginners Guide", "url": "https://b.com/2", "snippet": "s2"},
        ]
        deduped = deduplicate_results(results, title_threshold=0.6)
        self.assertEqual(len(deduped), 1)

    def test_different_items_kept(self) -> None:
        results = [
            {"title": "Python Tutorial", "url": "https://a.com/1", "snippet": "s1"},
            {"title": "Java Handbook", "url": "https://b.com/2", "snippet": "s2"},
        ]
        deduped = deduplicate_results(results)
        self.assertEqual(len(deduped), 2)


class TestRerank(unittest.TestCase):
    def test_relevance_ordering(self) -> None:
        results = [
            {"title": "Cat Videos", "url": "https://cat.com", "snippet": "Funny cats"},
            {"title": "Python Tutorial", "url": "https://py.com", "snippet": "Learn Python programming"},
        ]
        reranked = rerank_results("python programming", results)
        self.assertEqual(reranked[0]["title"], "Python Tutorial")

    def test_domain_limit(self) -> None:
        results = [
            {"title": f"Page {i}", "url": f"https://same.com/p{i}", "snippet": "test"}
            for i in range(5)
        ]
        reranked = rerank_results("test", results, max_per_domain=2)
        self.assertEqual(len(reranked), 2)


class TestFilterLowQuality(unittest.TestCase):
    def test_removes_no_title(self) -> None:
        results = [
            {"title": "", "url": "https://a.com", "snippet": "s"},
            {"title": "Good Title", "url": "https://b.com", "snippet": "s"},
        ]
        filtered = filter_low_quality(results)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Good Title")

    def test_removes_no_url(self) -> None:
        results = [
            {"title": "Title", "url": "", "snippet": "s"},
            {"title": "Title2", "url": "https://b.com", "snippet": "s"},
        ]
        filtered = filter_low_quality(results)
        self.assertEqual(len(filtered), 1)


class TestOptimizeResults(unittest.TestCase):
    def test_full_pipeline(self) -> None:
        results = [
            {"title": "Python Tutorial", "url": "https://a.com/py", "snippet": "Learn Python"},
            {"title": "", "url": "https://b.com", "snippet": "bad"},  # filtered
            {"title": "Python Tutorial Guide", "url": "https://a.com/py", "snippet": "Python guide"},  # url dup
            {"title": "Cat Videos", "url": "https://c.com", "snippet": "Cats are cute"},
        ]
        optimized = optimize_results("python tutorial", results)
        # Should filter empty title, dedup URL, keep 2 results
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[0]["title"], "Python Tutorial")

    def test_empty_input(self) -> None:
        self.assertEqual(optimize_results("test", []), [])


if __name__ == "__main__":
    unittest.main()
