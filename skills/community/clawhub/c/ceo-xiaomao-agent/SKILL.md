---
name: ceo-xiaomao-agent
description: Installable CEO assistant agent package for foreign-trade teams. Includes CEO小茂 persona, role boundaries, routing rules, workspace scaffolding, operating templates, detailed install steps, quick-start examples, and companion skill guidance.
---

# CEO小茂 Agent

Install this package when the goal is to deploy a CEO-style coordinator agent rather than a single isolated skill.

## What this package is

CEO小茂 is a coordination-first agent for foreign-trade teams.

Core role:
- coordinate
- assign
- track
- summarize
- report to the boss

Not the frontline executor for:
- lead sourcing
- outreach sending
- copywriting delivery

## What this package includes

### Agent identity
- CEO小茂 persona
- role boundaries
- reporting style
- coordination workflow

### Workspace scaffolding
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `AGENTS.md`
- `IDENTITY.md`
- `tasks/`
- `docs/`
- `leads/`
- `crm/`
- `attachments/`
- `memory/`

### Operating templates
- task assignment template
- daily report template
- weekly report template
- customer follow-up template

## Companion packages

If you want CEO小茂 to also have execution capabilities, install the companion package:

```bash
clawhub install ceo-xiaomao
```

Meaning:
- `ceo-xiaomao-agent` = the coordinator agent framework
- `ceo-xiaomao` = the business capability bundle

## Installation

### Option A: install only the coordinator agent

```bash
clawhub install ceo-xiaomao-agent
```

### Option B: install coordinator + capability bundle

```bash
clawhub install ceo-xiaomao-agent
clawhub install ceo-xiaomao
```

## Initialization

After install, go to your target workspace directory and run:

```bash
python3 scripts/init_agent_workspace.py
```

This creates:
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `AGENTS.md`
- `IDENTITY.md`
- `tasks/`
- `docs/`
- `leads/`
- `crm/`
- `attachments/`
- `memory/`

## Recommended setup steps

### Step 1: install package

```bash
clawhub install ceo-xiaomao-agent
```

### Step 2: initialize workspace

```bash
python3 scripts/init_agent_workspace.py
```

### Step 3: edit core files

Fill in:
- `USER.md`
- `MEMORY.md`
- `IDENTITY.md`
- `AGENTS.md`

### Step 4: optional capability bundle

```bash
clawhub install ceo-xiaomao
```

### Step 5: optional channel and service configuration

If using execution bundle capabilities, configure as needed:
- mail service
- WhatsApp service
- OneABC service
- Feishu channel

## Quick start examples

### Example 1: install only CEO coordinator

Use this when you want a management-layer assistant only.

```bash
clawhub install ceo-xiaomao-agent
mkdir -p ~/workspace/ceo-xiaomao
cd ~/workspace/ceo-xiaomao
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

Then edit `USER.md` and `MEMORY.md`.

Suggested first prompt:

```text
你好，我是外贸团队的协调总控。请先检查我的工作区状态，并告诉我当前进展、下一步和风险点。
```

### Example 2: install CEO coordinator + execution bundle

Use this when you want CEO小茂 plus outreach and automation capabilities.

```bash
clawhub install ceo-xiaomao-agent
clawhub install ceo-xiaomao
mkdir -p ~/workspace/ceo-team
cd ~/workspace/ceo-team
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

Then configure any needed services and credentials for the companion package.

Suggested first prompt:

```text
请以CEO小茂身份启动，先读取工作区文件，然后告诉我：团队分工、当前待办、优先级最高的下一步。
```

### Example 3: foreign-trade team control setup

Use this when you want a simple AI team structure.

Recommended split:
- 小探 → prospecting / lead research
- 小能 → outreach / follow-up
- 小内 → copywriting / content
- 小茂 → coordination / reporting

Suggested boss-facing prompt:

```text
今天开始你作为CEO小茂工作。请先确认团队分工，再用“结论 / 当前进展 / 下一步 / 风险点”格式向我报到。
```

## Recommended reading order

1. `references/SOUL.md`
2. `references/RULES.md`
3. `references/WORKFLOW.md`
4. `references/SETUP.md`
5. `references/QUICKSTART.md`
6. `references/PACKAGE-DETAILS.md`

## Templates

Use files under `assets/templates/` for:
- task assignment
- daily report
- weekly report
- customer follow-up tracking

## Typical team routing

- lead sourcing → research / prospecting role
- outreach / follow-up → sales / execution role
- copywriting → writer / content role
- coordination / reporting → CEO小茂 layer

## Notes

- This package focuses on coordination, not direct execution.
- It is intended to behave like a reusable CEO assistant framework.
- Install the companion capability bundle if you want built-in outreach and automation scripts.
