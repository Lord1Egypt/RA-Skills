# DeepSpeed Troubleshooting Guide

Common issues and solutions for DeepSpeed fine-tuning.

> **For ZeRO-specific issues** (ZeRO config tuning, stage selection, communication bottlenecks), see [zero_optimization.md](zero_optimization.md).

## Out of Memory (OOM) Errors

### Issue 1: CUDA Out of Memory

**Error:** `RuntimeError: CUDA out of memory. Tried to allocate X bytes`

**Solutions (in order of priority):**

1. **Reduce batch size:** `--per_device_train_batch_size 2`
2. **Enable gradient accumulation:** `--gradient_accumulation_steps 8`
3. **Enable gradient checkpointing:** `--gradient_checkpointing`
4. **Reduce sequence length:** `--max_seq_length 1024`
5. **Use mixed precision** (reduces memory by ~50%): `{ "bf16": { "enabled": true } }`
6. **Reduce data loader workers:** `--dataloader_num_workers 2`
7. **Enable ZeRO or increase ZeRO stage** — see [zero_optimization.md](zero_optimization.md) for ZeRO-specific OOM solutions.

### Issue 2: CPU Memory Exhausted

**Error:** `MemoryError: Unable to allocate X bytes`

1. **Reduce CPU offloading buffer size** (if using ZeRO CPU offload):
   ```json
   { "zero_optimization": { "offload_optimizer": { "buffer_count": 2 } } }
   ```
2. **Reduce data loader workers:** `--dataloader_num_workers 2`
3. **Avoid loading full dataset into memory** — use streaming or memory-mapped files.

## Training Issues

### Issue 3: NaN or Inf Loss

**Error:** `loss is nan` or `loss is inf`

1. **Use BF16 instead of FP16:** `{ "bf16": { "enabled": true } }`
2. **Reduce learning rate:** `--learning_rate 1e-5`
3. **Enable loss scaling** (FP16 only): `{ "fp16": { "loss_scale": 0, "initial_scale_power": 16 } }`
4. **Add gradient clipping:** `--max_grad_norm 1.0`
5. **Warmup learning rate:** `--warmup_ratio 0.1`
6. **Check data quality** — no missing values, no extreme numbers, correct tokenization.

> **ZeRO-specific NaN** (FP16 + ZeRO-3 precision loss): see [zero_optimization.md](zero_optimization.md).

### Issue 4: Loss Not Decreasing

1. **Increase learning rate** if too low: `--learning_rate 5e-5`
2. **Check training loop** — optimizer called, gradients flowing, model in training mode
3. **Check data loading** — dataset not corrupted, batch size > 1, data shuffled
4. **Monitor gradients:** `torch.Tensor.grad.abs().sum()` for each param
5. **Reduce overfitting:** `--weight_decay 0.01 --lora_dropout 0.1`

### Issue 5: Slow Training Speed

1. **Check GPU utilization:** `watch -n 1 nvidia-smi` — should be >80%
2. **Increase batch size:** `--per_device_train_batch_size 16`
3. **Use faster data loading:** `--dataloader_num_workers 4 --dataloader_pin_memory true`
4. **Use mixed precision:** `{ "bf16": { "enabled": true } }`
5. **Profile data loading** — measure time to iterate full dataloader

> **ZeRO-specific slowness** (communication overhead): see [zero_optimization.md](zero_optimization.md).

## Checkpoint Issues

### Issue 6: Checkpoint Save Fails

**Error:** `Error saving checkpoint` or `Permission denied`

1. **Check permissions:** `chmod -R 755 /path/to/output/dir`
2. **Check disk space:** `df -h`
3. **Reduce checkpoint frequency:** `--save_steps 500 --save_total_limit 3`
4. **For ZeRO-3:** `--zero3_save_16bit_model`

### Issue 7: Checkpoint Load Fails

**Error:** `Error loading checkpoint: file not found` or `Model architecture mismatch`

1. **Verify path:** `ls -la /path/to/checkpoint`
2. **Check architecture:** `AutoConfig.from_pretrained(checkpoint_path)`
3. **Trust remote code:** `--trust_remote_code true`
4. **Use same DeepSpeed config** as during training

## Communication Issues

### Issue 8: NCCL Errors

**Error:** `NCCL error: ...` or `RuntimeError: NCCL communicators have been destroyed`

1. **Set env vars:** `export NCCL_DEBUG=INFO NCCL_IB_DISABLE=1 NCCL_P2P_DISABLE=1`
2. **Check GPU visibility:** `echo $CUDA_VISIBLE_DEVICES && nvidia-smi`
3. **Verify network** (multi-node): `ping <other_node_ip>`
4. **Check NCCL version:** `python -c "import torch; print(torch.cuda.nccl.version())"`
5. **Use correct launcher:** single GPU `deepspeed train.py`, multi-GPU `deepspeed --num_gpus=4 train.py`

### Issue 9: Process Hanging

1. **Check for deadlocks** — GPU utilization, CPU usage, network traffic
2. **Enable NCCL debug:** `export NCCL_DEBUG=WARN`
3. **Adjust timeouts:** `export NCCL_BLOCKING_WAIT=1`
4. **Verify process count** matches GPU count
5. **Check data loading** isn't blocking

## Data Issues

### Issue 10: Data Loading Errors

