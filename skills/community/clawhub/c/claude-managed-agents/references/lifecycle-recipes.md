# Lifecycle recipes

## Agents

### Create with only a limited tool subset

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Read Only Analyst" \
  --model claude-sonnet-4-6 \
  --agent-toolset \
  --default-tool-enabled false \
  --enable-tool read \
  --enable-tool glob \
  --enable-tool grep
```

### Add a tool permission policy

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Approval Guarded Agent" \
  --model claude-sonnet-4-6 \
  --agent-toolset \
  --tool-policy bash=ask \
  --tool-policy write=ask \
  --tool-policy edit=ask
```

### Attach MCP servers

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Browser Agent" \
  --model claude-sonnet-4-6 \
  --agent-toolset \
  --mcp-server 'playwright=https://mcp.example.com/playwright'
```

### Attach skills

`--skill-ref` format is:

- `anthropic:skill_id[:version]`
- `custom:skill_id[:version]`

Example:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent update \
  --agent-id agent_123 \
  --version 1 \
  --skill-ref anthropic:xlsx \
  --skill-ref custom:skill_abc123:v2
```

### Add a custom tool

Use raw JSON for custom tools:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent create \
  --name "Weather Agent" \
  --model claude-sonnet-4-6 \
  --agent-toolset \
  --tool-json @/path/to/custom_tool.json
```

Example custom tool payload:

```json
{
  "type": "custom",
  "name": "get_weather",
  "description": "Get current weather for a location. Use this when the user asks for current conditions or local weather context. Do not use it for historical analysis. Return concise structured weather data only.",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "City or location name"}
    },
    "required": ["location"]
  }
}
```

### Update semantics to remember

- omitted scalar fields are preserved
- scalar fields replace old values when supplied
- array fields replace the whole array when supplied
- metadata merges by key
- no-op updates return the existing version without incrementing

### Archive

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent archive \
  --agent-id agent_123
```

### Delete

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  agent delete \
  --agent-id agent_123
```

Use delete for disposable fixtures or explicit permanent cleanup. Prefer archive when the agent record should remain available for inspection.

## Environments

### Limited networking with explicit hosts

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  environment create \
  --name "prod-safe" \
  --network limited \
  --allowed-host api.example.com \
  --allowed-host storage.example.com
```

### Limited networking plus package-manager and MCP access

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  environment create \
  --name "builder" \
  --network limited \
  --allowed-host api.example.com \
  --allow-package-managers \
  --allow-mcp-servers
```

### Add packages

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  environment create \
  --name "data-analysis" \
  --network unrestricted \
  --pip pandas==2.2.0 \
  --pip numpy==2.1.0 \
  --npm express@4.18.2 \
  --apt ffmpeg
```

## Sessions

### Pin to a specific agent version

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --agent-version 3 \
  --environment-id env_123
```

### Attach vaults

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --environment-id env_123 \
  --vault-id vault_1 \
  --vault-id vault_2
```

### Add resources with raw JSON

The helper accepts `--resource-json` for GitHub repositories and uploaded files.

GitHub repository example:

```json
{
  "type": "github_repository",
  "url": "https://github.com/example/repo",
  "authorization_token": "${GITHUB_TOKEN}",
  "checkout": {"type": "branch", "name": "main"},
  "mount_path": "/workspace/repo"
}
```

File mount example:

```json
{
  "type": "file",
  "file_id": "file_abc123",
  "mount_path": "/mnt/session/uploads/input.pdf"
}
```

### Deletion caution

- archived sessions preserve history and block new events
- deleted sessions permanently remove session record, events, and associated container
- archive can fail on running sessions, while delete may still succeed for disposable cleanup flows
- a running session cannot always be archived cleanly until interrupted or naturally idle
