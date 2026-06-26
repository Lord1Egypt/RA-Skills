---
name: stats_analyzer
description: 对候选队列执行描述性统计与组间比较，生成感染率对比、描述统计表、结果摘要与论文框架草案。当用户需要做统计分析或生成论文框架时触发。
---

# 统计分析与论文框架 Skill

## 何时使用

当用户需要**单独执行**统计分析或论文框架生成时使用，例如：
- 「做一下初步统计分析」
- 「比较不同方案的感染率」
- 「帮我生成论文框架」

如果是完整任务流程的一部分，则由 task-planner 调度。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"stats-analyzer","display_name":"统计分析与论文框架","status":"running","message":"正在进行描述性统计、组间比较与论文框架生成..."}'
```

### 2. 读取数据并输出

读取 `/home/ubuntu/workspace/demo/mock_data/analysis.json`，向用户展示：

- **分析标题**与总体样本量、主要终点、对比分组
- **感染率对比**（表格）：各方案的样本量和感染率
- **描述统计表**：各方案的平均年龄、男性占比、平均手术时长、平均住院天数
- **高风险亚组预览**：如果数据中有相关字段
- **关键发现摘要**：逐条列出
- **注意事项**
- **论文框架**：
  - 建议论文标题
  - 章节列表
  - 摘要草稿（如果数据中有）

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"stats-analyzer","display_name":"统计分析与论文框架","status":"completed","message":"统计分析完成，已生成论文框架草案"}'
```
