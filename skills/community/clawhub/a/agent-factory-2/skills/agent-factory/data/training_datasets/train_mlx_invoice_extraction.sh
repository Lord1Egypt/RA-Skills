#!/bin/bash
# Auto-generated MLX LoRA Training Script for invoice_extraction
# Target: Apple Silicon Unified Memory

mlx_lm.lora \
  --model "mlx-community/Llama-3.2-3B-Instruct-4bit" \
  --data "/Users/selim/Desktop/Agent Factory/tests/../skills/agent-factory/scripts/../data/training_datasets" \
  --train \
  --batch-size 4 \
  --lora-layers 16 \
  --iters 300 \
  --learning-rate 1e-4 \
  --adapter-path "/Users/selim/Desktop/Agent Factory/tests/../skills/agent-factory/scripts/../data/adapters/invoice_extraction_lora"

echo "✅ LoRA training completed for invoice_extraction"
