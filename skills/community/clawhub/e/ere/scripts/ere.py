#!/usr/bin/env python3
"""
ERE — Editorial Refinement Engine
Helper script for quantitative text analysis.

Usage:
  ere.py analyze <file>              — readability + structure metrics (JSON)
  ere.py diff <original> <refined>   — diff between original and refined (JSON)
  ere.py score <metrics.json>        — compute quality score from metrics
  ere.py profile <name>              — dump editorial profile as JSON
"""

import sys
import json
import re
import math
from pathlib import Path
from difflib import unified_diff, SequenceMatcher

SKILL_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = SKILL_DIR / "profiles"


# ── Profile Loader ──────────────────────────────────────────────

def load_profile(name: str = "default") -> dict:
    """Load editorial profile from YAML (simple subset parser)."""
    profile_file = PROFILES_DIR / f"{name}.yaml"
    if not profile_file.exists():
        profile_file = PROFILES_DIR / "default.yaml"

    if not profile_file.exists():
        return _default_profile()

    # Simple YAML subset parser (no PyYAML dependency)
    profile = {}
    current_section = profile
    section_stack = []
    indent_level = 0

    for line in profile_file.read_text().splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Count leading spaces
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        if current_indent == 0 and stripped.endswith(":"):
            # Top-level key
            key = stripped[:-1].strip()
            current_section = {}
            profile[key] = current_section
        elif current_indent > 0 and stripped.endswith(":"):
            # Nested key
            key = stripped[:-1].strip()
            new_section = {}
            current_section[key] = new_section
            section_stack.append((indent_level, current_section))
            indent_level = current_indent
            current_section = new_section
        elif ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            # Strip inline comments from value
            if "#" in value:
                value = value.split("#")[0].strip()

            # Parse value types
            if value.lower() in ("true", "yes"):
                parsed = True
            elif value.lower() in ("false", "no"):
                parsed = False
            elif value.isdigit():
                parsed = int(value)
            elif value.replace(".", "").isdigit():
                parsed = float(value)
            else:
                parsed = value.strip('"\'')
            current_section[key] = parsed

    return profile.get(name, profile.get("default", profile))


def _default_profile() -> dict:
    return {
        "style": "journalistic",
        "tone": "neutral",
        "refinement_level": 60,
        "language": "pt-BR",
        "engines": {
            "style": True, "structure": True, "rhythm": True,
            "lexical": True, "connectors": True, "context": False, "intro": True
        },
        "fact_preservation": {
            "entity_lock": True, "quote_protect": True, "claim_extract": False
        }
    }


# ── Readability Metrics ─────────────────────────────────────────

def analyze_text(text: str, language: str = "pt-BR") -> dict:
    """Compute readability and structure metrics."""
    sentences = _split_sentences(text)
    words = _split_words(text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    if not sentences or not words:
        return {"error": "Empty text"}

    # Basic counts
    num_sentences = len(sentences)
    num_words = len(words)
    num_paragraphs = len(paragraphs)
    num_chars = len(text)

    # Sentence metrics
    sentence_lengths = [len(_split_words(s)) for s in sentences]
    avg_sentence_len = sum(sentence_lengths) / num_sentences
    max_sentence_len = max(sentence_lengths)

    # Paragraph metrics
    paragraph_lengths = [len(p) for p in paragraphs]
    avg_paragraph_len = sum(paragraph_lengths) / num_paragraphs if num_paragraphs else 0

    # Word metrics
    avg_word_len = sum(len(w) for w in words) / num_words

    # Syllable estimation (simple heuristic for Portuguese)
    syllables = sum(_count_syllables_pt(w) if language == "pt-BR" else _count_syllables_en(w) for w in words)

    # Flesch Reading Ease (approximate)
    if language == "pt-BR":
        flesch = _flesch_pt(num_words, num_sentences, syllables)
    else:
        flesch = _flesch_en(num_words, num_sentences, syllables)

    # Lexical diversity (type-token ratio)
    unique_words = len(set(w.lower() for w in words))
    ttr = unique_words / num_words if num_words else 0

    # Passive voice detection (heuristic)
    passive_count = _count_passive_voice(text, language)

    # Connector density
    connector_count = _count_connectors(words, language)
    connector_density = connector_count / num_sentences if num_sentences else 0

    # Sentence length variance (rhythm indicator)
    variance = sum((l - avg_sentence_len) ** 2 for l in sentence_lengths) / num_sentences
    std_dev = math.sqrt(variance)

    return {
        "counts": {
            "characters": num_chars,
            "words": num_words,
            "sentences": num_sentences,
            "paragraphs": num_paragraphs,
            "unique_words": unique_words
        },
        "readability": {
            "flesch_score": round(flesch, 1),
            "flesch_level": _flesch_level(flesch, language),
            "avg_sentence_length": round(avg_sentence_len, 1),
            "max_sentence_length": max_sentence_len,
            "avg_word_length": round(avg_word_len, 1),
            "avg_paragraph_length": round(avg_paragraph_len, 0)
        },
        "diversity": {
            "ttr": round(ttr, 3),
            "connector_density": round(connector_density, 2)
        },
        "rhythm": {
            "sentence_std_dev": round(std_dev, 1),
            "passive_voice_count": passive_count
        },
        "language": language
    }


def _split_sentences(text: str) -> list:
    """Split text into sentences."""
    # Naive split by punctuation followed by space+capital or newline
    raw = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ú])', text)
    # Also split on explicit newlines between sentences
    result = []
    for segment in raw:
        sub = re.split(r'(?<=[.!?])\n+', segment)
        result.extend(s.strip() for s in sub if s.strip())
    return result or [text.strip()]


