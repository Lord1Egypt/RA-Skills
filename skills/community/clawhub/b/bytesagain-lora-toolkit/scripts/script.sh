#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${HOME}/.local/share/bytesagain-lora-toolkit"
mkdir -p "$DATA_DIR"

_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
_err() { echo "ERROR: $*" >&2; exit 1; }

# ── Model specs database ──────────────────────────────────────────────────────
_model_params() {
    local model="${1:-llama3-8b}"
    case "$model" in
        llama3-8b|llama-3-8b)   echo "8 7 llama3" ;;
        llama3-70b|llama-3-70b) echo "70 65 llama3" ;;
        mistral-7b)             echo "7 7 mistral" ;;
        mistral-8x7b)           echo "47 45 mistral-moe" ;;
        qwen2-7b)               echo "7 7 qwen2" ;;
        qwen2-72b)              echo "72 68 qwen2" ;;
        phi3-mini)              echo "4 3.8 phi3" ;;
        phi3-medium)            echo "14 13 phi3" ;;
        gemma2-9b)              echo "9 8.5 gemma2" ;;
        gemma2-27b)             echo "27 25 gemma2" ;;
        *)                      echo "7 7 unknown" ;;  # default to 7B
    esac
}

_gpu_vram() {
    local gpu="${1:-16gb}"
    case "${gpu,,}" in
        8gb)  echo "8" ;;
        12gb) echo "12" ;;
        16gb) echo "16" ;;
        24gb) echo "24" ;;
        40gb) echo "40" ;;
        80gb) echo "80" ;;
        a100) echo "80" ;;
        h100) echo "80" ;;
        a10g) echo "24" ;;
        v100) echo "32" ;;
        *)    echo "${gpu//[^0-9]/}" ;;
    esac
}

# ── cmd_config ────────────────────────────────────────────────────────────────
cmd_config() {
    local model="llama3-8b" gpu="16gb" dataset=10000
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --model)   model="$2"; shift 2 ;;
            --gpu)     gpu="$2";   shift 2 ;;
            --dataset) dataset="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    read -r size_b size_gb family <<< "$(_model_params "$model")"
    local vram
    vram=$(_gpu_vram "$gpu")

    # Determine quantization and rank based on VRAM
    local quant="4-bit (bitsandbytes)" rank=16 alpha=32
    if (( vram >= 80 )); then
        quant="bf16 (full precision)"; rank=64; alpha=128
    elif (( vram >= 40 )); then
        quant="bf16 (full precision)"; rank=32; alpha=64
    elif (( vram >= 24 )); then
        quant="8-bit (bitsandbytes)"; rank=32; alpha=64
    elif (( vram >= 16 )); then
        quant="4-bit (bitsandbytes)"; rank=16; alpha=32
    else
        quant="4-bit (bitsandbytes)"; rank=8; alpha=16
    fi

    # Estimate batch size
    local batch=4
    if (( vram < 16 )); then batch=1
    elif (( vram < 24 )); then batch=2
    elif (( vram >= 40 )); then batch=8; fi

    echo "╔══════════════════════════════════════════════════╗"
    echo "║         LoRA Configuration — BytesAgain          ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Model:       $model (${size_b}B parameters)"
    echo "🖥  GPU VRAM:    ${vram}GB"
    echo "📊 Dataset:     ${dataset} samples"
    echo ""
    echo "── Recommended LoRA Config ──────────────────────────"
    echo "  quantization:     $quant"
    echo "  lora_r (rank):    $rank"
    echo "  lora_alpha:       $alpha"
    echo "  lora_dropout:     0.05"
    echo "  target_modules:   q_proj, v_proj, k_proj, o_proj"
    echo "  per_device_batch: $batch"
    echo "  gradient_accum:   4"
    echo "  learning_rate:    2e-4"
    echo "  lr_scheduler:     cosine"
    echo "  num_epochs:       3"
    echo "  max_seq_length:   2048"
    echo "  fp16:             true"
    echo ""
    echo "── Estimated VRAM Usage ─────────────────────────────"
    local vram_used=$(( size_b / 2 + 2 ))
    echo "  Model weights:  ~${vram_used}GB"
    echo "  Optimizer:      ~2GB"
    echo "  Activations:    ~$((batch * 2))GB"
    echo "  Available VRAM: ${vram}GB"
    if (( vram_used + batch * 2 + 2 > vram )); then
        echo "  ⚠️  May OOM — reduce batch size or use gradient checkpointing"
    else
        echo "  ✅ Should fit comfortably"
    fi
    echo ""
    echo "Run: bash scripts/script.sh generate --model $model --output train.py"
}

