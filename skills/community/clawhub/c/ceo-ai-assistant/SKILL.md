---
name: CEO决策助手 v2.8
slug: ceo-ai-assistant
version: 2.8.0
description: 专为中国CEO打造的AI决策协作体系。主脑+子代理架构，支持飞书通知，定时简报，记忆系统，决策分级管理。5分钟安装，开箱即用。
author: 帅哥
homepage: https://clawhub.ai
license: MIT
---

# CEO决策助手 v2.8

专为中国CEO打造的AI决策协作体系，融合龙虾2.0架构。

## 核心功能

- 🧠 **主脑+子代理架构** - 协调者而非执行者，分工明确
- 📊 **6大代理矩阵** - main/news/stocks/work/projectmanager/secretary
- ⏰ **6大定时简报** - 早晨/检索/周会/日度/复盘
- 🧬 **记忆系统** - 分层记忆，永久学习，个性化
- 📈 **决策分级** - P0-P3分级处理，清晰高效
- 🔔 **飞书通知** - 实时推送，随时决策

## 快速安装

```bash
# 1. 克隆配置
openclaw configure --template ceo-ai-assistant

# 2. 配置飞书
openclaw config set channels.feishu.accounts.main.appId "你的APP_ID"
openclaw config set channels.feishu.accounts.main.appSecret "你的APP_SECRET"

# 3. 验证安装
openclaw status
```

## 代理职责

| 代理 | 职责 | 模型 |
|------|------|------|
| main | 协调、决策、汇总报告 | MiniMax/Qwen |
| news | 情报收集、趋势判断 | Qwen3.5+ |
| stocks | 行情分析、选股、风控 | Qwen3.5+ |
| work | 任务执行、项目推进 | Qwen3.5+ |
| projectmanager | 项目管理、里程碑 | Qwen3.5+ |
| secretary | 信息整合、决策归档 | Qwen3.5+ |

## 定时任务

| 时间 | 任务 |
|------|------|
| 7:50 | CEO早晨简报 |
| 8:00/18:00 | 超级检索日报 |
| 周一9:00 | 周度部门例会 |
| 21:00 | 日度汇总简报 |
| 20:00 | 知识库自动更新 |
| 周五17:00 | 周度复盘 |

## 决策分级

- **P0** 立即执行（紧急风控/重大机会）
- **P1** 24小时内决策（日度简报标注）
- **P2** 周内决策（周例会讨论）
- **P3** 月度审视（复盘）

## 数据存储

- MEMORY.md - 核心记忆（永久）
- memory/YYYY-MM-DD.md - 每日日志
- memory/knowledge/ - 用户偏好/禁忌/指令模式
- ceo-framework/ - 决策体系框架

## 支持

- 飞书：ou_9d198de9a562c93f8d8559cd0cd10f20
- 文档：见CEO决策协作体系v2.8.md
