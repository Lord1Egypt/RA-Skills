#!/usr/bin/env python3
"""
A/B Content Predictor v2.0.0 — predict which ad/post variant wins before spending money.

Depth 3 additions over v1:
  • Confidence intervals on every prediction (±N points, derived from dimension variance)
  • Rewrite surgery — specific fix suggestions per losing variant, not just warning flags
  • Cross-ICP scoring — show which audience responds best to each hook
  • Quality gate mode (--min-score) — flag variants below threshold
  • Winner margin analysis — neck-and-neck vs dominant winner changes the recommendation

Based on TRIBE v2 research findings (Meta AI, 2026) mapped to rule-based scoring:
  • Amygdala response    → loss framing, faces, social proof with stakes
  • Reward circuit       → gain framing, scarcity, identity alignment
  • Language cortex      → second-person, short sentences, concrete nouns
  • Visual cortex        → faces in first sentence, concrete imagery

Usage:
    python3 ab_predictor.py --product "crypto-mortgage" --variants variants.json
    python3 ab_predictor.py --product "va-loan" --text "You earned zero down. Use it."
    python3 ab_predictor.py --product "credit-repair" --variants hooks.json --rewrite
    python3 ab_predictor.py --variants hooks.json --cross-icp
    python3 ab_predictor.py --demo
"""

