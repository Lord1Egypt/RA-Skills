"""Integration tests for Deep Research v2 — full pipeline: plan → research → analyze → reflect → write.

Tests use mock mode (no real API calls). Minimum 10 test cases.

Run:
    python -m pytest test_integration.py -v
"""

import json
import os
import sys
import time
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from writer import WriterAgent, write_report, OutputFormat, ConfidenceLevel, _confidence_level, _confidence_badge
from analyst import analyze_findings, AnalysisResult
from reflection import ResearchPlan, reflect, _normalize_findings, _dimension_hits
from research_pipeline import run_looping_pipeline, run_researcher, run_analyst, run_writer


# ─── Test Data ────────────────────────────────────────────────────────────────

MOCK_QUESTION = "What is the current state of quantum computing?"

MOCK_RESEARCHER_OUTPUTS = [
    {
        "status": "complete",
        "dimension": "hardware",
        "queries": ["quantum computing hardware 2026"],
        "findings": [
            {
                "claim": "IBM unveiled a 1,121-qubit Condor processor in 2023",
                "source_url": "https://example.com/ibm-condor",
                "confidence": 0.95,
                "dimension": "hardware",
            },
            {
                "claim": "Google's Sycamore achieved quantum supremacy in 2019",
                "source_url": "https://example.com/google-sycamore",
                "confidence": 0.9,
                "dimension": "hardware",
            },
        ],
        "sources": [
            {"url": "https://example.com/ibm-condor", "title": "IBM Condor", "score": 0.95},
            {"url": "https://example.com/google-sycamore", "title": "Google Sycamore", "score": 0.9},
        ],
        "metadata": {"chunks_scanned": 5, "chunks_selected": 3, "chunks_expanded": 1},
    },
    {
        "status": "complete",
        "dimension": "applications",
        "queries": ["quantum computing applications"],
        "findings": [
            {
                "claim": "Quantum computing shows promise for drug discovery and cryptography",
                "source_url": "https://example.com/qc-apps",
                "confidence": 0.8,
                "dimension": "applications",
            },
            {
                "claim": "Quantum error correction remains a major challenge",
                "source_url": "https://example.com/qc-errors",
                "confidence": 0.85,
                "dimension": "applications",
            },
        ],
        "sources": [
            {"url": "https://example.com/qc-apps", "title": "QC Applications", "score": 0.8},
        ],
        "metadata": {"chunks_scanned": 4, "chunks_selected": 2, "chunks_expanded": 0},
    },
]

MOCK_ANALYST_OUTPUT = {
    "status": "complete",
    "themes": [
        {
            "name": "Quantum Hardware",
            "confidence": 0.9,
            "key_claims": ["IBM Condor 1,121 qubits", "Google Sycamore supremacy"],
            "findings": [],
        },
        {
            "name": "Applications & Challenges",
            "confidence": 0.8,
            "key_claims": ["Drug discovery", "Error correction"],
            "findings": [],
        },
    ],
    "contradictions": [
        {
            "claim_a": "Quantum computers will replace classical computers within 10 years",
            "claim_b": "Quantum computers will complement, not replace, classical computers",
            "source_a": "https://example.com/optimistic",
            "source_b": "https://example.com/pragmatic",
            "resolution": "The consensus leans toward complementarity for the foreseeable future",
        },
    ],
    "gaps": [
        {"question": "What are the latest quantum error correction breakthroughs?", "importance": "high"},
        {"question": "Cost comparison of quantum vs classical for specific workloads?", "importance": "medium"},
    ],
    "merged_findings": (
        MOCK_RESEARCHER_OUTPUTS[0]["findings"] + MOCK_RESEARCHER_OUTPUTS[1]["findings"]
    ),
}


# ─── Phase 3: Writer Tests ───────────────────────────────────────────────────


