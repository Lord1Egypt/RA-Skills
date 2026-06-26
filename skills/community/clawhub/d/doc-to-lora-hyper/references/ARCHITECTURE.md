# Doc-to-LoRA Architecture

Paper: [Charakorn et al., Sakana AI, Feb 2026](https://arxiv.org/abs/2602.15902)

## The Problem

You have a document and want a model to "know" it. Three existing approaches:

| Approach | Drawback |
|----------|----------|
| **RAG** | Document eats up context window. Retrieval adds latency. Model can ignore long context. |
| **LoRA fine-tuning** | Takes hours of GPU time per document. Not practical for ad-hoc docs. |
| **Context distillation** | Must re-train per document. Same cost problem as LoRA. |

## D2L's Solution: A Hypernetwork

Train a hypernetwork **once** (80K steps, 8xA100). After that, any new document is internalized in **seconds** with a single forward pass.

## Pipeline

```
Document (text)
    |
    v
[Context Encoder] -- full Gemma 2B, extracts per-layer hidden states
    |                  Output: [1, 26 layers, seq_len, 2048]
    v
[Perceiver Aggregator] -- 9 cross-attention blocks
    |                      Compresses variable-length to fixed bottleneck
    |                      Output: [1, 26, 1, 8, 512]
    |                              (layers, modules, rank, latent_dim)
    v
[HyperLoRA Head] -- 4 ResMLPBlocks + EinMix projection
    |                Generates LoRA A and B matrices
    |                Output per layer: A=[8, 2048], B=[8, 8192]
    v
[Apply to Base Model] -- patches down_proj in each transformer layer
    |                     delta = x @ A^T @ B^T * scaling
    v
[Generate] -- base model answers questions with knowledge baked in
```

## Component Details

### Context Encoder
- Same architecture as base model (Gemma 2 2B)
- Loaded as a **separate copy** (frozen, no gradients)
- Uses `PerLayerActivations` strategy: extracts hidden states from ALL 26 layers
- This is why PyTorch path needs ~10GB: two copies of the 2B model

### Perceiver Aggregator
- Based on Idefics2 Perceiver Resampler
- 9 blocks of cross-attention (latent queries attend to encoder features) + self-attention
- Bottleneck: 8 latent queries per layer/module/rank combination
- Compresses up to 6144 tokens into fixed-size representation
- ~100M parameters

### HyperLoRA Head
- 4 ResMLPBlocks with per-layer weights (EinMix)
- Each block: LayerNorm -> Linear(512, 2048) -> SiLU -> Linear(2048, 512) -> LayerNorm + residual
- Final projection: latent (512) -> LoRA weights (2048 + 8192 = 10240 per layer)
- L2 normalization before projection
- Learnable bias_A, bias_B and scaler_A, scaler_B per rank
- ~20M parameters

### LoRA Application
- Target: `down_proj` only (MLP down-projection in each transformer layer)
- Rank: 8
- Alpha (scaling): r^1.5 * 2 = 8^1.5 * 2 = 45.25
- No dropout (generated weights are implicitly regularized)
- Applied via monkey-patching the forward method of each target Linear layer

## Memory Breakdown (fp16)

### PyTorch Path
| Component | RAM |
|-----------|-----|
| Base model (Gemma 2 2B) | ~5 GB |
| Context encoder (Gemma 2 2B copy) | ~5 GB |
| Perceiver + HyperLoRA | ~0.2 GB |
| Generated LoRA matrices (26 layers x rank 8) | ~0.005 GB |
| KV cache + activations | ~1 GB |
| **Total** | **~11 GB** |

### MLX Path (after export)
| Component | RAM |
|-----------|-----|
| Base model (Gemma 2 2B, MLX format) | ~5 GB |
| LoRA adapter (safetensors) | ~0.005 GB |
| KV cache | ~0.5 GB |
| **Total** | **~5.5 GB** |

The MLX path is cheaper because the hypernetwork + context encoder are only needed during the **export** step, not at query time.

## Training (for reference, not runnable on Mac)

- **Loss**: KL divergence distillation (student with LoRA vs teacher without LoRA, both seeing the document)
- **Data**: Self-generated QA pairs from documents (SQuAD, PwC, DROP, etc.)
- **Optimizer**: AdamW fused, lr=4e-5, cosine schedule
- **Hardware**: 8x A100 80GB, 80K steps
- **Trainable params**: ~120M (perceiver + hyperLoRA head only; base model and encoder frozen)

## Design Choices Explained

| Choice | Reason |
|--------|--------|
| Rank 8 | Higher rank = linearly more parameters for hypernet to generate. 8 is the sweet spot. |
| `down_proj` only | MLP down-projection captures most of the factual knowledge. Targeting all modules would 6x the hypernet output size. |
| Separate context encoder | Allows independent quantization/optimization. Could use a different (smaller) encoder in future. |
| Perceiver bottleneck | O(latent x seq_len) vs O(seq_len^2) for self-attention. Handles variable doc lengths. |
| L1 regularization (0.1) | Encourages sparse LoRA updates - most layers get near-zero changes, a few get targeted knowledge injection. |
| Per-layer processing | Each transformer layer gets its own processing in the ResMLPBlocks. Layer 3's needs differ from layer 25's. |

## Chunk Merging

For documents longer than 6144 tokens, D2L:
1. Splits into overlapping chunks
2. Generates separate LoRA weights per chunk
3. Merges via `combine_lora()`: concatenates A matrices along rank dimension, adds bias block
4. Final LoRA rank = (n_chunks + 1) * r (bias adds one extra rank block)
