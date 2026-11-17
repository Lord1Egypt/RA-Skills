---
name: agentscope-test-fixture-generator
description: Generate test fixtures, mock data, and example configurations for AgentScope 2.0 agents and pipelines. Use this when the user needs to test AgentScope code, create unit test data, or generate example agent configurations for development and CI.
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
        required: false
        description: Optional API key for validating generated configs against a real provider.
      - name: AGENTSCOPE_MODEL
        required: false
        description: Optional default model name used in generated example configs.
    emoji: "🧪"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Test Fixture Generator

This skill generates ready-to-use test fixtures for AgentScope 2.0 projects. It helps developers quickly create mock data, example configurations, and test scaffolding for unit tests, integration tests, and documentation examples.

## What this skill does

- Generates mock agent configurations with various model providers
- Creates test fixture files for common AgentScope patterns
- Produces example pipeline configurations
- Generates mock response data for testing
- Creates pytest-compatible test scaffolding

## How to use

Run the generator script from this skill folder:

```bash
python3 scripts/generate_fixtures.py --output /path/to/test/fixtures --pattern sequential
```

Supported patterns:

- `sequential` - single agent chain fixtures
- `parallel` - multi-agent parallel execution fixtures
- `team` - team-based agent fixtures
- `dialogue` - multi-turn conversation fixtures

After generation:

```bash
cd /path/to/test/fixtures
pytest
```

## Security notes

- Generated fixtures use placeholder API keys and mock responses
- No real credentials are embedded in generated files
- All generated configs are safe for CI environments

## Troubleshooting

- If import fails, ensure agentscope is installed: `pip install agentscope`
- For model-specific fixtures, set the appropriate environment variable
- Generated tests require pytest: `pip install pytest`
