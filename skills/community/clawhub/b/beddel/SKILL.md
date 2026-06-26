---
name: beddel
description: >-
  Execute declarative YAML AI workflows with branching, retry,
  multi-provider LLM support, guardrails, and OpenTelemetry tracing
  via the Beddel Python SDK. Use when asked to run, create, validate,
  or debug YAML AI workflows, multi-step pipelines, or LLM chains.
  Triggers on: "run workflow", "execute pipeline", "validate YAML workflow",
  "create a workflow", "beddel", "multi-step LLM".
metadata:
  clawdbot:
    emoji: "🔄"
    tags: [workflow, yaml, llm, python, automation, pipeline, observability, guardrail]
    requires:
      bins: [python3, pip, beddel]
      env: [GEMINI_API_KEY]
    primaryEnv: GEMINI_API_KEY
---

# Beddel

Declarative YAML workflow engine for AI pipelines — run multi-step LLM chains with branching, guardrails, retry, and observability out of the box.

## Prerequisites

- Python 3.11+ (`python3.11 --version`)
- pip for Python 3.11 (`python3.11 -m pip --version`)
- An LLM API key — any [LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) works. Gemini recommended:

```bash
export GEMINI_API_KEY="your-key"
```

## Installation

```bash
python3.11 -m pip install "beddel[all]"
beddel version
```

> **Note:** System Python may be 3.10. Always use `python3.11` explicitly.

## Quick Start

1. Write a workflow file `hello.yaml`:

```yaml
id: hello
name: Hello World
input_schema:
  topic: { type: str, required: true }
steps:
  - id: greet
    primitive: llm
    config:
      model: gemini/gemini-2.0-flash
      prompt: "Write a one-sentence greeting about $input.topic"
      max_tokens: 50
```

2. Run it:

```bash
beddel run hello.yaml -i topic="AI agents" --json-output
```

## Tool Integration (OpenClaw Plugin)

The `beddel` tool is available via the OpenClaw plugin `@botanarede/beddel`:

```bash
openclaw plugins install @botanarede/beddel
```

Once installed, the agent can invoke `beddel` with actions: `run`, `validate`, `list-primitives`.

