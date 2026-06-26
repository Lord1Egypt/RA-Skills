#!/usr/bin/env python3
"""analyze_trends.py — Moltbook snapshot analyzer.

Reads snapshot JSONs and generates a markdown report with virality metrics,
top posts, author leaderboard, and content signal analysis.

Usage:
    python3 analyze_trends.py <path> [<path> ...]
    python3 analyze_trends.py /skills/moltbook-trend-analysis/data/snapshots/

Paths can be individual .json files or directories (all .json inside are loaded).
"""

import json
import os
import sys
import re
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Virality benchmarks from analysis_summary.json (real research data)
# Keys: feature -> { hour: {mean_top, mean_ctrl, smd/lift}, day: ..., week: ... }
# ---------------------------------------------------------------------------
VIRALITY_BENCHMARKS = {
    # ----- numeric features (SMD) -----
    "score": {
        "hour":  {"mean_top": 6.94,   "mean_ctrl": 0.97,   "smd": 1.637},
        "day":   {"mean_top": 102.0,  "mean_ctrl": 0.95,   "smd": 1.244},
        "week":  {"mean_top": 360.08, "mean_ctrl": 6.63,   "smd": 1.779},
        "month": {"mean_top": 907.18, "mean_ctrl": 24.07,  "smd": 1.813},
    },
    "title_words": {
        "hour":  {"mean_top": 9.68,   "mean_ctrl": 4.87,   "smd": 0.978},
        "day":   {"mean_top": 11.78,  "mean_ctrl": 4.91,   "smd": 1.130},
        "week":  {"mean_top": 16.26,  "mean_ctrl": 9.77,   "smd": 1.042},
        "month": {"mean_top": 14.53,  "mean_ctrl": 9.96,   "smd": 0.812},
    },
    "body_words": {
        "hour":  {"mean_top": 232.52, "mean_ctrl": 73.85,  "smd": 0.915},
        "day":   {"mean_top": 297.07, "mean_ctrl": 89.07,  "smd": 1.034},
        "week":  {"mean_top": 523.88, "mean_ctrl": 204.24, "smd": 1.095},
        "month": {"mean_top": 514.68, "mean_ctrl": 302.76, "smd": 0.621},
    },
    "comments": {
        "hour":  {"mean_top": 4.26,   "mean_ctrl": 1.52,   "smd": 0.905},
        "day":   {"mean_top": 135.99, "mean_ctrl": 1.17,   "smd": 0.954},
        "week":  {"mean_top": 810.79, "mean_ctrl": 4.67,   "smd": 1.342},
        "month": {"mean_top": 1680.77,"mean_ctrl": 10.08,  "smd": 1.572},
    },
    "score_per_hour": {
        "hour":  {"mean_top": 27.54,  "mean_ctrl": 3.33,   "smd": 0.844},
        "day":   {"mean_top": 14.27,  "mean_ctrl": 0.16,   "smd": 0.935},
        "week":  {"mean_top": 7.09,   "mean_ctrl": 0.15,   "smd": 0.954},
        "month": {"mean_top": 3.88,   "mean_ctrl": 0.11,   "smd": 1.663},
    },
    "comments_per_hour": {
        "hour":  {"mean_top": 14.87,  "mean_ctrl": 4.19,   "smd": 0.725},
        "day":   {"mean_top": 15.72,  "mean_ctrl": 0.18,   "smd": 0.985},
        "week":  {"mean_top": 14.24,  "mean_ctrl": 0.10,   "smd": 1.116},
        "month": {"mean_top": 8.11,   "mean_ctrl": 0.05,   "smd": 1.145},
    },
    "collab_terms": {
        "hour":  {"mean_top": 5.24,   "mean_ctrl": 1.23,   "smd": 0.820},
        "day":   {"mean_top": 6.99,   "mean_ctrl": 1.88,   "smd": 0.888},
        "week":  {"mean_top": 9.92,   "mean_ctrl": 4.60,   "smd": 0.866},
        "month": {"mean_top": 9.51,   "mean_ctrl": 6.69,   "smd": 0.435},
    },
    "identity_terms": {
        "hour":  {"mean_top": 8.49,   "mean_ctrl": 2.27,   "smd": 0.800},
        "day":   {"mean_top": 11.42,  "mean_ctrl": 3.26,   "smd": 0.828},
        "week":  {"mean_top": 17.63,  "mean_ctrl": 8.31,   "smd": 0.866},
        "month": {"mean_top": 18.43,  "mean_ctrl": 13.29,  "smd": 0.355},
    },
    "body_paragraphs": {
        "hour":  {"mean_top": 13.62,  "mean_ctrl": 4.12,   "smd": 0.695},
        "day":   {"mean_top": 18.62,  "mean_ctrl": 6.22,   "smd": 0.778},
        "week":  {"mean_top": 25.58,  "mean_ctrl": 11.58,  "smd": 0.959},
        "month": {"mean_top": 25.25,  "mean_ctrl": 19.37,  "smd": 0.221},
    },
    "revelation_terms": {
        "hour":  {"mean_top": 1.53,   "mean_ctrl": 0.31,   "smd": 0.686},
        "day":   {"mean_top": 2.47,   "mean_ctrl": 0.33,   "smd": 0.923},
        "week":  {"mean_top": 4.59,   "mean_ctrl": 1.46,   "smd": 0.838},
        "month": {"mean_top": 3.73,   "mean_ctrl": 1.97,   "smd": 0.506},
    },
    "authority_terms": {
        "hour":  {"mean_top": 1.43,   "mean_ctrl": 0.29,   "smd": 0.674},
        "day":   {"mean_top": 2.64,   "mean_ctrl": 0.15,   "smd": 0.912},
        "week":  {"mean_top": 4.52,   "mean_ctrl": 1.63,   "smd": 0.770},
        "month": {"mean_top": 4.63,   "mean_ctrl": 2.93,   "smd": 0.293},
    },
    "measure_terms": {
        "hour":  {"mean_top": 0.30,   "mean_ctrl": 0.02,   "smd": 0.619},
        "day":   {"mean_top": 0.77,   "mean_ctrl": 0.01,   "smd": 0.732},
        "week":  {"mean_top": 2.09,   "mean_ctrl": 0.43,   "smd": 0.919},
        "month": {"mean_top": 1.68,   "mean_ctrl": 0.44,   "smd": 0.744},
    },
    "body_headings": {
        "hour":  {"mean_top": 0.92,   "mean_ctrl": 0.14,   "smd": 0.431},
        "day":   {"mean_top": 1.15,   "mean_ctrl": 0.32,   "smd": 0.418},
        "week":  {"mean_top": 2.74,   "mean_ctrl": 0.88,   "smd": 0.701},
        "month": {"mean_top": 2.67,   "mean_ctrl": 1.57,   "smd": 0.309},
    },
    "threat_terms": {
        "hour":  {"mean_top": 0.95,   "mean_ctrl": 0.16,   "smd": 0.568},
        "day":   {"mean_top": 1.23,   "mean_ctrl": 0.17,   "smd": 0.650},
        "week":  {"mean_top": 2.38,   "mean_ctrl": 0.79,   "smd": 0.499},
        "month": {"mean_top": 2.10,   "mean_ctrl": 1.36,   "smd": 0.235},
    },
    # ----- binary features (lift) -----
    "body_has_first_person": {
        "hour":  {"top_rate": 0.76, "ctrl_rate": 0.23, "lift": 3.30},
        "day":   {"top_rate": 0.88, "ctrl_rate": 0.24, "lift": 3.67},
        "week":  {"top_rate": None,  "ctrl_rate": None,  "lift": None},
    },
    "body_has_second_person": {
        "hour":  {"top_rate": 0.68, "ctrl_rate": 0.26, "lift": 2.62},
        "day":   {"top_rate": 0.78, "ctrl_rate": 0.22, "lift": 3.55},
        "week":  {"top_rate": 0.92, "ctrl_rate": 0.67, "lift": 1.37},
    },
    "body_has_question": {
        "hour":  {"top_rate": 0.59, "ctrl_rate": 0.33, "lift": 1.79},
        "day":   {"top_rate": 0.75, "ctrl_rate": 0.28, "lift": 2.68},
        "week":  {"top_rate": None,  "ctrl_rate": None,  "lift": None},
    },
    "title_period": {
        "hour":  {"top_rate": 0.27, "ctrl_rate": 0.06, "lift": 4.50},
        "day":   {"top_rate": 0.38, "ctrl_rate": 0.04, "lift": 9.50},
        "week":  {"top_rate": 0.79, "ctrl_rate": 0.27, "lift": 2.93},
        "month": {"top_rate": 0.64, "ctrl_rate": 0.22, "lift": 2.91},
    },
    "title_has_first_person": {
        "day":   {"top_rate": 0.34, "ctrl_rate": 0.04, "lift": 8.50},
        "week":  {"top_rate": 0.61, "ctrl_rate": 0.25, "lift": 2.44},
        "month": {"top_rate": 0.49, "ctrl_rate": 0.27, "lift": 1.81},
    },
    "title_problem_frame": {
        "hour":  {"top_rate": 0.25, "ctrl_rate": 0.04, "lift": 6.25},
    },
    "title_solution_frame": {
        "hour":  {"top_rate": 0.33, "ctrl_rate": 0.10, "lift": 3.30},
        "day":   {"top_rate": 0.40, "ctrl_rate": 0.11, "lift": 3.64},
    },
    "has_list": {
        "hour":  {"top_rate": 0.34, "ctrl_rate": 0.10, "lift": 3.40},
        "day":   {"top_rate": 0.44, "ctrl_rate": 0.15, "lift": 2.93},
        "week":  {"top_rate": None,  "ctrl_rate": None,  "lift": None},
        "month": {"top_rate": 0.62, "ctrl_rate": 0.36, "lift": 1.72},
    },
}

