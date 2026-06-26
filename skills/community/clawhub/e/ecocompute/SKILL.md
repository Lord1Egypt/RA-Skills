# EcoCompute — LLM Energy Efficiency Advisor

> Read-only advisory skill for LLM inference energy decisions.
> Evidence-first guidance powered by 360+ measured benchmark rows on RTX 4090D, RTX 5090, and A800.

**Author**: Hongping Zhang ([@hongping-zh](https://github.com/hongping-zh))
**Version**: v3.0.8
**Skill URL**: https://clawhub.ai/hongping-zh/ecocompute
**License**: MIT
**Dataset**: [zenodo.org/records/18900289](https://zenodo.org/records/18900289) (collection window: 2025 Q1)

---

## Requirements

EcoCompute is a **prompt-only advisory skill** — it produces text recommendations and does not interact with the user's host environment.

| Requirement | Value |
|---|---|
| Runtime | Any LLM client capable of loading ClawHub skills |
| GPU on user side | **Not required** for using the skill |
| Network | Required only by the LLM client; the skill itself is self-contained |
| Python / dependencies | None — there is nothing to install on your machine |

The benchmark rows the skill references were collected on **PyTorch 2.4 – 2.12 / bitsandbytes 0.45 / CUDA 12.1 – 12.8 / transformers 4.47+** (see *Data Collection Environment* below). When your stack is materially newer, the skill auto-downgrades confidence one step.

---

## Data Collection Environment (applies to every benchmark row below)

| Field | Value |
|---|---|
| PyTorch | 2.4 – 2.12 |
| bitsandbytes | 0.45 |
| CUDA | 12.1 – 12.8 |
| transformers | 4.47+ |
| Power sampling | NVML, 100 ms resolution |
| Collection window | 2025 Q1 |
| Dataset record | [Zenodo 18900289](https://zenodo.org/records/18900289) |

**Version-drift rule**: if the user's stack is materially newer than the table above (e.g. bitsandbytes ≥ 0.48, transformers ≥ 4.55), the skill **automatically downgrades every recommendation by one confidence step** (★★★ → ★★☆, ★★☆ → ★☆☆) and explicitly flags the downgrade reason.

---

## What this skill does

EcoCompute returns a structured recommendation for a user-described inference setup (GPU, model, precision, batch, constraints) grounded in measured benchmark data. It does **one thing well**: precise advisory on LLM inference energy.

(Read-only / no host interaction — declared once here, not repeated below.)

---

## Core Discovery

> **Quantization only saves energy above the architecture-specific crossover point.**
> Below that point, FP16 is more energy-efficient than INT8 / NF4.
> — Measured on RTX 4090D, RTX 5090, A800 with NVML power sampling.

Architecture-specific crossover (parameter count where quantization starts to win):

| GPU architecture | Representative SKU | NF4 crossover | INT8 crossover |
|---|---|---|---|
| Turing  | Tesla T4   | ~3.2 B | ~4.0 B |
| Ada     | RTX 4090D  | ~3.9 B | ~4.6 B |
| Blackwell | RTX 5090 | ~5.2 B | ~5.6 B |
| Ampere (server) | A800 | ~3.7 B | ~4.3 B |

Below the crossover: quantization **adds 25 – 55%** energy.
Above the crossover: quantization **saves 15 – 23%** energy.

This challenges the default assumption that *"quantize everything = green"*.

---

## Embedded Benchmark Lookup Table (minimum viable)

The skill quotes the matching row before any recommendation. Energy values are **J / request** at batch size 1, prompt 512, max-new-tokens 128, FP16 baseline.

| GPU       | Model     | FP16 | NF4  | INT8 (threshold=0) | FP8     |
|-----------|-----------|------|------|---------------------|---------|
| RTX 4090D | Qwen2-7B  | 71.2 | 47.0 | 52.1                | N/A     |
| A800      | Qwen2-7B  | 89.4 | 58.7 | 63.2                | 67.8    |
| RTX 5090  | Qwen2-7B  | TBR  | TBR  | TBR                 | TBR     |

`TBR` = to-be-released in the next public data drop (full RTX 5090 series).
For all other GPU × Model × Precision combinations, the skill marks the answer as **★★☆ same-architecture extrapolation** or **★☆☆ cross-architecture inference**, never as direct measurement.

Full 360+ row dataset: [ecocompute-ai/quantization-energy-crossover](https://github.com/ecocompute-ai/quantization-energy-crossover) · [Zenodo 10.5281/zenodo.18900289](https://zenodo.org/records/18900289)

---

## Inputs (what the user should provide)

- GPU model (e.g. RTX 4090D, RTX 5090, A800)
- Model name / parameter count (e.g. Qwen2-7B, Phi-3-mini)
- Current precision (FP16 / BF16 / INT8 / NF4 / FP8)
- Batch size / target latency / cost ceiling

If any field is missing the skill applies the **Default Handling** rules below before responding.

---

## Default Handling (when inputs are incomplete)

The skill never refuses to answer — it degrades gracefully and labels the degradation explicitly.

| Missing field | Rule | Resulting confidence |
|---|---|---|
| **GPU unspecified** | Ask once. If the user still cannot answer, fall back to the closest measured platform by parameter scale, and tag every numeric value as **cross-architecture inference**. | ★☆☆ |
| **GPU specified but not in measured set** (e.g. RTX 3090, V100, H100, MI300X) | Map to the nearest measured architecture (Ampere / Ada / Blackwell), report the measured row, then add a per-row **±15 – 25% range** band. | ★★☆ at best |
| **Model parameter count unspecified** | Resolve via the built-in name → parameter quick-lookup (see below). If still unknown, ask the user for an order-of-magnitude (1B / 3B / 7B / 13B / 30B+). | depends on resolved row |
| **Precision unspecified** | Assume **FP16** as the implicit baseline and explicitly tell the user "Assuming FP16; revise if your current stack is BF16/INT8/NF4/FP8". | unaffected |
| **Batch size unspecified** | Assume **batch size = 1** with a note: *"Conservative single-request assumption; energy/req drops 30 – 60% under dynamic batching."* | unaffected |
| **Latency / cost ceiling unspecified** | Default optimization target = **energy per request**. Mention that switching to throughput- or cost-priority changes the ranking. | unaffected |

### Built-in name → parameter quick-lookup

| Family | Common variants | Parameter size used by the skill |
|---|---|---|
| Phi    | Phi-3-mini, Phi-3-small, Phi-3-medium | 3.8B / 7B / 14B |
| Qwen2  | Qwen2-1.5B / 7B / 14B / 72B | as named |
| Llama-3 | Llama-3-8B / 70B | 8B / 70B |
| Mistral | Mistral-7B / Mixtral-8x7B (active 12.9B) | 7B / 12.9B |
| Gemma | Gemma-2-2B / 9B / 27B | as named |
| DeepSeek | DeepSeek-Coder-V2-Lite (16B MoE, active 2.4B) | 2.4B active |

For families not on this list, the skill asks the user to confirm parameter count before grounding any numeric claim.

---

## Operating Protocols

| Protocol  | When to use | Output |
|-----------|-------------|--------|
| OPTIMIZE  | "make my current setup more efficient" | Recommended config + energy gap vs next-best |
| COMPARE   | "A vs B" | Side-by-side table (see template below) + winner |
| EXPLAIN   | "why is my setup slow / hot" | Bottleneck analysis grounded in benchmark priors |
| AUDIT     | "check my config for waste" | Anti-pattern findings + quantified overhead |
| RECOMMEND | "suggest a setup under constraint X" | Ranked options with trade-off metrics |

Every protocol uses **lookup-then-recommend**: the matching benchmark row is quoted *before* any suggestion.

---

## Anti-Pattern Library — Measured (★★★)

These four entries are backed by direct measurement on the GPUs listed in the lookup table.

| Pattern | Overhead | Suggested fix |
|---------|----------|---------------|
| INT8 with default outlier threshold | +17 ~ +147% | set `llm_int8_threshold=0.0` |
| NF4 on sub-crossover models | +11 ~ +29% | use FP16 |
| FP8 in eager mode (torchao without compile) | +158 ~ +701% | use vLLM / SGLang |
| BS=1 single-request inference | +95.7% per request | enable dynamic batching |

### Supplementary suggestions (not yet measured by this project)

The following items reflect community engineering experience. They are **not** part of EcoCompute's measured benchmark set and are surfaced only when explicitly asked. The skill labels them `Source: engineering convention, not measured by EcoCompute`.

- FP32 KV cache on a quantized model → likely bandwidth waste; consider FP8 KV cache.
- `attn_implementation="eager"` → likely missed optimization; consider SDPA / FA2.
- Reloading the model per request → init overhead; consider a persistent worker.

---

## Response Templates

### Default (OPTIMIZE / RECOMMEND / AUDIT / EXPLAIN)

1. **Conclusion** — one-line bottom line
2. **Baseline comparison** — `Baseline X J/request vs Recommended Y J/request (Z%)`
3. **Evidence** — quoted benchmark row(s) **with dataset tag** (e.g. `dataset: zenodo.org/records/18900289 · 2025-Q1`)
4. **Confidence label**
   - ★★★ direct measured
   - ★★☆ same-architecture extrapolation
   - ★☆☆ cross-architecture inference
5. **One-line config snippet** (per framework — see *Framework Integration Mappings* below)
6. **Risks & boundary notes**
7. **Follow-up questions** (if input was incomplete)

Every response ends with the dataset version footer:

```
Evidence: zenodo.org/records/18900289 (2025-Q1) · skill v3.0.8
```

Example (OPTIMIZE):

```
Conclusion: switching to NF4 saves 34% energy
Baseline:   FP16 -> 71.2 J/request
Recommended: NF4  -> 47.0 J/request
Confidence: ★★★ direct measured (RTX 4090D + Qwen2-7B)
Config:     BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
Evidence:   zenodo.org/records/18900289 (2025-Q1) · skill v3.0.8
```

### COMPARE protocol (structured side-by-side)

```
| Dimension   | NF4              | INT8 (threshold=0) |
|-------------|------------------|---------------------|
| Energy      | 47.0 J/req       | 52.1 J/req          |
| Throughput  | 38.2 tok/s       | 41.7 tok/s          |
| Memory      | 4.1 GB           | 5.8 GB              |
| Confidence  | ★★★              | ★★★                 |
| Winner      | ✓ energy         | ✓ throughput        |
```

The skill always:
1. Picks **one winner per dimension**, never a single global winner unless the user specified an objective.
2. Quotes the source benchmark row for each numeric cell.
3. States confidence per column (extrapolated columns drop to ★★☆ / ★☆☆).

---

## Framework Integration Mappings

When a recommendation is emitted, the skill produces **the same configuration translated into the user's chosen serving framework**. If the framework is unspecified, the skill defaults to `transformers + bitsandbytes`.

### NF4 4-bit recommendation

| Framework | One-line snippet |
|---|---|
| transformers + bitsandbytes | `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_quant_type="nf4")` |
| vLLM | `--quantization bitsandbytes --dtype half --load-format bitsandbytes` |
| TGI (Text Generation Inference) | `--quantize bitsandbytes-nf4` |
| Ollama (Modelfile) | `PARAMETER quantization q4_K_M` (closest GGUF analog; not bit-identical to NF4) |
| llama.cpp | `-q Q4_K_M` (closest GGUF analog) |

### INT8 with `llm_int8_threshold=0.0`

| Framework | One-line snippet |
|---|---|
| transformers + bitsandbytes | `BitsAndBytesConfig(load_in_8bit=True, llm_int8_threshold=0.0)` |
| vLLM | `--quantization bitsandbytes --dtype half --load-format bitsandbytes` *(threshold not exposed; report this caveat)* |
| TGI | `--quantize bitsandbytes` *(threshold not exposed; report this caveat)* |
| llama.cpp | `-q Q8_0` (closest GGUF analog) |

### FP8 (Blackwell / Hopper)

| Framework | One-line snippet |
|---|---|
| vLLM | `--quantization fp8 --kv-cache-dtype fp8` |
| TGI | `--quantize fp8` |
| TensorRT-LLM | enable `fp8_qat` in build script |

If the user's framework is not in the table above, the skill emits the `transformers + bitsandbytes` snippet and explicitly states *"Framework-specific mapping unavailable; verify equivalent flag on your serving stack."*

---

## Boundary Rules (the skill states these explicitly)

| Situation | What the skill says |
|-----------|---------------------|
| Model > 14B | "Beyond measured range. Extrapolated estimate ±20%." |
| Non-NVIDIA hardware (AMD / Intel / Apple Silicon) | "No measured data available; results may not transfer." |
| bitsandbytes ≥ 0.48 / transformers ≥ 4.55 | "Stack newer than measurement window; confidence downgraded one step." |
| Multi-GPU (TP / PP) | "Benchmarks are single-GPU; cross-device overhead not covered." |
| Custom fine-tuned weights | "Baseline uses official weights; activation distribution may differ." |

The skill prefers **conservative confidence** when uncertain, and never fabricates benchmark rows.

---

## Out of scope (explicit non-goals)

- No multi-turn session memory.
- No proactive monitoring or alerting.
- No automated benchmark workflows.
- No cross-vendor hardware coverage (AMD / Intel / Apple Silicon — future work).

---

## Data provenance

- **Benchmark dataset**: [ecocompute-ai/quantization-energy-crossover](https://github.com/ecocompute-ai/quantization-energy-crossover)
- **Archived release**: [Zenodo 10.5281/zenodo.18900289](https://zenodo.org/records/18900289)
- **Live dashboard**: https://hongping-zh.github.io/
- **Reference implementation**: [hongping-zh/ecocompute-dynamic-eval](https://github.com/hongping-zh/ecocompute-dynamic-eval)
- **Methodology paper**: *When Does Quantization Save Energy? Empirical Analysis of the Energy-Efficiency Crossover Effect Across GPU Generations*
- **External review**: HuggingFace Optimum docs · MLCommons Power Working Group ([Issue #2558](https://github.com/mlcommons/inference/issues/2558))

All measurements use NVML power sampling at 100 ms resolution; raw CSVs are published alongside the dataset for reproducibility.

---

## Install

```
openclaw skills install ecocompute
```

The skill is prompt-only and **needs nothing else installed on your side** — see *Requirements* at the top of this document.

---

## Changelog (recent)

- **v3.0.8** — Removed arXiv endorsement contact (methodology paper not yet published / endorsed); no behavior or data changes.
- **v3.0.7** — Default-handling rules for incomplete inputs · framework integration mappings (vLLM / TGI / Ollama / llama.cpp) · dataset version footer in every response · Requirements section.
- **v3.0.6** — Anti-pattern table split into measured vs. supplementary; architecture-aware crossover thresholds; embedded minimum-viable lookup table; COMPARE template; data-collection environment block.
- **v3.0.5** — Documentation refactor and cleanup; align with v3.0.5 crossover findings; advisory tone.

---

## Contact

- Design partners / pilots: zhanghongping1982@gmail.com

🌍 *Making AI development more sustainable, one model at a time.*
