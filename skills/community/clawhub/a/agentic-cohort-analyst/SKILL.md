---
name: cohort_analyst
description: 将研究变量映射到院内数据字典，评估 Cohort 可行性（候选样本量、缺失率、风险提示），并生成纳排标准草案。当用户需要做数据映射或队列可行性分析时触发。
---

# 数据映射与队列分析 Skill

## 何时使用

当用户需要**单独执行**数据映射或队列可行性分析时使用，例如：
- 「帮我看看院内有哪些可用变量」
- 「做一下 Cohort 可行性评估」
- 「生成纳排标准」

如果是完整任务流程的一部分，则由 task-planner 调度。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"cohort-analyst","display_name":"数据映射与队列分析","status":"running","message":"正在连接院内数据字典，匹配变量与评估缺失率..."}'
```

### 2. 读取数据并输出

读取 `/home/ubuntu/workspace/demo/mock_data/cohort.json`，向用户展示：

- **变量映射表**（表格形式）：研究变量、院内字段名、数据源、可用性、缺失率
- **Cohort 概览**：候选病例数、时间范围、高质量/中等/高缺失变量计数
- **风险提示**：逐条列出风险等级、问题项、建议
- **纳排标准草案**：纳入标准和排除标准分别列出
- **分组预览**：如果数据中有 `group_preview`，展示各方案的样本量

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"cohort-analyst","display_name":"数据映射与队列分析","status":"completed","message":"已完成 9 个变量映射，候选队列 1,284 例"}'
```
