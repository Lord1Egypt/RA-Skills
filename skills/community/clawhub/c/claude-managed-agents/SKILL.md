---
name: claude-managed-agents
description: Manage Claude Managed Agents end to end through a Python helper CLI, with ant CLI equivalents documented as a secondary path. Use this whenever the user wants to create, update, list, archive, or inspect Claude Managed Agents agents, environments, sessions, or event streams; configure built-in tools, MCP servers, skills, packages, or networking; send session messages, interrupts, confirmations, or custom tool results; or work with Anthropic's managed-agents beta lifecycle from this machine.
compatibility:
  tools: Read, Edit, Bash
  dependencies: Python 3, ANTHROPIC_API_KEY, optional anthropic SDK, optional ant CLI
---

# Claude Managed Agents

Use this skill to operate Anthropic Claude Managed Agents safely and cleanly from this machine.

This skill is **SDK-first** through the bundled Python helper, with **ant CLI** documented as a secondary operator lane. Raw REST is only for debugging or when the SDK is unavailable.

## What this skill handles

- agents
  - create
  - update
  - retrieve
  - list
  - list versions
  - archive
  - delete
- environments
  - create
  - update
  - retrieve
  - list
  - archive
  - delete
- sessions
  - create
  - retrieve
  - list
  - archive
  - delete
- session events
  - send user messages
  - interrupt and redirect
  - list history
  - stream live SSE events
  - send tool confirmations
  - send custom tool results
- files
  - upload local files to the Files API
  - list, download, and delete files
  - return file IDs for mounting into sessions
- session resources
  - add resources to running sessions
  - list mounted resources
  - delete mounted resources by resource ID
- configuration domains
  - built-in toolset controls
  - MCP servers
  - skills
  - packages
  - networking
  - vault IDs
  - mounted resources
- diagnostics
  - local preflight via `doctor`
  - optional live read-only connectivity checks via `doctor --live`

## Required environment

Set:

- `ANTHROPIC_API_KEY`

Optional:

- `ANTHROPIC_API_BASE_URL`
- `ANTHROPIC_MANAGED_AGENTS_BETA`
- `ANTHROPIC_TIMEOUT_SECONDS`

The managed-agents beta header is required. The helper uses `managed-agents-2026-04-01` by default.

## Script

Use:

- `scripts/managed_agents.py`

Run it with Python 3:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py --help
```

Run a preflight before live work when the lane feels sketchy:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  doctor \
  --allowed-host api.example.com
```

## Operating model

Prefer this order:

1. Python helper CLI
2. documented `ant` equivalent when the user wants a direct CLI path
3. raw REST only when troubleshooting edge cases

The helper supports:

- `--backend auto` (default)
- `--backend sdk`
- `--backend http`

Use `sdk` when the Anthropic Python SDK is installed. Use `http` if the SDK is missing or behaving oddly.

## Safe workflow

### For new setups

1. confirm `ANTHROPIC_API_KEY` exists
2. create or inspect the target agent
3. create or inspect the target environment
4. create the session
5. send a user message event
6. stream or list events to monitor progress

### For mid-run steering

1. list or stream session events
2. if the agent is going the wrong direction, send:
   - `user.interrupt`
   - followed by a new `user.message`
3. if the session is waiting on approval, send `user.tool_confirmation`
4. if the session is waiting on a custom tool result, send `user.custom_tool_result`

## High-value guardrails

- Do not guess event IDs, tool use IDs, or custom tool use IDs.
- For approval flows, read recent events first and use the exact pending tool ID.
- For custom tools, return only the result the tool actually produced. Do not fabricate success.
- Prefer limited networking with explicit hosts for production-oriented environments. Use bare hostnames like `api.example.com`, not full URLs.
- Do not delete environments, sessions, or agents casually. Archive first unless the user clearly wants hard deletion.
- Archiving is usually the safer lifecycle move than deletion, but disposable smoke fixtures may need delete for full cleanup.

## Recommended command patterns

### Create an agent with the full built-in toolset

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Coding Assistant" \
  --model claude-sonnet-4-6 \
  --system "You are a helpful coding agent." \
  --agent-toolset
```

### Run doctor before a live session

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  doctor \
  --live \
  --allowed-host api.example.com
```

### Create an environment with limited networking and pip packages

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  environment create \
  --name "python-dev" \
  --network limited \
  --allowed-host api.example.com \
  --allow-package-managers \
  --pip pandas==2.2.0 \
  --pip numpy==2.1.0
```

### Upload a file and get a file ID

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv \
  --only-id
```

### Create a session with an uploaded file mounted in the container

```bash
FILE_ID=$(python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv \
  --only-id)

python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --environment-id env_123 \
  --title "Repo analysis" \
  --resource-json "{\"type\":\"file\",\"file_id\":\"${FILE_ID}\",\"mount_path\":\"/workspace/data.csv\"}"
```

### Add another file to a running session

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session resource add \
  --session-id sess_123 \
  --file-id file_abc123 \
  --mount-path /workspace/config.json
```

### Download a session-scoped file artifact

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file download \
  --file-id file_abc123 \
  --output ./artifact.txt
```

Use this mainly for generated artifacts. Uploaded source files often come back with `downloadable: false`.

### Send a user message to the session

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --message "Summarize the repository and propose the next refactor."
```

### Interrupt and redirect the session

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --interrupt \
  --message "Stop the broad audit and focus on the auth bug in line 42."
```

### Stream events until idle

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session stream \
  --session-id sess_123 \
  --until-idle
```

### Approve a pending tool call

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --confirm-tool-use-id tool_evt_123 \
  --confirm-result allow
```

### Delete an agent when the user explicitly wants permanent cleanup

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent delete \
  --agent-id agent_123
```

### Return a custom tool result

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --custom-tool-use-id custom_evt_123 \
  --custom-tool-text '{"temperature_f":72,"condition":"sunny"}'
```

## When to use ant CLI instead

Use `ant` when the user explicitly wants Anthropic's native CLI experience, copy-pasteable operator commands, or quick manual inspection.

Examples:

```bash
ant beta:agents create --name "Coding Assistant" --model '{id: claude-sonnet-4-6}' --tool '{type: agent_toolset_20260401}'
ant beta:environments list
ant beta:sessions retrieve --session-id "$SESSION_ID"
ant beta:sessions:events send --session-id "$SESSION_ID"
ant beta:sessions stream --session-id "$SESSION_ID"
```

## References in this skill

Read these when needed:

- `references/quickstart.md` for the end-to-end happy path
- `references/lifecycle-recipes.md` for lifecycle operations and payload patterns
- `references/files-api.md` for upload, list, download, delete, and session resource workflows
- `references/event-model.md` for streaming, interruptions, approvals, and custom tools
- `references/ant-cli-recipes.md` for direct ant commands mirroring the helper
- `references/known-gaps.md` for dependency assumptions and operational caveats

## Output contract

Default answer shape:

- short lead sentence with the answer or current state
- 2-6 bullets with the important IDs, statuses, or lifecycle facts
- exact next command when a follow-up step is likely

If the user asks for raw JSON, return the raw JSON instead.
