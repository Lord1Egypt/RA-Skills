---
name: claw-turbo
version: 1.0.0
description: >
  Zero-latency regex-based skill routing middleware for OpenClaw.
  Intercepts known user commands (deploy, restart, print, check logs, etc.)
  using compiled regex patterns and executes skill scripts directly —
  bypassing LLM inference entirely. 400,000x faster than LLM routing
  for matched commands, with 100% accuracy.
metadata:
  openclaw:
    emoji: "⚡"
    homepage: "https://github.com/jacobye2017-afk/claw-turbo"
    primaryEnv: python
    requires:
      bins:
        - python3
        - bash
    os:
      - macos
      - linux
    tags:
      - routing
      - middleware
      - regex
      - performance
      - automation
      - devops
      - ollama
      - local-llm
---

## What is claw-turbo?

claw-turbo is a zero-latency, zero-ML skill routing middleware that sits between OpenClaw and your local LLM (Ollama). It intercepts user messages using regex pattern matching and executes skill scripts directly — no LLM inference needed.

**Simple commands get instant, perfect execution. Complex queries still go to your LLM.**

```
User message → claw-turbo (regex match, <0.01ms)
                  ├── MATCH → execute script directly (0ms, 100% accurate)
                  └── NO MATCH → forward to LLM (normal processing)
```

## Why use claw-turbo?

| Approach | Latency | Accuracy | Dependencies |
|----------|---------|----------|--------------|
| **claw-turbo** | **5 us** | **100%** | PyYAML only |
| LLM routing (Gemma/Llama) | 2-10s | ~80% | Ollama + VRAM |
| Semantic routing | 50-200ms | ~95% | embedding model |

Local LLMs are unreliable for simple, repetitive commands:
- They don't always follow tool-calling instructions
- They hallucinate flags and wrong parameters
- Context window limits cause instruction loss

## Installation

```bash
git clone https://github.com/jacobye2017-afk/claw-turbo.git
cd claw-turbo
pip install -e .
```

## Quick Start

### 1. Define routes in `routes.yaml`

```yaml
routes:
  - name: deploy-staging
    description: "Deploy a service to staging"
    patterns:
      - 'deploy\s+(?P<service>\w+)\s+(?:to\s+)?staging'
    command: 'bash /opt/scripts/deploy.sh {{service}} staging'
    response_template: "Deployed {{service}} to staging"

  - name: restart-service
    patterns:
      - 'restart\s+(?P<service>[\w-]+)'
    command: 'systemctl restart {{service}}'
    response_template: "Restarted {{service}}"
```

### 2. Test matching

```bash
claw-turbo test "deploy auth-service to staging"
# MATCHED: deploy-staging
#   Captures: {'service': 'auth-service'}
#   Time: 4.8us
```

### 3. Start the proxy

```bash
claw-turbo serve --port 11435
```

Then change OpenClaw's Ollama `baseUrl` to `http://127.0.0.1:11435`.

## Use Cases

- **DevOps**: "restart nginx", "deploy to staging", "show logs for api-server"
- **Document processing**: "print report ABC123", "generate invoice 456"
- **IoT / smart office**: "turn on lights", "set AC to 22 degrees"
- **Data pipelines**: "run ETL for 2024-01", "refresh dashboard"
- **Customer service**: "check order ORD-789", "refund order ORD-789"

## Features

- Sub-microsecond regex matching (compiled patterns)
- Named capture groups → template variables
- Hot-reload routes.yaml (no restart needed)
- Transparent HTTP proxy (Ollama API compatible)
- Multi-language patterns (Chinese, English, any language)
- Zero ML dependencies (PyYAML + stdlib only)
- Works fully offline

## CLI

```
claw-turbo serve [--port 11435]     Start HTTP proxy
claw-turbo test "message"           Test pattern matching
claw-turbo routes                   List all routes
claw-turbo add-skill <path>         Generate route from SKILL.md
```

## Links

- GitHub: https://github.com/jacobye2017-afk/claw-turbo
- Author: Jacob Ye (@jacobye2017-afk)
- License: MIT
