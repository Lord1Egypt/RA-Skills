import os
import torch
import numpy as np
import tqdm
from dd_tokenzier_base_v1 import SMILESBPETokenizer
from transformers import (
    Gemma2ForCausalLM,
    GPTNeoXForCausalLM,
    OlmoeForCausalLM,
    Qwen3MoeForCausalLM,
    DeepseekV3ForCausalLM,
    GraniteMoeForCausalLM,
    GPT2LMHeadModel,
    GemmaForCausalLM,
)
from peft import PeftModel
# === Configuration ===
MODEL_CLASSES = {
    "gemma2": Gemma2ForCausalLM,
    "gptneox": GPTNeoXForCausalLM,
    "ol": OlmoeForCausalLM,
    "qwen3": Qwen3MoeForCausalLM,
    "dpv3": DeepseekV3ForCausalLM,
    "granite": GraniteMoeForCausalLM,
    "gpt2": GPT2LMHeadModel,
    "gemma": GemmaForCausalLM,
}
# 超参
hyperparams = {
    "max_length": 64,
    "weight_decay": 0.0,
    "scheduler_T_max": 150_000,
    "min_frequency": 2,
    "top_p": 0.96,
    "n_generate": 1000,
}
def load_model(model_type, model_path, lora_path=None):
    print(f"Loading base model: {model_type} from {model_path}")
    model_cls = MODEL_CLASSES[model_type]
    model = model_cls.from_pretrained(model_path, output_attentions=False)
    if lora_path:
        print(f"Applying LoRA weights from: {lora_path}")
        model = PeftModel.from_pretrained(model, lora_path)
        model = model.merge_and_unload()
    return model
def generate_smiles(model, tokenizer, output_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    generated_smiles_list = []
    for _ in tqdm.tqdm(range(hyperparams["n_generate"]), desc="Generating"):
        input_ids = torch.LongTensor([[tokenizer.bos_token_id]]).to(device)
        generated_ids = model.generate(
            input_ids,
            max_length=hyperparams["max_length"],
            do_sample=True,
            top_p=hyperparams["top_p"],
            pad_token_id=tokenizer.eos_token_id,
        )
        smiles = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        print(smiles)
        generated_smiles_list.append(smiles)
    np.save(output_file, generated_smiles_list)
    print(f"Saved {len(generated_smiles_list)} SMILES to {output_file}")
def run(
    model_type,
    model_dir,
    tokenizer_path,
    output_file,
    lora_path=None,
):
    tokenizer = SMILESBPETokenizer.get_hf_tokenizer(
        tokenizer_path, model_max_length=hyperparams["max_length"]
    )
    print(f"Tokenizer vocab size: {tokenizer.vocab_size}")
    model = load_model(model_type=model_type, model_path=model_dir, lora_path=lora_path)
    generate_smiles(model, tokenizer, output_file)
if __name__ == "__main__":
    # === Dense Gemma2 1===
    run(
        model_type="gemma2",
        model_dir="checkpoints/250k/model",
        tokenizer_path="checkpoints/250k/tokenizer.json",
        output_file="gemma2-smi1k-dense2-ppl446.npy",
    )
    # === Gemma2 with LoRA ===
    run(
        model_type="gemma2",
        model_dir="checkpoints/d1rlhf/model-dense1",
        tokenizer_path="checkpoints/d1rlhf/tokenizer.json",
        lora_path="checkpoints/d1rlhf/model-lora-b256",
        output_file="gemma2-smi1k-d1b256.npy",
    )
    # === GPT2 base 2===
    run(
        model_type="gpt2",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        output_file="gpt2-smi1k-base.npy",
    )
    # ===GPT2 with LoRA ===
    run(
        model_type="gpt2",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        lora_path=model_dir="checkpoints/YOUR_LORA_PATH",
        output_file="gpt2-smi1k-d2lora.npy",
    )
    # === Gemma base 3===
    run(
        model_type="gemma",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        output_file="gpt2-smi1k-base.npy",
    )
    # ===Gemma with LoRA ===
    run(
        model_type="gemma",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        lora_path=model_dir="checkpoints/YOUR_LORA_PATH",
        output_file="gpt2-smi1k-d2lora.npy",
    )
    # === Qwen3 base 4===
    run(
        model_type="qwen3",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        output_file="gpt2-smi1k-base.npy",
    )
    # ===Qwen3 with LoRA ===
    run(
        model_type="qwen3",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        lora_path=model_dir="checkpoints/YOUR_LORA_PATH",
        output_file="gpt2-smi1k-d2lora.npy",
    )
    # === DeepSeek base 5===
    run(
        model_type="dpv3",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        output_file="gpt2-smi1k-base.npy",
    )
    # ===DeepSeek with LoRA ===
    run(
        model_type="dpv3",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        lora_path=model_dir="checkpoints/YOUR_LORA_PATH",
        output_file="gpt2-smi1k-d2lora.npy",
    )
    # === GPTNeoX base 6===
    run(
        model_type="gptneox",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        output_file="gpt2-smi1k-base.npy",
    )
    # ===GPTNeoX with LoRA ===
    run(
        model_type="gptneox",
        model_dir="checkpoints/YOUR_MODEL_PATH",
        tokenizer_path="YOUR_TOKENIZER_FILE.json",
        lora_path=model_dir="checkpoints/YOUR_LORA_PATH",
        output_file="gpt2-smi1k-d2lora.npy",
    )