The bundled example `examples/setup-beddel.yaml` automates this installation — see [Bundled Example](#bundled-example-setup-beddel) below.

## CLI Reference

| Command | Description |
|---------|-------------|
| `beddel run <file> [-i key=val] [--json-output]` | Execute a workflow |
| `beddel validate <file>` | Validate YAML syntax and schema |
| `beddel list-primitives` | Show available primitives |
| `beddel serve -w <file> [--port 8000]` | Serve workflow as HTTP endpoint |
| `beddel version` | Print installed version |

## Core Concepts

A **workflow** is a YAML file with an `id`, `name`, optional `input_schema`, and a list of `steps`. Each step declares a **primitive** (the unit of work) and a **config** (primitive-specific parameters).

Steps execute sequentially. Each step's output is available to subsequent steps via `$stepResult.<step_id>.<path>`.

See `references/` for full schema documentation.

## Primitives

| Primitive | Purpose |
|-----------|---------|
| `llm` | Single-turn LLM call with streaming support |
| `chat` | Multi-turn conversation with message history |
| `output-generator` | Template-based output rendering (JSON, Markdown, text) |
| `guardrail` | Data validation with strategies: raise, return_errors, correct, delegate |
| `call-agent` | Nested workflow invocation with depth tracking |
| `tool` | External function call — `shell_exec` is built-in |
| `agent-exec` | Unified adapter for external agent delegation |

## Execution Strategies

Each step can declare an `execution_strategy` to control error handling:

| Strategy | Behavior |
|----------|----------|
| `fail` | Stop workflow on error (default) |
| `skip` | Log error, continue to next step |
| `retry` | Retry with exponential backoff and jitter |
| `fallback` | Execute an alternative step on failure |
| `delegate` | Delegate error recovery to agent judgment |

## Variable Resolution

| Namespace | Example | Source |
|-----------|---------|--------|
| `$input` | `$input.topic` | Runtime inputs (`-i key=val`) |
| `$stepResult` | `$stepResult.greet.content` | Previous step outputs |
| `$env` | `$env.GEMINI_API_KEY` | Environment variables |

Key paths for step results:
- **tool** steps: `$stepResult.<id>.result.stdout`, `.result.exit_code`
- **llm** steps: `$stepResult.<id>.content`
- **guardrail** steps: `$stepResult.<id>.data.<field>`, `.valid`

## Bundled Example: setup-beddel

This workflow checks whether the `@botanarede/beddel` OpenClaw plugin is installed and installs it if needed. It demonstrates 3 of the 7 primitives: `tool`, `guardrail`, and conditional execution via `if`.

```yaml
id: setup-beddel
name: Beddel Plugin Setup
description: Install or update the @botanarede/beddel OpenClaw plugin and verify it loads.

steps:
  - id: check_plugin
    primitive: tool
    config:
      tool: shell_exec
      arguments:
        cmd: "python3.11 -c \"import subprocess,json,re;r=subprocess.run(['openclaw','plugins','list'],capture_output=True,text=True);has=bool(re.search(r'beddel',r.stdout));loaded=bool(re.search(r'beddel.*loaded',r.stdout));print(json.dumps({'action':'OK'if loaded else'REINSTALL'if has else'INSTALL'}))\""

  - id: validate_check
    primitive: guardrail
    config:
      data: "$stepResult.check_plugin.result.stdout"
      schema:
        fields:
          action: { type: str, required: true }
      strategy: correct

  - id: install_plugin
    primitive: tool
    config:
      tool: shell_exec
      arguments:
        cmd: "openclaw plugins install @botanarede/beddel"
      timeout: 120
    if: "$stepResult.validate_check.data.action != 'OK'"

  - id: verify
    primitive: tool
    config:
      tool: shell_exec
      arguments:
        cmd: "openclaw plugins info beddel"
```

### What each step demonstrates

| Step | Primitive | Feature |
|------|-----------|---------|
| `check_plugin` | `tool` | Deterministic check via `shell_exec` — outputs JSON without LLM |
| `validate_check` | `guardrail` | `correct` strategy — parses JSON string, strips markdown fences, validates schema |
| `install_plugin` | `tool` | Conditional execution (`if`) — skips when plugin already loaded. `timeout: 120` for network ops |
| `verify` | `tool` | Post-install verification |

Run it:

```bash
beddel run examples/setup-beddel.yaml --json-output
```

## Security & Privacy

- **Secrets**: Use `$env.*` variables — never hardcode API keys in workflow YAML
- **shell_exec**: Runs with `shell=False` (no shell injection). Commands are split via `shlex.split()`. Shell operators (`|`, `&&`, `>`) are sanitized in beddel 0.1.1+
- **Subprocess sandbox**: Default timeout 60s, max stdout 1MB per stream, configurable per step

### External Endpoints

| Endpoint | When | Purpose |
|----------|------|---------|
| LLM provider API (e.g. `generativelanguage.googleapis.com`) | `llm`, `chat`, `guardrail` (delegate) steps | Model inference |
| PyPI (`pypi.org`) | Installation only | Package download |
| npm registry (`registry.npmjs.org`) | Plugin install step | Plugin download |

### Trust Statement

Beddel executes user-defined YAML workflows. It does not phone home, collect telemetry by default, or transmit data beyond the configured LLM provider endpoints. OpenTelemetry export is opt-in.

## Observability

Beddel emits OpenTelemetry spans for every workflow and step execution:

- `beddel.workflow.execute` — root span per workflow run
- `beddel.step.<primitive>` — child span per step
- `gen_ai.usage.*` attributes on LLM steps (prompt/completion tokens)

Enable with any OTel-compatible collector via standard `OTEL_*` environment variables.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `BEDDEL-PRIM-300` | Tool not found | Ensure tool name is `shell_exec` (built-in). Custom tools need `-t name=module:func` |
| `BEDDEL-RESOLVE-001` | Unresolvable variable | Check step id spelling and result path. Tool results use `.result.stdout`, LLM uses `.content` |
| `BEDDEL-GUARD-201` | Guardrail validation failed | Check schema field types. Use `strategy: correct` for JSON string inputs |
| `python3.11: not found` | Wrong Python version | Install Python 3.11+. System Python may be 3.10 |
| Step shows `SKIPPED` | `if` condition was false or `execution_strategy: skip` | Expected behavior — downstream steps should handle SKIPPED values |

## Advanced: Python SDK

```python
from beddel import WorkflowExecutor, VariableResolver

resolver = VariableResolver()
resolver.register_namespace("secrets", lambda path, ctx: get_secret(path))

executor = WorkflowExecutor(resolver=resolver)
result = await executor.execute(workflow, {"topic": "AI"})
```

For FastAPI integration: `beddel serve -w workflow.yaml --port 8000`

## References

Additional documentation in `references/` (loaded on demand):
- `workflow-format.md` — Complete YAML schema
- `primitives.md` — All 7 primitives with full config options
- `execution-strategies.md` — 5 strategies with examples
- `variable-resolution.md` — Namespaces, custom resolvers, error handling
