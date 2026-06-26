#!/usr/bin/env python3
"""
Print a human-readable summary of merged JSON data for LLM consumption.

Usage:
    python3 summarize-merged.py [--input /tmp/td-merged.json] [--top N] [--topic TOPIC]
"""

import json
import argparse
from pathlib import Path


def display_transcript_status(article: dict) -> str:
    """Return the human-facing transcript state for podcast summaries."""
    status = article.get("transcript_status", "missing")
    if status == "ok" and article.get("transcript"):
        return "ready"
    return status


def summarize(data: dict, top_n: int = 10, topic_filter: str = None):
    """Print structured summary of merged data."""
    
    # Metadata
    meta = data.get("output_stats", {})
    print(f"=== Merged Data Summary ===")
    print(f"Total articles: {meta.get('total_articles', '?')}")
    print(f"Topics: {', '.join(data.get('topics', {}).keys())}")
    print()
    
    topics = data.get("topics", {})
    
    for topic_id, topic_data in topics.items():
        if topic_filter and topic_id != topic_filter:
            continue
        
        articles = topic_data.get("articles", [])
        if not isinstance(articles, list):
            continue
        
        print(f"=== {topic_id} ({len(articles)} articles) ===")
        
        # Sort by quality_score descending
        sorted_articles = sorted(
            [a for a in articles if isinstance(a, dict)],
            key=lambda a: a.get("quality_score", 0),
            reverse=True
        )
        
        for i, a in enumerate(sorted_articles[:top_n]):
            title = a.get("title", "?")[:100]
            source = a.get("source_name", "?")
            source_type = a.get("source_type", "?")
            qs = a.get("quality_score", 0)
            link = a.get("link") or a.get("reddit_url") or a.get("external_url", "")
            snippet = (a.get("snippet") or a.get("summary") or "")[:150]
            
            # Metrics for Twitter
            metrics = a.get("metrics", {})
            display_name = a.get("display_name", "")
            
            print(f"\n  [{i+1}] ({qs:.0f}pts) [{source_type}] {title}")
            print(f"      Source: {source}", end="")
            if display_name:
                print(f" ({display_name})", end="")
            print()
            if link:
                print(f"      Link: {link}")
            if snippet:
                print(f"      Snippet: {snippet}")
            if metrics:
                parts = []
                for k, v in metrics.items():
                    if v and v > 0:
                        parts.append(f"{k}={v}")
                if parts:
                    print(f"      Metrics: {', '.join(parts)}")
            
            # Reddit-specific
            reddit_score = a.get("score")
            num_comments = a.get("num_comments")
            if reddit_score is not None:
                print(f"      Reddit: {reddit_score}↑", end="")
                if num_comments:
                    print(f" · {num_comments} comments", end="")
                print()

            if source_type == "podcast":
                transcript_status = display_transcript_status(a)
                show_name = a.get("show_name") or source
                print(f"      Podcast: {show_name} · transcript={transcript_status}")
                if a.get("duration_seconds"):
                    print(f"      Duration: {a['duration_seconds']}s")
        
        print()


def main():
    parser = argparse.ArgumentParser(description="Summarize merged JSON for LLM consumption")
    parser.add_argument("--input", "-i", type=Path, default=Path("/tmp/td-merged.json"))
    parser.add_argument("--top", "-n", type=int, default=10, help="Top N articles per topic")
    parser.add_argument("--topic", "-t", type=str, default=None, help="Filter to specific topic")
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: {args.input} not found. Run the pipeline first.")
        return
    
    with open(args.input) as f:
        data = json.load(f)
    
    summarize(data, top_n=args.top, topic_filter=args.topic)


if __name__ == "__main__":
    main()
