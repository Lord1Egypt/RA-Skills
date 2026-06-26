# doc-to-lora

An [Agent Skill](https://agentskills.io) that lets AI agents internalize documents into a small language model (Gemma 2 2B) using [Doc-to-LoRA](https://arxiv.org/abs/2602.15902). The model can then answer questions about the document **without it being in the prompt**.

Works on any 16GB+ Mac with Apple Silicon.

## What This Does

```
Your document  -->  HyperNetwork (single forward pass)  -->  LoRA adapter weights
                                                                      |
                                                           Applied to Gemma 2 2B
                                                                      |
                                                           Answers questions
                                                           (no document in prompt)
```

Unlike RAG (which pastes chunks into the prompt) or LoRA fine-tuning (which takes hours), Doc-to-LoRA generates adapter weights in **seconds** via a trained hypernetwork.

## Install

### For Claude Code
```bash
# Project-level
cp -R . /path/to/your/project/.claude/skills/doc-to-lora

# Or personal (all projects)
cp -R . ~/.claude/skills/doc-to-lora
```

### For OpenClaw
```bash
cp -R . ~/.openclaw/skills/doc-to-lora
```

### For GitHub Copilot
```bash
cp -R . /path/to/your/project/.github/skills/doc-to-lora
```

### From skills.sh
```bash
npx skills add <owner>/doc-to-lora-skill
```

## Quick Start

Once installed, any compatible agent can use the skill. Just tell it:

> "Internalize this document and answer questions about it using doc-to-lora"

Or manually:

```bash
# 1. Setup (once)
bash scripts/setup.sh

# 2. Internalize a document and ask questions
python scripts/internalize.py \
  --input my_document.txt \
  --question "What is the main topic?"

# 3. Or use MLX for faster inference on Apple Silicon (~6GB RAM)
python scripts/export_d2l_to_mlx_adapter.py \
  --context-file my_document.txt \
  --output-dir adapters_d2l

python scripts/query_mlx.py \
  --adapter-dir adapters_d2l \
  --question "What is the main topic?"
```

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4), 16GB+ RAM
- Python 3.10+
- ~10GB disk (model weights + dependencies)
- HuggingFace account with [Gemma access](https://huggingface.co/google/gemma-2-2b-it)

## How It Works

A **hypernetwork** (trained once by [Sakana AI](https://sakana.ai) on 8xA100 GPUs) learns to generate LoRA adapter weights from any document:

1. **Context Encoder** extracts per-layer features from the document
2. **Perceiver Aggregator** compresses variable-length input to a fixed bottleneck
3. **HyperLoRA Head** projects the bottleneck into LoRA A/B matrices for every layer
4. The generated LoRA is applied to Gemma 2 2B's `down_proj` layers

See [references/ARCHITECTURE.md](references/ARCHITECTURE.md) for the full technical breakdown.

## Memory Usage

| Path | RAM at query time | Best for |
|------|-------------------|----------|
| PyTorch (MPS) | ~10-11 GB | Quick one-off queries |
| MLX (Metal) | ~5-6 GB | Repeated queries, tight RAM |

The PyTorch path loads two copies of Gemma 2B (base + context encoder). The MLX path only needs one copy after the adapter is exported.

## Limitations

- Base model is Gemma 2 2B (small model = limited reasoning)
- Max document length ~5000 words (longer docs are chunked)
- Best for factual recall, not deep multi-hop reasoning
- Training a new hypernetwork for a different base model requires 8xA100 GPUs

## Credits

- Paper: [Doc-to-LoRA](https://arxiv.org/abs/2602.15902) by Charakorn et al., Sakana AI (2026)
- Model weights: [SakanaAI/doc-to-lora](https://huggingface.co/SakanaAI/doc-to-lora)
- Skill format: [Agent Skills specification](https://agentskills.io/specification)

## License

MIT
