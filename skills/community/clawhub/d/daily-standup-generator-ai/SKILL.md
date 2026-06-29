---
name: Daily Standup Generator
slug: daily-standup-generator
description: >
  基于 Git 提交记录、项目管理工具和团队协作平台数据，自动生成结构化的每日站会报告。
  智能总结昨日进展、今日计划和阻塞项，支持 Slack/飞书/钉钉/Teams 多渠道推送。
version: 1.0.0
author: ai-gaoqian
tags:
  - productivity
  - team-collaboration
  - standup
  - agile
  - automation
metadata:
  openclaw:
    requires: ">=1.0.0"
---

# Daily Standup Generator

## 概述

自动化每日站会报告生成器。从代码仓库、任务管理工具和日历中提取数据，为每个团队成员生成个性化站会发言稿。

## 核心能力

### 1. 智能数据聚合
- Git 提交记录分析（昨日提交、代码量、分支动态）
- 项目管理工具集成（Jira / Linear / Asana / Trello）
- PR/MR 状态追踪（创建、审查、合并）
- CI/CD 流水线状态汇总

### 2. 个人站会报告
- 昨日完成事项（基于实际提交和任务状态变更）
- 今日计划（基于 Sprint Backlog 和活跃分支）
- 阻塞项自动识别（长期未更新任务、CI 失败、PR 待审查超时）
- 支持模板自定义（问题、进展、计划三要素）

### 3. 团队聚合视图
- 全队进展概览仪表板
- Sprint 燃尽图数据更新
- 风险预警（延期任务、冲突依赖）
- 跨团队依赖项追踪

### 4. 多渠道分发
- Slack / Discord 机器人推送
- 飞书 / 钉钉 / 企业微信通知
- Microsoft Teams 集成
- 邮件摘要发送
- Markdown / PDF / HTML 格式导出

### 5. 智能增强
- 自然语言润色（从 commit message 到专业表述）
- 时间估算（基于历史速度预测任务完成时间）
- 情感分析（识别团队状态波动）
- 回顾建议（标记需要讨论的议题）

## 使用方式

```
生成今日站会报告: <团队项目路径>
为成员生成报告: <成员姓名> <项目路径>
推送站会到 Slack: <webhook_url>
```

## 输出格式

- 个人站会脚本（昨日/今日/阻塞 三栏格式）
- 团队汇总看板
- Slack/飞书 Bot 推送消息

## 数据底座

基于 Scrum Guide 2024、Atlassian Agile Handbook、Google re:Work 团队效能研究，覆盖 8 种项目管理工具和 6 个沟通平台的集成方案。

## 定价

¥0.50 / 次生成
