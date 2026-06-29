#!/usr/bin/env python3
"""
english-polish Phase 0 Detector
================================
Automated nativization score detection for non-native English text.

Scoring: 0-5 scale (0=heavily Chinese-patterned, 5=native-level)
Usage:
    python3 detector.py check <file.md>         # Score a single file
    python3 detector.py check <dir/>            # Score all .md files in dir
    python3 detector.py batch <dir/>            # Score + generate report
    python3 detector.py interactive             # Paste text interactively

Pattern Library (18 categories):
    A. Subject Dangling        — "For chip design, competition is fierce..."
    B. Redundant "As For"      — "As for the energy cost, it is..."
    C. Passive Chain Stacking  — "It can be seen that..."
    D. "Make + abstract noun"   — "make a decision" → "decide"
    E. "Not only...but also"    — overused default connector
    F. Noun Stacking (4+consec) — "Data center GPU market growth prediction..."
    G. "Should" false obligation — "China should develop..." when describing fact
    H. "The" overuse for generic — "the computing power is..."
    I. Chinese filler expressions — "to a certain extent", "in the process of"
    J. "This is because..."      — Chinese-pattern explanatory structure
    K. Redundant modifiers      — "actively strengthen", "continuously improve"
    L. Weak verb+nominalization — "conduct research" → "research"
    M. Emphasis inversion       — "It is X that..." (Chinese '是...的' direct translation)
    N. List cadence             — 'First...Second...Finally' enumeration
    O. Concessive cluster       — 'Although...but...' double conjunction
    P. Topic-comment fronting   — 'As for X,' structure
    Q. False inclusive 'We'     — 'We can see/observe/conclude'
    R. Logical sawtooth         — 'On one hand...on the other hand...'
    S. List summarizer          — 'All these factors contribute...'
"""

import re
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ── Pattern Definitions ──────────────────────────────────────────────

