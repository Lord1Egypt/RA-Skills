#!/bin/bash
# Fine-tune Qwen3.5-4B with MLX LoRA for learning framework generation
set -e
cd "$(dirname "$0")/.."

if ! python3 -m mlx_lm.lora --help >/dev/null 2>&1; then
  echo "python3 -m mlx_lm.lora is not available. Install: python3 -m pip install mlx mlx-lm"
  exit 1
fi

if [[ ! -f data/sft/train.jsonl ]] || [[ ! -f data/sft/valid.jsonl ]]; then
  echo "Missing data/sft/train.jsonl or valid.jsonl. Run: python scripts/build_sft.py --teacher-mode bootstrap"
  exit 1
fi

echo "Starting LoRA fine-tuning..."
python3 -m mlx_lm.lora --config configs/train_qwen35_4b.yaml --train

echo "Done. Adapters saved to ./adapters"
