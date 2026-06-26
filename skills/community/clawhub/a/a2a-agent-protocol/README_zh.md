---
name: a2a-protocol
license: MIT
---

# a2a-protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

> 当需要构建 A2A 兼容智能体、发布 AgentCard 发现文档、向远程智能体发送任务，
> 或将 Agent2Agent 协议集成到现有智能体框架时使用此技能。

## 解决什么问题

AI 智能体长期处于孤岛状态。即使共享基础设施，也没有标准方式实现：
跨框架发现能力、委托任务、跟踪生命周期或交换结构化数据。

A2A（Agent2Agent）协议是由 Google 与 a2aproject 社区共同维护的开放标准，
解决了智能体互操作性问题。本技能使 AI 智能体具备 A2A 能力，覆盖发现、
任务提交、 streaming 、推送通知和多轮协作场景。

**触发条件：** 当用户想要连接智能体、委托任务、构建 A2A 服务器、
发布 AgentCard，或理解 A2A/MCP 关系时使用。

## 功能特性

- **协议学习** — 完整 A2A 概述、数据模型和操作参考
- **AgentCard 生成** — 构建用于发现的 JSON 身份文档
- **任务操作** — 发送、轮询、stream、订阅远程智能体任务
- **多轮支持** — 跨智能体会话与上下文线程
- **企业级认证** — API Key、Bearer、OAuth2、mTLS 方案指导
- **流式事件** — 实时 TaskStatusUpdateEvent 和 TaskArtifactUpdateEvent 处理

## 快速开始

### 安装

```bash
# 通过 ClawHub
clawhub install a2a-protocol

# 或手动安装
cp -r a2a-protocol/ ~/.openclaw/skills/
```

### 使用方式

```
/a2a-protocol              # 学习 A2A 概念
/a2a-protocol build-card   # 为发现服务生成 AgentCard
/a2a-protocol send-task    # 向远程 A2A 智能体发送任务
/a2a-protocol stream-task  # 从远程智能体实时获取任务更新
/a2a-protocol subscribe-task # 订阅来自远程智能体的推送通知
```

## 目录结构

```
a2a-protocol/
├── SKILL.md                    # 入口点
├── LICENSE                     # MIT 协议
├── README.md                   # 英文说明
├── README_zh.md                # 本文件（中文）
├── CONTRIBUTING.md             # 贡献指南
├── .gitignore
├── references/
│   ├── a2a-overview.md         # 协议概述与核心概念
│   ├── data-model.md           # 核心数据模型
│   ├── operations.md           # 所有 A2A 操作参考
│   └── agent-card-template.md # AgentCard JSON 模式与注解
└── scripts/                   # （预留辅助脚本）
```

## 参考资料

- [A2A 协议规范](https://a2a-protocol.org/latest/specification/)
- [A2A GitHub 仓库](https://github.com/a2aproject/A2A)
- [Python SDK (a2a-sdk)](https://github.com/a2aproject/a2a-python)

## 协议

本项目采用 MIT 协议 — 详见 [LICENSE](LICENSE)。

---

Powered by [MiniMax](https://minimax.io)。