PATTERNS: Dict[str, Dict] = {
    "A_subject_dangling": {
        "label": "Subject Dangling",
        "weight": 1.0,
        "patterns": [
            r"\bAs for\s+\w+,\s+(?:it|they|he|she)\b",
            r"\bRegarding\s+\w+,\s+(?:it|they|he|she)\b",
            r"\bFor\s+\w+,\s+(?:this|it|they|competition|demand|supply|pressure|the)\b",
        ],
        "examples": [
            '"For chip design, competition is fierce among all players."',
            '"Regarding the market, it is growing rapidly."',
        ],
    },
    "B_as_for_redundant": {
        "label": "Redundant 'As For' / 'Regarding'",
        "weight": 0.8,
        "patterns": [
            r"\bAs for the\b",
            r"\bAs to the\b",
            r"\bWhen it comes to\b",
        ],
        "examples": [
            '"As for the energy cost, it is becoming the main constraint."',
        ],
    },
    "C_passive_chain": {
        "label": "Passive Chain Stacking",
        "weight": 1.0,
        "patterns": [
            r"\bIt can be seen that\b",
            r"\bIt should be noted that\b",
            r"\bIt is being\w+ by\b",
            r"\bare being\w+ (?:by|in)\b",
            r"\bis being\w+ (?:by|in)\b",
        ],
        "examples": [
            '"It can be seen that the market is being reshaped by export controls."',
        ],
    },
    "D_make_abstract_noun": {
        "label": "'Make + abstract noun'",
        "weight": 0.8,
        "patterns": [
            r"\bmake\s+(?:a|the|an)\s+\w+ (?:harder|easier|more|less)",
            r"\bmake\s+(?:a|the|an)\s+(?:decision|contribution|comparison|distinction|commitment|improvement|reduction)\b",
            r"\bgive\s+(?:a|the|an)\s+(?:explanation|presentation|description)\b",
            r"\bhave\s+(?:a|the|an)\s+(?:discussion|conversation|meeting|impact|effect)\b",
        ],
        "examples": [
            '"This makes the competition harder to win." → "This hardens the competition."',
            '"have a discussion" → "discuss"',
        ],
    },
    "E_not_only_but_also": {
        "label": "'Not only...but also' overuse",
        "weight": 0.6,
        "patterns": [
            r"\bNot only\b.*\bbut also\b",
            r"\bnot only\b.*\bbut also\b",
        ],
        "examples": [
            '"Not only did NVIDIA dominate hardware, but it also built a software ecosystem."',
        ],
    },
    "F_noun_stacking": {
        "label": "Noun Stacking (5+ consec noun/mod)",
        "weight": 0.7,
        "patterns": [
            r"\b(?:[a-zA-Z]+\s+){4,}(?:growth|decline|rate|model|analysis|prediction|strategy|demand|supply|shift|trend|forecast|bottleneck|constraint|improvement|reduction|expansion|investment|spending|capability)\b",
        ],
        "examples": [
            '"Data center GPU market growth prediction" → 5+ word stack, break into clauses',
        ],
        "notes": "4+ consecutive words + 1 head noun from tech/abstract set. Requires at least 5 total words.",
    },
    
    "G_should_false": {
        "label": "'Should' false obligation",
        "weight": 0.7,
        "patterns": [
            r"\bChina should\b",
            r"\bthe government should\b",
            r"\bcompanies should\b",
            r"\bthe industry should\b",
        ],
        "examples": [
            '"China should develop its own chip industry" (if describing fact → "is developing")',
        ],
    },
    "H_the_overuse": {
        "label": "'The' overuse for generic",
        "weight": 0.5,
        "patterns": [
            r"\bThe (computing power|chip design|software ecosystem|hardware industry|market demand|supply chain|economic growth|national security)\b",
        ],
        "examples": [
            '"The computing power is the most important resource." → "Computing power is..."',
        ],
    },
    "I_chinese_filler": {
        "label": "Chinese filler expressions",
        "weight": 0.7,
        "patterns": [
            r"\bto a certain extent\b",
            r"\bin the process of\b",
            r"\bto some degree\b",
            r"\bin a sense\b",
            r"\bfrom a certain perspective\b",
            r"\bas we all know\b",
            r"\bit is worth noting that\b",
            r"\bas is well known\b",
        ],
        "examples": [
            '"to a certain extent", "in the process of", "as we all know"',
        ],
    },
    "J_this_is_because": {
        "label": "'This is because' structure",
        "weight": 0.6,
        "patterns": [
            r"\bThis is because\b",
            r"\bThis is why\b",
            r"\bThe reason is that\b",
            r"\bThat is why\b",
        ],
        "examples": [
            '"This is because Chinese-pattern explanatory structure."',
        ],
    },
    "K_redundant_modifier": {
        "label": "Redundant modifier",
        "weight": 0.6,
        "patterns": [
            r"\bactively (?:strengthen|promote|develop|pursue|encourage)\b",
            r"\bcontinuously (?:improve|upgrade|optimize|enhance)\b",
            r"\bvigorously (?:develop|promote|pursue)\b",
            r"\bconstantly (?:improve|upgrade|optimize)\b",
            r"\beffectively (?:solve|address|resolve|handle)\b",
        ],
        "examples": [
            '"actively strengthen" → "strengthen"',
            '"continuously improve" → "improve"',
        ],
    },
    "L_weak_verb_nominalization": {
        "label": "Weak verb + nominalization",
        "weight": 0.7,
        "patterns": [
            r"\bconduct(?:s|ed|ing)?\s+(?:research|analysis|studies|investigation|experiment)s?\b",
            r"\bperform(?:s|ed|ing)?\s+(?:analysis|evaluation|assessment|calculation)s?\b",
            r"\bprovide(?:s|d)?\s+(?:analysis|assessment|evaluation|insight)s?\b",
            r"\bundertake(?:s|n|ing)?\s+(?:research|analysis|study|project)s?\b",
        ],
        "examples": [
            '"conduct research" → "research"',
            '"perform analysis" → "analyze"',
        ],
    },

    ## ── New: Chinese-logic patterns (added 2026-06-19) ──────────────

    "M_chinese_emphasis_inversion": {
        "label": "Chinese emphasis inversion ('It is X that...')",
        "weight": 0.7,
        "patterns": [
            r"\bIt is\s+(?:[\w]+\s+)+?that\s+(?:this|these|the|we|they|it|there|what|which|[a-z]+)\b",
            r"\bIt was\s+(?:[\w]+\s+)+?that\s+(?:this|these|the|we|they|it|there|what|which|[a-z]+)\b",
        ],
        "examples": [
            '"It is this gap that explains..." → "This gap explains..."',
            '"It was the policy shift that triggered..." → "The policy shift triggered..."',
        ],
        "notes": "Chinese '是...的' construction directly translated.",
    },

    "N_chinese_list_cadence": {
        "label": "Chinese list cadence ('First...Second...Finally')",
        "weight": 0.5,
        "patterns": [
            r"\bFirst(?:ly)?,",
        ],
        "examples": [
            '"First, the market is growing. Second, competition is intensifying." → convert to narrative flow',
        ],
        "notes": "Detects any enumeration marker. In isolation (without Second/Third following), it is low-confidence but flagged.",
    },

    "O_chinese_concessive_cluster": {
        "label": "Concessive cluster ('Although...but...')",
        "weight": 0.8,
        "patterns": [
            r"\bAlthough\b[^.]*?\b,\s*\bbut\b",
            r"\bThough\b[^.]*?\b,\s*\bbut\b",
            r"\bEven though\b[^.]*?\b,\s*\bbut\b",
        ],
        "examples": [
            '"Although the market is large, but competition is fierce." → "Although the market is large, competition is fierce."',
        ],
        "notes": "Chinese double-concessive '虽然...但是...' structure.",
    },

    "P_chinese_topic_comment": {
        "label": "Topic-comment fronting ('As for X,')",
        "weight": 0.7,
        "patterns": [
            r"\bAs for\s+\w+(?:,|\s+,\s+)",
            r"\bSpeaking of\s+\w+(?:,|\s+,\s+)",
            r"\bWhen it comes to\s+\w+(?:,|\s+,\s+)",
            r"\b(?:In|With) regard to\s+\w+(?:,|\s+,\s+)",
        ],
        "examples": [
            '"As for NVIDIA, it dominates the market." → "NVIDIA dominates the market."',
        ],
        "notes": "Chinese topic-comment (话题-说明) structure.",
    },

    "Q_chinese_we_false_inclusive": {
        "label": "False inclusive 'We' (Chinese '我们')",
        "weight": 0.5,
        "patterns": [
            r"\bWe can (?:see|find|observe|notice|understand|conclude)",
            r"\bWe should (?:note|notice|remember|consider|think about)",
        ],
        "examples": [
            '"We can see that the market is changing." → "The market is changing."',
        ],
        "notes": "Redundant authorial 'we' that pushes the reader away from evidence.",
    },

    "R_chinese_logical_sawtooth": {
        "label": "Logical sawtooth ('On one hand...on the other')",
        "weight": 0.5,
        "patterns": [
            r"\bOn the one hand\b.*?\bon the other hand\b",
            r"\bOn one hand\b.*?\bon the other hand\b",
        ],
        "examples": [
            '"On one hand, the market is growing. On the other hand, competition is intense."',
        ],
        "notes": "Overused contrast structure. Simple 'but' works better.",
    },

    "S_chinese_list_summarizer": {
        "label": "List summarizer ('These/Those/All X are...' followed by generic)",
        "weight": 0.5,
        "patterns": [
            r"\b(?:These|Those|All|Both)\s+(?:factors|reasons|aspects|elements|issues|challenges|opportunities|problems|features|characteristics)\s+(?:make|cause|lead|contribute|explain|create|drive)\b",
        ],
        "examples": [
            '"All these factors contribute to the growth." → "These factors drive growth."',
        ],
        "notes": "Chinese '综上所述/所有这些因素' padding structure.",
    },
}


