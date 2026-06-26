---
name: feishu-agent-bind
description: Bind a Feishu group chat to a specific OpenClaw agent. Use when user wants to route a Feishu group to a dedicated agent (e.g., devops, hr, pm). Covers agent creation, workspace setup, binding configuration, session cleanup, and gateway restart.
---

# Feishu Group → Agent Binding

Route a Feishu group to a specific agent with isolated workspace.

## Prerequisites

- Agent must exist in `agents.list` (create via `openclaw agents add <id>`)
- Agent must have its own workspace (NOT shared with main)
- Gateway running

## Steps

### 1. Ensure agent has independent workspace

```bash
# Check current config
openclaw config get agents.list | jq '.[] | select(.id=="<agentId>") | .workspace'
```

If workspace is shared with main (`~/.openclaw/workspace`), create a dedicated one:

```bash
mkdir -p ~/.openclaw/workspace-<agentId>/memory
```

Write at minimum `SOUL.md` and `AGENTS.md` into the new workspace. Then update config:

```python
import json
with open(os.path.expanduser('~/.openclaw/openclaw.json')) as f:
    c = json.load(f)
for a in c['agents']['list']:
    if a['id'] == '<agentId>':
        a['workspace'] = os.path.expanduser(f'~/.openclaw/workspace-<agentId>')
        break
with open(os.path.expanduser('~/.openclaw/openclaw.json'), 'w') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
```

### 2. Add group to `channels.feishu.groups` (optional but recommended)

```python
# Add group config
fs_groups = c['channels']['feishu'].setdefault('groups', {})
fs_groups['<chat_id>'] = {'requireMention': False}
```

### 3. Add binding with `accountId` (CRITICAL)

**Must include `accountId` matching the Feishu account** (usually `"main"`), otherwise the binding is silently ignored during route matching.

```python
bindings = c.get('bindings', [])
bindings.append({
    "agentId": "<agentId>",
    "match": {
        "channel": "feishu",
        "peer": {"kind": "group", "id": "<chat_id>"},
        "accountId": "<feishu_account_id>"  # e.g. "main"
    }
})
c['bindings'] = bindings
```

Or via CLI:

```bash
# Get existing bindings first
openclaw config get bindings

# Set all bindings (existing + new)
openclaw config set --json bindings '[...existing..., {"agentId":"<agentId>","match":{"channel":"feishu","peer":{"kind":"group","id":"<chat_id>"},"accountId":"main"}}]'
```

### 4. Clean up stale sessions

If the group was previously handled by another agent, delete its old session to avoid cache issues:

```bash
# Find old sessions
openclaw sessions --all-agents --json | grep "<chat_id>"

# Delete from the old agent's session store
python3 -c "
import json, glob
for f in glob.glob(os.path.expanduser('~/.openclaw/agents/*/sessions/sessions.json')):
    with open(f) as fh: d = json.load(fh)
    keys = [k for k in d if '<chat_id>' in k]
    if keys:
        for k in keys: del d[k]
        with open(f,'w') as fh: json.dump(d, fh)
        print(f'Cleaned {f}: {keys}')
"
```

### 5. Restart gateway

```bash
openclaw gateway restart
```

### 6. Verify

```bash
# Check bindings
openclaw config get bindings

# Check sessions hit the right agent
openclaw status | grep "<chat_id>"
# Should show agent:<agentId>:feishu:group:<chat_id>
```

## Pitfalls (learned the hard way)

1. **Missing `accountId` in binding**: Binding without `accountId` defaults to matching account `"default"`, not `"main"`. The Feishu plugin passes its actual account ID (e.g. `"main"`), so the binding is never matched. Always set `accountId` explicitly.

2. **Shared workspace**: If multiple agents share the same workspace, they read the same SOUL.md/BOOTSTRAP.md and confuse identities. Always use separate workspaces.

3. **Stale sessions**: Old sessions cached under a different agent persist after binding changes. Delete them manually.

4. **Gateway restart required**: Binding changes need a full gateway restart to take effect.

5. **`openclaw agents bind` CLI pitfall**: The CLI command `openclaw agents bind --agent X --bind feishu:<chat_id>` sets `accountId=<chat_id>` instead of `peer.id=<chat_id>`. This is wrong for group routing. Use `config set --json bindings` directly instead.

6. **Binding order matters**: When multiple bindings match, first one wins. Put specific peer bindings before account-level bindings.
