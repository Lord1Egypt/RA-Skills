import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyst import analyze_findings


def test_deduplication_merges_near_duplicates():
    findings = [
        {
            "claim": "RAG combines retrieval with LLMs to reduce hallucination.",
            "source_url": "https://example.com/a",
            "dimension": "technical architecture",
            "confidence": 0.9,
        },
        {
            "claim": "Retrieval-augmented generation combines retrieval with LLMs to reduce hallucinations.",
            "source_url": "https://example.com/b",
            "dimension": "technical architecture",
            "confidence": 0.8,
        },
    ]

    result = analyze_findings(findings, dimensions=["technical architecture"])

    # Two highly similar claims should deduplicate into one analyzed finding id.
    assert len(result.confidence_map) == 1
    assert result.coverage_score == 1.0
    assert result.gaps == []


def test_theme_extraction_groups_by_keyword_cooccurrence():
    findings = [
        {"claim": "RAG uses a vector store and embeddings for retrieval.", "source_url": "https://example.com/rag1"},
        {"claim": "Hybrid search combines dense embeddings with sparse retrieval.", "source_url": "https://example.com/rag2"},
        {"claim": "Bond yields rise when inflation expectations increase.", "source_url": "https://example.com/macro1"},
        {"claim": "Higher inflation can push yields up and reduce bond prices.", "source_url": "https://example.com/macro2"},
    ]

    result = analyze_findings(findings, dimensions=["technical", "macro"])

    # Should produce 3-7 themes when enough findings exist.
    assert 1 <= len(result.themes) <= 7
    # At least two themes should exist given two distinct topic areas.
    assert len(result.themes) >= 2
    # Themes must reference finding ids (deduped ids).
    for theme in result.themes:
        assert "finding_ids" in theme
        assert len(theme["finding_ids"]) >= 1


def test_contradiction_detection_flags_opposing_claims():
    findings = [
        {
            "claim": "Increasing interest rates increase mortgage affordability.",
            "source_url": "https://example.com/claim-up",
        },
        {
            "claim": "Increasing interest rates decrease mortgage affordability.",
            "source_url": "https://example.com/claim-down",
        },
    ]

    result = analyze_findings(findings, dimensions=["housing"])

    assert len(result.contradictions) >= 1
    c = result.contradictions[0]
    assert "claim_a" in c and "claim_b" in c
    assert "Opposing polarity" in c.get("reason", "")

