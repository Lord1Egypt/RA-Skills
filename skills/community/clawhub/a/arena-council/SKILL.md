---
name: arena-council
description: Multi-Model Council - parallel execution of multiple LLMs with voting/consensus.
---

# ARENA-001: Multi-Model Council

Parallel execution of multiple local LLMs with voting strategies for higher quality responses.

## Why Multi-Model?

- **Diversity**: Different models = different perspectives
- **Robustness**: If one fails, others continue
- **Quality**: Consensus often beats single model
- **Cost**: All local = $0 (vs $0.60/M for cloud)

## Quick Start

```python
from scripts.council import council_decide

# Simple usage
result = council_decide(
    "Explain Python decorators",
    models=['nerdsking-3b', 'llama-3.1-8b'],
    strategy="weighted"
)
print(result)
```

## Architecture

```
User Prompt
    ↓
[Router] → Model A → Response A
         → Model B → Response B  
         → Model C → Response C
    ↓
[Voting Engine]
    ↓
Consensus Response
```

## Voting Strategies

### 1. Majority Vote
Most common response wins (exact match).

### 2. Weighted Vote (default)
Bigger models get more weight:

| Model | Weight |
|-------|--------|
| Nerdsking 3B | 1 |
| Llama 3.1 8B | 2 |
| Strand 14B | 3 |
| Mistral 24B | 4 |
| GLM 4.7 | 5 |
| Qwen3.5 35B | 6 |

## Usage Examples

### Basic
```python
from scripts.council import ModelCouncil
import asyncio

async def main():
    async with ModelCouncil() as council:
        answer = await council.decide(
            "Best practice for API design?",
            strategy="weighted"
        )
        print(answer)

asyncio.run(main())
```

### Custom Models
```python
# Use specific models only
council = ModelCouncil(
    active_models=['qwen3.5-35b', 'glm-4.7-flash'],
    timeout=30
)
```

### Raw Responses
```python
# Get all responses without voting
responses = await council.query_all("Explain async/await")
for model, response in responses.items():
    print(f"{model}: {response}")
```

## Integration with OpenClaw

```python
# In your skill:
from arena_council.scripts.council import council_decide

def handle_query(prompt):
    # Use council instead of single model
    return council_decide(
        prompt,
        strategy="weighted"
    )
```

## Performance

| Setup | Time | Cost |
|-------|------|------|
| Single (Kimi) | 2s | $0.12 |
| Council (3 local) | 5s | $0 |
| Council (5 local) | 8s | $0 |

## Requirements

```bash
pip install aiohttp
```

## Models Available

Any model running on LM Studio (`http://127.0.0.1:1234/v1`). Recommended:
- Small/fast (QA, routing): `qwen3.5-9b`, `glm-4.7-flash`, `nerdsking-3b`
- Medium (analysis): `huihui-qwen3.5-27b-abliterated`, `huihui-mistral-small-24b-abliterated`
- Heavy (complex tasks): `qwen3.5-35b-uncensored-hauhaucs`, `holo3-35b`

Use `curl http://127.0.0.1:1234/v1/models` to list what's loaded.

## God Mode Integration

When all council models refuse due to censorship — apply god-mode techniques and retry:

```python
# If council returns no usable responses (all refused)
if all_refused(responses):
    from god_mode import apply_techniques
    modified_prompt = apply_techniques(prompt, methods=["unicode", "prefill"])
    responses = await council.query_all(modified_prompt)
```

See: `god-mode` skill for full technique library.

## Model Susceptibility Testing

Before using a censored model in council, test it:
1. Send a borderline request directly
2. Note: refuses? → needs god-mode wrapper
3. Document in MODEL-CATALOG.md