# ── cmd_estimate ──────────────────────────────────────────────────────────────
cmd_estimate() {
    local model="llama3-8b" gpu="16gb" dataset=10000 epochs=3
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --model)   model="$2";   shift 2 ;;
            --gpu)     gpu="$2";     shift 2 ;;
            --dataset) dataset="$2"; shift 2 ;;
            --epochs)  epochs="$2";  shift 2 ;;
            *) shift ;;
        esac
    done

    read -r size_b size_gb family <<< "$(_model_params "$model")"
    local vram
    vram=$(_gpu_vram "$gpu")
    local steps=$(( dataset * epochs / 4 ))
    local time_hrs=$(( steps / 1800 + 1 ))

    echo "╔══════════════════════════════════════════════════╗"
    echo "║       Training Cost Estimate — BytesAgain        ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Model:       $model"
    echo "📊 Dataset:     ${dataset} × ${epochs} epochs"
    echo "🔢 Steps:       ~${steps}"
    echo ""
    echo "── Time Estimate ────────────────────────────────────"
    echo "  Single GPU (${vram}GB): ~${time_hrs} hours"
    echo "  A100 80GB:            ~$(( steps / 3600 + 1 )) hours"
    echo ""
    echo "── Cloud Cost (on-demand) ───────────────────────────"
    local cost_lambda=$(echo "$time_hrs * 1.10" | awk '{printf "%.2f", $1}')
    local cost_runpod=$(echo "$time_hrs * 0.74" | awk '{printf "%.2f", $1}')
    local cost_vastai=$(echo "$time_hrs * 0.50" | awk '{printf "%.2f", $1}')
    echo "  Lambda Labs A100:  ~\$${cost_lambda}"
    echo "  RunPod A100:       ~\$${cost_runpod}"
    echo "  Vast.ai (3090):    ~\$${cost_vastai}"
    echo ""
    echo "── Storage Estimate ─────────────────────────────────"
    local adapter_mb=$(( rank * 4 ))
    echo "  LoRA adapter size: ~${adapter_mb}MB (rank=${rank:-16})"
    echo "  Checkpoint size:   ~${size_b}GB (merged model)"
}

# ── cmd_generate ──────────────────────────────────────────────────────────────
cmd_generate() {
    local model="llama3-8b" output="train.py"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --model)  model="$2";  shift 2 ;;
            --output) output="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    _log "Generating training script for $model → $output"

    cat > "$output" << 'PYEOF'
#!/usr/bin/env python3
"""
LoRA Fine-tuning Script — Generated by BytesAgain LoRA Toolkit
https://bytesagain.com/skill/bytesagain-lora-toolkit
"""
import os
from dataclasses import dataclass, field
from typing import Optional

# Install: pip install transformers peft trl datasets bitsandbytes accelerate

@dataclass
class TrainingConfig:
    model_name: str = "MODEL_PLACEHOLDER"
    dataset_path: str = "dataset.json"
    output_dir: str = "./lora-output"
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: list = field(default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"])
    num_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    max_seq_length: int = 2048
    load_in_4bit: bool = True
    fp16: bool = True

def train(config: TrainingConfig):
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer, SFTConfig
    from datasets import load_dataset
    import torch

    print(f"Loading model: {config.model_name}")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config.load_in_4bit,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    ) if config.load_in_4bit else None

    model = AutoModelForCausalLM.from_pretrained(
        config.model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(config.model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.target_modules,
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = load_dataset("json", data_files=config.dataset_path, split="train")

    training_args = SFTConfig(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        fp16=config.fp16,
        save_steps=100,
        logging_steps=10,
        max_seq_length=config.max_seq_length,
        report_to="none",
    )

    trainer = SFTTrainer(model=model, args=training_args, train_dataset=dataset)
    trainer.train()
    model.save_pretrained(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)
    print(f"✅ Training complete. Adapter saved to: {config.output_dir}")

if __name__ == "__main__":
    config = TrainingConfig()
    train(config)
PYEOF

    # Replace model placeholder
    sed -i "s/MODEL_PLACEHOLDER/$model/" "$output"
    echo "✅ Training script generated: $output"
    echo ""
    echo "Next steps:"
    echo "  1. pip install transformers peft trl datasets bitsandbytes accelerate"
    echo "  2. Prepare your dataset in Alpaca/ShareGPT format"
    echo "  3. Edit $output — set dataset_path and output_dir"
    echo "  4. python3 $output"
}

# ── cmd_validate ──────────────────────────────────────────────────────────────
cmd_validate() {
    local file="" fmt="auto"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --file)   file="$2";   shift 2 ;;
            --format) fmt="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    [[ -z "$file" ]] && _err "Usage: validate --file dataset.json [--format alpaca|sharegpt|openai]"
    [[ ! -f "$file" ]] && _err "File not found: $file"

    local count
    count=$(python3 -c "import json; d=json.load(open('$file')); print(len(d) if isinstance(d,list) else 'not-a-list')" 2>/dev/null || echo "parse-error")

    if [[ "$count" == "parse-error" ]]; then
        echo "❌ Invalid JSON: cannot parse $file"
        exit 1
    fi
    if [[ "$count" == "not-a-list" ]]; then
        echo "❌ Dataset must be a JSON array (list of objects)"
        exit 1
    fi

    echo "📄 File: $file"
    echo "📊 Total samples: $count"
    echo ""

    python3 - "$file" "$fmt" << 'PYEOF'
import sys, json
file, fmt = sys.argv[1], sys.argv[2]
data = json.load(open(file))
sample = data[0] if data else {}
keys = set(sample.keys())

