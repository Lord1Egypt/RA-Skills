# Quick Start

Use the Agent SDK to build AI agents that read code, find bugs, and fix them.

## Prerequisites

- Node.js 18+ or Python 3.10+
- Anthropic account and API key

## Setup

```bash
mkdir my-agent && cd my-agent
# TypeScript
npm install @anthropic-ai/claude-agent-sdk
# Python
uv init && uv add claude-agent-sdk
# or pip install claude-agent-sdk
```

Set the `ANTHROPIC_API_KEY` environment variable.

## Build a Bug-Fixing Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"): print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

**Three parts to the code:**
1. `query` — Main entry point, returns an async iterator
2. `prompt` — What you want Claude to do
3. `options` — Agent configuration (tools, permissions, system prompt, etc.)

## Key Concepts

**Tool combinations:**
- `Read, Glob, Grep` — Read-only analysis
- `Read, Edit, Glob` — Analyze and modify code
- `Read, Edit, Bash, Glob, Grep` — Fully automated

**Permission modes:**
- `acceptEdits` — Auto-approves file edits (trusted workflows)
- `dontAsk` — Denies anything not in allow list
- `default` — Requires `canUseTool` callback
- `bypassPermissions` — Runs all allowed tools

## Custom Examples

Add web search: `allowed_tools=["Read", "Edit", "Glob", "WebSearch"]`
Custom system prompt: `system_prompt="You are a senior Python developer..."`
Run commands: Add `Bash` to `allowed_tools`

## Troubleshooting

Opus 4.7 requires Agent SDK v0.2.111+ (`thinking.type.enabled` replaced with `thinking.type.adaptive`).