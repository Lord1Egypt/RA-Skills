#!/usr/bin/env python3
"""Session Archiver — Extract structured knowledge from AI chat sessions."""
import json
import re
import sys
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

# ── Category extraction patterns ─────────────────────────────────────
CATEGORY_PATTERNS = {
    "decisions": re.compile(r'(decided?|chose|selected|opted|agreed?|concluded?|resolved?)', re.I),
    "todos": re.compile(r'(todo|to[\s-]do|action\s+item|follow[\s-]up|next\s+step|need\s+to|should\s+do)', re.I),
    "knowledge": re.compile(r'(learned?|found?|discovered?|noted?|key\s+(point|insight|takeaway))', re.I),
    "preferences": re.compile(r'(prefer|like|style|convention|naming|consistency)', re.I),
    "risks": re.compile(r'(risk|warning|caveat|caution|concern|security|vulnerability)', re.I),
}

PHASE_PATTERNS = {
    "problem": re.compile(r'(problem|issue|bug|need|want|goal|objective)', re.I),
    "exploration": re.compile(r'(explore|investigate|check|look\s+into|research|analyze)', re.I),
    "decision": re.compile(r'(decide|choose|select|go\s+with|use|implement)', re.I),
    "action": re.compile(r'(create|write|build|fix|add|update|deploy|push|merge|review)', re.I),
}


def parse_session(log_path: Path) -> Dict:
    """Parse a single session log into structured segments."""
    segments = {"problem": [], "exploration": [], "decision": [], "action": []}
    raw = log_path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    current_phase = "exploration"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect phase shifts
        for phase, pat in PHASE_PATTERNS.items():
            if pat.search(line):
                current_phase = phase
                break
        segments[current_phase].append(line)

    return {"source": log_path.name, "phases": segments, "raw_lines": len(lines)}


def extract_categories(lines: List[str]) -> Dict[str, List[str]]:
    """Extract 5 knowledge categories from conversation lines."""
    results = defaultdict(list)
    for line in lines:
        for category, pat in CATEGORY_PATTERNS.items():
            if pat.search(line):
                results[category].append(line[:200])
    return dict(results)


def build_topic_tags(parsed: Dict) -> List[str]:
    """Auto-generate topic tags from session content."""
    topics = set()
    lines_joined = " ".join(
        line for phase_lines in parsed["phases"].values()
        for line in phase_lines
    )
    # Common domain keywords
    domains = {
        "python", "javascript", "typescript", "rust", "go", "docker",
        "kubernetes", "aws", "api", "database", "react", "vue",
        "deployment", "testing", "security", "performance", "design",
        "architecture", "debug", "frontend", "backend", "devops",
    }
    for domain in domains:
        if domain in lines_joined.lower():
            topics.add(f"#{domain}")

    return sorted(topics)


def build_5sentence_summary(parsed: Dict) -> str:
    """Generate 5-sentence summary."""
    parts = []
    for phase in ["problem", "exploration", "decision", "action"]:
        lines = parsed["phases"].get(phase, [])
        if lines:
            parts.append(f"In the {phase} phase, {lines[0][:100]}.")
    if not parts:
        parts.append("No distinct phases detected.")
    while len(parts) < 5:
        parts.append("(additional context not available)")
    return " ".join(parts[:5])


def export_markdown(sessions: List[Dict]) -> str:
    """Export to Markdown format."""
    lines = ["# Session Archive\n"]
    for s in sessions:
        lines.append(f"## {s['summary']['source']}\n")
        lines.append(f"**Summary:** {s['summary']['short']}\n")
        lines.append(f"**Topics:** {', '.join(s['summary']['topics'])}\n")
        lines.append("### Categories\n")
        for cat, items in s["categories"].items():
            if items:
                lines.append(f"**{cat.title()}:**")
                for item in items[:5]:
                    lines.append(f"- {item}")
                lines.append("")
    return "\n".join(lines)


def export_json(sessions: List[Dict]) -> str:
    """Export to JSON."""
    return json.dumps(sessions, ensure_ascii=False, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Session Archiver — extract structured knowledge from chat sessions")
    parser.add_argument("--sessions", "-s", nargs="+", help="Session log files or directories", required=True)
    parser.add_argument("--dedup", "-d", action="store_true", help="De-duplicate across sessions")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "obsidian"], default="markdown")
    parser.add_argument("--outdir", "-o", help="Output directory")
    parser.add_argument("--graph", "-g", action="store_true", help="Generate cross-session graph")
    args = parser.parse_args()

    # Collect session files
    session_files = []
    for s in args.sessions:
        p = Path(s)
        if p.is_dir():
            session_files.extend(sorted(p.glob("*.log")) + sorted(p.glob("*.json")))
        else:
            session_files.append(p)

    if not session_files:
        # Self-test fallback
        test_log = Path("/tmp/test-session.log")
        test_log.write_text(
            "User: I need to fix the login bug.\n"
            "Assistant: Let's check the auth module.\n"
            "User: Let's use JWT tokens.\n"
            "Assistant: Good choice. I'll implement the fix.\n"
        )
        session_files = [test_log]

    # Parse
    parsed_sessions = [parse_session(f) for f in session_files]

    # Build output
    results = []
    for p in parsed_sessions:
        all_lines = [l for phase_lines in p["phases"].values() for l in phase_lines]
        categories = extract_categories(all_lines)
        topics = build_topic_tags(p)
        short_summary = build_5sentence_summary(p)
        results.append({
            "summary": {
                "source": p["source"],
                "lines": p["raw_lines"],
                "short": short_summary,
                "topics": topics,
            },
            "categories": categories,
            "phases": {k: v[:5] for k, v in p["phases"].items()},  # truncate for output
        })

    # Output
    if args.format == "json":
        output = export_json(results)
    else:
        output = export_markdown(results)

    if args.outdir:
        out_path = Path(args.outdir) / "session-archive.md"
        if args.format == "json":
            out_path = out_path.with_suffix(".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output)
        print(f"Written to {out_path}")
    else:
        print(output)

    if args.graph:
        # Simple cross-session graph (DOT-like output)
        print("\n--- Cross-Session Graph ---")
        for i, r in enumerate(results):
            others = [results[j]["summary"]["source"] for j in range(len(results)) if j != i]
            shared = set(r["summary"]["topics"])
            for j, o in enumerate(results):
                if j != i:
                    common = shared & set(o["summary"]["topics"])
                    if common:
                        print(f'  "{r["summary"]["source"]}" -> "{o["summary"]["source"]}" [label="{",".join(common)}"]')


if __name__ == "__main__":
    main()
