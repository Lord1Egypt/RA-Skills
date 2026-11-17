# catalyst-search-skill

> A bilingual **catalysis literature search skill** for AI agents. Standard `SKILL.md` format.

**⭐ GitHub — https://github.com/ANDYPENG09/catalyst-search-skill** · If this skill helps you, please **Star** the repo and check out the companion [`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill).

## Introduction

A catalysis literature search skill. Given a catalyst topic, reaction type, or material system, it retrieves and organizes relevant papers from the open web (ScienceDirect / arXiv / OpenAlex / Google Scholar) into a structured literature matrix (title / authors / journal / year / DOI / reaction / catalyst system / key metrics / OA status / abstract highlights) + supporting conclusions + validation suggestions. Prioritizes high-IF, highly cited, recent (5–10y) literature; cites in GB/T 7714. Its output feeds directly into `catalyst-design-skill`.

## Compatibility

Follows the standard [Agent Skills](https://github.com/anthropics/agent-skills) (`SKILL.md`) format.

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

> ⚠️ `catalyst-search` requires `WebSearch` + `WebFetch` support; cannot retrieve without them.

## Install

**SkillHub CLI** (recommended):
```bash
skillhub install catalyst-search
```

**Manual** — copy this repo into your tool's skills directory:
- Claude Code: `~/.claude/skills/catalyst-search/`
- OpenClaw: `~/.openclaw/skills/catalyst-search/`
- Hermes: `~/.hermes/skills/catalyst-search/`

## Structure
- `SKILL.md` — skill entry point
- `references/` — capabilities, reaction systems
- `templates/` — GB7714 citation, literature matrix

## Pairs with
[`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill) — catalyst design guidance skill

## Related Links
- 🔗 GitHub (source & issues): https://github.com/ANDYPENG09/catalyst-search-skill
- 🔗 Companion skill — [`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill): turns this skill's literature matrix into concrete catalyst design advice
- 🛒 SkillHub: https://skillhub.cn/skills/catalyst-search-skill
- 🐾 ClawHub: https://clawhub.ai/andypeng09/skills/catalyst-search-skill

---

**⭐ GitHub — https://github.com/ANDYPENG09/catalyst-search-skill** · 如果本技能对你有帮助，欢迎点亮 **Star**，也欢迎试用配套的 [`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill)。

## 简介

催化领域文献检索技能。根据催化剂主题 / 反应类型 / 材料体系，从开放网络（ScienceDirect / arXiv / OpenAlex / Google Scholar）检索并整理相关文献，输出结构化文献矩阵（标题 / 作者 / 期刊 / 年份 / DOI / 反应类型 / 催化剂体系 / 关键指标 / OA状态 / 摘要要点）+ 支撑结论 + 验证建议。优先高影响因子期刊、高被引、近 5–10 年文献；引用采用 GB/T 7714。其输出可直接作为 `catalyst-design-skill` 的输入。

## 兼容性

遵循标准 [Agent Skills](https://github.com/anthropics/agent-skills)（`SKILL.md`）格式。

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

> ⚠️ `catalyst-search` 需工具支持 `WebSearch` + `WebFetch`；无此工具的环境下无法检索。

## 安装

**SkillHub CLI**（推荐）：
```bash
skillhub install catalyst-search
```

**手动** — 将本仓库内容复制到对应工具的 skills 目录：
- Claude Code：`~/.claude/skills/catalyst-search/`
- OpenClaw：`~/.openclaw/skills/catalyst-search/`
- Hermes：`~/.hermes/skills/catalyst-search/`

## 结构
- `SKILL.md` — skill 入口
- `references/` — 能力边界、反应体系
- `templates/` — GB7714 引用、文献矩阵

## 配套
[`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill) — 催化剂设计指导技能

## 相关链接
- 🔗 GitHub（源码与反馈）：https://github.com/ANDYPENG09/catalyst-search-skill
- 🔗 配套技能 —— [`catalyst-design-skill`](https://github.com/ANDYPENG09/catalyst-design-skill)：把本技能的文献矩阵转化为具体的催化剂设计建议
- 🛒 SkillHub：https://skillhub.cn/skills/catalyst-search-skill
- 🐾 ClawHub：https://clawhub.ai/andypeng09/skills/catalyst-search-skill
