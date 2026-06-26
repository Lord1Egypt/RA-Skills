#!/usr/bin/env python3
"""
Build SFT data for answer-template generation from extracted 9702 questions.

Two modes are supported:
  - deepseek: synthesize higher-quality templates using the question + mark scheme context
  - bootstrap: create heuristic templates without external APIs
"""

import json
import os
import random
import re
from pathlib import Path
from typing import Optional

import pdfplumber

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

ANSWER_TEMPLATE_SYSTEM = """You are a Cambridge International A-Level Physics (9702) tutor.
Given a question and optional mark-scheme context, write an answer template that teaches a student how to structure the response without fully solving every step.

Use this exact format:
## Question type
[calculation / definition / explain / describe / derive / analyse / practical]

## Given
- Key quantities, conditions, diagrams, or data already present in the question

## Required
- What the student must find, state, explain, derive, or comment on

## Formulae / principles
- Relevant laws, equations, or physics principles

## Answer frame
1. First idea or setup
2. Intermediate step(s)
3. Final statement / conclusion

## Check
- Unit/sign/direction/significant-figure/logic checks

Keep it concise and specific to the question. Do not mention the mark scheme directly."""

QUESTION_TYPE_RULES = [
    ("derive", r"\bderive\b|\bshow that\b"),
    ("definition", r"\bdefine\b|\bstate what is meant by\b"),
    ("explain", r"\bexplain why\b|\bexplain\b"),
    ("describe", r"\bdescribe\b"),
    ("analyse", r"\bcompare\b|\bcomment\b|\bdiscuss\b|\bsuggest\b"),
    ("practical", r"\bexperiment\b|\bprocedure\b|\bmeasurement\b"),
]


def load_config() -> dict:
    cfg_path = PROJECT_ROOT / "config.yaml"
    if not cfg_path.exists():
        return {}
    import yaml

    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def iter_questions(path: Path):
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def infer_question_type(question: str) -> str:
    lowered = question.lower()
    for label, pattern in QUESTION_TYPE_RULES:
        if re.search(pattern, lowered):
            return label
    return "calculation" if re.search(r"\bcalculate\b|\bdetermine\b|\bfind\b", lowered) else "explain"


def clean_question_text(question: str) -> str:
    question = re.sub(r"For Examiner[’']?s Use", " ", question, flags=re.I)
    question = re.sub(r"\.{6,}", " ", question)
    question = re.sub(r"\b9702/\d{2}/[A-Z]/[A-Z]/\d{2,4}\b", " ", question)
    question = re.sub(r"\b(?:elementary charge|Planck constant|Avogadro constant|Boltzmann constant)\b.*", " ", question, flags=re.I)
    question = re.sub(r"\s+", " ", question).strip()
    return question


def is_usable_question(question: str) -> bool:
    if len(question) < 60:
        return False
    if question.count(".") > 15:
        return False
    if re.search(r"\b(?:elementary charge|Planck constant|Avogadro constant|gravitational constant)\b", question, re.I):
        return False
    if re.fullmatch(r"[\d\s\W]+", question):
        return False
    letters = sum(ch.isalpha() for ch in question)
    if letters / max(len(question), 1) < 0.35:
        return False
    return True


def extract_given_items(question: str) -> list[str]:
    items = []
    for match in re.finditer(r"\b([A-Za-z][A-Za-z0-9_/-]*)\s*=\s*([-+]?\d+(?:\.\d+)?)", question):
        items.append(f"{match.group(1)} = {match.group(2)}")
    if re.search(r"\bdiagram\b|\bfigure\b|\bgraph\b|\btable\b", question, re.I):
        items.append("Use the diagram/graph/table information provided")
    if not items:
        items.append("Extract the stated quantities and physical conditions from the question")
    return items[:4]


def extract_required(question: str) -> str:
    for trigger in ["calculate", "determine", "find", "show that", "derive", "define", "explain", "describe", "comment on", "suggest"]:
        match = re.search(rf"\b{re.escape(trigger)}\b(.+?)(?:[.;]|$)", question, re.I)
        if match:
            return f"{trigger} {match.group(1).strip()}"
    return "Answer the specific task asked in the question"


def formula_hints(question: str, question_type: str) -> list[str]:
    hints = []
    lowered = question.lower()
    patterns = [
        ("motion/kinematics equations", r"\bvelocity\b|\bacceleration\b|\bdisplacement\b"),
        ("Newton's laws and force balance", r"\bforce\b|\bweight\b|\bmass\b|\btension\b"),
        ("moment / torque relations", r"\bmoment\b|\btorque\b"),
        ("electrical circuit relations", r"\bcurrent\b|\bvoltage\b|\bresistance\b|\bpower\b"),
        ("energy conservation / work done", r"\benergy\b|\bwork\b|\bpower\b"),
        ("wave relations", r"\bwave\b|\bfrequency\b|\bwavelength\b"),
        ("thermal / gas laws", r"\bpressure\b|\btemperature\b|\bgas\b"),
        ("quantum / photoelectric principles", r"\bphotoelectric\b|\bphoton\b|\bquantum\b"),
    ]
    for label, pattern in patterns:
        if re.search(pattern, lowered):
            hints.append(label)
    if question_type == "definition":
        hints.append("Use the syllabus definition precisely")
    if question_type in {"explain", "describe", "analyse"}:
        hints.append("Link observations to physics reasoning")
    return hints[:4] or ["Choose the principle or equation that directly matches the asked quantity"]


