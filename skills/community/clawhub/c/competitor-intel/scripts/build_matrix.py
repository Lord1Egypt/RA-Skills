#!/usr/bin/env python3
"""
Competitive Matrix Builder
Usage: python3 build_matrix.py --input competitors.json
       python3 build_matrix.py --interactive

Input JSON format:
[
  {
    "name": "Company A",
    "url": "https://companya.com",
    "pricing": {"free": false, "starter": "$49/mo", "growth": "$149/mo", "enterprise": "Custom"},
    "features": ["feature1", "feature2"],
    "target": "SMB SaaS",
    "positioning": "The affordable option for growing teams",
    "strengths": ["Easy setup", "Good support"],
    "weaknesses": ["No API", "Limited integrations"],
    "g2_score": 4.3,
    "review_count": 250
  }
]
"""

import json
import sys
import argparse


def build_markdown_matrix(competitors, dimensions=None):
    if not competitors:
        return "No competitors provided."

    if dimensions is None:
        dimensions = ["Pricing Start", "Free Plan", "Target Market", "Positioning", "G2 Score", "Key Strengths", "Key Weaknesses"]

    # Header
    header = "| Dimension | " + " | ".join(c["name"] for c in competitors) + " |"
    separator = "|---|" + "---|" * len(competitors)

    rows = []

    for dim in dimensions:
        row_parts = [dim]

        for comp in competitors:
            if dim == "Pricing Start":
                pricing = comp.get("pricing", {})
                starter = pricing.get("starter", pricing.get("growth", "N/A"))
                row_parts.append(str(starter))
            elif dim == "Free Plan":
                pricing = comp.get("pricing", {})
                has_free = pricing.get("free", False)
                row_parts.append("✅" if has_free else "❌")
            elif dim == "Target Market":
                row_parts.append(comp.get("target", "N/A"))
            elif dim == "Positioning":
                pos = comp.get("positioning", "N/A")
                # Truncate long positioning statements
                if len(pos) > 50:
                    pos = pos[:47] + "..."
                row_parts.append(pos)
            elif dim == "G2 Score":
                score = comp.get("g2_score", "N/A")
                count = comp.get("review_count", "")
                if score != "N/A":
                    row_parts.append(f"⭐ {score} ({count} reviews)")
                else:
                    row_parts.append("N/A")
            elif dim == "Key Strengths":
                strengths = comp.get("strengths", [])
                row_parts.append(", ".join(strengths[:2]) if strengths else "N/A")
            elif dim == "Key Weaknesses":
                weaknesses = comp.get("weaknesses", [])
                row_parts.append(", ".join(weaknesses[:2]) if weaknesses else "N/A")
            else:
                row_parts.append(comp.get(dim.lower().replace(" ", "_"), "N/A"))

        rows.append("| " + " | ".join(row_parts) + " |")

    return "\n".join([header, separator] + rows)


def build_feature_matrix(competitors):
    """Build a feature-by-feature comparison matrix."""
    # Collect all unique features
    all_features = set()
    for comp in competitors:
        all_features.update(comp.get("features", []))

    all_features = sorted(all_features)

    if not all_features:
        return "No features data available."

    header = "| Feature | " + " | ".join(c["name"] for c in competitors) + " |"
    separator = "|---|" + "---|" * len(competitors)

    rows = []
    for feature in all_features:
        row_parts = [feature]
        for comp in competitors:
            has_feature = feature in comp.get("features", [])
            row_parts.append("✅" if has_feature else "❌")
        rows.append("| " + " | ".join(row_parts) + " |")

    return "\n".join([header, separator] + rows)


def identify_gaps(competitors):
    """Find features/weaknesses that represent market gaps."""
    weakness_counts = {}
    for comp in competitors:
        for weakness in comp.get("weaknesses", []):
            weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1

    gaps = [(w, c) for w, c in weakness_counts.items() if c >= 2]
    gaps.sort(key=lambda x: x[1], reverse=True)
    return gaps


def main():
    parser = argparse.ArgumentParser(description="Competitive Matrix Builder")
    parser.add_argument("--input", help="Path to JSON file with competitor data")
    parser.add_argument("--output", default="markdown", choices=["markdown", "json"])
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r") as f:
            competitors = json.load(f)
    elif not sys.stdin.isatty():
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print("No input provided. Run with --input <file.json> or pipe JSON data.", file=sys.stderr)
            sys.exit(1)
        competitors = json.loads(stdin_data)
    else:
        # Demo mode
        competitors = [
            {
                "name": "Competitor A",
                "pricing": {"free": True, "starter": "$49/mo", "growth": "$149/mo"},
                "features": ["feature1", "feature2", "feature3"],
                "target": "SMB",
                "positioning": "The easy button for small teams",
                "strengths": ["Simple UX", "Low price"],
                "weaknesses": ["No API", "Poor reporting"],
                "g2_score": 4.2,
                "review_count": 180
            },
            {
                "name": "Competitor B",
                "pricing": {"free": False, "starter": "$99/mo", "growth": "$299/mo"},
                "features": ["feature1", "feature4", "feature5"],
                "target": "Enterprise",
                "positioning": "Enterprise-grade reliability",
                "strengths": ["Robust API", "Advanced features"],
                "weaknesses": ["Expensive", "Complex setup"],
                "g2_score": 4.5,
                "review_count": 420
            }
        ]
        print("Demo mode (no input provided). Showing sample output.\n")

    if args.output == "json":
        print(json.dumps(competitors, indent=2))
        return

    print("# Competitive Analysis Matrix\n")
    print("## Overview\n")
    print(build_markdown_matrix(competitors))

    print("\n\n## Feature Comparison\n")
    print(build_feature_matrix(competitors))

    gaps = identify_gaps(competitors)
    if gaps:
        print("\n\n## Market Gaps (Shared Weaknesses)\n")
        print("These weaknesses appear across multiple competitors — potential differentiation opportunities:\n")
        for weakness, count in gaps:
            print(f"- **{weakness}** — {count}/{len(competitors)} competitors struggle with this")


if __name__ == "__main__":
    main()
