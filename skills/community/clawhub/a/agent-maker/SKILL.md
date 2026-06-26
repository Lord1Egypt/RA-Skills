---
name: agent-maker
description: 辅助创建 OpenClaw Agent 的技能。通过对话引导用户描述需求，自动生成新的 Agent 配置文件。
version: 1.0.0
author: squallfire
created_at: 2026-03-17
execution:
  type: shell
  command: ./tools/create-agent.sh
  arguments: "$@"
---

## 🎯 使用说明

当你需要创建一个新的 OpenClaw Agent 时，可以直接 @agent-maker 并描述你的需求。我会引导你完成 Agent 的配置，并生成完整的 Agent 定义文件。

### 触发方式
- @agent-maker 我想创建一个运维助手
- @agent-maker 帮我生成一个客服机器人
- @agent-maker 创建数据分析师 Agent

## 📋 Workflow

### 1. 需求收集
通过多轮对话收集以下信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| Agent 名称 | 英文小写+短横线 | `ops-agent` |
| 角色描述 | 一句话概括 | 资深运维工程师 |
| 核心职责 | 3-5 项主要工作 | 安装部署、安全巡检、木马查杀 |
| 关联 Skill | 需要调用的现有技能 | `deploy-service`, `security-audit` |
| 运行规则 | 触发条件/定时任务 | 每天凌晨2点自动巡检 |
| 输出格式 | 结果返回方式 | Markdown 报告 |

### 2. 生成配置文件
根据收集的信息，在 OpenClaw 的 agents 目录下创建：
~/.openclaw/workspace/agents/{agent_name}/
├── SOUL.md # Agent 核心定义
├── README.md # 使用说明
└── skills/ # 关联 Skill 的软链接


### 3. 注册与反馈
- 生成 Agent 配置文件
- 提示用户重启网关使生效
- 返回使用方式和示例

## 📝 对话模板

### 场景一：创建运维 Agent

用户：@agent-maker 我想创建一个运维助手
Agent Maker：好的，我们来一步步配置这个运维 Agent。

请为这个 Agent 起一个英文名称（小写+短横线）：
用户：ops-agent

用一句话描述它的角色：
用户：资深运维工程师，负责服务器部署和安全维护

它的核心职责有哪些？（每行一项）

用户：每天扫描系统漏洞
用户：发现木马立即隔离
用户：监控系统资源

需要调用哪些现有 Skill？（如没有则留空）
用户：deploy-service, security-audit, malware-kill

是否有特殊运行规则？（如定时任务）
用户：每天凌晨2点自动执行安全巡检

✅ Agent "ops-agent" 创建成功！

配置文件：~/.openclaw/workspace/agents/ops-agent/SOUL.md

关联 Skill：deploy-service, security-audit, malware-kill

使用方式：@ops-agent [你的指令]

请执行 openclaw gateway restart 使新 Agent 生效。



### 场景二：创建客服 Agent
用户：@agent-maker 帮我生成一个客服机器人
Agent Maker：好的，我们来配置客服 Agent。

Agent 名称（英文小写+短横线）：
用户：customer-service

角色描述：
用户：友好耐心的客服助手，解答用户常见问题

核心职责：
用户：回答产品咨询
用户：处理售后问题
用户：引导用户操作

关联 Skill：
用户：search-docs, ticket-system

运行规则：
用户：7x24小时自动响应，复杂问题转人工

✅ Agent "customer-service" 创建成功！



## 🛠️ 高级功能

### 支持模板创建
如果用户想快速创建常见类型的 Agent，可以直接选择模板：
- @agent-maker 用运维模板创建一个 Agent
- @agent-maker 用客服模板

### 支持 Skill 推荐
根据用户描述的职责，自动推荐相关的 Skill：
检测到您需要“安全巡检”功能，推荐安装以下 Skill：

security-audit：基础安全扫描

malware-kill：木马查杀

log-monitor：日志监控




### 支持配置文件预览
生成前可以让用户预览 SOUL.md 内容，确认无误后再保存。

## 📌 输出格式规范

生成的 SOUL.md 文件格式：



---
name: {agent_name}
description: {role_description}
created_at: {timestamp}
---

## 职责
{bullet_points_of_duties}

## 可用 Skill
{list_of_skills}

## 运行规则
{run_rules}

## 使用示例
@{agent_name} [你的指令]