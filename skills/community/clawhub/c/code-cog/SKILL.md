---
name: code-cog
description: "AI coding agent powered by CellCog Co-work. Code generation, debugging, refactoring, codebase exploration, terminal operations — executed directly on your machine. Lightweight with multimedia tools loaded on demand."
author: CellCog
homepage: https://cellcog.ai
metadata:
  openclaw:
    emoji: "💻"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
dependencies: [cellcog]
---
# Code Cog — The First Coding Agent Built for Agents

When your AI needs to code, it delegates to CodeCog. Direct codebase access, terminal operations, and file editing — executed on the user's machine via CellCog Co-work.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/path/to/project",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/path/to/project",
)
print(result["message"])
```


---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you how to use CellCog as a coding agent.

**CellCog Desktop Required:** The user must have CellCog Desktop installed and running for Co-work (direct machine access). Download at https://cellcog.ai

---

## Quick Start

**OpenClaw agents (fire-and-forget):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw")

result = client.create_chat(
    prompt="Refactor the authentication module to use JWT tokens",
    notify_session_key="agent:main:main",  # OpenClaw only
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="auth-refactor",
)
```

**All other agents (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw")

result = client.create_chat(
    prompt="Refactor the authentication module to use JWT tokens",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="auth-refactor",
)
```

**Key parameters:**
- `chat_mode="agent core"` — Lightweight coding agent (vs `"agent"` for full multimedia)
- `enable_cowork=True` — Enables Co-work (direct machine access)
- `cowork_working_directory` — The repo/directory to work in

---

## What CodeCog Can Do

### Code Generation & Editing
- Write new files, modules, and components
- Edit existing code with surgical precision
- Refactor codebases — rename, restructure, extract
- Port code between languages or frameworks

### Debugging & Fixing
- Read error logs and stack traces
- Identify root causes across multiple files
- Apply fixes and verify they work
- Run tests to confirm the fix

### Terminal Operations
- Run build commands, tests, linters
- Install dependencies (npm, pip, cargo, etc.)
- Git operations (status, diff, commit)
- Docker, deployment scripts

### Codebase Exploration
- Auto-reads AGENTS.md/CLAUDE.md for project conventions
- Explores directory structure before starting work
- Understands existing patterns and follows them
- Reads related files to maintain consistency

---

## What Makes CodeCog Different

### Built for Agents, Not Humans

Every other coding tool (Cursor, Claude Code, Codex, Windsurf) is designed for human developers sitting at a screen. CodeCog is designed for AI agents that need to code programmatically — fire a request, get results back, continue orchestrating.

### Starts Lean, Scales to Multimodal

CodeCog uses CellCog's Agent Core mode — a lightweight context focused on coding. But if your task unexpectedly needs images, PDFs, videos, or other capabilities, the agent loads those tools on demand. No other coding agent does this.

Example: Your agent asks CodeCog to set up a new project. CodeCog writes the code, then realizes it needs to generate a logo for the README — it loads image tools, generates the logo, and continues. Seamless.

### Direct Machine Access

Via CellCog Co-work, CodeCog operates directly on the user's filesystem:
- Reads and writes files on the real machine
- Runs terminal commands in the user's shell
- Respects project conventions (AGENTS.md, .gitignore, etc.)
- User approves write/execute operations for safety

---

## Chat Mode

**Always use `"agent core"` for CodeCog.** This is the dedicated lightweight mode optimized for coding.

| Mode | Use Case |
|------|----------|
| `"agent core"` | **CodeCog default** — coding, co-work, terminal ops (50 credits min) |
| `"agent"` | Full multimedia agent — use when you need images/video/audio alongside code (100 credits min) |
| `"agent team"` | Deep research + coding — use for architecture decisions or complex refactors needing research (500 credits min) |

---

## Example Prompts

### New Feature Development

```python
result = client.create_chat(
    prompt="Add a REST API endpoint for user profile updates with validation and tests",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="add-profile-api",
)
```

### Bug Fix from Error Log

```python
result = client.create_chat(
    prompt="""Fix this error in production:
TypeError: Cannot read properties of undefined (reading 'map')
at UserList.render (src/components/UserList.tsx:42)

The component crashes when the API returns an empty response.""",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="fix-userlist-crash",
)
```

### Codebase Refactor

```python
result = client.create_chat(
    prompt="Refactor the authentication module from session-based to JWT tokens. Update all middleware, tests, and API routes.",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="auth-refactor",
)
```

### Test Generation

```python
result = client.create_chat(
    prompt="Generate comprehensive unit tests for src/services/billing.py. Cover edge cases for proration, currency conversion, and failed payments.",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/projects/myapp",
    task_label="billing-tests",
)
```

See https://cellcog.ai for complete SDK API reference — delivery modes, `send_message()`, timeouts, file handling, and more.

---

## Co-work Setup

### Requirements
1. **CellCog Desktop** must be installed and running on the user's machine
2. **Working directory** must be specified — this is the root of the project/repo
3. User must be logged into CellCog Desktop with the same account

### What Co-work Enables
- `HumanComputer_Terminal` — Run shell commands on the user's machine
- `HumanComputer_Terminal_File_View` — Read files on the user's machine
- `HumanComputer_Terminal_File_Write` — Write files on the user's machine
- `HumanComputer_Terminal_File_Edit` — Edit files on the user's machine

### Safety Model
- **Read operations** are auto-approved (no interruption)
- **Write/execute operations** require user approval in the CellCog web UI
- Users can configure auto-approve for reads/writes within the working directory
- Sensitive paths (credentials, SSH keys) are always blocked

---

## Tips for Better Results

1. **Specify the working directory** — Always set `cowork_working_directory` to the project root
2. **Reference specific files** — "Fix the bug in src/auth/login.ts" is better than "fix the login bug"
3. **Mention conventions** — "Follow the existing test patterns" helps maintain consistency
4. **Include error context** — Stack traces, log output, and reproduction steps help debugging
5. **Use AGENTS.md** — Place an AGENTS.md at your repo root with build commands, style guides, and project structure. CodeCog reads it automatically.

---

## Limitations

- **macOS and Linux only** — CellCog Desktop (Co-work) is not yet available on Windows
- **CellCog Desktop required** — Without Co-work, CodeCog can still write code in its Docker workspace, but cannot access the user's machine directly
- **User approval for writes** — Write operations pause for user approval (configurable auto-approve available)

