"""Adaptive query classifier for tuning hybrid search alpha."""

import re
from typing import Dict, Optional

from ghostclaw.core.config import GhostclawConfig


class QueryClassifier:
    """
    Classifies query characteristics to determine optimal BM25/vector alpha.
    Alpha range: 0.3 (vector heavy) to 0.9 (BM25 heavy).
    """

    def __init__(self, config: Optional[GhostclawConfig] = None, custom_weights: Optional[Dict] = None):
        """
        Initialize classifier.

        Args:
            config: GhostclawConfig instance (reads qmd.query_classifier if exists)
            custom_weights: Override feature weights as dict
        """
        # Default weights for feature adjustments
        self.weights = {
            'exact_quotes': 0.3,
            'code_symbols': 0.2,
            'filters': 0.1,
        }
        if custom_weights:
            self.weights.update(custom_weights)
        elif config:
            # Try to load from config under qmd.query_classifier.feature_weights
            qmd_cfg = getattr(config, 'qmd', {}) if hasattr(config, 'qmd') else {}
            classifier_cfg = qmd_cfg.get('query_classifier', {})
            if 'feature_weights' in classifier_cfg:
                self.weights.update(classifier_cfg['feature_weights'])

    def classify(self, query: str, filters: Optional[Dict] = None) -> float:
        """
        Compute alpha for hybrid search based on query features.

        Strategy:
        - Very short (<=3 tokens): alpha = 0.9
        - Long (>=10 tokens): alpha = 0.3
        - Medium (4-9 tokens): alpha = 0.6 + adjustments

        Adjustments (added to medium base):
        - Exact quotes: +0.2
        - Code symbols: +0.1
        - Filters: +0.1
        """
        token_count = len(query.split())

        if token_count <= 3:
            return 0.9
        if token_count >= 10:
            return 0.3

        # Medium base
        alpha = 0.6

        # Exact quotes strongly favor BM25
        if '"' in query or "'" in query:
            alpha += self.weights['exact_quotes']

        # Code-like symbols (camelCase, snake_case, dots) → BM25 good
        if any(char in query for char in ['.', '_']) or re.search(r'[a-z]+[A-Z]', query):
            alpha += self.weights['code_symbols']

        # Filters present (repo_path, stack) → narrower search, BM25 OK
        if filters and (filters.get('repo_path') or filters.get('stack')):
            alpha += self.weights['filters']

        # Clamp to valid range
        alpha = max(0.3, min(0.9, alpha))
        return round(alpha, 2)
