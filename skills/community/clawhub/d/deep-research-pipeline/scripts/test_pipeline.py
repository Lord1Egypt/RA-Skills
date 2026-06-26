"""Tests for research_pipeline.py — mock data, no real API calls."""

import json
import os
import sys
import unittest
from unittest.mock import patch

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_pipeline import run_researcher, run_analyst, run_writer, _extract_findings, run_looping_pipeline
from reflection import ResearchPlan, ReflectionResult, reflect, _normalize_findings, _dimension_hits, _gap_score


# ─── Test data ────────────────────────────────────────────────────────────────

MOCK_SEARCH_RESULTS = [
    {
        "url": "https://example.com/rag-guide",
        "title": "RAG Architecture Guide",
        "content": "Retrieval-Augmented Generation (RAG) combines retrieval systems with LLMs. The key components are: embedding models, vector stores, and reranking. RAG reduces hallucination by grounding responses in retrieved documents.",
    },
    {
        "url": "https://example.com/rag-benchmarks",
        "title": "RAG Benchmarks 2026",
        "content": "Recent benchmarks show RAG systems achieving 85% accuracy on factual QA tasks. Chunk size of 512 tokens with overlap of 50 tokens performs best. Hybrid search (dense + sparse) outperforms either alone.",
    },
]

MOCK_RESEARCHER_OUTPUTS = [
    {
        "status": "complete",
        "dimension": "technical architecture",
        "queries": ["RAG architecture", "how RAG works"],
        "findings": [
            {
                "claim": "RAG combines retrieval with LLMs to reduce hallucination",
                "source_url": "https://example.com/rag-guide",
                "confidence": 0.9,
                "answers_question": "How does RAG work?",
            },
            {
                "claim": "RAG achieves 85% accuracy on factual QA tasks",
                "source_url": "https://example.com/rag-benchmarks",
                "confidence": 0.85,
                "answers_question": "How effective is RAG?",
            },
        ],
        "sources": [
            {
                "url": "https://example.com/rag-guide",
                "title": "RAG Architecture Guide",
                "score": 0.9,
            },
            {
                "url": "https://example.com/rag-benchmarks",
                "title": "RAG Benchmarks 2026",
                "score": 0.85,
            },
        ],
        "metadata": {"chunks_scanned": 2, "chunks_selected": 2, "chunks_expanded": 0},
    },
    {
        "status": "complete",
        "dimension": "benchmarks",
        "queries": ["RAG benchmarks 2026"],
        "findings": [
            {
                "claim": "Chunk size of 512 tokens with 50 token overlap is optimal",
                "source_url": "https://example.com/rag-benchmarks",
                "confidence": 0.8,
                "answers_question": "Best chunk size?",
            },
        ],
        "sources": [
            {
                "url": "https://example.com/rag-benchmarks",
                "title": "RAG Benchmarks 2026",
                "score": 0.85,
            },
        ],
        "metadata": {"chunks_scanned": 1, "chunks_selected": 1, "chunks_expanded": 0},
    },
]

