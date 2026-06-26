#!/usr/bin/env python3
"""
Inference script for the A-Level Physics CIE answer template model.

Includes a self-verification wrapper (generate_template_verified) that
critiques the initial output and re-prompts when structural or physics
issues are detected — an agentic critical-thinking loop at inference time.

Usage:
  python skill/scripts/inference.py "Your physics question here"
  python skill/scripts/inference.py --verified "Your physics question here"
  python skill/scripts/inference.py --interactive
  python skill/scripts/inference.py --file questions.txt

As a library:
  from skill.scripts.inference import generate_template, generate_template_verified
  print(generate_template_verified("Define specific heat capacity."))
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ADAPTER_PATH = PROJECT_ROOT / "adapters"
DEFAULT_BASE_MODEL = "Qwen/Qwen3-4B-MLX-4bit"

_model = None
_tokenizer = None


# ---------------------------------------------------------------------------
# Template parser (shared with adversarial_eval)
# ---------------------------------------------------------------------------

_SECTION_RE = re.compile(
    r"^##\s+(Question type|Given|Required|Formulae\s*/?\s*principles|Answer frame|Check)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

VALID_QUESTION_TYPES = {
    "calculation", "definition", "explain", "describe",
    "derive", "analyse", "practical",
}

QUESTION_TYPE_KEYWORDS = {
    "calculation": r"\bcalculate\b|\bdetermine\b|\bfind\b|\bhow many\b|\bhow much\b",
    "definition": r"\bdefine\b|\bstate what is meant\b|\bwhat is meant by\b",
    "explain":    r"\bexplain\b|\bwhy\b|\baccount for\b",
    "describe":   r"\bdescribe\b|\boutline\b",
    "derive":     r"\bderive\b|\bshow that\b|\bprove\b",
    "analyse":    r"\bcompare\b|\bcomment\b|\bdiscuss\b|\bsuggest\b|\bevaluate\b",
    "practical":  r"\bexperiment\b|\bprocedure\b|\bmeasurement\b|\buncertainty\b|\berror bar\b",
}

FORMULA_TOPIC_PATTERNS = {
    "kinematics":     (r"\bvelocity\b|\bacceleration\b|\bdisplacement\b|\bspeed\b|\bthrown\b|\bprojectile\b",
                       ["v = u + at", "s = ut + 0.5at^2", "v^2 = u^2 + 2as"]),
    "forces":         (r"\bforce\b|\bweight\b|\btension\b|\bmoment\b|\btorque\b|\bnewton\b",
                       ["F = ma", "moment = Fd", "W = mg"]),
    "energy":         (r"\benergy\b|\bwork\b|\bpower\b|\bkinetic\b|\bpotential\b",
                       ["KE = 0.5mv^2", "PE = mgh", "P = E/t", "W = Fd"]),
    "electricity":    (r"\bcurrent\b|\bvoltage\b|\bresistance\b|\bcircuit\b|\be\.m\.f\b|\binternal resistance\b",
                       ["V = IR", "P = IV", "E = V + Ir"]),
    "waves":          (r"\bwave\b|\bfrequency\b|\bwavelength\b|\bdiffraction\b|\binterference\b",
                       ["v = f*lambda", "n*lambda = d*sin(theta)"]),
    "thermal":        (r"\bheat\b|\btemperature\b|\bspecific heat\b|\blatent\b|\bgas\b|\bpressure\b",
                       ["Q = mc*delta_T", "Q = mL", "pV = nRT"]),
    "quantum":        (r"\bphoton\b|\bphotoelectric\b|\bde broglie\b|\bquantum\b|\benergy level\b",
                       ["E = hf", "hf = phi + KE_max", "lambda = h/p"]),
    "nuclear":        (r"\bdecay\b|\bhalf-life\b|\bnucleus\b|\bisotope\b|\bbinding energy\b|\bfission\b|\bfusion\b",
                       ["N = N0*e^(-lambda*t)", "t_half = ln2/lambda", "E = mc^2"]),
    "fields":         (r"\bgravitational field\b|\belectric field\b|\bmagnetic\b|\bflux\b|\binduction\b",
                       ["F = kQq/r^2", "phi = -GM/r", "F = BIl", "emf = -d(N*phi)/dt"]),
    "circular_motion": (r"\bcircular\b|\bcentripetal\b|\borbit\b|\bangular\b",
                        ["F = mv^2/r", "omega = 2*pi*f"]),
    "shm":            (r"\boscillat\b|\bsimple harmonic\b|\bperiod\b.*\bspring\b|\bpendulum\b",
                       ["x = x0*sin(omega*t)", "T = 2*pi*sqrt(m/k)"]),
}


def parse_template(text: str) -> Dict[str, object]:
    result = {
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
    splits = _SECTION_RE.split(text)
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
                items = [
                    ln.strip().lstrip("-•0123456789.) ").strip()
                    for ln in body.splitlines() if ln.strip()
                ]
                result[current_key] = items
    return result


# ---------------------------------------------------------------------------
# Self-verification critics
# ---------------------------------------------------------------------------

def _detect_issues(question: str, parsed: Dict) -> List[str]:
    """Return a list of plain-English issue descriptions found in the template."""
    issues = []

    # 1. Missing sections
    if not parsed["question_type"]:
        issues.append("Missing '## Question type' section.")
    if not parsed["formulae"] and not parsed["answer_frame"]:
        issues.append("Missing both '## Formulae / principles' and '## Answer frame' sections.")
    if not parsed["given"]:
        issues.append("Missing '## Given' section.")

    if issues:
        return issues

    # 2. Question-type plausibility
    q_type = parsed["question_type"] or ""
    normalised_type = q_type.split("/")[0].strip()
    if normalised_type and normalised_type not in VALID_QUESTION_TYPES:
        best_guess = _infer_type_from_question(question)
        issues.append(
            f"Question type '{q_type}' is not a standard CIE type. "
            f"Expected one of: {', '.join(sorted(VALID_QUESTION_TYPES))}. "
            f"Based on the question wording, '{best_guess}' seems more appropriate."
        )

    # 3. Type-keyword mismatch
    inferred = _infer_type_from_question(question)
    if normalised_type and inferred and normalised_type != inferred:
        if not (normalised_type in ("definition", "explain") and inferred in ("definition", "explain")):
            issues.append(
                f"Question type '{normalised_type}' may not match the question. "
                f"The question wording suggests '{inferred}'."
            )

    # 4. Formula relevance
    if parsed["formulae"]:
        topic_matched = False
        q_lower = question.lower()
        for topic, (pattern, _expected_formulas) in FORMULA_TOPIC_PATTERNS.items():
            if re.search(pattern, q_lower):
                topic_matched = True
                break
        formulae_text = " ".join(parsed["formulae"]).lower()
        if topic_matched and len(formulae_text) < 5:
            issues.append("Formulae section is present but appears empty or too short for a calculation-type question.")

    # 5. Calculation type should have formulae
    if normalised_type == "calculation" and not parsed["formulae"]:
        issues.append("Question type is 'calculation' but no formulae are listed.")

    # 6. Numeric values in question should appear in Given
    numbers_in_q = re.findall(r"(?<![A-Za-z])(\d+\.?\d*)", question)
    if numbers_in_q and not parsed["given"]:
        issues.append(
            f"The question contains numeric values ({', '.join(numbers_in_q[:3])}) "
            "but the '## Given' section is empty."
        )

    # 7. Answer frame should have at least 2 steps
    if parsed["answer_frame"] and len(parsed["answer_frame"]) < 2:
        issues.append("Answer frame has fewer than 2 steps; consider expanding.")

    return issues


def _infer_type_from_question(question: str) -> Optional[str]:
    q_lower = question.lower()
    for q_type, pattern in QUESTION_TYPE_KEYWORDS.items():
        if re.search(pattern, q_lower):
            return q_type
    return None


def _build_correction_prompt(question: str, first_output: str, issues: List[str]) -> str:
    issue_list = "\n".join(f"- {issue}" for issue in issues)
    return (
        f"You previously generated the following answer template for a CIE 9702 Physics question:\n\n"
        f"Question: {question}\n\n"
        f"Your template:\n{first_output}\n\n"
        f"Issues found:\n{issue_list}\n\n"
        f"Please regenerate the answer template, fixing all listed issues. "
        f"Use the standard format: ## Question type, ## Given, ## Required, "
        f"## Formulae / principles, ## Answer frame, ## Check."
    )


# ---------------------------------------------------------------------------
# Model loading and generation
# ---------------------------------------------------------------------------

def load_model(
    base_model: str = DEFAULT_BASE_MODEL,
    adapter_path: Optional[str] = None,
):
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    from mlx_lm import load

    ap = str(adapter_path or DEFAULT_ADAPTER_PATH)
    _model, _tokenizer = load(base_model, adapter_path=ap)
    return _model, _tokenizer


def _generate_raw(
    prompt_text: str,
    max_tokens: int = 400,
    base_model: str = DEFAULT_BASE_MODEL,
    adapter_path: Optional[str] = None,
) -> str:
    from mlx_lm import generate

    model, tokenizer = load_model(base_model, adapter_path)
    return generate(model, tokenizer, prompt=prompt_text, max_tokens=max_tokens)


def _apply_chat(question: str) -> str:
    _, tokenizer = load_model()
    messages = [{"role": "user", "content": question}]
    return tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )


def generate_template(
    question: str,
    max_tokens: int = 400,
    base_model: str = DEFAULT_BASE_MODEL,
    adapter_path: Optional[str] = None,
) -> str:
    """Single-pass generation (no self-verification)."""
    load_model(base_model, adapter_path)
    prompt = _apply_chat(question)
    return _generate_raw(prompt, max_tokens, base_model, adapter_path)


def generate_template_verified(
    question: str,
    max_tokens: int = 400,
    max_retries: int = 2,
    base_model: str = DEFAULT_BASE_MODEL,
    adapter_path: Optional[str] = None,
    verbose: bool = False,
) -> Tuple[str, Dict]:
    """
    Agentic self-verification loop:
      1. Generate answer template
      2. Parse and critique it
      3. If issues found, re-prompt with correction instructions
      4. Return best output + metadata

    Returns (template_text, metadata) where metadata contains:
      - attempts: number of generation passes
      - issues_found: list of issues detected on each pass
      - improved: whether the final output is from a correction pass
    """
    load_model(base_model, adapter_path)
    meta = {"attempts": 0, "issues_found": [], "improved": False}

    best_output = None
    best_issues = None

    for attempt in range(1 + max_retries):
        meta["attempts"] = attempt + 1

        if attempt == 0:
            prompt = _apply_chat(question)
        else:
            correction = _build_correction_prompt(question, best_output, best_issues)
            prompt = _apply_chat(correction)

        output = _generate_raw(prompt, max_tokens, base_model, adapter_path)
        parsed = parse_template(output)
        issues = _detect_issues(question, parsed)
        meta["issues_found"].append(issues)

        if verbose and issues:
            print(f"  [verify] attempt {attempt+1}: {len(issues)} issue(s)", file=sys.stderr)
            for iss in issues:
                print(f"    - {iss}", file=sys.stderr)

        if not issues:
            if attempt > 0:
                meta["improved"] = True
            return output, meta

        if best_output is None or len(issues) < len(best_issues):
            best_output = output
            best_issues = issues

    if meta["attempts"] > 1:
        final_parsed = parse_template(best_output)
        final_issues = _detect_issues(question, final_parsed)
        if len(final_issues) < len(meta["issues_found"][0]):
            meta["improved"] = True

    return best_output, meta


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="CIE 9702 Physics answer template generator")
    ap.add_argument("question", nargs="?", help="Physics question text")
    ap.add_argument("--file", type=str, help="File with one question per line")
    ap.add_argument("--interactive", action="store_true", help="Interactive mode")
    ap.add_argument("--verified", action="store_true",
                    help="Use self-verification (agentic critical thinking)")
    ap.add_argument("--max-retries", type=int, default=2,
                    help="Max correction passes for --verified mode")
    ap.add_argument("--verbose", action="store_true",
                    help="Print verification details to stderr")
    ap.add_argument("--max-tokens", type=int, default=400)
    ap.add_argument("--base-model", type=str, default=DEFAULT_BASE_MODEL)
    ap.add_argument("--adapter-path", type=str, default=str(DEFAULT_ADAPTER_PATH))
    args = ap.parse_args()

    gen_fn = generate_template
    gen_kwargs = dict(max_tokens=args.max_tokens, base_model=args.base_model, adapter_path=args.adapter_path)

    if args.verified:
        def gen_fn(q, **kw):
            output, meta = generate_template_verified(
                q, max_retries=args.max_retries, verbose=args.verbose, **kw
            )
            if args.verbose:
                print(f"  [verify] {meta['attempts']} attempt(s), improved={meta['improved']}", file=sys.stderr)
            return output

    if args.interactive:
        mode = "verified" if args.verified else "single-pass"
        print(f"A-Level Physics CIE — Answer Template Generator ({mode})")
        print("Type a question and press Enter. Ctrl+C to exit.\n")
        while True:
            try:
                q = input("Q: ").strip()
                if not q:
                    continue
                print()
                print(gen_fn(q, **gen_kwargs))
                print()
            except (KeyboardInterrupt, EOFError):
                print("\nBye.")
                break
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            questions = [line.strip() for line in f if line.strip()]
        for i, q in enumerate(questions, 1):
            print(f"\n{'='*60}\nQ{i}: {q}\n{'='*60}")
            print(gen_fn(q, **gen_kwargs))
    elif args.question:
        print(gen_fn(args.question, **gen_kwargs))
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
