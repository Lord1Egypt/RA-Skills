---
name: calling-agent-squad
version: 1.0.0
description: Activate a multi-agent team (the Squad) to manage complex projects, business tasks, or development workflows. The squad includes a Manager, Architect, Coder, Reviewer, and Observer. Use when the user wants to "call a squad", "start a project", or "deploy squad" with specialized roles and quality control loops.
tags: [multi-agent, squad, workflow, project-management]
author: Megan
---

# Calling Agent Squad

This skill coordinates a specialized team of agents to handle your tasks with professional rigor.

## 🎯 Usage

### Mode 1: Standard (Default)
```
calling squad [project] [task details]
```
- I act as all roles (Manager, Researcher, Architect, Copywriter, Reviewer, Observer)
- **Before each role**: I read their SOUL.md and IDENTITY.md to adopt their persona
- After task completion: I return to my normal self (Megan)
- Like playing a script - put on the mask, do the job, take it off

### Mode 2: Full (Spawn Real Sub-Agents)
```
calling squad full [project] [task details]
```
- Spawns real sub-agents via `openclaw agent`
- Each agent runs in its own workspace with its own SOUL.md/IDENTITY.md
- Slower but more professional - agents work independently
- Suitable for complex tasks requiring specialized expertise

---

## How It Works

### Standard Mode
When user says `calling squad [project] [task]`:
1. Create project folder: `Documents/squad_projects/[project]_[yyyymmdd]/`
2. For each role (Researcher → Architect → Copywriter → Reviewer → Observer):
   - Read that role's `SOUL.md` and `IDENTITY.md` from `agents/[role]/`
   - Adopt their persona and complete their task
3. Save all deliverables to project folder
4. Return to normal (Megan) after completion

### Full Mode
When user says `calling squad full [project] [task]`:
1. Run: `openclaw agent --agent squad-manager -m "Mission: [project] - [task]"`
2. Squad-manager spawns sub-agents with their own workspaces
3. Each agent reads its own SOUL.md/IDENTITY.md
4. Results saved to project folder

---

## ⚠️ Important Notes

- **Standard mode**: I read SOUL/IDENTITY for each role, then return to Megan after - no memory contamination
- **Full mode**: Sub-agents have separate context windows, completely isolated
- **Cost**: Standard uses ~same tokens as normal; Full uses more (multiple agent sessions)

---

## 🛠️ Maintenance

To re-initialize agents (for Full mode):
```bash
bash ~/.openclaw/workspace/skills/calling-agent-squad/squad-init.sh
```

---

## Folder Structure

**Root**: `~/.openclaw/workspace/skills/calling-agent-squad/agents/`

| Agent | Config Folder |
|-------|---------------|
| 🦞 Manager | `agents/squad-manager/` |
| 📐 Architect | `agents/architect/` |
| 🔍 Researcher | `agents/researcher/` |
| ✍️ Copywriter | `agents/copywriter/` |
| 🛠️ Coder | `agents/coder/` |
| 🛡️ Reviewers | `agents/code-reviewer/`, `agents/brand-reviewer/` |
| 📋 Observer | `agents/observer/` |

Each folder contains: SOUL.md, IDENTITY.md, TOOLS.md, USER.md

---

## Project Output

All projects saved to: `Documents/squad_projects/[project]_[yyyymmdd]/`

---

## The Team

- **Squad Manager**: Orchestrates, delegates, and arbitrates
- **Architect**: Plans system blueprints and maintains handbook
- **Researcher**: Gathers market and technical intelligence (facts first, deep insights)
- **Copywriter**: Creates marketing and technical copy
- **Code Reviewer**: Audits for security and logic errors
- **Brand Reviewer**: Ensures brand consistency
- **Observer**: Logs mission and extracts new rules