def bootstrap_answer_template(question: str) -> str:
    question_type = infer_question_type(question)
    given_items = extract_given_items(question)
    required = extract_required(question)
    formulae = formula_hints(question, question_type)

    if question_type == "definition":
        frame = [
            "Start with the formal physics definition",
            "State any quantities involved using correct terminology",
            "Keep the wording precise and concise",
        ]
        checks = ["Use standard Cambridge wording and include units only if part of the definition"]
    elif question_type in {"explain", "describe", "analyse"}:
        frame = [
            "Identify the relevant physics idea",
            "Link the situation/data to that idea step by step",
            "End with the exact conclusion that answers the prompt",
        ]
        checks = ["Ensure each statement is causally linked and not just descriptive filler"]
    else:
        frame = [
            "List the known quantities and the target quantity",
            "Choose the governing equation or principle and rearrange if needed",
            "Substitute values carefully and present the final result clearly",
        ]
        checks = ["Check units, sign/direction, and whether the answer magnitude is reasonable"]

    return "\n".join(
        [
            "## Question type",
            question_type,
            "",
            "## Given",
            *[f"- {item}" for item in given_items],
            "",
            "## Required",
            f"- {required}",
            "",
            "## Formulae / principles",
            *[f"- {item}" for item in formulae],
            "",
            "## Answer frame",
            *[f"{idx}. {step}" for idx, step in enumerate(frame, start=1)],
            "",
            "## Check",
            *[f"- {item}" for item in checks],
        ]
    )


def load_markscheme_excerpt(cache: dict[str, str], filename: Optional[str]) -> str:
    if not filename:
        return ""
    if filename in cache:
        return cache[filename]

    path = PROJECT_ROOT / "data" / "raw" / filename
    if not path.exists():
        cache[filename] = ""
        return ""

    try:
        with pdfplumber.open(path) as pdf:
            pages = []
            for page in pdf.pages[:4]:
                text = page.extract_text()
                if text:
                    pages.append(text)
    except Exception:
        cache[filename] = ""
        return ""

    excerpt = re.sub(r"\s+", " ", " ".join(pages))[:3500]
    cache[filename] = excerpt
    return excerpt


def generate_via_deepseek(question: str, markscheme_excerpt: str, client: "OpenAI") -> Optional[str]:
    user_prompt = f"Question:\n{question}\n"
    if markscheme_excerpt:
        user_prompt += f"\nMark scheme context:\n{markscheme_excerpt}\n"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": ANSWER_TEMPLATE_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=400,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[WARN] API error: {exc}")
        return None


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--teacher-mode", choices=["deepseek", "bootstrap"], default="bootstrap")
    ap.add_argument("--max-samples", type=int, default=0, help="0 = all")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    cfg = load_config()
    sft_cfg = cfg.get("sft", {})
    val_ratio = sft_cfg.get("val_ratio", 0.1)
    max_len = sft_cfg.get("max_question_length", 2500)

    questions_path = PROJECT_ROOT / "data" / "questions.jsonl"
    out_dir = PROJECT_ROOT / "data" / "sft"
    out_dir.mkdir(parents=True, exist_ok=True)

    questions = list(iter_questions(questions_path))
    if not questions:
        print("No questions in data/questions.jsonl. Run scraper and extract_questions first.")
        return

    if args.max_samples:
        questions = questions[: args.max_samples]
    random.seed(args.seed)
    random.shuffle(questions)

    n_val = max(1, int(len(questions) * val_ratio))
    val_set = set(range(len(questions) - n_val, len(questions)))
    train_data, valid_data = [], []

    client = None
    if args.teacher_mode == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("DEEPSEEK_API_KEY not set. Use --teacher-mode bootstrap for testing.")
            return
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    markscheme_cache: dict = {}
    if args.teacher_mode == "deepseek":
        ms_files = set(q.get("markscheme_pdf") for q in questions if q.get("markscheme_pdf"))
        print(f"Pre-caching {len(ms_files)} mark scheme PDFs...", flush=True)
        for ms in sorted(ms_files):
            load_markscheme_excerpt(markscheme_cache, ms)
        cached = sum(1 for v in markscheme_cache.values() if v)
        print(f"  Cached {cached}/{len(ms_files)} mark schemes with text", flush=True)

    processed = 0
    skipped = 0
    api_ok = 0
    api_fail = 0
    for i, question_row in enumerate(questions):
        question = clean_question_text((question_row.get("text") or "").strip())
        if not is_usable_question(question):
            skipped += 1
            continue
        question = question[:max_len]
        markscheme_excerpt = load_markscheme_excerpt(markscheme_cache, question_row.get("markscheme_pdf"))

        completion = bootstrap_answer_template(question)
        if args.teacher_mode == "deepseek" and client:
            generated = generate_via_deepseek(question, markscheme_excerpt, client)
            if generated:
                completion = generated
                api_ok += 1
            else:
                api_fail += 1

        row = {
            "prompt": question,
            "completion": completion,
            "metadata": {
                "source": question_row.get("source"),
                "question_id": question_row.get("question_id"),
                "paper_no": question_row.get("paper_no"),
                "variant": question_row.get("variant"),
                "markscheme_pdf": question_row.get("markscheme_pdf"),
            },
        }
        if i in val_set:
            valid_data.append(row)
        else:
            train_data.append(row)

        processed += 1
        if processed % 25 == 0:
            print(f"  [{processed}] api_ok={api_ok} api_fail={api_fail} skipped={skipped}", flush=True)

    train_path = out_dir / "train.jsonl"
    valid_path = out_dir / "valid.jsonl"
    with open(train_path, "w", encoding="utf-8") as f:
        for row in train_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(valid_path, "w", encoding="utf-8") as f:
        for row in valid_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(train_data)} train and {len(valid_data)} valid examples to {out_dir}")


if __name__ == "__main__":
    main()