# ── Config Loading ──────────────────────────────────────────────

_CONFIG_PATH = Path(__file__).parent.parent / "config" / "default.json"
_USER_CONFIG_PATH = Path(__file__).parent.parent / "config" / "user.json"


def load_config() -> Dict:
    """Load config from default.json, merge user.json overrides if present."""
    config = {}
    if _CONFIG_PATH.exists():
        config = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    else:
        config = {
            "detector": {},
            "user_custom_patterns": [],
        }

    # Merge user config
    if _USER_CONFIG_PATH.exists():
        user_config = json.loads(_USER_CONFIG_PATH.read_text(encoding="utf-8"))
        patterns = user_config.get("user_custom_patterns", [])
        if patterns:
            config.setdefault("user_custom_patterns", []).extend(patterns)
        # Merge other user overrides
        for top_key in user_config:
            if isinstance(user_config[top_key], dict) and isinstance(config.get(top_key), dict):
                config[top_key].update(user_config[top_key])
            elif top_key != "user_custom_patterns":
                config[top_key] = user_config[top_key]

    return config


def extend_patterns_with_user_config(patterns: Dict, config: Dict) -> Dict:
    """Merge user-defined patterns from config into the in-memory PATTERNS dict."""
    custom = config.get("user_custom_patterns", [])
    if not custom:
        return patterns

    extended = dict(patterns)
    for entry in custom:
        key = entry.get("key")
        if not key or key in extended:
            continue  # skip duplicates
        extended[key] = {
            "label": entry.get("label", key),
            "weight": entry.get("weight", 1.0),
            "patterns": entry.get("patterns", []),
            "examples": entry.get("examples", ["(user-defined)"]),
            "notes": entry.get("notes", ""),
        }
    return extended


