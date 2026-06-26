"""Context Expander — Decides if selected chunks need surrounding context, fetches it.

After LLM chunk selection, some chunks may be "context cliffs" — the most relevant
info is in the middle of a longer document and adjacent sections add critical context.

Usage:
    python context_expander.py --selected <json_file_or_stdin> --question "..." --max-expansions 5

Input: JSON array of selected chunks (output from chunk_selector.py)
Output: JSON array with expanded content where needed
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from typing import Optional

from llm_client import call_llm as _call_glm


def _fetch_url(url: str, max_chars: int = 30000) -> Optional[str]:
    """Fetch a URL and return text content."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text" not in content_type and "json" not in content_type:
                return None
            data = resp.read(max_chars).decode(errors="replace")
            return data
    except Exception:
        return None


def expand_context(
    selected_chunks: list[dict],
    question: str,
    max_expansions: int = 5,
    api_key: Optional[str] = None,
) -> list[dict]:
    """For each chunk, decide if surrounding context would help. Fetch if so."""

    if not selected_chunks:
        return []

    # First pass: LLM decides which chunks need expansion
    expansion_decisions = _decide_expansions(selected_chunks, question, api_key=api_key)

    # Limit expansions
    to_expand = [d for d in expansion_decisions if d.get("needs_expansion", False)][
        :max_expansions
    ]

    expanded_chunks = []
    expand_urls = {d["index"] for d in to_expand}

    for i, chunk in enumerate(selected_chunks):
        if i in expand_urls:
            url = chunk.get("url", "")
            if url and url.startswith("http"):
                full_content = _fetch_url(url)
                if full_content:
                    expanded = {**chunk}
                    expanded["original_content"] = chunk.get("content", "")
                    expanded["content"] = full_content
                    expanded["expanded"] = True
                    expanded_chunks.append(expanded)
                    continue

        # No expansion needed or failed
        expanded_chunks.append({**chunk, "expanded": False})

    return expanded_chunks


def _decide_expansions(chunks: list[dict], question: str, api_key: Optional[str] = None) -> list[dict]:
    """Ask LLM which chunks need surrounding context."""
    system = (
        "You are a research context analyzer. For each chunk, decide if the "
        "research question would benefit from seeing more of the source document.\n\n"
        "A chunk needs expansion if:\n"
        "- It references something not explained ('as mentioned above', 'this approach')\n"
        "- It's clearly a fragment of a longer explanation\n"
        "- It mentions data/statistics without full context\n"
        "- It's a conclusion without the reasoning leading to it\n\n"
        'Output ONLY JSON array: [{"index": N, "needs_expansion": bool, '
        '"reason": "..."}]'
    )

    numbered = []
    for i, chunk in enumerate(chunks):
        numbered.append(
            f"[{i}] (score: {chunk.get('score', '?')})\n{chunk.get('content', '')[:1500]}"
        )

    prompt = (
        f"Question: {question}\n\n"
        f"Chunks:\n{chr(10).join(numbered)}\n\n"
        "Which chunks need more context from their source documents?"
    )

    try:
        response = _call_glm(prompt, system, max_tokens=2048, temperature=0.1, api_key=api_key)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        decisions = json.loads(response)
        if not isinstance(decisions, list):
            decisions = [decisions]
        return decisions
    except Exception:
        # On error, don't expand anything
        return [
            {"index": i, "needs_expansion": False, "reason": "LLM error"}
            for i in range(len(chunks))
        ]


def main():
    parser = argparse.ArgumentParser(
        description="Expand chunk context from source documents"
    )
    parser.add_argument("--selected", "-s", help="JSON file with selected chunks")
    parser.add_argument("--question", "-q", required=True, help="Research question")
    parser.add_argument("--max-expansions", type=int, default=5)
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    args = parser.parse_args()

    if args.stdin or not args.selected:
        chunks = json.load(sys.stdin)
    else:
        with open(args.selected) as f:
            chunks = json.load(f)

    if not isinstance(chunks, list):
        chunks = [chunks]

    expanded = expand_context(chunks, args.question, args.max_expansions)
    print(json.dumps(expanded, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
