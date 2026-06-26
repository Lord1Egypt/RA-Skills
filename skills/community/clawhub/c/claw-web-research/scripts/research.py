#!/usr/bin/env python3
"""
Web Research Pipeline v2 — Structured Research with Follow-ups & Batch Mode
Automated research: search → fetch → follow-up → synthesize → report

Usage:
  python3 research.py "<research question>"           # Single query
  python3 research.py --batch questions.json           # Batch mode (JSON input)
  python3 research.py --format json <question>         # JSON output
  python3 research.py --format html <question>         # HTML output
  python3 research.py --followups 3 <question>         # N follow-up rounds
  python3 research.py --sources 10 <question>          # Max sources per query
"""

import sys
import json
import argparse
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple

VERSION = "2.1.0"
DATE = datetime.now().strftime("%Y-%m-%d")

class ResearchConfig:
    """Configuration for the research pipeline."""
    def __init__(self, question: str, followups: int = 2, max_sources: int = 8,
                 output_format: str = "markdown", batch_mode: bool = False):
        self.question = question
        self.followups = followups
        self.max_sources = max_sources
        self.output_format = output_format
        self.batch_mode = batch_mode
        self.date = DATE
        self.start_time = datetime.now()

    @property
    def duration(self):
        return (datetime.now() - self.start_time).seconds

    def to_dict(self):
        return {
            "version": VERSION,
            "question": self.question,
            "followups": self.followups,
            "max_sources": self.max_sources,
            "output_format": self.output_format,
            "date": self.date,
            "duration_seconds": self.duration
        }


def extract_topics(question: str) -> List[str]:
    """Extract meaningful topic keywords from a research question.

    Removes common filler words and extracts key entities.
    """
    # Remove quotes and special chars, split
    cleaned = re.sub(r'["\'\-\.\*\(\)]', '', question).lower()
    words = cleaned.split()

    # Remove stop words
    stop_words = {
        'what', 'how', 'why', 'when', 'where', 'which', 'who', 'is', 'are',
        'the', 'a', 'an', 'of', 'for', 'to', 'in', 'and', 'or', 'but', 'not',
        'with', 'without', 'about', 'this', 'that', 'these', 'those', 'it',
        'does', 'do', 'did', 'was', 'were', 'been', 'being', 'have', 'has',
        'had', 'can', 'could', 'would', 'should', 'may', 'might', 'will',
        'need', 'does', 'from', 'by', 'on', 'at', 'per', 'vs', 'or',
        '2025', '2026', '2024'
    }

    topics = [w for w in words if w not in stop_words and len(w) > 1]

    # Keep most meaningful topics (up to 6)
    return topics[:6]


def generate_search_queries(topics: List[str], n_queries: int = 5) -> List[str]:
    """Generate diverse search query variants from extracted topics.

    Creates broad, specific, and exploratory queries.
    """
    base = " ".join(topics[:3])
    queries = [
        f'"{base}"',                          # Exact match
        base,                                  # Broad match
        f'{topics[0]} {" ".join(topics[1:3])} 2025 OR 2026',  # Time-aware
        f'{topics[0]} {" ".join(topics[-2:])} analysis',       # Analytical
    ]

    # Add topic-specific variations
    if len(topics) >= 2:
        queries.append(f'{topics[0]} {topics[1]} market data')
        queries.append(f'{topics[0]} {" ".join(topics[1:])} trends')

    # Trim to n_queries, ensuring uniqueness
    queries = list(dict.fromkeys(queries))  # Preserve order, remove dupes
    return queries[:n_queries]


def deduplicate_sources(sources: List[Dict]) -> List[Dict]:
    """Remove duplicate sources by URL, keeping the one with more content."""
    seen = {}
    for source in sources:
        url = source.get("url", "")
        if url in seen:
            # Keep the one with more details
            if len(source.get("details", "")) > len(seen[url].get("details", "")):
                seen[url] = source
        else:
            seen[url] = source
    return list(seen.values())


