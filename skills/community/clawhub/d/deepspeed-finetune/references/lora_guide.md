# LoRA/QLoRA Fine-tuning Guide

Comprehensive guide for parameter-efficient fine-tuning with LoRA and QLoRA.

## What is LoRA?

**LoRA (Low-Rank Adaptation)** freezes pre-trained model weights and injects trainable rank decomposition matrices into each layer. This significantly reduces trainable parameters while maintaining model performance.

### Key Benefits

- **Memory Efficient**: Only 0.1%-3% of parameters trainable
- **Storage Efficient**: Save only adapters (MB vs GB)
- **Fast Training**: Fewer parameters to update
- **No Catastrophic Forgetting**: Base model preserved
- **Portability**: Adapters can be swapped/combined

## Installation

```bash
# Install PEFT and dependencies
pip install peft transformers datasets accelerate
pip install bitsandbytes  # For QLoRA
pip install deepspeed      # For ZeRO optimization
```

## LoRA Configuration

### Basic LoRA Config

```python
from peft import LoraConfig, TaskType

lora_config = LoraConfig(
    r=16,                      # LoRA rank
    lora_alpha=32,             # LoRA scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Target modules
    lora_dropout=0.05,         # Dropout
    bias="none",               # Bias training
    task_type=TaskType.CAUSAL_LM,  # Task type
)
```

### Rank Selection Guide

**Low Rank (r=4-8):**
- Minimal parameters
- Faster training
- May limit adaptation capacity
- Good for: Simple tasks, quick experiments

**Medium Rank (r=16-32):**
- Balanced parameters and performance
- Good default for most tasks
- Good for: Instruction tuning, domain adaptation

**High Rank (r=64-128):**
- More adaptation capacity
- Slower training
- Risk of overfitting
- Good for: Complex tasks, fine-grained control

### Alpha Scaling

- `lora_alpha` = scaling factor
- Usually `alpha = 2 * r` is good default
- Higher alpha = stronger adaptation impact
- Tune alpha based on convergence speed

### Target Modules Selection

**LLM Attention Layers (Common):**
```python
# LLaMA, Mistral, etc.
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]

# Including MLP layers
target_modules = [
    "q_proj", "v_proj", "k_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
]
```

**Vision Transformers:**
```python
# ViT models
target_modules = ["query", "value", "key", "output"]
```

**BERT-like:**
```python
# BERT, RoBERTa
target_modules = ["query", "value", "key", "output"]
```

## QLoRA (4-bit Quantization + LoRA)

### BitsAndBytes Configuration

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,              # Enable 4-bit loading
    bnb_4bit_quant_type="nf4",       # Normal Float 4 (best performance)
    bnb_4bit_compute_dtype="bfloat16",  # Compute dtype
    bnb_4bit_use_double_quant=True, # Double quantization (saves memory)
)
```

### QLoRA Benefits

- **Extreme Memory Efficiency**: Train 65B models on 48GB GPU
- **Minimal Performance Drop**: Near full-precision performance
- **Cost Effective**: Lower hardware requirements
- **Accessibility**: Fine-tune large models on consumer GPUs

### QLoRA Workflow

```python
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM

# 1. Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# 2. Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

# 3. Add LoRA adapters
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
```

## Training with DeepSpeed

### LoRA + ZeRO-2 (Recommended)

```json
// ds config
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
    "contiguous_gradients": true
  }
}
```

**Why ZeRO-2 for LoRA:**
- LoRA already reduces parameters
- ZeRO-2 handles gradients efficiently
- Faster than ZeRO-3 for small adapter training
- Good balance for adapter training

### QLoRA + ZeRO-2

```json
// ds config
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

**CPU offloading recommended** for QLoRA due to limited GPU memory.

## Saving and Loading

### Saving Adapters Only

```python
# Save adapters (MB size)
model.save_pretrained("./lora-adapters")
tokenizer.save_pretrained("./lora-adapters")
```

### Merging Adapters

```python
# Merge adapters into base model (optional)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")
```

