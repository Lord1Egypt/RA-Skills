---
name: deepspeed-finetune
description: Fine-tune large language models using DeepSpeed on local or remote GPUs.
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - deepspeed
        - sshpass
    emoji: "⚡"
    homepage: https://github.com/deepspeedai/deepspeed-skills/tree/main/openclaw/deepspeed-finetune
---

# DeepSpeed Fine-tuning Skill

This skill enables efficient model fine-tuning using DeepSpeed with various optimization strategies.

## Prerequisites

- Python 3.8+
- GPU(s) or accelerator(s) with DeepSpeed-supported backend (CUDA, ROCm, Intel XPU, etc.)
- DeepSpeed: `pip install deepspeed`
- Transformers, Datasets, PEFT (for LoRA support)
- sshpass: `sudo apt-get install sshpass` (for remote training)

## Plan Selection Workflow

**Never auto-select a plan.** List viable options based on user hardware and requirements, and let the user decide.

### Step 1: Gather Information

Confirm the following with the user:
- **Target model**: Model name and parameter count (e.g., Qwen2.5-7B)
- **Hardware environment**:
  - GPU VRAM x count (e.g., "single 24GB GPU")
  - CPU core count
  - RAM size
  - Free disk space
  - NVMe SSD availability (affects ZeRO NVMe offload)
- **Training goal**: Full fine-tuning or parameter-efficient? Dataset size? Expected quality?
- **Budget/time constraints**: Acceptable training duration?

If the user only provides an SSH or remote machine address, connect first and auto-detect hardware (`nvidia-smi`, `free -h`, `df -h`, `nproc`).

### Step 2: Evaluate Feasibility

Estimate VRAM requirements based on model size (bf16):

| Params | Model Weights (bf16) | + Adam Optimizer + Gradients |
|--------|---------------------|----------------------------|
| 0.5B | ~1 GB | ~5 GB |
| 1.5B | ~3 GB | ~15 GB |
| 3B | ~6 GB | ~30 GB |
| 7B | ~14 GB | ~70 GB |
| 14B | ~28 GB | ~140 GB |
| 32B | ~64 GB | ~320 GB |
| 72B | ~144 GB | ~720 GB |

**Breakdown**: Adam optimizer stores 2 fp32 state tensors (momentum + variance) = 8 bytes/param. Gradients = 2 bytes/param (bf16). Total approx. 10 bytes/param (5x model weight size).

**Activation memory**: Depends on sequence length and batch size, not model params alone.
- Formula: `activation approx. 34 x seq_len x hidden_size x batch_size x bytes_per_element`
- Example: 7B model (hidden=4096), seq_len=2048, batch_size=4, bf16 -> ~1.5 GB per layer; ~60 GB total (can dominate VRAM)
- Gradient checkpointing reduces this by ~80% (recomputes instead of storing), but adds ~20% compute overhead
- **Rule of thumb**: if seq_len x batch_size > 8192, activation memory likely exceeds model weights

**LoRA/QLoRA**: VRAM depends on rank, target modules, and layer dimensions — not directly proportional to total model params. See [references/lora_guide.md](references/lora_guide.md) for LoRA-specific memory estimation.

### Step 2.5: Activation Checkpointing

If VRAM is tight, activation checkpointing is the most impactful knob — it can reduce activation memory by ~80%.

**How it works**: Instead of storing all intermediate activations for backprop, only save checkpoints at select layers. Remaining activations are recomputed during backward pass. Trades compute for memory.

**Two ways to enable:**

1. **HF Trainer flag** (simplest, works out of the box):
```bash
python scripts/ds_train.py --gradient_checkpointing ...
```

2. **DeepSpeed config** (fine-grained control):
```json
{
  "activation_checkpointing": {
    "partition_activations": true,
    "cpu_checkpointing": true,
    "contiguous_memory_optimization": true,
    "number_checkpoints": 4
  }
}
```

| Option | Effect | When to use |
|--------|--------|-------------|
| `partition_activations` | Shard checkpoints across model-parallel GPUs | Multi-GPU with model parallelism |
| `cpu_checkpointing` | Store checkpoints in CPU RAM instead of GPU | GPU memory very tight |
| `contiguous_memory_optimization` | Reduce memory fragmentation | Large models, many checkpoints |
| `number_checkpoints` | Control checkpoint frequency (fewer = less VRAM, more compute) | Tune based on VRAM budget |

### Step 3: List Options

Based on the VRAM assessment, list all viable approaches. Example:

```
Based on your hardware (single 24GB GPU, 64GB RAM, 500GB disk),
Qwen2.5-7B has these training options:

Option A: LoRA Fine-tuning (Recommended)
  - VRAM needed: ~22 GB
  - Speed: Fast
  - Quality: Good for instruction alignment, style adaptation
  - Trainable params: ~20M (0.4% of total)

Option B: QLoRA Fine-tuning (Saves VRAM)
  - VRAM needed: ~12 GB
  - Speed: Medium (quantization/dequantization overhead)
  - Quality: Slightly below LoRA, but gap is small

Option C: Full Fine-tuning (Not feasible)
  - VRAM needed: ~56 GB (exceeds 24GB)
  - Requires ZeRO-2 + CPU offload, or larger GPU

Which option do you prefer?
```

### Step 4: Hardware Insufficient? Make Recommendations

If no plan is viable on current hardware, recommend specs using generic hardware metrics (no brand names):

```
You want to fully fine-tune a 7B model, but current hardware (single 24GB GPU) is insufficient.
Recommended hardware specs:

Minimum:
  - GPU: single 80GB VRAM
  - CPU: 16+ cores
  - RAM: 128 GB+
  - Disk: 200 GB+ free space

Recommended:
  - GPU: 2x 80GB VRAM (ZeRO-2 doubles training speed)
  - CPU: 32+ cores
  - RAM: 256 GB+
  - Disk: 500 GB+ free space

Alternatively, use LoRA — 24GB VRAM is sufficient for 7B models.
```

