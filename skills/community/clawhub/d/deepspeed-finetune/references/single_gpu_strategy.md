# Single-GPU Training Strategy

When training on a single GPU, choose the right strategy based on model size and available VRAM.

## Strategy Selection Table

| Scenario | Strategy | Key Parameters |
|----------|----------|---------------|
| Single GPU + model fits (e.g., 4090 with 0.5B-7B) | Pure HF Trainer (no DeepSpeed needed) | `--bf16 True` |
| Single GPU + tight VRAM (e.g., T4 with 7B) | DeepSpeed ZeRO-1 | ~30% VRAM savings |
| Single GPU + not enough VRAM | DeepSpeed ZeRO-2 + CPU offload | Offload optimizer to CPU |
| Single GPU + severely limited VRAM | DeepSpeed ZeRO-3 + CPU/NVMe offload + LoRA | Offload params + optimizer |
| Multi-GPU | DeepSpeed ZeRO-2/3 + deepspeed launcher | Choose stage as needed |

## Using DeepSpeed on a Single GPU

### Method 1: HF Trainer Auto-Init (Recommended, no MPI required)

```bash
python3 scripts/ds_train.py \
  --model_name_or_path Qwen/Qwen2.5-7B \
  --deepspeed assets/ds_config_zero2.json \
  --dataset_path my_data \
  ...
```

### Method 2: DeepSpeed Launcher (Single GPU)

```bash
deepspeed --num_gpus=1 scripts/ds_train.py \
  --deepspeed assets/ds_config_zero2.json \
  ...
```

## Single-GPU DeepSpeed + CPU Offload Example

When GPU VRAM is insufficient, offload optimizer state to CPU memory:

```json
{
  "bf16": {"enabled": true},
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    }
  },
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto"
}
```

## Single-GPU DeepSpeed + NVMe Offload Example

When CPU memory is also insufficient (extreme cases), offload to NVMe SSD:

```json
{
  "bf16": {"enabled": true},
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "nvme",
      "nvme_path": "/local_nvme"
    },
    "offload_param": {
      "device": "nvme",
      "nvme_path": "/local_nvme"
    }
  },
  "aio": {
    "block_size": 1048576,
    "queue_depth": 8,
    "thread_count": 2
  },
  "train_batch_size": "auto"
}
```

## Important Notes

- **Single GPU does not need MPI**: HF Trainer initializes DeepSpeed internally via Accelerate; no `mpirun` or `deepspeed` launcher required.
- **MPI errors on single GPU?**: Check if you're using the `deepspeed` launcher instead of running `python3` directly. Method 1 is recommended for single GPU.
- **Offloading slows training**: CPU offload is ~2-3x slower, NVMe offload is ~5-10x slower. But running slower is better than not running at all.
- **LoRA + DeepSpeed stack well**: ZeRO-2 + LoRA is the best cost-performance combination.

## Decision Principles

**Model fits in VRAM (estimate: params × 2 bytes < 70% VRAM)** → Pure HF Trainer
- Simpler, no distributed overhead, easier debugging
- DeepSpeed on single GPU won't be faster than HF Trainer because distributed backend init adds overhead

**Model doesn't fit** → DeepSpeed + offload
- ZeRO-2 + CPU offload: optimizer offloaded to CPU memory, ~50% VRAM reduction
- ZeRO-3 + CPU/NVMe offload: params also sharded, for extreme VRAM shortage
- DeepSpeed's single-GPU value is **VRAM extension**, not speed

**Multi-GPU** → DeepSpeed required, data/model parallelism gives significant speedup