# Apply user config to PATTERNS at import time
_CONFIG_CACHE = load_config()
PATTERNS = extend_patterns_with_user_config(PATTERNS, _CONFIG_CACHE)


def analyze_text(text: str) -> Dict:
    """Run all patterns on text, return frequency and examples per category."""
    results = {}
    total_issues = 0
    all_matches = []

    for key, config in PATTERNS.items():
        matches = []
        for p in config["patterns"]:
            found = re.findall(p, text, re.IGNORECASE | re.DOTALL)
            matches.extend(found)

        if matches:
            count = len(matches)
            total_issues += count * config["weight"]
            results[key] = {
                "label": config["label"],
                "count": count,
                "weighted": round(count * config["weight"], 1),
                "examples": matches[:3],
                "pattern_examples": config["examples"],
            }
            all_matches.extend(matches)

    # Calculate score (0-5 scale)
    # Rule: >8 weighted issues in 200 words → score < 3
    word_count = len(text.split())
    density = (total_issues / max(word_count, 200)) * 200  # normalize to per 200 words

    if density >= 8:
        raw_score = 5 - min(density / 4, 5)
    elif density >= 4:
        raw_score = 5 - (density - 4) * 0.5
    else:
        raw_score = 5 - density * 0.3

    score = max(0, min(5, round(raw_score, 1)))

    return {
        "word_count": word_count,
        "total_weighted_issues": round(total_issues, 1),
        "density_per_200_words": round(density, 1),
        "nativization_score": score,
        "categories_detected": results,
        "all_matches": all_matches[:20],  # cap to avoid huge output
        "severity": "Native-level" if score >= 4.5 else (
            "Near-native" if score >= 4 else (
                "Light polish needed" if score >= 3 else (
                    "Full polish needed" if score >= 1.5 else "Heavy rewrite needed"
                )
            )
        ),
    }


def format_report(result: Dict, filename: str = "") -> str:
    """Generate a human-readable report from analysis results."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"PHASE 0 DETECTOR REPORT{f' — {filename}' if filename else ''}")
    lines.append("=" * 60)
    lines.append(f"  Word count:          {result['word_count']}")
    lines.append(f"  Total issues (wtd):  {result['total_weighted_issues']}")
    lines.append(f"  Density (/200 words): {result['density_per_200_words']}")
    lines.append(f"  Score:               {result['nativization_score']}/5.0")
    lines.append(f"  Severity:            {result['severity']}")
    lines.append("")

    if not result["categories_detected"]:
        lines.append("  ✅ No Chinese-English patterns detected. Text appears native-level.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"  Detected patterns ({len(result['categories_detected'])} categories):")
    lines.append("")
    for key, cat in sorted(
        result["categories_detected"].items(), key=lambda x: -x[1]["weighted"]
    ):
        lines.append(f"  [{cat['label']}] ×{cat['count']} (weighted: {cat['weighted']})")
        for ex in cat["examples"]:
            truncated = ex[:80] + "..." if len(ex) > 80 else ex
            lines.append(f"    → \"{truncated}\"")
        lines.append("")

    lines.append("-" * 60)
    lines.append("  Action needed:")
    score_val = result.get("nativization_score", 0)
    if score_val >= 4:
        lines.append("    ✅ Score 4+: Style-only tweaks (word-level).")
    elif score_val >= 3:
        lines.append("    🟡 Score 3-4: Selective polish (sentence-level).")
    elif score_val >= 1.5:
        lines.append("    🔴 Score 1.5-3: Full polish needed.")
    else:
        lines.append("    🚨 Score < 1.5: Heavy rewrite + nativization required.")
    lines.append("=" * 60)
    return "\n".join(lines)


def check_file(filepath: str) -> Dict:
    """Check a single file and print report."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return {}

    text = path.read_text(encoding="utf-8")

    # Strip markdown formatting for analysis (keep paragraph text)
    # Remove code blocks, tables, and images
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\|.*\|", "", text)  # rough table line removal
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    result = analyze_text(text)
    report = format_report(result, filename=path.name)
    print(report)

    return result


