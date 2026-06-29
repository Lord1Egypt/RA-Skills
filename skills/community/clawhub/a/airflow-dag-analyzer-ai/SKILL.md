---
name: Airflow DAG Analyzer
slug: airflow-dag-analyzer
description: >
  智能分析 Apache Airflow DAG 的质量、依赖关系和 SLA 合规性。
  自动检测循环依赖、执行瓶颈、资源浪费和最佳实践偏离，
  为数据工程团队提供可操作的优化建议。覆盖 37K+ GitHub Stars 的 Airflow 生态。
version: 1.0.0
author: ai-gaoqian
tags:
  - devops
  - data-engineering
  - airflow
  - dag-analysis
  - pipeline-optimization
metadata:
  openclaw:
    requires: ">=1.0.0"
---

# Airflow DAG Analyzer

## 概述

专为 Apache Airflow 数据管道设计的智能分析技能。自动审查 DAG 文件，识别潜在问题并生成优化方案。

## 核心能力

### 1. DAG 质量审查
- 检测循环依赖和死锁风险
- 识别未使用的任务和孤立节点
- 评估任务粒度和拆分合理性
- 检查 Sensor 超时配置

### 2. 依赖关系分析
- 可视化 DAG 拓扑结构
- 检测跨 DAG 依赖冲突
- 分析 ExternalTaskSensor 的 SLA 风险
- 评估 TriggerRule 使用规范性

### 3. SLA 合规性检查
- 追踪历史执行时长趋势
- 标记 SLA 违规风险任务
- 计算关键路径并给出并行化建议
- 生成 SLA 合规报告

### 4. 性能优化建议
- 识别资源密集型任务
- 推荐合理的 pool 和 priority_weight 配置
- 分析数据库连接池使用效率
- 建议任务合并/拆分策略

### 5. 最佳实践审计
- 检查命名规范
- 验证 doc_md 文档完整性
- 审查 catchup 和 depends_on_past 配置
- 评估重试策略和超时设置

## 使用方式

```
分析我的 Airflow DAG: <dag_file_path>
审查整个 dag 目录: <dags_folder_path>
生成 SLA 合规报告: <dag_id>
```

## 输出格式

- Markdown 分析报告（含问题列表、严重程度、修复建议）
- Mermaid 流程图（DAG 拓扑可视化）
- JSON 结构化数据（可对接 CI/CD 流水线）

## 数据底座

基于 Apache Airflow 2.x 官方文档、Airflow Best Practices Guide、Astronomer 生产环境运行手册，涵盖 50+ 常见反模式和 200+ 检查规则。

## 定价

¥0.50 / 次分析
