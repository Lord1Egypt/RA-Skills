# DeepSeek — V4 Flash & Pro CLI Skill

> Use DeepSeek V4 from the command line — one-shot Q&A, thinking mode, multi-turn chat. No special CLI needed.

[![clawhub](https://img.shields.io/badge/clawhub-deepseek--v4-blue)](https://clawhub.ai/skills/deepseek-v4)
[![deepseek](https://img.shields.io/badge/DeepSeek-V4-green)](https://platform.deepseek.com)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

DeepSeek V4 is one of the most capable and affordable LLMs available — but there's no official CLI. Getting started requires writing API boilerplate every time. This skill gives you a clean, one-command interface to DeepSeek V4 Flash and Pro directly from your terminal.

## What it does

**One-shot Q&A** — ask Flash or Pro a question, get a streamed answer  
**Thinking mode** — watch DeepSeek V4-Pro reason through hard problems step by step  
**Multi-turn chat** — interactive conversation with context  
**Model guide** — pricing, model IDs, when to use which  
**No special CLI** — uses `uv` + Python, works anywhere  

## Models

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| V4 Flash ⚡ | Fast | $0.014/M in | Q&A, writing, code, summaries |
| V4 Pro 🚀 | Slower | $0.174/M in | Math, hard reasoning, deep analysis |

Both support 1M token context. Cache hits are 10× cheaper.

## Installation

```bash
openclaw install deepseek
export DEEPSEEK_API_KEY=your_key_here
```

Get your API key at [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

## Usage

```bash
# Quick question (Flash — fast & cheap)
uv run ~/.openclaw/skills/deepseek/scripts/ask.py "What changed in DeepSeek V4?"

# Use Pro for hard problems
uv run ~/.openclaw/skills/deepseek/scripts/ask.py "Explain transformer attention" --model pro

# Thinking mode — see the reasoning process
uv run ~/.openclaw/skills/deepseek/scripts/ask.py "Prove sqrt(2) is irrational" --think

# Interactive chat
uv run ~/.openclaw/skills/deepseek/scripts/chat.py --model flash

# Show models & pricing
uv run ~/.openclaw/skills/deepseek/scripts/models.py
```

## Keywords

DeepSeek · DeepSeek V4 · DeepSeek V4 Flash · DeepSeek V4 Pro · deepseek-v4-flash · deepseek-v4-pro · deepseek api · deepseek cli · deepseek chat · thinking mode · deepseek reasoning · LLM cli · cheap LLM · fast LLM · openai compatible · open source LLM · chinese AI · AI model · command line AI · deepseek-reasoner · deepseek-chat · 深度求索 · DeepSeek接口 · AI assistant cli

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/deepseek-v4)
