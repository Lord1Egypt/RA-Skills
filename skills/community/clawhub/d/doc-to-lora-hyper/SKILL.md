---
name: doc-to-lora
description: >
  Internalize a document into a small language model (Gemma 2 2B) using Doc-to-LoRA
  so it can answer questions WITHOUT the document in the prompt. Use when the user
  wants to: feed a document to a local model, internalize knowledge from a file or
  URL, create a LoRA adapter from a document, answer questions from a document using
  a small on-device model, or run knowledge-grounded inference on a Mac. Also use
  when asked about Doc-to-LoRA, HyperLoRA, or document internalization.
license: MIT
compatibility: >
  macOS with Apple Silicon (M1+), 16GB+ RAM. Requires: Python 3.10+, uv package
  manager (https://docs.astral.sh/uv/), HF_TOKEN env var with Gemma model access
  (https://huggingface.co/google/gemma-2-2b-it), ~10GB disk for model weights.
  Works on CPU/MPS (no CUDA needed). MLX path recommended for Apple Silicon.
  This skill must be used inside a clone of the doc-to-lora repository
  (https://github.com/Manojbhat09/doc-to-lora-hyper-skill).
metadata:
  author: Manojbhat09
  version: "1.2.0"
  paper: "https://arxiv.org/abs/2602.15902"
  base-model: google/gemma-2-2b-it
  framework: pytorch,mlx
  openclaw:
    requires:
      env:
        - HF_TOKEN
      bins:
        - python3
        - uv
    os: darwin
---

# Doc-to-LoRA Skill

Internalize any document into a small model's weights in seconds. No fine-tuning
loop, no RAG retrieval at query time. The model "knows" the document.

## How It Works (30-second summary)

A trained **hypernetwork** reads your document and instantly generates LoRA adapter
weights for every layer of Gemma 2 2B. The adapter is applied to the base model,
which can then answer questions about the document without it being in the prompt.

```
Document --> Context Encoder --> Perceiver --> HyperLoRA --> LoRA weights
                                                                |
                                                    Apply to Gemma 2 2B
                                                                |
                                                    Answer questions (no doc in prompt)
```

For architecture details, read `references/ARCHITECTURE.md` in this skill directory.

## Security Notes

- **Checkpoint loading**: `internalize.py` uses `torch.load(weights_only=False)`
  because D2L checkpoints embed Python config dataclasses (AggregatorConfig,
  LoraConfig, HypernetConfig) alongside tensor weights. The upstream D2L project
  uses this format. **Only load checkpoints you trust.** The default checkpoint
  source is the official `SakanaAI/doc-to-lora` HuggingFace repository.
- **HF_TOKEN**: Required for downloading gated Gemma weights. This is a sensitive
  secret. The scripts only pass it to `huggingface-cli download` and
  `transformers` model loading. It is not sent anywhere else.
- **No remote code execution**: setup.sh does not download or execute remote
  scripts. It requires `uv` and `python3` to be pre-installed by the user.
  All dependency installation is done via `uv pip install` with pinned versions.
- **Checkpoint integrity**: After downloading, you can verify the checkpoint
  against the HuggingFace repo's commit hash. The download uses `huggingface-cli`
  which verifies checksums automatically.

## Prerequisites

This skill runs inside a clone of the **doc-to-lora repository**. It is not
a standalone tool.

Required before setup:
- `python3` (3.10+)
- `uv` package manager: https://docs.astral.sh/uv/getting-started/installation/
- `HF_TOKEN` env var: https://huggingface.co/settings/tokens (with Gemma access)
- Clone of the D2L repo with `install_mac.sh` present

Run setup once. This installs Python dependencies and downloads model weights
(~7GB total).

```bash
export HF_TOKEN=hf_your_token_here
bash ${CLAUDE_SKILL_DIR}/scripts/setup.sh
```

If setup was already completed, skip this step. Check with:
```bash
test -d trained_d2l/gemma_demo && echo "Weights present" || echo "Run setup first"
```

## Workflow A: PyTorch Path (simpler, ~10GB RAM)

Use this when the user provides a document and wants answers.
The `internalize.py` script handles both internalization and querying in one call.

### Internalize a document and ask questions

```bash
python ${CLAUDE_SKILL_DIR}/scripts/internalize.py \
  --input "path/to/document.txt" \
  --question "What is the main finding?" \
  --checkpoint trained_d2l/gemma_demo/checkpoint-80000/pytorch_model.bin
```

Or pass text directly:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/internalize.py \
  --text "Paste the document content here..." \
  --question "What is this about?"
```

For multiple questions, pass them comma-separated:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/internalize.py \
  --input "path/to/document.txt" \
  --question "Question 1?,Question 2?,Question 3?"
```

For programmatic use, output results as JSON:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/internalize.py \
  --input doc.txt --question "Q?" --output-json results.json
```

## Workflow B: MLX Path (faster, ~6GB RAM, recommended for Mac)

Use this for best performance on Apple Silicon. Two-phase: export once, query fast.

### Step 1: Export LoRA adapter from document

```bash
python scripts/export_d2l_to_mlx_adapter.py \
  --checkpoint trained_d2l/gemma_demo/checkpoint-80000/pytorch_model.bin \
  --context-file "path/to/document.txt" \
  --output-dir adapters_d2l
```

### Step 2: Query with MLX (lightweight, Metal-accelerated)

```bash
python ${CLAUDE_SKILL_DIR}/scripts/query_mlx.py \
  --adapter-dir adapters_d2l \
  --question "What is the main finding?"
```

## When to Use Which Path

| Scenario | Path | Why |
|----------|------|-----|
| Quick one-off question about a doc | PyTorch | Simpler, no export step |
| Many questions about the same doc | MLX | Export once, query fast and cheap |
| RAM-constrained (16GB Mac) | MLX | ~6GB vs ~10GB at query time |
| Multiple documents to compare | MLX | Export each, swap adapters instantly |

## Limitations

- **Base model**: Gemma 2 2B only (with released weights). Small model = limited reasoning.
- **Document length**: Up to ~6144 tokens (~4000-5000 words). Longer docs are chunked.
- **Training required for new base models**: The hypernetwork must be trained (8xA100 GPUs) to support a different base model. Inference is Mac-friendly.
- **Factual recall, not reasoning**: Best for "what does the doc say" questions, not deep multi-hop reasoning over the document.
- **No real-time updates**: Once internalized, the adapter is static. Change the doc = re-internalize.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'ctx_to_lora'` | Run setup: `bash ${CLAUDE_SKILL_DIR}/scripts/setup.sh` |
| `FileNotFoundError: trained_d2l/...` | Download weights: `uv run huggingface-cli download SakanaAI/doc-to-lora --local-dir trained_d2l` |
| `FileNotFoundError: install_mac.sh` | This skill must be used inside a doc-to-lora repo clone that contains `install_mac.sh` |
| `RuntimeError: MPS backend out of memory` | Use MLX path instead, or close other apps |
| `ImportError: bitsandbytes` | Expected on Mac. The scripts auto-disable quantization on non-CUDA. |
| Answers seem wrong / generic | Check if LoRA is applied: outputs should differ from baseline. Try rephrasing. |
