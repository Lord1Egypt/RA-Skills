"""CertainLogic Smart Router v1.0.0

Routes queries to appropriate model tiers based on keyword/pattern matching.
Pure recommendation — skill returns model choice, agent calls LLM.

Usage:
    python3 scripts/smart_router.py "your query" [--profile coding|research|marketing]

Returns JSON: {"model_tier": "default", "confidence": 0.87, "reasoning": "..."}
"""
import json
import re
import sys
import argparse
from typing import Dict, Any, Tuple, Optional
from pathlib import Path


class SmartRouter:
    """Keyword-based query router. Returns model tier recommendations."""

    # Default profiles — user can override via config
    DEFAULT_PROFILES = {
        "coding": {
            "description": "Code generation, debugging, review",
            "keywords": {
                "cheap": ["print", "syntax", "indent", "comment", "variable"],
                "default": ["function", "class", "module", "import", "debug", "refactor"],
                "powerful": ["architecture", "system design", "optimization", "complex algorithm", "concurrency"]
            },
            "patterns": {
                "cheap": [r"^what is ", r"^how to print", r"^syntax for"],
                "default": [r"write a function", r"fix this code", r"debug this"],
                "powerful": [r"design a system", r"optimize performance", r"complex"]
            }
        },
        "research": {
            "description": "Deep analysis, synthesis, technical writing",
            "keywords": {
                "cheap": ["define", "list", "summarize briefly"],
                "default": ["analyze", "compare", "evaluate", "synthesize"],
                "powerful": ["deep dive", "comprehensive review", "meta-analysis", "systematic review"]
            },
            "patterns": {
                "cheap": [r"^what is ", r"^list the ", r"^brief"],
                "default": [r"compare and contrast", r"analyze the", r"evaluate"],
                "powerful": [r"thorough analysis", r"comprehensive", r"deep dive"]
            }
        },
        "marketing": {
            "description": "Copywriting, social media, email",
            "keywords": {
                "cheap": ["caption", "hashtag", "short", "tweet"],
                "default": ["blog post", "email", "newsletter", "product description"],
                "powerful": ["campaign strategy", "brand voice", "conversion optimization", "A/B test"]
            },
            "patterns": {
                "cheap": [r"^write a tweet", r"^caption for", r"#hashtag"],
                "default": [r"write a blog", r"draft an email", r"newsletter"],
                "powerful": [r"marketing campaign", r"brand strategy", r"conversion"]
            }
        },
        "general": {
            "description": "Default profile for uncategorized queries",
            "keywords": {
                "cheap": ["hello", "hi", "thanks", "bye", "simple"],
                "default": ["explain", "help", "how to", "what is", "why does"],
                "powerful": ["complex", "difficult", "advanced", "expert", "doctoral"]
            },
            "patterns": {
                "cheap": [r"^(hi|hello|hey)", r"^thank"],
                "default": [r"^how to", r"^what is", r"^explain"],
                "powerful": [r"advanced", r"expert level", r"complex problem"]
            }
        }
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)
        self.profiles = self.config.get("profiles", self.DEFAULT_PROFILES)

    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load user config if provided, else empty."""
        if config_path and config_path.exists():
            return json.loads(config_path.read_text())
        return {}

    def classify(self, query: str, profile_name: Optional[str] = None) -> Tuple[str, float, str]:
        """Classify query and return model tier recommendation.

        Returns: (tier, confidence, reasoning)
        tier: 'cheap' | 'default' | 'powerful'
        """
        query_lower = query.lower()

        # Auto-detect profile if not specified
        if profile_name is None:
            profile_name = self._detect_profile(query_lower)

        profile = self.profiles.get(profile_name, self.profiles["general"])

        # Score each tier
        scores = {"cheap": 0.0, "default": 0.0, "powerful": 0.0}

        # Keyword matching
        keywords = profile.get("keywords", {})
        for tier, words in keywords.items():
            matches = sum(1 for w in words if w.lower() in query_lower)
            scores[tier] += matches * 0.5

        # Pattern matching
        patterns = profile.get("patterns", {})
        for tier, pat_list in patterns.items():
            matches = sum(1 for p in pat_list if re.search(p, query_lower))
            scores[tier] += matches * 0.8

        # Normalize
        if max(scores.values()) > 0:
            max_score = max(scores.values())
            for tier in scores:
                scores[tier] /= max_score

        # Select highest scoring tier, default to 'default'
        selected_tier = max(scores, key=scores.get) if max(scores.values()) > 0 else "default"
        confidence = scores[selected_tier]

        reasoning = self._build_reasoning(selected_tier, profile_name, scores)

        return selected_tier, confidence, reasoning

    def _detect_profile(self, query_lower: str) -> str:
        """Auto-detect profile based on query content."""
        profile_scores = {}

        for name, profile in self.profiles.items():
            if name == "general":
                continue
            score = 0
            keywords = profile.get("keywords", {})
            for tier, words in keywords.items():
                score += sum(1 for w in words if w.lower() in query_lower)
            profile_scores[name] = score

        if max(profile_scores.values(), default=0) > 0:
            return max(profile_scores, key=profile_scores.get)
        return "general"

    def _build_reasoning(self, tier: str, profile: str, scores: Dict[str, float]) -> str:
        parts = [f"Profile: {profile}", f"Tier: {tier}"]
        for t, s in scores.items():
            if s > 0:
                parts.append(f"{t} score: {s:.2f}")
        return " | ".join(parts)

    def route(self, query: str, profile: Optional[str] = None,
              force_cheap: bool = False, force_powerful: bool = False) -> Dict[str, Any]:
        """Full routing with override support."""
        if force_cheap:
            return {
                "query": query,
                "profile": profile or "general",
                "model_tier": "cheap",
                "confidence": 1.0,
                "reasoning": "Forced cheap via --cheap flag",
                "override": True
            }

        if force_powerful:
            return {
                "query": query,
                "profile": profile or "general",
                "model_tier": "powerful",
                "confidence": 1.0,
                "reasoning": "Forced powerful via --powerful flag",
                "override": True
            }

        tier, confidence, reasoning = self.classify(query, profile)

        return {
            "query": query,
            "profile": profile or self._detect_profile(query.lower()),
            "model_tier": tier,
            "confidence": confidence,
            "reasoning": reasoning,
            "override": False
        }


def main():
    parser = argparse.ArgumentParser(description="CertainLogic Smart Router")
    parser.add_argument("query", help="Query to route")
    parser.add_argument("--profile", choices=["coding", "research", "marketing", "general"],
                        help="Force profile")
    parser.add_argument("--cheap", action="store_true", help="Force cheap tier")
    parser.add_argument("--powerful", action="store_true", help="Force powerful tier")
    parser.add_argument("--config", type=Path, help="Path to custom config JSON")

    args = parser.parse_args()

    router = SmartRouter(config_path=args.config)
    result = router.route(
        args.query,
        profile=args.profile,
        force_cheap=args.cheap,
        force_powerful=args.powerful
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