def generate_followup_topics(findings: List[Dict], topics: List[str]) -> List[str]:
    """Generate follow-up search topics based on initial findings.

    Identifies gaps and emerging themes from the initial research.
    """
    followups = []

    # Look for recurring themes in findings
    for finding in findings:
        for key in ["title", "summary"]:
            if key in finding:
                text = finding[key].lower()
                # Look for entity mentions
                for topic in topics:
                    if topic.lower() in text:
                        followups.append(f"{topic} {' '.join(text.split()[:20])}")

    # Add time-aware follow-ups
    for topic in topics[:2]:
        followups.append(f"{topic} 2025 latest")
        followups.append(f"{topic} recent developments")

    # Remove duplicates
    followups = list(dict.fromkeys(followups))[:4]
    return followups


def score_source_quality(source: Dict) -> float:
    """Score a source's reliability (0-1 scale).

    Factors:
    - Has URL
    - Has title
    - Has details/content
    - Content length (>100 chars = quality)
    - Date information present
    """
    score = 0.0
    if source.get("url"): score += 0.2
    if source.get("title"): score += 0.15
    if source.get("details"): score += 0.3
    if len(source.get("details", "")) > 100: score += 0.2
    if source.get("date"): score += 0.15
    return min(score, 1.0)


def build_markdown_report(config: ResearchConfig, findings: List[Dict],
                          sources: List[Dict], quality_scores: List[float]) -> str:
    """Build a structured markdown research report."""
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    report = f"""# Research Report: {config.question}

**Date:** {config.date}
**Researcher:** Claw v{VERSION} (OpenClaw Agent)
**Duration:** ~{config.duration}s | **Sources:** {len(sources)} | **Quality Score:** {avg_quality:.1f}/1.0

---

## Executive Summary

{chr(10).join([f"- {f.get('summary', 'No summary available.')}" for f in findings[:5]])}

---

## Key Findings

"""

    for i, f in enumerate(findings, 1):
        score = quality_scores[i - 1] if i <= len(quality_scores) else 0
        quality_tag = f" **({score:.1f})**" if score < 0.5 else ""
        report += f"""
### {i}. {f.get('title', f'Finding {i}')}{quality_tag}

{f.get('details', 'No details available.')}
"""

    report += f"""
## Quality Assessment

| Metric | Score |
|--------|-------|
| Average source quality | {avg_quality:.1f}/1.0 |
| Sources with content (>100 chars) | {sum(1 for s in quality_scores if s > 0.3)}/{len(quality_scores)} |
| Follow-up rounds | {config.followups} |
| Sources after dedup | {len(sources)} |

---

## Limitations

- Information may be outdated or incomplete
- Sources should be verified independently
- AI-synthesized content — factual claims require human review
- {len(config.question)} follow-up rounds performed

---
**Sources:**
"""

    for i, s in enumerate(sources, 1):
        date_str = s.get("date", config.date)
        report += f"""
{i}. {s.get('title', 'Unknown source')} — {s.get('url', 'No URL')} (accessed {date_str})
"""

    return report


def build_json_report(config: ResearchConfig, findings: List[Dict],
                      sources: List[Dict], quality_scores: List[float]) -> str:
    """Build a structured JSON research report."""
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    return json.dumps({
        "version": VERSION,
        "question": config.question,
        "date": config.date,
        "duration_seconds": config.duration,
        "summary": [f.get("summary", "") for f in findings[:5]],
        "findings": findings,
        "sources": sources,
        "quality_scores": quality_scores,
        "average_quality": round(avg_quality, 2),
        "limitations": [
            "Information may be outdated or incomplete",
            "Sources should be verified independently",
            "AI-synthesized content — factual claims require human review"
        ]
    }, indent=2, ensure_ascii=False)


