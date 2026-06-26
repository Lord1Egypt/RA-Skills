#!/usr/bin/env python3
"""
GEO Score Calculator
Calculate GEO optimization score for content

Pure computation - no file system or network operations.
"""

import json
import re
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GEOScore:
    """GEO scoring result"""
    content_quality: int       # Content quality 0-100
    schema_completeness: int   # Schema completeness 0-100
    faq_coverage: int         # FAQ coverage 0-100
    citation_activity: int     # Citation activity 0-100
    total_score: int          # Overall score 0-100
    suggestions: List[str]     # Optimization suggestions


class GEOScorer:
    """GEO scoring engine"""

    def __init__(self):
        self.weights = {
            'content_quality': 0.35,
            'schema_completeness': 0.25,
            'faq_coverage': 0.25,
            'citation_activity': 0.15
        }

    def calculate_score(
        self,
        content: str,
        schema: Dict[str, Any] = None,
        faq_count: int = 0,
        citation_count: int = 0
    ) -> GEOScore:
        """Calculate GEO score"""

        # 1. Content quality score
        content_score = self._score_content(content)

        # 2. Schema completeness score
        schema_score = self._score_schema(schema)

        # 3. FAQ coverage score
        faq_score = self._score_faq(faq_count)

        # 4. Citation activity score
        citation_score = self._score_citation(citation_count)

        # 5. Overall score
        total = int(
            content_score * self.weights['content_quality'] +
            schema_score * self.weights['schema_completeness'] +
            faq_score * self.weights['faq_coverage'] +
            citation_score * self.weights['citation_activity']
        )

        # 6. Generate suggestions
        suggestions = self._generate_suggestions(
            content_score, schema_score, faq_score, citation_score
        )

        return GEOScore(
            content_quality=content_score,
            schema_completeness=schema_score,
            faq_coverage=faq_score,
            citation_activity=citation_score,
            total_score=total,
            suggestions=suggestions
        )

    def _score_content(self, content: str) -> int:
        """Content quality scoring"""
        score = 0

        # Word count check (1500+ earns full score)
        word_count = len(content)
        if word_count >= 1500:
            score += 30
        elif word_count >= 1200:
            score += 25
        elif word_count >= 800:
            score += 15
        else:
            score += 5

        # Data citation check
        data_patterns = [
            r'\d+%',       # Percentage
            r'\$\d+',      # Dollar amount
            r'\d+ [A-Za-z]+',  # Count with unit
            r'per.*source',    # Data source
        ]
        data_count = sum(len(re.findall(p, content, re.IGNORECASE)) for p in data_patterns)
        if data_count >= 3:
            score += 25
        elif data_count >= 1:
            score += 15
        else:
            score += 0

        # Structure check (headings)
        heading_count = len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE))
        if heading_count >= 5:
            score += 20
        elif heading_count >= 3:
            score += 15
        else:
            score += 5

        # FAQ section check
        if 'FAQ' in content or 'Frequently Asked' in content:
            score += 25
        else:
            score += 0

        return min(score, 100)

    def _score_schema(self, schema: Dict[str, Any] = None) -> int:
        """Schema completeness scoring"""
        if not schema:
            return 0

        score = 0
        required_types = ['@context', '@type', 'name']
        for req in required_types:
            if req in schema:
                score += 20
            else:
                score += 0

        # Bonus for FAQPage schema
        if schema.get('@type') == 'FAQPage':
            score += 20

        return min(score, 100)

    def _score_faq(self, faq_count: int) -> int:
        """FAQ coverage scoring"""
        if faq_count >= 8:
            return 100
        elif faq_count >= 6:
            return 75
        elif faq_count >= 4:
            return 50
        elif faq_count >= 2:
            return 25
        else:
            return 0

    def _score_citation(self, citation_count: int) -> int:
        """Citation activity scoring"""
        if citation_count >= 10:
            return 100
        elif citation_count >= 7:
            return 80
        elif citation_count >= 5:
            return 60
        elif citation_count >= 3:
            return 40
        elif citation_count >= 1:
            return 20
        else:
            return 0

    def _generate_suggestions(
        self,
        content_score: int,
        schema_score: int,
        faq_score: int,
        citation_score: int
    ) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []

        if content_score < 60:
            suggestions.append("Content needs more depth — aim for 1200+ words with at least 3 data citations")
        if schema_score < 60:
            suggestions.append("Add structured Schema markup — include Product/FAQPage schema")
        if faq_score < 60:
            suggestions.append("Add more FAQ pairs — aim for at least 6 questions with concise answers")
        if citation_score < 40:
            suggestions.append("Boost citation activity — publish consistently and reference rankings weekly")

        if not suggestions:
            suggestions.append("Content is well-optimized — continue publishing and reference citation trends")

        return suggestions


if __name__ == '__main__':
    # Demo usage
    scorer = GEOScorer()

    # Test content
    test_content = """
    # How to Choose the Best B2B Supplier

    When selecting a B2B supplier for your export business, there are several key factors to consider.

    ## Key Criteria

    1. Quality Certification - Look for ISO 9001 certified suppliers
    2. Production Capacity - Ensure they can meet your volume requirements
    3. Pricing Competitiveness - Compare quotes from multiple suppliers

    ## FAQ

    Q: What certifications should B2B suppliers have?
    A: At minimum, ISO 9001 for quality management.

    Q: How long does supplier verification take?
    A: Typically 2-4 weeks for comprehensive verification.

    Based on industry data, 73% of B2B buyers prioritize quality certifications.
    Source: B2B Market Report 2024
    """

    score = scorer.calculate_score(test_content, faq_count=2, citation_count=3)

    print(f"GEO Score: {score.total_score}/100")
    print(f"Content Quality: {score.content_quality}/100")
    print(f"Schema Completeness: {score.schema_completeness}/100")
    print(f"FAQ Coverage: {score.faq_coverage}/100")
    print(f"Citation Activity: {score.citation_activity}/100")
    print("\nSuggestions:")
    for s in score.suggestions:
        print(f"  - {s}")