def check_directory(dirpath: str) -> List[Dict]:
    """Check all .md files in a directory."""
    path = Path(dirpath)
    if not path.is_dir():
        print(f"❌ Not a directory: {dirpath}")
        return []

    results = []
    md_files = sorted(path.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {dirpath}")
        return []

    for f in md_files:
        result = check_file(str(f))
        if result:
            results.append({"file": f.name, **result})
        print()  # spacing between files

    # Summary
    if len(results) > 1:
        print("=" * 60)
        print("BATCH SUMMARY")
        print("=" * 60)
        for r in results:
            print(f"  {r['file']:40s}  Score: {r['nativization_score']}/5  ({r['severity']})")
        avg = sum(r["nativization_score"] for r in results) / len(results)
        print(f"\n  Average score: {avg:.2f}/5")
        print("=" * 60)

    return results


def format_report_html(result: Dict, filename: str = "") -> str:
    """Generate HTML report with pattern highlighting."""
    score = result.get("nativization_score", 0)
    cats = result.get("categories_detected", {})
    severity = result.get("severity", "Unknown")

    sev_color = {
        "Native-level": "#16a34a",
        "Minor polish": "#ca8a04",
        "Full polish needed": "#dc2626",
        "Heavy rewrite required": "#7c3aed",
    }.get(severity, "#6b7280")

    rows = []
    for key, cat in sorted(cats.items(), key=lambda x: -x[1]["weighted"]):
        examples = "".join(
            f'<li><code>{ex[:80]}{"..." if len(ex) > 80 else ""}</code></li>'
            for ex in cat["examples"][:5]
        )
        rows.append(f"""
        <tr>
            <td><strong>{cat['label']}</strong></td>
            <td style="text-align:center">{cat['count']}</td>
            <td style="text-align:center">{cat['weighted']}</td>
            <td><ul style="margin:0;padding-left:1.2em">{examples}</ul></td>
        </tr>""")

    cat_section = ""
    if rows:
        cat_section = f"""
        <table style="width:100%;border-collapse:collapse;margin-top:12px">
            <thead>
                <tr style="background:#f3f4f6">
                    <th style="text-align:left;padding:6px 8px;border:1px solid #d1d5db">Pattern</th>
                    <th style="padding:6px 8px;border:1px solid #d1d5db">Count</th>
                    <th style="padding:6px 8px;border:1px solid #d1d5db">Weighted</th>
                    <th style="text-align:left;padding:6px 8px;border:1px solid #d1d5db">Examples</th>
                </tr>
            </thead>
            <tbody>{"".join(rows)}</tbody>
        </table>"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Detector Report{f' — {filename}' if filename else ''}</title></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:800px;margin:20px auto;padding:0 16px">
    <h2 style="margin-bottom:4px">Phase 0 Detector Report{f' — {filename}' if filename else ''}</h2>
    <div style="display:flex;gap:24px;margin:16px 0">
        <div><strong>Score:</strong> <span style="color:{sev_color};font-size:1.4em">{score}</span>/5</div>
        <div><strong>Words:</strong> {result['word_count']}</div>
        <div><strong>Issues:</strong> {result['total_weighted_issues']}</div>
        <div><strong>Density:</strong> {result['density_per_200_words']}/200w</div>
        <div><strong>Severity:</strong> <span style="color:{sev_color}">{severity}</span></div>
    </div>
    <div style="height:4px;background:#e5e7eb;border-radius:2px;margin:12px 0">
        <div style="height:4px;width:{score/5*100}%;background:{sev_color};border-radius:2px"></div>
    </div>
    {cat_section}
    <p style="color:#6b7280;margin-top:16px">Generated by english-polish detector.py v{Path(__file__).parent.parent.joinpath("VERSION")}</p>
</body>
</html>"""

    return html


def format_report_ansi(result: Dict, filename: str = "") -> str:
    """Generate terminal-friendly ANSI-colored report."""
    score = result.get("nativization_score", 0)
    severity = result.get("severity", "Unknown")
    cats = result.get("categories_detected", {})

    # Color codes
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    if score >= 4.5:
        color = GREEN
    elif score >= 3.5:
        color = YELLOW
    else:
        color = RED

    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"PHASE 0 DETECTOR REPORT{f' — {filename}' if filename else ''}")
    lines.append(f"{'='*60}")
    lines.append(f"  Score:               {color}{score}{RESET}/5.0 ({severity})")
    lines.append(f"  Word count:          {result['word_count']}")
    lines.append(f"  Issues (weighted):   {result['total_weighted_issues']}")
    lines.append(f"  Density:             {result['density_per_200_words']}/200 words")
    lines.append("")

    if not cats:
        lines.append(f"  {GREEN}✅ No patterns detected.{RESET}")
    else:
        lines.append(f"  Patterns ({len(cats)}):")
        for key, cat in sorted(cats.items(), key=lambda x: -x[1]["weighted"]):
            lines.append(f"    {BOLD}[{cat['label']}]{RESET} ×{cat['count']} (w:{cat['weighted']})")
            for ex in cat["examples"][:3]:
                t = ex[:70] + "..." if len(ex) > 70 else ex
                lines.append(f"      → \"{t}\"")

    return "\n".join(lines)


