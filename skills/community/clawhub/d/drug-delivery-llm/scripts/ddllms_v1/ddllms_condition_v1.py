import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# === 调===
model_name = "laituan245/t5-v1_1-base-caption2smiles"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# === 条件===
prompt = "This molecule can be excited by visible light"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids  # Single sample
# === 生成===
print("Generating SMILES sequences...")
outputs = model.generate(
    input_ids,
    max_length=50,
    num_return_sequences=2000,
    no_repeat_ngram_size=2,
    top_k=50,
    top_p=0.9,
    temperature=1.0,
    do_sample=True,
    early_stopping=True
)
# === 解码===
t5_smiles = [
    tokenizer.decode(item, skip_special_tokens=True)
    for item in tqdm(outputs, desc="Decoding")
]
# === 存===
np.save("t5_generated_smiles.npy", t5_smiles)
print(f"Saved {len(t5_smiles)} SMILES strings to 't5_generated_smiles.npy'")