import re
import sys
import json
import argparse
import importlib.util as _ilu
import pathlib as _pl
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Backend: content_resonance_scorer.py (claude-3's TRIBE-based scorer)
# Loaded dynamically so ab_predictor.py stays portable if scorer is absent.
# ---------------------------------------------------------------------------

def _load_crs():
    """Load content_resonance_scorer from sibling project dir."""
    here = _pl.Path(__file__).parent
    scorer_path = here.parent / "content-resonance-scorer" / "content_resonance_scorer.py"
    if not scorer_path.exists():
        return None
    spec = _ilu.spec_from_file_location("content_resonance_scorer", scorer_path)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_CRS = _load_crs()

# Field shim: CRS FeatureScores attribute → (ab_predictor dimension, normalization divisor)
_CRS_FIELD_MAP = {
    "loss_framing_score":       ("loss",          1.0),
    "gain_framing_score":       ("gain",          1.0),
    "social_proof_density":     ("social_proof",  5.0),
    "urgency_density":          ("urgency",       3.0),
    "identity_alignment_score": ("identity",      1.0),
    "sentence_complexity_score":("simplicity",    1.0),
    "second_person_density":    ("second_person", 8.0),
    "concrete_noun_density":    ("concrete",      6.0),
}


# ---------------------------------------------------------------------------
# Neural weight profiles per ICP
# ---------------------------------------------------------------------------

ICP_NEURAL_WEIGHTS = {
    "crypto-mortgage": {
        "loss":         0.8,
        "gain":         1.8,
        "social_proof": 0.9,
        "urgency":      0.6,
        "identity":     1.7,
        "simplicity":   0.8,
        "second_person":1.2,
        "concrete":     1.5,
    },
    "credit-repair": {
        "loss":         1.8,
        "gain":         1.3,
        "social_proof": 1.6,
        "urgency":      1.2,
        "identity":     1.5,
        "simplicity":   1.7,
        "second_person":1.6,
        "concrete":     1.4,
    },
    "va-loan": {
        "loss":         1.4,
        "gain":         1.3,
        "social_proof": 1.3,
        "urgency":      0.7,
        "identity":     2.0,
        "simplicity":   1.5,
        "second_person":1.4,
        "concrete":     1.3,
    },
    "realtor-partner": {
        "loss":         1.5,
        "gain":         1.4,
        "social_proof": 1.8,
        "urgency":      0.5,
        "identity":     1.3,
        "simplicity":   1.3,
        "second_person":1.2,
        "concrete":     1.8,
    },
    "first-time-buyer": {
        "loss":         1.3,
        "gain":         1.4,
        "social_proof": 1.7,
        "urgency":      1.0,
        "identity":     1.4,
        "simplicity":   2.0,
        "second_person":1.7,
        "concrete":     1.5,
    },
}

DEFAULT_WEIGHTS = {k: 1.0 for k in ["loss","gain","social_proof","urgency","identity","simplicity","second_person","concrete"]}

ICP_LABELS = {
    "crypto-mortgage":  "BTC/ETH holder buying without selling",
    "credit-repair":    "500-680 score, shame-sensitive",
    "va-loan":          "Veteran, earned-it framing",
    "realtor-partner":  "Agent/broker, B2B professional",
    "first-time-buyer": "First home, rate-shocked, overwhelmed",
}


# ---------------------------------------------------------------------------
# Rewrite surgery templates (depth 3)
# ICP → dimension → specific, actionable fix instruction
# ---------------------------------------------------------------------------

REWRITE_TEMPLATES = {
    "crypto-mortgage": {
        "gain":         "Add upside specificity: 'Your BTC keeps appreciating while you build equity. Zero coins sold.'",
        "identity":     "Signal in-group: 'BTC holders who bought before 2022 are using this. Here's the exact play.'",
        "concrete":     "Add real numbers: '$200K-$2M in unrealized gains → $0 down via pledge, zero capital gains event.'",
        "second_person":"Open with 'you': 'You don't have to choose between crypto and homeownership.'",
        "urgency":      "REMOVE urgency language — this ICP finds scarcity tactics manipulative.",
    },
    "credit-repair": {
        "loss":         "Add loss framing: 'Every month at 580 costs you $410 more than a buyer at 760. That gap is fixable.'",
        "social_proof": "Add peer proof: 'Most buyers in your score range don't realize they're 90 days from mortgage-ready.'",
        "simplicity":   "Break into short sentences. Remove jargon. 'Step 1: Pull your report. Step 2: Dispute errors. Step 3: Pay down one card.'",
        "second_person":"Lead with 'you': 'You're not stuck. Your score can move 80-120 points in 90 days.'",
        "identity":     "Reframe identity: 'People with a 580 score who follow this plan become homeowners. You can too.'",
        "concrete":     "Name the exact number: 'From 580 to 660 in 90 days — here's the 3-step plan.'",
    },
    "va-loan": {
        "identity":     "Lead with earned-it: 'You served. This benefit was built for you. Zero down, no PMI — it's yours to use.'",
        "loss":         "Frame the unused benefit: 'Every month without using your VA entitlement is $0-down left on the table.'",
        "simplicity":   "Direct cadence: 'Step 1. Get your COE. Step 2. Find a VA-approved lender. Step 3. Close at $0 down.'",
        "concrete":     "Name the benefit explicitly: '$0 down payment. No PMI. VA funding fee waived for disabled veterans.'",
        "urgency":      "REMOVE pressure — veterans distrust urgency. Let the benefit sell itself.",
    },
    "realtor-partner": {
        "social_proof": "Add peer case study: '47 agents switched their preferred lender last quarter. Here's why.'",
        "concrete":     "Name results: '3-day faster closings. 0 last-minute blow-ups in 6 months. 94% on-time close rate.'",
        "loss":         "Frame the reliability cost: 'Every blown deal is a lost referral. Here's what consistent closings look like.'",
        "urgency":      "REMOVE urgency — sounds sales-y to a professional. Track record sells.",
        "gain":         "Frame in agent outcomes: 'More closings, fewer fallouts, clients who send referrals.'",
    },
    "first-time-buyer": {
        "simplicity":   "Use the 3-step format: '3 things to do this week: 1) Pull your credit. 2) Talk to one lender. 3) Know your number.'",
        "social_proof": "Normalize the fear: 'Most first-time buyers feel overwhelmed here. It gets simple fast — here's the checklist.'",
        "second_person":"Make it personal: 'You don't need 20% down. You don't need perfect credit. You need this one checklist.'",
        "concrete":     "Name the number: '$6,000-$12,000 total to get into a $300K home with FHA.'",
        "gain":         "Show the monthly comparison: 'Your rent is $1,600/month. A $300K home runs $1,900. For $300 more, you own it.'",
    },
}

DEFAULT_REWRITES = {
    "loss":         "Add loss framing — what is the reader missing by not acting?",
    "gain":         "Add gain/benefit framing — what specific upside does the reader get?",
    "social_proof": "Add social proof — how many people like them have done this?",
    "urgency":      "Add a timing signal — why does this matter now vs later?",
    "identity":     "Add identity alignment — signal this is built for people like them.",
    "simplicity":   "Simplify — shorter sentences, remove jargon.",
    "second_person":"Add more 'you/your' — make it directly about the reader.",
    "concrete":     "Add specific numbers — dollar amounts, timeframes, percentages.",
}


# ---------------------------------------------------------------------------
# Feature extractors
# ---------------------------------------------------------------------------

LOSS_WORDS = {
    "lose","losing","lost","miss","missing","behind","cost","risk","waste",
    "wasting","stuck","trap","trapped","landlord","rent","paying someone",
    "throwing away","giving away","left behind","fall behind","can't afford",
    "denied","rejected","ignored","blew up","blown","never","without",
}
GAIN_WORDS = {
    "save","saving","earn","earning","build","building","grow","growing",
    "keep","keeping","own","owning","get","gain","profit","upside","more",
    "ahead","equity","wealth","appreciate","compound","benefit","win","won",
    "free","zero","no cost","no PMI","no down","approved","qualify",
}
SOCIAL_PROOF_WORDS = {
    "most","many","people","buyers","veterans","agents","clients","others",
    "everyone","average","typical","thousands","hundreds","families","couples",
    "statistics","data","research","percent","study","proven","according to",
}
URGENCY_WORDS = {
    "now","today","limited","before","deadline","soon","last","final",
    "expires","ending","closing","while","don't wait","act","immediately",
    "window","opportunity","rates are","market is","won't last",
}
IDENTITY_WORDS = {
    "veteran","veterans","served","service","crypto","bitcoin","ethereum","holders",
    "first-time","renter","renters","first generation","entrepreneur","self-employed",
    "family","couples","couple","professional","agent","realtor",
    "people like you","someone like you","for you","built for",
}
CONCRETE_PATTERN = re.compile(
    r'\$[\d,]+|\d+[\s-]?(day|month|year|point|percent|%|step|BR|bed|bath|hour|minute|sq)',
    re.IGNORECASE
)
SECOND_PERSON = re.compile(r'\b(you|your|you\'re|you\'ve|you\'ll|yourself)\b', re.IGNORECASE)
FACE_PATTERN = re.compile(r'\b(I|me|my|we|our|Patrick|Sarah|[A-Z][a-z]+)\b')


def _words(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text.lower())


def _score_features_via_crs(text: str) -> dict[str, float]:
    """Feature extraction via content_resonance_scorer backend."""
    scored = _CRS.score_text(text)
    f = scored.features
    feats = {}
    for crs_attr, (dim, divisor) in _CRS_FIELD_MAP.items():
        raw = getattr(f, crs_attr, 0.0)
        feats[dim] = min(1.0, raw / divisor)
    feats["_face_first"] = 1.0 if FACE_PATTERN.search(text[:100]) else 0.0
    feats["_word_count"] = float(scored.word_count)
    feats["_sentences"] = float(scored.sentence_count)
    return feats


def _score_features_internal(text: str) -> dict[str, float]:
    """Fallback feature extraction (used when CRS backend is unavailable)."""
    words = _words(text)
    n = max(len(words), 1)
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    n_sentences = max(len(sentences), 1)
    avg_words_per_sentence = n / n_sentences

    loss_hits = sum(1 for w in words if w in LOSS_WORDS)
    gain_hits = sum(1 for w in words if w in GAIN_WORDS)
    social_hits = sum(1 for w in words if w in SOCIAL_PROOF_WORDS)
    urgency_hits = sum(1 for w in words if w in URGENCY_WORDS)
    identity_hits = sum(1 for w in words if w in IDENTITY_WORDS)
    concrete_hits = len(CONCRETE_PATTERN.findall(text))
    second_person_hits = len(SECOND_PERSON.findall(text))
    face_in_first_30 = len(FACE_PATTERN.findall(text[:100])) > 0

    simplicity_score = max(0.0, 1.0 - (avg_words_per_sentence - 8) / 20)

    return {
        "loss":          min(1.0, loss_hits / max(n * 0.05, 1)),
        "gain":          min(1.0, gain_hits / max(n * 0.05, 1)),
        "social_proof":  min(1.0, social_hits / max(n * 0.05, 1)),
        "urgency":       min(1.0, urgency_hits / max(n * 0.03, 1)),
        "identity":      min(1.0, identity_hits / max(n * 0.04, 1)),
        "simplicity":    max(0.0, simplicity_score),
        "second_person": min(1.0, second_person_hits / max(n * 0.08, 1)),
        "concrete":      min(1.0, concrete_hits / max(n_sentences * 0.5, 1)),
        "_face_first":   1.0 if face_in_first_30 else 0.0,
        "_word_count":   n,
        "_sentences":    n_sentences,
    }


def score_features(text: str) -> dict[str, float]:
    """Extract normalized feature scores. Uses CRS backend when available."""
    if _CRS is not None:
        return _score_features_via_crs(text)
    return _score_features_internal(text)


def resonance_score(text: str, icp_key: str) -> dict:
    """
    Score content against an ICP's neural weight profile.
    Returns score 0-100, confidence interval, per-dimension breakdown.
    """
    weights = ICP_NEURAL_WEIGHTS.get(icp_key, DEFAULT_WEIGHTS)
    features = score_features(text)

    weighted_sum = 0.0
    total_weight = 0.0
    breakdown = {}

    for dim, weight in weights.items():
        feat_val = features.get(dim, 0.0)
        contribution = feat_val * weight
        weighted_sum += contribution
        total_weight += weight
        breakdown[dim] = {
            "raw": round(feat_val, 3),
            "weight": weight,
            "contribution": round(contribution, 3),
        }

    if features.get("_face_first"):
        weighted_sum += 0.05 * total_weight / len(weights)

    raw_score = weighted_sum / total_weight if total_weight else 0
    score_100 = min(100, round(raw_score * 100))
    ci = confidence_interval(breakdown, score_100)

    result = {
        "score": score_100,
        "ci": ci,
        "icp": icp_key,
        "word_count": int(features["_word_count"]),
        "sentences": int(features["_sentences"]),
        "breakdown": breakdown,
        "flags": _get_flags(features, icp_key, score_100),
        "backend": "crs" if _CRS is not None else "internal",
    }

    if _CRS is not None:
        crs_baseline = round(_CRS.score_text(text).features.resonance_score, 1)
        divergence = abs(score_100 - crs_baseline)
        result["_crs_baseline"] = crs_baseline
        result["_divergence"] = round(divergence, 1)
        if divergence >= 15:
            result["flags"].append(
                f"⚠ ICP weighting shifts score {divergence:.0f}pts from baseline "
                f"({score_100} vs CRS {crs_baseline:.0f}) — review ICP profile weights"
            )

    return result


# ---------------------------------------------------------------------------
# Depth 3: Confidence intervals
# ---------------------------------------------------------------------------

def confidence_interval(breakdown: dict, score: int) -> int:
    """
    Prediction confidence interval (±N points).

    Derived from variance across weighted dimension contributions.
    High variance = signal concentrated in 1-2 dimensions = shakier prediction.
    Low variance = signal spread evenly = more reliable.

    Score extremes (very high/low) reduce CI — less likely to flip category.
    """
    contributions = [d["contribution"] for d in breakdown.values()]
    if not contributions:
        return 15
    n = len(contributions)
    mean = sum(contributions) / n
    variance = sum((c - mean) ** 2 for c in contributions) / n
    std = variance ** 0.5
    # Map std → CI: low variance → ±5, high → ±20
    ci = max(5, min(20, round(std * 100 * 1.8)))
    # Extreme scores are more reliable — tighten CI
    if score >= 85 or score <= 20:
        ci = max(5, ci - 4)
    return ci


# ---------------------------------------------------------------------------
# Depth 3: Cross-ICP scoring
# ---------------------------------------------------------------------------

def cross_icp_score(text: str) -> dict[str, dict]:
    """
    Score text against all ICP profiles.
    Returns {icp_key: {"score": N, "ci": N, "label": str}} sorted best-first.
    """
    results = {}
    for icp_key in ICP_NEURAL_WEIGHTS:
        r = resonance_score(text, icp_key)
        results[icp_key] = {
            "score": r["score"],
            "ci": r["ci"],
            "label": ICP_LABELS.get(icp_key, icp_key),
        }
    return dict(sorted(results.items(), key=lambda x: x[1]["score"], reverse=True))


# ---------------------------------------------------------------------------
# Depth 3: Rewrite surgery
# ---------------------------------------------------------------------------

def generate_rewrite_suggestions(features: dict, icp_key: str, score: int) -> list[str]:
    """
    Generate specific, actionable rewrite instructions for a low-scoring variant.
    Returns targeted fix suggestions (not just warning flags).
    """
    if score >= 70:
        return []  # publish-ready — no surgery needed

    weights = ICP_NEURAL_WEIGHTS.get(icp_key, DEFAULT_WEIGHTS)
    icp_rewrites = REWRITE_TEMPLATES.get(icp_key, {})
    suggestions = []

    # Find dimensions where: (weight is high AND raw signal is weak) OR (weight is low AND raw is strong)
    dim_gaps = []
    for dim, weight in weights.items():
        if dim.startswith("_"):
            continue
        raw = features.get(dim, 0.0)
        if weight <= 0.7 and raw > 0.1:
            dim_gaps.append((dim, weight, raw, "overuse"))
        elif weight >= 1.3 and raw < 0.15:
            gap = weight * (1.0 - raw)
            dim_gaps.append((dim, weight, raw, gap))

    actionable = [(d, w, r, g) for d, w, r, g in dim_gaps if g != "overuse"]
    overuse = [(d, w, r, g) for d, w, r, g in dim_gaps if g == "overuse"]
    actionable.sort(key=lambda x: x[3], reverse=True)

    for dim, weight, raw, gap in actionable[:3]:
        fix = icp_rewrites.get(dim) or DEFAULT_REWRITES.get(dim, f"Strengthen {dim}")
        suggestions.append(f"→ [{dim.upper().replace('_', ' ')}] {fix}")

    for dim, weight, raw, _ in overuse:
        fix = icp_rewrites.get(dim) or f"Reduce {dim} — backfires with this ICP."
        suggestions.append(f"→ [REMOVE {dim.upper().replace('_', ' ')}] {fix}")

    return suggestions


def _get_flags(features: dict, icp_key: str, score: int) -> list[str]:
    """Generate human-readable coaching flags."""
    flags = []
    weights = ICP_NEURAL_WEIGHTS.get(icp_key, DEFAULT_WEIGHTS)

    if features["loss"] < 0.02 and weights["loss"] >= 1.4:
        flags.append("⚠ Add loss framing — this ICP is loss-aversion dominant")
    if features["gain"] < 0.02 and weights["gain"] >= 1.5:
        flags.append("⚠ Add gain/upside framing — this ICP responds to opportunity")
    if features["social_proof"] < 0.02 and weights["social_proof"] >= 1.5:
        flags.append("⚠ Add social proof — this ICP needs peer validation")
    if features["urgency"] > 0.1 and weights["urgency"] <= 0.7:
        flags.append("⚠ Reduce urgency language — may backfire with this ICP")
    if features["second_person"] < 0.03 and weights["second_person"] >= 1.4:
        flags.append("⚠ Add more 'you/your' — this ICP responds to direct address")
    if features["simplicity"] < 0.4 and weights["simplicity"] >= 1.5:
        flags.append("⚠ Simplify sentences — this ICP is easily overwhelmed")
    if features["concrete"] < 0.1 and weights["concrete"] >= 1.4:
        flags.append("⚠ Add concrete numbers/specifics — this ICP trusts data")
    if score >= 70:
        flags.append("✓ Strong resonance — publish-ready for this ICP")
    elif score >= 50:
        flags.append("~ Moderate resonance — refine before spending ad budget")
    else:
        flags.append("✗ Low resonance — rewrite against ICP hook formulas before use")

    return flags


# ---------------------------------------------------------------------------
# A/B comparison
# ---------------------------------------------------------------------------

@dataclass
class Variant:
    label: str
    text: str
    score: int = 0
    ci: int = 10
    breakdown: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)
    rewrites: list = field(default_factory=list)
    features: dict = field(default_factory=dict)


