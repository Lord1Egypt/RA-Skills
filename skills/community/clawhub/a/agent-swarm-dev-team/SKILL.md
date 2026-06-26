---
name: agent-swarm-dev-team
version: 1.0.0
description: Agent Swarm 一人开发团队 - 编排多个 AI 编码 Agent（Codex + Claude Code）完成开发任务
author: sunnyhot
license: MIT
keywords:
  - agent-swarm
  - multi-agent
  - codex
  - claude-code
  - dev-team
---

# Agent Swarm Dev Team - 一人开发团队

**编排多个 AI 编码 Agent，一人完成开发团队的工作量**

---

## ✨ 核心功能

### 🤖 **多 Agent 编排**
- ✅ Codex Agent（后端逻辑、复杂 Bug）
- ✅ Claude Code Agent（前端、Git 操作）
- ✅ Gemini（UI 设计规范）
- ✅ 自动路由到最合适的模型

### 🌳 **Git Worktree 隔离**
- ✅ 每个 Agent 独立 Worktree
- ✅ 独立分支工作
- ✅ 互不干扰

### 💻 **tmux 会话管理**
- ✅ Agent 运行在 tmux 会话中
- ✅ 支持中途纠偏
- ✅ 无需终止重启

### 🔍 **三模型代码审查**
- ✅ Codex Review（边界情况、逻辑错误）
- ✅ Gemini Code Assist（安全漏洞）
- ✅ Claude Code Review（验证发现）

### ⏰ **Cron 监控循环**
- ✅ 每 10 分钟自动检测 Agent 状态
- ✅ tmux 存活检查
- ✅ PR 和 CI 状态检查
- ✅ 失败自动重生（最多 3 次）

### 🔄 **Ralph Loop V2**
- ✅ 自改进 Prompt 系统
- ✅ 结合业务上下文重写 Prompt
- ✅ 成功模式自动沉淀

---

## 🚀 使用方法

### **1. 初始化配置**

```bash
node scripts/init-swarm.cjs
```

---

### **2. Spawn Agent**

```bash
# Codex Agent
./scripts/run-agent.sh codex "feat/custom-templates" "gpt-5.3-codex"

# Claude Code Agent
./scripts/run-agent.sh claude "fix/billing-bug" "claude-opus-4.5"
```

---

### **3. 监控 Agent**

```bash
./scripts/check-agents.sh
```

---

### **4. 发送指令**

```bash
# 中途纠偏
tmux send-keys -t codex-templates "Stop. Focus on the API layer." Enter
```

---

## 📋 核心架构

```
你（决策者）
 └── Zoe（OpenClaw 编排器，业务上下文）
      ├── Codex Agent 1（feat/custom-templates，tmux: codex-templates）
      ├── Codex Agent 2（fix/billing-bug，tmux: codex-billing）
      ├── Claude Code Agent（feat/ui-refresh，tmux: cc-ui）
      └── Cron 监控脚本（每 10 分钟，check-agents.sh）
           ├── 检查 tmux 会话是否存活
           ├── 通过 gh CLI 检查 PR 和 CI 状态
           └── 失败 → Zoe 重写 Prompt → 重生 Agent
```

---

## 📊 Definition of Done

Agent 必须知道：**PR 创建 ≠ 完成**

- ✅ PR 已创建
- ✅ 分支已同步 main（无合并冲突）
- ✅ CI 通过（lint、类型检查、单元测试、E2E）
- ✅ Codex Review 通过
- ✅ Claude Code Review 通过
- ✅ Gemini Review 通过
- ✅ UI 变更包含截图

---

## 🎯 模型选择指南

| 模型 | 适用场景 | 特点 |
|------|----------|------|
| Codex (gpt-5.3-codex) | 后端逻辑、复杂 Bug、多文件重构 | 慢但深入 |
| Claude Code (claude-opus-4.5) | 前端、Git 操作 | 快速，权限问题更少 |
| Gemini | UI 设计规范 | 生成 HTML/CSS 规范 |

---

## 🔧 配置文件

### `.clawdbot/active-tasks.json`

```json
{
  "id": "feat-custom-templates",
  "tmuxSession": "codex-templates",
  "agent": "codex",
  "description": "Custom email templates for agency customer",
  "repo": "medialyst",
  "worktree": "feat-custom-templates",
  "branch": "feat/custom-templates",
  "startedAt": 1740268800000,
  "status": "running",
  "notifyOnComplete": true
}
```

---

## 🌍 中国用户适配

### **通知渠道**

| 原方案 | 国内替代 |
|--------|----------|
| Telegram | 飞书自定义机器人 |
| Telegram | 钉钉自定义机器人 |
| Telegram | 企业微信应用消息 |

### **监控平台**

| 原方案 | 国内替代 |
|--------|----------|
| Sentry | 阿里云 ARMS |
| Sentry | 腾讯云前端性能监控 |

### **代码托管**

- ✅ GitHub + gh CLI（推荐保留）
- ✅ Gitee（需要修改脚本）

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 多 Agent 编排
- ✅ Git Worktree 隔离
- ✅ tmux 会话管理
- ✅ 三模型代码审查
- ✅ Cron 监控循环
- ✅ Ralph Loop V2

---

**🤖 一人完成开发团队的工作量！**
