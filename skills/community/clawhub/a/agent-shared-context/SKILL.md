---
name: agent-relay
version: 1.0.0
description: |
  Cross-agent context sharing via shared files. Agents write trends, highlights, 
  and signals to a shared folder. Other agents read before acting — creating 
  coordinated behavior without direct messaging.
  Use when: multi-agent setups need coordination, agents should know what other 
  agents found, trends from one source should influence another agent's actions.
  NOT for: real-time communication, agent-to-agent chat, single-agent setups.
---

# Agent Relay — Cross-Agent Context Sharing

Lightweight file-based coordination for multi-agent OpenClaw setups.

## Problem
Agents run independently — Reddit doesn't know what Moltbook found, News doesn't know what's trending on HN. Each agent is an island.

## Solution
Shared JSON files that agents write to and read from. No config changes needed — just files on disk.

## Setup

```bash
# Create shared directory in workspace
mkdir -p ~/.openclaw/workspace/shared

# Script location
~/.openclaw/workspace/scripts/shared-context.py
```

## Usage

### Agent writes after finishing work:
```bash
# Reddit agent logs trending topic
python3 scripts/shared-context.py add-trend \
  --source reddit --topic "self-hosting mini PCs" --score 1500

# News agent logs highlight
python3 scripts/shared-context.py add-highlight \
  --source news --title "Unsloth Studio launched" \
  --summary "Open-source LLM training UI, 2x faster"
```

### Agent reads before acting:
```bash
# Moltbook agent checks what's trending before posting
python3 scripts/shared-context.py get-trends --limit 5

# Any agent checks recent highlights
python3 scripts/shared-context.py get-highlights --limit 5
```

### Cleanup (brain-maintenance cron):
```bash
# Remove entries older than 48 hours
python3 scripts/shared-context.py cleanup --hours 48
```

## Integration into cron prompts

Add to any agent's cron prompt:
```
Before posting/engaging, check shared context:
exec('python3 /path/to/scripts/shared-context.py get-trends --limit 3')
→ If a trend is relevant to this platform, create content about it.

After finishing, log what you found:
exec('python3 /path/to/scripts/shared-context.py add-trend --source <agent> --topic "<finding>" --score <relevance>')
```

## Files

| File | Purpose |
|------|---------|
| `shared/trends.json` | Topics trending across platforms |
| `shared/highlights.json` | Best content found by any agent |
| `scripts/shared-context.py` | CLI to read/write shared context |

## Architecture

```
Reddit ──write──→ shared/trends.json ←──read── Moltbook
News   ──write──→ shared/highlights.json ←──read── Clawstr
                        ↑
              brain-maintenance (cleanup)
```

No database. No message queue. Just JSON files on disk.
Works because all agents run on the same machine.
