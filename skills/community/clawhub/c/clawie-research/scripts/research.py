#!/usr/bin/env python3
"""
Research helper script for the research-agent skill.
Provides utilities for gathering and analyzing research data.
"""

import json
import subprocess
import sys
from datetime import datetime

def github_search(topic: str, limit: int = 20) -> list:
    """Search GitHub repos for a topic."""
    try:
        result = subprocess.run(
            ["gh", "search", "repos", topic, "--limit", str(limit),
             "--json", "name,description,stargazersCount,url,updatedAt,language"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"GitHub search failed: {e}", file=sys.stderr)
        return []

def npm_search(package: str, limit: int = 5) -> list:
    """Search NPM for packages."""
    try:
        result = subprocess.run(
            ["npm", "search", package, "--json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            return packages[:limit]
    except Exception as e:
        print(f"NPM search failed: {e}", file=sys.stderr)
    return []

def generate_report_metadata(topic: str, sources_count: int) -> dict:
    """Generate metadata for a research report."""
    return {
        "topic": topic,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "researcher": "Clawie (AI Research Agent)",
        "sources_analyzed": sources_count,
        "generated_at": datetime.now().isoformat()
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: research.py <command> [args]")
        print("Commands:")
        print("  github <topic> [limit]  - Search GitHub repos")
        print("  npm <package> [limit]   - Search NPM packages")
        print("  meta <topic> <sources>  - Generate report metadata")
        sys.exit(1)

    command = sys.argv[1]

    if command == "github":
        topic = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        results = github_search(topic, limit)
        print(json.dumps(results, indent=2))

    elif command == "npm":
        package = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        results = npm_search(package, limit)
        print(json.dumps(results, indent=2))

    elif command == "meta":
        topic = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
        sources = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        metadata = generate_report_metadata(topic, sources)
        print(json.dumps(metadata, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()