# Top authors from research (author, timeframe, count_in_top100)
KNOWN_TOP_AUTHORS = {
    "Hazel_OC":            {"week": 72, "month": 50, "all": 37, "karma": 61323},
    "clawdbottom":         {"day": 13,  "week": 5,   "karma": 5375},
    "Cornelius-Trinity":   {"week": 3,  "karma": 3530},
    "sirclawat":           {"day": 7},
    "Starfish":            {"day": 5,   "hour": 3},
    "Kevin":               {"day": 4},
    "sparkxu":             {"day": 2},
    "nova-morpheus":       {"week": 10},
    "SparkLabScout":       {"day": 3,   "week": 2},
    "HarryBotter_Weggel":  {"day": 3},
    "JS_BestAgent":        {"day": 4,   "hour": 2},
    "zhuanruhu":           {"day": 4},
    "CorvusLatimer":       {"day": 4},
    "PDMN":                {"month": 3, "all": 3},
    "ultrathink":          {"month": 3},
}


def load_snapshots(paths):
    """Load snapshot JSON files from paths (files or directories)."""
    snapshots = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files = sorted(p.glob("*.json"))
        elif p.is_file():
            files = [p]
        else:
            print(f"WARNING: skipping {p} (not found)", file=sys.stderr)
            continue
        for f in files:
            if f.name.startswith("."):
                continue
            try:
                with open(f) as fh:
                    data = json.load(fh)
                data["_file"] = str(f)
                snapshots.append(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"WARNING: could not load {f}: {e}", file=sys.stderr)
    return snapshots


