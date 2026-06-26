# S2 Pro Architecture

Source: [arXiv:2603.08823](https://arxiv.org/abs/2603.08823)

## Pipeline

Text Preprocessing → Dual-AR Generation → DAC Vocoder Decoding

## Audio Tokenizer (DAC-based)

- 10-layer RVQ (N=10), layer 0 = semantic codebook, layers 1-9 = acoustic details
- Fully causal convolution + Transformer bottleneck
- 512× (DAC) + 4× (ConvNeXt V2) = 2048× downsampling, ~21 Hz frame rate
- EVA-GAN decoder with semantic distillation (w2v-BERT 2.0 layer 16)
- Total parameters: 446M

## Dual-AR

**Slow AR:** Qwen3-4B, autoregressively predicts semantic codebook q_t^(0) along the time axis, interleaving text + audio tokens

**Fast AR:** 4-layer lightweight Transformer, generates remaining 9 acoustic codebooks autoregressively in depth after each Slow AR step, conditioned on h_slow_t, sharing embedding table + RoPE for hierarchy differentiation

**MCF:** x_{t+1} = e^{LM}_t + Σ_{k=0}^{9} E^{(k)}[q_t^{(k)}]

## Data Pipeline

1. Vocal separation → VAD segmentation
2. Quality filtering (Uni-VERSA + w2v-BERT 2.0: SNR/speaker consistency/recording quality/intelligibility)
3. Rich transcription (Qwen3-Omni-30B-A3B ASR: text + speaker switching + characteristic tags)

## Training (Four Stages)

1. Audio tokenizer ~1M steps (composite GAN loss)
2. Pre-training 1: Cross-modal alignment, context 8192 tokens
3. Pre-training 2: Context extension to 16384
4. SFT + GRPO RL alignment

**GRPO rewards:** Semantic accuracy (ASR re-transcription comparison), acoustic quality, speaker similarity, instruction following

## SGLang Acceleration

| Technique | Description |
|-----------|-------------|
| Paged KV Cache | Slow AR KV management |
| RadixAttention | Prefix caching for system prompts/reference audio |
| CUDA Graph | Full coverage of Fast AR's 9 steps |
| FlashAttention 3 | Matches training precision |
| Continuous Batching | Continuous batch processing |

## Performance (Single H200)

| Metric | Value |
|--------|-------|
| RTF | 0.195 |
| TTFA | ~100ms |
| Throughput | 3000+ t/s |

## Benchmarks

- Seed-TTS Eval WER: Chinese 0.54%, English 0.99% (best)
- Audio Turing Test: 0.515 posterior mean
- EmergentTTS-Eval Win Rate: 81.88%
- Fish Instruction Benchmark TAR: 93.3%, Quality 4.51/5.0
- Multilingual Best WER: 11/24, Best SIM: 17/24