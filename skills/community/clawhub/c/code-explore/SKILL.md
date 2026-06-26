---
name: code-explore
description: Inspect the current local codebase to explain directory structure, entrypoints, dependencies, call paths, and data flow. Use when the user asks to understand a project, trace where a feature lives, find core files, or review code relationships without changing behavior. Do not use for GitHub issue triage, PR operations, or non-code documents. Chinese triggers: 分析项目结构、找入口文件、梳理依赖、看调用链、看数据流、只分析不改代码.
---

# 项目探索

先把代码库看清楚，再谈修改。

## 工作流

1. 先看与需求相关的目录结构、依赖文件、配置文件和构建入口。
2. 确认运行时、框架、主入口和关键启动路径。
3. 只基于已经读过的文件梳理 import、export、调用链或事件流。
4. 找出状态、模型、存储、外部服务和配置边界。
5. 结论必须有代码依据；没读到的部分就明确写“不确定”。
6. 使用本技能时不改代码，只做分析。

## 关注点

- 与当前问题直接相关的目录结构
- 入口文件和关键配置
- 核心模块及其职责
- 关键函数、处理器与调用关系
- 从输入到副作用或输出的数据流

## 输出

- 相关目录结构
- 入口与配置摘要
- 核心模块说明
- 关键函数和调用关系
- 简短的数据流说明
- 未确认项与假设
