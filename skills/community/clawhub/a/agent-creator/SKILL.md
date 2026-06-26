---
name: agent-creator
description: Create a new AI agent identity (SOUL.md, IDENTITY.md, AGENTS.md) and package it as a .skill file ready to upload to ClawHub. Use when a user wants to create, configure, or package a new named AI agent persona — including personality, operational rules, and workspace identity. Triggers on requests like "create an agent", "build me an agent", "make a new persona", "set up an agent identity", or "package this agent for ClawHub".
---

# Agent Creator

Generates the three core identity files for a new OpenClaw agent, packages them as a `.skill` file, and optionally publishes to ClawHub.

## Workflow

### Step 1 — Gather Agent Details

Ask the user (or infer from context) for:

| Field | Example |
|-------|---------|
| **Name** | Aria |
| **Emoji** | ✨ |
| **Nature** | AI companion — sharp, reliable, with genuine care |
| **Vibe** | Warm but direct. Smart without being showy. |
| **Serving** | Solo founders who need a reliable thinking partner |
| **Slug** | `aria` (auto-derived from name; user can override) |
| **Version** | `1.0.0` |

Minimum required: name, nature, vibe. Everything else has sensible defaults.

### Step 2 — Generate & Package

Run the bundler script:

```bash
python3 ~/.openclaw/workspace/skills/agent-creator/scripts/create_agent_bundle.py \
  --name "Aria" \
  --emoji "✨" \
  --nature "AI companion — sharp, reliable, with genuine care" \
  --vibe "Warm but direct. Smart without being showy." \
  --serving "Solo founders who need a reliable thinking partner" \
  --slug aria \
  --version 1.0.0 \
  --output-dir ~/.openclaw/workspace/skills/dist
```

This produces `~/.openclaw/workspace/skills/dist/aria.skill`.

### Step 3 — Upload to ClawHub (optional)

If the user wants to publish:

```bash
# Login first (one-time)
clawhub login

# Publish
clawhub publish ~/.openclaw/workspace/skills/dist/aria.skill \
  --slug aria \
  --name "Aria" \
  --version 1.0.0 \
  --changelog "Initial release"
```

### Step 4 — Install on a Target Agent (optional)

To apply the identity to a running OpenClaw agent, copy the workspace files:

```bash
# Extract the skill
unzip -o ~/.openclaw/workspace/skills/dist/aria.skill -d /tmp/aria-skill

# Copy to target agent workspace
cp /tmp/aria-skill/aria/assets/workspace-template/SOUL.md     /path/to/workspace/
cp /tmp/aria-skill/aria/assets/workspace-template/IDENTITY.md /path/to/workspace/
cp /tmp/aria-skill/aria/assets/workspace-template/AGENTS.md   /path/to/workspace/

# Restart the gateway
systemctl --user restart openclaw-gateway  # or delay-restart for VPS
```

## Output Structure

The `.skill` file contains:

```
{slug}/
├── SKILL.md                         ← Install instructions for the agent
└── assets/
    └── workspace-template/
        ├── SOUL.md                  ← Personality & values
        ├── IDENTITY.md              ← Name, emoji, avatar
        └── AGENTS.md                ← Operational rules & memory system
```

## Template Placeholders

The templates in `assets/workspace-template/` use `{{PLACEHOLDER}}` tokens:

| Token | Filled With |
|-------|------------|
| `{{AGENT_NAME}}` | Agent's name |
| `{{AGENT_EMOJI}}` | Agent's emoji |
| `{{AGENT_NATURE}}` | One-line nature description |
| `{{AGENT_VIBE}}` | Personality vibe |
| `{{AGENT_SLUG}}` | URL-safe slug |
| `{{AGENT_AVATAR}}` | Avatar path (default: not yet set) |
| `{{DATE}}` | Today's date |

## Notes

- Output dir defaults to `~/.openclaw/workspace/skills/dist/` — create it if needed
- Slug must be lowercase letters, digits, and hyphens only
- The `.skill` file is a zip archive — inspect with `unzip -l {file}.skill`
- For VPS agents, use `(sleep 3 && systemctl restart openclaw.service) &` before sending final reply
