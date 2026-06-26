# Claude Managed Agents quickstart

This skill is designed for full-lifecycle Claude Managed Agents operations.

## Prerequisites

Set:

```bash
export ANTHROPIC_API_KEY="..."
```

Optional:

```bash
export ANTHROPIC_TIMEOUT_SECONDS=60
export ANTHROPIC_MANAGED_AGENTS_BETA=managed-agents-2026-04-01
```

## Happy-path lifecycle

### 0. Run doctor first when setting up a new lane

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  doctor \
  --live \
  --allowed-host api.example.com
```

### 1. Create an agent

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Coding Assistant" \
  --model claude-sonnet-4-6 \
  --system "You are a helpful coding agent." \
  --agent-toolset
```

### 2. Create an environment

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  environment create \
  --name "quickstart-env" \
  --network unrestricted
```

### 3. Optionally upload a local file

```bash
FILE_ID=$(python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv \
  --only-id)
```

### 4. Start a session

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --environment-id env_123 \
  --title "Quickstart session" \
  --resource-json "{\"type\":\"file\",\"file_id\":\"${FILE_ID}\",\"mount_path\":\"/workspace/data.csv\"}"
```

### 5. Send a task

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --message "Create a Python script that prints the first 20 Fibonacci numbers."
```

### 6. Optionally add another file after the session is already running

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session resource add \
  --session-id sess_123 \
  --file-id "$FILE_ID" \
  --mount-path /workspace/data-copy.csv
```

### 7. Stream progress

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session stream \
  --session-id sess_123 \
  --until-idle
```

## SDK vs HTTP fallback

The helper defaults to `--backend auto`.

- If the `anthropic` Python SDK is installed, it uses SDK methods for CRUD operations.
- If not, it falls back to direct HTTPS calls for CRUD.
- Streaming uses HTTP SSE directly.

If you need deterministic behavior:

```bash
python3 .../managed_agents.py agent list --backend sdk
python3 .../managed_agents.py agent list --backend http
```

## Choosing the right lifecycle action

- **doctor** before live work when credentials, backend selection, host formatting, or API connectivity might be suspect

- **list** when you do not know the right ID yet
- **get** when you know the exact resource ID
- **update** when modifying an existing resource in place
- **archive** when you want to preserve history and prevent future writes
- **delete** only when the user clearly wants permanent removal and the platform permits it
- **agent delete** when you want to zero out disposable fixtures instead of leaving archived agent records behind
