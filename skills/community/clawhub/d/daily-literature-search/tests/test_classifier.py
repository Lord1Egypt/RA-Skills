#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for paper classification logic.
Run: python3 -m pytest tests/test_classifier.py
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestBAllClassification:
    """Test B-ALL classification keywords."""
    
    def test_b_all_keywords_basic(self):
        """Test basic B-ALL keyword matching."""
        from classifier import classify_by_keywords
        
        test_cases = [
            ("B-cell acute lymphoblastic leukemia treatment", "B-ALL"),
            ("B-ALL relapse after CAR-T therapy", "B-ALL"),
            ("CD19-targeted therapy in ALL", "B-ALL"),
            ("Blinatumomab for pediatric ALL", "B-ALL"),
            ("Inotuzumab ozogamicin outcomes", "B-ALL"),
        ]
        
        for text, expected in test_cases:
            result = classify_by_keywords(text, category="B-ALL")
            assert result == "B-ALL", f"Failed for: {text}"
    
    def test_mm_keywords_basic(self):
        """Test MM keyword matching."""
        from classifier import classify_by_keywords
        
        test_cases = [
            ("Multiple myeloma treatment with elranatamab", "MM"),
            ("BCMA-targeted CAR-T in myeloma", "MM"),
            ("Teclistamab for relapsed MM", "MM"),
            ("Talquetamab GPRC5D bispecific", "MM"),
            ("Plasma cell dyscrasia management", "MM"),
        ]
        
        for text, expected in test_cases:
            result = classify_by_keywords(text, category="MM")
            assert result == "MM", f"Failed for: {text}"


class TestDOIExtraction:
    """Test DOI extraction utilities."""
    
    def test_doi_normalization(self):
        """Test DOI normalization."""
        from utils import normalize_doi
        
        test_cases = [
            ("10.1038/s41375-026-02867-9", "10.1038/s41375-026-02867-9"),
            ("https://doi.org/10.1038/s41375-026-02867-9", "10.1038/s41375-026-02867-9"),
            ("DOI:10.1038/s41375-026-02867-9", "10.1038/s41375-026-02867-9"),
            ("10.1038/S41375-026-02867-9", "10.1038/s41375-026-02867-9"),  # lowercase
        ]
        
        for input_doi, expected in test_cases:
            result = normalize_doi(input_doi)
            assert result == expected, f"Failed for: {input_doi}"
    
    def test_doi_extraction_from_text(self):
        """Test DOI extraction from text."""
        from utils import extract_doi_from_text
        
        test_cases = [
            ("DOI: 10.1038/s41375-026-02867-9", "10.1038/s41375-026-02867-9"),
            ("https://doi.org/10.1007/s11899-026-00772-7", "10.1007/s11899-026-00772-7"),
            ("Paper with doi 10.1182/blood.2025032536 published", "10.1182/blood.2025032536"),
            ("No DOI here", None),
        ]
        
        for text, expected in test_cases:
            result = extract_doi_from_text(text)
            assert result == expected, f"Failed for: {text}"


class TestFilenameSafety:
    """Test safe filename generation."""
    
    def test_safe_filename_basic(self):
        """Test basic filename sanitization."""
        from utils import safe_filename
        
        test_cases = [
            ("Normal Title", "Normal_Title"),
            ("Title with/special:chars*", "Title_withspecialchars"),
            ("A Very Long Title That Should Be Truncated Because It Exceeds The Maximum Length Allowed",
             "A_Very_Long_Title_That_Should_Be_Truncat"),  # 50 chars
        ]
        
        for title, expected_prefix in test_cases:
            result = safe_filename(title)
            assert result.startswith(expected_prefix[:20]), f"Failed for: {title}"


class TestDeduplication:
    """Test deduplication logic."""
    
    def test_batch_dedup(self):
        """Test within-batch deduplication."""
        from utils import normalize_doi
        
        papers = [
            {"doi": "10.1038/test1", "title": "Paper 1"},
            {"doi": "10.1038/test1", "title": "Paper 1 Duplicate"},  # Duplicate
            {"doi": "10.1038/test2", "title": "Paper 2"},
        ]
        
        dois = set()
        unique_papers = []
        
        for paper in papers:
            doi = normalize_doi(paper.get("doi"))
            if doi and doi not in dois:
                dois.add(doi)
                unique_papers.append(paper)
        
        assert len(unique_papers) == 2, "Should remove 1 duplicate"
    
    def test_library_dedup(self):
        """Test library deduplication."""
        from utils import normalize_doi
        
        existing_dois = {"10.1038/test1", "10.1038/test2"}
        new_papers = [
            {"doi": "10.1038/test1", "title": "Already in library"},  # Should skip
            {"doi": "10.1038/test3", "title": "New paper"},  # Should keep
        ]
        
        unique_papers = []
        for paper in new_papers:
            doi = normalize_doi(paper.get("doi"))
            if doi and doi not in existing_dois:
                unique_papers.append(paper)
        
        assert len(unique_papers) == 1, "Should skip 1 existing paper"
        assert unique_papers[0]["title"] == "New paper"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
