---
name: agentscope-agent-test-harness
description: Create and run lightweight tests for AgentScope agents without hitting external APIs. Use this whenever the user wants to validate agent wiring, tool binding, or prompt formatting before live model calls.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
    primaryEnv: OPENAI_API_KEY
    envVars:
      - name: OPENAI_API_KEY
        required: true
        description: OpenAI or compatible API key.
      - name: AGENTSCOPE_TEST_MODE
        required: false
        description: When set, skip live model calls and run offline assertions only.
    emoji: "\U0001F9EA"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Agent Test Harness

This skill helps you test AgentScope agents with mocked models and offline assertions.

## What this skill does

- Creates a test harness for an existing agent module
- Replaces the live model with a fake one that returns canned responses
- Asserts tool calls, message formatting, and agent state transitions
- Reports pass/fail in markdown

## Usage

Run the harness generator from this skill folder:

```bash
python3 scripts/generate_harness.py --agent /path/to/agent_module.py --output /path/to/test_harness.py
```

Then run:

```bash
python3 -m pytest /path/to/test_harness.py
```

## Safety

- No live API calls are made unless the agent explicitly uses a real model.
- Tests are offline by default.
