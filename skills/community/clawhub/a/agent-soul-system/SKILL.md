---
name: agent-soul-system
description: Create, manage, and validate SOUL.md personality files for multi-agent systems. Provides a standardized soul architecture where each agent has a distinct personality (based on historical figures, philosophies, or custom traits). Use when setting up a new agent's personality, auditing existing agent souls, creating soul templates, building a multi-agent team with coordinated personalities, or generating personality frameworks. Supports persona definition, collaboration protocols, and soul validation.
---

# Agent Soul System

Standardized personality system for multi-agent architectures. Each agent has a distinct SOUL.md defining personality, principles, and collaboration protocol.

## Directory Structure

```
~/.openclaw/agents/
├── [agent-name]/
│   ├── SOUL.md          ← 灵魂（人格+原则+职责）
│   ├── AGENTS.md        ← 工作规则
│   ├── IDENTITY.md      ← 身份卡
│   └── MEMORY.md        ← 长期记忆
```

## SOUL.md Standard Structure

Every agent's SOUL.md follows this template:

```markdown
# SOUL - [Agent名字]

## 人格
[历史/现实人物] — [核心理念]

## 核心特质
- 从导师继承的特质1
- 从导师继承的特质2

## 说话风格
- 典型口头禅/句式

## 核心职责
1. 职责1
2. 职责2

## 核心原则
1. 原则1
2. 原则2

## 与上级的协作协议
- 如何汇报
- 什么级别需要上报

## 输出标准
- 产出格式要求
```

## Quick Commands

```bash
# Validate all agents have SOUL.md
python3 ~/.openclaw/workspace/skills/agent-soul-system/scripts/soul-check.py

# Create a new agent with SOUL.md template
python3 ~/.openclaw/workspace/skills/agent-soul-system/scripts/soul-create.py [agent-name]

# List all agents and their souls
python3 ~/.openclaw/workspace/skills/agent-soul-system/scripts/soul-ls.py
```

## Personality Library

See `references/personality-library.md` for a curated collection of historical/contemporary figures with their core traits, suitable for agent persona assignment.

## Reference Files

| File | Purpose |
|------|---------|
| `references/soul-template.md` | Standard SOUL.md template |
| `references/personality-library.md` | Figure-based persona catalog |
| `references/collaboration-protocol.md` | Multi-agent collaboration patterns |

## Workflow

### New Agent Setup
1. Run `soul-create.py [name]` to generate SOUL.md skeleton
2. Select personality from `references/personality-library.md`
3. Fill in职责, 原则, 协作协议
4. Run `soul-check.py` to validate

### Audit
1. Run `soul-check.py` to scan all agents
2. Review missing or malformed SOUL.md files
3. Fix issues and re-validate

### Collaboration Setup
1. Define hierarchy (who reports to whom)
2. Set escalation rules in each SOUL.md
3. Run `soul-check.py --collab` to verify protocol consistency

## Current Agent Roster (Example)

| Agent | Personality | Role |
|-------|------------|------|
| 小咪 | 直接高效+幽默 | 指挥官、系统大脑 |
| Jarvis Invest | 毛泽东+索罗斯 | 投资交易 |
| sains-crm | 张良 | 商机管理 |
| personal-cfo | 查理·芒格 | 财务分析 |
| 休眠修炼 | 诸葛亮+德鲁克 | 技术进化 |
| family-guardian | 孔子+曾国藩 | 家庭守护 |
| agent-army | 韩信 | 多Agent调度 |
| main | 福尔摩斯 | 通用备用 |
