---
name: eo-quickstart
description: "Everything Openclaw (EO) Quickstart - 5-minute onboarding guide for multi-expert collaboration plugin"
metadata:
  openclaw: {}
---

# EO Quickstart - 新手入门指南

> 🦞⚙️ 让每个 Agent 都穿上机甲 — 5分钟入门多专家协作

## 这是什么？

EO Quickstart 是一个**新手引导 Skill**，帮助你在 5 分钟内完成 Everything Openclaw 插件的配置，并运行第一个多专家协作项目。

**前置要求**：已安装 [Everything Openclaw (EO) 插件](https://clawhub.com/plugins/eo-collaboration)

## 功能

- ✅ 自动检测 EO 插件安装状态
- ✅ 引导配置第一个项目
- ✅ 运行第一个多专家协作任务
- ✅ 常见问题排查

## 快速开始

### 第一步：安装插件

```bash
openclaw plugins install eo-collaboration
# 或
clawhub install eo-collaboration
```

### 第二步：初始化项目

```
请告诉我你想要开发什么类型的项目？

例如：
- "我要开发一个博客系统"
- "我要做一个小程序"
- "我要搭建一个电商后台"
```

### 第三步：体验多专家协作

插件安装后，你可以使用以下命令：

| 命令 | 功能 |
|------|------|
| `eo_plan("项目需求")` | 规划师专家生成项目计划 |
| `eo_architect("系统架构")` | 架构师专家设计技术方案 |
| `eo_code_review("代码")` | 审查专家评审代码 |

## 工作原理

```
你输入任务
    ↓
EO 插件调度
    ↓
多专家并行/串行执行
    ↓
Checkpoint 质量验证
    ↓
输出结果 + 报告
```

## 适用场景

- 不知道从哪里开始用 EO 插件
- 想快速体验多专家协作效果
- 需要一个清晰的项目启动流程

## 依赖插件

本 Skill 基于 **[Everything Openclaw (EO)](https://clawhub.com/plugins/eo-collaboration)** 插件。

安装命令：
```bash
openclaw plugins install eo-collaboration
```

## 限制

- 需要 OpenClaw Agent 环境
- 部分高级功能需要专业模式

---

*🦞⚙️ EO - 让每个 Agent 都穿上机甲*
