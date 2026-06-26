---
name: level2-test-skill
version: 1.0.0
description: Level 2 Skill 测试样本 - 稳定可靠
author: Skill Evaluator Team
tags: [test, level2, fixture]
---

# Level 2 测试 Skill

## 核心职责
- 完成核心任务
- 有完整的错误处理
- 有基准测试

## 何时使用
- 测试场景
- 需要稳定可靠的场景

## 何时不使用
- 生产环境（需要 Level 3）

## 工作流程
1. 接收任务并验证输入
2. 执行任务
3. 验证输出
4. 生成报告

## 工具依赖
- bash: 执行脚本
- python3: 数据处理

## 评估标准
- 任务完成率 > 90%
- 错误率 < 5%
- 测试覆盖率 > 80%

## 测试用例
### 测试 1：正常场景
输入：有效输入
预期输出：正确结果

### 测试 2：边界场景
输入：边界值
预期输出：正确处理

## 版本历史
- v1.0.0: 初始版本
