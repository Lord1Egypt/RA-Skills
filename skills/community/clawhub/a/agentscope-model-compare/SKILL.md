---
name: agentscope-model-compare
description: Compare multiple LLM models for use with AgentScope 2.0. Use this whenever the user wants to evaluate models, benchmark responses, or choose the best model for their agent task.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - DASHSCOPE_API_KEY
      bins:
        - python3
    primaryEnv: OPENAI_API_KEY
    envVars:
      - name: OPENAI_API_KEY
        required: true
        description: OpenAI API key for OpenAI models.
      - name: DASHSCOPE_API_KEY
        required: false
        description: Optional DashScope API key for Alibaba Cloud models.
    emoji: "\u2694\uFE0F"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Model Compare

This skill runs the same AgentScope task against multiple LLM models and compares latency, token usage, and output style.

## What this skill does

- Configures multiple AgentScope chat models
- Runs a shared agent task against each model
- Reports latency, token counts, and output length
- Highlights which models completed vs failed

## Usage

Run the comparison script from this skill folder:

```bash
python3 scripts/compare_models.py --task "Translate this into Chinese: Hello world"
```

The script uses environment variables for API keys and prints a comparison table.

## Safety

- API keys are read from `.env`, which is gitignored.
- No keys are hardcoded.
- Costs may apply; limit concurrent calls if needed.
