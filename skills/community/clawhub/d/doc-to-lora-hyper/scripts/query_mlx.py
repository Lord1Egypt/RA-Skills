#!/usr/bin/env python3
"""
Query a Doc-to-LoRA adapter using MLX (Apple Silicon optimized).

Requires a pre-exported adapter directory (from export_d2l_to_mlx_adapter.py).
Uses ~6GB RAM vs ~10GB for the PyTorch path.

Usage:
    python query_mlx.py --adapter-dir adapters_d2l --question "What is it about?"
    python query_mlx.py --question "Q1?,Q2?" --adapter-dir adapters_d2l
"""

import argparse
import json
import time
from pathlib import Path

from mlx_lm.utils import load
from mlx_lm.generate import generate


def main():
    parser = argparse.ArgumentParser(description="Query D2L adapter via MLX")
    parser.add_argument(
        "--question", required=True,
        help="Question(s) to ask. Comma-separated for multiple.",
    )
    parser.add_argument(
        "--adapter-dir", default="adapters_d2l",
        help="Path to exported MLX adapter directory",
    )
    parser.add_argument(
        "--model", default="mlx-community/gemma-2-2b-it",
        help="MLX model to load",
    )
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument(
        "--output-json", default=None,
        help="Write results to JSON file",
    )
    parser.add_argument(
        "--baseline", action="store_true",
        help="Also show baseline (no adapter) for comparison",
    )
    args = parser.parse_args()

    questions = [q.strip() for q in args.question.split(",")]
    results = []

    # Load model with adapter
    print(f"Loading model: {args.model}")
    print(f"Adapter: {args.adapter_dir}")
    model, tokenizer = load(args.model, adapter_path=args.adapter_dir)

    for q in questions:
        t0 = time.time()
        answer = generate(model, tokenizer, q, max_tokens=args.max_tokens, verbose=False)
        elapsed = time.time() - t0
        results.append({"question": q, "answer": answer, "time_s": round(elapsed, 2)})
        print(f"\nQ: {q}")
        print(f"A: {answer}")
        print(f"   ({elapsed:.1f}s)")

    if args.baseline:
        print("\n--- Baseline (no adapter) ---")
        base_model, base_tok = load(args.model)
        for q in questions:
            answer = generate(base_model, base_tok, q, max_tokens=args.max_tokens, verbose=False)
            print(f"\nQ: {q}")
            print(f"A (baseline): {answer}")

    if args.output_json:
        Path(args.output_json).write_text(json.dumps({"results": results}, indent=2))
        print(f"\nResults written to {args.output_json}")


if __name__ == "__main__":
    main()
