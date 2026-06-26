---
name: dashscope-llm
description: "通过阿里云 DashScope 的 OpenAI 兼容 API 发送简单单轮对话请求，用于快速 LLM 测试、提示词实验或一次性文本生成。"
version: "1.0.0"
---

# dashscope-llm

Use this skill when you need to send a simple chat request to DashScope through its OpenAI-compatible API.

## What this skill does

This skill provides a minimal CLI wrapper at `scripts/cli.py` that:

- reads `DASHSCOPE_API_KEY` from the environment
- connects to `https://dashscope.aliyuncs.com/compatible-mode/v1`
- sends a single user message with the OpenAI Python SDK
- prints the model response to stdout

## When to use it

Use this skill for quick LLM checks, prompt experiments, or simple one-shot generations against DashScope models.

Do not use it when you need:

- multi-turn conversation state
- streaming output
- tool calling
- structured output handling
- advanced retry or error management

## Prerequisites

Make sure the environment has:

- `DASHSCOPE_API_KEY` set
- Python available
- the `openai` Python package installed

Example:

```bash
export DASHSCOPE_API_KEY="your_api_key"
python3 scripts/cli.py --model qwen3.6-plus --message "你是谁？"
```

## CLI arguments

The script supports:

- `--model`: model name, default is `qwen3.6-plus`
- `--message`: user prompt, default is `你是谁？`
