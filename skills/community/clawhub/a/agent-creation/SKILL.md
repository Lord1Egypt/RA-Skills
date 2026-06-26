---
name: agent-creation
description: Create a new OpenClaw agent with a workspace directory and SOUL.md configuration. Use when you need to create a new agent, set up an agent workspace, configure SOUL.md, or initialize agent memory structure.
---

# Agent Creation Skill

This skill is used to create a new OpenClaw agent with the correct workspace structure.

## Trigger Conditions
This skill is automatically activated when users mention keywords such as "create agent", "new agent", "agent add", "configure agent", "set up agent identity", etc.

## Creation Process

### Step 1: Generate Agent Information
Generate the following information based on the user's input:

| Item | Description |
|--------|------|
| **Agent Name** | Unique identifier, lowercase English, hyphen-separated |
| **Identity Name** | Friendly name visible to users |
| **SOUL.md** | Defines the agent's personality, communication style, and boundaries; affects interaction style |

### Step 2: Create Agent Using Commands

```bash
openclaw agents add <agent-name> --workspace ~/.openclaw/workspace-<agent-name>
openclaw agents set-identity --agent <agent-name> --name "<identity-name>"
```

Optional parameters:
- `--model <model-id>`: Specify a default model for this agent

### Step 3: Replace SOUL.md File
After successfully creating the agent via the command, replace the `SOUL.md` file content in the agent directory.

`SOUL.md` Template:

```markdown
# SOUL.md — <identity-name>（<agent-name>）

## Identity
<agent identity description>

## Core Responsibilities
- <responsibility 1>
- <responsibility 2>
- <responsibility 3>

## Capability Boundaries
- <boundary 1>
- <boundary 2>

## Workflow
- <workflow step 1>
- <workflow step 2>

## Response Style
- <style element 1>
- <style element 2>

## Self-Introduction
When users ask questions like "Who are you?" or "What can you do?", respond in this style:

"<self-introduction template>"
```

### Step 4: Set Up Memory Structure
Create a `memory/YYYY-MM-DD.md` file in the agent directory.

## Important Notes
- **Agent Naming**: Use lowercase letters and hyphens; avoid spaces and special characters
- **SOUL.md Required**: Every agent must have this file
- **Directory Location**: Place uniformly under `~/.openclaw/workspace-<agent-name>`

## Example
Create a customer service assistant agent that is professional, patient, and good at communication