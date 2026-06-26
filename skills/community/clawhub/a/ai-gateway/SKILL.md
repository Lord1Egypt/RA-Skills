---
name: ai-gateway
description: >
  Access 340+ AI models via the Agnic AI Gateway -- chat, image generation,
  model listing. Use when the user wants to chat with AI, generate images,
  ask GPT, use Claude, list models, delegate to another LLM, or get a
  second opinion. Covers "ask GPT", "use Claude", "generate an image",
  "list AI models", "call a model".
user-invocable: true
disable-model-invocation: false
context: fork
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest ai *)"
---

# AI Gateway

Access 340+ AI models (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more) through the Agnic AI Gateway. Costs are deducted from your USDC balance per token. Free models available for development.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Commands

### List models

```bash
npx agnic@latest ai models [--provider <name>] [--search <term>] [--json]
```

### Chat with a model

```bash
npx agnic@latest ai chat --model <provider/model-name> --prompt "<text>" [--system "<text>"] [--json]
```

### Generate an image

```bash
npx agnic@latest ai image --prompt "<text>" [--aspect-ratio 16:9] [--output file.png] [--json]
```

Models use `provider/model-name` format (e.g., `openai/gpt-4o`, `meta-llama/llama-3.3-70b`).
See `reference/models-and-options.md` for full model list, all options, and input validation rules.

## Examples

```bash
# List OpenAI models
npx agnic@latest ai models --provider openai --json

# Chat with GPT-4o
npx agnic@latest ai chat --model openai/gpt-4o --prompt 'Explain quantum computing in one sentence'

# Use a free model
npx agnic@latest ai chat --model meta-llama/llama-3.3-70b --prompt 'What is 2+2?' --json

# Generate an image
npx agnic@latest ai image --prompt 'A sunset over mountains' --output sunset.png

# Generate widescreen image
npx agnic@latest ai image --prompt 'Cyberpunk cityscape' --aspect-ratio 16:9 --output city.png
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Wallet must have USDC balance (free models available for testing)

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- "Insufficient balance" -- Fund wallet at [app.agnic.ai](https://app.agnic.ai)
- "Model not found" -- Check available models with `npx agnic@latest ai models`
- "No image returned" -- Try a different model or rephrase the prompt
- "Rate limit exceeded" -- Wait a moment and retry
