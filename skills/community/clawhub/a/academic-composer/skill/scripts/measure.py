#!/usr/bin/env python3
"""
Quantitative scorer for writing style signals, syntactic complexity, and semantic density.

Three measurement axes:
  A. Style Pattern Score (0-100, lower = more natural)
  B. Syntactic Complexity (MDD mean + variance vs. human baselines)
  C. Semantic Density (TTR, content-word ratio, specificity)

Usage:
  python measure.py --file essay.txt --json
  echo "ESSAY TEXT" | python measure.py --stdin --json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

PATTERNS: List[Dict[str, Any]] = [
    {"id": "P01_UNDUE_EMPHASIS", "name": "Undue emphasis", "category": "content",
     "regex": r"(plays? a (vital|crucial|significant) role|stands as a testament|lasting impact|profound significance)"},
    {"id": "P02_SUPERFICIAL_ANALYSIS", "name": "Superficial analysis", "category": "content",
     "regex": r"(in today's (?:fast[- ]paced )?world|broadly speaking|it is clear that)\b"},
    {"id": "P03_REGRESSION_TO_MEAN", "name": "Regression to the mean", "category": "content",
     "regex": r"\b(various|several|numerous)\s+(stakeholders|aspects|dimensions|facets)\b"},
    {"id": "P04_AI_VOCABULARY", "name": "AI vocabulary", "category": "vocabulary",
     "regex": r"\b(delve|intricate|tapestry|pivotal|underscore|landscape|foster|testament|enhance|crucial)\b"},
    {"id": "P05_EXCESSIVE_ADVERBS", "name": "Excessive adverbs", "category": "vocabulary",
     "regex": r"\b(significantly|notably|remarkably|fundamentally|profoundly)\b"},
    {"id": "P06_CLICHE_METAPHORS", "name": "Cliche metaphors", "category": "vocabulary",
     "regex": r"\b(tapestry|beacon|cornerstone|journey together|landscape of)\b"},
    {"id": "P07_REDUNDANT_MODIFIERS", "name": "Redundant modifiers", "category": "vocabulary",
     "regex": r"\b(very unique|extremely essential|highly innovative|completely unanimous|truly inevitable)\b"},
    {"id": "P08_FILLER_HEDGING", "name": "Filler hedging", "category": "vocabulary",
     "regex": r"(it is worth noting|it is important to note|it should be mentioned|needless to say)"},
    {"id": "P09_NEGATIVE_PARALLELISM", "name": "Negative parallelisms", "category": "rhetorical",
     "regex": r"(?i)\bit'?s not [^.]{3,40},\s?it'?s\b"},
    {"id": "P10_RULE_OF_THREES", "name": "Rule of threes", "category": "rhetorical",
     "regex": r"\b(\w+,\s+\w+,\s+and\s+\w+)\b"},
    {"id": "P11_FALSE_RANGES", "name": "False ranges", "category": "rhetorical",
     "regex": r"from [^,]{5,50} to [^.\n]{5,50}"},
    {"id": "P12_PRESENT_PARTICIPLE_TAIL", "name": "Present participle tailing", "category": "rhetorical",
     "regex": r",\s*(highlighting|underscoring|emphasizing|showcasing|demonstrating)\s"},
    {"id": "P13_OVER_ATTRIBUTION", "name": "Over-attribution", "category": "rhetorical",
     "regex": r"(?i)\b(experts say|critics argue|observers have|many scholars|industry leaders)\b"},
    {"id": "P14_COMPULSIVE_SUMMARIES", "name": "Compulsive summaries", "category": "rhetorical",
     "regex": r"(?im)^(Overall,|In conclusion,|To summarize,|In summary,)"},
    {"id": "P15_EM_DASH_OVERKILL", "name": "Em dash overkill", "category": "punctuation",
     "regex": r"\u2014"},
    {"id": "P16_EN_DASH_AVOIDANCE", "name": "En dash / hyphen misuse", "category": "punctuation",
     "regex": r"\b\d{4}[-\u2013]\d{4}\b"},
    {"id": "P17_TRANSITION_OVERUSE", "name": "Transition overuse", "category": "punctuation",
     "regex": r"\b(Furthermore|Moreover|Additionally|Consequently|Nevertheless)[,:]\s"},
    {"id": "P18_COLLABORATIVE_REGISTER", "name": "Collaborative register", "category": "register",
     "regex": r"(?i)(i hope this helps|let me know if you need|feel free to reach out|happy to assist)"},
    {"id": "P19_LETTER_FORMALITY", "name": "Letter-style formality", "category": "register",
     "regex": r"(?i)(i hope (?:this email|this message) finds you well|dear reader|yours sincerely)"},
    {"id": "P20_INSTRUCTIONAL_CONDESCENSION", "name": "Instructional condescension", "category": "register",
     "regex": r"(?i)\b(here's how to|follow these steps|first, you should|it'?s important to understand that)\b"},
    {"id": "P21_MARKDOWN_ARTIFACTS", "name": "Markdown artifacts", "category": "formatting",
     "regex": r"(\*\*|#{1,6}\s|```|\[.*\]\(.*\))"},
    {"id": "P22_EXCESSIVE_LISTS", "name": "Excessive lists", "category": "formatting",
     "regex": r"(?m)^[\s]*([-*]|\d+\.)\s"},
    {"id": "P23_TEXTBOOK_BOLDING", "name": "Textbook bolding", "category": "formatting",
     "regex": r"\*\*[^*]+\*\*"},
    {"id": "P24_EMOJI_SYMBOL", "name": "Emoji/symbol injection", "category": "formatting",
     "regex": r"[\U0001F300-\U0001FAFF\u2713\u2714\u2705\U0001F680\U0001F4A1]"},
]

PATTERN_WEIGHTS: Dict[str, float] = {
    "P04_AI_VOCABULARY": 0.062114147518838286,
    "P05_EXCESSIVE_ADVERBS": 0.05395132253816986,
    "P06_CLICHE_METAPHORS": 0.13577738498369918,
    "P10_RULE_OF_THREES": 0.08061744685481181,
    "P11_FALSE_RANGES": 0.034135437549311635,
    "P12_PRESENT_PARTICIPLE_TAIL": 0.11333005124822323,
    "P13_OVER_ATTRIBUTION": 0.05287685072546817,
    "P14_COMPULSIVE_SUMMARIES": 0.05978647318777634,
    "P15_EM_DASH_OVERKILL": 0.13577738498369918,
    "P17_TRANSITION_OVERUSE": 7.873044260382927e-05,
    "P21_MARKDOWN_ARTIFACTS": 0.13577738498369918,
    "P23_TEXTBOOK_BOLDING": 0.13577738498369918,
}

HUMAN_MDD_MEAN = 2.333775514332394
HUMAN_MDD_VARIANCE = 0.01989719949201613
AI_SCORE_THRESHOLD = 15.0
MDD_MEAN_LOW = 2.15
MDD_MEAN_HIGH = 2.55
MDD_VARIANCE_MIN = 0.016
TTR_MIN = 0.50
CONTENT_WORD_RATIO_LOW = 0.52
CONTENT_WORD_RATIO_HIGH = 0.65
CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV"}


def _word_count(text: str) -> int:
    return len(text.split())


def compute_pattern_scores(text: str) -> Tuple[float, List[Dict[str, Any]]]:
    wc = _word_count(text)
    if wc == 0:
        return 0.0, []
    details: List[Dict[str, Any]] = []
    weighted_sum = 0.0
    for pat in PATTERNS:
        matches = list(re.finditer(pat["regex"], text))
        count = len(matches)
        density = (count / wc) * 1000
        weight = PATTERN_WEIGHTS.get(pat["id"], 0.0)
        contribution = density * weight
        details.append({"id": pat["id"], "name": pat["name"], "category": pat["category"],
                        "count": count, "density_per_1k": round(density, 3),
                        "weight": round(weight, 4), "contribution": round(contribution, 4)})
        weighted_sum += contribution
    score = min(100.0, (weighted_sum / 5.0) * 100.0)
    return round(score, 1), details


def _load_spacy():
    import spacy
    try:
        return spacy.load("en_core_web_sm", disable=["ner", "textcat"])
    except OSError:
        raise OSError("spaCy model 'en_core_web_sm' not found. Install: python -m spacy download en_core_web_sm")


def compute_mdd(text: str) -> Dict[str, Any]:
    nlp = _load_spacy()
    doc = nlp(text)
    sent_mdds: List[float] = []
    for sent in doc.sents:
        tokens = [t for t in sent if not t.is_punct and not t.is_space]
        if len(tokens) < 3:
            continue
        distances = [abs(tok.i - tok.head.i) for tok in tokens if tok.dep_ != "ROOT"]
        if distances:
            sent_mdds.append(sum(distances) / len(distances))
    if not sent_mdds:
        return {"mdd_mean": 0.0, "mdd_variance": 0.0, "n_sentences": 0, "mdd_pass": False,
                "distance_from_human": {"mean_delta": 0.0, "variance_delta": 0.0}}
    mdd_mean = sum(sent_mdds) / len(sent_mdds)
    mdd_var = sum((m - mdd_mean) ** 2 for m in sent_mdds) / len(sent_mdds) if len(sent_mdds) > 1 else 0.0
    return {"mdd_mean": round(mdd_mean, 4), "mdd_variance": round(mdd_var, 4),
            "n_sentences": len(sent_mdds),
            "mdd_pass": MDD_MEAN_LOW <= mdd_mean <= MDD_MEAN_HIGH and mdd_var >= MDD_VARIANCE_MIN,
            "distance_from_human": {"mean_delta": round(mdd_mean - HUMAN_MDD_MEAN, 4),
                                    "variance_delta": round(mdd_var - HUMAN_MDD_VARIANCE, 4)}}


def compute_semantic_density(text: str) -> Dict[str, Any]:
    nlp = _load_spacy()
    doc = nlp(text)
    all_tokens, content_tokens = [], []
    entity_count, numeric_count = len(doc.ents), 0
    for tok in doc:
        if tok.is_space or tok.is_punct:
            continue
        lemma = tok.lemma_.lower()
        all_tokens.append(lemma)
        if tok.pos_ in CONTENT_POS:
            content_tokens.append(lemma)
        if tok.like_num:
            numeric_count += 1
    n_all, n_content = len(all_tokens), len(content_tokens)
    ttr = len(set(content_tokens)) / n_content if n_content > 0 else 0.0
    content_ratio = n_content / n_all if n_all > 0 else 0.0
    specificity = (entity_count + numeric_count) / n_all if n_all > 0 else 0.0
    return {"ttr": round(ttr, 4), "content_word_ratio": round(content_ratio, 4),
            "specificity": round(specificity, 4), "n_tokens": n_all, "n_content_tokens": n_content,
            "n_entities": entity_count, "n_numeric": numeric_count,
            "ttr_pass": ttr >= TTR_MIN,
            "ratio_pass": CONTENT_WORD_RATIO_LOW <= content_ratio <= CONTENT_WORD_RATIO_HIGH}


def measure(text: str) -> Dict[str, Any]:
    ai_score, pattern_details = compute_pattern_scores(text)
    mdd = compute_mdd(text)
    density = compute_semantic_density(text)
    ai_pass = ai_score <= AI_SCORE_THRESHOLD
    overall_pass = ai_pass and mdd["mdd_pass"] and density["ttr_pass"] and density["ratio_pass"]
    top_issues = _identify_top_issues(ai_score, ai_pass, pattern_details, mdd, density)
    return {"passes": overall_pass, "ai_pattern_score": ai_score, "ai_pattern_pass": ai_pass,
            "pattern_details": pattern_details, "syntactic": mdd, "semantic": density,
            "top_issues": top_issues, "word_count": _word_count(text)}


def _identify_top_issues(ai_score, ai_pass, pattern_details, mdd, density) -> List[str]:
    issues: List[Tuple[float, str]] = []
    if not ai_pass:
        flagged = sorted([p for p in pattern_details if p["count"] > 0 and p["weight"] > 0],
                         key=lambda p: p["contribution"], reverse=True)
        for p in flagged[:3]:
            issues.append((p["contribution"],
                           f"Reduce {p['name']}: {p['count']} hits, density {p['density_per_1k']}/1k words"))
    if not mdd.get("mdd_pass", True):
        d = mdd["distance_from_human"]
        if mdd["mdd_mean"] < MDD_MEAN_LOW or mdd["mdd_mean"] > MDD_MEAN_HIGH:
            issues.append((abs(d["mean_delta"]),
                           f"MDD mean {mdd['mdd_mean']} outside [{MDD_MEAN_LOW}-{MDD_MEAN_HIGH}]"))
        if mdd["mdd_variance"] < MDD_VARIANCE_MIN:
            issues.append((abs(d["variance_delta"]),
                           f"MDD variance {mdd['mdd_variance']} below {MDD_VARIANCE_MIN}"))
    if not density.get("ttr_pass", True):
        issues.append((TTR_MIN - density["ttr"], f"TTR {density['ttr']:.4f} below {TTR_MIN}"))
    if not density.get("ratio_pass", True):
        cwr = density["content_word_ratio"]
        if cwr < CONTENT_WORD_RATIO_LOW:
            issues.append((CONTENT_WORD_RATIO_LOW - cwr, f"Content-word ratio {cwr:.4f} too low"))
        elif cwr > CONTENT_WORD_RATIO_HIGH:
            issues.append((cwr - CONTENT_WORD_RATIO_HIGH, f"Content-word ratio {cwr:.4f} too high"))
    issues.sort(key=lambda x: x[0], reverse=True)
    return [msg for _, msg in issues[:5]]


def main():
    parser = argparse.ArgumentParser(description="Measure writing style signals")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to essay text file")
    group.add_argument("--stdin", action="store_true", help="Read essay from stdin (avoids CLI arg exposure)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    report = measure(text)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        status = "PASS" if report["passes"] else "FAIL"
        print(f"Style Report: {status} | Score: {report['ai_pattern_score']}/100 | "
              f"MDD: {report['syntactic']['mdd_mean']} | TTR: {report['semantic']['ttr']}")
        for iss in report["top_issues"]:
            print(f"  - {iss}")


if __name__ == "__main__":
    main()
