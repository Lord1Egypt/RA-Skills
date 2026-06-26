---
name: deepseek-v4
version: 1.0.0
author: jiajiaoy
homepage: https://clawhub.ai/skills/deepseek-v4
description: "Use DeepSeek V4 (Flash & Pro) from the command line — one-shot Q&A, thinking mode, multi-turn chat. OpenAI-compatible API, no special CLI needed. Supports deepseek-v4-flash and deepseek-v4-pro."
keywords:
  - deepseek
  - deepseek v4
  - deepseek-v4-flash
  - deepseek-v4-pro
  - deepseek api
  - deepseek cli
  - deepseek chat
  - deepseek reasoning
  - deepseek thinking mode
  - LLM cli
  - AI cli
  - cheap LLM
  - fast LLM
  - openai compatible
  - chinese AI
  - open source LLM
  - deepseek v4 flash
  - deepseek v4 pro
  - AI model
  - LLM api
  - deepseek-reasoner
  - deepseek-chat
  - AI assistant cli
  - command line AI
  - 深度求索
  - DeepSeek接口
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["uv"],"env":["DEEPSEEK_API_KEY"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# DeepSeek V4

Use DeepSeek V4 Flash and Pro directly from your terminal — one-shot questions, deep reasoning with thinking mode, and multi-turn chat. No special CLI required; uses the OpenAI-compatible API via a small Python script.

## Setup

**1. Get API key:** https://platform.deepseek.com/api_keys

**2. Set environment variable:**
```bash
export DEEPSEEK_API_KEY=your_key_here
# Add to ~/.zshrc or ~/.bashrc to persist
```

## Models

| Model | ID | Best for | Price (input/output) |
|-------|----|----------|---------------------|
| V4 Flash ⚡ | `deepseek-v4-flash` | Q&A, writing, coding, summaries | $0.014 / $0.028 per 1M |
| V4 Pro 🚀 | `deepseek-v4-pro` | Hard reasoning, math, deep analysis | $0.174 / $0.348 per 1M |

Both support **1M token context**. Cache hits are 10× cheaper.

Legacy aliases (`deepseek-chat` → flash, `deepseek-reasoner` → pro) deprecated 2026-07-24.

## Commands

### One-shot question (Flash — fast & cheap)
```bash
uv run {baseDir}/scripts/ask.py "Explain the difference between V4 Flash and V4 Pro"
```

### One-shot with Pro model
```bash
uv run {baseDir}/scripts/ask.py "Write a merge sort in Rust" --model pro
```

### Thinking mode (Pro with visible reasoning trace)
```bash
uv run {baseDir}/scripts/ask.py "Prove that there are infinitely many primes" --think
```

### Multi-turn chat
```bash
uv run {baseDir}/scripts/chat.py --model flash
uv run {baseDir}/scripts/chat.py --model pro --think
```

### Show models & pricing
```bash
uv run {baseDir}/scripts/models.py
```

## Model Selection Guide

Use **Flash** when:
- Everyday Q&A and explanations
- Writing, editing, translation
- Code generation and review
- Summarization and classification
- Cost is a priority

Use **Pro** when:
- Multi-step math or logic problems
- Complex debugging or architecture decisions
- Deep research and analysis
- You want to see the reasoning process (--think)

## Tips

- **Thinking mode** (`--think`) streams the internal reasoning before the final answer — useful for hard problems and to verify correctness
- **System prompt**: `--system "You are a concise assistant"` to set tone
- **No streaming**: `--no-stream` for cleaner output in scripts
- DeepSeek's API is OpenAI-compatible — any OpenAI SDK works with `base_url="https://api.deepseek.com/v1"`
