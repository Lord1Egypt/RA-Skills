---
name: agent-create-config
description: |
  创建 OpenClaw 专属员工 Agent 的完整配置流程。
  融合「one-person-company」和「agentgener」两个技能，支持从需求收集到 Agent 上线的完整闭环。
  当用户需要创建新 Agent、创建新的机器人、制作一个新 Agent 时触发。
---

# Agent 新建配置 - 完整流程

## 概述

本技能是「一人公司 Agent 创建」与「OpenClaw Agent 绑定配置」的融合体，提供从需求收集到 Agent 正式上线的完整流程。

## 完整流程（7 阶段）

详见：`references/MERGED_PROCESS.md`

### 阶段速览

| 阶段 | 内容 |
|------|------|
| 1 | 收集需求（名称/模型/API/Skill/飞书绑定） |
| 2 | 创建工作区 `workspace-{name}/` |
| 3 | 生成所有配置文件 |
| 4 | 注册 Agent 到 `openclaw.json` |
| 5 | 绑定飞书/多账号 + `bindings` 路由 |
| 6 | 重启生效 + 日志验证 |
| 7 | 交付确认 |

## 快速使用

当用户说"创建一个 xxx Agent"时：

1. 阅读 `references/MERGED_PROCESS.md` 获取完整流程
2. 按阶段一问用户收集信息
3. 将创建任务分配给 coder agent 执行

## 核心原则

- CEO 不执行，只协调；创建任务分配给 coder
- 配置文件严格遵守行数限制（SOUL ≤20行，AGENTS ≤80行，MEMORY ≤50行）
- `bindings` 必须放在 openclaw.json 顶层
- 重启后才能生效