def _split_words(text: str) -> list:
    """Split text into words."""
    return [w for w in re.findall(r'\b\w+\b', text.lower()) if len(w) > 0]


def _count_syllables_pt(word: str) -> int:
    """Simple Portuguese syllable counter (heuristic)."""
    word = word.lower()
    # Count vowel groups as syllables
    vowels = 'aeiouáéíóúâêôãõàèìòù'
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    return max(count, 1)


def _count_syllables_en(word: str) -> int:
    """Simple English syllable counter (heuristic)."""
    word = word.lower()
    vowels = 'aeiouy'
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith('e') and count > 1:
        count -= 1
    return max(count, 1)


def _flesch_pt(words: int, sentences: int, syllables: int) -> float:
    """Flesch Reading Ease for Portuguese (Martins et al. adaptation)."""
    if sentences == 0 or words == 0:
        return 0
    return 248.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))


def _flesch_en(words: int, sentences: int, syllables: int) -> float:
    """Flesch Reading Ease for English."""
    if sentences == 0 or words == 0:
        return 0
    return 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))


def _flesch_level(score: float, language: str = "pt-BR") -> str:
    """Map Flesch score to readability level."""
    if language == "pt-BR":
        if score >= 75: return "Muito Fácil"
        if score >= 50: return "Fácil"
        if score >= 25: return "Difícil"
        return "Muito Difícil"
    else:
        if score >= 90: return "Very Easy"
        if score >= 80: return "Easy"
        if score >= 70: return "Fairly Easy"
        if score >= 60: return "Standard"
        if score >= 50: return "Fairly Difficult"
        if score >= 30: return "Difficult"
        return "Very Confusing"


def _count_passive_voice(text: str, language: str) -> int:
    """Heuristic passive voice detection."""
    if language == "pt-BR":
        patterns = [
            r'\b(é|são|foi|foram|era|eram|será|serão|está|estão|estava|estavam)\s+\w+(?:ad[oa]|id[oa])\b',
            r'\b\w+(?:ad[oa]|id[oa])\s+(?:por|pelo|pela|pelos|pelas)\b',
        ]
    else:
        patterns = [
            r'\b(?:is|are|was|were|been|being)\s+\w+ed\b',
            r'\b\w+ed\s+by\b',
        ]
    count = 0
    for p in patterns:
        count += len(re.findall(p, text, re.IGNORECASE))
    return count


def _count_connectors(words: list, language: str) -> int:
    """Count discourse connectors."""
    pt_connectors = {
        'portanto', 'contudo', 'entretanto', 'ademais', 'além', 'assim',
        'consequentemente', 'todavia', 'embora', 'enquanto', 'pois',
        'porém', 'assim', 'dessa', 'desse', 'nesse', 'nessa',
        'primeiramente', 'segundamente', 'finalmente', 'outrossim',
        'não', 'apenas', 'mas', 'também', 'ainda', 'já', 'assim',
        'logo', 'então', 'depois', 'antes', 'agora', 'sempre',
    }
    en_connectors = {
        'therefore', 'however', 'moreover', 'furthermore', 'nevertheless',
        'although', 'while', 'because', 'thus', 'hence', 'consequently',
        'additionally', 'first', 'second', 'finally', 'indeed',
    }
    connectors = pt_connectors if language == "pt-BR" else en_connectors
    return sum(1 for w in words if w.lower() in connectors)


