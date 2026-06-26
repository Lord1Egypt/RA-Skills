# Claw Compactor Documentation
> **Open-source LLM token compression for AI agents - reduce costs by up to 97%**

## What is LLM Token Compression?
LLM token compression is the process of reducing the number of tokens sent to large language models (like GPT-4, Claude, Gemini, or Llama) without losing the meaning or critical information in the context. Every token costs money - and as AI agents work with larger context windows (100K+ tokens), those costs add up fast.

**Claw Compactor** solves this by compressing workspace files, memory, session transcripts, and prompt context *before* they reach the LLM. The result: same AI quality, dramatically lower cost.

## How Does Claw Compactor Work?
Claw Compactor uses a **5-layer deterministic compression pipeline** that processes text through increasingly aggressive optimization stages:

1. **Rule Engine (L1)** - Removes duplicate lines, strips markdown filler, merges redundant sections. Fully lossless. Typical savings: 4–8%.

2. **Dictionary Encoding (L2)** - Learns a codebook of frequently repeated phrases and replaces them with short `$XX` codes. Fully lossless with roundtrip decompression. Typical savings: 4–5%.

3. **Observation Compression (L3)** - Converts raw session transcripts (often 100K+ tokens of JSONL) into structured 3K-token summaries. This is where the 97% savings come from.

4. **RLE Patterns (L4)** - Replaces common patterns like file paths, IP addresses, and enumerated lists with shorthand notation. Fully lossless. Typical savings: 1–2%.

5. **Compressed Context Protocol (L5)** - Applies format-level abbreviation at ultra/medium/light levels. Typical savings: 20–60%.

An optional **Layer 6 (Engram)** uses LLM calls to build real-time Observational Memory - a live knowledge base that auto-compresses conversations into structured, priority-annotated observations.

## Getting Started
```bash

# Clone the repository
git clone https://github.com/aeromomo/claw-compactor.git
cd claw-compactor

# Run a non-destructive benchmark
python3 scripts/mem_compress.py /path/to/workspace benchmark

# Run full compression pipeline
python3 scripts/mem_compress.py /path/to/workspace full

# Auto-compress on file changes
python3 scripts/mem_compress.py /path/to/workspace auto
```

## How to Reduce LLM API Costs
If you're spending hundreds or thousands of dollars per month on LLM API calls, here are the most effective strategies:

### 1. Compress Your Context (Claw Compactor)
Use Claw Compactor to reduce the token count of everything loaded into context - memory files, session history, workspace documentation. This is the highest-impact optimization because it reduces *every* API call.

### 2. Enable Prompt Caching
Most LLM providers (Anthropic, OpenAI) offer prompt caching that reduces cost by 90% for cached prefix tokens. Combine with Claw Compactor for compound savings:
- 50% token reduction (compression) × 90% cache discount = **95% effective cost reduction**

### 3. Use Tiered Context Loading
Instead of loading full files, use Claw Compactor's tiered summaries:
- **L0** (~200 tokens) - Ultra-compressed executive summary
- **L1** (~500 tokens) - Key facts and decisions
- **L2** (full) - Complete context when needed

### 4. Optimize Token Formats
Claw Compactor's tokenizer optimizer reformats text to be more token-efficient - for example, restructuring whitespace and punctuation patterns that waste tokens.

## Token Compression for Different LLM Providers
Claw Compactor works with any LLM that accepts text input:

**OpenAI**, Models=GPT-4, GPT-4o, GPT-3.5, Compatible=
**Anthropic**, Models=Claude 3.5, Claude Opus, Claude Sonnet, Compatible=
**Google**, Models=Gemini Pro, Gemini Ultra, Compatible=
**Meta**, Models=Llama 3, Llama 2, Compatible=
**Mistral**, Models=Mistral Large, Mixtral, Compatible=
**Local LLMs**, Models=Ollama, llama.cpp, vLLM, Compatible=

## Frequently Asked Questions

### How much money can I save with token compression?
Typical savings: 50–70% on first run. For autonomous agents running 24/7, this can mean saving $5,000–$8,000/month on a $10,000 bill.

### Does compression affect AI response quality?
The 3 lossless layers (L1, L2, L4) have zero impact on quality. The lossy layers (L3, L5) preserve all facts, decisions, and context - only verbose formatting is removed.

### Can I use Claw Compactor without OpenClaw?
Yes. Claw Compactor is a standalone Python tool. OpenClaw integration (hooks, auto-compress) is optional.

### What about Chinese/Japanese/Korean text?
Full CJK support including character-aware token estimation and Chinese punctuation normalization.

## Links
- [GitHub Repository](https://github.com/aeromomo/claw-compactor), [Benchmark Results](benchmarks.md), [OpenClaw Platform](https://openclaw.ai), [Community Discord](https://discord.com/invite/clawd), [Skill Reference](../SKILL.md)