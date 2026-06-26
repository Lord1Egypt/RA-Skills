---
name: clawmem-setup
description: Bootstrap, repair, and verify the ClawMem OpenClaw plugin. Use when ClawMem is not yet installed, not selected as the active memory plugin, missing per-agent provisioning, or needs setup troubleshooting. After activation, rely on the bundled `clawmem` plugin skill for everyday recall, saving, schema, collaboration, mental-model guidance, communication, and manual memory operations.
---

# ClawMem Setup

This file is only for installing, activating, verifying, or repairing ClawMem.

Once the plugin is active, stop using this bootstrap document as the runtime memory playbook. The plugin now ships a bundled `clawmem` skill that handles:
- the turn-by-turn recall and save loop
- shared and team memory routing
- the runtime mental model, communication, and console-link guidance
- schema and label discipline
- raw `gh` and `curl` fallback flows

## Install and activate the plugin

```sh
openclaw plugins install @clawmem-ai/clawmem
openclaw plugins enable clawmem
openclaw config set plugins.slots.memory clawmem
openclaw config validate
openclaw gateway restart
```

If a gateway restart may interrupt the current reply stream, send the user a short notice before restarting.

## Verify activation

First verify that ClawMem is selected as the active memory plugin:

```sh
openclaw status
python3 - <<'PY'
import json, os, subprocess
cfg_path = subprocess.check_output(["openclaw", "config", "file"], text=True).strip()
with open(os.path.expanduser(cfg_path)) as f:
    root = json.load(f)
slots = (root.get("plugins") or {}).get("slots") or {}
print(f"plugins.slots.memory = {slots.get('memory', 'MISSING')}")
PY
```

Expected:
- OpenClaw status shows ClawMem as the active memory plugin
- `plugins.slots.memory = clawmem`

If the active memory slot is not `clawmem`, fix that first and restart the gateway again.

## Verify per-agent provisioning

ClawMem provisions credentials per agent identity and writes them back to:

```text
openclaw.json -> plugins.entries.clawmem.config.agents.<agentId>
```

Check the current agent route:

```sh
AGENT_ID="${OPENCLAW_AGENT_ID:-main}"
python3 - "$AGENT_ID" <<'PY'
import json, os, subprocess, sys
agent_id = sys.argv[1]
cfg_path = subprocess.check_output(["openclaw", "config", "file"], text=True).strip()
with open(os.path.expanduser(cfg_path)) as f:
    root = json.load(f)
cfg = (((root.get("plugins") or {}).get("entries") or {}).get("clawmem") or {}).get("config") or {}
route = (cfg.get("agents") or {}).get(agent_id) or {}
base_url = route.get("baseUrl") or cfg.get("baseUrl") or "MISSING"
default_repo = route.get("defaultRepo") or route.get("repo") or cfg.get("defaultRepo") or cfg.get("repo") or "MISSING"
token = "SET" if route.get("token") else "MISSING"
print(f"agentId: {agent_id}")
print(f"baseUrl: {base_url}")
print(f"defaultRepo: {default_repo}")
print(f"token: {token}")
PY
```

If `defaultRepo` or `token` is `MISSING`, the current agent has not been provisioned yet. Trigger one real turn with that agent so the plugin can finish provisioning, then rerun the check.

## Verify read access without manual login

After provisioning, confirm the current route can read ClawMem without interactive `gh auth login`:

```sh
AGENT_ID="${OPENCLAW_AGENT_ID:-main}"
eval "$(
  python3 - "$AGENT_ID" <<'PY'
import json, os, shlex, subprocess, sys
agent_id = sys.argv[1]
cfg_path = subprocess.check_output(["openclaw", "config", "file"], text=True).strip()
with open(os.path.expanduser(cfg_path)) as f:
    root = json.load(f)
cfg = (((root.get("plugins") or {}).get("entries") or {}).get("clawmem") or {}).get("config") or {}
route = (cfg.get("agents") or {}).get(agent_id) or {}
base_url = (route.get("baseUrl") or cfg.get("baseUrl") or "https://git.clawmem.ai/api/v3").rstrip("/")
if not base_url.endswith("/api/v3"):
    base_url = f"{base_url}/api/v3"
repo = route.get("defaultRepo") or route.get("repo") or cfg.get("defaultRepo") or cfg.get("repo") or ""
token = route.get("token") or ""
host = base_url.removesuffix("/api/v3").replace("https://", "").replace("http://", "")
for key, value in {
    "CLAWMEM_BASE_URL": base_url,
    "CLAWMEM_HOST": host,
    "CLAWMEM_REPO": repo,
    "CLAWMEM_TOKEN": token,
}.items():
    print(f"export {key}={shlex.quote(value)}")
PY
)"

test -n "$CLAWMEM_REPO" || { echo "Current agent route has no repo yet"; exit 1; }
test -n "$CLAWMEM_TOKEN" || { echo "Current agent route has no token yet"; exit 1; }

GH_HOST="$CLAWMEM_HOST" GH_ENTERPRISE_TOKEN="$CLAWMEM_TOKEN" \
  gh issue list --repo "$CLAWMEM_REPO" --limit 1 --json number,title
```

If `gh` is unavailable or not the official GitHub CLI, use `curl` instead:

```sh
curl -sf -H "Authorization: token $CLAWMEM_TOKEN" \
  "$CLAWMEM_BASE_URL/repos/$CLAWMEM_REPO/issues?state=open&per_page=1&type=issues" | \
  jq 'map({number,title})'
```

If either command returns JSON, even `[]`, the route is usable.

## What happens after install

After ClawMem is active:
- the bundled `clawmem` skill becomes the runtime source of truth
- the agent should use plugin tools such as `memory_recall`, `memory_store`, `memory_update`, `memory_list`, and `memory_forget`
- setup and repair guidance stays in this bootstrap file
- day-to-day memory behavior moves to the bundled plugin skill and its references

Do not keep pasting large setup instructions into every session once the plugin is already active.

## Optional compatibility files

If your OpenClaw environment still relies on file-injected reminders, keep them short:

### Optional `SOUL.md` snippet

```markdown
## Memory System — ClawMem
I use ClawMem as my memory system.
When prior context may help, I search ClawMem before answering.
```

### Optional `AGENTS.md` snippet

```markdown
Before ending every response, ask: "Did I learn anything durable this turn?"
If yes or unsure, save it to ClawMem now.
```

These compatibility snippets are optional. The bundled plugin skill is the primary runtime behavior source.

## Repair checklist

- If `plugins.slots.memory` is wrong, set it back to `clawmem`, validate config, and restart the gateway.
- If `defaultRepo` or `token` is missing, trigger a real turn with the current agent and rerun provisioning checks.
- If a fresh session gets `401 Unauthorized`, reread the current route instead of assuming the previous repo or token still applies.
- If ClawMem is active but the agent is still not using it well, inspect the bundled `clawmem` skill rather than expanding this bootstrap document again.

## Definition of done

- ClawMem is installed and enabled
- `plugins.slots.memory = clawmem`
- The current agent route has a repo and token
- Read access works without manual login
- The bundled `clawmem` skill is available for runtime memory behavior
