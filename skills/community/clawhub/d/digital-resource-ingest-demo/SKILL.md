---
name: digital-resource-ingest-demo
description: 数字资源入库演示技能 - 演示如何通过 TaskFlow 编排业务流程后，将数字内容发布到 ClawHub 资源中心
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      - taskflow
    tags:
      - demo
      - digital-resource
      - workflow
  author: terrycarter1985
  created: "2026-08-25"
  version: "1.0.0"
  license: MIT
---

# 数字资源入库演示技能 v1.0.0

## 概述

本技能是一个实际演示案例，展示从业务流程处理到数字资源入库的完整流程。
它本身既是演示内容，也是流程验证的产物。

## 适用场景

- 需要将知识文档、工具脚本、模板等数字资产系统化管理
- 多步骤工作流需要持久化状态和可追溯性
- 团队协作中需要统一的资源分类和检索机制

## 使用方式

1. 通过 TaskFlow 编排预处理流程（审核、分类、元数据填充）
2. 使用 `clawhub publish` 完成入库
3. 通过 `clawhub search` 验证入库结果

## 元数据规范

本技能遵循数字资源管理实践指南定义的元数据标准：
- 必填：name, description, author, created, version, tags
- 可选：source, license, dependencies, related

## 版本历史

- 1.0.0 (2026-08-25): 初始版本，演示完整入库流程
