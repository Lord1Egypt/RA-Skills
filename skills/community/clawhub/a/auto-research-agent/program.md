# Research Program - Baseline

## Baseline Status
- Model: GPT-like transformer (3 layers, 4 heads, 128 dim)
- Optimizer: AdamW (lr=1e-3)
- Evaluation: val_loss
- Baseline Score: 2.500

## Research Goal
Minimize validation loss through architectural and hyperparameter improvements.

## Modifiable Range
- Model architecture (layers, heads, hidden_dim, vocab_size)
- Optimizer (learning_rate, betas, weight_decay)
- Training parameters (batch_size, seq_len)
- Regularization (dropout)

## Constraints
- Training time: 5 minutes fixed
- Single GPU
- Only modify train.py

## Current Focus
Start with learning rate tuning, then try architectural changes.

## Quick Commands
```bash
# Run single experiment
python train.py

# Check current results
cat experiments.md
```
