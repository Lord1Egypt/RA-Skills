#!/usr/bin/env python3
"""
english-polish Phase 1-3 Polisher
==================================
Automated nativization + diff output for non-native English text.

Usage:
    python3 polish.py check <file.md>          # Phase 0 detection only
    python3 polish.py polish <file.md>         # Full polish + diff
    python3 polish.py polish <file.md> -o <out> # Polish to custom output
    python3 polish.py polish <file.md> --style-only  # Phase 3 only
    python3 polish.py batch <dir/>             # Batch polish all .md files

Phases:
    1. Grammar & Mechanics — fix articles, tense, S-V agreement, punctuation
    2. Fluency & Flow      — break long sentences, remove fillers, fix Chinglish patterns
    3. Style & Idiom       — word choice elevation, rhythm, native-voice alignment

Output:
    - Polished <file>-polished.md (or custom path)
    - Diff summary in markdown format
    - Nativization score before/after
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import detector for scoring
sys.path.insert(0, str(Path(__file__).parent))
from detector import analyze_text, PATTERNS as DETECTOR_PATTERNS, load_config

# ── Config Loading ──────────────────────────────────────────────

_POLISH_CONFIG = load_config()
_USER_CUSTOM_REPLACEMENTS = _POLISH_CONFIG.get("user_custom_replacements", [])

# ── Chinese-English Filler/Word Mapping ──────────────────────────────

# "中文思维直译"高频词映射 — replace these with more natural alternatives
DIRECT_TRANSLATION_MAP = {
    "mainly through": "primarily via",
    "mainly rely on": "rely primarily on",
    "in the process of": "while",
    "in the process of building": "while building",
    "to a certain extent": "partially",
    "to some extent": "partially",
    "from a certain perspective": "",  # delete these filler phrases
    "from this perspective": "",
    "in this context": "",
    "in the long run": "over the long term",
    "in the long term": "over the long term",
    "as we all know": "",  # delete
    "it is worth noting that": "",  # delete
    "it should be noted that": "",  # delete
    "it can be seen that": "",  # delete
    "it is obvious that": "",  # delete
    "without doubt": "undoubtedly",
    "without any doubt": "undoubtedly",
    "there is no doubt that": "undoubtedly,",
    "due to the fact that": "because",
    "in spite of the fact that": "although",
    "on the grounds that": "because",
    "at this point in time": "now",
    "at the present time": "currently",
    "in the near future": "soon",
    "a large number of": "many",
    "the majority of": "most",
    "a small number of": "a few",
    "more and more": "increasingly",
    "more and more important": "increasingly important",
    "more and more complex": "increasingly complex",
    "more and more difficult": "increasingly difficult",
}

# Weak verb → strong verb replacements
WEAK_VERB_MAP = {
    r"\bmake a decision\b": "decide",
    r"\bmake a contribution\b": "contribute",
    r"\bmake a comparison\b": "compare",
    r"\bmake a distinction\b": "distinguish",
    r"\bmake an improvement\b": "improve",
    r"\bmake a reduction\b": "reduce",
    r"\bgive an explanation\b": "explain",
    r"\bgive a presentation\b": "present",
    r"\bgive a description\b": "describe",
    r"\bhave a discussion\b": "discuss",
    r"\bhave a conversation\b": "converse",
    r"\bhave an impact\b": "impact",
    r"\bhave an effect\b": "affect",
    r"\bconduct research\b": "research",
    r"\bconduct analysis\b": "analyze",
    r"\bconduct studies\b": "study",
    r"\bperform analysis\b": "analyze",
    r"\bperform an evaluation\b": "evaluate",
    r"\bprovide an analysis\b": "analyze",
    r"\bprovide insight\b": "illuminate",
}

# Redundant modifier pairs (first word deleted)
REDUNDANT_MODIFIERS = [
    (r"\bactively (strengthen|promote|develop|pursue|encourage)\b", r"\1"),
    (r"\bcontinuously (improve|upgrade|optimize|enhance)\b", r"\1"),
    (r"\bvigorously (develop|promote|pursue)\b", r"\1"),
    (r"\bconstantly (improve|upgrade|optimize|enhance)\b", r"\1"),
    (r"\beffectively (solve|address|resolve|handle)\b", r"\1"),
    (r"\bjointly (develop|promote|work)\b", r"\1"),
]


def apply_phase1(text: str) -> Tuple[str, List[str]]:
    """Phase 1: Grammar & Mechanics fixes."""
    changes = []
    original = text

    # Fix "Although...but..." pattern
    text, n = re.subn(
        r"\bAlthough\b([^.]*?)\b,\s*\bbut\b",
        lambda m: f"Although{m.group(1)},",
        text,
    )
    if n:
        changes.append(f"Fixed {n}x 'Although...but...' → 'Although...'")

    # Fix "Not only...but also" → "Not only...and"
    text, n = re.subn(r"\bNot only\b([^,]*?),?\s*\bbut also\b", r"Not only\1, and also", text)
    if n:
        changes.append(f"Refined {n}x 'Not only...but also'")

    # Fix "Therefore, we can see that..." → delete we can see
    text, n = re.subn(r"\btherefore,?\s*we can see that\b", "Therefore", text, flags=re.IGNORECASE)
    if n:
        changes.append(f"Removed {n}x 'we can see that' filler")

    # Fix "The reason is because" → "The reason is that"
    text, n = re.subn(r"\bThe reason is because\b", "The reason is that", text)
    if n:
        changes.append(f"Fixed {n}x 'reason is because'")

    # Fix "On one hand...on the other hand" → restructure with "But"
    text, n = re.subn(
        r"\bOn (?:the )?one hand\b[\s\S]*?\bon the other hand\b,",
        "But",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Simplified {n}x 'On one hand...on the other hand' → 'But'")

    # Fix "We can see/observe that" → delete
    text, n = re.subn(r"\bWe can (?:see|observe|notice|understand|conclude)\s+that\b", "", text, flags=re.IGNORECASE)
    if n:
        changes.append(f"Removed {n}x 'We can see/observe that'")

    # Fix "It is/was X that..." emphasis inversion → simplify
    text, n = re.subn(
        r"\bIt (?:is|was)\s+(?:[\w]+\s+)+?that\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Simplified {n}x 'It is/was...that' emphasis inversion")

    if len(changes) == 0:
        changes.append("No Phase 1 changes needed")

    return text, changes


def apply_phase2(text: str) -> Tuple[str, List[str]]:
    """Phase 2: Fluency & Flow — Chinglish pattern fixes."""
    changes = []
    original = text

    # Remove Chinese filler expressions (with sentence boundary protection)
    def protect_cap(t: str) -> str:
        t = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), t)
        t = re.sub(r',\s+,', ',', t)
        t = re.sub(r'\s{2,}', ' ', t)
        t = re.sub(r'^[a-z]', lambda m: m.group(0).upper(), t)
        return t

    for phrase, replacement in DIRECT_TRANSLATION_MAP.items():
        if not phrase:
            continue
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if replacement:
            text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
            if n:
                shortened = replacement[:40] if replacement else "(deleted)"
                changes.append(f"Replaced '{phrase}' → '{shortened}' ({n}x)")
                text = protect_cap(text)
        else:
            text, n = re.subn(pattern, "", text, flags=re.IGNORECASE)
            if n:
                changes.append(f"Removed '{phrase}' ({n}x)")
                text = protect_cap(text)
                text = re.sub(r'\s{2,}', ' ', text)
                text = re.sub(r'^,\s*', '', text)

    # Replace weak verb structures
    for pattern, replacement in WEAK_VERB_MAP.items():
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        if n:
            # Extract readable name from pattern
            name = pattern.replace(r"\b", "").replace("?", "")
            changes.append(f"Strengthened '{name}' → '{replacement}' ({n}x)")

    # Remove redundant modifiers
    for pattern, replacement in REDUNDANT_MODIFIERS:
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        if n:
            changes.append(f"Simplified redundant modifier ({n}x)")

    # ── New patterns P0-3: M-Q-R-S fixes ──

    # Fix "We can see/observe/conclude" (pattern Q)
    text, n = re.subn(
        r"\bWe can (?:see|find|observe|notice|understand|conclude)\s+that\b",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if n:
        changes.append(f"Removed {n}x 'We can (see|find|observe)...that' (false inclusive)")
        text = re.sub(r'^\s*,\s*', '', text)

    # Fix "On one hand...on the other hand" (pattern R) — already in Phase 1,
    # but also catch inline uses not handled by Phase 1
    text, n = re.subn(
        r"\bOn (?:the )?one hand[\s\S]*?\bon the other(?: hand)?",
        "But",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Simplified {n}x remaining 'On one hand...on the other'")

    # Simplify "All these factors contribute..." (pattern S)
    text, n = re.subn(
        r"\b(?:All |Both )?(?:These|Those)\s+(?:factors|reasons|aspects|issues|challenges|opportunities|problems)\s+(?:make|cause|lead|contribute|explain|create|drive)\s+(?:the|to|this)?\s?",
        "These ",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Simplified {n}x list-summarizer pattern")
        text = re.sub(r'\s{2,}', ' ', text)

    if len(changes) == 0:
        changes.append("No Phase 2 changes needed")

    return text, changes


def apply_phase3(text: str) -> Tuple[str, List[str]]:
    """Phase 3: Style & Idiom — word-level elevation.

    This phase operates on words and short phrases, not full syntax.
    It:
    - Replaces overused formal connectors (However/Moreover/Furthermore) with varied alternatives
    - Shifts weak "there is/are" constructions
    - Breaks up long sentences (>40 words)
    - Replaces "can be verbed" with active voice where clear
    - Removes unnecessary "that" after reporting verbs
    - Adds sentence rhythm variety (mixes simple/compound/complex)
    """
    changes = []
    original = text

    # ── 3a. Overused connector diversification ──
    # Replace every other "However," at sentence start
    sentences = re.split(r'(?<=[.!?])\s+', text)
    however_count = 0
    new_sentences = []
    for sent in sentences:
        m = re.match(r"\bHowever,", sent)
        if m:
            however_count += 1
            if however_count % 2 == 0:
                # Even instance: replace with varied connector
                replacements = ["That said,", "Still,", "Yet", "At the same time,"]
                sent = re.sub(r"\bHowever,", replacements[however_count % len(replacements)], sent, count=1)
        new_sentences.append(sent)
    text = " ".join(new_sentences)
    if however_count >= 2:
        changes.append(f"Diversified {however_count}x 'However,' at sentence start")

    # Replace consecutive "Moreover," / "Furthermore," / "Additionally,"
    for word in ["Moreover,", "Furthermore,", "Additionally,"]:
        text, n = re.subn(
            r"\b" + re.escape(word) + r"\s+" + re.escape(word),
            word,
            text,
        )
        if n:
            changes.append(f"Removed {n}x consecutive '{word}' duplication")

    # Replace "moreover" → "furthermore" (avoid repetition)
    moreover_count = len(re.findall(r"\bMoreover", text, re.IGNORECASE))
    if moreover_count >= 2:
        text, n = re.subn(r"\bMoreover\b", "Further", text, count=1, flags=re.IGNORECASE)
        changes.append("Varied 'Moreover' → 'Further' (repetition avoidance)")

    # ── 3b. Weak "There is/are" → direct subject ──
    text, n = re.subn(
        r"\bThere (?:is|are) (?:a|an|the|no|several|many)\b",
        "",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Simplified {n}x 'There is/are' → direct statement")

    # ── 3c. Active voice: "can be + past participle" → active ──
    text, n = re.subn(
        r"\bcan be (\w+ed)\b(?: by\b)?",
        lambda m: f"{m.group(1)}",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Converted {n}x passive 'can be Xed' → active")

    # ── 3d. Remove unnecessary "that" after reporting verbs ──
    text, n = re.subn(
        r"\b(suggest|argue|note|observe|conclude|claim|state|indicate|show|demonstrate)\s+that\b",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )
    if n:
        changes.append(f"Removed {n}x unnecessary 'that' after reporting verbs")

    # ── 3e. Long sentence breakup (>50 words) ──
    # Find long sentences and insert a break point
    def break_long_sentence(match):
        sent = match.group(0)
        words = sent.split()
        if len(words) <= 45:
            return sent
        # Find a good break point around the middle
        half = len(words) // 2
        # Look for "and", "which", "while", "with" near halfway
        for offset in range(min(10, half)):
            for break_word in ["and", "which", "while", "with", "but"]:
                if words[half + offset] == break_word or words[half - offset] == break_word:
                    idx = half + offset if words[half + offset] == break_word else half - offset
                    prefix = " ".join(words[:idx])
                    suffix = " ".join(words[idx:])
                    if break_word in ("and", "but"):
                        return f"{prefix}. {suffix.capitalize()}"
                    else:
                        return f"{prefix}, {suffix}"
        # No good break point: insert semicolon at halfway
        return " ".join(words[:half]) + "; " + " ".join(words[half:])

    text, n = re.subn(r"[A-Z][^.!?]*[.!?]", break_long_sentence, text)
    if n:
        # can't easily count actual breaks, only check if function changed anything
        pass

    # Count long sentences after processing
    long_count = sum(1 for s in re.split(r'(?<=[.!?])\s+', text) if len(s.split()) > 50)
    if long_count == 0:
        changes.append("Broken up long sentences (>50 words)")

    # ── 3f. Fix "You can" → more authoritative IMPERATIVE ──
    text, n = re.subn(r"\bYou can\b", "One can", text, flags=re.IGNORECASE)
    if n:
        changes.append(f"Replaced {n}x 'You can' → 'One can' (formal tone)")

    if len(changes) == 0:
        changes.append("Style pass: no automated changes needed")

    return text, changes


def generate_diff(original: str, polished: str, filename: str) -> str:
    """Generate unified diff string between original and polished text."""
    # Use system diff for structured output
    try:
        with open("/tmp/polish_orig.md", "w") as f:
            f.write(original)
        with open("/tmp/polish_new.md", "w") as f:
            f.write(polished)

        result = subprocess.run(
            ["diff", "-u", "/tmp/polish_orig.md", "/tmp/polish_new.md"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        diff_text = result.stdout
        if result.returncode == 0:
            return "# No changes detected.\n"

        # Clean up diff: remove temp file path noise, limit to 80 changed lines
        lines = diff_text.split('\n')
        # Keep header (---/+++), hunks (@@), and changes (-/+) 
        clean = []
        changed_lines = 0
        for line in lines:
            if line.startswith('--- ') or line.startswith('+++ '):
                # Shorten paths
                clean.append(line.replace('/tmp/polish_orig.md', filename).replace('/tmp/polish_new.md', filename))
            elif line.startswith('@@'):
                clean.append(line)
            elif line.startswith('-') or line.startswith('+'):
                changed_lines += 1
                if changed_lines <= 80:
                    clean.append(line)
            else:
                clean.append(line)

        if changed_lines > 80:
            clean.append(f'# ... ({changed_lines - 80} more changed lines truncated)')

        return '\n'.join(clean)

    except Exception:
        pass

    # Fallback: simple word-level diff summary
    orig_words = original.split()
    new_words = polished.split()
    diff_lines = ["# Word-level diff (no system diff available)"]
    if len(orig_words) != len(new_words):
        diff_lines.append(f"# Word count: {len(orig_words)} → {len(new_words)}")

    changed = []
    min_len = min(len(orig_words), len(new_words))
    for i in range(min_len):
        if orig_words[i] != new_words[i]:
            changed.append((orig_words[i], new_words[i]))

    if changed:
        diff_lines.append(f"# {len(changed)} word-level changes (showing first 20):")
        for old, new in changed[:20]:
            diff_lines.append(f"- {old} → {new}")
    else:
        diff_lines.append("# No word-level changes detected.")

    return "\n".join(diff_lines)


def polish_file(
    filepath: str,
    output_path: Optional[str] = None,
    style_only: bool = False,
) -> Dict:
    """Run full polish pipeline on a file."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return {}

    text = path.read_text(encoding="utf-8")
    original_text = text

    # Phase 0: score before
    before_result = analyze_text(text)

    # Apply phases
    p1_text, p1_changes = apply_phase1(text)
    p2_text, p2_changes = apply_phase2(p1_text)

    if style_only:
        polished_text, p3_changes = text, []
    else:
        polished_text, p3_changes = apply_phase3(p2_text)

    # Phase 0: score after
    after_result = analyze_text(polished_text)

    # Generate diff
    diff_content = generate_diff(original_text, polished_text, path.name)

    # Write output
    if output_path:
        out = Path(output_path)
    else:
        out = path.parent / f"{path.stem}-polished{path.suffix}"

    out.write_text(polished_text, encoding="utf-8")

    # Build report
    report_lines = []
    report_lines.append(f"# English Polish Report — {path.name}")
    report_lines.append("")
    report_lines.append(f"**File**: {path}")
    report_lines.append(f"**Output**: {out}")
    report_lines.append(f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append("")

    report_lines.append("## Polish Summary")
    report_lines.append(f"- Original word count: {before_result['word_count']}")
    report_lines.append(f"- Polished word count: {len(polished_text.split())}")
    report_lines.append(
        f"- Nativization score: {before_result['nativization_score']}/5 → {after_result['nativization_score']}/5"
    )
    report_lines.append(
        f"- Severity: {before_result['severity']} → {after_result['severity']}"
    )
    report_lines.append("")

    report_lines.append("## Phase 1: Grammar & Mechanics")
    for c in p1_changes:
        report_lines.append(f"- {c}")
    report_lines.append("")

    report_lines.append("## Phase 2: Fluency & Flow (Chinglish Patterns)")
    for c in p2_changes:
        report_lines.append(f"- {c}")
    report_lines.append("")

    report_lines.append("## Phase 3: Style & Idiom")
    for c in p3_changes:
        report_lines.append(f"- {c}")
    report_lines.append("")

    # Detected patterns (before)
    if before_result["categories_detected"]:
        report_lines.append("## Patterns Detected (before polish)")
        for key, cat in sorted(
            before_result["categories_detected"].items(), key=lambda x: -x[1]["weighted"]
        ):
            report_lines.append(
                f"- **{cat['label']}**: {cat['count']} instances"
            )
        report_lines.append("")

    # Diff section
    report_lines.append("## Diff (before → after)")
    report_lines.append(
        f"_Showing up to 80 changed lines. Full {_count_diff_lines(diff_content)} lines collapsed._"
    )
    report_lines.append("```diff")
    report_lines.append(diff_content)
    report_lines.append("```")
    report_lines.append("")

    report_lines.append(
        f"> _Polish completed. Review changes before accepting._"
    )

    report_text = "\n".join(report_lines)
    report_out = out.parent / f"{out.stem}-report.md"
    report_out.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\n📄 Polished file: {out}")
    print(f"📄 Report: {report_out}")

    return {
        "file": path.name,
        "output": str(out),
        "report": str(report_out),
        "before_score": before_result["nativization_score"],
        "after_score": after_result["nativization_score"],
        "before_severity": before_result["severity"],
        "after_severity": after_result["severity"],
        "changes": {
            "phase1": p1_changes,
            "phase2": p2_changes,
            "phase3": p3_changes,
        },
    }


def _count_diff_lines(diff_text: str) -> int:
    """Count how many lines changed in a diff output."""
    count = 0
    for line in diff_text.split('\n'):
        if line.startswith('+') or line.startswith('-'):
            if not line.startswith('+++') and not line.startswith('---'):
                count += 1
    return count


def batch_polish(dirpath: str):
    """Polish all .md files in a directory."""
    path = Path(dirpath)
    if not path.is_dir():
        print(f"❌ Not a directory: {dirpath}")
        return

    results = []
    md_files = sorted(path.glob("*.md"))
    if not md_files:
        print(f"No .md files in {dirpath}")
        return

    for f in md_files:
        print(f"\n{'='*60}")
        print(f"Processing: {f.name}")
        print(f"{'='*60}")
        result = polish_file(str(f))
        if result:
            results.append(result)

    if results:
        summary_path = path / "batch-polish-summary.json"
        with open(summary_path, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📊 Batch summary: {summary_path}")

        avg_before = sum(r["before_score"] for r in results) / len(results)
        avg_after = sum(r["after_score"] for r in results) / len(results)
        print(f"Average score: {avg_before:.2f} → {avg_after:.2f}")


def _polish_report_html(
    filename: str,
    before_score: float,
    after_score: float,
    before_severity: str,
    after_severity: str,
    p1_changes: List[str],
    p2_changes: List[str],
    p3_changes: List[str],
    diff_lines: int,
) -> str:
    """Generate HTML version of polish report."""
    color = lambda s: "#16a34a" if s >= 4.5 else ("#ca8a04" if s >= 3.5 else "#dc2626")
    sev_color_b = color(before_score)
    sev_color_a = color(after_score)

    def bullet_list(items):
        if not items:
            return "<p style=\"color:#6b7280\">No changes.</p>"
        return "<ul>" + "".join(f"<li>{c}</li>" for c in items) + "</ul>"

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Polish Report — {filename}</title>
<style>
  body {{ font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:800px;margin:20px auto;padding:0 16px }}
  h2 {{ margin-bottom:4px }}
  .score-bar {{ height:8px;background:#e5e7eb;border-radius:4px;margin:12px 0 }}
  .score-fill {{ height:8px;border-radius:4px }}
  .severity {{ font-size:1.1em }}
  .improved {{ color:#16a34a;font-weight:bold }}
  .diff-preview {{ background:#1e293b;color:#e2e8f0;padding:12px;border-radius:6px;font-family:monospace;font-size:13px;overflow-x:auto }}
</style>
</head>
<body>
    <h2>Polish Report — {filename}</h2>
    <div style="display:flex;gap:24px;margin:16px 0">
        <div><strong>Before:</strong> <span style="color:{sev_color_b}">{before_score}</span>/5 ({before_severity})</div>
        <div><strong>After:</strong> <span style="color:{sev_color_a}">{after_score}</span>/5 ({after_severity})</div>
    </div>
    <div class="score-bar">
        <div class="score-fill" style="width:{before_score/5*100}%;background:{sev_color_b};opacity:0.5"></div>
        <div class="score-fill" style="width:{after_score/5*100}%;background:{sev_color_a}"></div>
    </div>

    <h3>Phase 1: Grammar & Mechanics</h3>{bullet_list(p1_changes)}
    <h3>Phase 2: Fluency & Flow</h3>{bullet_list(p2_changes)}
    <h3>Phase 3: Style & Idiom</h3>{bullet_list(p3_changes)}

    <h3>Diff</h3>
    <p style="color:#6b7280">{diff_lines} lines changed.</p>
    <p>See {filename.replace('.md', '-report.md')} for full diff.</p>

    <p style="color:#6b7280;margin-top:24px">Generated by english-polish polish.py</p>
</body>
</html>"""
    return html


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 polish.py check <file.md>              # Phase 0 detection")
        print("  python3 polish.py polish <file.md> [--output <out>] [--format text|html]")
        print("  python3 polish.py polish <file.md> --style-only  # Style tweaks only")
        print("  python3 polish.py batch <dir/>                 # Batch polish all")
        print()
        print("Formats:")
        print("  text (default): Markdown report")
        print("  html:           HTML report with score bar")
        sys.exit(1)

    # Parse --format and --output before command
    output_format = "text"
    args = sys.argv[1:]
    clean_args = []
    i = 0
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        else:
            clean_args.append(args[i])
            i += 1

    command = clean_args[0] if clean_args else ""

    if command == "check":
        target = clean_args[1] if len(clean_args) > 1 else None
        if not target:
            print("❌ Missing file path")
            sys.exit(1)
        from detector import check_file
        from detector import format_report_html as det_html
        from detector import format_report_ansi as det_ansi
        if output_format == "html":
            # Reimplement check with HTML
            from detector import analyze_text
            path = Path(target)
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            text = re.sub(r"\|.*\|", "", text)
            result = analyze_text(text)
            print(det_html(result, path.name))
        elif output_format == "ansi":
            from detector import analyze_text
            path = Path(target)
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            text = re.sub(r"\|.*\|", "", text)
            result = analyze_text(text)
            print(det_ansi(result, path.name))
        else:
            from detector import check_file
            check_file(target)
        sys.exit(0)

    if command == "polish":
        if len(clean_args) < 2:
            print("❌ Missing file path")
            sys.exit(1)
        target = clean_args[1]
        output = None
        style_only = False

        args_iter = iter(clean_args[2:])
        for arg in args_iter:
            if arg == "-o" or arg == "--output":
                try:
                    output = next(args_iter)
                except StopIteration:
                    print("❌ Missing value for -o/--output")
                    sys.exit(1)
            elif arg == "--style-only":
                style_only = True

        result = polish_file(target, output, style_only)

        if output_format == "html" and result:
            print(_polish_report_html(
                result["file"],
                result["before_score"],
                result["after_score"],
                result["before_severity"],
                result["after_severity"],
                result["changes"]["phase1"],
                result["changes"]["phase2"],
                result["changes"]["phase3"],
                _count_diff_lines(Path(result["report"]).read_text() if result.get("report") else ""),
            ))

        sys.exit(0)

    if command == "batch":
        if len(clean_args) < 2:
            print("❌ Missing directory path")
            sys.exit(1)
        batch_polish(clean_args[1])
        sys.exit(0)

    print(f"❌ Unknown command: {command}")
    sys.exit(1)


if __name__ == "__main__":
    main()
