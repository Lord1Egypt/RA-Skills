---
name: agent-lens
description: "Track AI agent API calls, analyze token usage, and optimize costs. Use when user wants to monitor LLM spending, debug API calls, track token consumption, or generate cost reports for OpenAI/Anthropic/Google/DeepSeek APIs."
version: 2.1.0
author: lrg913427-dot
license: MIT
metadata:
  hermes:
    tags: [llm, cost, tracking, observability, tokens, api, monitoring, agent]
    related_skills: [db-explorer]
---

# Agent Lens

Track every AI API call, analyze token usage, and optimize costs.

## When to Use

Activate this skill when the user:
- Says "how much am I spending", "token usage", "API costs"
- Wants to know which model is most expensive
- Needs to optimize prompt costs
- Wants to track API call latency or error rates
- Mentions "budget", "cost optimization", or "token counting"
- Asks "why is my API bill so high"

## Quick Start

```bash
# Install
pip install git+https://github.com/lrg913427-dot/agent-lens.git

# Generate demo data and see it in action
agent-lens demo

# View stats
agent-lens stats
agent-lens cost
agent-lens recent
```

## Three Ways to Track

### 1. Decorator (easiest)

```python
from agent_lens import AgentLens

lens = AgentLens(agent_name="my-agent")

@lens.track(model="gpt-4o")
def call_api(prompt):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

# Token usage is auto-extracted from OpenAI-style responses
result = call_api("Hello")
```

### 2. Context Manager (flexible)

```python
from agent_lens import AgentLens

lens = AgentLens(agent_name="my-agent")

with lens.trace(model="claude-3.5-sonnet") as t:
    result = client.chat.completions.create(...)
    t.input_tokens = result.usage.prompt_tokens
    t.output_tokens = result.usage.completion_tokens
```

### 3. Direct Record (manual)

```python
from agent_lens import AgentLens

lens = AgentLens(agent_name="my-agent")
lens.record(
    model="gpt-4o",
    input_tokens=1500,
    output_tokens=800,
    latency_ms=2300,
)
```

### Global Shortcuts

```python
from agent_lens import record, trace, track

record(model="gpt-4o", input_tokens=100, output_tokens=50)

with trace(model="gpt-4o") as t:
    ...

@track(model="gpt-4o")
def my_func():
    ...
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `agent-lens stats` | Overview: total calls, tokens, cost |
| `agent-lens report --by model` | Breakdown by model/provider/agent |
| `agent-lens cost` | Cost ranking with percentage bars |
| `agent-lens recent -n 10` | Latest API calls |
| `agent-lens top` | Most expensive calls |
| `agent-lens export --json` | Export to JSON |
| `agent-lens export -o data.csv` | Export to CSV |
| `agent-lens clean --before <ts>` | Clean old data |
| `agent-lens demo` | Generate sample data |

## Cost Optimization Workflow

When user asks "how can I save money":

1. **Run cost report**: `agent-lens cost`
2. **Identify expensive models**: Which models cost the most?
3. **Check token efficiency**: Are prompts too long?
4. **Suggest cheaper alternatives**:
   - gpt-4o → gpt-4o-mini (10x cheaper)
   - claude-3.5-sonnet → claude-3.5-haiku (4x cheaper)
   - gpt-4 → gpt-4o (2x cheaper)
5. **Check caching**: Are there repeated prompts?
6. **Check error rate**: `agent-lens report --by status`

## Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Count tokens for a given model."""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

# Check before sending
prompt = "Your long prompt here..."
tokens = count_tokens(prompt)
print(f"Prompt: {tokens} tokens")
print(f"Estimated cost: ${tokens * 2.50 / 1_000_000:.4f}")
```

## Supported Models

Pricing data for: OpenAI (GPT-4o, o1, o3), Anthropic (Claude 3.5/4), Google (Gemini 2.x), DeepSeek, Mistral, Qwen, GLM, MiMo.

Unknown models are tracked but cost shows "—".

## Integration with Hermes

```python
# Track Hermes agent API calls
from agent_lens import AgentLens

lens = AgentLens(agent_name="hermes-main")

# In your agent loop:
with lens.trace(model=config.model) as t:
    response = agent.run_conversation(message)
    t.input_tokens = response.get("input_tokens", 0)
    t.output_tokens = response.get("output_tokens", 0)
```

## Data Storage

SQLite at `~/.agent-lens/traces.db`. Fully local, no cloud service needed.

## Pitfalls

- Token extraction auto-works only for OpenAI-compatible response format
- For non-OpenAI providers, manually set `t.input_tokens` and `t.output_tokens`
- Cost estimates use list prices; actual costs may differ with discounts
- Database grows over time; use `agent-lens clean` periodically

## Verification

```bash
agent-lens demo        # Generate 20 sample records
agent-lens stats       # Should show 20 calls
agent-lens cost        # Should show cost breakdown by model
```
