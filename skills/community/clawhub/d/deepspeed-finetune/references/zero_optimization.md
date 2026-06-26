# ZeRO Optimization Deep Dive

ZeRO (Zero Redundancy Optimizer) strategies, offloading, mixed precision, and performance tuning.

> **For general training troubleshooting** (OOM, NaN, NCCL, data loading, etc.), see [troubleshooting.md](troubleshooting.md).

## ZeRO Overview

ZeRO partitions optimizer states, gradients, and parameters across GPUs to eliminate redundancy.

| Configuration | Memory Reduction | Model Size Limit |
|--------------|------------------|------------------|
| Standard DDP | 1x | Limited by GPU |
| ZeRO-1 | ~4x | Small improvement |
| ZeRO-2 | ~8x | Moderate improvement |
| ZeRO-3 | ~10x+ | Massive models possible |

## ZeRO-1: Optimizer State Partitioning

- **Partitioned:** optimizer states (momentum, variance)
- **Not partitioned:** gradients, parameters
- **Memory saved:** ~4x vs DDP (optimizer states = 32 bytes/param → 32/N per GPU)
- **Communication:** standard DDP all-reduce during optimizer step
- **Best for:** models with large optimizer states (Adam), when communication is bottleneck

## ZeRO-2: Gradient Partitioning

- **Partitioned:** optimizer states + gradients
- **Not partitioned:** parameters
- **Memory saved:** ~8x vs DDP (~75% of DDP memory)
- **Communication:** all-reduce + all-gather during backward/optimizer steps

### Advanced Configuration

```json
{
  "zero_optimization": {
    "stage": 2,
    "overlap_comm": true,
    "contiguous_gradients": true,
    "allgather_bucket_size": 5e8,
    "reduce_bucket_size": 5e8,
    "allreduce_bucket_size": 5e8
  }
}
```

- **Bucket sizes:** larger = fewer messages, higher memory. Start with `5e8` (500MB) and tune.
- **`overlap_comm`:** overlaps communication with computation (significant speedup on modern interconnects).
- **`contiguous_gradients`:** uses contiguous memory for gradients.

**Best for:** default choice for most workloads, 7B-30B models.

## ZeRO-3: Parameter Partitioning

- **Partitioned:** optimizer states + gradients + parameters
- **Memory saved:** ~10x+ vs DDP (~90%+ of DDP memory)
- **Communication:** all-gather parameters during forward, all-reduce during backward

### Key Concepts

**Parameter Materialization:** Parameters are only copied to GPU when needed, then freed.

**Parameter Persistence Threshold** (`stage3_param_persistence_threshold`):
- Controls how many parameters stay resident in GPU memory.
- Higher = faster but more memory; lower = more aggressive offloading.
- Use `"auto"` for automatic selection.

**Prefetch Strategy** (tune these for ZeRO-3 performance):
```json
{
  "stage3_prefetch_bucket_size": "auto",
  "stage3_max_live_parameters": 1e9,
  "stage3_max_reuse_distance": 1e9
}
```

### Full Configuration Example

```json
{
  "zero_optimization": {
    "stage": 3,
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": "auto",
    "stage3_prefetch_bucket_size": "auto",
    "stage3_param_persistence_threshold": "auto",
    "stage3_max_live_parameters": 1e9,
    "stage3_max_reuse_distance": 1e9,
    "stage3_gather_16bit_weights_on_model_save": true
  }
}
```

### Saving Model Weights (ZeRO-3)

```python
# Consolidate distributed weights before saving:
deepspeed.zero.gather_distributed_parameters(model)
model.save_pretrained(output_dir)
```

Or via CLI: `--zero3_save_16bit_model`

**Best for:** 30B+ models, limited GPU memory, consumer GPUs.

## Offloading Strategies

### CPU Offloading

```json
{
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true,
      "buffer_count": 4,
      "fast_init": false
    }
  }
}
```

For ZeRO-3, also add `offload_param: { "device": "cpu", "pin_memory": true }`.

**Performance impact:** ZeRO-2 ~20-30% slower; ZeRO-3 ~30-50% slower than GPU-only.

### NVMe Offloading

```json
{
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "nvme",
      "nvme_path": "/local_nvme",
      "pin_memory": true,
      "buffer_count": 4,
      "max_in_cpu": 1e9
    },
    "offload_param": {
      "device": "nvme",
      "nvme_path": "/local_nvme",
      "pin_memory": true,
      "buffer_count": 5,
      "max_in_cpu": 1e9
    }
  }
}
```

**Requirements:** Fast NVMe SSD (PCIe 4.0+), 2-3x model size in disk space.
**Performance impact:** ~2-3x slower than GPU-only, but enables massive models.

## Mixed Precision

| Feature | BF16 | FP16 |
|---------|------|------|
| Dynamic range | Wider (8 exp bits) | Narrower (5 exp bits) |
| Loss scaling | Not needed | Required |
| Stability | Better | Prone to overflow |
| GPU support | A100+, RTX 30/40 | All modern GPUs |

**BF16** (preferred): `{ "bf16": { "enabled": true, "loss_scale": 0 } }`

