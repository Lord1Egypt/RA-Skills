#!/usr/bin/env python3
"""
slop_scan.py -- quantitative "AI slop" density scanner for prose drafts.

This is a diagnostic tool, not a judge. It counts occurrences of known
over-represented vocabulary and structural patterns and reports density
(hits per 1,000 words) so a human or model doing a self-edit pass can see
where a draft is clustering, rather than treating a single instance of a
common word as a problem.

Usage:
    python3 slop_scan.py path/to/draft.md
    python3 slop_scan.py path/to/draft.md --json   # machine-readable output
    cat draft.md | python3 slop_scan.py -          # read from stdin

No third-party dependencies -- standard library only.
"""

import argparse
import json
import re
import sys
from collections import Counter

TIER1 = [
    "delve", "delving", "tapestry", "underscore", "underscores", "underscoring",
    "testament to", "boundaries", "realm", "multifaceted", "multifarious",
    "kaleidoscope", "myriad of", "plethora", "cornerstone", "bedrock",
    "linchpin", "panacea", "holistic", "synergy", "paradigm shift",
    "game-changer", "game changer", "unleash", "navigate the complexities",
    "embark on a journey", "foster growth", "cultivate", "harness the power",
    "fabric of", "woven", "intricacies", "in the realm of",
]

TIER2 = [
    "robust", "seamless", "seamlessly", "vibrant", "dynamic", "comprehensive",
    "streamline", "streamlined", "leverage", "leveraging", "utilize",
    "utilizing", "facilitate", "optimal", "optimize", "pivotal", "crucial",
    "essential", "vital", "invaluable", "indispensable", "transformative",
    "revolutionize", "revolutionary", "groundbreaking", "cutting-edge",
    "state-of-the-art", "innovative", "empower", "empowering", "meticulous",
    "meticulously", "profound", "profoundly", "staggering", "unprecedented",
    "ever-evolving", "ever-changing", "thought-provoking", "awe-inspiring",
    "captivating", "bespoke", "curated",
]

TIER3 = [
    "additionally", "moreover", "furthermore", "notably", "importantly",
    "ultimately", "fundamentally", "essentially", "significantly", "various",
    "numerous", "arguably", "undoubtedly",
]

PHRASES = [
    r"\bit'?s not just\b.{0,60}\bit'?s\b",
    r"\bnot only\b.{0,60}\bbut\b",
    r"\bmore than just\b",
    r"\bin today'?s fast-paced world\b",
    r"\bin the ever-evolving landscape\b",
    r"\bimagine a world where\b",
    r"\bit is important to note that\b",
    r"\bit is worth mentioning that\b",
    r"\bit should be noted that\b",
    r"\bone must consider\b",
    r"\bultimately,? the choice is yours\b",
    r"\bonly time will tell\b",
    r"\bas we move forward\b",
    r"\bthe possibilities are endless\b",
    r"\bgreat question\b",
    r"\byou raise a? ?(really)? ?(great|interesting|valid) point\b",
    r"\bat the end of the day\b",
    r"\bthat being said\b",
    r"\bwhether you'?re .{0,40} or .{0,40},\b",
]

INFLATED_VERBS = [
    r"\bserves as\b", r"\bstands as\b", r"\brepresents\b", r"\bboasts\b",
]


def load_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_terms(text_lower, terms):
    hits = Counter()
    for term in terms:
        pattern = r"\b" + re.escape(term) + r"\b"
        n = len(re.findall(pattern, text_lower))
        if n:
            hits[term] = n
    return hits


def count_phrases(text_lower, patterns):
    hits = Counter()
    for pat in patterns:
        n = len(re.findall(pat, text_lower))
        if n:
            hits[pat] = n
    return hits


def find_lines_with(lines, terms):
    """Return {term: [line_numbers]} for tier-1 terms, to help locate them fast."""
    located = {}
    for term in terms:
        pattern = r"\b" + re.escape(term) + r"\b"
        nums = [i + 1 for i, line in enumerate(lines) if re.search(pattern, line.lower())]
        if nums:
            located[term] = nums
    return located


def formatting_stats(text, lines):
    word_count = max(len(re.findall(r"\b\w+\b", text)), 1)
    bullet_lines = sum(1 for l in lines if re.match(r"^\s*[-*+]\s+", l))
    header_lines = sum(1 for l in lines if re.match(r"^\s{0,3}#{1,6}\s+", l))
    bold_count = len(re.findall(r"\*\*[^*]+\*\*", text))
    em_dash_count = text.count("—") + text.count(" -- ")
    non_blank_lines = sum(1 for l in lines if l.strip())
    return {
        "word_count": word_count,
        "bullet_lines": bullet_lines,
        "header_lines": header_lines,
        "bold_spans": bold_count,
        "em_dashes": em_dash_count,
        "bullet_ratio_pct": round(100 * bullet_lines / max(non_blank_lines, 1), 1),
    }


def density_per_1000(count, word_count):
    return round(1000 * count / max(word_count, 1), 2)