MOCK_ANALYST_OUTPUT = {
    "status": "complete",
    "themes": [
        {
            "name": "RAG Architecture",
            "confidence": 0.9,
            "key_claims": ["RAG reduces hallucination"],
        }
    ],
    "contradictions": [],
    "gaps": [{"question": "Cost comparison with fine-tuning?", "importance": "medium"}],
    "merged_findings": MOCK_RESEARCHER_OUTPUTS[0]["findings"]
    + MOCK_RESEARCHER_OUTPUTS[1]["findings"],
}


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestRunResearcher(unittest.TestCase):
    """Test researcher pipeline."""

    @patch("research_pipeline.generate_queries")
    def test_researcher_returns_queries_when_no_results(self, mock_gen):
        """Without search results, returns queries for caller."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "RAG architecture", "rationale": "test"}
        ]
        result = run_researcher(
            "How does RAG work?",
            "technical architecture",
            ["What are RAG components?"],
            max_sources=5,
        )
        self.assertEqual(result["status"], "queries_ready")
        self.assertEqual(result["dimension"], "technical architecture")
        self.assertEqual(len(result["queries"]), 1)

    @patch("research_pipeline.generate_queries")
    @patch("research_pipeline.select_relevant_chunks")
    @patch("research_pipeline.expand_context")
    @patch("research_pipeline._extract_findings")
    def test_researcher_full_pipeline(
        self, mock_extract, mock_expand, mock_select, mock_gen
    ):
        """Full pipeline with search results."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "test", "rationale": "r"}
        ]
        mock_select.return_value = [
            {
                "url": "https://example.com",
                "title": "Test",
                "content": "RAG content",
                "score": 0.9,
            }
        ]
        mock_expand.return_value = mock_select.return_value
        mock_extract.return_value = [
            {
                "claim": "RAG works",
                "source_url": "https://example.com",
                "confidence": 0.9,
                "answers_question": "q1",
            }
        ]

        result = run_researcher(
            "How does RAG work?",
            "technical architecture",
            ["What are components?"],
            max_sources=10,
            search_results=MOCK_SEARCH_RESULTS,
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(len(result["findings"]), 1)
        self.assertEqual(result["findings"][0]["claim"], "RAG works")
        self.assertEqual(result["metadata"]["chunks_scanned"], 2)
        self.assertEqual(result["metadata"]["chunks_selected"], 1)

    @patch("research_pipeline.generate_queries")
    def test_researcher_no_content(self, mock_gen):
        """Empty search results returns no_content."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "test", "rationale": "r"}
        ]
        result = run_researcher(
            "test",
            "dim",
            [],
            max_sources=5,
            search_results=[{"url": "", "content": None}],
        )
        self.assertEqual(result["status"], "no_content")
        self.assertEqual(result["findings"], [])


class TestRunAnalyst(unittest.TestCase):
    """Test analyst pipeline."""

    @patch("research_pipeline._call_glm")
    def test_analyst_with_mock_llm(self, mock_glm):
        mock_glm.return_value = json.dumps(
            {
                "themes": [
                    {
                        "name": "RAG",
                        "findings": [],
                        "confidence": 0.9,
                        "key_claims": ["claim1"],
                    }
                ],
                "contradictions": [],
                "gaps": [
                    {
                        "question": "gap?",
                        "importance": "medium",
                        "suggested_search": "test",
                    }
                ],
                "merged_findings": [
                    {
                        "claim": "c1",
                        "sources": ["u1"],
                        "confidence": 0.9,
                        "theme": "RAG",
                    }
                ],
            }
        )

        result = run_analyst(MOCK_RESEARCHER_OUTPUTS)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(len(result["themes"]), 1)
        self.assertEqual(result["themes"][0]["name"], "RAG")
        self.assertEqual(result["total_findings_input"], 3)

    @patch("research_pipeline._call_glm")
    def test_analyst_empty_input(self, mock_glm):
        result = run_analyst([{"findings": []}])
        self.assertEqual(result["status"], "no_findings")
        mock_glm.assert_not_called()

    @patch("research_pipeline._call_glm", side_effect=RuntimeError("API fail"))
    def test_analyst_fallback_on_error(self, mock_glm):
        result = run_analyst(MOCK_RESEARCHER_OUTPUTS)
        self.assertEqual(result["status"], "fallback")
        # Should still have merged findings (simple dedup)
        self.assertGreater(len(result["merged_findings"]), 0)


class TestRunWriter(unittest.TestCase):
    """Test writer pipeline."""

    @patch("writer._call_glm")
    def test_writer_generates_report(self, mock_glm):
        mock_glm.return_value = "# RAG Research Report\n\n## Executive Summary\n\nRAG is effective.\n\n## Details\n\nRAG achieves 85% accuracy [https://example.com].\n\n## Confidence\n\nSection confidence: 0.9"

        result = run_writer(MOCK_ANALYST_OUTPUT, "How does RAG work?")
        self.assertEqual(result["status"], "complete")
        self.assertIn("RAG", result["report"])
        self.assertIn("##", result["report"])
        self.assertEqual(result["metadata"]["themes_count"], 1)
        self.assertEqual(result["metadata"]["gaps_count"], 1)

    @patch("writer._call_glm", side_effect=RuntimeError("API fail"))
    def test_writer_fallback_on_error(self, mock_glm):
        result = run_writer(MOCK_ANALYST_OUTPUT, "test?")
        self.assertEqual(result["status"], "complete")
        self.assertIn("Research Report", result["report"])


class TestExtractFindings(unittest.TestCase):
    """Test finding extraction."""

    @patch("research_pipeline._call_glm")
    def test_extract_findings(self, mock_glm):
        mock_glm.return_value = json.dumps(
            [
                {
                    "claim": "c1",
                    "source_url": "http://x",
                    "confidence": 0.9,
                    "answers_question": "q1",
                }
            ]
        )
        chunks = [{"url": "http://x", "content": "some text", "score": 0.8}]
        findings = _extract_findings(chunks, "question?", "dim", ["q1"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["claim"], "c1")

    @patch("research_pipeline._call_glm", side_effect=RuntimeError("fail"))
    def test_extract_findings_fallback(self, mock_glm):
        findings = _extract_findings([], "q?", "d", [])
        self.assertEqual(findings, [])


class TestReflect(unittest.TestCase):
    """Test reflection loop logic — no API calls."""

    def _make_plan(self, dimensions=None):
        return ResearchPlan(
            question="What is RAG?",
            dimensions=dimensions or ["architecture", "benchmarks", "limitations"],
            dimension_questions={"architecture": ["What is RAG?"], "benchmarks": ["How effective?"], "limitations": ["What are the limits?"]},
            budget_seconds=900,
            budget_tokens=60000,
        )

    def test_full_coverage_stops(self):
        """All dimensions covered with high confidence → should_continue=False."""
        plan = self._make_plan()
        findings = [
            {"theme": "architecture", "claims": ["c1"], "confidence": 0.9, "sources": ["s1"], "dimension": "architecture"},
            {"theme": "benchmarks", "claims": ["c2"], "confidence": 0.85, "sources": ["s2"], "dimension": "benchmarks"},
            {"theme": "limitations", "claims": ["c3"], "confidence": 0.8, "sources": ["s3"], "dimension": "limitations"},
        ]
        result = reflect(plan, findings, cycle=1, max_cycles=8)
        self.assertFalse(result.should_continue)
        self.assertGreaterEqual(result.coverage_score, 0.8)
        self.assertEqual(len(result.gaps), 0)

    def test_partial_coverage_continues(self):
        """Only 1 of 3 dimensions covered → should_continue=True."""
        plan = self._make_plan()
        findings = [
            {"theme": "architecture", "claims": ["c1"], "confidence": 0.9, "sources": ["s1"], "dimension": "architecture"},
        ]
        result = reflect(plan, findings, cycle=1, max_cycles=8)
        self.assertTrue(result.should_continue)
        self.assertLess(result.coverage_score, 0.8)
        self.assertGreater(len(result.next_dimensions), 0)

    def test_max_cycles_hard_stop(self):
        """At max_cycles, should_continue=False regardless of coverage."""
        plan = self._make_plan()
        findings = []  # No findings at all
        result = reflect(plan, findings, cycle=8, max_cycles=8)
        self.assertFalse(result.should_continue)

    def test_empty_findings_stops(self):
        """Empty findings after cycle >= 1 → stop."""
        plan = self._make_plan()
        result = reflect(plan, [], cycle=1, max_cycles=8)
        self.assertFalse(result.should_continue)

    def test_progress_summary_includes_cycle_info(self):
        """Summary should mention cycle number and covered/missing dims."""
        plan = self._make_plan()
        findings = [
            {"theme": "architecture", "claims": ["c1"], "confidence": 0.9, "sources": [], "dimension": "architecture"},
        ]
        result = reflect(plan, findings, cycle=2, max_cycles=5)
        self.assertIn("Cycle 2/5", result.summary)
        self.assertIn("architecture", result.summary)

    def test_dimension_hits_fuzzy_match(self):
        """Dimension matching should be case-insensitive and substring-aware."""
        hits = _dimension_hits(["Architecture", "benchmarks"], [
            {"theme": "architecture", "confidence": 0.9},
            {"dimension": "Benchmarks and metrics", "confidence": 0.8},
        ])
        self.assertEqual(hits.get("Architecture", 0), 1)
        self.assertEqual(hits.get("benchmarks", 0), 1)

    def test_gap_score_high_for_no_hits(self):
        """No hits, no confidence → gap score near 1.0."""
        score = _gap_score(hit_count=0, avg_confidence=0.0)
        self.assertGreater(score, 0.7)

    def test_gap_score_low_for_good_coverage(self):
        """Many hits, high confidence → gap score near 0.0."""
        score = _gap_score(hit_count=3, avg_confidence=0.9)
        self.assertLess(score, 0.3)

    def test_normalize_findings_wrapped(self):
        """Unwraps {merged_findings: [...]} format."""
        raw = {"merged_findings": [{"theme": "t", "claims": [], "sources": []}]}
        result = _normalize_findings(raw)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["theme"], "t")

    def test_normalize_findings_flat(self):
        """Groups flat findings by dimension."""
        raw = [
            {"claim": "c1", "dimension": "arch", "confidence": 0.9},
            {"claim": "c2", "dimension": "arch", "confidence": 0.8},
        ]
        result = _normalize_findings(raw)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["theme"], "arch")
        self.assertEqual(len(result[0]["claims"]), 2)


class TestLoopingPipelineIntegration(unittest.TestCase):
    """Integration test: full pipeline in mock mode, 1 cycle."""

    @patch("research_pipeline.generate_queries")
    def test_single_cycle_mock_pipeline(self, mock_gen):
        """Run a 1-cycle research on a simple topic with mock data."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "machine learning", "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question="What is machine learning?",
            max_cycles=1,
            mock_mode=True,
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["cycles_completed"], 1)
        self.assertGreater(result["final_coverage"], 0.0)
        self.assertIn("machine learning", result["report"].lower())
        self.assertIn("cycle 1", result["report"].lower())
        self.assertEqual(len(result["cycle_history"]), 1)

        # Check cycle history structure
        cycle = result["cycle_history"][0]
        self.assertIn("researcher_outputs", cycle)
        self.assertIn("analyst_output", cycle)
        self.assertIn("reflection", cycle)
        self.assertIn("should_continue", cycle["reflection"])
        self.assertIn("coverage_score", cycle["reflection"])
        self.assertIn("summary", cycle["reflection"])

    @patch("research_pipeline.generate_queries")
    def test_multi_cycle_mock_stops_early(self, mock_gen):
        """Pipeline should stop when coverage is sufficient, even if max_cycles > 1."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "Simple question", "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question="Simple question",
            max_cycles=5,
            mock_mode=True,
        )
        # Mock data covers all dimensions in cycle 1, so it should stop
        self.assertLessEqual(result["cycles_completed"], 2)
        self.assertEqual(result["status"], "complete")

    @patch("research_pipeline.generate_queries")
    def test_pipeline_metadata(self, mock_gen):
        """Pipeline returns correct metadata."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "Test question", "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question="Test question",
            max_cycles=1,
            mock_mode=True,
        )
        meta = result["metadata"]
        self.assertIn("total_duration_seconds", meta)
        self.assertIn("total_findings", meta)
        self.assertEqual(meta["max_cycles"], 1)
        self.assertIsInstance(meta["dimensions"], list)


if __name__ == "__main__":
    unittest.main()
