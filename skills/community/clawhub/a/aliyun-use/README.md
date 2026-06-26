# Aliyun Bailian(百炼) for OpenClaw

This is an OpenClaw skill that provides integration with Alibaba Cloud Bailian LLM via DashScope Anthropic API.

## What This Skill Does

This skill enables OpenClaw to access Alibaba Cloud's AI capabilities:

- **Chat** - General-purpose LLM chat with Qwen, GLM, Kimi, MiniMax models
- **Translate** - Language translation between 14 languages
- **Code Generation** - Use `qwen3-coder-next` or `qwen3-coder-plus` for coding tasks

## Installation

This skill is installed as part of OpenClaw. Once installed, the `aliyun-use` skill will be automatically available.

## Setup

You'll need an Aliyun Bailian API key:

1. Go to https://bailian.console.aliyun.com/
2. Sign up for an account
3. Subscribe to Coding Plan to get your API key (note: Coding Plan API key `sk-sp-xxx` is different from regular DashScope API key)
4. Set the `ALIYUN_BAILIAN_API_KEY` environment variable

## Usage in OpenClaw

Once configured, you can use Aliyun tools directly in OpenClaw:

```
/aliyun-use chat --model qwen3.5-plus "your message"
/aliyun-use translate "your text" --target-lang zh
```

Or use them as tools in your agent workflow.

## Requirements

- Python 3.10+
- `ALIYUN_BAILIAN_API_KEY` environment variable

## Available Models

**Flagship:** `qwen3.5-plus`, `qwen3-max-2026-01-23`

**Coder:** `qwen3-coder-next`, `qwen3-coder-plus`

**Other:** `glm-5`, `glm-4.7`, `kimi-k2.5`, `MiniMax-M2.5`

## Documentation

- [SKILL.md](SKILL.md) - Complete skill documentation
- [references/API.md](references/API.md) - Detailed API reference
- [assets/models.json](assets/models.json) - Available models

## License

MIT
