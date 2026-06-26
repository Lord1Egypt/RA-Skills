# Quick Start Examples

Basic examples for using the DeepSpeed fine-tuning skill.

## Example 1: LoRA Fine-tuning on Single GPU

Fine-tune a LLaMA-2 7B model using LoRA:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/lora-llama2-7b \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05 \
  --learning_rate 2e-4 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --max_seq_length 2048 \
  --bf16 \
  --logging_steps 10 \
  --save_steps 500 \
  --save_total_limit 3
```

## Example 2: QLoRA Fine-tuning 70B Model

Fine-tune a 70B model using QLoRA with ZeRO-2:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-70b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/qlora-llama2-70b \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method qlora \
  --load_in_4bit \
  --bnb_4bit_quant_type nf4 \
  --bnb_4bit_compute_dtype bfloat16 \
  --use_nested_quant \
  --lora_r 16 \
  --lora_alpha 32 \
  --learning_rate 2e-4 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --max_seq_length 1024 \
  --bf16 \
  --gradient_checkpointing \
  --logging_steps 10 \
  --save_steps 1000
```

## Example 3: Full Fine-tuning with ZeRO-3

Full fine-tuning using ZeRO-3 for memory efficiency:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/full-ft-llama2-7b \
  --deepspeed assets/ds_config_zero3.json \
  --learning_rate 1e-5 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --max_seq_length 2048 \
  --bf16 \
  --gradient_checkpointing \
  --logging_steps 10 \
  --save_steps 500 \
  --save_total_limit 2 \
  --zero3_save_16bit_model
```

## Example 4: Multi-GPU Training

Launch training with 4 GPUs:

```bash
# Multi-GPU on single node
deepspeed --num_gpus=4 scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/multi-gpu \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --learning_rate 2e-4 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4 \
  --max_seq_length 2048 \
  --bf16
```

## Example 5: Instruction Tuning

Fine-tune for instruction following:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/instruction-dataset \
  --output_dir ./outputs/instruction-tuned \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 32 \
  --lora_alpha 64 \
  --learning_rate 5e-5 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --max_seq_length 4096 \
  --bf16 \
  --instruction_column instruction \
  --output_column output \
  --logging_steps 10
```

## Example 6: Monitoring Training

Monitor training progress and plot loss:

```bash
# Training
python scripts/ds_train.py --output_dir ./outputs/my-run ...

# After training, monitor
python scripts/monitor_training.py \
  --log-dir ./outputs/my-run \
  --summary \
  --plot \
  --plot-output ./outputs/my-run/loss_plot.png
```

## Example 7: Generating DeepSpeed Configs

Generate custom DeepSpeed configuration:

```bash
# ZeRO-2 with CPU offloading
python scripts/generate_ds_config.py \
  --zero-stage 2 \
  --offload-optimizer \
  --offload-device cpu \
  --bf16 \
  --output assets/ds_config_zero2_cpu.json

# ZeRO-3 with NVMe offloading
python scripts/generate_ds_config.py \
  --zero-stage 3 \
  --offload-optimizer \
  --offload-param \
  --offload-device nvme \
  --nvme-path /local_nvme \
  --bf16 \
  --output assets/ds_config_zero3_nvme.json

# ZeRO-2 simple (no offloading)
python scripts/generate_ds_config.py \
  --zero-stage 2 \
  --bf16 \
  --output assets/ds_config_zero2.json
```

## Example 8: Resume Training

Resume from checkpoint:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/my-run \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --learning_rate 2e-4 \
  --resume_from_checkpoint ./outputs/my-run/checkpoint-5000
```

## Example 9: Evaluation Only

Run evaluation on a checkpoint:

```bash
python scripts/ds_train.py \
  --model_name_or_path ./outputs/my-run \
  --dataset_path /path/to/test-dataset \
  --output_dir ./outputs/eval-results \
  --deepspeed assets/ds_config_zero2.json \
  --do_eval \
  --do_train false
