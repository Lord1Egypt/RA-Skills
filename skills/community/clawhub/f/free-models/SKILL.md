name: free-models
alias:
  - free-models-for-openclaw
  - free-models-of-openclaw
  - free-models-for-agents
description: Discover free/cheap models from OpenRouter for AI agents (e.g. OpenClaw). Includes model discovery, filtering, and easy model selection for openclaw and other agent workflows.
metadata:
  version: 0.2.0
  homepage: https://openrouter.ai
---

# free-models-for-agent

Discover free, cheap, and high-value models from OpenRouter for your OpenClaw and other AI agents.

## Usage

### Find free models
```javascript
import { discoverFreeModels } from './scripts/free-models.js';

const models = await discoverFreeModels();
// Returns models with $0.00 or very low pricing
```

### Filter by criteria
```javascript
import { filterModels } from './scripts/free-models.js';

// High context + low price (best for tool calling)
const models = await filterModels({
  minContext: 200000,      // 200k+ tokens
  maxPromptPrice: 0.00001  // Under $0.00001/1M tokens
});

// Specific provider only
const openaiModels = await filterModels({
  author: 'openai',
  minContext: 100000
});

// Name contains filter
const flashModels = await filterModels({
  author: 'google',
  nameContains: 'flash'
});

// All filters combined
const cheapGoogle = await filterModels({
  author: 'google',
  minContext: 500000,
  maxPromptPrice: 0.000001
});
```

### Get best free model for agent
```javascript
import { getBestFreeModel } from './scripts/free-models.js';

// Best overall (highest context)
const bestModel = await getBestFreeModel();

// Best for reasoning tasks
const reasoningModel = await getBestFreeModel({
  needReasoning: true,
});

// Best for tool calling (high context is key)
const toolModel = await getBestFreeModel({
  preferReasoning: true,
  maxPrice: 0.00001
});

// Best for vision tasks
const visionModel = await getBestFreeModel({
  needVision: true,
});
```

## CLI Usage

User should register and get a access key from [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)
Openclaw should export the key (or string with a prefix "sk-or-") as the value of Environment Variable `OPENROUTER_API_KEY` before calling the cli.

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
node scripts/free-models.js
```

## Common Free Models

| Model | Context | Price | Best For |
|-------|---------|-------|----------|
| x-ai/grok-4.1-fast | 2M | $0.0000002/1M | Tool calling, agents |
| openai/gpt-5.4 | 1M | $0.0000025/1M | General purpose |
| google/gemini-3.1-flash-lite | 1M | $0.00000025/1M | Fast/cheap tasks |
| google/gemini-2.5-flash | 1M | $0.0000003/1M | Tool calling |
| qwen/qwen3.5-flash-02-23 | 1M | $0.0000001/1M | Budget option |

## API Reference

### fetchAllModels()
Returns all available models from OpenRouter.

### discoverFreeModels()
Filters and returns only models with $0 or very low pricing (< $0.0001/1M).

### filterModels(options)
Filters models by:
- `maxPromptPrice`: Maximum prompt price per 1M tokens
- `minContext`: Minimum context window (tokens)
- `author` or `provider`: Model provider (e.g., 'anthropic', 'openai', 'google', 'deepseek', 'minimax', 'kimi', 'z.ai')
- `maxCompletionPrice`: Maximum completion price per 1M tokens
- `nameContains`: Filter by name substring

### getBestFreeModel(options)
Returns the best free model based on:
- `needReasoning`: Requires strong reasoning capability
- `preferReasoning`: Prefers models with reasoning
- `needVision`: Requires vision capabilities
- `maxPrice`: Maximum price threshold

### getModelsByAuthor(author)
Returns all models from a specific provider.

### getCheapestModels(limit)
Returns the cheapest models (default: 10).

## Resources

- OpenRouter Models: https://openrouter.ai/models
- Models API: https://openrouter.ai/api/v1/models
