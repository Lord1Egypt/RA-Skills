# Agent SDK Overview

Use Claude Code as a library to build production-grade AI agents.

## Installation

**TypeScript:** `npm install @anthropic-ai/claude-agent-sdk`
**Python:** `pip install claude-agent-sdk` or `uv add claude-agent-sdk`

The TypeScript SDK bundles the local Claude Code binary as an optional dependency, no separate Claude Code installation required.

## Authentication

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Also supports Amazon Bedrock, Claude Platform on AWS, Google Vertex AI, Microsoft Azure.

## Quick Examples

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
    prompt: "Find and fix the bug in auth.ts",
    options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
    console.log(message);
}
```

## Built-in Tools

| Tool | Function |
|------|----------|
| **Read** | Read files in the working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Bash** | Run terminal commands, scripts, git operations |
| **Monitor** | Watch background scripts and react to output lines as events |
| **Glob** | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| **Grep** | Search file contents with regular expressions |
| **WebSearch** | Search the web for current information |
| **WebFetch** | Fetch and parse web page content |
| **AskUserQuestion** | Ask clarification questions with multi-choice options |

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `acceptEdits` | Auto-approve file edits and common filesystem commands | Trusted development workflows |
| `dontAsk` | Deny anything not in `allowedTools` | Locked-down headless agents |
| `default` | Require `canUseTool` callback to handle approval | Custom approval workflows |
| `bypassPermissions` | Run every tool without prompting | Sandboxed CI, fully trusted environments |

## Core Features

- **Sub-agents:** Spawn specialized agents for focused sub-tasks, configure with `AgentDefinition`
- **MCP:** Connect to external systems (databases, browsers, APIs) via Model Context Protocol. Configure `mcpServers`
- **Hooks:** Run custom code at key points in the agent lifecycle (PreToolUse, PostToolUse, Stop, etc.)
- **Sessions:** Preserve context across multiple exchanges, support resume and fork
- **Skills / Commands / Memory:** Load project-level configuration from `.claude/`

## Comparison with Other Claude Tools

| | Agent SDK | Client SDK | Claude Code CLI |
|------|-----------|------------|-----------------|
| **Tool execution** | Claude executes directly | You implement tool loop | Interactive |
| **Best for** | CI/CD, custom apps, production automation | Direct API access | Interactive development, one-off tasks |

The Agent SDK runs the agent loop inside your own process, directly operating on files on your infrastructure. Suitable for both local prototyping and production deployment.