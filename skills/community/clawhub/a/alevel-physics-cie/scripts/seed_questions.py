#!/usr/bin/env python3
"""
Create seed data/questions.jsonl for testing the pipeline without scraping.
Useful when cie.fraft.org is unavailable or for quick iteration.
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

SEED_QUESTIONS = [
    {
        "source": "seed",
        "paper": "sample",
        "question_id": "1",
        "text": "A ball is thrown vertically upwards. State the direction of its acceleration at the highest point of its motion.",
        "marks": 1,
    },
    {
        "source": "seed",
        "paper": "sample",
        "question_id": "2",
        "text": "Define the moment of a force about a point.",
        "marks": 2,
    },
    {
        "source": "seed",
        "paper": "sample",
        "question_id": "3",
        "text": "A wire of length L and cross-sectional area A has resistance R. The wire is stretched to double its length. Assuming the volume of the wire remains constant, derive an expression for the new resistance in terms of R.",
        "marks": 3,
    },
    {
        "source": "seed",
        "paper": "sample",
        "question_id": "4",
        "text": "Explain why the internal resistance of a cell causes the terminal potential difference to decrease when the current drawn from the cell increases.",
        "marks": 3,
    },
    {
        "source": "seed",
        "paper": "sample",
        "question_id": "5",
        "text": "Describe the photoelectric effect and state two observations that cannot be explained by the wave theory of light.",
        "marks": 4,
    },
]


def main():
    out_path = PROJECT_ROOT / "data" / "questions.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for q in SEED_QUESTIONS:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    print(f"Wrote {len(SEED_QUESTIONS)} seed questions to {out_path}")


if __name__ == "__main__":
    main()
