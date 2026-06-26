# DeepSpeed Reference Guide

Quick reference for DeepSpeed configuration and common usage patterns.

> **For ZeRO optimization details, see [zero_optimization.md](zero_optimization.md).**

## Installation

```bash
# Core DeepSpeed
pip install deepspeed

# With extra dependencies
pip install deepspeed[autodistillation]

# Build from source (latest features)
git clone https://github.com/microsoft/DeepSpeed.git
cd DeepSpeed
pip install -e .
```

## Common Configurations

### Configuration 1: Single GPU, Small Model

```json
{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "bf16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 0
  }
}
```

### Configuration 2: Multi-GPU, Medium Model (ZeRO-2)

```json
{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "bf16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 2,
    "overlap_comm": true,
    "contiguous_gradients": true,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    }
  }
}
```

### Configuration 3: Large Model, CPU Offload (ZeRO-3)

```json
{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "bf16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 3,
    "overlap_comm": true,
    "contiguous_gradients": true,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    }
  }
}
```

### Configuration 4: Massive Model, NVMe Offload (ZeRO-3)

```json
{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "bf16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 3,
    "overlap_comm": true,
    "contiguous_gradients": true,
    "offload_optimizer": {
      "device": "nvme",
      "nvme_path": "/local_nvme",
      "pin_memory": true
    },
    "offload_param": {
      "device": "nvme",
      "nvme_path": "/local_nvme",
      "pin_memory": true
    }
  }
}
```

## Best Practices

1. **Start with ZeRO-2**: Good default for most use cases
2. **Use BF16 when possible**: Better stability than FP16
3. **Enable gradient checkpointing**: When memory constrained
4. **Tune batch sizes**: Balance memory and GPU utilization
5. **Monitor GPU utilization**: Aim for >80% for efficient training
6. **Use appropriate offloading**: CPU > NVMe in most cases
7. **Profile before scaling**: Understand bottlenecks first
8. **Save checkpoints regularly**: Training can be long
9. **Use tensor cores**: BF16/FP16 for acceleration
10. **Pin memory for transfers**: When using CPU offloading

## Debugging Tips

1. **Check device placement**: Ensure model and data on correct GPUs
2. **Verify communication**: Check NCCL logs for errors
3. **Profile with Nsight**: Identify bottlenecks
4. **Monitor memory**: Use `nvidia-smi` and DeepSpeed logging
5. **Start small**: Test with smaller model/batch first
6. **Reduce complexity**: Disable features to isolate issues
7. **Check data loading**: Ensure data pipeline isn't bottleneck
8. **Validate configs**: Use `ds_report` to check configuration

## Resources

- [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed)
- [DeepSpeed Documentation](https://www.deepspeed.ai/)
- [ZeRO Paper](https://arxiv.org/abs/1910.02054)
- [DeepSpeed Tutorial](https://www.deepspeed.ai/tutorials/)