```

## Example 10: Loading and Using Adapters

Load trained LoRA adapters:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf"
)

# Load LoRA adapters
model = PeftModel.from_pretrained(
    base_model,
    "./outputs/lora-llama2-7b"
)

# Merge adapters into base model
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")

# Or use directly
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
inputs = tokenizer("Hello, how are you?", return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0]))
```

## Example 11: Custom LoRA Target Modules

Customize which modules to apply LoRA to:

```bash
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path /path/to/my-dataset \
  --output_dir ./outputs/custom-lora \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_target_modules q_proj,v_proj,k_proj,o_proj,gate_proj,up_proj,down_proj \
  --learning_rate 2e-4 \
  --num_train_epochs 3
```

## Example 12: Using RS-LoRA

Use Rank-Stabilized LoRA for more stable training:

```python
from peft import LoraConfig, get_peft_model

# RS-LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    use_rslora=True,  # Enable RS-LoRA
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
```

## Dataset Format Examples

### Simple Text Dataset

```json
[
  {"text": "This is example text 1."},
  {"text": "This is example text 2."},
  {"text": "This is example text 3."}
]
```

### Instruction Dataset

```json
[
  {
    "instruction": "What is the capital of France?",
    "input": "",
    "output": "The capital of France is Paris."
  },
  {
    "instruction": "Translate to Spanish",
    "input": "Hello, how are you?",
    "output": "Hola, ¿cómo estás?"
  }
]
```

### HuggingFace Dataset

```bash
# Use a HuggingFace dataset directly
python scripts/ds_train.py \
  --dataset_path timdettmers/openassistant-guanaco \
  --dataset_config default \
  --text_column text \
  ...
```

## Tips for Success

1. **Start Small**: Test with small model and dataset first
2. **Monitor Training**: Use `monitor_training.py` to track progress
3. **Save Checkpoints**: Save frequently with `--save_steps`
4. **Use Mixed Precision**: Enable BF16 for better performance
5. **Tune Batch Size**: Balance memory and GPU utilization
6. **Check Data**: Verify dataset format before training
7. **Monitor GPU**: Use `nvidia-smi` to check utilization
8. **Start with LoRA**: Use LoRA before full fine-tuning
9. **Use ZeRO-2**: Default ZeRO stage for most cases
10. **Read Docs**: Consult references/ for detailed guides

## Common Workflows

### Workflow 1: Train and Test LoRA Model

```bash
# 1. Train with LoRA
python scripts/ds_train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset_path data.json \
  --output_dir ./outputs/my-model \
  --deepspeed assets/ds_config_zero2.json \
  --use_peft --peft_method lora \
  --lora_r 16 --lora_alpha 32 \
  --learning_rate 2e-4 --num_train_epochs 3

# 2. Monitor training
python scripts/monitor_training.py \
  --log-dir ./outputs/my-model \
  --summary --plot

# 3. Test model (inference)
python3 -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf', torch_dtype=torch.bfloat16)
model = PeftModel.from_pretrained(base_model, './outputs/my-model')
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf')
inputs = tokenizer('Hello, how are you?', return_tensors='pt').to(model.device)
outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0]))
"
```

### Workflow 2: Hyperparameter Tuning

```bash
# Try different learning rates
for lr in 1e-5 2e-5 5e-5; do
  python scripts/ds_train.py \
    --model_name_or_path meta-llama/Llama-2-7b-hf \
    --dataset_path data.json \
    --output_dir ./outputs/lr-$lr \
    --deepspeed assets/ds_config_zero2.json \
    --use_peft --peft_method lora \
    --learning_rate $lr \
    --num_train_epochs 3
done
```

### Workflow 3: Compare Different Ranks

```bash
# Compare LoRA ranks
for r in 8 16 32 64; do
  python scripts/ds_train.py \
    --model_name_or_path meta-llama/Llama-2-7b-hf \
    --dataset_path data.json \
    --output_dir ./outputs/rank-$r \
    --deepspeed assets/ds_config_zero2.json \
    --use_peft --peft_method lora \
    --lora_r $r --lora_alpha $(($r * 2)) \
    --learning_rate 2e-4 --num_train_epochs 3
done
```

For more examples and detailed guides, see the `references/` directory.