### Loading Adapters

```python
# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf"
)

# Load adapters
from peft import PeftModel
model = PeftModel.from_pretrained(base_model, "./lora-adapters")
```

## Advanced Techniques

### Multi-LoRA (Multiple Tasks)

```python
# Train separate adapters for different tasks
# Each task has its own LoRA config

# Load multiple adapters
model = AutoModelForCausalLM.from_pretrained("base-model")
model = PeftModel.from_pretrained(model, "task1-adapters")
model.load_adapter("task2-adapters", adapter_name="task2")

# Switch between adapters
model.set_adapter("task1")  # Use task1 adapters
model.set_adapter("task2")  # Use task2 adapters
```

### Ranked-Stabilized LoRA (Rank-stabilized scaling)

```python
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    use_rslora=True,  # Enable RS-LoRA
    target_modules=["q_proj", "v_proj"],
    task_type=TaskType.CAUSAL_LM
)
```

**Benefits:**
- More stable across different ranks
- Better performance for varying ranks
- Reduces need for extensive hyperparameter tuning

### DoRA (Weight-Decomposed Low-Rank Adaptation)

Alternative to LoRA that decomposes magnitude and direction.

```python
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    use_dora=True,  # Enable DORA
    target_modules=["q_proj", "v_proj"],
    task_type=TaskType.CAUSAL_LM
)
```

## Best Practices

### LoRA Training

1. **Start with r=16**: Good default for most tasks
2. **Use alpha=2*r**: Standard scaling convention
3. **Target attention layers**: Most impact per parameter
4. **Use dropout=0.05**: Prevents overfitting
5. **Freeze base model**: Only train adapters
6. **Use appropriate LR**: Usually higher than full fine-tuning

### QLoRA Training

1. **Use NF4 quantization**: Best performance
2. **Double quantization**: Saves extra memory
3. **BF16 compute dtype**: Better stability
4. **CPU offloading**: If GPU memory tight
5. **Gradient checkpointing**: Further reduce memory
6. **Small batch sizes**: Due to memory constraints

### Hyperparameter Tuning

```python
# Common good starting points
# For instruction tuning: r=16, alpha=32, lr=2e-4
# For domain adaptation: r=8, alpha=16, lr=1e-4
# For style transfer: r=32, alpha=64, lr=3e-4
```

## Common Issues and Solutions

### Issue: Poor Convergence

**Solutions:**
- Increase LoRA rank (r=32 or r=64)
- Increase alpha scaling
- Reduce dropout (dropout=0.01)
- Adjust learning rate
- Increase training epochs

### Issue: Overfitting

**Solutions:**
- Reduce LoRA rank
- Increase dropout
- Use weight decay
- Add data augmentation
- Early stopping

### Issue: Memory Out of Bounds

**Solutions:**
- Enable gradient checkpointing
- Reduce batch size
- Use ZeRO-2 with CPU offloading
- For QLoRA: reduce sequence length
- Use smaller rank

### Issue: Slow Training

**Solutions:**
- Use ZeRO-2 instead of ZeRO-3
- Increase micro-batch size
- Reduce gradient accumulation steps
- Use mixed precision (BF16/FP16)
- Optimize data loading

## Example Training Commands

### LoRA Fine-tuning

```bash
python ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path my-data \
  --output_dir ./lora-output \
  --deepspeed ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05 \
  --learning_rate 2e-4 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4
```

### QLoRA Fine-tuning

```bash
python ds_train.py \
  --model_name_or_path meta-llama/Llama-2-70b-hf \
  --dataset_path my-data \
  --output_dir ./qlora-output \
  --deepspeed ds_config_zero2.json \
  --use_peft \
  --peft_method qlora \
  --load_in_4bit \
  --lora_r 16 \
  --lora_alpha 32 \
  --learning_rate 2e-4 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2
```

## Resources

- [PEFT GitHub](https://github.com/huggingface/peft)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [HuggingFace PEFT Docs](https://huggingface.co/docs/peft)