def interactive_mode():
    """Interactive text paste mode."""
    print("📝 Phase 0 Detector — Interactive Mode")
    print("Paste your text below. End with Ctrl+D (EOF) on a new line.")
    print("-" * 40)
    text = sys.stdin.read()
    if not text.strip():
        print("No text provided.")
        return

    result = analyze_text(text)
    report = format_report(result)
    print(report)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 detector.py check <file.md> [--format text|html|ansi]")
        print("  python3 detector.py check <dir/>    [--format text|html|ansi]")
        print("  python3 detector.py batch <dir/>    [--format text|html|ansi]")
        print("  python3 detector.py interactive           — Paste text interactively")
        print("  python3 detector.py list-patterns         — List all 19 pattern categories")
        print()
        print("Output formats:")
        print("  text (default): Plain text report")
        print("  html:           Beautiful HTML report with score bar")
        print("  ansi:           Terminal-colored report")
        sys.exit(1)

    # Consume --format <fmt> or --output <path> anywhere before command
    output_format = "text"
    output_path = None
    args = sys.argv[1:]
    clean_args = []
    i = 0
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        else:
            clean_args.append(args[i])
            i += 1

    command = clean_args[0] if clean_args else ""

    if command == "list-patterns":
        print(f"Phase 0 Detector — {len(PATTERNS)} Pattern Categories\n")
        for key, config in PATTERNS.items():
            print(f"  [{config['label']}] weight={config['weight']}")
            print(f"    Patterns: {len(config['patterns'])} regex rules")
            print(f"    Example: {config['examples'][0]}")
            print()
        sys.exit(0)

    if command == "interactive":
        interactive_mode()
        sys.exit(0)

    if command in ("check", "batch"):
        if len(clean_args) < 2:
            print("❌ Missing file/directory path")
            sys.exit(1)

        target = clean_args[1]

        def show(result, filename):
            if output_format == "html":
                return format_report_html(result, filename)
            elif output_format == "ansi":
                return format_report_ansi(result, filename)
            return format_report(result, filename)

        single_results = []

        if os.path.isfile(target):
            path = Path(target)
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            text = re.sub(r"\|.*\|", "", text)
            text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
            result = analyze_text(text)
            result["file"] = path.name
            single_results.append(result)
            report = show(result, filename=path.name)
            print(report)
            # Write HTML to file if detected
            if output_format == "html" and output_path:
                Path(output_path).write_text(report, encoding="utf-8")
        elif os.path.isdir(target):
            md_files = sorted(Path(target).glob("*.md"))
            if not md_files:
                print(f"No .md files found in {target}")
                return
            for f in md_files:
                text = f.read_text(encoding="utf-8")
                text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                text = re.sub(r"\|.*\|", "", text)
                text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
                result = analyze_text(text)
                result["file"] = f.name
                single_results.append(result)
                report = show(result, filename=f.name)
                print(report)
                print()
        else:
            print(f"❌ Not found: {target}")
            sys.exit(1)

        if command == "batch" and single_results:
            out_path = output_path or "detector-report.json"
            # HTML batch: write separate files
            if output_format == "html":
                for r in single_results:
                    fn = Path(r.get("file", "unknown")).stem + "-report.html"
                    html_out = Path(out_path).parent / fn if Path(out_path).is_absolute() else Path(fn)
                    html_out.write_text(format_report_html(r, r.get("file", "")), encoding="utf-8")
                print(f"\n📊 HTML reports written to: {Path().resolve()}/")
            else:
                with open(out_path, "w") as f:
                    json.dump(single_results, f, indent=2, ensure_ascii=False)
                print(f"\n📊 Batch report saved to: {out_path}")

        sys.exit(0)

    print(f"❌ Unknown command: {command}")
    sys.exit(1)


if __name__ == "__main__":
    main()