class TestWriterAgentConfidence(unittest.TestCase):
    """Test confidence level mapping and badges."""

    def test_high_confidence(self):
        self.assertEqual(_confidence_level(0.9), ConfidenceLevel.HIGH)
        self.assertEqual(_confidence_level(0.8), ConfidenceLevel.HIGH)

    def test_medium_confidence(self):
        self.assertEqual(_confidence_level(0.7), ConfidenceLevel.MEDIUM)
        self.assertEqual(_confidence_level(0.6), ConfidenceLevel.MEDIUM)

    def test_low_confidence(self):
        self.assertEqual(_confidence_level(0.5), ConfidenceLevel.LOW)
        self.assertEqual(_confidence_level(0.4), ConfidenceLevel.LOW)

    def test_uncertain_confidence(self):
        self.assertEqual(_confidence_level(0.3), ConfidenceLevel.UNCERTAIN)
        self.assertEqual(_confidence_level(0.0), ConfidenceLevel.UNCERTAIN)

    def test_invalid_confidence(self):
        self.assertEqual(_confidence_level("bad"), ConfidenceLevel.UNCERTAIN)
        self.assertEqual(_confidence_level(None), ConfidenceLevel.UNCERTAIN)

    def test_badges_are_emoji(self):
        for level in ConfidenceLevel:
            badge = _confidence_badge(level)
            self.assertIsInstance(badge, str)
            self.assertTrue(len(badge) >= 1)


class TestWriterAgentReport(unittest.TestCase):
    """Test report generation in all formats."""

    def setUp(self):
        self.agent = WriterAgent(use_llm=False)  # No API calls

    def test_full_report_has_all_sections(self):
        """Full report must contain all required sections."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.REPORT
        )
        report = result["report"]

        self.assertIn("# Research Report:", report)
        self.assertIn("## Executive Summary", report)
        self.assertIn("## Key Findings", report)
        self.assertIn("## Detailed Analysis", report)
        self.assertIn("## Contradictions", report)
        self.assertIn("## Knowledge Gaps", report)
        self.assertIn("## Sources", report)
        self.assertIn("## Methodology", report)
        self.assertEqual(result["status"], "complete")

    def test_full_report_has_citations(self):
        """Report must contain inline source citations."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.REPORT
        )
        report = result["report"]

        # Citations should appear as [source](url)
        self.assertIn("source", report)

    def test_full_report_has_confidence_indicators(self):
        """Report must contain confidence badges/indicators."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.REPORT
        )
        report = result["report"]

        # Should have emoji badges
        self.assertIn("🟢", report)

    def test_full_report_has_contradiction_callouts(self):
        """Report must call out contradictions with warnings."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.REPORT
        )
        report = result["report"]

        self.assertIn("Contradiction", report)
        self.assertIn("Source A:", report)
        self.assertIn("Source B:", report)
        self.assertIn("Resolution:", report)

    def test_summary_format(self):
        """Summary format should be concise."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.SUMMARY
        )
        report = result["report"]

        self.assertIn("Executive Summary", report)
        self.assertIn("Top Findings", report)
        self.assertEqual(result["format"], "summary")

    def test_brief_format(self):
        """Brief format should be bullet-point style."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.BRIEF
        )
        report = result["report"]

        self.assertIn("Research Brief", report)
        self.assertIn("Key Points:", report)
        self.assertEqual(result["format"], "brief")

    def test_json_format(self):
        """JSON format should return structured data."""
        result = self.agent.write_report(
            MOCK_ANALYST_OUTPUT, MOCK_QUESTION, OutputFormat.JSON
        )

        self.assertEqual(result["format"], "json")
        self.assertIn("summary", result)
        self.assertIn("findings", result)
        self.assertIn("contradictions", result)
        self.assertIn("gaps", result)
        self.assertIn("sources", result)
        # Findings should have confidence_level annotations
        for f in result["findings"]:
            self.assertIn("confidence_level", f)
            self.assertIn("confidence_badge", f)

    def test_empty_analyst_output(self):
        """Writer should handle empty input gracefully."""
        empty_output = {
            "themes": [],
            "contradictions": [],
            "gaps": [],
            "merged_findings": [],
        }
        result = self.agent.write_report(
            empty_output, "Empty question?", OutputFormat.REPORT
        )
        self.assertEqual(result["status"], "complete")
        self.assertIn("Research Report", result["report"])


