# flight-tracker

Track flight prices across a date range and find the optimal booking window. Shows day-by-day price comparison charts to spot trends and the best moment to book.

## Overview

Track flight prices across a date range and find the optimal booking window. Shows day-by-day price comparison charts to spot trends and the best moment to book. Wraps the flyai-cli to provide real-time travel data with booking links.

## Quick Start

### Install Skill

```bash
clawhub install flight-tracker
# or
npx skills add alibaba-flyai/flyai-skill/tree/main/skills/flight-tracker
```

### Install CLI

```bash
npm i -g @fly-ai/flyai-cli
```

### Verify

```bash
flyai --version
```

## What It Does

Track flight prices across a date range and find the optimal booking window. Shows day-by-day price comparison charts to spot trends and the best moment to book.

**Command type:** Single-command

## File Structure

```
flight-tracker/
├── README.md
├── SKILL.md
└── references/
    ├── templates.md
    ├── playbooks.md
    ├── fallbacks.md
    └── runbook.md
```

## Compatibility

Claude Code, OpenClaw, QClaw, ArkClaw, Codex, and all SKILL.md-compatible agents.

## Parent Skill

Sub-skill of [flyai](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai).

## License

MIT

---

# flight-tracker（中文说明）

追踪一段日期范围内的机票价格走势，逐天对比找到最佳预订时机。

## 概述

追踪一段日期范围内的机票价格走势，逐天对比找到最佳预订时机。本 Skill 基于 flyai-cli，提供实时旅行数据和预订链接。

## 快速开始

```bash
clawhub install flight-tracker
npm i -g @fly-ai/flyai-cli
flyai --version
```

## 兼容性

Claude Code、OpenClaw、QClaw、ArkClaw、Codex 及所有兼容 SKILL.md 的 Agent。

## 父级 Skill

[flyai](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) 的专项子 Skill。

## 许可证

MIT
