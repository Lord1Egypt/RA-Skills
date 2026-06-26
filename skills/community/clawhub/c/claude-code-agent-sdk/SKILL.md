---
name: claude-code-agent-sdk
description: Claude Agent SDK documentation — build production AI agents with Claude Code as a library in Python or TypeScript. Use when building, configuring, or debugging agents with the Claude Agent SDK.
---

# Claude Code Agent SDK

Build production-grade AI agents using Claude Code as a library. Supports Python and TypeScript.

## Covers

- Quickstart and setup
- Agent loop and message types
- Tool configuration and built-in tools
- Hooks for intercepting agent behavior
- Session management (resume, fork, continue)
- MCP server integration
- Sub-agents and parallel execution
- Permissions and security
- Custom tools
- Streaming and structured outputs
- Cost tracking and observability
- Claude Code features (skills, commands, memory)
- Hosting and deployment
- Python and TypeScript API references.

## Quick Navigation

Reference files are split by topic in `references/`. Load only what you need:

### Core
- **[overview.md](references/overview.md)** — SDK overview, installation, authentication, built-in tools, permission modes
- **[quickstart.md](references/quickstart.md)** — Quick start: building a bug fix agent
- **[agent-loop.md](references/agent-loop.md)** — Agent loop: message types, tool execution, context window, compression

### Agent Control
- **[hooks.md](references/hooks.md)** — Hooks: PreToolUse/PostToolUse/Stop, matchers, callback functions
- **[permissions.md](references/permissions.md)** — Permissions: allowedTools/disallowedTools, permission modes
- **[user-input.md](references/user-input.md)** — User input: approval prompts, AskUserQuestion

### Sessions & State
- **[sessions.md](references/sessions.md)** — Session management: continue/resume/fork, ClaudeSDKClient
- **[file-checkpointing.md](references/file-checkpointing.md)** — File checkpointing: track and restore file changes

### Tools & Integration
- **[custom-tools.md](references/custom-tools.md)** — Custom tools: in-process MCP server
- **[mcp.md](references/mcp.md)** — MCP: connect external tools + tool search extending to thousands of tools

### Sub-agents & Parallelism
- **[subagents.md](references/subagents.md)** — Sub-agents: AgentDefinition, context isolation, parallel tasks + todo tracking

### Streaming & Output
- **[streaming-output.md](references/streaming-output.md)** — Streaming responses + input schemas + structured outputs (JSON Schema/Zod/Pydantic)

### Configuration & Features
- **[claude-code-features.md](references/claude-code-features.md)** — Claude Code features: settingSources, CLAUDE.md, skills
- **[modifying-system-prompts.md](references/modifying-system-prompts.md)** — System prompts: claude_code preset vs custom
- **[skills.md](references/skills.md)** — Agent Skills
- **[slash-commands.md](references/slash-commands.md)** — Slash commands
- **[plugins.md](references/plugins.md)** — Plugin system

### Operations
- **[hosting.md](references/hosting.md)** — Hosting + secure deployment: Docker, cloud, CI/CD, isolation, credential management
- **[cost-tracking.md](references/cost-tracking.md)** — Cost tracking: token usage, budgeting
- **[observability.md](references/observability.md)** — Observability: OpenTelemetry
- **[migration-guide.md](references/migration-guide.md)** — Migration guide

### API Reference
- **[python.md](references/python.md)** — Python SDK API reference
- **[typescript.md](references/typescript.md)** — TypeScript SDK API reference (includes V2 deprecation notes)

## Key Patterns

### Basic agent
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Fix the bug in auth.py",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
):
    print(message)
```

### With hooks
```python
options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[validate_command])]}
)
```

### With MCP servers
```python
options = ClaudeAgentOptions(
    mcp_servers={"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}
)
```

### With sub-agents
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Agent"],
    agents={"reviewer": AgentDefinition(
        description="Code reviewer",
        prompt="Review code quality",
        tools=["Read", "Glob", "Grep"]
    )}
)
```

### Multi-turn with sessions
```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyze the auth module")
    async for msg in client.receive_response(): print(msg)
    await client.query("Now refactor it")  # auto-continues
    async for msg in client.receive_response(): print(msg)
```