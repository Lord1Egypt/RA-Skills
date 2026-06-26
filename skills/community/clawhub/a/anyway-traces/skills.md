> ## Documentation Index
> Fetch the complete documentation index at: https://docs.anyway.sh/llms.txt
> Use this file to discover all available pages before exploring further.

# AI Agent Skill

> Copy the Anyway skill to teach your AI coding agent how to instrument your applications

<Card title="Download SKILL.md" icon="download" href="https://docs.anyway.sh/skills.md">
  Download the skill file and add it to your AI coding agent's context.
</Card>

## What is this?

A skill file is a markdown file that gives AI coding agents (Claude Code, Cursor, Windsurf, etc.) domain-specific knowledge. The Anyway skill teaches your agent how to add observability and tracing to your AI applications using the Anyway SDK.

With this skill installed, you can give your agent instructions like:

* "Add Anyway tracing to my app"
* "Instrument this function with workflow and task spans"
* "Set up the Anyway SDK with environment variables"

## Skill

Copy the content below or use the download link above to add the skill to your AI coding agent's context.

```markdown  theme={null}
---
name: anyway
description: Instrument AI/LLM applications with Anyway observability SDK. Use when adding tracing, monitoring, or observability to code that calls OpenAI, Anthropic, or other LLM providers.
user-invocable: false
---

Anyway is a financial OS for AI agents that lets you monetize agent outcomes and capture real value. Anyway SDK provides AI observability, cost tracking, and better monetization for LLM applications.

## SDKs

- **Python** (`anyway-sdk`): Python 3.10+
- **JavaScript** (`@anyway-sh/node-server-sdk`): Node.js 18+

## Documentation

Fetch the relevant page(s) below for up-to-date installation, configuration, and usage instructions:

- Quickstart: https://docs.anyway.sh/quickstart
- Python SDK installation: https://docs.anyway.sh/sdk/python/installation
- Python SDK configuration: https://docs.anyway.sh/sdk/python/configuration
- Python SDK tracing: https://docs.anyway.sh/sdk/python/tracing
- JavaScript SDK installation: https://docs.anyway.sh/sdk/js/installation
- JavaScript SDK configuration: https://docs.anyway.sh/sdk/js/configuration
- JavaScript SDK tracing: https://docs.anyway.sh/sdk/js/tracing

## Rules

- Never hardcode API keys — use environment variables or a secrets manager
- Always call `Traceloop.init()` (Python) or `initialize()` (JS) before any LLM calls
- For ESM/Next.js projects, always pass provider modules via `instrumentModules`
- The collector endpoint is `https://collector.anyway.sh/`
- The SDK auto-instruments calls to OpenAI, Anthropic, Cohere, Bedrock, Vertex AI, and other providers — manual span creation is only needed for workflow/task structure
```


Built with [Mintlify](https://mintlify.com).