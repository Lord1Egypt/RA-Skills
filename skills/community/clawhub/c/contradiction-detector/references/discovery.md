# Step 1 — Discovery

Thorough discovery is the foundation of a reliable audit. Missing even one instruction source means contradictions slip through undetected.

## 1.1 — Enumerate all agents

```bash
# Primary: use OpenClaw CLI
openclaw agents list 2>/dev/null

# Fallback: scan workspace for agent directories (any dir with AGENTS.md)
find /opt/ocana/openclaw/workspace -maxdepth 2 -name "AGENTS.md" -exec dirname {} \; | sort

# Also check openclaw.json for registered agents
cat /opt/ocana/openclaw/openclaw.json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
for a in d.get('agents', {}).get('list', []):
    print(f\"{a.get('id', '?'):20s} → {a.get('workspace', '?')}\")
" 2>/dev/null
```

## 1.2 — Collect instruction files per agent

For EACH agent workspace, check for ALL of these files:

| File | Role | Priority |
|------|------|----------|
| `AGENTS.md` | Behavioral rules, tool usage, communication rules | High |
| `SOUL.md` | Persona, tone, identity, custom instructions | Medium |
| `HEARTBEAT.md` | Periodic task instructions | High (for periodic behavior) |
| `MEMORY.md` | Accumulated context, decisions, facts | Medium |
| `IDENTITY.md` | Name, emoji, avatar | Low |
| `USER.md` | User preferences, timezone, style | Low |
| `TOOLS.md` | Environment-specific tool notes | Low |
| `BOOTSTRAP.md` | First-run instructions | Low |

```bash
WORKSPACE="/opt/ocana/openclaw/workspace"
for agent_dir in "$WORKSPACE" $(find "$WORKSPACE" -maxdepth 2 -name "AGENTS.md" -exec dirname {} \; | grep -v "^$WORKSPACE$"); do
  echo "=== $(basename $agent_dir) ==="
  for f in AGENTS.md SOUL.md HEARTBEAT.md MEMORY.md IDENTITY.md USER.md TOOLS.md BOOTSTRAP.md; do
    [ -f "$agent_dir/$f" ] && echo "  ✓ $f ($(wc -l < "$agent_dir/$f") lines)" || echo "  ✗ $f"
  done
done
```

## 1.3 — Collect skill files

Skills inject instructions when triggered. They can contradict agent-level files:

```bash
# Workspace-level skills
find /opt/ocana/openclaw/workspace/skills -name "SKILL.md" 2>/dev/null | while read f; do
  skill_name=$(grep -m1 '^name:' "$f" | sed 's/name: *//' | tr -d '"')
  echo "  Skill: ${skill_name:-$(dirname $f | xargs basename)} → $f"
done

# System-level skills
find /usr/lib/node_modules/openclaw/skills -name "SKILL.md" 2>/dev/null | while read f; do
  skill_name=$(grep -m1 '^name:' "$f" | sed 's/name: *//' | tr -d '"')
  echo "  System: ${skill_name:-$(dirname $f | xargs basename)} → $f"
done
```

## 1.4 — Collect cron jobs and their payloads

Cron jobs are the #1 source of contradictions because they contain inline prompts that override HEARTBEAT.md at runtime:

```bash
# List all cron jobs
openclaw cron list --json 2>/dev/null || openclaw cron list

# Extract from openclaw.json
cat /opt/ocana/openclaw/openclaw.json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
for i, j in enumerate(d.get('cron', [])):
    agent = j.get('agent', 'main')
    schedule = j.get('schedule', '?')
    prompt = j.get('prompt', j.get('payload', ''))[:200]
    print(f'Cron {i}: agent={agent} schedule={schedule}')
    print(f'  Prompt: {prompt}...' if len(prompt) >= 200 else f'  Prompt: {prompt}')
" 2>/dev/null
```

**Critical**: For each cron job, record:
- Target agent ID
- Whether it has an inline prompt (most do)
- Full text of the inline prompt
- Whether the prompt says "follow HEARTBEAT.md" or contains its own instructions

## 1.5 — Collect hook scripts

Hooks fire on events and can modify agent state. Check for conflicts with agent instructions:

```bash
find /opt/ocana/openclaw/workspace/hooks -type f -name "*.js" -o -name "*.sh" -o -name "*.md" 2>/dev/null | sort
```

## 1.6 — Build the file inventory

Create a mental map (or scratch file) of every instruction source per agent:

```
Agent: <id>
  AGENTS.md: <path> (<lines> lines)
  SOUL.md: <path> (<lines> lines)
  HEARTBEAT.md: <path> (<lines> lines)
  Cron jobs: <count> (inline prompts: yes/no)
  Skills: <list of skill names>
  Hooks: <list of hook names>
```

Only proceed to Step 2 when the inventory is complete.