# ── Diff Generator ──────────────────────────────────────────────

def generate_diff(original: str, refined: str, context_lines: int = 2) -> dict:
    """Generate structured diff between original and refined text."""
    orig_lines = original.splitlines(keepends=True)
    ref_lines = refined.splitlines(keepends=True)

    # Unified diff
    diff_lines = list(unified_diff(
        orig_lines, ref_lines,
        fromfile="original", tofile="refined",
        n=context_lines
    ))

    # Similarity ratio
    similarity = SequenceMatcher(None, original, refined).ratio()

    # Classify changes
    additions = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
    change_count = max(additions, deletions)  # a pair of +/- counts as 1 change

    # Word count change
    orig_words = len(_split_words(original))
    ref_words = len(_split_words(refined))
    word_delta = ref_words - orig_words
    word_delta_pct = round((word_delta / orig_words * 100), 1) if orig_words else 0

    return {
        "similarity": round(similarity, 3),
        "changes": change_count,
        "word_count": {
            "original": orig_words,
            "refined": ref_words,
            "delta": word_delta,
            "delta_pct": word_delta_pct
        },
        "unified_diff": "".join(diff_lines) if diff_lines else "(no changes)"
    }


# ── Quality Score ───────────────────────────────────────────────

def compute_score(original_metrics: dict, refined_metrics: dict, diff: dict) -> dict:
    """
    Compute composite quality score.
    Formula: Q = 0.30*F + 0.20*N + 0.15*R + 0.20*S + 0.10*E + 0.05*V
    """
    # Factual Fidelity (F) — estimated from similarity + entity preservation
    similarity = diff.get("similarity", 0)
    factual_fidelity = min(100, max(0, similarity * 100 + 10))

    # Editorial Naturalness (N) — lower connector density = more natural
    r = refined_metrics
    connector_density = r.get("diversity", {}).get("connector_density", 0)
    naturalness = min(100, max(0, 100 - (connector_density * 30)))

    # Readability (R) — from Flesch score
    flesch = r.get("readability", {}).get("flesch_score", 0)
    readability = min(100, max(0, flesch))

    # Style Adherence (S) — estimated from sentence length variance
    std_dev = r.get("rhythm", {}).get("sentence_std_dev", 10)
    style = min(100, max(0, 100 - abs(std_dev - 8) * 5))

    # SEO Utility (E) — placeholder (expanded in Phase 2)
    seo = 85

    # Reviewability (V) — from diff change count
    changes = diff.get("changes", 0)
    reviewability = min(100, max(0, 100 - changes * 2))

    composite = (
        0.30 * factual_fidelity +
        0.20 * naturalness +
        0.15 * readability +
        0.20 * style +
        0.10 * seo +
        0.05 * reviewability
    )

    return {
        "composite": round(composite, 1),
        "subscores": {
            "factual_fidelity": round(factual_fidelity, 1),
            "editorial_naturalness": round(naturalness, 1),
            "readability": round(readability, 1),
            "style_adherence": round(style, 1),
            "seo_utility": round(seo, 1),
            "reviewability": round(reviewability, 1)
        },
        "formula": "0.30F + 0.20N + 0.15R + 0.20S + 0.10E + 0.05V"
    }


# ── CLI ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: ere.py <analyze|diff|score|profile> [args...]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "profile":
        name = sys.argv[2] if len(sys.argv) > 2 else "default"
        profile = load_profile(name)
        print(json.dumps(profile, indent=2, ensure_ascii=False))

    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: ere.py analyze <file> [language]", file=sys.stderr)
            sys.exit(1)
        text = Path(sys.argv[2]).read_text()
        lang = sys.argv[3] if len(sys.argv) > 3 else "pt-BR"
        metrics = analyze_text(text, lang)
        print(json.dumps(metrics, indent=2, ensure_ascii=False))

    elif command == "diff":
        if len(sys.argv) < 4:
            print("Usage: ere.py diff <orig_file> <refined_file>", file=sys.stderr)
            sys.exit(1)
        orig = Path(sys.argv[2]).read_text()
        ref = Path(sys.argv[3]).read_text()
        diff = generate_diff(orig, ref)
        print(json.dumps(diff, indent=2, ensure_ascii=False))

    elif command == "score":
        # Read original and refined metrics from stdin
        data = json.load(sys.stdin)
        orig_m = data.get("original_metrics", {})
        ref_m = data.get("refined_metrics", {})
        diff = data.get("diff", {})
        score = compute_score(orig_m, ref_m, diff)
        print(json.dumps(score, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
