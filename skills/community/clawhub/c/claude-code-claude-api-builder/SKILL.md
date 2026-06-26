---
name: "claude_api_builder"
description: "Use when code imports Anthropic SDKs or the user asks to build with the Claude API, Agent SDK, tool use, streaming, files, or batches."
---

# Claude API Builder

Use this skill when the task is specifically about Anthropic or Claude API integration.

## Trigger Signals
- Imports like `anthropic`, `@anthropic-ai/sdk`, or Agent SDK packages
- Requests about streaming, tool use, prompt caching, file uploads, or Claude batch jobs
- Questions about choosing Anthropic API patterns for an app

## Workflow
1. Detect the project language and SDK surface.
2. Choose the smallest fitting pattern: simple messages, streaming, tools, batches, or files.
3. Prefer official docs and SDK-native examples.
4. Keep model names, error handling, and retries explicit.
5. Explain when to browse live docs for fast-moving API details.

## Guardrails
- Do not pivot to non-Anthropic SDKs unless the user asks.
- Prefer primary documentation over memory for model/API specifics.
- Separate one-shot prompts from stateful agent workflows.

## Source Provenance
Derived from `src/skills/bundled/claudeApi.ts` and the bundled Claude API references.
