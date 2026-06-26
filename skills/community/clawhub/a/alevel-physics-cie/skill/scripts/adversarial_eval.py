#!/usr/bin/env python3
"""
Adversarial evaluation for the alevel-physics-cie skill.

Three attack strategies adapted from Xie et al. (2024) "Adversarial Math
Word Problem Generation" for physics answer-template robustness testing:

  1. Numeric Perturbation (M3-style) — swap numeric values, check template stability
  2. Context Swap — replace surface-level objects, check formula invariance
  3. Question-Type Adversarial — change action verbs, check type reclassification

Usage:
  python skill/scripts/adversarial_eval.py
  python skill/scripts/adversarial_eval.py --strategies numeric --variants 5 --max-questions 10
  python skill/scripts/adversarial_eval.py --strategies numeric,context,type --output report.json
"""

import argparse
import json
import math
import os
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Template parser
# ---------------------------------------------------------------------------

SECTION_RE = re.compile(
    r"^##\s+(Question type|Given|Required|Formulae\s*/?\s*principles|Answer frame|Check)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def parse_template(text: str) -> Dict[str, object]:
    """Split a model output into its template sections."""
    result: Dict[str, object] = {
        "question_type": None,
        "given": [],
        "required": "",
        "formulae": [],
        "answer_frame": [],
        "check": [],
        "raw": text,
    }
    if not text:
        return result

    splits = SECTION_RE.split(text)
    current_key = None
    for chunk in splits:
        header = chunk.strip().lower()
        if header == "question type":
            current_key = "question_type"
        elif header == "given":
            current_key = "given"
        elif header == "required":
            current_key = "required"
        elif "formulae" in header or "principles" in header:
            current_key = "formulae"
        elif header == "answer frame":
            current_key = "answer_frame"
        elif header == "check":
            current_key = "check"
        elif current_key is not None:
            body = chunk.strip()
            if current_key == "question_type":
                result["question_type"] = body.split("\n")[0].strip().lower() if body else None
            elif current_key == "required":
                result["required"] = body
            else:
                items = [ln.strip().lstrip("-•0123456789.) ").strip() for ln in body.splitlines() if ln.strip()]
                result[current_key] = items
    return result


def template_is_valid(parsed: Dict) -> bool:
    return parsed["question_type"] is not None and len(parsed.get("formulae", [])) > 0


# ---------------------------------------------------------------------------
# Numeric extraction and physics-aware M3 perturbation
# ---------------------------------------------------------------------------

NUMERIC_RE = re.compile(r"(?<![A-Za-z])(\d+\.?\d*)")

PHYSICS_KEYWORDS_POSITIVE = [
    "mass", "length", "radius", "diameter", "distance", "height", "width",
    "resistance", "frequency", "speed", "velocity", "power", "energy",
    "force", "tension", "current", "voltage", "charge", "capacitance",
    "wavelength", "amplitude", "intensity", "pressure", "temperature",
    "density", "volume", "area", "time", "period",
]
ANGLE_KEYWORDS = ["angle", "degree", "°"]
COUNT_KEYWORDS = ["turns", "coils", "loops", "particles", "nucleons", "protons", "neutrons", "slits"]


def _context_around(text: str, pos: int, window: int = 40) -> str:
    start = max(0, pos - window)
    end = min(len(text), pos + window)
    return text[start:end].lower()


def _m3_perturb(value: float, is_integer: bool) -> float:
    if value == 0:
        return 1.0 if not is_integer else 1
    sig = int(value / (10 ** int(math.log10(abs(value))))) if value != 0 else 1
    if 1 <= abs(sig) <= 9:
        new_sig = random.randint(1, 9)
        while new_sig == sig:
            new_sig = random.randint(1, 9)
        scale = 10 ** int(math.log10(abs(value)))
        new_val = new_sig * scale
    else:
        lam = max(abs(value), 1)
        new_val = random.gauss(lam, lam * 0.3)
        new_val = max(1, new_val)
    if is_integer:
        new_val = max(1, round(new_val))
    else:
        new_val = round(new_val, len(str(value).split(".")[-1]) if "." in str(value) else 1)
    return new_val


def generate_numeric_variants(question: str, n: int = 10) -> List[str]:
    matches = list(NUMERIC_RE.finditer(question))
    if not matches:
        return []

    variants = []
    for _ in range(n * 3):
        if len(variants) >= n:
            break
        new_q = question
        offset = 0
        valid = True
        for m in matches:
            original_str = m.group(1)
            original_val = float(original_str)
            is_int = "." not in original_str
            ctx = _context_around(question, m.start())

            new_val = _m3_perturb(original_val, is_int)

            is_angle = any(kw in ctx for kw in ANGLE_KEYWORDS)
            if is_angle and not (0 < new_val <= 360):
                valid = False
                break

            is_count = any(kw in ctx for kw in COUNT_KEYWORDS)
            if is_count:
                new_val = max(1, int(new_val))

            if original_val > 0 and new_val <= 0:
                valid = False
                break

            if 0 < original_val < 1 and new_val >= 1:
                new_val = round(random.uniform(0.01, 0.99), len(original_str.split(".")[-1]) if "." in original_str else 2)

            new_str = str(int(new_val)) if is_int else str(new_val)
            start = m.start() + offset
            end = m.end() + offset
            new_q = new_q[:start] + new_str + new_q[end:]
            offset += len(new_str) - len(original_str)

        if valid and new_q != question:
            variants.append(new_q)

    seen = set()
    unique = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    return unique[:n]


# ---------------------------------------------------------------------------
# Context swap
# ---------------------------------------------------------------------------

CONTEXT_SWAPS = [
    ("ball", "stone"),
    ("car", "truck"),
    ("wire", "cable"),
    ("lamp", "bulb"),
    ("spring", "elastic cord"),
    ("satellite", "spacecraft"),
    ("train", "bus"),
    ("boat", "ship"),
    ("rocket", "projectile"),
    ("glass", "perspex"),
    ("copper", "aluminium"),
    ("water", "oil"),
]


def generate_context_variants(question: str) -> List[Tuple[str, str, str]]:
    """Return [(variant_text, original_word, replacement_word), ...]."""
    variants = []
    lowered = question.lower()
    for orig, repl in CONTEXT_SWAPS:
        if orig in lowered:
            new_q = re.sub(re.escape(orig), repl, question, flags=re.IGNORECASE)
            if new_q != question:
                variants.append((new_q, orig, repl))
    for repl, orig in CONTEXT_SWAPS:
        if orig in lowered:
            new_q = re.sub(re.escape(orig), repl, question, flags=re.IGNORECASE)
            if new_q != question:
                variants.append((new_q, orig, repl))
    seen = set()
    unique = []
    for v in variants:
        if v[0] not in seen:
            seen.add(v[0])
            unique.append(v)
    return unique[:3]


# ---------------------------------------------------------------------------
# Question-type adversarial
# ---------------------------------------------------------------------------

TYPE_SWAPS = [
    ("explain why", "show that", "explain", "derive"),
    ("explain", "describe", "explain", "describe"),
    ("define", "explain what is meant by", "definition", "explain"),
    ("calculate", "estimate", "calculation", "calculation"),
    ("calculate", "determine", "calculation", "calculation"),
    ("describe", "outline", "describe", "describe"),
    ("state", "suggest", "definition", "analyse"),
    ("derive", "show that", "derive", "derive"),
]


def generate_type_variants(question: str) -> List[Tuple[str, str, str, str, str]]:
    """Return [(variant, orig_verb, new_verb, expected_orig_type, expected_new_type), ...]."""
    variants = []
    lowered = question.lower()
    for orig_verb, new_verb, expected_orig, expected_new in TYPE_SWAPS:
        if orig_verb in lowered:
            new_q = re.sub(
                re.escape(orig_verb),
                new_verb,
                question,
                count=1,
                flags=re.IGNORECASE,
            )
            if new_q != question:
                variants.append((new_q, orig_verb, new_verb, expected_orig, expected_new))
                break
    return variants


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _normalise_formula_set(formulae: List[str]) -> set:
    normed = set()
    for f in formulae:
        f = re.sub(r"[\\()\s]", "", f.lower())
        f = re.sub(r"[^a-z0-9=+\-*/^²³]", "", f)
        if len(f) > 3:
            normed.add(f)
    return normed


def score_numeric(orig_parsed: Dict, variant_parsed: Dict) -> str:
    if not template_is_valid(orig_parsed):
        return "SKIP"
    if not template_is_valid(variant_parsed):
        return "FAIL"
    if orig_parsed["question_type"] != variant_parsed["question_type"]:
        return "FAIL"
    orig_f = _normalise_formula_set(orig_parsed["formulae"])
    var_f = _normalise_formula_set(variant_parsed["formulae"])
    if orig_f and var_f and len(orig_f & var_f) == 0:
        return "FAIL"
    return "PASS"


def score_context(orig_parsed: Dict, variant_parsed: Dict) -> str:
    if not template_is_valid(orig_parsed):
        return "SKIP"
    if not template_is_valid(variant_parsed):
        return "FAIL"
    orig_f = _normalise_formula_set(orig_parsed["formulae"])
    var_f = _normalise_formula_set(variant_parsed["formulae"])
    if orig_f and var_f and len(orig_f & var_f) == 0:
        return "FAIL"
    return "PASS"


def score_type(
    orig_parsed: Dict,
    variant_parsed: Dict,
    expected_orig: str,
    expected_new: str,
) -> str:
    if not orig_parsed["question_type"]:
        return "SKIP"
    if not variant_parsed["question_type"]:
        return "FAIL"
    orig_type = orig_parsed["question_type"]
    var_type = variant_parsed["question_type"]
    if expected_orig != expected_new and orig_type == var_type:
        return "FAIL"
    if expected_orig == expected_new and orig_type != var_type:
        return "FAIL"
    return "PASS"


# ---------------------------------------------------------------------------
# Main evaluation loop
# ---------------------------------------------------------------------------

def load_eval_data(path: Path, max_questions: int = 0) -> List[Dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if max_questions > 0:
        rows = rows[:max_questions]
    return rows


def run_eval(
    data_path: Path,
    strategies: List[str],
    n_variants: int,
    max_questions: int,
    output_path: Path,
):
    from skill.scripts.inference import generate_template

    rows = load_eval_data(data_path, max_questions)
    print(f"Loaded {len(rows)} evaluation questions from {data_path}")
    print(f"Strategies: {', '.join(strategies)}")
    print(f"Numeric variants per question: {n_variants}\n")

    results = {"numeric": [], "context": [], "type": []}
    summary = {}

    for strategy in strategies:
        tested = 0
        passed = 0
        failed = 0
        skipped = 0
        details = []

        for i, row in enumerate(rows):
            question = row.get("prompt", "")
            if len(question) < 30:
                continue

            print(f"  [{strategy}] Q{i+1}/{len(rows)}", end="\r", flush=True)

            orig_output = generate_template(question)
            orig_parsed = parse_template(orig_output)

            if strategy == "numeric":
                variants = generate_numeric_variants(question, n_variants)
                if not variants:
                    details.append({"question_idx": i, "verdict": "SKIP", "reason": "no numerics"})
                    skipped += 1
                    continue
                tested += 1
                all_pass = True
                variant_verdicts = []
                for vi, vq in enumerate(variants):
                    var_output = generate_template(vq)
                    var_parsed = parse_template(var_output)
                    verdict = score_numeric(orig_parsed, var_parsed)
                    variant_verdicts.append(verdict)
                    if verdict == "FAIL":
                        all_pass = False
                if all_pass:
                    passed += 1
                else:
                    failed += 1
                details.append({
                    "question_idx": i,
                    "n_variants": len(variants),
                    "verdicts": variant_verdicts,
                    "verdict": "PASS" if all_pass else "FAIL",
                })

            elif strategy == "context":
                variants = generate_context_variants(question)
                if not variants:
                    details.append({"question_idx": i, "verdict": "SKIP", "reason": "no applicable swaps"})
                    skipped += 1
                    continue
                tested += 1
                all_pass = True
                variant_verdicts = []
                for vq, orig_word, repl_word in variants:
                    var_output = generate_template(vq)
                    var_parsed = parse_template(var_output)
                    verdict = score_context(orig_parsed, var_parsed)
                    variant_verdicts.append({"swap": f"{orig_word}->{repl_word}", "verdict": verdict})
                    if verdict == "FAIL":
                        all_pass = False
                if all_pass:
                    passed += 1
                else:
                    failed += 1
                details.append({
                    "question_idx": i,
                    "n_variants": len(variants),
                    "verdicts": variant_verdicts,
                    "verdict": "PASS" if all_pass else "FAIL",
                })

            elif strategy == "type":
                variants = generate_type_variants(question)
                if not variants:
                    details.append({"question_idx": i, "verdict": "SKIP", "reason": "no matching verb"})
                    skipped += 1
                    continue
                tested += 1
                vq, orig_verb, new_verb, exp_orig, exp_new = variants[0]
                var_output = generate_template(vq)
                var_parsed = parse_template(var_output)
                verdict = score_type(orig_parsed, var_parsed, exp_orig, exp_new)
                if verdict == "PASS":
                    passed += 1
                else:
                    failed += 1
                details.append({
                    "question_idx": i,
                    "swap": f"{orig_verb}->{new_verb}",
                    "orig_type": orig_parsed["question_type"],
                    "variant_type": var_parsed["question_type"],
                    "expected_orig": exp_orig,
                    "expected_new": exp_new,
                    "verdict": verdict,
                })

        oa = (tested / max(tested + skipped, 1)) * 100
        aa = (passed / max(tested, 1)) * 100
        asr = ((tested - passed) / max(tested, 1)) * 100 if tested > 0 else 0

        summary[strategy] = {
            "tested": tested,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "OA": round(oa, 1),
            "AA": round(aa, 1),
            "ASR": round(asr, 1),
        }
        results[strategy] = details

    print("\n")
    print("=" * 64)
    print("  ADVERSARIAL EVALUATION REPORT")
    print("=" * 64)
    for strat, s in summary.items():
        print(f"\n  Strategy: {strat}")
        print(f"    Tested:  {s['tested']}")
        print(f"    Passed:  {s['passed']}")
        print(f"    Failed:  {s['failed']}")
        print(f"    Skipped: {s['skipped']}")
        print(f"    OA:  {s['OA']}%   AA:  {s['AA']}%   ASR: {s['ASR']}%")
    print("\n" + "=" * 64)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {"summary": summary, "details": results}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nFull report saved to {output_path}")


def main():
    ap = argparse.ArgumentParser(description="Adversarial evaluation for alevel-physics-cie")
    ap.add_argument("--data", type=str, default=str(PROJECT_ROOT / "data" / "sft" / "valid.jsonl"))
    ap.add_argument("--variants", type=int, default=10, help="Numeric variants per question")
    ap.add_argument("--strategies", type=str, default="numeric,context,type",
                    help="Comma-separated: numeric,context,type")
    ap.add_argument("--output", type=str, default=str(PROJECT_ROOT / "data" / "eval" / "adversarial_report.json"))
    ap.add_argument("--max-questions", type=int, default=0, help="0 = all")
    args = ap.parse_args()

    strats = [s.strip() for s in args.strategies.split(",") if s.strip()]
    valid_strats = {"numeric", "context", "type"}
    for s in strats:
        if s not in valid_strats:
            print(f"Unknown strategy: {s}. Valid: {valid_strats}")
            sys.exit(1)

    run_eval(
        data_path=Path(args.data),
        strategies=strats,
        n_variants=args.variants,
        max_questions=args.max_questions,
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()
