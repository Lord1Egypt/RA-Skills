---
name: agentscope-config-validator
description: Validate AgentScope 2.0 project configuration files for correctness, completeness, and common mistakes. Use this whenever the user wants to check an agentscope project setup, debug config issues, or review pyproject.toml and model settings before running agents.
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
      - name: AGENTSCOPE_MODEL
        required: false
        description: Optional default model name.
    emoji: "\u2705"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Config Validator

This skill inspects an AgentScope 2.0 project directory and reports configuration issues.

## What this skill does

- Reads `pyproject.toml` and checks `agentscope` dependency
- Checks for `.env` and warns if `OPENAI_API_KEY` is missing
- Looks for example agents and verifies they import cleanly
- Reports missing optional dependencies

## Usage

Run the validator script from this skill folder:

```bash
python3 scripts/validate_project.py --project /path/to/agentscope/project
```

Output is a short markdown report with pass/fail findings.
