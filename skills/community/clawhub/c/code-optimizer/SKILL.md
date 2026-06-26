---
name: code-optimizer
description: 代码质量自动评估与优化系统 — 基于ML的代码评分、策略选择、自动优化
author: openclaw
slug: code-optimizer
version: 1.0.0
tags: [code-quality, evaluation, ml, optimization, code-review]
homepage: https://clawhub.ai/skills/code-optimizer
---

# 🔧 Code Optimizer — 代码质量自动评估与优化

## 概述

基于机器学习的代码质量自动评估和优化系统。从 15 个标准测试案例、35 个特征维度出发，通过平衡随机森林模型自动评估代码质量并选择最优生成策略。

### 核心能力

| 功能 | 描述 |
|------|------|
| 📊 **代码质量评估** | 35维度特征分析，ML评分模型，综合质量报告 |
| 🎯 **智能策略选择** | 平衡随机森林 + 规则引擎混合架构，自动选择最优代码生成策略 |
| 🔄 **自动反馈闭环** | 评估结果自动记录，持续优化ML模型 |
| 📋 **标准化测试** | 15个标准测试案例覆盖算法、调试、重构、数据结构 |

### 性能指标

| 指标 | 结果 |
|------|------|
| 评分差异 | 0.36 分 (↓96% 相比基线) |
| 不平衡比 | 6:1 (从 36:1 改善) |
| 宏 F1 | 0.410 (↑40%) |
| 处理速度 | 0.006 秒/案例 |
| ML 使用率 | 100% (阈值优化后) |

## 安装

### 前提条件
- Python 3.9+
- scikit-learn 1.0+
- numpy, pandas

### 通过 ClawHub 安装

```bash
clawhub install code-optimizer
```

### 手动安装

```bash
# 克隆或复制到 skills 目录
cd ~/.openclaw/workspace
pip install scikit-learn numpy pandas

# 安装技能
clawhub install code-optimizer
```

## 使用方法

### 评估代码质量

```bash
# 评估单个文件
code-eval evaluate --code-file my_code.py --task "实现功能"

# 评估代码字符串
code-eval evaluate --code "def hello(): pass" --task "Hello World"

# 批量评估
code-eval batch --dir ./code_samples
```

### 运行标准测试

```bash
# 运行所有 15 个标准测试
code-eval test-suite

# 运行指定测试
code-eval test --case CASE_001
```

### 选择生成策略

```bash
# 自动选择最优策略
code-eval select-strategy --code-file my_code.py
# 输出: balanced | emphasize_correctness | extreme_correctness
```

### 生成报告

```bash
# 生成 HTML 报告
code-eval report --format html --output report.html
```

## 配置

### 主配置

```yaml
# config.yaml
evaluator:
  model_path: models/balanced_forest.pkl
  threshold: 0.5
  feature_count: 35

strategies:
  - balanced
  - emphasize_correctness
  - extreme_correctness

integration:
  auto_evaluate: true
  log_results: true
  feedback_loop: true
```

## 与 Hermes 集成

当与 Hermes 记忆系统配合使用时：
1. 自动评估每个代码生成任务
2. 评估结果存入记忆系统
3. ML 数据集持续扩充
4. 策略选择融入任务规划

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-23 | 初始版本：代码评估 + 策略选择 + ML模型 |

## 许可

MIT License