# ─── Phase 4: Integration Tests ──────────────────────────────────────────────


class TestFullPipelineIntegration(unittest.TestCase):
    """End-to-end integration tests: plan → research → analyze → reflect → write."""

    @patch("research_pipeline.generate_queries")
    def test_single_cycle_mock_pipeline(self, mock_gen):
        """Full pipeline in mock mode, 1 cycle."""
        mock_gen.return_value = [
            {"type": "semantic", "query": MOCK_QUESTION, "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question=MOCK_QUESTION,
            max_cycles=1,
            mock_mode=True,
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["cycles_completed"], 1)
        self.assertIn("quantum computing", result["report"].lower())

        # Check cycle history
        cycle = result["cycle_history"][0]
        self.assertIn("researcher_outputs", cycle)
        self.assertIn("analyst_output", cycle)
        self.assertIn("reflection", cycle)

    @patch("research_pipeline.generate_queries")
    def test_multi_cycle_mock_stops_early(self, mock_gen):
        """Pipeline should stop when coverage is sufficient."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "Simple question", "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question="Simple question",
            max_cycles=5,
            mock_mode=True,
        )
        self.assertLessEqual(result["cycles_completed"], 2)
        self.assertEqual(result["status"], "complete")

    @patch("research_pipeline.generate_queries")
    def test_pipeline_with_writer_integration(self, mock_gen):
        """Pipeline output should be a valid report."""
        mock_gen.return_value = [
            {"type": "semantic", "query": MOCK_QUESTION, "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question=MOCK_QUESTION,
            max_cycles=1,
            mock_mode=True,
        )

        # The mock pipeline produces a basic report
        report = result["report"]
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 50)

    def test_analyst_to_writer_flow(self):
        """Analyst output feeds correctly into writer."""
        # Step 1: Run analyst on researcher outputs
        with patch("research_pipeline._call_glm") as mock_glm:
            mock_glm.return_value = json.dumps(MOCK_ANALYST_OUTPUT)
            analyst_result = run_analyst(MOCK_RESEARCHER_OUTPUTS)

        # Step 2: Feed into writer
        writer_agent = WriterAgent(use_llm=False)
        writer_result = writer_agent.write_report(
            analyst_result, MOCK_QUESTION, OutputFormat.REPORT
        )

        self.assertEqual(writer_result["status"], "complete")
        self.assertIn("Research Report", writer_result["report"])
        self.assertEqual(writer_result["metadata"]["themes_count"], 2)

    def test_reflection_in_pipeline_context(self):
        """Reflection works correctly within the pipeline loop."""
        plan = ResearchPlan(
            question=MOCK_QUESTION,
            dimensions=["hardware", "applications", "theory"],
            dimension_questions={
                "hardware": ["What processors exist?"],
                "applications": ["What are the use cases?"],
                "theory": ["How does it work?"],
            },
        )

        # Simulate findings that cover 2 of 3 dimensions
        findings = [
            {"dimension": "hardware", "claim": "c1", "confidence": 0.9},
            {"dimension": "applications", "claim": "c2", "confidence": 0.8},
        ]

        result = reflect(plan, findings, cycle=1, max_cycles=5)

        # Should continue because theory dimension is missing
        self.assertTrue(result.should_continue)
        self.assertIn("theory", result.next_dimensions)
        self.assertLess(result.coverage_score, 1.0)

    def test_empty_findings_stop_pipeline(self):
        """Empty findings should stop the pipeline."""
        plan = ResearchPlan(
            question="test",
            dimensions=["dim1", "dim2"],
            dimension_questions={},
        )
        result = reflect(plan, [], cycle=1, max_cycles=5)
        self.assertFalse(result.should_continue)

    @patch("research_pipeline.generate_queries")
    def test_max_cycles_hard_stop(self, mock_gen):
        """Pipeline must stop at max cycles regardless of coverage."""
        mock_gen.return_value = [
            {"type": "semantic", "query": "test", "rationale": "test"}
        ]
        result = run_looping_pipeline(
            question="test",
            max_cycles=8,
            mock_mode=True,
        )
        self.assertLessEqual(result["cycles_completed"], 8)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases: empty results, failures, etc."""

    def test_empty_researcher_output_to_analyst(self):
        """Analyst handles empty researcher outputs."""
        result = run_analyst([{"findings": []}])
        self.assertEqual(result["status"], "no_findings")

    def test_writer_with_minimal_input(self):
        """Writer handles minimal analyst output."""
        minimal = {
            "themes": [],
            "contradictions": [],
            "gaps": [],
            "merged_findings": [],
        }
        agent = WriterAgent(use_llm=False)
        result = agent.write_report(minimal, "test?", OutputFormat.REPORT)
        self.assertEqual(result["status"], "complete")
        self.assertIn("Research Report", result["report"])

    def test_writer_with_single_finding(self):
        """Writer handles single finding."""
        single = {
            "themes": [{"name": "Only Theme", "confidence": 0.7, "key_claims": []}],
            "contradictions": [],
            "gaps": [],
            "merged_findings": [
                {"claim": "Only finding", "confidence": 0.7, "source_url": "https://example.com"}
            ],
        }
        agent = WriterAgent(use_llm=False)
        result = agent.write_report(single, "single?", OutputFormat.REPORT)
        self.assertIn("Only finding", result["report"])

    def test_normalize_findings_researcher_format(self):
        """Normalize handles researcher output format."""
        raw = [
            {"dimension": "dim1", "findings": [
                {"claim": "c1", "confidence": 0.9, "source_url": "u1"},
                {"claim": "c2", "confidence": 0.8, "source_url": "u2"},
            ]},
            {"dimension": "dim2", "findings": [
                {"claim": "c3", "confidence": 0.7, "source_url": "u3"},
            ]},
        ]
        result = _normalize_findings(raw)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["theme"], "dim1")
        self.assertEqual(len(result[0]["claims"]), 2)
        self.assertEqual(result[1]["theme"], "dim2")

    def test_dimension_hits_case_insensitive(self):
        """Dimension matching is case-insensitive."""
        hits = _dimension_hits(
            ["Hardware", "Applications"],
            [
                {"dimension": "hardware", "confidence": 0.9},
                {"theme": "APPLICATIONS", "confidence": 0.8},
            ],
        )
        self.assertEqual(hits["Hardware"], 1)
        self.assertEqual(hits["Applications"], 1)

    def test_convenience_write_report_function(self):
        """The convenience function works correctly."""
        result = write_report(
            MOCK_ANALYST_OUTPUT,
            MOCK_QUESTION,
            fmt="brief",
            use_llm=False,
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["format"], "brief")
        self.assertIn("Research Brief", result["report"])


class TestReflectionWithAnalystIntegration(unittest.TestCase):
    """Test reflection using analyst output directly."""

    def test_analyst_findings_feed_reflection(self):
        """Analyst merged_findings feed into reflection correctly."""
        plan = ResearchPlan(
            question="test",
            dimensions=["hardware", "applications"],
            dimension_questions={},
        )

        # Use analyst's merged_findings as reflection input
        findings = MOCK_ANALYST_OUTPUT["merged_findings"]
        result = reflect(plan, findings, cycle=1, max_cycles=5)

        # Should have some coverage
        self.assertGreater(result.coverage_score, 0.0)

    def test_reflection_output_structure(self):
        """Reflection result has all required fields."""
        plan = ResearchPlan(question="test", dimensions=["dim1"], dimension_questions={})
        result = reflect(plan, [], cycle=1, max_cycles=3)

        self.assertIsInstance(result.should_continue, bool)
        self.assertIsInstance(result.gaps, list)
        self.assertIsInstance(result.coverage_score, float)
        self.assertIsInstance(result.next_dimensions, list)
        self.assertIsInstance(result.summary, str)
        self.assertIn("Cycle 1/3", result.summary)


if __name__ == "__main__":
    unittest.main()
