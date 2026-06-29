---
name: api-cost-compare
description: Compare AI API pricing across 18 models from 6 providers — find the cheapest model for your use case (coding, chat, writing, reasoning) and track your API spending. One command saves you thousands per year.
version: 1.2.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [API, Pricing, Cost-Optimization, LLM, OpenAI, Anthropic, DeepSeek, CLI]
    homepage: https://github.com/minirr890112-byte/api-cost-compare
---

# api-cost-compare

## Problem → Solution

**The problem**: You're building an AI app and picking a model. Claude Opus 4.7 costs $15/M tokens input, GPT-4o costs $2.50, DeepSeek V4 Flash costs $0.14. The pricing landscape shifts monthly. You're probably overpaying by 90%+ because you picked the default model. $4,000/year wasted on API costs you didn't need to spend.

**The solution**: One command compares 18 models across 6 providers for your specific scenario (coding, chat, writing, reasoning). Realistic token estimates per scenario. Spending tracker to know exactly what you're burning.

## Quick Start

```bash
pip install git+https://github.com/minirr890112-byte/api-cost-compare.git

api-cost list              # All 18 models with pricing
api-cost recommend coding  # Cheapest for your use case
api-cost compare 0 1 chat  # Head-to-head comparison
api-cost track 3.50 openai gpt-4o  # Log spending
api-cost report            # Spending summary
```

## Real Output

```
$ api-cost recommend coding

⭐ #1   Mistral Mistral Small 3        $1.65/month
⭐ #2   DeepSeek DeepSeek V4 Flash     $1.89/month
⭐ #3   OpenAI GPT-4o-mini             $2.92/month

💸 Choosing #1 over Claude Opus 4.7 saves $335.85/month ($4,030/year)
```

## Providers Covered

OpenAI · Anthropic · Google · DeepSeek · xAI · Mistral

## Scenarios

| Scenario | Input tokens | Output tokens | Requests/day |
|----------|-------------|---------------|--------------|
| coding   | 5,000       | 2,000         | 50           |
| chat     | 500         | 500           | 100          |
| writing  | 1,000       | 3,000         | 10           |
| reasoning| 2,000       | 4,000         | 20           |

---
⭐ **Star this repo to stop burning money on AI APIs**: [github.com/minirr890112-byte/api-cost-compare](https://github.com/minirr890112-byte/api-cost-compare)
