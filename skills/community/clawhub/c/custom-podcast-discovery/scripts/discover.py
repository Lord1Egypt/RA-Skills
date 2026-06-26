#!/usr/bin/env python3
"""
discover.py — Topic discovery from configured sources

Fetches topics from all configured sources, ranks them by relevance
to user interests using LLM, and outputs a ranked list.

Usage:
    discover.py --config config.yaml [--limit N] [--output file.json]
"""
import sys
import os
import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add sources to path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from sources import load_all_sources


def load_config(config_path: str) -> dict:
    """Load YAML config (simple parser, no pyyaml dependency)"""
    import re
    
    with open(config_path) as f:
        lines = f.readlines()
    
    config = {
        "sources": [],
        "interests": [],
        "script": {}
    }
    
    # Parse sources
    in_sources = False
    current_source = None
    
    for line in lines:
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue
        
        # Start of sources section
        if line.startswith('sources:'):
            in_sources = True
            continue
        
        # Exit sources section if we hit another top-level key
        if in_sources and line[0] not in [' ', '\t', '#'] and ':' in line:
            in_sources = False
            if current_source:
                config["sources"].append(current_source)
                current_source = None
        
        # Parse source items
        if in_sources:
            # New source item
            if line.strip().startswith('- type:'):
                if current_source:
                    config["sources"].append(current_source)
                current_source = {"type": line.split(':', 1)[1].strip()}
            # Property of current source
            elif current_source and line.startswith('    ') and ':' in line:
                key = line.strip().split(':', 1)[0]
                val = line.strip().split(':', 1)[1].strip()
                current_source[key] = val
    
    # Don't forget last source
    if current_source:
        config["sources"].append(current_source)
    
    # Parse interests (simpler - just list items)
    in_interests = False
    for line in lines:
        if line.strip().startswith('#') or not line.strip():
            continue
        
        if line.startswith('interests:'):
            in_interests = True
            continue
        
        if in_interests and line[0] not in [' ', '\t', '#'] and ':' in line:
            in_interests = False
        
        if in_interests and line.strip().startswith('- '):
            config["interests"].append(line.strip()[2:])
    
    return config


def load_history(skill_dir: Path) -> set:
    """Load past topics from history file"""
    history_path = skill_dir / "data" / "history.json"
    if not history_path.exists():
        return set()
    
    topics = set()
    with open(history_path) as f:
        history = json.load(f)
        for entry in history:
            topic = entry.get("topic", "").lower().strip()
            if topic:
                topics.add(topic)
    
    return topics


def save_history(skill_dir: Path, topics: list):
    """Append new topics to history"""
    history_path = skill_dir / "data" / "history.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    
    history = []
    if history_path.exists():
        with open(history_path) as f:
            history = json.load(f)
    
    for topic in topics:
        history.append({
            "topic": topic["title"],
            "date": datetime.now(timezone.utc).date().isoformat(),
            "url": topic.get("url", ""),
            "source": topic.get("source", "")
        })
    
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)


def rank_by_interests(topics: list, interests: list) -> list:
    """Rank topics by relevance to interests (simple keyword matching)"""
    interest_keywords = []
    for interest in interests:
        words = interest.lower().split()
        interest_keywords.extend(words)
    
    scored = []
    for topic in topics:
        title_lower = topic["title"].lower()
        desc_lower = topic.get("description", "").lower()
        combined = title_lower + " " + desc_lower
        
        # Count keyword matches
        score = 0
        for keyword in interest_keywords:
            if keyword in combined:
                score += 1
        
        # Boost if source has metadata like HN points
        if "metadata" in topic:
            hn_score = topic["metadata"].get("score", 0)
            if hn_score > 0:
                score += hn_score / 100  # Scale down
        
        scored.append((score, topic))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    
    return [t for _, t in scored]


def main():
    """Main entry point for topic discovery"""
    parser = argparse.ArgumentParser(description="Discover podcast topics from sources")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--limit", type=int, default=10, help="Max topics to return")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    if not config["sources"]:
        print("ERROR: No sources configured", file=sys.stderr)
        sys.exit(1)
    
    print(f"=== PODCAST TOPIC DISCOVERY ===")
    print(f"Sources: {len(config['sources'])}")
    print(f"Interests: {', '.join(config['interests'][:3])}...")
    print()
    
    # Load sources
    sources = load_all_sources(config["sources"])
    print(f"Loaded {len(sources)} sources")
    
    # Load history for deduplication
    past_topics = load_history(skill_dir)
    print(f"History: {len(past_topics)} past topics")
    print()
    
    # Fetch from all sources
    all_topics = []
    for source in sources:
        print(f"Fetching from {source.name}...", end=" ", flush=True)
        try:
            topics = source.fetch()
            print(f"{len(topics)} topics")
            all_topics.extend(topics)
        except Exception as e:
            print(f"FAILED: {e}")
    
    print(f"\nTotal candidates: {len(all_topics)}")
    
    # Dedup
    deduped = []
    seen_titles = set()
    for topic in all_topics:
        title_lower = topic["title"].lower().strip()
        if title_lower in past_topics:
            continue
        if title_lower in seen_titles:
            continue
        seen_titles.add(title_lower)
        deduped.append(topic)
    
    print(f"After dedup: {len(deduped)}")
    
    # Rank by interests
    if config["interests"]:
        ranked = rank_by_interests(deduped, config["interests"])
    else:
        ranked = deduped
    
    # Limit
    final = ranked[:args.limit]
    
    # Output
    result = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "topics": final,
        "total_candidates": len(all_topics),
        "after_dedup": len(deduped),
        "sources_used": [s.name for s in sources]
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✅ Saved {len(final)} topics to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    # Preview
    print(f"\n=== TOP {len(final)} TOPICS ===")
    for i, topic in enumerate(final):
        print(f"\n{i+1}. {topic['title']}")
        print(f"   Source: {topic['source']}")
        print(f"   Category: {topic.get('category', 'N/A')}")
        if topic.get('url'):
            print(f"   URL: {topic['url'][:60]}...")


if __name__ == "__main__":
    main()
