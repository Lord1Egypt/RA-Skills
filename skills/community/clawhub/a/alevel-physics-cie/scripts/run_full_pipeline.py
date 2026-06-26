#!/usr/bin/env python3
"""
Full pipeline: Scrape all 9702 papers → Extract questions → Build SFT → Fine-tune.

Usage:
  python scripts/run_full_pipeline.py [--skip-scrape] [--skip-train] [--teacher bootstrap|deepseek]

Steps:
  1. Scrape all available 9702 physics PDFs from cie.fraft.org
  2. Extract text-based questions from PDFs (skips MCQ Paper 1)
  3. Build SFT data with answer-template framing
  4. Fine-tune Qwen3.5-4B with MLX LoRA
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], cwd: Path = None) -> bool:
    r = subprocess.run(cmd, cwd=cwd or PROJECT_ROOT)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(description="Run full scrape → extract → SFT → train pipeline")
    ap.add_argument("--skip-scrape", action="store_true", help="Use existing data/raw PDFs")
    ap.add_argument("--skip-train", action="store_true", help="Stop after building SFT data")
    ap.add_argument("--teacher", choices=["bootstrap", "deepseek"], default="bootstrap",
                    help="Teacher for SFT: bootstrap (template) or deepseek (API)")
    args = ap.parse_args()

    # 1. Scrape
    if not args.skip_scrape:
        print("\n=== Step 1: Scraping 9702 papers from cie.fraft.org ===\n")
        if not run([sys.executable, "-m", "scraper.scrape_9702"]):
            print("Scrape failed. Try: python -m scraper.scrape_fraft")
            sys.exit(1)
    else:
        print("Skipping scrape (--skip-scrape)")

    # 2. Extract questions
    print("\n=== Step 2: Extracting questions from PDFs ===\n")
    if not run([sys.executable, "-m", "scraper.extract_questions"]):
        sys.exit(1)

    q_path = PROJECT_ROOT / "data" / "questions.jsonl"
    if not q_path.exists() or q_path.stat().st_size == 0:
        print("No questions extracted. Check data/raw for PDFs.")
        sys.exit(1)

    # 3. Build SFT
    print("\n=== Step 3: Building SFT data (answer-template framing) ===\n")
    if not run([sys.executable, "scripts/build_sft.py", "--teacher-mode", args.teacher]):
        sys.exit(1)

    if args.skip_train:
        print("\nPipeline stopped (--skip-train). Run: bash scripts/train.sh")
        return

    # 4. Fine-tune
    print("\n=== Step 4: Fine-tuning Qwen3.5-4B with MLX LoRA ===\n")
    if not run(["bash", "scripts/train.sh"]):
        print("Train failed. Run manually: mlx_lm.lora --config configs/train_qwen35_4b.yaml --train")
        sys.exit(1)

    print("\n=== Pipeline complete. Adapters saved to ./adapters ===")


if __name__ == "__main__":
    main()