def compare_variants(variants: list[Variant], icp_key: str, show_rewrites: bool = False) -> list[Variant]:
    """Score all variants and return sorted best-first."""
    for v in variants:
        result = resonance_score(v.text, icp_key)
        v.score = result["score"]
        v.ci = result["ci"]
        v.breakdown = result["breakdown"]
        v.flags = result["flags"]
        v.features = score_features(v.text)
        if show_rewrites:
            v.rewrites = generate_rewrite_suggestions(v.features, icp_key, v.score)
    return sorted(variants, key=lambda v: v.score, reverse=True)


def print_comparison(variants: list[Variant], icp_key: str, show_rewrites: bool = False,
                     show_cross_icp: bool = False, min_score: Optional[int] = None):
    sep = "━" * 64
    print(f"\n{sep}")
    print(f"A/B RESONANCE PREDICTION — ICP: {icp_key}")
    print(f"                           ({ICP_LABELS.get(icp_key, '')})")
    print(f"{sep}")
    print(f"{'Rank':<5} {'Label':<22} {'Score':<8} {'CI':<8} Words")
    print("─" * 64)

    for i, v in enumerate(variants, 1):
        medals = ["🥇", "🥈", "🥉"]
        medal = medals[i - 1] if i - 1 < len(medals) else f" #{i}"
        bar_len = v.score // 5
        bar_str = "█" * bar_len + "░" * (20 - bar_len)
        ci_str = f"±{v.ci}"
        wc = int(v.features.get("_word_count", 0))
        below_gate = min_score and v.score < min_score
        gate_flag = " ⛔ BELOW GATE" if below_gate else ""
        print(f"  {medal}  {v.label:<22} [{bar_str}] {v.score}/100 {ci_str:<6} ({wc}w){gate_flag}")

    print()
    winner = variants[0]
    runner_up = variants[1] if len(variants) > 1 else None
    margin = (winner.score - runner_up.score) if runner_up else None

    print(f"PREDICTED WINNER: {winner.label}")
    print(f"Score: {winner.score}/100 (±{winner.ci})")

    if margin is not None:
        if margin <= 10:
            print(f"Margin: +{margin} pts — NECK AND NECK. Run a real A/B test before committing budget.")
        elif margin <= 25:
            print(f"Margin: +{margin} pts — Clear advantage. Winner likely; test to confirm.")
        else:
            print(f"Margin: +{margin} pts — DOMINANT. Ship the winner.")

    print()
    print("Winner strengths:")
    for flag in winner.flags:
        if flag.startswith("✓") or flag.startswith("~"):
            print(f"  {flag}")

    if len(variants) > 1:
        loser = variants[-1]
        print(f"\nWHY '{loser.label}' LOSES ({loser.score}/100 ±{loser.ci}):")
        for f in [x for x in loser.flags if x.startswith("⚠") or x.startswith("✗")][:3]:
            print(f"  {f}")
        if show_rewrites and loser.rewrites:
            print(f"\n  REWRITE SURGERY — {loser.label}:")
            for suggestion in loser.rewrites:
                print(f"    {suggestion}")

    if show_rewrites:
        for v in variants[1:-1]:  # middle variants (already handled first/last)
            if v.rewrites:
                print(f"\n  REWRITE SURGERY — {v.label} ({v.score}/100):")
                for suggestion in v.rewrites:
                    print(f"    {suggestion}")

    if show_cross_icp:
        print(f"\n{'─' * 64}")
        print(f"CROSS-ICP PERFORMANCE — '{winner.label}'")
        print(f"{'ICP':<24} {'Score':<8} {'CI':<6} Audience")
        print("─" * 64)
        cross = cross_icp_score(winner.text)
        for icp, data in cross.items():
            marker = " ◀ current" if icp == icp_key else ""
            print(f"  {icp:<24} {data['score']}/100   ±{data['ci']:<4} {data['label']}{marker}")
        best_icp = list(cross.keys())[0]
        if best_icp != icp_key:
            print(f"\n  💡 This hook performs best for: {best_icp} ({cross[best_icp]['score']}/100)")
            print(f"     Consider retargeting to that audience.")

    print(f"\n{sep}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

__version__ = "2.0.0"


def main():
    parser = argparse.ArgumentParser(
        description="A/B content resonance predictor v2 — confidence intervals, rewrite surgery, cross-ICP scoring"
    )
    parser.add_argument("--product", "-p", default="first-time-buyer",
                        help="ICP key: crypto-mortgage, credit-repair, va-loan, realtor-partner, first-time-buyer")
    parser.add_argument("--variants", help="JSON file with [{label, text}] array")
    parser.add_argument("--text", help="Score a single piece of content")
    parser.add_argument("--demo", action="store_true", help="Run demo comparison (no API key needed)")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output JSON")
    parser.add_argument("--version", action="version", version=f"ab-predictor {__version__}")
    # Depth 3 flags
    parser.add_argument("--rewrite", action="store_true",
                        help="Show specific rewrite surgery for losing variants")
    parser.add_argument("--cross-icp", dest="cross_icp", action="store_true",
                        help="Show winner performance across all ICP profiles")
    parser.add_argument("--min-score", dest="min_score", type=int, default=None,
                        help="Quality gate: flag variants below this score threshold (e.g. --min-score=60)")
    args = parser.parse_args()

    if args.demo:
        demo_variants = [
            Variant("Hook A — Loss frame",
                    "You don't have to sell your Bitcoin to buy a house. "
                    "Pledge it as collateral. Keep the upside. Get the keys. "
                    "No capital gains. No missed appreciation. "
                    "Crypto holders: this is real and it's available now."),
            Variant("Hook B — Generic",
                    "Looking to buy a home? We offer competitive rates and fast pre-approvals. "
                    "Our experienced team will guide you through the process. "
                    "Contact us today to learn more about our mortgage options."),
            Variant("Hook C — Identity + concrete",
                    "BTC holders who bought before 2022 are sitting on $200K-$2M in "
                    "unrealized gains. Fannie Mae now lets you pledge that crypto as collateral "
                    "— zero capital gains event, zero coins sold. "
                    "Your coins appreciate while you build equity. That's the move."),
        ]
        ranked = compare_variants(demo_variants, "crypto-mortgage", show_rewrites=True)
        print_comparison(ranked, "crypto-mortgage", show_rewrites=True,
                         show_cross_icp=True, min_score=args.min_score)
        return

    if args.text:
        result = resonance_score(args.text, args.product)
        if args.as_json:
            features = score_features(args.text)
            result["rewrite_suggestions"] = generate_rewrite_suggestions(
                features, args.product, result["score"]
            )
            if args.cross_icp:
                result["cross_icp"] = cross_icp_score(args.text)
            print(json.dumps(result, indent=2))
        else:
            print(f"\nResonance score for '{args.product}': {result['score']}/100 (±{result['ci']})")
            for flag in result["flags"]:
                print(f"  {flag}")
            if args.rewrite:
                features = score_features(args.text)
                rewrites = generate_rewrite_suggestions(features, args.product, result["score"])
                if rewrites:
                    print("\nRewrite suggestions:")
                    for r in rewrites:
                        print(f"  {r}")
            if args.cross_icp:
                cross = cross_icp_score(args.text)
                print(f"\nCross-ICP performance:")
                for icp, data in cross.items():
                    marker = " ◀" if icp == args.product else ""
                    print(f"  {icp:<24} {data['score']}/100 ±{data['ci']}{marker}")
        return

    if args.variants:
        with open(args.variants) as f:
            raw = json.load(f)
        variants = [Variant(label=v["label"], text=v["text"]) for v in raw]
        ranked = compare_variants(variants, args.product, show_rewrites=args.rewrite)
        if args.as_json:
            output = []
            for v in ranked:
                item = {"label": v.label, "score": v.score, "ci": v.ci, "flags": v.flags}
                if args.rewrite:
                    item["rewrite_suggestions"] = v.rewrites
                if args.cross_icp:
                    item["cross_icp"] = cross_icp_score(v.text)
                output.append(item)
            print(json.dumps(output, indent=2))
        else:
            print_comparison(ranked, args.product, show_rewrites=args.rewrite,
                             show_cross_icp=args.cross_icp, min_score=args.min_score)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