**Error:** `KeyError: 'column_name'` or `Token indices sequence length is longer than maximum sequence length`

1. **Verify dataset:** `load_dataset("path/to/data").features`
2. **Check column names:** `--text_column text --instruction_column instruction`
3. **Adjust max length:** `--max_seq_length 2048`
4. **Handle truncation:** `tokenizer(text, truncation=True, max_length=max_length, padding=False)`
5. **Check for empty data:** `assert len(dataset) > 0`

## Model Issues

### Issue 11: Model Loading Errors

**Error:** `OSError: model_name_or_path does not exist` or `ValueError: Loading model requires torch_dtype`

1. **Verify model path** (local absolute path or HuggingFace name with internet)
2. **Specify dtype:** `--torch_dtype bfloat16`
3. **Trust remote code:** `--trust_remote_code true`
4. **Upgrade transformers:** `pip install --upgrade transformers`
5. **Clear cache:** `rm -rf ~/.cache/huggingface/`

### Issue 12: LoRA Adapter Issues

**Error:** `ValueError: The model does not support LoRA` or `RuntimeError: Target module not found`

1. **Install PEFT:** `pip install peft`
2. **Check target modules:** `--lora_target_modules q_proj,v_proj,k_proj,o_proj`
3. **Verify task type:** `TaskType.CAUSAL_LM` for LLMs, `TaskType.SEQ_2_SEQ_LM` for encoder-decoder
4. **Match model architecture** — LLaMA: `q_proj,v_proj,k_proj,o_proj`; BERT: `query,value,key,output`
5. **QLoRA:** `--use_nested_quant true`

## Environment Issues

### Issue 13: Installation Errors

**Error:** `ModuleNotFoundError: No module named 'deepspeed'`

1. `pip install deepspeed` (or clone + `pip install -e .` from source)
2. Install deps: `pip install deepspeed[autodistillation] transformers datasets accelerate peft bitsandbytes`
3. Check Python >= 3.8 and CUDA version match PyTorch
4. Reinstall: `pip uninstall deepspeed -y && pip install deepspeed`

### Issue 14: CUDA Driver Issues

**Error:** `RuntimeError: CUDA out of memory` or `invalid device ordinal`

1. `nvidia-smi` — check driver and GPU status
2. Check visibility: `echo $CUDA_VISIBLE_DEVICES`
3. Verify PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
4. Update NVIDIA drivers if version is old

## MPI Errors

MPI is needed for multi-GPU only. **Single-GPU training does not need MPI.**

### Typical Errors
```
ModuleNotFoundError: No module named 'mpi4py'
MPI_ERRORS_ARE_FATAL: Local abort before MPI_INIT completed
ORTE_ERROR_LOG: A system-required executable either could not be found
```

### Troubleshooting Steps

1. **Single GPU?** Just use `python3 scripts/ds_train.py --deepspeed ds_config.json` (no MPI needed). Avoid the `deepspeed` launcher which triggers MPI.

2. **Multi-GPU?** Install MPI:
   ```bash
   pip install mpi4py
   sudo apt-get install -y openmpi-bin libopenmpi-dev  # Ubuntu
   pip install --force-reinstall --no-cache-dir mpi4py
   ```

3. **Broken OpenMPI config** (common in cloud/Docker like AutoDL) — missing `openmpi-bin`:
   ```bash
   sudo apt-get install -y openmpi-bin
   pip install --force-reinstall --no-cache-dir mpi4py
   ```

4. **No sudo?** Use Gloo backend to bypass MPI:
   ```bash
   export MASTER_ADDR=127.0.0.1 MASTER_PORT=29500 RANK=0 WORLD_SIZE=1
   python3 scripts/ds_train.py --deepspeed ds_config.json
   ```

5. **Nuclear option:** `pip uninstall deepspeed mpi4py -y && pip install deepspeed mpi4py`

## Debugging Tips

- **Detailed logging:** `export TORCH_SHOW_CPP_STACKTRACES=1`
- **Debug mode:** `deepspeed --debug train.py ...`
- **Profile:** `with deepspeed.Profiling(): ...`
- **Memory check:**
  ```python
  print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f} GB")
  print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f} GB")
  ```
- **Monitor:** `tensorboard --logdir ./output_dir`

## Common Error Messages Quick Reference

| Error | Most Likely Cause | Quick Fix |
|-------|-------------------|-----------|
| CUDA out of memory | Batch too large | Reduce batch size |
| Loss is nan | Learning rate too high | Reduce LR |
| NCCL error | Network/GPU issue | Check NVLink/InfiniBand |
| Module not found | Missing dependency | Install missing package |
| Checkpoint save failed | Disk space/permissions | Check free space |
| Data loading error | Wrong column name | Verify dataset columns |
| LoRA not working | Wrong target modules | Check model architecture |
| Slow training | Low GPU utilization | Increase batch size |
| Process hanging | Deadlock/comm issue | Check NCCL settings |
| Model load failed | Wrong path/version | Verify model install |
| MPI init failed | Missing/broken MPI | See MPI Errors section |

## Getting Help

1. **DeepSpeed Issues**: https://github.com/microsoft/DeepSpeed/issues
2. **HuggingFace Forums**: https://discuss.huggingface.co/
3. **Environment report:** `python -m deepspeed.env_report`
4. Provide a minimal reproduction script and system info (GPU, CUDA, DeepSpeed/Python versions).
