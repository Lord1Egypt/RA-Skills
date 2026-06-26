---
name: agent-usage-stats
description: "选择要监控的 AI 助手 → 查看 token 消耗。支持 Hermes / Claude Code / CodeX / OpenClaw / Reasonix / DeepSeek TUI"
version: 2.7.13
author: zhy
license: MIT
source: https://github.com/zhy/token-stats
clawhub: https://clawhub.ai/zhy/agent-usage-stats
tags:
  - token
  - usage
  - monitoring
  - cross-agent
  - interactive
---

# token-stats — 选个 Agent 看它的消耗

## 核心原则

1. **每次运行都弹菜单** — 你想看哪个 Agent 就选哪个，不预设
2. **数据来自本地** — 不联网，纯读你的 Agent 本地数据文件
3. **零依赖** — 纯 Python 标准库，装完即用

## 前置条件

- Python 3.11+
- 至少一种 Agent 有使用记录：Hermes / Claude Code / CodeX / OpenClaw / Reasonix / DeepSeek TUI
- 安装方式：从 clone 或解压目录运行 `python3 token-stats.py setup`，默认安装到 `~/.token-stats/`
- 更新方式：git clone 用户 `cd ~/token-stats && git pull`，ClawHub 用户 `token-stats update`

## 用法速查

```bash
# 交互式菜单（默认）
token-stats

# 跳过菜单直接看
token-stats -a hermes
token-stats -a claude-code
token-stats -a codex

# 实时监控
token-stats --watch
token-stats -a hermes --watch

# 查看本机装了哪些 Agent
token-stats --list-backends

# 查看版本
token-stats --version
```

## Hermes 集成

Hermes 的 SKILL.md 里可以这样用：

```yaml
run: token-stats -a hermes
```

这样每次任务结束会自动输出 Hermes 的 token 消耗，不弹菜单。

## 数据源说明

| Agent | 数据读哪里 |
|-------|-----------|
| Hermes | `~/.hermes/state.db` → sessions 表 |
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` + `~/.codex/sessions/**/*.jsonl` |
| OpenClaw | `~/.openclaw/agents/main/sessions/` |
