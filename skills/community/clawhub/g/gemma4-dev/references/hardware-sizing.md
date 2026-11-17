# Gemma 4 Hardware Sizing & VRAM Matrix

This reference guides developers in selecting the optimal Gemma 4 model variant, quantization format, and hardware compute configuration.

---

## 1. VRAM & Hardware Footprint Matrix

| Model | Parameters | Context Window | FP16 (Unquantized) | 8-Bit (INT8 / BitsAndBytes) | 4-Bit (AWQ / GPTQ / GGUF) | Minimum Recommended Hardware |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E2B** | 2.3B | 128K | ~4.6 GB | ~2.5 GB | ~1.4 GB | Raspberry Pi 5 (8GB), iPhone / Android (NPU), WebGPU |
| **Gemma 4 E4B** | 4.2B | 128K | ~8.4 GB | ~4.5 GB | ~2.6 GB | Apple Silicon M-series (8GB+), RTX 3050 / 4050, Edge TPUs |
| **Gemma 4 12B** | 12.1B | 256K | ~24.2 GB | ~13.0 GB | ~7.2 GB | Single RTX 3060 / 4060 (8GB/12GB), Apple Silicon M-series (16GB+) |
| **Gemma 4 26B A4B** | 26.0B (MoE, 4B active) | 256K | ~52.0 GB | ~28.0 GB | ~15.5 GB | Single RTX 3090 / 4090 (24GB) or Apple Silicon (32GB+) |
| **Gemma 4 31B** | 30.8B (Dense) | 256K | ~62.0 GB | ~33.0 GB | ~18.5 GB | Dual RTX 3090 / 4090 (48GB), A100 / H100 (80GB) |
| **EmbeddingGemma** | 300M | 2K | ~600 MB | ~350 MB | ~200 MB | Any CPU / Mobile device / Micro-VM |
| **ShieldGemma 2** | 4.0B | 8K | ~8.0 GB | ~4.2 GB | ~2.4 GB | Integrated alongside primary LLM on 16GB+ VRAM |

---

## 2. KV Cache Considerations for Long Contexts

Gemma 4 supports up to 256K context tokens. While weight memory is static, KV cache memory scales linearly with sequence length:

- **KV Cache Allocation (FP16)**:
  - At **8K context**: < 0.5 GB VRAM.
  - At **64K context**: ~3–5 GB VRAM overhead.
  - At **128K context**: ~7–10 GB VRAM overhead.
  - At **256K context**: ~14–18 GB VRAM overhead.
- **Optimization Strategy**:
  - When running 12B or 26B models on consumer hardware (12GB–24GB VRAM) with long prompts (>64K tokens), enable **PagedAttention** (vLLM) or **FlashAttention-2 / FlashInfer**.
  - Quantize KV cache to FP8 or INT8 where supported to halve context memory overhead without measurable degradation.

---

## 3. Architecture Deep-Dive: 26B A4B MoE vs. 31B Dense

- **Gemma 4 26B A4B (Mixture-of-Experts)**:
  - Uses 26B total parameters across experts, but routes only **4B active parameters** per forward token.
  - Delivers inference generation speeds comparable to a 4B parameter model while achieving reasoning and coding benchmark scores close to the 31B dense variant.
  - Ideal for latency-critical agentic tool-calling loops and interactive coding agents.
- **Gemma 4 31B (Dense)**:
  - Activates all 31B parameters on every token.
  - Provides maximal deep reasoning and complex syntactic transformation, but requires higher memory bandwidth and compute throughput.
