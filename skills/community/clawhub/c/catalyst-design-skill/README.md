# catalyst-design-skill

> A bilingual **catalyst design guidance skill** for AI agents. Standard `SKILL.md` format, no script dependencies.

**⭐ GitHub — https://github.com/ANDYPENG09/catalyst-design-skill** · If this skill helps you, please **Star** the repo and check out the companion [`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill).

## Introduction

A catalyst design guidance skill built on a layered, traceable, dynamically evolving methodology system. It advises on catalyst composition selection, structural design, synthesis strategy, and performance optimization. Covers HER / OER / ORR / PEMWE electrocatalysis. Each advice item carries a source tag (literature-confirmed vs empirical) and confidence, with an actionable validation path. Runs standalone or pairs with `catalyst-search-skill` — consuming its literature matrix for sharper targeting.

## Compatibility

Follows the standard [Agent Skills](https://github.com/anthropics/agent-skills) (`SKILL.md`) format with no script dependencies.

| Tool | Status | Note |
|---|---|---|
| Claude Code | ✅ | Native; `~/.claude/skills/` |
| Cursor | ✅ | `~/.cursor/skills/` |
| OpenClaw | ✅ | `~/.openclaw/skills/` |
| Hermes (Nous Research) | ✅ | `~/.hermes/skills/`; interop with OpenClaw |
| WorkBuddy | ✅ | SkillHub ecosystem |
| QClaw | ✅ | OpenClaw framework |
| ima | ✅ | Knowledge hub |
| Codex (OpenAI) | ⚠️ | Non-native; adapt via AGENTS.md |

> ✅ `catalyst-design` has no tool dependencies; works in all the above.

## Install

**SkillHub CLI** (recommended):
```bash
skillhub install catalyst-design
```

**Manual** — copy this repo into your tool's skills directory:
- Claude Code: `~/.claude/skills/catalyst-design/`
- OpenClaw: `~/.openclaw/skills/catalyst-design/`
- Hermes: `~/.hermes/skills/catalyst-design/`

## Structure
- `SKILL.md` — skill entry point
- `references/` — design methodology, traceability registry, update protocol
- `templates/` — design proposal template

## Pairs with
[`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill) — catalysis literature search skill

## Related Links
- 🔗 GitHub (source & issues): https://github.com/ANDYPENG09/catalyst-design-skill
- 🔗 Companion skill — [`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill): catalysis literature search → structured matrix feeding this skill
- 🛒 SkillHub: https://skillhub.cn/skills/catalyst-design-skill
- 🐾 ClawHub: https://clawhub.ai/andypeng09/skills/catalyst-design-skill

---

**⭐ GitHub — https://github.com/ANDYPENG09/catalyst-design-skill** · 如果本技能对你有帮助，欢迎点亮 **Star**，也欢迎试用配套的 [`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill)。

## 简介

催化剂设计指导技能。基于分层、可追溯、可动态演进的方法论体系，为催化剂组分选择、结构设计、合成策略与性能优化提供建议。覆盖 HER / OER / ORR / PEMWE 等电催化反应；每条建议标注来源（文献已证实 / 经验推测）与置信度，并附可执行验证路径。可独立运行，也可与 `catalyst-search-skill` 协作——消费其文献矩阵以增强针对性。

## 兼容性

遵循标准 [Agent Skills](https://github.com/anthropics/agent-skills)（`SKILL.md`）格式，无脚本依赖。

| 工具 | 状态 | 说明 |
|---|---|---|
| Claude Code | ✅ | 原生支持；`~/.claude/skills/` |
| Cursor | ✅ | `~/.cursor/skills/` |
| OpenClaw | ✅ | `~/.openclaw/skills/` |
| Hermes (Nous Research) | ✅ | `~/.hermes/skills/`；与 OpenClaw 互通 |
| WorkBuddy | ✅ | SkillHub 生态 |
| QClaw | ✅ | OpenClaw 框架 |
| ima | ✅ | 知识号发布 |
| Codex (OpenAI) | ⚠️ | 非原生；需经 AGENTS.md 适配 |

> ✅ `catalyst-design` 无工具依赖，以上工具均可用。

## 安装

**SkillHub CLI**（推荐）：
```bash
skillhub install catalyst-design
```

**手动** — 将本仓库内容复制到对应工具的 skills 目录：
- Claude Code：`~/.claude/skills/catalyst-design/`
- OpenClaw：`~/.openclaw/skills/catalyst-design/`
- Hermes：`~/.hermes/skills/catalyst-design/`

## 结构
- `SKILL.md` — skill 入口
- `references/` — 设计方法论体系、可追溯台账、更新协议
- `templates/` — 设计建议书模板

## 配套
[`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill) — 催化文献检索技能

## 相关链接
- 🔗 GitHub（源码与反馈）：https://github.com/ANDYPENG09/catalyst-design-skill
- 🔗 配套技能 —— [`catalyst-search-skill`](https://github.com/ANDYPENG09/catalyst-search-skill)：催化文献检索，输出结构化矩阵供本技能消费
- 🛒 SkillHub：https://skillhub.cn/skills/catalyst-design-skill
- 🐾 ClawHub：https://clawhub.ai/andypeng09/skills/catalyst-design-skill
