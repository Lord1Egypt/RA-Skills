"""Task feature extractor for memory routing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# Keyword lists for feature extraction
_QUESTION_WORDS = {"what", "how", "why", "explain", "describe", "tell", "who", "when", "where"}
_COMPLEXITY_INDICATORS = {"then", "after", "also", "and then", "additionally", "furthermore", "multiple", "steps"}
_DOMAIN_KEYWORDS = {
    "database": {"database", "sql", "query", "table", "index", "postgres", "mysql", "mongodb"},
    "web": {"web", "html", "css", "javascript", "react", "vue", "frontend", "backend"},
    "api": {"api", "endpoint", "rest", "graphql", "http", "request", "response"},
    "ml": {"ml", "machine learning", "model", "train", "predict", "neural", "deep learning", "ai"},
    "finance": {"finance", "financial", "market", "stock", "trading", "revenue", "profit"},
    "devops": {"deploy", "docker", "kubernetes", "ci", "cd", "pipeline", "infrastructure"},
}
_TASK_TYPE_KEYWORDS = {
    "debugging": {"debug", "fix", "error", "bug", "issue", "problem", "broken"},
    "optimization": {"optimize", "performance", "speed", "efficient", "faster", "slow"},
    "implementation": {"implement", "build", "create", "develop", "add", "write", "make"},
    "analysis": {"analyze", "analysis", "compare", "evaluate", "assess", "investigate"},
    "review": {"review", "check", "audit", "inspect", "verify"},
}


@dataclass
class TaskFeatures:
    requires_knowledge: bool = False
    is_complex: bool = False
    has_history: bool = False
    domain: Optional[str] = None
    task_type: Optional[str] = None
    keywords: list[str] = field(default_factory=list)


class TaskFeatureExtractor:
    """Extract features from a query/context for memory routing."""

    def extract(self, query: str, context: Optional[dict] = None) -> TaskFeatures:
        """Extract task features from query and optional context."""
        query_lower = query.lower()
        words = set(re.findall(r"\w+", query_lower))

        # Knowledge requirement: question words or knowledge-seeking patterns
        requires_knowledge = bool(words & _QUESTION_WORDS)

        # Complexity: long query or multi-step indicators
        is_complex = (
            len(query) > 100
            or bool(words & _COMPLEXITY_INDICATORS)
            or query.count(",") > 2
        )

        # History: check context for existing task references
        has_history = False
        if context:
            has_history = bool(
                context.get("active_tasks")
                or context.get("recent_experiences")
                or context.get("continuation")
            )

        # Domain detection
        domain = None
        max_overlap = 0
        for d, kws in _DOMAIN_KEYWORDS.items():
            overlap = len(words & kws)
            if overlap > max_overlap:
                max_overlap = overlap
                domain = d

        # Task type classification
        task_type = None
        max_type_overlap = 0
        for tt, kws in _TASK_TYPE_KEYWORDS.items():
            overlap = len(words & kws)
            if overlap > max_type_overlap:
                max_type_overlap = overlap
                task_type = tt

        # Keywords: unique non-stopword terms
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                      "being", "have", "has", "had", "do", "does", "did", "will",
                      "would", "could", "should", "may", "might", "can", "shall",
                      "to", "of", "in", "for", "on", "with", "at", "by", "from",
                      "it", "this", "that", "these", "those", "i", "me", "my"}
        keywords = [w for w in words - stopwords if len(w) > 2]

        return TaskFeatures(
            requires_knowledge=requires_knowledge,
            is_complex=is_complex,
            has_history=has_history,
            domain=domain,
            task_type=task_type,
            keywords=keywords,
        )