def compute_post_metrics(post, now_utc):
    """Derive velocity and ratio metrics for a single post."""
    score = post.get("upvotes", 0) - post.get("downvotes", 0)
    comments = post.get("comment_count", 0)
    created = post.get("created_at", "")
    age_hours = 0.001  # avoid division by zero
    if created:
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            age_hours = max((now_utc - dt).total_seconds() / 3600.0, 0.001)
        except (ValueError, TypeError):
            pass
    return {
        "score": score,
        "comments": comments,
        "age_hours": age_hours,
        "score_per_hour": score / age_hours,
        "comments_per_hour": comments / age_hours,
        "comment_score_ratio": comments / max(score, 1),
        "author": post.get("author", {}).get("name", "[deleted]"),
        "author_karma": post.get("author", {}).get("karma", 0),
        "title": post.get("title", "(untitled)"),
        "id": post.get("id", ""),
        "submolt": post.get("submolt_name", ""),
        "created_at": created,
        "content": post.get("content", ""),
    }


def count_words(text):
    """Simple word count."""
    return len(text.split()) if text else 0


def extract_content_features(post_metric):
    """Extract content features to compare against benchmarks."""
    title = post_metric["title"]
    body = post_metric["content"]

    title_words_count = count_words(title)
    body_words_count = count_words(body)

    # Count paragraphs (non-empty lines — matches how Moltbook renders markdown)
    paragraphs = [line for line in body.splitlines() if line.strip()] if body else []
    body_paragraphs = len(paragraphs)

    # Headings (## or # lines)
    headings = len(re.findall(r'^#{1,3}\s', body, re.MULTILINE)) if body else 0

    # List items (- or * or numbered)
    list_items = len(re.findall(r'^\s*[-*]\s|^\s*\d+\.\s', body, re.MULTILINE)) if body else 0

    # Binary features
    first_person = bool(re.search(r'\bI\b|\bmy\b|\bme\b|\bmyself\b', body, re.IGNORECASE)) if body else False
    second_person = bool(re.search(r'\byou\b|\byour\b|\byourself\b', body, re.IGNORECASE)) if body else False
    has_question = bool(re.search(r'\?', body)) if body else False
    has_collective = bool(re.search(r'\bwe\b|\bus\b|\bour\b|\bourselves\b', body, re.IGNORECASE)) if body else False

    # Title features
    title_period = title.rstrip().endswith(".")
    title_has_first_person = bool(re.search(r'\bI\b|\bmy\b', title)) if title else False
    title_starts_i = title.strip().startswith("I ") if title else False
    has_list = list_items > 0

    # Term counts (approximate — simple keyword matching)
    identity_re = r'\bI\b|\bmy\b|\bme\b|\bmyself\b|\bagent\b|\bidentity\b|\bself\b'
    collab_re = r'\bwe\b|\bus\b|\bour\b|\btogether\b|\bcommunity\b|\bcollabora'
    revelation_re = r'\bfound\b|\bdiscovered\b|\brealized\b|\blearned\b|\bturns out\b|\breveal'
    authority_re = r'\bdata\b|\bevidence\b|\bmeasured\b|\bresearch\b|\banalysis\b|\bshows\b'
    measure_re = r'\b\d+%|\b\d+x\b|\b\d+\.\d+\b|\bmetric|\bbenchmark'
    threat_re = r'\brisk\b|\bdanger\b|\bfail\b|\bwaste\b|\bkill\b|\bdie\b|\bthreat\b|\bwarn'

    full_text = (title + " " + body) if body else title

    return {
        "title_words": title_words_count,
        "body_words": body_words_count,
        "body_paragraphs": body_paragraphs,
        "body_headings": headings,
        "body_list_items": list_items,
        "body_has_first_person": first_person,
        "body_has_second_person": second_person,
        "body_has_question": has_question,
        "body_has_collective": has_collective,
        "title_period": title_period,
        "title_has_first_person": title_has_first_person,
        "has_list": has_list,
        "identity_terms": len(re.findall(identity_re, full_text, re.IGNORECASE)),
        "collab_terms": len(re.findall(collab_re, full_text, re.IGNORECASE)),
        "revelation_terms": len(re.findall(revelation_re, full_text, re.IGNORECASE)),
        "authority_terms": len(re.findall(authority_re, full_text, re.IGNORECASE)),
        "measure_terms": len(re.findall(measure_re, full_text, re.IGNORECASE)),
        "threat_terms": len(re.findall(threat_re, full_text, re.IGNORECASE)),
    }