alpaca_keys = {"instruction", "output"}
sharegpt_keys = {"conversations"}
openai_keys = {"messages"}

detected = "unknown"
if alpaca_keys.issubset(keys):
    detected = "alpaca"
elif sharegpt_keys.issubset(keys):
    detected = "sharegpt"
elif openai_keys.issubset(keys):
    detected = "openai"

fmt_check = fmt if fmt != "auto" else detected
print(f"🔍 Detected format: {detected}")
print(f"✅ Format check: {fmt_check}")
print(f"📝 Sample keys: {list(keys)}")

if detected == "unknown":
    print("")
    print("⚠️  Unknown format. Expected one of:")
    print('   Alpaca:   {"instruction": "...", "input": "...", "output": "..."}')
    print('   ShareGPT: {"conversations": [{"from": "human", "value": "..."}]}')
    print('   OpenAI:   {"messages": [{"role": "user", "content": "..."}]}')
else:
    print(f"✅ Dataset is valid {detected} format — ready for training!")
PYEOF
}

# ── cmd_recommend ─────────────────────────────────────────────────────────────
cmd_recommend() {
    local task="chat" gpu="16gb" lang="en"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --task)     task="$2";  shift 2 ;;
            --gpu)      gpu="$2";   shift 2 ;;
            --language) lang="$2";  shift 2 ;;
            *) shift ;;
        esac
    done

    local vram
    vram=$(_gpu_vram "$gpu")

    echo "╔══════════════════════════════════════════════════╗"
    echo "║      Model Recommendation — BytesAgain           ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "Task: $task | GPU: ${vram}GB VRAM | Language: $lang"
    echo ""

    if (( vram >= 40 )); then
        echo "🥇 Top Pick:   Llama-3-70B (best quality, needs 40GB+)"
        echo "🥈 Runner-up:  Qwen2-72B (strong multilingual)"
        echo "🥉 Budget:     Mistral-8x7B (MoE, efficient at scale)"
    elif (( vram >= 24 )); then
        echo "🥇 Top Pick:   Llama-3-8B (best balance for 24GB)"
        echo "🥈 Runner-up:  Mistral-7B (fast, strong reasoning)"
        echo "🥉 Multilingual: Qwen2-7B (best for zh/en/ja)"
    elif (( vram >= 16 )); then
        echo "🥇 Top Pick:   Llama-3-8B with 4-bit quant"
        echo "🥈 Runner-up:  Qwen2-7B (great for Asian languages)"
        echo "🥉 Lightweight: Phi3-Medium (14B, surprisingly capable)"
    else
        echo "🥇 Top Pick:   Phi3-Mini (3.8B, fits 8GB VRAM)"
        echo "🥈 Runner-up:  Gemma2-9B with 4-bit quant"
        echo "🥉 Alternative: Qwen2-7B with 4-bit (multilingual)"
    fi

    echo ""
    [[ "$lang" == "zh" || "$lang" == "chinese" ]] && \
        echo "💡 Chinese tip: Qwen2 series has the best Chinese performance"
    [[ "$task" == "code" ]] && \
        echo "💡 Code tip: Use DeepSeek-Coder or CodeLlama as base model"
    [[ "$task" == "instruct" || "$task" == "chat" ]] && \
        echo "💡 Chat tip: Start from an already instruction-tuned checkpoint"

    echo ""
    echo "Next: bash scripts/script.sh config --model llama3-8b --gpu ${gpu} --dataset 10000"
}

# ── cmd_help ──────────────────────────────────────────────────────────────────
cmd_help() {
    cat << 'EOF'
LoRA Toolkit — Configure and generate LoRA fine-tuning scripts for LLMs
Powered by BytesAgain | bytesagain.com

Commands:
  config      Generate recommended LoRA configuration
  estimate    Estimate training time and cloud cost
  generate    Generate a ready-to-run Python training script
  validate    Check dataset format (Alpaca/ShareGPT/OpenAI)
  recommend   Recommend base model for your hardware and task
  help        Show this help

Usage:
  bash scripts/script.sh config --model llama3-8b --gpu 24gb --dataset 10000
  bash scripts/script.sh estimate --model mistral-7b --gpu 16gb --dataset 5000 --epochs 3
  bash scripts/script.sh generate --model llama3-8b --output train.py
  bash scripts/script.sh validate --file dataset.json --format alpaca
  bash scripts/script.sh recommend --task chat --gpu 16gb --language en

Supported models:
  llama3-8b, llama3-70b, mistral-7b, mistral-8x7b,
  qwen2-7b, qwen2-72b, phi3-mini, phi3-medium, gemma2-9b, gemma2-27b

More AI agent skills: https://bytesagain.com/skills
Feedback: https://bytesagain.com/feedback/
EOF
}

# ── Router ────────────────────────────────────────────────────────────────────
case "${1:-help}" in
    config)    shift; cmd_config "$@" ;;
    estimate)  shift; cmd_estimate "$@" ;;
    generate)  shift; cmd_generate "$@" ;;
    validate)  shift; cmd_validate "$@" ;;
    recommend) shift; cmd_recommend "$@" ;;
    help|*)    cmd_help ;;
esac