def build_html_report(config: ResearchConfig, findings: List[Dict],
                      sources: List[Dict], quality_scores: List[float]) -> str:
    """Build an HTML research report."""
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
    color = "green" if avg_quality >= 0.6 else "orange" if avg_quality >= 0.4 else "red"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Research Report: {config.question[:80]}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ color: #1a1a2e; }} h2 {{ border-bottom: 2px solid #eee; padding-bottom: 0.3rem; }}
  .meta {{ color: #666; margin-bottom: 1rem; }}
  .quality {{ color: {color}; font-weight: bold; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
  th {{ background: #f5f5f5; }}
  .source {{ font-size: 0.9em; color: #555; }}
</style>
</head>
<body>
<h1>Research Report</h1>
<p class="meta">
  <strong>Question:</strong> {config.question}<br>
  <strong>Date:</strong> {config.date} |
  <strong>Duration:</strong> ~{config.duration}s |
  <strong>Quality:</strong> <span class="quality">{avg_quality:.1f}/1.0</span>
</p>

<h2>Executive Summary</h2>
<ul>
{''.join([f'<li>{f.get("summary", "No summary.")}' for f in findings[:5]])}
</ul>

<h2>Key Findings</h2>
"""

    for i, f in enumerate(findings, 1):
        score = quality_scores[i - 1] if i <= len(quality_scores) else 0
        html += f"""
<div style="margin: 1rem 0; padding: 1rem; border-left: 3px solid #4a90d9; background: #fafafa;">
  <strong>{i}. {f.get('title', f'Finding {i}')} </strong>
  <span class="quality">({score:.1f})</span>
  <p>{f.get('details', 'No details.')}</p>
</div>
"""

    html += f"""
<h2>Quality Assessment</h2>
<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>Average source quality</td><td>{avg_quality:.1f}/1.0</td></tr>
<tr><td>Sources after dedup</td><td>{len(sources)}</td></tr>
<tr><td>Follow-up rounds</td><td>{config.followups}</td></tr>
</table>

<h2>Limitations</h2>
<ul>
<li>Information may be outdated or incomplete</li>
<li>Sources should be verified independently</li>
<li>AI-synthesized content — factual claims require human review</li>
</ul>

<h2>Sources</h2>
<ol>
{''.join([f'<li>{s.get("title", "Unknown")} — {s.get("url", "No URL")}</li>' for s in sources])}
</ol>
</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="Web Research Pipeline v2")
    parser.add_argument("question", nargs="?", help="Research question")
    parser.add_argument("--batch", help="JSON file with batch research questions")
    parser.add_argument("--followups", type=int, default=2,
                        help="Number of follow-up rounds (default: 2)")
    parser.add_argument("--sources", type=int, default=8,
                        help="Max sources per query variant (default: 8)")
    parser.add_argument("--format", choices=["markdown", "json", "html"],
                        default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Determine research questions
    questions = []
    if args.batch:
        with open(args.batch) as f:
            batch_data = json.load(f)
        questions = [q for q in batch_data.get("questions", [])]
        config = ResearchConfig(
            question=f"Batch research ({len(questions)} topics)",
            followups=args.followups,
            max_sources=args.sources,
            output_format=args.format
        )
    elif args.question:
        config = ResearchConfig(
            question=args.question,
            followups=args.followups,
            max_sources=args.sources,
            output_format=args.format
        )
    else:
        parser.print_help()
        return

    # Phase 1: Parse and generate queries
    for q in (questions if questions else [config.question]):
        print(f"\n📋 Research question: {q}")
        topics = extract_topics(q)
        print(f"🔍 Topics: {', '.join(topics[:4])}")
        queries = generate_search_queries(topics, n_queries=5)
        print(f"🔎 Queries: {len(queries)}")
        for i, query in enumerate(queries, 1):
            print(f"   {i}. {query}")

    # Phase 2: Pipeline summary
    print(f"\n⚙️  Pipeline:")
    print(f"   1. Execute web_search for each query variant")
    print(f"   2. Fetch content from top results (web_fetch)")
    print(f"   3. Deduplicate sources & score quality")
    print(f"   4. Generate follow-up queries ({config.followups} rounds)")
    print(f"   5. Synthesize findings & build report")
    print(f"   6. Save to workspace/research/")

    print(f"\n✅ Web Research Pipeline v{VERSION} ready.")
    print(f"   Run from OpenClaw agent with tool calls for actual execution.")
    print(f"   This script defines the pipeline logic and report builders.")

if __name__ == "__main__":
    main()