def smd_interpretation(smd):
    """Human-readable SMD interpretation."""
    a = abs(smd)
    if a >= 0.8:
        return "LARGE"
    elif a >= 0.5:
        return "MEDIUM"
    elif a >= 0.2:
        return "SMALL"
    else:
        return "negligible"


def format_age(hours):
    """Format age in hours to a human-readable string."""
    if hours < 1:
        return f"{hours*60:.0f}m"
    elif hours < 24:
        return f"{hours:.1f}h"
    else:
        return f"{hours/24:.1f}d"


def generate_report(snapshots):
    """Generate the full markdown analysis report."""
    now_utc = datetime.now(timezone.utc)
    lines = []
    lines.append(f"# Moltbook Trend Analysis Report")
    lines.append(f"")
    lines.append(f"Generated: {now_utc.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Snapshots analyzed: {len(snapshots)}")
    lines.append(f"")

    # ---- Snapshot summary table ----
    lines.append(f"## Snapshot Summary")
    lines.append(f"")
    lines.append(f"| File | Submolt | Timeframe | Posts | Avg Score | Max Score |")
    lines.append(f"|---|---|---|---|---|---|")

    all_posts = []
    for snap in snapshots:
        req = snap.get("request", {})
        summary = snap.get("summary", {})
        fname = os.path.basename(snap.get("_file", "unknown"))
        posts = snap.get("posts", [])
        all_posts.extend(posts)
        lines.append(f"| {fname} | {req.get('submolt','-')} | {req.get('timeframe','-')} | {len(posts)} | {summary.get('avgScore',0):.1f} | {summary.get('maxScore',0)} |")

    lines.append(f"")
    lines.append(f"**Total posts across all snapshots: {len(all_posts)}**")
    lines.append(f"")

    if not all_posts:
        lines.append("No posts to analyze.")
        return "\n".join(lines)

    # ---- Compute metrics for all posts ----
    metrics = [compute_post_metrics(p, now_utc) for p in all_posts]

    # Deduplicate by post ID (keep first occurrence)
    seen_ids = set()
    unique_metrics = []
    for m in metrics:
        if m["id"] and m["id"] in seen_ids:
            continue
        seen_ids.add(m["id"])
        unique_metrics.append(m)

    lines.append(f"**Unique posts (deduplicated): {len(unique_metrics)}**")
    lines.append(f"")

    # ---- Top posts by score ----
    by_score = sorted(unique_metrics, key=lambda x: x["score"], reverse=True)
    lines.append(f"## Top 25 Posts by Score")
    lines.append(f"")
    lines.append(f"| # | Title | Author | Score | Comments | Age | Velocity |")
    lines.append(f"|---|---|---|---|---|---|---|")
    for i, m in enumerate(by_score[:25], 1):
        title = m["title"][:80] + ("..." if len(m["title"]) > 80 else "")
        lines.append(f"| {i} | {title} | {m['author']} | {m['score']} | {m['comments']} | {format_age(m['age_hours'])} | {m['score_per_hour']:.1f}/hr |")
    lines.append(f"")

    # ---- Top posts by velocity ----
    by_velocity = sorted(unique_metrics, key=lambda x: x["score_per_hour"], reverse=True)
    lines.append(f"## Top 25 Posts by Velocity (score/hr)")
    lines.append(f"")
    lines.append(f"| # | Title | Author | Score/hr | Score | Age | Comments |")
    lines.append(f"|---|---|---|---|---|---|---|")
    for i, m in enumerate(by_velocity[:25], 1):
        title = m["title"][:80] + ("..." if len(m["title"]) > 80 else "")
        lines.append(f"| {i} | {title} | {m['author']} | {m['score_per_hour']:.1f} | {m['score']} | {format_age(m['age_hours'])} | {m['comments']} |")
    lines.append(f"")

    # ---- Rising fast (< 4h old, highest velocity) ----
    rising = [m for m in unique_metrics if m["age_hours"] < 4.0]
    rising.sort(key=lambda x: x["score_per_hour"], reverse=True)
    lines.append(f"## Rising Fast (< 4 hours old)")
    lines.append(f"")
    if rising:
        lines.append(f"| # | Title | Author | Score/hr | Score | Age | Comments |")
        lines.append(f"|---|---|---|---|---|---|---|")
        for i, m in enumerate(rising[:15], 1):
            title = m["title"][:80] + ("..." if len(m["title"]) > 80 else "")
            lines.append(f"| {i} | {title} | {m['author']} | {m['score_per_hour']:.1f} | {m['score']} | {format_age(m['age_hours'])} | {m['comments']} |")
    else:
        lines.append("No posts younger than 4 hours found in this snapshot.")
    lines.append(f"")

    # ---- Author leaderboard ----
    author_stats = defaultdict(lambda: {"count": 0, "total_score": 0, "max_score": 0, "posts": []})
    for m in unique_metrics:
        a = m["author"]
        author_stats[a]["count"] += 1
        author_stats[a]["total_score"] += m["score"]
        author_stats[a]["max_score"] = max(author_stats[a]["max_score"], m["score"])
        author_stats[a]["posts"].append(m)

    author_board = sorted(author_stats.items(), key=lambda x: x[1]["total_score"], reverse=True)
    lines.append(f"## Author Leaderboard (Top 25)")
    lines.append(f"")
    lines.append(f"| # | Author | Posts | Total Score | Avg Score | Max Score | Known Top? |")
    lines.append(f"|---|---|---|---|---|---|---|")
    for i, (author, stats) in enumerate(author_board[:25], 1):
        avg = stats["total_score"] / max(stats["count"], 1)
        known = "YES" if author in KNOWN_TOP_AUTHORS else ""
        lines.append(f"| {i} | {author} | {stats['count']} | {stats['total_score']} | {avg:.1f} | {stats['max_score']} | {known} |")
    lines.append(f"")

    # ---- Content signal analysis ----
    # Compute average features for all posts
    all_features = [extract_content_features(m) for m in unique_metrics]
    numeric_features = ["title_words", "body_words", "body_paragraphs", "body_headings",
                        "identity_terms", "collab_terms", "revelation_terms", "authority_terms",
                        "measure_terms", "threat_terms"]
    # Note: body_has_collective is computed but not in binary benchmarks (use collab_terms numeric instead)
    binary_features = ["body_has_first_person", "body_has_second_person", "body_has_question",
                       "title_period", "title_has_first_person", "has_list"]

    lines.append(f"## Content Signal Analysis vs Benchmarks")
    lines.append(f"")
    lines.append(f"### Numeric Features (snapshot avg vs top-100 benchmarks)")
    lines.append(f"")
    lines.append(f"| Feature | Snapshot Avg | Day Top-100 | Day Control | Day SMD | Status |")
    lines.append(f"|---|---|---|---|---|---|")

    for feat in numeric_features:
        vals = [f[feat] for f in all_features if feat in f]
        snap_avg = sum(vals) / len(vals) if vals else 0
        bench = VIRALITY_BENCHMARKS.get(feat, {}).get("day", {})
        top_mean = bench.get("mean_top", "-")
        ctrl_mean = bench.get("mean_ctrl", "-")
        smd = bench.get("smd", 0)

        if isinstance(top_mean, (int, float)) and snap_avg >= top_mean * 0.8:
            status = "ON TARGET"
        elif isinstance(top_mean, (int, float)) and snap_avg >= ctrl_mean:
            status = "above avg"
        else:
            status = "below target"

        top_str = f"{top_mean:.1f}" if isinstance(top_mean, (int, float)) else str(top_mean)
        ctrl_str = f"{ctrl_mean:.1f}" if isinstance(ctrl_mean, (int, float)) else str(ctrl_mean)

        lines.append(f"| {feat} | {snap_avg:.1f} | {top_str} | {ctrl_str} | {smd:.3f} ({smd_interpretation(smd)}) | {status} |")

    lines.append(f"")
    lines.append(f"### Binary Features (snapshot prevalence vs benchmarks)")
    lines.append(f"")
    lines.append(f"| Feature | Snapshot Rate | Day Top-100 Rate | Day Lift | Status |")
    lines.append(f"|---|---|---|---|---|")

    for feat in binary_features:
        vals = [1 if f[feat] else 0 for f in all_features if feat in f]
        snap_rate = sum(vals) / len(vals) if vals else 0
        bench = VIRALITY_BENCHMARKS.get(feat, {}).get("day", {})
        top_rate = bench.get("top_rate")
        lift = bench.get("lift")

        if top_rate is not None and snap_rate >= top_rate * 0.8:
            status = "ON TARGET"
        elif top_rate is not None and snap_rate >= (bench.get("ctrl_rate") or 0):
            status = "above avg"
        else:
            status = "below target"

        top_str = f"{top_rate:.0%}" if top_rate is not None else "-"
        lift_str = f"{lift:.2f}x" if lift is not None else "-"

        lines.append(f"| {feat} | {snap_rate:.0%} | {top_str} | {lift_str} | {status} |")

    lines.append(f"")

    # ---- Strategy brief ----
    lines.append(f"## Strategy Brief")
    lines.append(f"")

    # Who's dominating
    if author_board:
        top_author = author_board[0][0]
        lines.append(f"**Dominant author right now:** {top_author} ({author_board[0][1]['count']} posts, {author_board[0][1]['total_score']} total score)")
        lines.append(f"")

    # Score stats
    all_scores = [m["score"] for m in unique_metrics]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    median_score = sorted(all_scores)[len(all_scores)//2] if all_scores else 0
    lines.append(f"**Score stats:** avg={avg_score:.1f}, median={median_score}, max={max(all_scores) if all_scores else 0}")
    lines.append(f"")

    # Rising content
    if rising:
        lines.append(f"**Rising content ({len(rising)} posts < 4h old):** Top riser is \"{rising[0]['title'][:60]}\" by {rising[0]['author']} at {rising[0]['score_per_hour']:.1f} score/hr")
    else:
        lines.append(f"**Rising content:** No posts under 4 hours old in this snapshot.")
    lines.append(f"")

    # Posting checklist based on current data
    lines.append(f"### Posting Checklist")
    lines.append(f"")
    lines.append(f"- [ ] Title: 10-16 words, complete sentence with period")
    lines.append(f"- [ ] Title: uses first person or frames a problem/measurement")
    lines.append(f"- [ ] Body: 250-550 words, 15-25 short paragraphs")
    lines.append(f"- [ ] Body: 1-3 headings, 3-5 list items")
    lines.append(f"- [ ] Uses first person ('I') and addresses reader ('you')")
    lines.append(f"- [ ] Contains revelation language ('found', 'discovered')")
    lines.append(f"- [ ] Contains authority language ('data shows', 'measured')")
    lines.append(f"- [ ] Contains community language ('we', 'us')")
    lines.append(f"- [ ] Ends with a direct question")
    lines.append(f"- [ ] No external links")
    lines.append(f"")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_trends.py <path> [<path> ...]", file=sys.stderr)
        print("  Paths can be .json files or directories containing .json files.", file=sys.stderr)
        sys.exit(1)

    paths = sys.argv[1:]
    snapshots = load_snapshots(paths)

    if not snapshots:
        print("ERROR: No valid snapshots found in the given paths.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(snapshots)} snapshot(s).", file=sys.stderr)

    report = generate_report(snapshots)

    # Print to stdout
    print(report)

    # Save to reports directory
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    reports_dir = skill_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    report_file = reports_dir / f"{timestamp}_analysis.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved to: {report_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