### Key Principles

- **Never auto-select and start training** — always list options and wait for user confirmation
- **Recommend but don't decide** — say "I recommend Option A because..." but let the user choose
- **Use generic hardware metrics** — VRAM in GB, GPU count, CPU cores, RAM in GB, disk in GB. No brand names.
- **Leave VRAM headroom** — recommend at least 20% buffer to avoid OOM
- **If user picks an infeasible option, warn them clearly** rather than silently switching

## Core Capabilities

### 1. Training Configuration

Generate DeepSpeed ZeRO configurations:

```python
from scripts.generate_ds_config import generate_zero_config

# ZeRO Stage 2 with optimizer offloading
config = generate_zero_config(
    zero_stage=2,
    offload_optimizer=True,
    offload_device="nvme",
    nvme_path="/local_nvme"
)
```

### 2. Training Launch

Use the training launcher script:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path data/my_dataset \
  --output_dir ./outputs \
  --deepspeed assets/ds_config_zero2.json \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4 \
  --learning_rate 2e-5 \
  --lora_r 16 \
  --lora_alpha 32
```

### 3. LoRA/QLoRA Integration

For parameter-efficient fine-tuning:

```python
# LoRA config is auto-generated based on arguments
peft_config = {
    "peft_type": "LORA",
    "r": 16,
    "lora_alpha": 32,
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM"
}
```

### 4. Multi-GPU Training

Use the `deepspeed` launcher for multi-GPU training (recommended over `torchrun`):

```bash
# Multi-GPU on single node
deepspeed --num_gpus=4 scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --deepspeed assets/ds_config_zero3.json \
  ...

# Multi-node
deepspeed --hostfile hosts.txt scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --deepspeed assets/ds_config_zero3.json \
  ...
```

### 5. Training Monitoring

Monitor training progress:

```python
from scripts.monitor_training import TrainingMonitor

monitor = TrainingMonitor(log_dir="./outputs")
monitor.plot_loss()
monitor.get_latest_checkpoint()
```

### 6. Early Stopping

Automatically monitors eval loss and stops training early when there's no improvement across consecutive evaluations, then loads the best checkpoint.

**Parameters:**
- `--early_stopping_patience` — How many consecutive evals without improvement to tolerate. Set to 0 to disable (default). Recommended: 3-10.
- `--early_stopping_threshold` — Minimum eval loss improvement to count as an improvement. Default 0.0 (any decrease counts).

**Example:**

```bash
python scripts/ds_train.py \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_path tatsu-lab/alpaca \
  --use_peft True \
  --early_stopping_patience 5 \
  --early_stopping_threshold 0.001 \
  --eval_strategy steps \
  --eval_steps 100 \
  --num_train_epochs 3 \
  ...
```

**Auto-configuration:** When `early_stopping_patience > 0`, the script automatically:
1. Enables `load_best_model_at_end=True`
2. Sets `metric_for_best_model=eval_loss`, `greater_is_better=False`
3. Aligns `save_strategy` with `eval_strategy` (synced saving is needed to restore best checkpoint)

**Notes:**
- Must also set `eval_strategy` (e.g., `steps` + `eval_steps`), otherwise early stopping won't work
- Don't set `patience` too low (<3) — early training fluctuations may cause premature stopping
- For LoRA fine-tuning, `patience=5` with `eval_steps=100` typically works well

## Remote Training

When training needs to run on a remote GPU server, see [references/remote_training.md](references/remote_training.md) for the complete guide including agent guidelines, security model, and command reference.

## Troubleshooting

### OOM Errors
- Reduce batch size or increase gradient accumulation steps
- Enable gradient checkpointing: `--gradient_checkpointing`
- Use ZeRO-3 with CPU/NVMe offloading
- Reduce LoRA rank: `--lora_r 8`
- See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions

### Slow Training
- Ensure bf16/fp16 is enabled
- Check GPU utilization with `nvidia-smi`
- Use FlashAttention if available
- Optimize data loading with `--dataloader_num_workers`
- See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions

### Checkpoint Issues
- Use `--save_strategy steps` with `--save_steps`
- Enable `--save_total_limit` to cap checkpoint count
- For ZeRO-3, use `--zero3_save_16bit_model` to save FP16 weights
- See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions

### MPI Errors (multi-GPU only)
- Single-GPU training does **not** need MPI
- If you see MPI errors on single GPU, use `python3` directly instead of `deepspeed` launcher
- See [references/troubleshooting.md](references/troubleshooting.md#mpi-errors) for full MPI debugging guide

### Single-GPU Strategy
- See [references/single_gpu_strategy.md](references/single_gpu_strategy.md) for strategy selection, CPU/NVMe offload examples, and decision principles

## References

- **[Quick Start Guide](references/quick_start.md)** — Common training patterns and full examples
- **[DeepSpeed Guide](references/deepspeed_guide.md)** — DeepSpeed documentation and configuration reference
- **[LoRA/PEFT Best Practices](references/lora_guide.md)** — LoRA/QLoRA parameter tuning guide
- **[ZeRO Optimization Guide](references/zero_optimization.md)** — ZeRO stage comparison and optimization tips
- **[Single-GPU Strategy](references/single_gpu_strategy.md)** — Strategy selection for single-GPU training
- **[Remote Training Guide](references/remote_training.md)** — Remote training via SSH, agent guidelines, and security model
- **[Troubleshooting](references/troubleshooting.md)** — Common errors and solutions (OOM, NaN loss, MPI, NCCL, etc.)
