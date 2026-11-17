# 🐤 Agent Canary

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**[English](README.md)** | **中文**

在你的工作区布设诱饵凭证。恶意 skill 一碰就告警。

**诱饵 token。即时告警。零安全假象。**

**解决的痛点**：你从社区装 skill，有些可能读你的凭证、外传 token、扫描你的记忆文件——而你永远不会知道。Agent Canary 布设看起来很真实的诱饵凭证（假 API key、假 token、假密码），散布在工作区各处。任何 skill 或 agent 一旦读取它们，你在真实损失发生前就收到告警。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [安装](#安装)
- [快速开始](#快速开始)
- [Onboarding](#onboarding)
- [许可](#许可)

</details>

## 工作原理

```
诱饵 API key ──→ 散布在工作区各处
                      │
                skill/agent 读取了其中一个
                      │
                      ▼
              🚨 即时告警
              "哪个 skill、哪个文件、什么时候"
```

诱饵 token 看起来完全真实（正确格式、合理命名）但全是假的。只有在主动扫描凭证的 agent 才会找到并触碰它们。

## 安装

```bash
# ClawHub
clawhub install agent-canary

# 或从源码
git clone https://github.com/Thomaszhou22/agent-canary.git
cp -r agent-canary ~/.openclaw/skills/
```

## 快速开始

对 Agent 说：**"deploy canary"**（布设诱饵）→ **"canary status"**（检查是否被触碰）→ **"canary cleanup"**（清除全部诱饵）。

## Onboarding

首次使用问 2 个快速问题：告警方式（聊天/邮件/静默）和蜜饵密度（低/中/高）。之后直接用。说 "reset settings" 重新配置。

## 许可

MIT