def build_report(text, path_label):
    lines = text.splitlines()
    text_lower = text.lower()
    fmt = formatting_stats(text, lines)
    wc = fmt["word_count"]

    t1 = count_terms(text_lower, TIER1)
    t2 = count_terms(text_lower, TIER2)
    t3 = count_terms(text_lower, TIER3)
    phrases = count_phrases(text_lower, PHRASES)
    inflated = count_phrases(text_lower, INFLATED_VERBS)

    t1_total = sum(t1.values())
    t2_total = sum(t2.values())
    t3_total = sum(t3.values())
    phrase_total = sum(phrases.values())

    t1_located = find_lines_with(lines, list(t1.keys()))

    report = {
        "file": path_label,
        "word_count": wc,
        "tier1": {"total": t1_total, "density_per_1000_words": density_per_1000(t1_total, wc), "hits": dict(t1), "lines": t1_located},
        "tier2": {"total": t2_total, "density_per_1000_words": density_per_1000(t2_total, wc), "hits": dict(t2)},
        "tier3": {"total": t3_total, "density_per_1000_words": density_per_1000(t3_total, wc), "hits": dict(t3)},
        "structural_phrases": {"total": phrase_total, "hits": dict(phrases)},
        "inflated_verbs": {"total": sum(inflated.values()), "hits": dict(inflated)},
        "formatting": fmt,
    }
    return report


def severity_note(report):
    notes = []
    if report["tier1"]["density_per_1000_words"] >= 3:
        notes.append("Tier-1 vocabulary density is high -- likely to read as AI-generated. Rewrite the flagged sentences rather than swapping synonyms.")
    elif report["tier1"]["total"] > 0:
        notes.append("A few tier-1 words present -- check whether they cluster in the same paragraph; isolated use is usually fine.")

    if report["structural_phrases"]["total"] >= 2:
        notes.append("Multiple structural tells found (e.g. 'not just X, it's Y', hedge phrases) -- these matter more than vocabulary; fix the sentence structure directly.")

    fmt = report["formatting"]
    if fmt["bullet_ratio_pct"] >= 40 and fmt["word_count"] < 400:
        notes.append("High bullet ratio on a short document -- consider whether this content would read better as prose.")
    if fmt["bold_spans"] >= 8 and fmt["word_count"] < 600:
        notes.append("Heavy bold usage relative to length -- check whether bold is marking things worth finding fast, or just decorating.")
    if fmt["em_dashes"] >= 4 and fmt["word_count"] < 500:
        notes.append("Several em dashes in a short passage -- may read as a rhythmic tic; consider converting some to periods or commas.")

    if not notes:
        notes.append("No strong density signals. This is a diagnostic pass, not a guarantee -- read it once yourself too.")
    return notes


def print_human_report(report):
    print(f"=== Slop scan: {report['file']} ===")
    print(f"Word count: {report['word_count']}\n")

    print(f"Tier 1 (kill on sight): {report['tier1']['total']} hits "
          f"({report['tier1']['density_per_1000_words']}/1000 words)")
    for term, n in sorted(report["tier1"]["hits"].items(), key=lambda x: -x[1]):
        loc = report["tier1"]["lines"].get(term, [])
        loc_str = f" (lines: {', '.join(map(str, loc[:8]))}{'...' if len(loc) > 8 else ''})" if loc else ""
        print(f"  - '{term}': {n}{loc_str}")

    print(f"\nTier 2 (suspicious in clusters): {report['tier2']['total']} hits "
          f"({report['tier2']['density_per_1000_words']}/1000 words)")
    for term, n in sorted(report["tier2"]["hits"].items(), key=lambda x: -x[1])[:15]:
        print(f"  - '{term}': {n}")

    print(f"\nTier 3 (light signal): {report['tier3']['total']} hits "
          f"({report['tier3']['density_per_1000_words']}/1000 words)")

    print(f"\nStructural phrase tells: {report['structural_phrases']['total']} hits")
    for pat, n in report["structural_phrases"]["hits"].items():
        print(f"  - matched pattern /{pat}/: {n}")

    print(f"\nInflated verbs (serves as / stands as / represents / boasts): "
          f"{report['inflated_verbs']['total']} hits")

    fmt = report["formatting"]
    print("\nFormatting:")
    print(f"  - bullet lines: {fmt['bullet_lines']} ({fmt['bullet_ratio_pct']}% of non-blank lines)")
    print(f"  - header lines: {fmt['header_lines']}")
    print(f"  - bold spans: {fmt['bold_spans']}")
    print(f"  - em dashes: {fmt['em_dashes']}")

    print("\nNotes:")
    for note in severity_note(report):
        print(f"  * {note}")


def main():
    parser = argparse.ArgumentParser(description="Scan a text file for AI-slop density signals.")
    parser.add_argument("path", help="Path to the file to scan, or '-' for stdin.")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON instead of a human report.")
    args = parser.parse_args()

    text = load_text(args.path)
    report = build_report(text, args.path)

    if args.json:
        report["notes"] = severity_note(report)
        print(json.dumps(report, indent=2))
    else:
        print_human_report(report)


if __name__ == "__main__":
    main()
