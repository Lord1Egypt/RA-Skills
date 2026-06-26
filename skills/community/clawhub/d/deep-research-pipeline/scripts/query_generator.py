"""Query Generator — Generates multiple search query variants for a research question.

Usage:
    python query_generator.py --question "How does RAG work?" --max-queries 5
    echo '{"question": "..."}' | python query_generator.py --stdin

Output: JSON array of query objects with type, query, and rationale.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from typing import Optional

from llm_client import call_llm as _call_glm


def generate_queries(
    question: str,
    max_queries: int = 5,
    api_key: Optional[str] = None,
) -> list[dict]:
    """Generate multiple search query variants using LLM + rule-based expansion.

    Returns list of dicts: [{"type": str, "query": str, "rationale": str}]
    """

    system = (
        "You are a research query generator. Given a research question, "
        "generate diverse search query variants. Each should cover a different "
        "angle or aspect. Output ONLY valid JSON array, no markdown."
    )

    prompt = f"""Generate {max_queries} search query variants for this research question:

"{question}"

Rules:
- Mix broad and specific queries
- Include technical and layperson phrasings
- Include at least one query targeting recent developments (add year if helpful)
- Include at least one query targeting comparisons or alternatives
- No duplicate intents

Output JSON array: [{{"type": "semantic|keyword|broad|specific|comparative", "query": "...", "rationale": "..."}}]"""

    try:
        response = _call_glm(prompt, system, max_tokens=2048, temperature=0.7, api_key=api_key)
        # Strip markdown fences if present
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        queries = json.loads(response)
        if not isinstance(queries, list):
            queries = [queries]
        return queries[:max_queries]
    except Exception:
        # Fallback: rule-based query generation
        return _rule_based_queries(question, max_queries)


def _rule_based_queries(question: str, max_queries: int) -> list[dict]:
    """Fallback: generate query variants without LLM."""
    queries = []

    # Original
    queries.append(
        {
            "type": "semantic",
            "query": question,
            "rationale": "Original question",
        }
    )

    # Add "how" variant
    if not question.lower().startswith("how"):
        queries.append(
            {
                "type": "specific",
                "query": f"how does {question.lower().rstrip('?')}",
                "rationale": "Procedural angle",
            }
        )

    # Add comparison variant
    queries.append(
        {
            "type": "comparative",
            "query": f"{question} alternatives compared 2026",
            "rationale": "Comparison angle with recency",
        }
    )

    # Add broad variant — remove modifiers
    words = question.split()
    if len(words) > 4:
        core = " ".join(words[:4])
        queries.append(
            {
                "type": "broad",
                "query": core,
                "rationale": "Broader search, fewer modifiers",
            }
        )

    # Add "best practices" variant
    queries.append(
        {
            "type": "keyword",
            "query": f"best practices {question.lower().rstrip('?')} 2026",
            "rationale": "Practical guidance angle",
        }
    )

    return queries[:max_queries]


def main():
    parser = argparse.ArgumentParser(description="Generate search query variants")
    parser.add_argument("--question", "-q", help="Research question")
    parser.add_argument("--max-queries", "-n", type=int, default=5)
    parser.add_argument(
        "--stdin", action="store_true", help="Read question from stdin JSON"
    )
    args = parser.parse_args()

    if args.stdin:
        data = json.load(sys.stdin)
        question = data.get("question", data.get("q", ""))
    elif args.question:
        question = args.question
    else:
        print("Error: provide --question or --stdin", file=sys.stderr)
        sys.exit(1)

    queries = generate_queries(question, args.max_queries)
    print(json.dumps(queries, indent=2))


if __name__ == "__main__":
    main()