**FP16** (older GPUs):
```json
{
  "fp16": { "enabled": true, "loss_scale": 0, "loss_scale_window": 1000,
    "initial_scale_power": 16, "hysteresis": 2, "min_loss_scale": 1 }
}
```

## Performance Optimization

### Batch Size & Gradient Accumulation

```
Effective batch = micro_batch_size × gradient_accumulation_steps × num_gpus
```

- **ZeRO-3:** start with micro-batch 2-4
- **ZeRO-2:** can use 8-16

### Communication Tuning

- `overlap_comm: true` — overlaps all-reduce with backward pass (10-20% speedup on NVLink/InfiniBand)
- Larger bucket sizes (`reduce_bucket_size: 5e8`) = fewer messages, less latency
- Tune `stage3_prefetch_bucket_size` for ZeRO-3 parameter pipelining

### Gradient Checkpointing

Reduces memory ~2x, adds ~20% compute overhead. Enable with `--gradient_checkpointing` or `model.gradient_checkpointing_enable()`.

### Memory vs Speed Trade-offs

| Configuration | Speed | Memory | Use Case |
|--------------|-------|--------|----------|
| ZeRO-0 | Fastest | High | Small models, debugging |
| ZeRO-1 | Fast | Medium-High | Simple partitioning |
| ZeRO-2 | Medium | Medium | Default choice |
| ZeRO-2 + CPU Offload | Medium | Low-Medium | Memory constrained |
| ZeRO-3 | Slow-Medium | Low | Large models |
| ZeRO-3 + CPU Offload | Slow | Very Low | Very large models |
| ZeRO-3 + NVMe Offload | Very Slow | Minimal | Massive models |

## Troubleshooting

> **ZeRO-specific issues only.** For general problems, see [troubleshooting.md](troubleshooting.md).

### ZeRO-3 OOM Despite Using Stage 3

1. **Reduce `stage3_param_persistence_threshold`:** `{ "stage3_param_persistence_threshold": 1e5 }`
2. **Reduce `stage3_max_live_parameters`:** `{ "stage3_max_live_parameters": 5e8 }`
3. **Enable parameter offloading:** `{ "offload_param": { "device": "cpu", "pin_memory": true } }`
4. **Enable optimizer offloading:** `{ "offload_optimizer": { "device": "cpu", "pin_memory": true } }`

### ZeRO Training Slower Than Expected

1. **Enable `overlap_comm`:** `{ "overlap_comm": true }`
2. **Tune bucket sizes** (larger = fewer messages): `{ "reduce_bucket_size": 5e8 }`
3. **Check interconnect** — ZeRO-3 benefits greatly from NVLink/InfiniBand. On slow Ethernet, ZeRO-2 may be faster.
4. **Reduce ZeRO stage** if memory allows — ZeRO-2 has less communication overhead.
5. **Tune prefetch:** `{ "stage3_prefetch_bucket_size": 1e8 }`

### FP16 + ZeRO-3 Precision Issues

1. **Switch to BF16** — wider dynamic range eliminates most precision loss.
2. **If BF16 unavailable,** increase FP16 loss scale window: `{ "fp16": { "loss_scale_window": 1000, "initial_scale_power": 16 } }`
3. **Reduce learning rate** — precision loss amplifies with large LRs.
4. **Enable gradient clipping:** `--max_grad_norm 1.0`

### ZeRO Stage Selection Guide

| Scenario | Recommendation |
|----------|---------------|
| Model fits in GPU with DDP | ZeRO-0 (no ZeRO) |
| Slightly too large for DDP | ZeRO-1 or ZeRO-2 |
| Default for 7B-30B models | ZeRO-2 |
| Model > 30B or very tight on memory | ZeRO-3 |
| ZeRO-3 still OOM | ZeRO-3 + CPU offload |
| Extreme memory constraint | ZeRO-3 + NVMe offload |

## Profiling

- **Profile:** `with deepspeed.Profiling(): training_loop()`
- **Check logs** for all-reduce, all-gather, offload, and compute times
- **Environment report:** `python -m deepspeed.env_report`

## Best Practices

1. Start with ZeRO-2 (good default)
2. Use BF16 when possible
3. Enable gradient checkpointing when memory constrained
4. Tune batch sizes for GPU utilization
5. Monitor GPU utilization (aim >80%)
6. Use ZeRO-3 only when needed (30B+ models)
7. Enable `overlap_comm` on fast interconnects
8. Tune bucket sizes (start with 5e8)
9. Profile before scaling
10. Save checkpoints regularly
11. Pin memory for CPU offloading transfers

## Resources

- [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed)
- [DeepSpeed Documentation](https://www.deepspeed.ai/)
- [ZeRO Paper](https://arxiv.org/abs/1910.02054)
- [ZeRO-Offload Paper](https://arxiv.org/abs/2101.09860)
- [ZeRO-Infinity Paper](https://arxiv.org/abs/2104.07857)
- [DeepSpeed ZeRO Docs](https://www.deepspeed.ai/tutorials/zero/)
