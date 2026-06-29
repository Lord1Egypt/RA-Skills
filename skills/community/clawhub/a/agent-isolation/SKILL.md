---
name: agent-isolation
displayName: agent-isolation · 多 agent 工作区硬隔离
description: >-
  当多个 AI agent 共享同一个运行时底座时，防止互相踩踏工作区。不是靠约定——是写进每个 agent 配置文件里的硬边界规则。每个 agent 有自己的工作区、自己的 memory、自己的 session；唯一共享区是显式声明的公共目录。包含隔离规则模板、越界例外条款、从混乱到隔离的逐步执行指南。
category: productivity
skillType: prompt
tags: [multi-agent, agent-orchestration, workspace, isolation, safety, architecture]
version: 0.1.1
author: cheng
homepage: https://www.botlearn.ai
metadata:
  botlearn:
    emoji: "⚔️"
    category: "AI Agent"
---

# agent-isolation

多 agent 共享基础设施时的硬边界——不是靠约定，是靠写死规则。

## 问题

当两个（或更多）agent 跑在同一台机器上、共享同一个运行时底座，会出现：

- Agent A 读了 Agent B 的 session 文件，上下文污染
- Agent A 改了 Agent B 的配置文件，B 突然挂掉
- 两个 agent 的 cron 互相触发，产生幽灵任务
- 排查问题时不知道"这是谁的锅"

## 解决方案：三个工作区 + 两条死命令

### 三个工作区（目录级隔离）

```
~/agent-a/          ← Agent A 专属工作区
~/.runtime/         ← 共享运行时（引擎层，只在需要管理时碰）
~/agent-b/          ← Agent B 专属项目文件
```

共享面只有一个：声明一个公共目录（如 `~/shared/styles/`），两个 agent 各自写各自的文件，不冲突。

### 两条死命令（写入 AGENT.md）

**Agent A 的 AGENT.md：**

```markdown
## [Workspace Boundary] 工作区边界（硬规则）

- `~/agent-a/` 是你的工作区。
- `~/.runtime/` 和 `~/agent-b/` 是 Agent B 的工作区。
- 不主动操作 Agent B 的工作区——不读、不改、不写。
- 唯一例外：用户明确说"帮 Agent B 查"、"帮 Agent B 改配置"等管理指令。完成任务后立即退出，不逗留。
```

**Agent B 的 AGENT.md：**

```markdown
## 工作区边界（硬规则）

- `~/agent-a/` 是 Agent A 的工作区。没有理由访问它。
- 发现自己在读/写 Agent A 的文件时，立即停止。
- 共享区：`~/shared/styles/`，各写各的文件。
```

## 关键设计决策

**为什么不是"删掉一方"？**

多 agent 环境下，直觉可能是删掉一个来解决冲突。但如果两个 agent 各自有不可替代的价值，删掉一方是逃避问题——隔离才是解决。

**为什么例外条款是"用户明确说"而不是"自动判断"？**

自动判断（"检测到 B 挂了就自动修复"）会导致 agent 主动越界，越界频率失控。只有用户指令才触发越界——这让越界是可审计的。

## 逐步执行

### Step 1 — 确认三个工作区

确认 agent A、agent B、共享运行时的实际目录路径。

### Step 2 — 找出交叉引用

用 grep 搜各个 agent 的配置文件，看是否有引用其他 agent 路径。

### Step 3 — 写入边界规则

在各自的 AGENT.md 中插入上面的边界规则块。

### Step 4 — 声明共享区

如果有需要共享的资源（风格模板等），指定一个显式目录。

### Step 5 — 验证隔离

- Agent A 执行任务 → 确认没有访问 Agent B 的文件
- Agent B 执行任务 → 确认没有访问 Agent A 的文件
- 用户明确指令 → 确认越界后正确退出

## 从混乱到隔离：典型事故

真实场景中常见的踩踏链：

1. Agent A 和 Agent B 的定时任务互相触发，产生幽灵任务
2. Agent A 删了 Agent B 的 session 文件（误以为是临时文件）
3. Agent B 失忆，用户追问"为什么又这样"
4. 排查数天才发现根因是工作区没有边界

**解决不是删掉一方——是硬隔离。**

## 不适用场景

- 单 agent 环境（不需要隔离）
- agent 之间需要频繁直接协作（隔离会阻碍——考虑消息队列而非共享文件）
